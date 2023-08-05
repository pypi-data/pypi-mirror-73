import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *


@jsii.data_type(jsii_type="monocdk-experiment.cloud_assembly_schema.AmiContextQuery", jsii_struct_bases=[], name_mapping={'account': 'account', 'filters': 'filters', 'region': 'region', 'owners': 'owners'})
class AmiContextQuery():
    def __init__(self, *, account: str, filters: typing.Mapping[str, typing.List[str]], region: str, owners: typing.Optional[typing.List[str]]=None) -> None:
        """Query to AMI context provider.

        :param account: Account to query.
        :param filters: Filters to DescribeImages call.
        :param region: Region to query.
        :param owners: Owners to DescribeImages call. Default: - All owners

        stability
        :stability: experimental
        """
        self._values = {
            'account': account,
            'filters': filters,
            'region': region,
        }
        if owners is not None: self._values["owners"] = owners

    @builtins.property
    def account(self) -> str:
        """Account to query.

        stability
        :stability: experimental
        """
        return self._values.get('account')

    @builtins.property
    def filters(self) -> typing.Mapping[str, typing.List[str]]:
        """Filters to DescribeImages call.

        stability
        :stability: experimental
        """
        return self._values.get('filters')

    @builtins.property
    def region(self) -> str:
        """Region to query.

        stability
        :stability: experimental
        """
        return self._values.get('region')

    @builtins.property
    def owners(self) -> typing.Optional[typing.List[str]]:
        """Owners to DescribeImages call.

        default
        :default: - All owners

        stability
        :stability: experimental
        """
        return self._values.get('owners')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AmiContextQuery(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.cloud_assembly_schema.ArtifactManifest", jsii_struct_bases=[], name_mapping={'type': 'type', 'dependencies': 'dependencies', 'environment': 'environment', 'metadata': 'metadata', 'properties': 'properties'})
class ArtifactManifest():
    def __init__(self, *, type: "ArtifactType", dependencies: typing.Optional[typing.List[str]]=None, environment: typing.Optional[str]=None, metadata: typing.Optional[typing.Mapping[str, typing.List["MetadataEntry"]]]=None, properties: typing.Optional[typing.Union["AwsCloudFormationStackProperties", "AssetManifestProperties", "TreeArtifactProperties", "NestedCloudAssemblyProperties"]]=None) -> None:
        """A manifest for a single artifact within the cloud assembly.

        :param type: The type of artifact.
        :param dependencies: IDs of artifacts that must be deployed before this artifact. Default: - no dependencies.
        :param environment: The environment into which this artifact is deployed. Default: - no envrionment.
        :param metadata: Associated metadata. Default: - no metadata.
        :param properties: The set of properties for this artifact (depends on type). Default: - no properties.

        stability
        :stability: experimental
        """
        self._values = {
            'type': type,
        }
        if dependencies is not None: self._values["dependencies"] = dependencies
        if environment is not None: self._values["environment"] = environment
        if metadata is not None: self._values["metadata"] = metadata
        if properties is not None: self._values["properties"] = properties

    @builtins.property
    def type(self) -> "ArtifactType":
        """The type of artifact.

        stability
        :stability: experimental
        """
        return self._values.get('type')

    @builtins.property
    def dependencies(self) -> typing.Optional[typing.List[str]]:
        """IDs of artifacts that must be deployed before this artifact.

        default
        :default: - no dependencies.

        stability
        :stability: experimental
        """
        return self._values.get('dependencies')

    @builtins.property
    def environment(self) -> typing.Optional[str]:
        """The environment into which this artifact is deployed.

        default
        :default: - no envrionment.

        stability
        :stability: experimental
        """
        return self._values.get('environment')

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[str, typing.List["MetadataEntry"]]]:
        """Associated metadata.

        default
        :default: - no metadata.

        stability
        :stability: experimental
        """
        return self._values.get('metadata')

    @builtins.property
    def properties(self) -> typing.Optional[typing.Union["AwsCloudFormationStackProperties", "AssetManifestProperties", "TreeArtifactProperties", "NestedCloudAssemblyProperties"]]:
        """The set of properties for this artifact (depends on type).

        default
        :default: - no properties.

        stability
        :stability: experimental
        """
        return self._values.get('properties')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ArtifactManifest(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.cloud_assembly_schema.ArtifactMetadataEntryType")
class ArtifactMetadataEntryType(enum.Enum):
    """Type of artifact metadata entry.

    stability
    :stability: experimental
    """
    ASSET = "ASSET"
    """Asset in metadata.

    stability
    :stability: experimental
    """
    INFO = "INFO"
    """Metadata key used to print INFO-level messages by the toolkit when an app is syntheized.

    stability
    :stability: experimental
    """
    WARN = "WARN"
    """Metadata key used to print WARNING-level messages by the toolkit when an app is syntheized.

    stability
    :stability: experimental
    """
    ERROR = "ERROR"
    """Metadata key used to print ERROR-level messages by the toolkit when an app is syntheized.

    stability
    :stability: experimental
    """
    LOGICAL_ID = "LOGICAL_ID"
    """Represents the CloudFormation logical ID of a resource at a certain path.

    stability
    :stability: experimental
    """
    STACK_TAGS = "STACK_TAGS"
    """Represents tags of a stack.

    stability
    :stability: experimental
    """

@jsii.enum(jsii_type="monocdk-experiment.cloud_assembly_schema.ArtifactType")
class ArtifactType(enum.Enum):
    """Type of cloud artifact.

    stability
    :stability: experimental
    """
    NONE = "NONE"
    """Stub required because of JSII.

    stability
    :stability: experimental
    """
    AWS_CLOUDFORMATION_STACK = "AWS_CLOUDFORMATION_STACK"
    """The artifact is an AWS CloudFormation stack.

    stability
    :stability: experimental
    """
    CDK_TREE = "CDK_TREE"
    """The artifact contains the CDK application's construct tree.

    stability
    :stability: experimental
    """
    ASSET_MANIFEST = "ASSET_MANIFEST"
    """Manifest for all assets in the Cloud Assembly.

    stability
    :stability: experimental
    """
    NESTED_CLOUD_ASSEMBLY = "NESTED_CLOUD_ASSEMBLY"
    """Nested Cloud Assembly.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="monocdk-experiment.cloud_assembly_schema.AssemblyManifest", jsii_struct_bases=[], name_mapping={'version': 'version', 'artifacts': 'artifacts', 'missing': 'missing', 'runtime': 'runtime'})
class AssemblyManifest():
    def __init__(self, *, version: str, artifacts: typing.Optional[typing.Mapping[str, "ArtifactManifest"]]=None, missing: typing.Optional[typing.List["MissingContext"]]=None, runtime: typing.Optional["RuntimeInfo"]=None) -> None:
        """A manifest which describes the cloud assembly.

        :param version: Protocol version.
        :param artifacts: The set of artifacts in this assembly. Default: - no artifacts.
        :param missing: Missing context information. If this field has values, it means that the cloud assembly is not complete and should not be deployed. Default: - no missing context.
        :param runtime: Runtime information. Default: - no info.

        stability
        :stability: experimental
        """
        if isinstance(runtime, dict): runtime = RuntimeInfo(**runtime)
        self._values = {
            'version': version,
        }
        if artifacts is not None: self._values["artifacts"] = artifacts
        if missing is not None: self._values["missing"] = missing
        if runtime is not None: self._values["runtime"] = runtime

    @builtins.property
    def version(self) -> str:
        """Protocol version.

        stability
        :stability: experimental
        """
        return self._values.get('version')

    @builtins.property
    def artifacts(self) -> typing.Optional[typing.Mapping[str, "ArtifactManifest"]]:
        """The set of artifacts in this assembly.

        default
        :default: - no artifacts.

        stability
        :stability: experimental
        """
        return self._values.get('artifacts')

    @builtins.property
    def missing(self) -> typing.Optional[typing.List["MissingContext"]]:
        """Missing context information.

        If this field has values, it means that the
        cloud assembly is not complete and should not be deployed.

        default
        :default: - no missing context.

        stability
        :stability: experimental
        """
        return self._values.get('missing')

    @builtins.property
    def runtime(self) -> typing.Optional["RuntimeInfo"]:
        """Runtime information.

        default
        :default: - no info.

        stability
        :stability: experimental
        """
        return self._values.get('runtime')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AssemblyManifest(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.cloud_assembly_schema.AssetManifest", jsii_struct_bases=[], name_mapping={'version': 'version', 'docker_images': 'dockerImages', 'files': 'files'})
class AssetManifest():
    def __init__(self, *, version: str, docker_images: typing.Optional[typing.Mapping[str, "DockerImageAsset"]]=None, files: typing.Optional[typing.Mapping[str, "FileAsset"]]=None) -> None:
        """Definitions for the asset manifest.

        :param version: Version of the manifest.
        :param docker_images: The Docker image assets in this manifest. Default: - No Docker images
        :param files: The file assets in this manifest. Default: - No files

        stability
        :stability: experimental
        """
        self._values = {
            'version': version,
        }
        if docker_images is not None: self._values["docker_images"] = docker_images
        if files is not None: self._values["files"] = files

    @builtins.property
    def version(self) -> str:
        """Version of the manifest.

        stability
        :stability: experimental
        """
        return self._values.get('version')

    @builtins.property
    def docker_images(self) -> typing.Optional[typing.Mapping[str, "DockerImageAsset"]]:
        """The Docker image assets in this manifest.

        default
        :default: - No Docker images

        stability
        :stability: experimental
        """
        return self._values.get('docker_images')

    @builtins.property
    def files(self) -> typing.Optional[typing.Mapping[str, "FileAsset"]]:
        """The file assets in this manifest.

        default
        :default: - No files

        stability
        :stability: experimental
        """
        return self._values.get('files')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AssetManifest(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.cloud_assembly_schema.AssetManifestProperties", jsii_struct_bases=[], name_mapping={'file': 'file', 'requires_bootstrap_stack_version': 'requiresBootstrapStackVersion'})
class AssetManifestProperties():
    def __init__(self, *, file: str, requires_bootstrap_stack_version: typing.Optional[jsii.Number]=None) -> None:
        """Artifact properties for the Asset Manifest.

        :param file: Filename of the asset manifest.
        :param requires_bootstrap_stack_version: Version of bootstrap stack required to deploy this stack. Default: - Version 1 (basic modern bootstrap stack)

        stability
        :stability: experimental
        """
        self._values = {
            'file': file,
        }
        if requires_bootstrap_stack_version is not None: self._values["requires_bootstrap_stack_version"] = requires_bootstrap_stack_version

    @builtins.property
    def file(self) -> str:
        """Filename of the asset manifest.

        stability
        :stability: experimental
        """
        return self._values.get('file')

    @builtins.property
    def requires_bootstrap_stack_version(self) -> typing.Optional[jsii.Number]:
        """Version of bootstrap stack required to deploy this stack.

        default
        :default: - Version 1 (basic modern bootstrap stack)

        stability
        :stability: experimental
        """
        return self._values.get('requires_bootstrap_stack_version')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AssetManifestProperties(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.cloud_assembly_schema.AvailabilityZonesContextQuery", jsii_struct_bases=[], name_mapping={'account': 'account', 'region': 'region'})
class AvailabilityZonesContextQuery():
    def __init__(self, *, account: str, region: str) -> None:
        """Query to availability zone context provider.

        :param account: Query account.
        :param region: Query region.

        stability
        :stability: experimental
        """
        self._values = {
            'account': account,
            'region': region,
        }

    @builtins.property
    def account(self) -> str:
        """Query account.

        stability
        :stability: experimental
        """
        return self._values.get('account')

    @builtins.property
    def region(self) -> str:
        """Query region.

        stability
        :stability: experimental
        """
        return self._values.get('region')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AvailabilityZonesContextQuery(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.cloud_assembly_schema.AwsCloudFormationStackProperties", jsii_struct_bases=[], name_mapping={'template_file': 'templateFile', 'assume_role_arn': 'assumeRoleArn', 'cloud_formation_execution_role_arn': 'cloudFormationExecutionRoleArn', 'parameters': 'parameters', 'requires_bootstrap_stack_version': 'requiresBootstrapStackVersion', 'stack_name': 'stackName', 'stack_template_asset_object_url': 'stackTemplateAssetObjectUrl', 'termination_protection': 'terminationProtection'})
class AwsCloudFormationStackProperties():
    def __init__(self, *, template_file: str, assume_role_arn: typing.Optional[str]=None, cloud_formation_execution_role_arn: typing.Optional[str]=None, parameters: typing.Optional[typing.Mapping[str, str]]=None, requires_bootstrap_stack_version: typing.Optional[jsii.Number]=None, stack_name: typing.Optional[str]=None, stack_template_asset_object_url: typing.Optional[str]=None, termination_protection: typing.Optional[bool]=None) -> None:
        """Artifact properties for CloudFormation stacks.

        :param template_file: A file relative to the assembly root which contains the CloudFormation template for this stack.
        :param assume_role_arn: The role that needs to be assumed to deploy the stack. Default: - No role is assumed (current credentials are used)
        :param cloud_formation_execution_role_arn: The role that is passed to CloudFormation to execute the change set. Default: - No role is passed (currently assumed role/credentials are used)
        :param parameters: Values for CloudFormation stack parameters that should be passed when the stack is deployed. Default: - No parameters
        :param requires_bootstrap_stack_version: Version of bootstrap stack required to deploy this stack. Default: - No bootstrap stack required
        :param stack_name: The name to use for the CloudFormation stack. Default: - name derived from artifact ID
        :param stack_template_asset_object_url: If the stack template has already been included in the asset manifest, its asset URL. Default: - Not uploaded yet, upload just before deploying
        :param termination_protection: Whether to enable termination protection for this stack. Default: false

        stability
        :stability: experimental
        """
        self._values = {
            'template_file': template_file,
        }
        if assume_role_arn is not None: self._values["assume_role_arn"] = assume_role_arn
        if cloud_formation_execution_role_arn is not None: self._values["cloud_formation_execution_role_arn"] = cloud_formation_execution_role_arn
        if parameters is not None: self._values["parameters"] = parameters
        if requires_bootstrap_stack_version is not None: self._values["requires_bootstrap_stack_version"] = requires_bootstrap_stack_version
        if stack_name is not None: self._values["stack_name"] = stack_name
        if stack_template_asset_object_url is not None: self._values["stack_template_asset_object_url"] = stack_template_asset_object_url
        if termination_protection is not None: self._values["termination_protection"] = termination_protection

    @builtins.property
    def template_file(self) -> str:
        """A file relative to the assembly root which contains the CloudFormation template for this stack.

        stability
        :stability: experimental
        """
        return self._values.get('template_file')

    @builtins.property
    def assume_role_arn(self) -> typing.Optional[str]:
        """The role that needs to be assumed to deploy the stack.

        default
        :default: - No role is assumed (current credentials are used)

        stability
        :stability: experimental
        """
        return self._values.get('assume_role_arn')

    @builtins.property
    def cloud_formation_execution_role_arn(self) -> typing.Optional[str]:
        """The role that is passed to CloudFormation to execute the change set.

        default
        :default: - No role is passed (currently assumed role/credentials are used)

        stability
        :stability: experimental
        """
        return self._values.get('cloud_formation_execution_role_arn')

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Values for CloudFormation stack parameters that should be passed when the stack is deployed.

        default
        :default: - No parameters

        stability
        :stability: experimental
        """
        return self._values.get('parameters')

    @builtins.property
    def requires_bootstrap_stack_version(self) -> typing.Optional[jsii.Number]:
        """Version of bootstrap stack required to deploy this stack.

        default
        :default: - No bootstrap stack required

        stability
        :stability: experimental
        """
        return self._values.get('requires_bootstrap_stack_version')

    @builtins.property
    def stack_name(self) -> typing.Optional[str]:
        """The name to use for the CloudFormation stack.

        default
        :default: - name derived from artifact ID

        stability
        :stability: experimental
        """
        return self._values.get('stack_name')

    @builtins.property
    def stack_template_asset_object_url(self) -> typing.Optional[str]:
        """If the stack template has already been included in the asset manifest, its asset URL.

        default
        :default: - Not uploaded yet, upload just before deploying

        stability
        :stability: experimental
        """
        return self._values.get('stack_template_asset_object_url')

    @builtins.property
    def termination_protection(self) -> typing.Optional[bool]:
        """Whether to enable termination protection for this stack.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('termination_protection')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AwsCloudFormationStackProperties(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.cloud_assembly_schema.AwsDestination", jsii_struct_bases=[], name_mapping={'assume_role_arn': 'assumeRoleArn', 'assume_role_external_id': 'assumeRoleExternalId', 'region': 'region'})
class AwsDestination():
    def __init__(self, *, assume_role_arn: typing.Optional[str]=None, assume_role_external_id: typing.Optional[str]=None, region: typing.Optional[str]=None) -> None:
        """Destination for assets that need to be uploaded to AWS.

        :param assume_role_arn: The role that needs to be assumed while publishing this asset. Default: - No role will be assumed
        :param assume_role_external_id: The ExternalId that needs to be supplied while assuming this role. Default: - No ExternalId will be supplied
        :param region: The region where this asset will need to be published. Default: - Current region

        stability
        :stability: experimental
        """
        self._values = {
        }
        if assume_role_arn is not None: self._values["assume_role_arn"] = assume_role_arn
        if assume_role_external_id is not None: self._values["assume_role_external_id"] = assume_role_external_id
        if region is not None: self._values["region"] = region

    @builtins.property
    def assume_role_arn(self) -> typing.Optional[str]:
        """The role that needs to be assumed while publishing this asset.

        default
        :default: - No role will be assumed

        stability
        :stability: experimental
        """
        return self._values.get('assume_role_arn')

    @builtins.property
    def assume_role_external_id(self) -> typing.Optional[str]:
        """The ExternalId that needs to be supplied while assuming this role.

        default
        :default: - No ExternalId will be supplied

        stability
        :stability: experimental
        """
        return self._values.get('assume_role_external_id')

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """The region where this asset will need to be published.

        default
        :default: - Current region

        stability
        :stability: experimental
        """
        return self._values.get('region')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AwsDestination(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.cloud_assembly_schema.ContainerImageAssetMetadataEntry", jsii_struct_bases=[], name_mapping={'id': 'id', 'packaging': 'packaging', 'path': 'path', 'source_hash': 'sourceHash', 'build_args': 'buildArgs', 'file': 'file', 'image_name_parameter': 'imageNameParameter', 'image_tag': 'imageTag', 'repository_name': 'repositoryName', 'target': 'target'})
class ContainerImageAssetMetadataEntry():
    def __init__(self, *, id: str, packaging: str, path: str, source_hash: str, build_args: typing.Optional[typing.Mapping[str, str]]=None, file: typing.Optional[str]=None, image_name_parameter: typing.Optional[str]=None, image_tag: typing.Optional[str]=None, repository_name: typing.Optional[str]=None, target: typing.Optional[str]=None) -> None:
        """Metadata Entry spec for container images.

        :param id: Logical identifier for the asset.
        :param packaging: Type of asset.
        :param path: Path on disk to the asset.
        :param source_hash: The hash of the asset source.
        :param build_args: Build args to pass to the ``docker build`` command. Default: no build args are passed
        :param file: Path to the Dockerfile (relative to the directory). Default: - no file is passed
        :param image_name_parameter: ECR Repository name and repo digest (separated by "@sha256:") where this image is stored. Default: undefined If not specified, ``repositoryName`` and ``imageTag`` are required because otherwise how will the stack know where to find the asset, ha?
        :param image_tag: The docker image tag to use for tagging pushed images. This field is required if ``imageParameterName`` is ommited (otherwise, the app won't be able to find the image). Default: - this parameter is REQUIRED after 1.21.0
        :param repository_name: ECR repository name, if omitted a default name based on the asset's ID is used instead. Specify this property if you need to statically address the image, e.g. from a Kubernetes Pod. Note, this is only the repository name, without the registry and the tag parts. Default: - this parameter is REQUIRED after 1.21.0
        :param target: Docker target to build to. Default: no build target

        stability
        :stability: experimental
        """
        self._values = {
            'id': id,
            'packaging': packaging,
            'path': path,
            'source_hash': source_hash,
        }
        if build_args is not None: self._values["build_args"] = build_args
        if file is not None: self._values["file"] = file
        if image_name_parameter is not None: self._values["image_name_parameter"] = image_name_parameter
        if image_tag is not None: self._values["image_tag"] = image_tag
        if repository_name is not None: self._values["repository_name"] = repository_name
        if target is not None: self._values["target"] = target

    @builtins.property
    def id(self) -> str:
        """Logical identifier for the asset.

        stability
        :stability: experimental
        """
        return self._values.get('id')

    @builtins.property
    def packaging(self) -> str:
        """Type of asset.

        stability
        :stability: experimental
        """
        return self._values.get('packaging')

    @builtins.property
    def path(self) -> str:
        """Path on disk to the asset.

        stability
        :stability: experimental
        """
        return self._values.get('path')

    @builtins.property
    def source_hash(self) -> str:
        """The hash of the asset source.

        stability
        :stability: experimental
        """
        return self._values.get('source_hash')

    @builtins.property
    def build_args(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Build args to pass to the ``docker build`` command.

        default
        :default: no build args are passed

        stability
        :stability: experimental
        """
        return self._values.get('build_args')

    @builtins.property
    def file(self) -> typing.Optional[str]:
        """Path to the Dockerfile (relative to the directory).

        default
        :default: - no file is passed

        stability
        :stability: experimental
        """
        return self._values.get('file')

    @builtins.property
    def image_name_parameter(self) -> typing.Optional[str]:
        """ECR Repository name and repo digest (separated by "@sha256:") where this image is stored.

        default
        :default:

        undefined If not specified, ``repositoryName`` and ``imageTag`` are
        required because otherwise how will the stack know where to find the asset,
        ha?

        deprecated
        :deprecated:

        specify ``repositoryName`` and ``imageTag`` instead, and then you
        know where the image will go.

        stability
        :stability: deprecated
        """
        return self._values.get('image_name_parameter')

    @builtins.property
    def image_tag(self) -> typing.Optional[str]:
        """The docker image tag to use for tagging pushed images.

        This field is
        required if ``imageParameterName`` is ommited (otherwise, the app won't be
        able to find the image).

        default
        :default: - this parameter is REQUIRED after 1.21.0

        stability
        :stability: experimental
        """
        return self._values.get('image_tag')

    @builtins.property
    def repository_name(self) -> typing.Optional[str]:
        """ECR repository name, if omitted a default name based on the asset's ID is used instead.

        Specify this property if you need to statically address the
        image, e.g. from a Kubernetes Pod. Note, this is only the repository name,
        without the registry and the tag parts.

        default
        :default: - this parameter is REQUIRED after 1.21.0

        stability
        :stability: experimental
        """
        return self._values.get('repository_name')

    @builtins.property
    def target(self) -> typing.Optional[str]:
        """Docker target to build to.

        default
        :default: no build target

        stability
        :stability: experimental
        """
        return self._values.get('target')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ContainerImageAssetMetadataEntry(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.cloud_assembly_schema.ContextProvider")
class ContextProvider(enum.Enum):
    """Identifier for the context provider.

    stability
    :stability: experimental
    """
    AMI_PROVIDER = "AMI_PROVIDER"
    """AMI provider.

    stability
    :stability: experimental
    """
    AVAILABILITY_ZONE_PROVIDER = "AVAILABILITY_ZONE_PROVIDER"
    """AZ provider.

    stability
    :stability: experimental
    """
    HOSTED_ZONE_PROVIDER = "HOSTED_ZONE_PROVIDER"
    """Route53 Hosted Zone provider.

    stability
    :stability: experimental
    """
    SSM_PARAMETER_PROVIDER = "SSM_PARAMETER_PROVIDER"
    """SSM Parameter Provider.

    stability
    :stability: experimental
    """
    VPC_PROVIDER = "VPC_PROVIDER"
    """VPC Provider.

    stability
    :stability: experimental
    """
    ENDPOINT_SERVICE_AVAILABILITY_ZONE_PROVIDER = "ENDPOINT_SERVICE_AVAILABILITY_ZONE_PROVIDER"
    """VPC Endpoint Service AZ Provider.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="monocdk-experiment.cloud_assembly_schema.DockerImageAsset", jsii_struct_bases=[], name_mapping={'destinations': 'destinations', 'source': 'source'})
class DockerImageAsset():
    def __init__(self, *, destinations: typing.Mapping[str, "DockerImageDestination"], source: "DockerImageSource") -> None:
        """A file asset.

        :param destinations: Destinations for this file asset.
        :param source: Source description for file assets.

        stability
        :stability: experimental
        """
        if isinstance(source, dict): source = DockerImageSource(**source)
        self._values = {
            'destinations': destinations,
            'source': source,
        }

    @builtins.property
    def destinations(self) -> typing.Mapping[str, "DockerImageDestination"]:
        """Destinations for this file asset.

        stability
        :stability: experimental
        """
        return self._values.get('destinations')

    @builtins.property
    def source(self) -> "DockerImageSource":
        """Source description for file assets.

        stability
        :stability: experimental
        """
        return self._values.get('source')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DockerImageAsset(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.cloud_assembly_schema.DockerImageDestination", jsii_struct_bases=[AwsDestination], name_mapping={'assume_role_arn': 'assumeRoleArn', 'assume_role_external_id': 'assumeRoleExternalId', 'region': 'region', 'image_tag': 'imageTag', 'repository_name': 'repositoryName'})
class DockerImageDestination(AwsDestination):
    def __init__(self, *, assume_role_arn: typing.Optional[str]=None, assume_role_external_id: typing.Optional[str]=None, region: typing.Optional[str]=None, image_tag: str, repository_name: str) -> None:
        """Where to publish docker images.

        :param assume_role_arn: The role that needs to be assumed while publishing this asset. Default: - No role will be assumed
        :param assume_role_external_id: The ExternalId that needs to be supplied while assuming this role. Default: - No ExternalId will be supplied
        :param region: The region where this asset will need to be published. Default: - Current region
        :param image_tag: Tag of the image to publish.
        :param repository_name: Name of the ECR repository to publish to.

        stability
        :stability: experimental
        """
        self._values = {
            'image_tag': image_tag,
            'repository_name': repository_name,
        }
        if assume_role_arn is not None: self._values["assume_role_arn"] = assume_role_arn
        if assume_role_external_id is not None: self._values["assume_role_external_id"] = assume_role_external_id
        if region is not None: self._values["region"] = region

    @builtins.property
    def assume_role_arn(self) -> typing.Optional[str]:
        """The role that needs to be assumed while publishing this asset.

        default
        :default: - No role will be assumed

        stability
        :stability: experimental
        """
        return self._values.get('assume_role_arn')

    @builtins.property
    def assume_role_external_id(self) -> typing.Optional[str]:
        """The ExternalId that needs to be supplied while assuming this role.

        default
        :default: - No ExternalId will be supplied

        stability
        :stability: experimental
        """
        return self._values.get('assume_role_external_id')

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """The region where this asset will need to be published.

        default
        :default: - Current region

        stability
        :stability: experimental
        """
        return self._values.get('region')

    @builtins.property
    def image_tag(self) -> str:
        """Tag of the image to publish.

        stability
        :stability: experimental
        """
        return self._values.get('image_tag')

    @builtins.property
    def repository_name(self) -> str:
        """Name of the ECR repository to publish to.

        stability
        :stability: experimental
        """
        return self._values.get('repository_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DockerImageDestination(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.cloud_assembly_schema.DockerImageSource", jsii_struct_bases=[], name_mapping={'directory': 'directory', 'docker_build_args': 'dockerBuildArgs', 'docker_build_target': 'dockerBuildTarget', 'docker_file': 'dockerFile'})
class DockerImageSource():
    def __init__(self, *, directory: str, docker_build_args: typing.Optional[typing.Mapping[str, str]]=None, docker_build_target: typing.Optional[str]=None, docker_file: typing.Optional[str]=None) -> None:
        """Properties for how to produce a Docker image from a source.

        :param directory: The directory containing the Docker image build instructions. This path is relative to the asset manifest location.
        :param docker_build_args: Additional build arguments. Default: - No additional build arguments
        :param docker_build_target: Target build stage in a Dockerfile with multiple build stages. Default: - The last stage in the Dockerfile
        :param docker_file: The name of the file with build instructions. Default: "Dockerfile"

        stability
        :stability: experimental
        """
        self._values = {
            'directory': directory,
        }
        if docker_build_args is not None: self._values["docker_build_args"] = docker_build_args
        if docker_build_target is not None: self._values["docker_build_target"] = docker_build_target
        if docker_file is not None: self._values["docker_file"] = docker_file

    @builtins.property
    def directory(self) -> str:
        """The directory containing the Docker image build instructions.

        This path is relative to the asset manifest location.

        stability
        :stability: experimental
        """
        return self._values.get('directory')

    @builtins.property
    def docker_build_args(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Additional build arguments.

        default
        :default: - No additional build arguments

        stability
        :stability: experimental
        """
        return self._values.get('docker_build_args')

    @builtins.property
    def docker_build_target(self) -> typing.Optional[str]:
        """Target build stage in a Dockerfile with multiple build stages.

        default
        :default: - The last stage in the Dockerfile

        stability
        :stability: experimental
        """
        return self._values.get('docker_build_target')

    @builtins.property
    def docker_file(self) -> typing.Optional[str]:
        """The name of the file with build instructions.

        default
        :default: "Dockerfile"

        stability
        :stability: experimental
        """
        return self._values.get('docker_file')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DockerImageSource(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.cloud_assembly_schema.EndpointServiceAvailabilityZonesContextQuery", jsii_struct_bases=[], name_mapping={'account': 'account', 'region': 'region', 'service_name': 'serviceName'})
class EndpointServiceAvailabilityZonesContextQuery():
    def __init__(self, *, account: str, region: str, service_name: str) -> None:
        """Query to endpoint service context provider.

        :param account: Query account.
        :param region: Query region.
        :param service_name: Query service name.

        stability
        :stability: experimental
        """
        self._values = {
            'account': account,
            'region': region,
            'service_name': service_name,
        }

    @builtins.property
    def account(self) -> str:
        """Query account.

        stability
        :stability: experimental
        """
        return self._values.get('account')

    @builtins.property
    def region(self) -> str:
        """Query region.

        stability
        :stability: experimental
        """
        return self._values.get('region')

    @builtins.property
    def service_name(self) -> str:
        """Query service name.

        stability
        :stability: experimental
        """
        return self._values.get('service_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EndpointServiceAvailabilityZonesContextQuery(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.cloud_assembly_schema.FileAsset", jsii_struct_bases=[], name_mapping={'destinations': 'destinations', 'source': 'source'})
class FileAsset():
    def __init__(self, *, destinations: typing.Mapping[str, "FileDestination"], source: "FileSource") -> None:
        """A file asset.

        :param destinations: Destinations for this file asset.
        :param source: Source description for file assets.

        stability
        :stability: experimental
        """
        if isinstance(source, dict): source = FileSource(**source)
        self._values = {
            'destinations': destinations,
            'source': source,
        }

    @builtins.property
    def destinations(self) -> typing.Mapping[str, "FileDestination"]:
        """Destinations for this file asset.

        stability
        :stability: experimental
        """
        return self._values.get('destinations')

    @builtins.property
    def source(self) -> "FileSource":
        """Source description for file assets.

        stability
        :stability: experimental
        """
        return self._values.get('source')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FileAsset(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.cloud_assembly_schema.FileAssetMetadataEntry", jsii_struct_bases=[], name_mapping={'artifact_hash_parameter': 'artifactHashParameter', 'id': 'id', 'packaging': 'packaging', 'path': 'path', 's3_bucket_parameter': 's3BucketParameter', 's3_key_parameter': 's3KeyParameter', 'source_hash': 'sourceHash'})
class FileAssetMetadataEntry():
    def __init__(self, *, artifact_hash_parameter: str, id: str, packaging: str, path: str, s3_bucket_parameter: str, s3_key_parameter: str, source_hash: str) -> None:
        """Metadata Entry spec for files.

        :param artifact_hash_parameter: The name of the parameter where the hash of the bundled asset should be passed in.
        :param id: Logical identifier for the asset.
        :param packaging: Requested packaging style.
        :param path: Path on disk to the asset.
        :param s3_bucket_parameter: Name of parameter where S3 bucket should be passed in.
        :param s3_key_parameter: Name of parameter where S3 key should be passed in.
        :param source_hash: The hash of the asset source.

        stability
        :stability: experimental
        """
        self._values = {
            'artifact_hash_parameter': artifact_hash_parameter,
            'id': id,
            'packaging': packaging,
            'path': path,
            's3_bucket_parameter': s3_bucket_parameter,
            's3_key_parameter': s3_key_parameter,
            'source_hash': source_hash,
        }

    @builtins.property
    def artifact_hash_parameter(self) -> str:
        """The name of the parameter where the hash of the bundled asset should be passed in.

        stability
        :stability: experimental
        """
        return self._values.get('artifact_hash_parameter')

    @builtins.property
    def id(self) -> str:
        """Logical identifier for the asset.

        stability
        :stability: experimental
        """
        return self._values.get('id')

    @builtins.property
    def packaging(self) -> str:
        """Requested packaging style.

        stability
        :stability: experimental
        """
        return self._values.get('packaging')

    @builtins.property
    def path(self) -> str:
        """Path on disk to the asset.

        stability
        :stability: experimental
        """
        return self._values.get('path')

    @builtins.property
    def s3_bucket_parameter(self) -> str:
        """Name of parameter where S3 bucket should be passed in.

        stability
        :stability: experimental
        """
        return self._values.get('s3_bucket_parameter')

    @builtins.property
    def s3_key_parameter(self) -> str:
        """Name of parameter where S3 key should be passed in.

        stability
        :stability: experimental
        """
        return self._values.get('s3_key_parameter')

    @builtins.property
    def source_hash(self) -> str:
        """The hash of the asset source.

        stability
        :stability: experimental
        """
        return self._values.get('source_hash')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FileAssetMetadataEntry(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.cloud_assembly_schema.FileAssetPackaging")
class FileAssetPackaging(enum.Enum):
    """Packaging strategy for file assets.

    stability
    :stability: experimental
    """
    FILE = "FILE"
    """Upload the given path as a file.

    stability
    :stability: experimental
    """
    ZIP_DIRECTORY = "ZIP_DIRECTORY"
    """The given path is a directory, zip it and upload.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="monocdk-experiment.cloud_assembly_schema.FileDestination", jsii_struct_bases=[AwsDestination], name_mapping={'assume_role_arn': 'assumeRoleArn', 'assume_role_external_id': 'assumeRoleExternalId', 'region': 'region', 'bucket_name': 'bucketName', 'object_key': 'objectKey'})
class FileDestination(AwsDestination):
    def __init__(self, *, assume_role_arn: typing.Optional[str]=None, assume_role_external_id: typing.Optional[str]=None, region: typing.Optional[str]=None, bucket_name: str, object_key: str) -> None:
        """Where in S3 a file asset needs to be published.

        :param assume_role_arn: The role that needs to be assumed while publishing this asset. Default: - No role will be assumed
        :param assume_role_external_id: The ExternalId that needs to be supplied while assuming this role. Default: - No ExternalId will be supplied
        :param region: The region where this asset will need to be published. Default: - Current region
        :param bucket_name: The name of the bucket.
        :param object_key: The destination object key.

        stability
        :stability: experimental
        """
        self._values = {
            'bucket_name': bucket_name,
            'object_key': object_key,
        }
        if assume_role_arn is not None: self._values["assume_role_arn"] = assume_role_arn
        if assume_role_external_id is not None: self._values["assume_role_external_id"] = assume_role_external_id
        if region is not None: self._values["region"] = region

    @builtins.property
    def assume_role_arn(self) -> typing.Optional[str]:
        """The role that needs to be assumed while publishing this asset.

        default
        :default: - No role will be assumed

        stability
        :stability: experimental
        """
        return self._values.get('assume_role_arn')

    @builtins.property
    def assume_role_external_id(self) -> typing.Optional[str]:
        """The ExternalId that needs to be supplied while assuming this role.

        default
        :default: - No ExternalId will be supplied

        stability
        :stability: experimental
        """
        return self._values.get('assume_role_external_id')

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """The region where this asset will need to be published.

        default
        :default: - Current region

        stability
        :stability: experimental
        """
        return self._values.get('region')

    @builtins.property
    def bucket_name(self) -> str:
        """The name of the bucket.

        stability
        :stability: experimental
        """
        return self._values.get('bucket_name')

    @builtins.property
    def object_key(self) -> str:
        """The destination object key.

        stability
        :stability: experimental
        """
        return self._values.get('object_key')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FileDestination(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.cloud_assembly_schema.FileSource", jsii_struct_bases=[], name_mapping={'path': 'path', 'packaging': 'packaging'})
class FileSource():
    def __init__(self, *, path: str, packaging: typing.Optional["FileAssetPackaging"]=None) -> None:
        """Describe the source of a file asset.

        :param path: The filesystem object to upload. This path is relative to the asset manifest location.
        :param packaging: Packaging method. Default: FILE

        stability
        :stability: experimental
        """
        self._values = {
            'path': path,
        }
        if packaging is not None: self._values["packaging"] = packaging

    @builtins.property
    def path(self) -> str:
        """The filesystem object to upload.

        This path is relative to the asset manifest location.

        stability
        :stability: experimental
        """
        return self._values.get('path')

    @builtins.property
    def packaging(self) -> typing.Optional["FileAssetPackaging"]:
        """Packaging method.

        default
        :default: FILE

        stability
        :stability: experimental
        """
        return self._values.get('packaging')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FileSource(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.cloud_assembly_schema.HostedZoneContextQuery", jsii_struct_bases=[], name_mapping={'account': 'account', 'domain_name': 'domainName', 'region': 'region', 'private_zone': 'privateZone', 'vpc_id': 'vpcId'})
class HostedZoneContextQuery():
    def __init__(self, *, account: str, domain_name: str, region: str, private_zone: typing.Optional[bool]=None, vpc_id: typing.Optional[str]=None) -> None:
        """Query to hosted zone context provider.

        :param account: Query account.
        :param domain_name: The domain name e.g. example.com to lookup.
        :param region: Query region.
        :param private_zone: True if the zone you want to find is a private hosted zone. Default: false
        :param vpc_id: The VPC ID to that the private zone must be associated with. If you provide VPC ID and privateZone is false, this will return no results and raise an error. Default: - Required if privateZone=true

        stability
        :stability: experimental
        """
        self._values = {
            'account': account,
            'domain_name': domain_name,
            'region': region,
        }
        if private_zone is not None: self._values["private_zone"] = private_zone
        if vpc_id is not None: self._values["vpc_id"] = vpc_id

    @builtins.property
    def account(self) -> str:
        """Query account.

        stability
        :stability: experimental
        """
        return self._values.get('account')

    @builtins.property
    def domain_name(self) -> str:
        """The domain name e.g. example.com to lookup.

        stability
        :stability: experimental
        """
        return self._values.get('domain_name')

    @builtins.property
    def region(self) -> str:
        """Query region.

        stability
        :stability: experimental
        """
        return self._values.get('region')

    @builtins.property
    def private_zone(self) -> typing.Optional[bool]:
        """True if the zone you want to find is a private hosted zone.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('private_zone')

    @builtins.property
    def vpc_id(self) -> typing.Optional[str]:
        """The VPC ID to that the private zone must be associated with.

        If you provide VPC ID and privateZone is false, this will return no results
        and raise an error.

        default
        :default: - Required if privateZone=true

        stability
        :stability: experimental
        """
        return self._values.get('vpc_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'HostedZoneContextQuery(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class Manifest(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.cloud_assembly_schema.Manifest"):
    """Protocol utility class.

    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="load")
    @builtins.classmethod
    def load(cls, file_path: str) -> "AssemblyManifest":
        """Deprecated.

        :param file_path: -

        deprecated
        :deprecated: use ``loadAssemblyManifest()``

        stability
        :stability: deprecated
        """
        return jsii.sinvoke(cls, "load", [file_path])

    @jsii.member(jsii_name="loadAssemblyManifest")
    @builtins.classmethod
    def load_assembly_manifest(cls, file_path: str) -> "AssemblyManifest":
        """Load and validates the cloud assembly manifest from file.

        :param file_path: - path to the manifest file.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "loadAssemblyManifest", [file_path])

    @jsii.member(jsii_name="loadAssetManifest")
    @builtins.classmethod
    def load_asset_manifest(cls, file_path: str) -> "AssetManifest":
        """Load and validates the asset manifest from file.

        :param file_path: - path to the manifest file.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "loadAssetManifest", [file_path])

    @jsii.member(jsii_name="save")
    @builtins.classmethod
    def save(cls, manifest: "AssemblyManifest", file_path: str) -> None:
        """Deprecated.

        :param manifest: -
        :param file_path: -

        deprecated
        :deprecated: use ``saveAssemblyManifest()``

        stability
        :stability: deprecated
        """
        return jsii.sinvoke(cls, "save", [manifest, file_path])

    @jsii.member(jsii_name="saveAssemblyManifest")
    @builtins.classmethod
    def save_assembly_manifest(cls, manifest: "AssemblyManifest", file_path: str) -> None:
        """Validates and saves the cloud assembly manifest to file.

        :param manifest: - manifest.
        :param file_path: - output file path.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "saveAssemblyManifest", [manifest, file_path])

    @jsii.member(jsii_name="saveAssetManifest")
    @builtins.classmethod
    def save_asset_manifest(cls, manifest: "AssetManifest", file_path: str) -> None:
        """Validates and saves the asset manifest to file.

        :param manifest: - manifest.
        :param file_path: - output file path.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "saveAssetManifest", [manifest, file_path])

    @jsii.member(jsii_name="version")
    @builtins.classmethod
    def version(cls) -> str:
        """Fetch the current schema version number.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "version", [])


@jsii.data_type(jsii_type="monocdk-experiment.cloud_assembly_schema.MetadataEntry", jsii_struct_bases=[], name_mapping={'type': 'type', 'data': 'data', 'trace': 'trace'})
class MetadataEntry():
    def __init__(self, *, type: str, data: typing.Optional[typing.Union[str, "FileAssetMetadataEntry", "ContainerImageAssetMetadataEntry", typing.List["Tag"]]]=None, trace: typing.Optional[typing.List[str]]=None) -> None:
        """A metadata entry in a cloud assembly artifact.

        :param type: The type of the metadata entry.
        :param data: The data. Default: - no data.
        :param trace: A stack trace for when the entry was created. Default: - no trace.

        stability
        :stability: experimental
        """
        self._values = {
            'type': type,
        }
        if data is not None: self._values["data"] = data
        if trace is not None: self._values["trace"] = trace

    @builtins.property
    def type(self) -> str:
        """The type of the metadata entry.

        stability
        :stability: experimental
        """
        return self._values.get('type')

    @builtins.property
    def data(self) -> typing.Optional[typing.Union[str, "FileAssetMetadataEntry", "ContainerImageAssetMetadataEntry", typing.List["Tag"]]]:
        """The data.

        default
        :default: - no data.

        stability
        :stability: experimental
        """
        return self._values.get('data')

    @builtins.property
    def trace(self) -> typing.Optional[typing.List[str]]:
        """A stack trace for when the entry was created.

        default
        :default: - no trace.

        stability
        :stability: experimental
        """
        return self._values.get('trace')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'MetadataEntry(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.cloud_assembly_schema.MissingContext", jsii_struct_bases=[], name_mapping={'key': 'key', 'props': 'props', 'provider': 'provider'})
class MissingContext():
    def __init__(self, *, key: str, props: typing.Union["AmiContextQuery", "AvailabilityZonesContextQuery", "HostedZoneContextQuery", "SSMParameterContextQuery", "VpcContextQuery", "EndpointServiceAvailabilityZonesContextQuery"], provider: "ContextProvider") -> None:
        """Represents a missing piece of context.

        :param key: The missing context key.
        :param props: A set of provider-specific options.
        :param provider: The provider from which we expect this context key to be obtained.

        stability
        :stability: experimental
        """
        self._values = {
            'key': key,
            'props': props,
            'provider': provider,
        }

    @builtins.property
    def key(self) -> str:
        """The missing context key.

        stability
        :stability: experimental
        """
        return self._values.get('key')

    @builtins.property
    def props(self) -> typing.Union["AmiContextQuery", "AvailabilityZonesContextQuery", "HostedZoneContextQuery", "SSMParameterContextQuery", "VpcContextQuery", "EndpointServiceAvailabilityZonesContextQuery"]:
        """A set of provider-specific options.

        stability
        :stability: experimental
        """
        return self._values.get('props')

    @builtins.property
    def provider(self) -> "ContextProvider":
        """The provider from which we expect this context key to be obtained.

        stability
        :stability: experimental
        """
        return self._values.get('provider')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'MissingContext(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.cloud_assembly_schema.NestedCloudAssemblyProperties", jsii_struct_bases=[], name_mapping={'directory_name': 'directoryName', 'display_name': 'displayName'})
class NestedCloudAssemblyProperties():
    def __init__(self, *, directory_name: str, display_name: typing.Optional[str]=None) -> None:
        """Artifact properties for nested cloud assemblies.

        :param directory_name: Relative path to the nested cloud assembly.
        :param display_name: Display name for the cloud assembly. Default: - The artifact ID

        stability
        :stability: experimental
        """
        self._values = {
            'directory_name': directory_name,
        }
        if display_name is not None: self._values["display_name"] = display_name

    @builtins.property
    def directory_name(self) -> str:
        """Relative path to the nested cloud assembly.

        stability
        :stability: experimental
        """
        return self._values.get('directory_name')

    @builtins.property
    def display_name(self) -> typing.Optional[str]:
        """Display name for the cloud assembly.

        default
        :default: - The artifact ID

        stability
        :stability: experimental
        """
        return self._values.get('display_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NestedCloudAssemblyProperties(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.cloud_assembly_schema.RuntimeInfo", jsii_struct_bases=[], name_mapping={'libraries': 'libraries'})
class RuntimeInfo():
    def __init__(self, *, libraries: typing.Mapping[str, str]) -> None:
        """Information about the application's runtime components.

        :param libraries: The list of libraries loaded in the application, associated with their versions.

        stability
        :stability: experimental
        """
        self._values = {
            'libraries': libraries,
        }

    @builtins.property
    def libraries(self) -> typing.Mapping[str, str]:
        """The list of libraries loaded in the application, associated with their versions.

        stability
        :stability: experimental
        """
        return self._values.get('libraries')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RuntimeInfo(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.cloud_assembly_schema.SSMParameterContextQuery", jsii_struct_bases=[], name_mapping={'account': 'account', 'parameter_name': 'parameterName', 'region': 'region'})
class SSMParameterContextQuery():
    def __init__(self, *, account: str, parameter_name: str, region: str) -> None:
        """Query to SSM Parameter Context Provider.

        :param account: Query account.
        :param parameter_name: Parameter name to query.
        :param region: Query region.

        stability
        :stability: experimental
        """
        self._values = {
            'account': account,
            'parameter_name': parameter_name,
            'region': region,
        }

    @builtins.property
    def account(self) -> str:
        """Query account.

        stability
        :stability: experimental
        """
        return self._values.get('account')

    @builtins.property
    def parameter_name(self) -> str:
        """Parameter name to query.

        stability
        :stability: experimental
        """
        return self._values.get('parameter_name')

    @builtins.property
    def region(self) -> str:
        """Query region.

        stability
        :stability: experimental
        """
        return self._values.get('region')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SSMParameterContextQuery(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.cloud_assembly_schema.Tag", jsii_struct_bases=[], name_mapping={'key': 'key', 'value': 'value'})
class Tag():
    def __init__(self, *, key: str, value: str) -> None:
        """Metadata Entry spec for stack tag.

        :param key: Tag key.
        :param value: Tag value.

        stability
        :stability: experimental
        """
        self._values = {
            'key': key,
            'value': value,
        }

    @builtins.property
    def key(self) -> str:
        """Tag key.

        stability
        :stability: experimental
        """
        return self._values.get('key')

    @builtins.property
    def value(self) -> str:
        """Tag value.

        stability
        :stability: experimental
        """
        return self._values.get('value')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'Tag(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.cloud_assembly_schema.TreeArtifactProperties", jsii_struct_bases=[], name_mapping={'file': 'file'})
class TreeArtifactProperties():
    def __init__(self, *, file: str) -> None:
        """Artifact properties for the Construct Tree Artifact.

        :param file: Filename of the tree artifact.

        stability
        :stability: experimental
        """
        self._values = {
            'file': file,
        }

    @builtins.property
    def file(self) -> str:
        """Filename of the tree artifact.

        stability
        :stability: experimental
        """
        return self._values.get('file')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TreeArtifactProperties(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.cloud_assembly_schema.VpcContextQuery", jsii_struct_bases=[], name_mapping={'account': 'account', 'filter': 'filter', 'region': 'region', 'return_asymmetric_subnets': 'returnAsymmetricSubnets', 'subnet_group_name_tag': 'subnetGroupNameTag'})
class VpcContextQuery():
    def __init__(self, *, account: str, filter: typing.Mapping[str, str], region: str, return_asymmetric_subnets: typing.Optional[bool]=None, subnet_group_name_tag: typing.Optional[str]=None) -> None:
        """Query input for looking up a VPC.

        :param account: Query account.
        :param filter: Filters to apply to the VPC. Filter parameters are the same as passed to DescribeVpcs.
        :param region: Query region.
        :param return_asymmetric_subnets: Whether to populate the subnetGroups field of the {@link VpcContextResponse}, which contains potentially asymmetric subnet groups. Default: false
        :param subnet_group_name_tag: Optional tag for subnet group name. If not provided, we'll look at the aws-cdk:subnet-name tag. If the subnet does not have the specified tag, we'll use its type as the name. Default: 'aws-cdk:subnet-name'

        stability
        :stability: experimental
        """
        self._values = {
            'account': account,
            'filter': filter,
            'region': region,
        }
        if return_asymmetric_subnets is not None: self._values["return_asymmetric_subnets"] = return_asymmetric_subnets
        if subnet_group_name_tag is not None: self._values["subnet_group_name_tag"] = subnet_group_name_tag

    @builtins.property
    def account(self) -> str:
        """Query account.

        stability
        :stability: experimental
        """
        return self._values.get('account')

    @builtins.property
    def filter(self) -> typing.Mapping[str, str]:
        """Filters to apply to the VPC.

        Filter parameters are the same as passed to DescribeVpcs.

        see
        :see: https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeVpcs.html
        stability
        :stability: experimental
        """
        return self._values.get('filter')

    @builtins.property
    def region(self) -> str:
        """Query region.

        stability
        :stability: experimental
        """
        return self._values.get('region')

    @builtins.property
    def return_asymmetric_subnets(self) -> typing.Optional[bool]:
        """Whether to populate the subnetGroups field of the {@link VpcContextResponse}, which contains potentially asymmetric subnet groups.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('return_asymmetric_subnets')

    @builtins.property
    def subnet_group_name_tag(self) -> typing.Optional[str]:
        """Optional tag for subnet group name.

        If not provided, we'll look at the aws-cdk:subnet-name tag.
        If the subnet does not have the specified tag,
        we'll use its type as the name.

        default
        :default: 'aws-cdk:subnet-name'

        stability
        :stability: experimental
        """
        return self._values.get('subnet_group_name_tag')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'VpcContextQuery(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "AmiContextQuery",
    "ArtifactManifest",
    "ArtifactMetadataEntryType",
    "ArtifactType",
    "AssemblyManifest",
    "AssetManifest",
    "AssetManifestProperties",
    "AvailabilityZonesContextQuery",
    "AwsCloudFormationStackProperties",
    "AwsDestination",
    "ContainerImageAssetMetadataEntry",
    "ContextProvider",
    "DockerImageAsset",
    "DockerImageDestination",
    "DockerImageSource",
    "EndpointServiceAvailabilityZonesContextQuery",
    "FileAsset",
    "FileAssetMetadataEntry",
    "FileAssetPackaging",
    "FileDestination",
    "FileSource",
    "HostedZoneContextQuery",
    "Manifest",
    "MetadataEntry",
    "MissingContext",
    "NestedCloudAssemblyProperties",
    "RuntimeInfo",
    "SSMParameterContextQuery",
    "Tag",
    "TreeArtifactProperties",
    "VpcContextQuery",
]

publication.publish()
