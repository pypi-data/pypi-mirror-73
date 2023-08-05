import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *


class Default(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.region_info.Default"):
    """Provides default values for certain regional information points.

    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="servicePrincipal")
    @builtins.classmethod
    def service_principal(cls, service: str, region: str, url_suffix: str) -> str:
        """Computes a "standard" AWS Service principal for a given service, region and suffix.

        This is useful for example when
        you need to compute a service principal name, but you do not have a synthesize-time region literal available (so
        all you have is ``{ "Ref": "AWS::Region" }``). This way you get the same defaulting behavior that is normally used
        for built-in data.

        :param service: the name of the service (s3, s3.amazonaws.com, ...).
        :param region: the region in which the service principal is needed.
        :param url_suffix: the URL suffix for the partition in which the region is located.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "servicePrincipal", [service, region, url_suffix])

    @jsii.python.classproperty
    @jsii.member(jsii_name="VPC_ENDPOINT_SERVICE_NAME_PREFIX")
    def VPC_ENDPOINT_SERVICE_NAME_PREFIX(cls) -> str:
        """The default value for a VPC Endpoint Service name prefix, useful if you do not have a synthesize-time region literal available (all you have is ``{ "Ref": "AWS::Region" }``).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VPC_ENDPOINT_SERVICE_NAME_PREFIX")


class Fact(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.region_info.Fact"):
    """A database of regional information.

    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="find")
    @builtins.classmethod
    def find(cls, region: str, name: str) -> typing.Optional[str]:
        """Retrieves a fact from this Fact database.

        :param region: the name of the region (e.g: ``us-east-1``).
        :param name: the name of the fact being looked up (see the ``FactName`` class for details).

        return
        :return: the fact value if it is known, and ``undefined`` otherwise.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "find", [region, name])

    @jsii.member(jsii_name="register")
    @builtins.classmethod
    def register(cls, fact: "IFact", allow_replacing: typing.Optional[bool]=None) -> None:
        """Registers a new fact in this Fact database.

        :param fact: the new fact to be registered.
        :param allow_replacing: whether new facts can replace existing facts or not.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "register", [fact, allow_replacing])

    @jsii.member(jsii_name="requireFact")
    @builtins.classmethod
    def require_fact(cls, region: str, name: str) -> str:
        """Retrieve a fact from the Fact database.

        (retrieval will fail if the specified region or
        fact name does not exist.)

        :param region: the name of the region (e.g: ``us-east-1``).
        :param name: the name of the fact being looked up (see the ``FactName`` class for details).

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "requireFact", [region, name])

    @jsii.member(jsii_name="unregister")
    @builtins.classmethod
    def unregister(cls, region: str, name: str, value: typing.Optional[str]=None) -> None:
        """Removes a fact from the database.

        :param region: the region for which the fact is to be removed.
        :param name: the name of the fact to remove.
        :param value: the value that should be removed (removal will fail if the value is specified, but does not match the current stored value).

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "unregister", [region, name, value])

    @jsii.python.classproperty
    @jsii.member(jsii_name="regions")
    def regions(cls) -> typing.List[str]:
        """
        return
        :return:

        the list of names of AWS regions for which there is at least one registered fact. This
        may not be an exhaustive list of all available AWS regions.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "regions")


class FactName(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.region_info.FactName"):
    """All standardized fact names.

    stability
    :stability: experimental
    """
    def __init__(self) -> None:
        jsii.create(FactName, self, [])

    @jsii.member(jsii_name="servicePrincipal")
    @builtins.classmethod
    def service_principal(cls, service: str) -> str:
        """The name of the regional service principal for a given service.

        :param service: the service name, either simple (e.g: ``s3``, ``codedeploy``) or qualified (e.g: ``s3.amazonaws.com``). The ``.amazonaws.com`` and ``.amazonaws.com.cn`` domains are stripped from service names, so they are canonicalized in that respect.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "servicePrincipal", [service])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CDK_METADATA_RESOURCE_AVAILABLE")
    def CDK_METADATA_RESOURCE_AVAILABLE(cls) -> str:
        """Whether the AWS::CDK::Metadata CloudFormation Resource is available in-region or not.

        The value is a boolean
        modelled as ``YES`` or ``NO``.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "CDK_METADATA_RESOURCE_AVAILABLE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="DOMAIN_SUFFIX")
    def DOMAIN_SUFFIX(cls) -> str:
        """The domain suffix for a region (e.g: 'amazonaws.com`).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "DOMAIN_SUFFIX")

    @jsii.python.classproperty
    @jsii.member(jsii_name="PARTITION")
    def PARTITION(cls) -> str:
        """The name of the partition for a region (e.g: 'aws', 'aws-cn', ...).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "PARTITION")

    @jsii.python.classproperty
    @jsii.member(jsii_name="S3_STATIC_WEBSITE_ENDPOINT")
    def S3_STATIC_WEBSITE_ENDPOINT(cls) -> str:
        """The endpoint used for hosting S3 static websites.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "S3_STATIC_WEBSITE_ENDPOINT")

    @jsii.python.classproperty
    @jsii.member(jsii_name="S3_STATIC_WEBSITE_ZONE_53_HOSTED_ZONE_ID")
    def S3_STATIC_WEBSITE_ZONE_53_HOSTED_ZONE_ID(cls) -> str:
        """The endpoint used for aliasing S3 static websites in Route 53.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "S3_STATIC_WEBSITE_ZONE_53_HOSTED_ZONE_ID")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VPC_ENDPOINT_SERVICE_NAME_PREFIX")
    def VPC_ENDPOINT_SERVICE_NAME_PREFIX(cls) -> str:
        """The prefix for VPC Endpoint Service names, cn.com.amazonaws.vpce for China regions, com.amazonaws.vpce otherwise.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VPC_ENDPOINT_SERVICE_NAME_PREFIX")


@jsii.interface(jsii_type="monocdk-experiment.region_info.IFact")
class IFact(jsii.compat.Protocol):
    """A fact that can be registered about a particular region.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IFactProxy

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """The name of this fact.

        Standardized values are provided by the ``Facts`` class.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> str:
        """The region for which this fact applies.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> str:
        """The value of this fact.

        stability
        :stability: experimental
        """
        ...


class _IFactProxy():
    """A fact that can be registered about a particular region.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.region_info.IFact"
    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """The name of this fact.

        Standardized values are provided by the ``Facts`` class.

        stability
        :stability: experimental
        """
        return jsii.get(self, "name")

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> str:
        """The region for which this fact applies.

        stability
        :stability: experimental
        """
        return jsii.get(self, "region")

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> str:
        """The value of this fact.

        stability
        :stability: experimental
        """
        return jsii.get(self, "value")


class RegionInfo(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.region_info.RegionInfo"):
    """Information pertaining to an AWS region.

    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="get")
    @builtins.classmethod
    def get(cls, name: str) -> "RegionInfo":
        """Obtain region info for a given region name.

        :param name: the name of the region (e.g: us-east-1).

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "get", [name])

    @jsii.member(jsii_name="servicePrincipal")
    def service_principal(self, service: str) -> typing.Optional[str]:
        """The name of the service principal for a given service in this region.

        :param service: the service name (e.g: s3.amazonaws.com).

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "servicePrincipal", [service])

    @jsii.python.classproperty
    @jsii.member(jsii_name="regions")
    def regions(cls) -> typing.List["RegionInfo"]:
        """
        return
        :return:

        the list of names of AWS regions for which there is at least one registered fact. This
        may not be an exaustive list of all available AWS regions.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "regions")

    @builtins.property
    @jsii.member(jsii_name="cdkMetadataResourceAvailable")
    def cdk_metadata_resource_available(self) -> bool:
        """Whether the ``AWS::CDK::Metadata`` CloudFormation Resource is available in this region or not.

        stability
        :stability: experimental
        """
        return jsii.get(self, "cdkMetadataResourceAvailable")

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "name")

    @builtins.property
    @jsii.member(jsii_name="domainSuffix")
    def domain_suffix(self) -> typing.Optional[str]:
        """The domain name suffix (e.g: amazonaws.com) for this region.

        stability
        :stability: experimental
        """
        return jsii.get(self, "domainSuffix")

    @builtins.property
    @jsii.member(jsii_name="partition")
    def partition(self) -> typing.Optional[str]:
        """The name of the ARN partition for this region (e.g: aws).

        stability
        :stability: experimental
        """
        return jsii.get(self, "partition")

    @builtins.property
    @jsii.member(jsii_name="s3StaticWebsiteEndpoint")
    def s3_static_website_endpoint(self) -> typing.Optional[str]:
        """The endpoint used by S3 static website hosting in this region (e.g: s3-static-website-us-east-1.amazonaws.com).

        stability
        :stability: experimental
        """
        return jsii.get(self, "s3StaticWebsiteEndpoint")

    @builtins.property
    @jsii.member(jsii_name="s3StaticWebsiteHostedZoneId")
    def s3_static_website_hosted_zone_id(self) -> typing.Optional[str]:
        """The hosted zone ID used by Route 53 to alias a S3 static website in this region (e.g: Z2O1EMRO9K5GLX).

        stability
        :stability: experimental
        """
        return jsii.get(self, "s3StaticWebsiteHostedZoneId")

    @builtins.property
    @jsii.member(jsii_name="vpcEndpointServiceNamePrefix")
    def vpc_endpoint_service_name_prefix(self) -> typing.Optional[str]:
        """The prefix for VPC Endpoint Service names, cn.com.amazonaws.vpce for China regions, com.amazonaws.vpce otherwise.

        stability
        :stability: experimental
        """
        return jsii.get(self, "vpcEndpointServiceNamePrefix")


__all__ = [
    "Default",
    "Fact",
    "FactName",
    "IFact",
    "RegionInfo",
]

publication.publish()
