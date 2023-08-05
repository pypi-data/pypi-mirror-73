from typing import List

from concurrent.futures.thread import ThreadPoolExecutor

from provider.limit.command import LimitOptions
from provider.limit.data.allowed_resources import ALLOWED_SERVICES_CODES
from shared.common import (
    ResourceProvider,
    Resource,
    ResourceDigest,
    message_handler,
    ResourceCache,
    LimitsValues,
)
from shared.common_aws import get_paginator
from shared.error_handler import exception

SERVICEQUOTA_TO_BOTO3 = {
    "elasticloadbalancing": "elbv2",
    "elasticfilesystem": "efs",
    "vpc": "ec2",
    "codeguru-profiler": "codeguruprofiler",
    "AWSCloudMap": "servicediscovery",
}

MAX_EXECUTION_PARALLEL = 2


class LimitResources(ResourceProvider):
    def __init__(self, options: LimitOptions):
        """
        All resources

        :param options:
        """
        super().__init__()
        self.options = options
        self.cache = ResourceCache()

    @exception
    # pylint: disable=too-many-locals
    def get_resources(self) -> List[Resource]:

        threshold_requested = (
            0 if self.options.threshold is None else self.options.threshold
        )

        client_quota = self.options.session.client("service-quotas")

        resources_found = []

        services = self.options.services

        with ThreadPoolExecutor(MAX_EXECUTION_PARALLEL) as executor:
            results = executor.map(
                lambda service_name: self.analyze_service(
                    service_name=service_name,
                    client_quota=client_quota,
                    threshold_requested=int(threshold_requested),
                ),
                services,
            )

        for result in results:
            if result is not None:
                resources_found.extend(result)

        return resources_found

    @exception
    def analyze_service(self, service_name, client_quota, threshold_requested):
        cache_key = "aws_limits_" + service_name + "_" + self.options.region_name
        cache = self.cache.get_key(cache_key)
        resources_found = []
        if service_name not in cache:
            return []

        for data_quota_code in cache[service_name]:
            if data_quota_code is None:
                continue
            resource_found = self.analyze_quota(
                client_quota=client_quota,
                data_quota_code=data_quota_code,
                service=service_name,
                threshold_requested=threshold_requested,
            )
            if resource_found is not None:
                resources_found.append(resource_found)
        return resources_found

    @exception
    # pylint: disable=too-many-locals
    def analyze_quota(
        self, client_quota, data_quota_code, service, threshold_requested
    ):
        resource_found = None
        quota_data = ALLOWED_SERVICES_CODES[service][data_quota_code["quota_code"]]

        value_aws = value = data_quota_code["value"]

        # Quota is adjustable by ticket request, then must override this values.
        if bool(data_quota_code["adjustable"]) is True:
            try:
                response_quota = client_quota.get_service_quota(
                    ServiceCode=service, QuotaCode=data_quota_code["quota_code"]
                )
                if "Value" in response_quota["Quota"]:
                    value = response_quota["Quota"]["Value"]
                else:
                    value = data_quota_code["value"]
            except client_quota.exceptions.NoSuchResourceException:
                value = data_quota_code["value"]

        if self.options.verbose:
            message_handler(
                "Collecting data from Quota: "
                + service
                + " - "
                + data_quota_code["quota_name"]
                + "...",
                "HEADER",
            )

        # Need to convert some quota-services endpoint
        if service in SERVICEQUOTA_TO_BOTO3:
            service = SERVICEQUOTA_TO_BOTO3.get(service)

        client = self.options.session.client(
            service, region_name=self.options.region_name
        )

        usage = 0

        # Check filters by resource
        if "filter" in quota_data:
            filters = quota_data["filter"]
        else:
            filters = None

        pages = get_paginator(
            client=client,
            operation_name=quota_data["method"],
            resource_type="aws_limit",
            filters=filters,
        )
        if not pages:
            if filters:
                response = getattr(client, quota_data["method"])(**filters)
            else:
                response = getattr(client, quota_data["method"])()
            usage = len(response[quota_data["key"]])
        else:
            for page in pages:
                usage = usage + len(page[quota_data["key"]])

        try:
            percent = round((usage / value) * 100, 2)
        except ZeroDivisionError:
            percent = 0

        if percent >= threshold_requested:
            resource_found = Resource(
                digest=ResourceDigest(
                    id=data_quota_code["quota_code"], type="aws_limit"
                ),
                name="",
                group="",
                limits=LimitsValues(
                    quota_name=data_quota_code["quota_name"],
                    quota_code=data_quota_code["quota_code"],
                    aws_limit=int(value_aws),
                    local_limit=int(value),
                    usage=int(usage),
                    service=service,
                    percent=percent,
                ),
            )

        return resource_found
