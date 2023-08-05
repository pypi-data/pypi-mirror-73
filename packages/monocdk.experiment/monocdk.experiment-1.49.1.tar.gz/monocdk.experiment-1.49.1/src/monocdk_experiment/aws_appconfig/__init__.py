import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (CfnResource as _CfnResource_7760e8e4, Construct as _Construct_f50a3f53, FromCloudFormationOptions as _FromCloudFormationOptions_5f49f6f1, TreeInspector as _TreeInspector_154f5999, IInspectable as _IInspectable_051e6ed8, IResolvable as _IResolvable_9ceae33e)


@jsii.implements(_IInspectable_051e6ed8)
class CfnApplication(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_appconfig.CfnApplication"):
    """A CloudFormation ``AWS::AppConfig::Application``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-application.html
    cloudformationResource:
    :cloudformationResource:: AWS::AppConfig::Application
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, name: str, description: typing.Optional[str]=None, tags: typing.Optional[typing.List["TagsProperty"]]=None) -> None:
        """Create a new ``AWS::AppConfig::Application``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::AppConfig::Application.Name``.
        :param description: ``AWS::AppConfig::Application.Description``.
        :param tags: ``AWS::AppConfig::Application.Tags``.
        """
        props = CfnApplicationProps(name=name, description=description, tags=tags)

        jsii.create(CfnApplication, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnApplication":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = _FromCloudFormationOptions_5f49f6f1(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_154f5999) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::AppConfig::Application.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-application.html#cfn-appconfig-application-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::AppConfig::Application.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-application.html#cfn-appconfig-application-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["TagsProperty"]]:
        """``AWS::AppConfig::Application.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-application.html#cfn-appconfig-application-tags
        """
        return jsii.get(self, "tags")

    @tags.setter
    def tags(self, value: typing.Optional[typing.List["TagsProperty"]]) -> None:
        jsii.set(self, "tags", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_appconfig.CfnApplication.TagsProperty", jsii_struct_bases=[], name_mapping={'key': 'key', 'value': 'value'})
    class TagsProperty():
        def __init__(self, *, key: typing.Optional[str]=None, value: typing.Optional[str]=None) -> None:
            """
            :param key: ``CfnApplication.TagsProperty.Key``.
            :param value: ``CfnApplication.TagsProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-application-tags.html
            """
            self._values = {
            }
            if key is not None: self._values["key"] = key
            if value is not None: self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[str]:
            """``CfnApplication.TagsProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-application-tags.html#cfn-appconfig-application-tags-key
            """
            return self._values.get('key')

        @builtins.property
        def value(self) -> typing.Optional[str]:
            """``CfnApplication.TagsProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-application-tags.html#cfn-appconfig-application-tags-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TagsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_appconfig.CfnApplicationProps", jsii_struct_bases=[], name_mapping={'name': 'name', 'description': 'description', 'tags': 'tags'})
class CfnApplicationProps():
    def __init__(self, *, name: str, description: typing.Optional[str]=None, tags: typing.Optional[typing.List["CfnApplication.TagsProperty"]]=None) -> None:
        """Properties for defining a ``AWS::AppConfig::Application``.

        :param name: ``AWS::AppConfig::Application.Name``.
        :param description: ``AWS::AppConfig::Application.Description``.
        :param tags: ``AWS::AppConfig::Application.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-application.html
        """
        self._values = {
            'name': name,
        }
        if description is not None: self._values["description"] = description
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def name(self) -> str:
        """``AWS::AppConfig::Application.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-application.html#cfn-appconfig-application-name
        """
        return self._values.get('name')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::AppConfig::Application.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-application.html#cfn-appconfig-application-description
        """
        return self._values.get('description')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["CfnApplication.TagsProperty"]]:
        """``AWS::AppConfig::Application.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-application.html#cfn-appconfig-application-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnApplicationProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnConfigurationProfile(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_appconfig.CfnConfigurationProfile"):
    """A CloudFormation ``AWS::AppConfig::ConfigurationProfile``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-configurationprofile.html
    cloudformationResource:
    :cloudformationResource:: AWS::AppConfig::ConfigurationProfile
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, application_id: str, location_uri: str, name: str, description: typing.Optional[str]=None, retrieval_role_arn: typing.Optional[str]=None, tags: typing.Optional[typing.List["TagsProperty"]]=None, validators: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ValidatorsProperty", _IResolvable_9ceae33e]]]]=None) -> None:
        """Create a new ``AWS::AppConfig::ConfigurationProfile``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: ``AWS::AppConfig::ConfigurationProfile.ApplicationId``.
        :param location_uri: ``AWS::AppConfig::ConfigurationProfile.LocationUri``.
        :param name: ``AWS::AppConfig::ConfigurationProfile.Name``.
        :param description: ``AWS::AppConfig::ConfigurationProfile.Description``.
        :param retrieval_role_arn: ``AWS::AppConfig::ConfigurationProfile.RetrievalRoleArn``.
        :param tags: ``AWS::AppConfig::ConfigurationProfile.Tags``.
        :param validators: ``AWS::AppConfig::ConfigurationProfile.Validators``.
        """
        props = CfnConfigurationProfileProps(application_id=application_id, location_uri=location_uri, name=name, description=description, retrieval_role_arn=retrieval_role_arn, tags=tags, validators=validators)

        jsii.create(CfnConfigurationProfile, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnConfigurationProfile":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = _FromCloudFormationOptions_5f49f6f1(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_154f5999) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> str:
        """``AWS::AppConfig::ConfigurationProfile.ApplicationId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-configurationprofile.html#cfn-appconfig-configurationprofile-applicationid
        """
        return jsii.get(self, "applicationId")

    @application_id.setter
    def application_id(self, value: str) -> None:
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="locationUri")
    def location_uri(self) -> str:
        """``AWS::AppConfig::ConfigurationProfile.LocationUri``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-configurationprofile.html#cfn-appconfig-configurationprofile-locationuri
        """
        return jsii.get(self, "locationUri")

    @location_uri.setter
    def location_uri(self, value: str) -> None:
        jsii.set(self, "locationUri", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::AppConfig::ConfigurationProfile.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-configurationprofile.html#cfn-appconfig-configurationprofile-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::AppConfig::ConfigurationProfile.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-configurationprofile.html#cfn-appconfig-configurationprofile-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="retrievalRoleArn")
    def retrieval_role_arn(self) -> typing.Optional[str]:
        """``AWS::AppConfig::ConfigurationProfile.RetrievalRoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-configurationprofile.html#cfn-appconfig-configurationprofile-retrievalrolearn
        """
        return jsii.get(self, "retrievalRoleArn")

    @retrieval_role_arn.setter
    def retrieval_role_arn(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "retrievalRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["TagsProperty"]]:
        """``AWS::AppConfig::ConfigurationProfile.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-configurationprofile.html#cfn-appconfig-configurationprofile-tags
        """
        return jsii.get(self, "tags")

    @tags.setter
    def tags(self, value: typing.Optional[typing.List["TagsProperty"]]) -> None:
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="validators")
    def validators(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ValidatorsProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::AppConfig::ConfigurationProfile.Validators``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-configurationprofile.html#cfn-appconfig-configurationprofile-validators
        """
        return jsii.get(self, "validators")

    @validators.setter
    def validators(self, value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ValidatorsProperty", _IResolvable_9ceae33e]]]]) -> None:
        jsii.set(self, "validators", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_appconfig.CfnConfigurationProfile.TagsProperty", jsii_struct_bases=[], name_mapping={'key': 'key', 'value': 'value'})
    class TagsProperty():
        def __init__(self, *, key: typing.Optional[str]=None, value: typing.Optional[str]=None) -> None:
            """
            :param key: ``CfnConfigurationProfile.TagsProperty.Key``.
            :param value: ``CfnConfigurationProfile.TagsProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-configurationprofile-tags.html
            """
            self._values = {
            }
            if key is not None: self._values["key"] = key
            if value is not None: self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[str]:
            """``CfnConfigurationProfile.TagsProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-configurationprofile-tags.html#cfn-appconfig-configurationprofile-tags-key
            """
            return self._values.get('key')

        @builtins.property
        def value(self) -> typing.Optional[str]:
            """``CfnConfigurationProfile.TagsProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-configurationprofile-tags.html#cfn-appconfig-configurationprofile-tags-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TagsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appconfig.CfnConfigurationProfile.ValidatorsProperty", jsii_struct_bases=[], name_mapping={'content': 'content', 'type': 'type'})
    class ValidatorsProperty():
        def __init__(self, *, content: typing.Optional[str]=None, type: typing.Optional[str]=None) -> None:
            """
            :param content: ``CfnConfigurationProfile.ValidatorsProperty.Content``.
            :param type: ``CfnConfigurationProfile.ValidatorsProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-configurationprofile-validators.html
            """
            self._values = {
            }
            if content is not None: self._values["content"] = content
            if type is not None: self._values["type"] = type

        @builtins.property
        def content(self) -> typing.Optional[str]:
            """``CfnConfigurationProfile.ValidatorsProperty.Content``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-configurationprofile-validators.html#cfn-appconfig-configurationprofile-validators-content
            """
            return self._values.get('content')

        @builtins.property
        def type(self) -> typing.Optional[str]:
            """``CfnConfigurationProfile.ValidatorsProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-configurationprofile-validators.html#cfn-appconfig-configurationprofile-validators-type
            """
            return self._values.get('type')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ValidatorsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_appconfig.CfnConfigurationProfileProps", jsii_struct_bases=[], name_mapping={'application_id': 'applicationId', 'location_uri': 'locationUri', 'name': 'name', 'description': 'description', 'retrieval_role_arn': 'retrievalRoleArn', 'tags': 'tags', 'validators': 'validators'})
class CfnConfigurationProfileProps():
    def __init__(self, *, application_id: str, location_uri: str, name: str, description: typing.Optional[str]=None, retrieval_role_arn: typing.Optional[str]=None, tags: typing.Optional[typing.List["CfnConfigurationProfile.TagsProperty"]]=None, validators: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnConfigurationProfile.ValidatorsProperty", _IResolvable_9ceae33e]]]]=None) -> None:
        """Properties for defining a ``AWS::AppConfig::ConfigurationProfile``.

        :param application_id: ``AWS::AppConfig::ConfigurationProfile.ApplicationId``.
        :param location_uri: ``AWS::AppConfig::ConfigurationProfile.LocationUri``.
        :param name: ``AWS::AppConfig::ConfigurationProfile.Name``.
        :param description: ``AWS::AppConfig::ConfigurationProfile.Description``.
        :param retrieval_role_arn: ``AWS::AppConfig::ConfigurationProfile.RetrievalRoleArn``.
        :param tags: ``AWS::AppConfig::ConfigurationProfile.Tags``.
        :param validators: ``AWS::AppConfig::ConfigurationProfile.Validators``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-configurationprofile.html
        """
        self._values = {
            'application_id': application_id,
            'location_uri': location_uri,
            'name': name,
        }
        if description is not None: self._values["description"] = description
        if retrieval_role_arn is not None: self._values["retrieval_role_arn"] = retrieval_role_arn
        if tags is not None: self._values["tags"] = tags
        if validators is not None: self._values["validators"] = validators

    @builtins.property
    def application_id(self) -> str:
        """``AWS::AppConfig::ConfigurationProfile.ApplicationId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-configurationprofile.html#cfn-appconfig-configurationprofile-applicationid
        """
        return self._values.get('application_id')

    @builtins.property
    def location_uri(self) -> str:
        """``AWS::AppConfig::ConfigurationProfile.LocationUri``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-configurationprofile.html#cfn-appconfig-configurationprofile-locationuri
        """
        return self._values.get('location_uri')

    @builtins.property
    def name(self) -> str:
        """``AWS::AppConfig::ConfigurationProfile.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-configurationprofile.html#cfn-appconfig-configurationprofile-name
        """
        return self._values.get('name')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::AppConfig::ConfigurationProfile.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-configurationprofile.html#cfn-appconfig-configurationprofile-description
        """
        return self._values.get('description')

    @builtins.property
    def retrieval_role_arn(self) -> typing.Optional[str]:
        """``AWS::AppConfig::ConfigurationProfile.RetrievalRoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-configurationprofile.html#cfn-appconfig-configurationprofile-retrievalrolearn
        """
        return self._values.get('retrieval_role_arn')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["CfnConfigurationProfile.TagsProperty"]]:
        """``AWS::AppConfig::ConfigurationProfile.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-configurationprofile.html#cfn-appconfig-configurationprofile-tags
        """
        return self._values.get('tags')

    @builtins.property
    def validators(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnConfigurationProfile.ValidatorsProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::AppConfig::ConfigurationProfile.Validators``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-configurationprofile.html#cfn-appconfig-configurationprofile-validators
        """
        return self._values.get('validators')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnConfigurationProfileProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnDeployment(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_appconfig.CfnDeployment"):
    """A CloudFormation ``AWS::AppConfig::Deployment``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deployment.html
    cloudformationResource:
    :cloudformationResource:: AWS::AppConfig::Deployment
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, application_id: str, configuration_profile_id: str, configuration_version: str, deployment_strategy_id: str, environment_id: str, description: typing.Optional[str]=None, tags: typing.Optional[typing.List["TagsProperty"]]=None) -> None:
        """Create a new ``AWS::AppConfig::Deployment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: ``AWS::AppConfig::Deployment.ApplicationId``.
        :param configuration_profile_id: ``AWS::AppConfig::Deployment.ConfigurationProfileId``.
        :param configuration_version: ``AWS::AppConfig::Deployment.ConfigurationVersion``.
        :param deployment_strategy_id: ``AWS::AppConfig::Deployment.DeploymentStrategyId``.
        :param environment_id: ``AWS::AppConfig::Deployment.EnvironmentId``.
        :param description: ``AWS::AppConfig::Deployment.Description``.
        :param tags: ``AWS::AppConfig::Deployment.Tags``.
        """
        props = CfnDeploymentProps(application_id=application_id, configuration_profile_id=configuration_profile_id, configuration_version=configuration_version, deployment_strategy_id=deployment_strategy_id, environment_id=environment_id, description=description, tags=tags)

        jsii.create(CfnDeployment, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnDeployment":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = _FromCloudFormationOptions_5f49f6f1(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_154f5999) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> str:
        """``AWS::AppConfig::Deployment.ApplicationId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deployment.html#cfn-appconfig-deployment-applicationid
        """
        return jsii.get(self, "applicationId")

    @application_id.setter
    def application_id(self, value: str) -> None:
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="configurationProfileId")
    def configuration_profile_id(self) -> str:
        """``AWS::AppConfig::Deployment.ConfigurationProfileId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deployment.html#cfn-appconfig-deployment-configurationprofileid
        """
        return jsii.get(self, "configurationProfileId")

    @configuration_profile_id.setter
    def configuration_profile_id(self, value: str) -> None:
        jsii.set(self, "configurationProfileId", value)

    @builtins.property
    @jsii.member(jsii_name="configurationVersion")
    def configuration_version(self) -> str:
        """``AWS::AppConfig::Deployment.ConfigurationVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deployment.html#cfn-appconfig-deployment-configurationversion
        """
        return jsii.get(self, "configurationVersion")

    @configuration_version.setter
    def configuration_version(self, value: str) -> None:
        jsii.set(self, "configurationVersion", value)

    @builtins.property
    @jsii.member(jsii_name="deploymentStrategyId")
    def deployment_strategy_id(self) -> str:
        """``AWS::AppConfig::Deployment.DeploymentStrategyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deployment.html#cfn-appconfig-deployment-deploymentstrategyid
        """
        return jsii.get(self, "deploymentStrategyId")

    @deployment_strategy_id.setter
    def deployment_strategy_id(self, value: str) -> None:
        jsii.set(self, "deploymentStrategyId", value)

    @builtins.property
    @jsii.member(jsii_name="environmentId")
    def environment_id(self) -> str:
        """``AWS::AppConfig::Deployment.EnvironmentId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deployment.html#cfn-appconfig-deployment-environmentid
        """
        return jsii.get(self, "environmentId")

    @environment_id.setter
    def environment_id(self, value: str) -> None:
        jsii.set(self, "environmentId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::AppConfig::Deployment.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deployment.html#cfn-appconfig-deployment-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["TagsProperty"]]:
        """``AWS::AppConfig::Deployment.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deployment.html#cfn-appconfig-deployment-tags
        """
        return jsii.get(self, "tags")

    @tags.setter
    def tags(self, value: typing.Optional[typing.List["TagsProperty"]]) -> None:
        jsii.set(self, "tags", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_appconfig.CfnDeployment.TagsProperty", jsii_struct_bases=[], name_mapping={'key': 'key', 'value': 'value'})
    class TagsProperty():
        def __init__(self, *, key: typing.Optional[str]=None, value: typing.Optional[str]=None) -> None:
            """
            :param key: ``CfnDeployment.TagsProperty.Key``.
            :param value: ``CfnDeployment.TagsProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-deployment-tags.html
            """
            self._values = {
            }
            if key is not None: self._values["key"] = key
            if value is not None: self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[str]:
            """``CfnDeployment.TagsProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-deployment-tags.html#cfn-appconfig-deployment-tags-key
            """
            return self._values.get('key')

        @builtins.property
        def value(self) -> typing.Optional[str]:
            """``CfnDeployment.TagsProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-deployment-tags.html#cfn-appconfig-deployment-tags-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TagsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_appconfig.CfnDeploymentProps", jsii_struct_bases=[], name_mapping={'application_id': 'applicationId', 'configuration_profile_id': 'configurationProfileId', 'configuration_version': 'configurationVersion', 'deployment_strategy_id': 'deploymentStrategyId', 'environment_id': 'environmentId', 'description': 'description', 'tags': 'tags'})
class CfnDeploymentProps():
    def __init__(self, *, application_id: str, configuration_profile_id: str, configuration_version: str, deployment_strategy_id: str, environment_id: str, description: typing.Optional[str]=None, tags: typing.Optional[typing.List["CfnDeployment.TagsProperty"]]=None) -> None:
        """Properties for defining a ``AWS::AppConfig::Deployment``.

        :param application_id: ``AWS::AppConfig::Deployment.ApplicationId``.
        :param configuration_profile_id: ``AWS::AppConfig::Deployment.ConfigurationProfileId``.
        :param configuration_version: ``AWS::AppConfig::Deployment.ConfigurationVersion``.
        :param deployment_strategy_id: ``AWS::AppConfig::Deployment.DeploymentStrategyId``.
        :param environment_id: ``AWS::AppConfig::Deployment.EnvironmentId``.
        :param description: ``AWS::AppConfig::Deployment.Description``.
        :param tags: ``AWS::AppConfig::Deployment.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deployment.html
        """
        self._values = {
            'application_id': application_id,
            'configuration_profile_id': configuration_profile_id,
            'configuration_version': configuration_version,
            'deployment_strategy_id': deployment_strategy_id,
            'environment_id': environment_id,
        }
        if description is not None: self._values["description"] = description
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def application_id(self) -> str:
        """``AWS::AppConfig::Deployment.ApplicationId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deployment.html#cfn-appconfig-deployment-applicationid
        """
        return self._values.get('application_id')

    @builtins.property
    def configuration_profile_id(self) -> str:
        """``AWS::AppConfig::Deployment.ConfigurationProfileId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deployment.html#cfn-appconfig-deployment-configurationprofileid
        """
        return self._values.get('configuration_profile_id')

    @builtins.property
    def configuration_version(self) -> str:
        """``AWS::AppConfig::Deployment.ConfigurationVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deployment.html#cfn-appconfig-deployment-configurationversion
        """
        return self._values.get('configuration_version')

    @builtins.property
    def deployment_strategy_id(self) -> str:
        """``AWS::AppConfig::Deployment.DeploymentStrategyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deployment.html#cfn-appconfig-deployment-deploymentstrategyid
        """
        return self._values.get('deployment_strategy_id')

    @builtins.property
    def environment_id(self) -> str:
        """``AWS::AppConfig::Deployment.EnvironmentId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deployment.html#cfn-appconfig-deployment-environmentid
        """
        return self._values.get('environment_id')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::AppConfig::Deployment.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deployment.html#cfn-appconfig-deployment-description
        """
        return self._values.get('description')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["CfnDeployment.TagsProperty"]]:
        """``AWS::AppConfig::Deployment.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deployment.html#cfn-appconfig-deployment-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDeploymentProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnDeploymentStrategy(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_appconfig.CfnDeploymentStrategy"):
    """A CloudFormation ``AWS::AppConfig::DeploymentStrategy``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deploymentstrategy.html
    cloudformationResource:
    :cloudformationResource:: AWS::AppConfig::DeploymentStrategy
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, deployment_duration_in_minutes: jsii.Number, growth_factor: jsii.Number, name: str, replicate_to: str, description: typing.Optional[str]=None, final_bake_time_in_minutes: typing.Optional[jsii.Number]=None, growth_type: typing.Optional[str]=None, tags: typing.Optional[typing.List["TagsProperty"]]=None) -> None:
        """Create a new ``AWS::AppConfig::DeploymentStrategy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param deployment_duration_in_minutes: ``AWS::AppConfig::DeploymentStrategy.DeploymentDurationInMinutes``.
        :param growth_factor: ``AWS::AppConfig::DeploymentStrategy.GrowthFactor``.
        :param name: ``AWS::AppConfig::DeploymentStrategy.Name``.
        :param replicate_to: ``AWS::AppConfig::DeploymentStrategy.ReplicateTo``.
        :param description: ``AWS::AppConfig::DeploymentStrategy.Description``.
        :param final_bake_time_in_minutes: ``AWS::AppConfig::DeploymentStrategy.FinalBakeTimeInMinutes``.
        :param growth_type: ``AWS::AppConfig::DeploymentStrategy.GrowthType``.
        :param tags: ``AWS::AppConfig::DeploymentStrategy.Tags``.
        """
        props = CfnDeploymentStrategyProps(deployment_duration_in_minutes=deployment_duration_in_minutes, growth_factor=growth_factor, name=name, replicate_to=replicate_to, description=description, final_bake_time_in_minutes=final_bake_time_in_minutes, growth_type=growth_type, tags=tags)

        jsii.create(CfnDeploymentStrategy, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnDeploymentStrategy":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = _FromCloudFormationOptions_5f49f6f1(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_154f5999) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="deploymentDurationInMinutes")
    def deployment_duration_in_minutes(self) -> jsii.Number:
        """``AWS::AppConfig::DeploymentStrategy.DeploymentDurationInMinutes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deploymentstrategy.html#cfn-appconfig-deploymentstrategy-deploymentdurationinminutes
        """
        return jsii.get(self, "deploymentDurationInMinutes")

    @deployment_duration_in_minutes.setter
    def deployment_duration_in_minutes(self, value: jsii.Number) -> None:
        jsii.set(self, "deploymentDurationInMinutes", value)

    @builtins.property
    @jsii.member(jsii_name="growthFactor")
    def growth_factor(self) -> jsii.Number:
        """``AWS::AppConfig::DeploymentStrategy.GrowthFactor``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deploymentstrategy.html#cfn-appconfig-deploymentstrategy-growthfactor
        """
        return jsii.get(self, "growthFactor")

    @growth_factor.setter
    def growth_factor(self, value: jsii.Number) -> None:
        jsii.set(self, "growthFactor", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::AppConfig::DeploymentStrategy.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deploymentstrategy.html#cfn-appconfig-deploymentstrategy-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="replicateTo")
    def replicate_to(self) -> str:
        """``AWS::AppConfig::DeploymentStrategy.ReplicateTo``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deploymentstrategy.html#cfn-appconfig-deploymentstrategy-replicateto
        """
        return jsii.get(self, "replicateTo")

    @replicate_to.setter
    def replicate_to(self, value: str) -> None:
        jsii.set(self, "replicateTo", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::AppConfig::DeploymentStrategy.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deploymentstrategy.html#cfn-appconfig-deploymentstrategy-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="finalBakeTimeInMinutes")
    def final_bake_time_in_minutes(self) -> typing.Optional[jsii.Number]:
        """``AWS::AppConfig::DeploymentStrategy.FinalBakeTimeInMinutes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deploymentstrategy.html#cfn-appconfig-deploymentstrategy-finalbaketimeinminutes
        """
        return jsii.get(self, "finalBakeTimeInMinutes")

    @final_bake_time_in_minutes.setter
    def final_bake_time_in_minutes(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "finalBakeTimeInMinutes", value)

    @builtins.property
    @jsii.member(jsii_name="growthType")
    def growth_type(self) -> typing.Optional[str]:
        """``AWS::AppConfig::DeploymentStrategy.GrowthType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deploymentstrategy.html#cfn-appconfig-deploymentstrategy-growthtype
        """
        return jsii.get(self, "growthType")

    @growth_type.setter
    def growth_type(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "growthType", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["TagsProperty"]]:
        """``AWS::AppConfig::DeploymentStrategy.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deploymentstrategy.html#cfn-appconfig-deploymentstrategy-tags
        """
        return jsii.get(self, "tags")

    @tags.setter
    def tags(self, value: typing.Optional[typing.List["TagsProperty"]]) -> None:
        jsii.set(self, "tags", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_appconfig.CfnDeploymentStrategy.TagsProperty", jsii_struct_bases=[], name_mapping={'key': 'key', 'value': 'value'})
    class TagsProperty():
        def __init__(self, *, key: typing.Optional[str]=None, value: typing.Optional[str]=None) -> None:
            """
            :param key: ``CfnDeploymentStrategy.TagsProperty.Key``.
            :param value: ``CfnDeploymentStrategy.TagsProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-deploymentstrategy-tags.html
            """
            self._values = {
            }
            if key is not None: self._values["key"] = key
            if value is not None: self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[str]:
            """``CfnDeploymentStrategy.TagsProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-deploymentstrategy-tags.html#cfn-appconfig-deploymentstrategy-tags-key
            """
            return self._values.get('key')

        @builtins.property
        def value(self) -> typing.Optional[str]:
            """``CfnDeploymentStrategy.TagsProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-deploymentstrategy-tags.html#cfn-appconfig-deploymentstrategy-tags-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TagsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_appconfig.CfnDeploymentStrategyProps", jsii_struct_bases=[], name_mapping={'deployment_duration_in_minutes': 'deploymentDurationInMinutes', 'growth_factor': 'growthFactor', 'name': 'name', 'replicate_to': 'replicateTo', 'description': 'description', 'final_bake_time_in_minutes': 'finalBakeTimeInMinutes', 'growth_type': 'growthType', 'tags': 'tags'})
class CfnDeploymentStrategyProps():
    def __init__(self, *, deployment_duration_in_minutes: jsii.Number, growth_factor: jsii.Number, name: str, replicate_to: str, description: typing.Optional[str]=None, final_bake_time_in_minutes: typing.Optional[jsii.Number]=None, growth_type: typing.Optional[str]=None, tags: typing.Optional[typing.List["CfnDeploymentStrategy.TagsProperty"]]=None) -> None:
        """Properties for defining a ``AWS::AppConfig::DeploymentStrategy``.

        :param deployment_duration_in_minutes: ``AWS::AppConfig::DeploymentStrategy.DeploymentDurationInMinutes``.
        :param growth_factor: ``AWS::AppConfig::DeploymentStrategy.GrowthFactor``.
        :param name: ``AWS::AppConfig::DeploymentStrategy.Name``.
        :param replicate_to: ``AWS::AppConfig::DeploymentStrategy.ReplicateTo``.
        :param description: ``AWS::AppConfig::DeploymentStrategy.Description``.
        :param final_bake_time_in_minutes: ``AWS::AppConfig::DeploymentStrategy.FinalBakeTimeInMinutes``.
        :param growth_type: ``AWS::AppConfig::DeploymentStrategy.GrowthType``.
        :param tags: ``AWS::AppConfig::DeploymentStrategy.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deploymentstrategy.html
        """
        self._values = {
            'deployment_duration_in_minutes': deployment_duration_in_minutes,
            'growth_factor': growth_factor,
            'name': name,
            'replicate_to': replicate_to,
        }
        if description is not None: self._values["description"] = description
        if final_bake_time_in_minutes is not None: self._values["final_bake_time_in_minutes"] = final_bake_time_in_minutes
        if growth_type is not None: self._values["growth_type"] = growth_type
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def deployment_duration_in_minutes(self) -> jsii.Number:
        """``AWS::AppConfig::DeploymentStrategy.DeploymentDurationInMinutes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deploymentstrategy.html#cfn-appconfig-deploymentstrategy-deploymentdurationinminutes
        """
        return self._values.get('deployment_duration_in_minutes')

    @builtins.property
    def growth_factor(self) -> jsii.Number:
        """``AWS::AppConfig::DeploymentStrategy.GrowthFactor``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deploymentstrategy.html#cfn-appconfig-deploymentstrategy-growthfactor
        """
        return self._values.get('growth_factor')

    @builtins.property
    def name(self) -> str:
        """``AWS::AppConfig::DeploymentStrategy.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deploymentstrategy.html#cfn-appconfig-deploymentstrategy-name
        """
        return self._values.get('name')

    @builtins.property
    def replicate_to(self) -> str:
        """``AWS::AppConfig::DeploymentStrategy.ReplicateTo``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deploymentstrategy.html#cfn-appconfig-deploymentstrategy-replicateto
        """
        return self._values.get('replicate_to')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::AppConfig::DeploymentStrategy.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deploymentstrategy.html#cfn-appconfig-deploymentstrategy-description
        """
        return self._values.get('description')

    @builtins.property
    def final_bake_time_in_minutes(self) -> typing.Optional[jsii.Number]:
        """``AWS::AppConfig::DeploymentStrategy.FinalBakeTimeInMinutes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deploymentstrategy.html#cfn-appconfig-deploymentstrategy-finalbaketimeinminutes
        """
        return self._values.get('final_bake_time_in_minutes')

    @builtins.property
    def growth_type(self) -> typing.Optional[str]:
        """``AWS::AppConfig::DeploymentStrategy.GrowthType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deploymentstrategy.html#cfn-appconfig-deploymentstrategy-growthtype
        """
        return self._values.get('growth_type')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["CfnDeploymentStrategy.TagsProperty"]]:
        """``AWS::AppConfig::DeploymentStrategy.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deploymentstrategy.html#cfn-appconfig-deploymentstrategy-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDeploymentStrategyProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnEnvironment(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_appconfig.CfnEnvironment"):
    """A CloudFormation ``AWS::AppConfig::Environment``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-environment.html
    cloudformationResource:
    :cloudformationResource:: AWS::AppConfig::Environment
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, application_id: str, name: str, description: typing.Optional[str]=None, monitors: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["MonitorsProperty", _IResolvable_9ceae33e]]]]=None, tags: typing.Optional[typing.List["TagsProperty"]]=None) -> None:
        """Create a new ``AWS::AppConfig::Environment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: ``AWS::AppConfig::Environment.ApplicationId``.
        :param name: ``AWS::AppConfig::Environment.Name``.
        :param description: ``AWS::AppConfig::Environment.Description``.
        :param monitors: ``AWS::AppConfig::Environment.Monitors``.
        :param tags: ``AWS::AppConfig::Environment.Tags``.
        """
        props = CfnEnvironmentProps(application_id=application_id, name=name, description=description, monitors=monitors, tags=tags)

        jsii.create(CfnEnvironment, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnEnvironment":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = _FromCloudFormationOptions_5f49f6f1(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_154f5999) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> str:
        """``AWS::AppConfig::Environment.ApplicationId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-environment.html#cfn-appconfig-environment-applicationid
        """
        return jsii.get(self, "applicationId")

    @application_id.setter
    def application_id(self, value: str) -> None:
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::AppConfig::Environment.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-environment.html#cfn-appconfig-environment-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::AppConfig::Environment.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-environment.html#cfn-appconfig-environment-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="monitors")
    def monitors(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["MonitorsProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::AppConfig::Environment.Monitors``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-environment.html#cfn-appconfig-environment-monitors
        """
        return jsii.get(self, "monitors")

    @monitors.setter
    def monitors(self, value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["MonitorsProperty", _IResolvable_9ceae33e]]]]) -> None:
        jsii.set(self, "monitors", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["TagsProperty"]]:
        """``AWS::AppConfig::Environment.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-environment.html#cfn-appconfig-environment-tags
        """
        return jsii.get(self, "tags")

    @tags.setter
    def tags(self, value: typing.Optional[typing.List["TagsProperty"]]) -> None:
        jsii.set(self, "tags", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_appconfig.CfnEnvironment.MonitorsProperty", jsii_struct_bases=[], name_mapping={'alarm_arn': 'alarmArn', 'alarm_role_arn': 'alarmRoleArn'})
    class MonitorsProperty():
        def __init__(self, *, alarm_arn: typing.Optional[str]=None, alarm_role_arn: typing.Optional[str]=None) -> None:
            """
            :param alarm_arn: ``CfnEnvironment.MonitorsProperty.AlarmArn``.
            :param alarm_role_arn: ``CfnEnvironment.MonitorsProperty.AlarmRoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-environment-monitors.html
            """
            self._values = {
            }
            if alarm_arn is not None: self._values["alarm_arn"] = alarm_arn
            if alarm_role_arn is not None: self._values["alarm_role_arn"] = alarm_role_arn

        @builtins.property
        def alarm_arn(self) -> typing.Optional[str]:
            """``CfnEnvironment.MonitorsProperty.AlarmArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-environment-monitors.html#cfn-appconfig-environment-monitors-alarmarn
            """
            return self._values.get('alarm_arn')

        @builtins.property
        def alarm_role_arn(self) -> typing.Optional[str]:
            """``CfnEnvironment.MonitorsProperty.AlarmRoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-environment-monitors.html#cfn-appconfig-environment-monitors-alarmrolearn
            """
            return self._values.get('alarm_role_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'MonitorsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_appconfig.CfnEnvironment.TagsProperty", jsii_struct_bases=[], name_mapping={'key': 'key', 'value': 'value'})
    class TagsProperty():
        def __init__(self, *, key: typing.Optional[str]=None, value: typing.Optional[str]=None) -> None:
            """
            :param key: ``CfnEnvironment.TagsProperty.Key``.
            :param value: ``CfnEnvironment.TagsProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-environment-tags.html
            """
            self._values = {
            }
            if key is not None: self._values["key"] = key
            if value is not None: self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[str]:
            """``CfnEnvironment.TagsProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-environment-tags.html#cfn-appconfig-environment-tags-key
            """
            return self._values.get('key')

        @builtins.property
        def value(self) -> typing.Optional[str]:
            """``CfnEnvironment.TagsProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-environment-tags.html#cfn-appconfig-environment-tags-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TagsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_appconfig.CfnEnvironmentProps", jsii_struct_bases=[], name_mapping={'application_id': 'applicationId', 'name': 'name', 'description': 'description', 'monitors': 'monitors', 'tags': 'tags'})
class CfnEnvironmentProps():
    def __init__(self, *, application_id: str, name: str, description: typing.Optional[str]=None, monitors: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnEnvironment.MonitorsProperty", _IResolvable_9ceae33e]]]]=None, tags: typing.Optional[typing.List["CfnEnvironment.TagsProperty"]]=None) -> None:
        """Properties for defining a ``AWS::AppConfig::Environment``.

        :param application_id: ``AWS::AppConfig::Environment.ApplicationId``.
        :param name: ``AWS::AppConfig::Environment.Name``.
        :param description: ``AWS::AppConfig::Environment.Description``.
        :param monitors: ``AWS::AppConfig::Environment.Monitors``.
        :param tags: ``AWS::AppConfig::Environment.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-environment.html
        """
        self._values = {
            'application_id': application_id,
            'name': name,
        }
        if description is not None: self._values["description"] = description
        if monitors is not None: self._values["monitors"] = monitors
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def application_id(self) -> str:
        """``AWS::AppConfig::Environment.ApplicationId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-environment.html#cfn-appconfig-environment-applicationid
        """
        return self._values.get('application_id')

    @builtins.property
    def name(self) -> str:
        """``AWS::AppConfig::Environment.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-environment.html#cfn-appconfig-environment-name
        """
        return self._values.get('name')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::AppConfig::Environment.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-environment.html#cfn-appconfig-environment-description
        """
        return self._values.get('description')

    @builtins.property
    def monitors(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnEnvironment.MonitorsProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::AppConfig::Environment.Monitors``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-environment.html#cfn-appconfig-environment-monitors
        """
        return self._values.get('monitors')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["CfnEnvironment.TagsProperty"]]:
        """``AWS::AppConfig::Environment.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-environment.html#cfn-appconfig-environment-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnEnvironmentProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnHostedConfigurationVersion(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_appconfig.CfnHostedConfigurationVersion"):
    """A CloudFormation ``AWS::AppConfig::HostedConfigurationVersion``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-hostedconfigurationversion.html
    cloudformationResource:
    :cloudformationResource:: AWS::AppConfig::HostedConfigurationVersion
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, application_id: str, configuration_profile_id: str, content: str, content_type: str, description: typing.Optional[str]=None, latest_version_number: typing.Optional[jsii.Number]=None) -> None:
        """Create a new ``AWS::AppConfig::HostedConfigurationVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: ``AWS::AppConfig::HostedConfigurationVersion.ApplicationId``.
        :param configuration_profile_id: ``AWS::AppConfig::HostedConfigurationVersion.ConfigurationProfileId``.
        :param content: ``AWS::AppConfig::HostedConfigurationVersion.Content``.
        :param content_type: ``AWS::AppConfig::HostedConfigurationVersion.ContentType``.
        :param description: ``AWS::AppConfig::HostedConfigurationVersion.Description``.
        :param latest_version_number: ``AWS::AppConfig::HostedConfigurationVersion.LatestVersionNumber``.
        """
        props = CfnHostedConfigurationVersionProps(application_id=application_id, configuration_profile_id=configuration_profile_id, content=content, content_type=content_type, description=description, latest_version_number=latest_version_number)

        jsii.create(CfnHostedConfigurationVersion, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnHostedConfigurationVersion":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = _FromCloudFormationOptions_5f49f6f1(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_154f5999) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> str:
        """``AWS::AppConfig::HostedConfigurationVersion.ApplicationId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-hostedconfigurationversion.html#cfn-appconfig-hostedconfigurationversion-applicationid
        """
        return jsii.get(self, "applicationId")

    @application_id.setter
    def application_id(self, value: str) -> None:
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="configurationProfileId")
    def configuration_profile_id(self) -> str:
        """``AWS::AppConfig::HostedConfigurationVersion.ConfigurationProfileId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-hostedconfigurationversion.html#cfn-appconfig-hostedconfigurationversion-configurationprofileid
        """
        return jsii.get(self, "configurationProfileId")

    @configuration_profile_id.setter
    def configuration_profile_id(self, value: str) -> None:
        jsii.set(self, "configurationProfileId", value)

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> str:
        """``AWS::AppConfig::HostedConfigurationVersion.Content``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-hostedconfigurationversion.html#cfn-appconfig-hostedconfigurationversion-content
        """
        return jsii.get(self, "content")

    @content.setter
    def content(self, value: str) -> None:
        jsii.set(self, "content", value)

    @builtins.property
    @jsii.member(jsii_name="contentType")
    def content_type(self) -> str:
        """``AWS::AppConfig::HostedConfigurationVersion.ContentType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-hostedconfigurationversion.html#cfn-appconfig-hostedconfigurationversion-contenttype
        """
        return jsii.get(self, "contentType")

    @content_type.setter
    def content_type(self, value: str) -> None:
        jsii.set(self, "contentType", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::AppConfig::HostedConfigurationVersion.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-hostedconfigurationversion.html#cfn-appconfig-hostedconfigurationversion-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="latestVersionNumber")
    def latest_version_number(self) -> typing.Optional[jsii.Number]:
        """``AWS::AppConfig::HostedConfigurationVersion.LatestVersionNumber``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-hostedconfigurationversion.html#cfn-appconfig-hostedconfigurationversion-latestversionnumber
        """
        return jsii.get(self, "latestVersionNumber")

    @latest_version_number.setter
    def latest_version_number(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "latestVersionNumber", value)


@jsii.data_type(jsii_type="monocdk-experiment.aws_appconfig.CfnHostedConfigurationVersionProps", jsii_struct_bases=[], name_mapping={'application_id': 'applicationId', 'configuration_profile_id': 'configurationProfileId', 'content': 'content', 'content_type': 'contentType', 'description': 'description', 'latest_version_number': 'latestVersionNumber'})
class CfnHostedConfigurationVersionProps():
    def __init__(self, *, application_id: str, configuration_profile_id: str, content: str, content_type: str, description: typing.Optional[str]=None, latest_version_number: typing.Optional[jsii.Number]=None) -> None:
        """Properties for defining a ``AWS::AppConfig::HostedConfigurationVersion``.

        :param application_id: ``AWS::AppConfig::HostedConfigurationVersion.ApplicationId``.
        :param configuration_profile_id: ``AWS::AppConfig::HostedConfigurationVersion.ConfigurationProfileId``.
        :param content: ``AWS::AppConfig::HostedConfigurationVersion.Content``.
        :param content_type: ``AWS::AppConfig::HostedConfigurationVersion.ContentType``.
        :param description: ``AWS::AppConfig::HostedConfigurationVersion.Description``.
        :param latest_version_number: ``AWS::AppConfig::HostedConfigurationVersion.LatestVersionNumber``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-hostedconfigurationversion.html
        """
        self._values = {
            'application_id': application_id,
            'configuration_profile_id': configuration_profile_id,
            'content': content,
            'content_type': content_type,
        }
        if description is not None: self._values["description"] = description
        if latest_version_number is not None: self._values["latest_version_number"] = latest_version_number

    @builtins.property
    def application_id(self) -> str:
        """``AWS::AppConfig::HostedConfigurationVersion.ApplicationId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-hostedconfigurationversion.html#cfn-appconfig-hostedconfigurationversion-applicationid
        """
        return self._values.get('application_id')

    @builtins.property
    def configuration_profile_id(self) -> str:
        """``AWS::AppConfig::HostedConfigurationVersion.ConfigurationProfileId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-hostedconfigurationversion.html#cfn-appconfig-hostedconfigurationversion-configurationprofileid
        """
        return self._values.get('configuration_profile_id')

    @builtins.property
    def content(self) -> str:
        """``AWS::AppConfig::HostedConfigurationVersion.Content``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-hostedconfigurationversion.html#cfn-appconfig-hostedconfigurationversion-content
        """
        return self._values.get('content')

    @builtins.property
    def content_type(self) -> str:
        """``AWS::AppConfig::HostedConfigurationVersion.ContentType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-hostedconfigurationversion.html#cfn-appconfig-hostedconfigurationversion-contenttype
        """
        return self._values.get('content_type')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::AppConfig::HostedConfigurationVersion.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-hostedconfigurationversion.html#cfn-appconfig-hostedconfigurationversion-description
        """
        return self._values.get('description')

    @builtins.property
    def latest_version_number(self) -> typing.Optional[jsii.Number]:
        """``AWS::AppConfig::HostedConfigurationVersion.LatestVersionNumber``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-hostedconfigurationversion.html#cfn-appconfig-hostedconfigurationversion-latestversionnumber
        """
        return self._values.get('latest_version_number')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnHostedConfigurationVersionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CfnApplication",
    "CfnApplicationProps",
    "CfnConfigurationProfile",
    "CfnConfigurationProfileProps",
    "CfnDeployment",
    "CfnDeploymentProps",
    "CfnDeploymentStrategy",
    "CfnDeploymentStrategyProps",
    "CfnEnvironment",
    "CfnEnvironmentProps",
    "CfnHostedConfigurationVersion",
    "CfnHostedConfigurationVersionProps",
]

publication.publish()
