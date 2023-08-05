import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (Duration as _Duration_5170c158, Construct as _Construct_f50a3f53, Resource as _Resource_884d0774, CfnResource as _CfnResource_7760e8e4, FromCloudFormationOptions as _FromCloudFormationOptions_5f49f6f1, TreeInspector as _TreeInspector_154f5999, TagManager as _TagManager_2508893f, IResolvable as _IResolvable_9ceae33e, IInspectable as _IInspectable_051e6ed8, CfnTag as _CfnTag_b4661f1a, IResource as _IResource_72f7ee7e, SecretValue as _SecretValue_99478b8b)
from ..assets import (FollowMode as _FollowMode_f74e7125)
from ..aws_applicationautoscaling import (EnableScalingProps as _EnableScalingProps_5e50c056, BaseTargetTrackingProps as _BaseTargetTrackingProps_3d6586ed, BaseScalableAttribute as _BaseScalableAttribute_ba74233b, BasicStepScalingPolicyProps as _BasicStepScalingPolicyProps_548d6784, ScalingSchedule as _ScalingSchedule_c85ff455, BaseScalableAttributeProps as _BaseScalableAttributeProps_c3394117, ServiceNamespace as _ServiceNamespace_23356894)
from ..aws_autoscaling import (CommonAutoScalingGroupProps as _CommonAutoScalingGroupProps_43a23fca, BlockDevice as _BlockDevice_6b64cf0c, HealthCheck as _HealthCheck_ed599e14, Monitoring as _Monitoring_11cb7f01, NotificationConfiguration as _NotificationConfiguration_396b88c6, RollingUpdateConfiguration as _RollingUpdateConfiguration_c96dd49e, UpdateType as _UpdateType_7a2ac17e, AutoScalingGroup as _AutoScalingGroup_003d0b84, IAutoScalingGroup as _IAutoScalingGroup_a753dc94)
from ..aws_cloudwatch import (Metric as _Metric_53e89548, MetricOptions as _MetricOptions_ad2c4d5d, IMetric as _IMetric_bfdc01fe)
from ..aws_ec2 import (SubnetSelection as _SubnetSelection_36a13cd6, InstanceType as _InstanceType_85a97b30, IMachineImage as _IMachineImage_d5cd7b45, IVpc as _IVpc_3795853f, ISecurityGroup as _ISecurityGroup_d72ab8e8, Connections as _Connections_231f38b5, MachineImageConfig as _MachineImageConfig_815fc1b9, AmazonLinuxGeneration as _AmazonLinuxGeneration_f5d20aaa)
from ..aws_ecr import (IRepository as _IRepository_aa6e452c)
from ..aws_ecr_assets import (DockerImageAssetOptions as _DockerImageAssetOptions_b5a48cdf, DockerImageAsset as _DockerImageAsset_e5a78fae)
from ..aws_elasticloadbalancing import (LoadBalancer as _LoadBalancer_6d00b4b8, ILoadBalancerTarget as _ILoadBalancerTarget_87ce58b8)
from ..aws_elasticloadbalancingv2 import (LoadBalancerTargetProps as _LoadBalancerTargetProps_80dbd4a5, IApplicationTargetGroup as _IApplicationTargetGroup_1bf77cc5, INetworkTargetGroup as _INetworkTargetGroup_1183b98f, IApplicationLoadBalancerTarget as _IApplicationLoadBalancerTarget_079c540c, INetworkLoadBalancerTarget as _INetworkLoadBalancerTarget_c44e1c1e, ApplicationListener as _ApplicationListener_58c10c5c, AddApplicationTargetsProps as _AddApplicationTargetsProps_a8f3da0a, NetworkListener as _NetworkListener_921cec4b, AddNetworkTargetsProps as _AddNetworkTargetsProps_c9bbd436, ApplicationTargetGroup as _ApplicationTargetGroup_7d0a8d54)
from ..aws_iam import (IRole as _IRole_e69bbae4, PolicyStatement as _PolicyStatement_f75dc775, Grant as _Grant_96af6d2d, IGrantable as _IGrantable_0fcfc53a)
from ..aws_logs import (ILogGroup as _ILogGroup_6b54c8e1, RetentionDays as _RetentionDays_bdc7ad1f)
from ..aws_secretsmanager import (ISecret as _ISecret_75279d36)
from ..aws_servicediscovery import (Service as _Service_4702d1e5, IService as _IService_f28ba3c9, NamespaceType as _NamespaceType_df1ca402, INamespace as _INamespace_2b56a022, DnsRecordType as _DnsRecordType_acb5afbb)
from ..aws_sns import (ITopic as _ITopic_ef0ebe0e)
from ..aws_ssm import (IParameter as _IParameter_f25c9bbf)


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.AddAutoScalingGroupCapacityOptions", jsii_struct_bases=[], name_mapping={'can_containers_access_instance_role': 'canContainersAccessInstanceRole', 'spot_instance_draining': 'spotInstanceDraining', 'task_drain_time': 'taskDrainTime'})
class AddAutoScalingGroupCapacityOptions():
    def __init__(self, *, can_containers_access_instance_role: typing.Optional[bool]=None, spot_instance_draining: typing.Optional[bool]=None, task_drain_time: typing.Optional[_Duration_5170c158]=None) -> None:
        """The properties for adding an AutoScalingGroup.

        :param can_containers_access_instance_role: Specifies whether the containers can access the container instance role. Default: false
        :param spot_instance_draining: Specify whether to enable Automated Draining for Spot Instances running Amazon ECS Services. For more information, see `Using Spot Instances <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/container-instance-spot.html>`_. Default: false
        :param task_drain_time: The time period to wait before force terminating an instance that is draining. This creates a Lambda function that is used by a lifecycle hook for the AutoScalingGroup that will delay instance termination until all ECS tasks have drained from the instance. Set to 0 to disable task draining. Set to 0 to disable task draining. Default: Duration.minutes(5)

        stability
        :stability: experimental
        """
        self._values = {
        }
        if can_containers_access_instance_role is not None: self._values["can_containers_access_instance_role"] = can_containers_access_instance_role
        if spot_instance_draining is not None: self._values["spot_instance_draining"] = spot_instance_draining
        if task_drain_time is not None: self._values["task_drain_time"] = task_drain_time

    @builtins.property
    def can_containers_access_instance_role(self) -> typing.Optional[bool]:
        """Specifies whether the containers can access the container instance role.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('can_containers_access_instance_role')

    @builtins.property
    def spot_instance_draining(self) -> typing.Optional[bool]:
        """Specify whether to enable Automated Draining for Spot Instances running Amazon ECS Services.

        For more information, see `Using Spot Instances <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/container-instance-spot.html>`_.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('spot_instance_draining')

    @builtins.property
    def task_drain_time(self) -> typing.Optional[_Duration_5170c158]:
        """The time period to wait before force terminating an instance that is draining.

        This creates a Lambda function that is used by a lifecycle hook for the
        AutoScalingGroup that will delay instance termination until all ECS tasks
        have drained from the instance. Set to 0 to disable task draining.

        Set to 0 to disable task draining.

        default
        :default: Duration.minutes(5)

        stability
        :stability: experimental
        """
        return self._values.get('task_drain_time')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AddAutoScalingGroupCapacityOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.AddCapacityOptions", jsii_struct_bases=[AddAutoScalingGroupCapacityOptions, _CommonAutoScalingGroupProps_43a23fca], name_mapping={'can_containers_access_instance_role': 'canContainersAccessInstanceRole', 'spot_instance_draining': 'spotInstanceDraining', 'task_drain_time': 'taskDrainTime', 'allow_all_outbound': 'allowAllOutbound', 'associate_public_ip_address': 'associatePublicIpAddress', 'block_devices': 'blockDevices', 'cooldown': 'cooldown', 'desired_capacity': 'desiredCapacity', 'health_check': 'healthCheck', 'ignore_unmodified_size_properties': 'ignoreUnmodifiedSizeProperties', 'instance_monitoring': 'instanceMonitoring', 'key_name': 'keyName', 'max_capacity': 'maxCapacity', 'max_instance_lifetime': 'maxInstanceLifetime', 'min_capacity': 'minCapacity', 'notifications': 'notifications', 'notifications_topic': 'notificationsTopic', 'replacing_update_min_successful_instances_percent': 'replacingUpdateMinSuccessfulInstancesPercent', 'resource_signal_count': 'resourceSignalCount', 'resource_signal_timeout': 'resourceSignalTimeout', 'rolling_update_configuration': 'rollingUpdateConfiguration', 'spot_price': 'spotPrice', 'update_type': 'updateType', 'vpc_subnets': 'vpcSubnets', 'instance_type': 'instanceType', 'machine_image': 'machineImage'})
class AddCapacityOptions(AddAutoScalingGroupCapacityOptions, _CommonAutoScalingGroupProps_43a23fca):
    def __init__(self, *, can_containers_access_instance_role: typing.Optional[bool]=None, spot_instance_draining: typing.Optional[bool]=None, task_drain_time: typing.Optional[_Duration_5170c158]=None, allow_all_outbound: typing.Optional[bool]=None, associate_public_ip_address: typing.Optional[bool]=None, block_devices: typing.Optional[typing.List[_BlockDevice_6b64cf0c]]=None, cooldown: typing.Optional[_Duration_5170c158]=None, desired_capacity: typing.Optional[jsii.Number]=None, health_check: typing.Optional[_HealthCheck_ed599e14]=None, ignore_unmodified_size_properties: typing.Optional[bool]=None, instance_monitoring: typing.Optional[_Monitoring_11cb7f01]=None, key_name: typing.Optional[str]=None, max_capacity: typing.Optional[jsii.Number]=None, max_instance_lifetime: typing.Optional[_Duration_5170c158]=None, min_capacity: typing.Optional[jsii.Number]=None, notifications: typing.Optional[typing.List[_NotificationConfiguration_396b88c6]]=None, notifications_topic: typing.Optional[_ITopic_ef0ebe0e]=None, replacing_update_min_successful_instances_percent: typing.Optional[jsii.Number]=None, resource_signal_count: typing.Optional[jsii.Number]=None, resource_signal_timeout: typing.Optional[_Duration_5170c158]=None, rolling_update_configuration: typing.Optional[_RollingUpdateConfiguration_c96dd49e]=None, spot_price: typing.Optional[str]=None, update_type: typing.Optional[_UpdateType_7a2ac17e]=None, vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6]=None, instance_type: _InstanceType_85a97b30, machine_image: typing.Optional[_IMachineImage_d5cd7b45]=None) -> None:
        """The properties for adding instance capacity to an AutoScalingGroup.

        :param can_containers_access_instance_role: Specifies whether the containers can access the container instance role. Default: false
        :param spot_instance_draining: Specify whether to enable Automated Draining for Spot Instances running Amazon ECS Services. For more information, see `Using Spot Instances <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/container-instance-spot.html>`_. Default: false
        :param task_drain_time: The time period to wait before force terminating an instance that is draining. This creates a Lambda function that is used by a lifecycle hook for the AutoScalingGroup that will delay instance termination until all ECS tasks have drained from the instance. Set to 0 to disable task draining. Set to 0 to disable task draining. Default: Duration.minutes(5)
        :param allow_all_outbound: Whether the instances can initiate connections to anywhere by default. Default: true
        :param associate_public_ip_address: Whether instances in the Auto Scaling Group should have public IP addresses associated with them. Default: - Use subnet setting.
        :param block_devices: Specifies how block devices are exposed to the instance. You can specify virtual devices and EBS volumes. Each instance that is launched has an associated root device volume, either an Amazon EBS volume or an instance store volume. You can use block device mappings to specify additional EBS volumes or instance store volumes to attach to an instance when it is launched. Default: - Uses the block device mapping of the AMI
        :param cooldown: Default scaling cooldown for this AutoScalingGroup. Default: Duration.minutes(5)
        :param desired_capacity: Initial amount of instances in the fleet. If this is set to a number, every deployment will reset the amount of instances to this number. It is recommended to leave this value blank. Default: minCapacity, and leave unchanged during deployment
        :param health_check: Configuration for health checks. Default: - HealthCheck.ec2 with no grace period
        :param ignore_unmodified_size_properties: If the ASG has scheduled actions, don't reset unchanged group sizes. Only used if the ASG has scheduled actions (which may scale your ASG up or down regardless of cdk deployments). If true, the size of the group will only be reset if it has been changed in the CDK app. If false, the sizes will always be changed back to what they were in the CDK app on deployment. Default: true
        :param instance_monitoring: Controls whether instances in this group are launched with detailed or basic monitoring. When detailed monitoring is enabled, Amazon CloudWatch generates metrics every minute and your account is charged a fee. When you disable detailed monitoring, CloudWatch generates metrics every 5 minutes. Default: - Monitoring.DETAILED
        :param key_name: Name of SSH keypair to grant access to instances. Default: - No SSH access will be possible.
        :param max_capacity: Maximum number of instances in the fleet. Default: desiredCapacity
        :param max_instance_lifetime: The maximum amount of time that an instance can be in service. The maximum duration applies to all current and future instances in the group. As an instance approaches its maximum duration, it is terminated and replaced, and cannot be used again. You must specify a value of at least 604,800 seconds (7 days). To clear a previously set value, simply leave this property undefinied. Default: none
        :param min_capacity: Minimum number of instances in the fleet. Default: 1
        :param notifications: Configure autoscaling group to send notifications about fleet changes to an SNS topic(s). Default: - No fleet change notifications will be sent.
        :param notifications_topic: SNS topic to send notifications about fleet changes. Default: - No fleet change notifications will be sent.
        :param replacing_update_min_successful_instances_percent: Configuration for replacing updates. Only used if updateType == UpdateType.ReplacingUpdate. Specifies how many instances must signal success for the update to succeed. Default: minSuccessfulInstancesPercent
        :param resource_signal_count: How many ResourceSignal calls CloudFormation expects before the resource is considered created. Default: 1
        :param resource_signal_timeout: The length of time to wait for the resourceSignalCount. The maximum value is 43200 (12 hours). Default: Duration.minutes(5)
        :param rolling_update_configuration: Configuration for rolling updates. Only used if updateType == UpdateType.RollingUpdate. Default: - RollingUpdateConfiguration with defaults.
        :param spot_price: The maximum hourly price (in USD) to be paid for any Spot Instance launched to fulfill the request. Spot Instances are launched when the price you specify exceeds the current Spot market price. Default: none
        :param update_type: What to do when an AutoScalingGroup's instance configuration is changed. This is applied when any of the settings on the ASG are changed that affect how the instances should be created (VPC, instance type, startup scripts, etc.). It indicates how the existing instances should be replaced with new instances matching the new config. By default, nothing is done and only new instances are launched with the new config. Default: UpdateType.None
        :param vpc_subnets: Where to place instances within the VPC. Default: - All Private subnets.
        :param instance_type: The EC2 instance type to use when launching instances into the AutoScalingGroup.
        :param machine_image: The ECS-optimized AMI variant to use. For more information, see `Amazon ECS-optimized AMIs <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html>`_. Default: - Amazon Linux 2

        stability
        :stability: experimental
        """
        if isinstance(rolling_update_configuration, dict): rolling_update_configuration = _RollingUpdateConfiguration_c96dd49e(**rolling_update_configuration)
        if isinstance(vpc_subnets, dict): vpc_subnets = _SubnetSelection_36a13cd6(**vpc_subnets)
        self._values = {
            'instance_type': instance_type,
        }
        if can_containers_access_instance_role is not None: self._values["can_containers_access_instance_role"] = can_containers_access_instance_role
        if spot_instance_draining is not None: self._values["spot_instance_draining"] = spot_instance_draining
        if task_drain_time is not None: self._values["task_drain_time"] = task_drain_time
        if allow_all_outbound is not None: self._values["allow_all_outbound"] = allow_all_outbound
        if associate_public_ip_address is not None: self._values["associate_public_ip_address"] = associate_public_ip_address
        if block_devices is not None: self._values["block_devices"] = block_devices
        if cooldown is not None: self._values["cooldown"] = cooldown
        if desired_capacity is not None: self._values["desired_capacity"] = desired_capacity
        if health_check is not None: self._values["health_check"] = health_check
        if ignore_unmodified_size_properties is not None: self._values["ignore_unmodified_size_properties"] = ignore_unmodified_size_properties
        if instance_monitoring is not None: self._values["instance_monitoring"] = instance_monitoring
        if key_name is not None: self._values["key_name"] = key_name
        if max_capacity is not None: self._values["max_capacity"] = max_capacity
        if max_instance_lifetime is not None: self._values["max_instance_lifetime"] = max_instance_lifetime
        if min_capacity is not None: self._values["min_capacity"] = min_capacity
        if notifications is not None: self._values["notifications"] = notifications
        if notifications_topic is not None: self._values["notifications_topic"] = notifications_topic
        if replacing_update_min_successful_instances_percent is not None: self._values["replacing_update_min_successful_instances_percent"] = replacing_update_min_successful_instances_percent
        if resource_signal_count is not None: self._values["resource_signal_count"] = resource_signal_count
        if resource_signal_timeout is not None: self._values["resource_signal_timeout"] = resource_signal_timeout
        if rolling_update_configuration is not None: self._values["rolling_update_configuration"] = rolling_update_configuration
        if spot_price is not None: self._values["spot_price"] = spot_price
        if update_type is not None: self._values["update_type"] = update_type
        if vpc_subnets is not None: self._values["vpc_subnets"] = vpc_subnets
        if machine_image is not None: self._values["machine_image"] = machine_image

    @builtins.property
    def can_containers_access_instance_role(self) -> typing.Optional[bool]:
        """Specifies whether the containers can access the container instance role.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('can_containers_access_instance_role')

    @builtins.property
    def spot_instance_draining(self) -> typing.Optional[bool]:
        """Specify whether to enable Automated Draining for Spot Instances running Amazon ECS Services.

        For more information, see `Using Spot Instances <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/container-instance-spot.html>`_.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('spot_instance_draining')

    @builtins.property
    def task_drain_time(self) -> typing.Optional[_Duration_5170c158]:
        """The time period to wait before force terminating an instance that is draining.

        This creates a Lambda function that is used by a lifecycle hook for the
        AutoScalingGroup that will delay instance termination until all ECS tasks
        have drained from the instance. Set to 0 to disable task draining.

        Set to 0 to disable task draining.

        default
        :default: Duration.minutes(5)

        stability
        :stability: experimental
        """
        return self._values.get('task_drain_time')

    @builtins.property
    def allow_all_outbound(self) -> typing.Optional[bool]:
        """Whether the instances can initiate connections to anywhere by default.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('allow_all_outbound')

    @builtins.property
    def associate_public_ip_address(self) -> typing.Optional[bool]:
        """Whether instances in the Auto Scaling Group should have public IP addresses associated with them.

        default
        :default: - Use subnet setting.

        stability
        :stability: experimental
        """
        return self._values.get('associate_public_ip_address')

    @builtins.property
    def block_devices(self) -> typing.Optional[typing.List[_BlockDevice_6b64cf0c]]:
        """Specifies how block devices are exposed to the instance. You can specify virtual devices and EBS volumes.

        Each instance that is launched has an associated root device volume,
        either an Amazon EBS volume or an instance store volume.
        You can use block device mappings to specify additional EBS volumes or
        instance store volumes to attach to an instance when it is launched.

        default
        :default: - Uses the block device mapping of the AMI

        see
        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/block-device-mapping-concepts.html
        stability
        :stability: experimental
        """
        return self._values.get('block_devices')

    @builtins.property
    def cooldown(self) -> typing.Optional[_Duration_5170c158]:
        """Default scaling cooldown for this AutoScalingGroup.

        default
        :default: Duration.minutes(5)

        stability
        :stability: experimental
        """
        return self._values.get('cooldown')

    @builtins.property
    def desired_capacity(self) -> typing.Optional[jsii.Number]:
        """Initial amount of instances in the fleet.

        If this is set to a number, every deployment will reset the amount of
        instances to this number. It is recommended to leave this value blank.

        default
        :default: minCapacity, and leave unchanged during deployment

        see
        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-desiredcapacity
        stability
        :stability: experimental
        """
        return self._values.get('desired_capacity')

    @builtins.property
    def health_check(self) -> typing.Optional[_HealthCheck_ed599e14]:
        """Configuration for health checks.

        default
        :default: - HealthCheck.ec2 with no grace period

        stability
        :stability: experimental
        """
        return self._values.get('health_check')

    @builtins.property
    def ignore_unmodified_size_properties(self) -> typing.Optional[bool]:
        """If the ASG has scheduled actions, don't reset unchanged group sizes.

        Only used if the ASG has scheduled actions (which may scale your ASG up
        or down regardless of cdk deployments). If true, the size of the group
        will only be reset if it has been changed in the CDK app. If false, the
        sizes will always be changed back to what they were in the CDK app
        on deployment.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('ignore_unmodified_size_properties')

    @builtins.property
    def instance_monitoring(self) -> typing.Optional[_Monitoring_11cb7f01]:
        """Controls whether instances in this group are launched with detailed or basic monitoring.

        When detailed monitoring is enabled, Amazon CloudWatch generates metrics every minute and your account
        is charged a fee. When you disable detailed monitoring, CloudWatch generates metrics every 5 minutes.

        default
        :default: - Monitoring.DETAILED

        see
        :see: https://docs.aws.amazon.com/autoscaling/latest/userguide/as-instance-monitoring.html#enable-as-instance-metrics
        stability
        :stability: experimental
        """
        return self._values.get('instance_monitoring')

    @builtins.property
    def key_name(self) -> typing.Optional[str]:
        """Name of SSH keypair to grant access to instances.

        default
        :default: - No SSH access will be possible.

        stability
        :stability: experimental
        """
        return self._values.get('key_name')

    @builtins.property
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        """Maximum number of instances in the fleet.

        default
        :default: desiredCapacity

        stability
        :stability: experimental
        """
        return self._values.get('max_capacity')

    @builtins.property
    def max_instance_lifetime(self) -> typing.Optional[_Duration_5170c158]:
        """The maximum amount of time that an instance can be in service.

        The maximum duration applies
        to all current and future instances in the group. As an instance approaches its maximum duration,
        it is terminated and replaced, and cannot be used again.

        You must specify a value of at least 604,800 seconds (7 days). To clear a previously set value,
        simply leave this property undefinied.

        default
        :default: none

        see
        :see: https://docs.aws.amazon.com/autoscaling/ec2/userguide/asg-max-instance-lifetime.html
        stability
        :stability: experimental
        """
        return self._values.get('max_instance_lifetime')

    @builtins.property
    def min_capacity(self) -> typing.Optional[jsii.Number]:
        """Minimum number of instances in the fleet.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('min_capacity')

    @builtins.property
    def notifications(self) -> typing.Optional[typing.List[_NotificationConfiguration_396b88c6]]:
        """Configure autoscaling group to send notifications about fleet changes to an SNS topic(s).

        default
        :default: - No fleet change notifications will be sent.

        see
        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-notificationconfigurations
        stability
        :stability: experimental
        """
        return self._values.get('notifications')

    @builtins.property
    def notifications_topic(self) -> typing.Optional[_ITopic_ef0ebe0e]:
        """SNS topic to send notifications about fleet changes.

        default
        :default: - No fleet change notifications will be sent.

        deprecated
        :deprecated: use ``notifications``

        stability
        :stability: deprecated
        """
        return self._values.get('notifications_topic')

    @builtins.property
    def replacing_update_min_successful_instances_percent(self) -> typing.Optional[jsii.Number]:
        """Configuration for replacing updates.

        Only used if updateType == UpdateType.ReplacingUpdate. Specifies how
        many instances must signal success for the update to succeed.

        default
        :default: minSuccessfulInstancesPercent

        stability
        :stability: experimental
        """
        return self._values.get('replacing_update_min_successful_instances_percent')

    @builtins.property
    def resource_signal_count(self) -> typing.Optional[jsii.Number]:
        """How many ResourceSignal calls CloudFormation expects before the resource is considered created.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('resource_signal_count')

    @builtins.property
    def resource_signal_timeout(self) -> typing.Optional[_Duration_5170c158]:
        """The length of time to wait for the resourceSignalCount.

        The maximum value is 43200 (12 hours).

        default
        :default: Duration.minutes(5)

        stability
        :stability: experimental
        """
        return self._values.get('resource_signal_timeout')

    @builtins.property
    def rolling_update_configuration(self) -> typing.Optional[_RollingUpdateConfiguration_c96dd49e]:
        """Configuration for rolling updates.

        Only used if updateType == UpdateType.RollingUpdate.

        default
        :default: - RollingUpdateConfiguration with defaults.

        stability
        :stability: experimental
        """
        return self._values.get('rolling_update_configuration')

    @builtins.property
    def spot_price(self) -> typing.Optional[str]:
        """The maximum hourly price (in USD) to be paid for any Spot Instance launched to fulfill the request.

        Spot Instances are
        launched when the price you specify exceeds the current Spot market price.

        default
        :default: none

        stability
        :stability: experimental
        """
        return self._values.get('spot_price')

    @builtins.property
    def update_type(self) -> typing.Optional[_UpdateType_7a2ac17e]:
        """What to do when an AutoScalingGroup's instance configuration is changed.

        This is applied when any of the settings on the ASG are changed that
        affect how the instances should be created (VPC, instance type, startup
        scripts, etc.). It indicates how the existing instances should be
        replaced with new instances matching the new config. By default, nothing
        is done and only new instances are launched with the new config.

        default
        :default: UpdateType.None

        stability
        :stability: experimental
        """
        return self._values.get('update_type')

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_36a13cd6]:
        """Where to place instances within the VPC.

        default
        :default: - All Private subnets.

        stability
        :stability: experimental
        """
        return self._values.get('vpc_subnets')

    @builtins.property
    def instance_type(self) -> _InstanceType_85a97b30:
        """The EC2 instance type to use when launching instances into the AutoScalingGroup.

        stability
        :stability: experimental
        """
        return self._values.get('instance_type')

    @builtins.property
    def machine_image(self) -> typing.Optional[_IMachineImage_d5cd7b45]:
        """The ECS-optimized AMI variant to use.

        For more information, see
        `Amazon ECS-optimized AMIs <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html>`_.

        default
        :default: - Amazon Linux 2

        stability
        :stability: experimental
        """
        return self._values.get('machine_image')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AddCapacityOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.aws_ecs.AmiHardwareType")
class AmiHardwareType(enum.Enum):
    """The ECS-optimized AMI variant to use.

    For more information, see
    `Amazon ECS-optimized AMIs <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html>`_.

    stability
    :stability: experimental
    """
    STANDARD = "STANDARD"
    """Use the standard Amazon ECS-optimized AMI.

    stability
    :stability: experimental
    """
    GPU = "GPU"
    """Use the Amazon ECS GPU-optimized AMI.

    stability
    :stability: experimental
    """
    ARM = "ARM"
    """Use the Amazon ECS-optimized Amazon Linux 2 (arm64) AMI.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.AppMeshProxyConfigurationConfigProps", jsii_struct_bases=[], name_mapping={'container_name': 'containerName', 'properties': 'properties'})
class AppMeshProxyConfigurationConfigProps():
    def __init__(self, *, container_name: str, properties: "AppMeshProxyConfigurationProps") -> None:
        """The configuration to use when setting an App Mesh proxy configuration.

        :param container_name: The name of the container that will serve as the App Mesh proxy.
        :param properties: The set of network configuration parameters to provide the Container Network Interface (CNI) plugin.

        stability
        :stability: experimental
        """
        if isinstance(properties, dict): properties = AppMeshProxyConfigurationProps(**properties)
        self._values = {
            'container_name': container_name,
            'properties': properties,
        }

    @builtins.property
    def container_name(self) -> str:
        """The name of the container that will serve as the App Mesh proxy.

        stability
        :stability: experimental
        """
        return self._values.get('container_name')

    @builtins.property
    def properties(self) -> "AppMeshProxyConfigurationProps":
        """The set of network configuration parameters to provide the Container Network Interface (CNI) plugin.

        stability
        :stability: experimental
        """
        return self._values.get('properties')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AppMeshProxyConfigurationConfigProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.AppMeshProxyConfigurationProps", jsii_struct_bases=[], name_mapping={'app_ports': 'appPorts', 'proxy_egress_port': 'proxyEgressPort', 'proxy_ingress_port': 'proxyIngressPort', 'egress_ignored_i_ps': 'egressIgnoredIPs', 'egress_ignored_ports': 'egressIgnoredPorts', 'ignored_gid': 'ignoredGID', 'ignored_uid': 'ignoredUID'})
class AppMeshProxyConfigurationProps():
    def __init__(self, *, app_ports: typing.List[jsii.Number], proxy_egress_port: jsii.Number, proxy_ingress_port: jsii.Number, egress_ignored_i_ps: typing.Optional[typing.List[str]]=None, egress_ignored_ports: typing.Optional[typing.List[jsii.Number]]=None, ignored_gid: typing.Optional[jsii.Number]=None, ignored_uid: typing.Optional[jsii.Number]=None) -> None:
        """Interface for setting the properties of proxy configuration.

        :param app_ports: The list of ports that the application uses. Network traffic to these ports is forwarded to the ProxyIngressPort and ProxyEgressPort.
        :param proxy_egress_port: Specifies the port that outgoing traffic from the AppPorts is directed to.
        :param proxy_ingress_port: Specifies the port that incoming traffic to the AppPorts is directed to.
        :param egress_ignored_i_ps: The egress traffic going to these specified IP addresses is ignored and not redirected to the ProxyEgressPort. It can be an empty list.
        :param egress_ignored_ports: The egress traffic going to these specified ports is ignored and not redirected to the ProxyEgressPort. It can be an empty list.
        :param ignored_gid: The group ID (GID) of the proxy container as defined by the user parameter in a container definition. This is used to ensure the proxy ignores its own traffic. If IgnoredUID is specified, this field can be empty.
        :param ignored_uid: The user ID (UID) of the proxy container as defined by the user parameter in a container definition. This is used to ensure the proxy ignores its own traffic. If IgnoredGID is specified, this field can be empty.

        stability
        :stability: experimental
        """
        self._values = {
            'app_ports': app_ports,
            'proxy_egress_port': proxy_egress_port,
            'proxy_ingress_port': proxy_ingress_port,
        }
        if egress_ignored_i_ps is not None: self._values["egress_ignored_i_ps"] = egress_ignored_i_ps
        if egress_ignored_ports is not None: self._values["egress_ignored_ports"] = egress_ignored_ports
        if ignored_gid is not None: self._values["ignored_gid"] = ignored_gid
        if ignored_uid is not None: self._values["ignored_uid"] = ignored_uid

    @builtins.property
    def app_ports(self) -> typing.List[jsii.Number]:
        """The list of ports that the application uses.

        Network traffic to these ports is forwarded to the ProxyIngressPort and ProxyEgressPort.

        stability
        :stability: experimental
        """
        return self._values.get('app_ports')

    @builtins.property
    def proxy_egress_port(self) -> jsii.Number:
        """Specifies the port that outgoing traffic from the AppPorts is directed to.

        stability
        :stability: experimental
        """
        return self._values.get('proxy_egress_port')

    @builtins.property
    def proxy_ingress_port(self) -> jsii.Number:
        """Specifies the port that incoming traffic to the AppPorts is directed to.

        stability
        :stability: experimental
        """
        return self._values.get('proxy_ingress_port')

    @builtins.property
    def egress_ignored_i_ps(self) -> typing.Optional[typing.List[str]]:
        """The egress traffic going to these specified IP addresses is ignored and not redirected to the ProxyEgressPort.

        It can be an empty list.

        stability
        :stability: experimental
        """
        return self._values.get('egress_ignored_i_ps')

    @builtins.property
    def egress_ignored_ports(self) -> typing.Optional[typing.List[jsii.Number]]:
        """The egress traffic going to these specified ports is ignored and not redirected to the ProxyEgressPort.

        It can be an empty list.

        stability
        :stability: experimental
        """
        return self._values.get('egress_ignored_ports')

    @builtins.property
    def ignored_gid(self) -> typing.Optional[jsii.Number]:
        """The group ID (GID) of the proxy container as defined by the user parameter in a container definition.

        This is used to ensure the proxy ignores its own traffic. If IgnoredUID is specified, this field can be empty.

        stability
        :stability: experimental
        """
        return self._values.get('ignored_gid')

    @builtins.property
    def ignored_uid(self) -> typing.Optional[jsii.Number]:
        """The user ID (UID) of the proxy container as defined by the user parameter in a container definition.

        This is used to ensure the proxy ignores its own traffic. If IgnoredGID is specified, this field can be empty.

        stability
        :stability: experimental
        """
        return self._values.get('ignored_uid')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AppMeshProxyConfigurationProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.AssetImageProps", jsii_struct_bases=[_DockerImageAssetOptions_b5a48cdf], name_mapping={'exclude': 'exclude', 'follow': 'follow', 'extra_hash': 'extraHash', 'build_args': 'buildArgs', 'file': 'file', 'repository_name': 'repositoryName', 'target': 'target'})
class AssetImageProps(_DockerImageAssetOptions_b5a48cdf):
    def __init__(self, *, exclude: typing.Optional[typing.List[str]]=None, follow: typing.Optional[_FollowMode_f74e7125]=None, extra_hash: typing.Optional[str]=None, build_args: typing.Optional[typing.Mapping[str, str]]=None, file: typing.Optional[str]=None, repository_name: typing.Optional[str]=None, target: typing.Optional[str]=None) -> None:
        """The properties for building an AssetImage.

        :param exclude: Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: Never
        :param extra_hash: Extra information to encode into the fingerprint (e.g. build instructions and other inputs). Default: - hash is only based on source content
        :param build_args: Build args to pass to the ``docker build`` command. Since Docker build arguments are resolved before deployment, keys and values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or ``queue.queueUrl``). Default: - no build args are passed
        :param file: Path to the Dockerfile (relative to the directory). Default: 'Dockerfile'
        :param repository_name: ECR repository name. Specify this property if you need to statically address the image, e.g. from a Kubernetes Pod. Note, this is only the repository name, without the registry and the tag parts. Default: - the default ECR repository for CDK assets
        :param target: Docker target to build to. Default: - no target

        stability
        :stability: experimental
        """
        self._values = {
        }
        if exclude is not None: self._values["exclude"] = exclude
        if follow is not None: self._values["follow"] = follow
        if extra_hash is not None: self._values["extra_hash"] = extra_hash
        if build_args is not None: self._values["build_args"] = build_args
        if file is not None: self._values["file"] = file
        if repository_name is not None: self._values["repository_name"] = repository_name
        if target is not None: self._values["target"] = target

    @builtins.property
    def exclude(self) -> typing.Optional[typing.List[str]]:
        """Glob patterns to exclude from the copy.

        default
        :default: nothing is excluded

        stability
        :stability: deprecated
        """
        return self._values.get('exclude')

    @builtins.property
    def follow(self) -> typing.Optional[_FollowMode_f74e7125]:
        """A strategy for how to handle symlinks.

        default
        :default: Never

        stability
        :stability: deprecated
        """
        return self._values.get('follow')

    @builtins.property
    def extra_hash(self) -> typing.Optional[str]:
        """Extra information to encode into the fingerprint (e.g. build instructions and other inputs).

        default
        :default: - hash is only based on source content

        stability
        :stability: deprecated
        """
        return self._values.get('extra_hash')

    @builtins.property
    def build_args(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Build args to pass to the ``docker build`` command.

        Since Docker build arguments are resolved before deployment, keys and
        values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or
        ``queue.queueUrl``).

        default
        :default: - no build args are passed

        stability
        :stability: experimental
        """
        return self._values.get('build_args')

    @builtins.property
    def file(self) -> typing.Optional[str]:
        """Path to the Dockerfile (relative to the directory).

        default
        :default: 'Dockerfile'

        stability
        :stability: experimental
        """
        return self._values.get('file')

    @builtins.property
    def repository_name(self) -> typing.Optional[str]:
        """ECR repository name.

        Specify this property if you need to statically address the image, e.g.
        from a Kubernetes Pod. Note, this is only the repository name, without the
        registry and the tag parts.

        default
        :default: - the default ECR repository for CDK assets

        deprecated
        :deprecated:

        to control the location of docker image assets, please override
        ``Stack.addDockerImageAsset``. this feature will be removed in future
        releases.

        stability
        :stability: deprecated
        """
        return self._values.get('repository_name')

    @builtins.property
    def target(self) -> typing.Optional[str]:
        """Docker target to build to.

        default
        :default: - no target

        stability
        :stability: experimental
        """
        return self._values.get('target')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AssetImageProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.AwsLogDriverProps", jsii_struct_bases=[], name_mapping={'stream_prefix': 'streamPrefix', 'datetime_format': 'datetimeFormat', 'log_group': 'logGroup', 'log_retention': 'logRetention', 'multiline_pattern': 'multilinePattern'})
class AwsLogDriverProps():
    def __init__(self, *, stream_prefix: str, datetime_format: typing.Optional[str]=None, log_group: typing.Optional[_ILogGroup_6b54c8e1]=None, log_retention: typing.Optional[_RetentionDays_bdc7ad1f]=None, multiline_pattern: typing.Optional[str]=None) -> None:
        """Specifies the awslogs log driver configuration options.

        :param stream_prefix: Prefix for the log streams. The awslogs-stream-prefix option allows you to associate a log stream with the specified prefix, the container name, and the ID of the Amazon ECS task to which the container belongs. If you specify a prefix with this option, then the log stream takes the following format:: prefix-name/container-name/ecs-task-id
        :param datetime_format: This option defines a multiline start pattern in Python strftime format. A log message consists of a line that matches the pattern and any following lines that don’t match the pattern. Thus the matched line is the delimiter between log messages. Default: - No multiline matching.
        :param log_group: The log group to log to. Default: - A log group is automatically created.
        :param log_retention: The number of days log events are kept in CloudWatch Logs when the log group is automatically created by this construct. Default: - Logs never expire.
        :param multiline_pattern: This option defines a multiline start pattern using a regular expression. A log message consists of a line that matches the pattern and any following lines that don’t match the pattern. Thus the matched line is the delimiter between log messages. This option is ignored if datetimeFormat is also configured. Default: - No multiline matching.

        stability
        :stability: experimental
        """
        self._values = {
            'stream_prefix': stream_prefix,
        }
        if datetime_format is not None: self._values["datetime_format"] = datetime_format
        if log_group is not None: self._values["log_group"] = log_group
        if log_retention is not None: self._values["log_retention"] = log_retention
        if multiline_pattern is not None: self._values["multiline_pattern"] = multiline_pattern

    @builtins.property
    def stream_prefix(self) -> str:
        """Prefix for the log streams.

        The awslogs-stream-prefix option allows you to associate a log stream
        with the specified prefix, the container name, and the ID of the Amazon
        ECS task to which the container belongs. If you specify a prefix with
        this option, then the log stream takes the following format::

            prefix-name/container-name/ecs-task-id

        stability
        :stability: experimental
        """
        return self._values.get('stream_prefix')

    @builtins.property
    def datetime_format(self) -> typing.Optional[str]:
        """This option defines a multiline start pattern in Python strftime format.

        A log message consists of a line that matches the pattern and any
        following lines that don’t match the pattern. Thus the matched line is
        the delimiter between log messages.

        default
        :default: - No multiline matching.

        stability
        :stability: experimental
        """
        return self._values.get('datetime_format')

    @builtins.property
    def log_group(self) -> typing.Optional[_ILogGroup_6b54c8e1]:
        """The log group to log to.

        default
        :default: - A log group is automatically created.

        stability
        :stability: experimental
        """
        return self._values.get('log_group')

    @builtins.property
    def log_retention(self) -> typing.Optional[_RetentionDays_bdc7ad1f]:
        """The number of days log events are kept in CloudWatch Logs when the log group is automatically created by this construct.

        default
        :default: - Logs never expire.

        stability
        :stability: experimental
        """
        return self._values.get('log_retention')

    @builtins.property
    def multiline_pattern(self) -> typing.Optional[str]:
        """This option defines a multiline start pattern using a regular expression.

        A log message consists of a line that matches the pattern and any
        following lines that don’t match the pattern. Thus the matched line is
        the delimiter between log messages.

        This option is ignored if datetimeFormat is also configured.

        default
        :default: - No multiline matching.

        stability
        :stability: experimental
        """
        return self._values.get('multiline_pattern')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AwsLogDriverProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.BaseLogDriverProps", jsii_struct_bases=[], name_mapping={'env': 'env', 'env_regex': 'envRegex', 'labels': 'labels', 'tag': 'tag'})
class BaseLogDriverProps():
    def __init__(self, *, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None) -> None:
        """
        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID

        stability
        :stability: experimental
        """
        self._values = {
        }
        if env is not None: self._values["env"] = env
        if env_regex is not None: self._values["env_regex"] = env_regex
        if labels is not None: self._values["labels"] = labels
        if tag is not None: self._values["tag"] = tag

    @builtins.property
    def env(self) -> typing.Optional[typing.List[str]]:
        """The env option takes an array of keys.

        If there is collision between
        label and env keys, the value of the env takes precedence. Adds additional fields
        to the extra attributes of a logging message.

        default
        :default: - No env

        stability
        :stability: experimental
        """
        return self._values.get('env')

    @builtins.property
    def env_regex(self) -> typing.Optional[str]:
        """The env-regex option is similar to and compatible with env.

        Its value is a regular
        expression to match logging-related environment variables. It is used for advanced
        log tag options.

        default
        :default: - No envRegex

        stability
        :stability: experimental
        """
        return self._values.get('env_regex')

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[str]]:
        """The labels option takes an array of keys.

        If there is collision
        between label and env keys, the value of the env takes precedence. Adds additional
        fields to the extra attributes of a logging message.

        default
        :default: - No labels

        stability
        :stability: experimental
        """
        return self._values.get('labels')

    @builtins.property
    def tag(self) -> typing.Optional[str]:
        """By default, Docker uses the first 12 characters of the container ID to tag log messages.

        Refer to the log tag option documentation for customizing the
        log tag format.

        default
        :default: - The first 12 characters of the container ID

        stability
        :stability: experimental
        """
        return self._values.get('tag')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BaseLogDriverProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.BaseServiceOptions", jsii_struct_bases=[], name_mapping={'cluster': 'cluster', 'cloud_map_options': 'cloudMapOptions', 'deployment_controller': 'deploymentController', 'desired_count': 'desiredCount', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'health_check_grace_period': 'healthCheckGracePeriod', 'max_healthy_percent': 'maxHealthyPercent', 'min_healthy_percent': 'minHealthyPercent', 'propagate_tags': 'propagateTags', 'service_name': 'serviceName'})
class BaseServiceOptions():
    def __init__(self, *, cluster: "ICluster", cloud_map_options: typing.Optional["CloudMapOptions"]=None, deployment_controller: typing.Optional["DeploymentController"]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[_Duration_5170c158]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional["PropagatedTagSource"]=None, service_name: typing.Optional[str]=None) -> None:
        """The properties for the base Ec2Service or FargateService service.

        :param cluster: The name of the cluster that hosts the service.
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param deployment_controller: Specifies which deployment controller to use for the service. For more information, see `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_ Default: - Rolling update (ECS)
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Valid values are: PropagatedTagSource.SERVICE, PropagatedTagSource.TASK_DEFINITION or PropagatedTagSource.NONE Default: PropagatedTagSource.NONE
        :param service_name: The name of the service. Default: - CloudFormation-generated name.

        stability
        :stability: experimental
        """
        if isinstance(cloud_map_options, dict): cloud_map_options = CloudMapOptions(**cloud_map_options)
        if isinstance(deployment_controller, dict): deployment_controller = DeploymentController(**deployment_controller)
        self._values = {
            'cluster': cluster,
        }
        if cloud_map_options is not None: self._values["cloud_map_options"] = cloud_map_options
        if deployment_controller is not None: self._values["deployment_controller"] = deployment_controller
        if desired_count is not None: self._values["desired_count"] = desired_count
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None: self._values["health_check_grace_period"] = health_check_grace_period
        if max_healthy_percent is not None: self._values["max_healthy_percent"] = max_healthy_percent
        if min_healthy_percent is not None: self._values["min_healthy_percent"] = min_healthy_percent
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if service_name is not None: self._values["service_name"] = service_name

    @builtins.property
    def cluster(self) -> "ICluster":
        """The name of the cluster that hosts the service.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @builtins.property
    def cloud_map_options(self) -> typing.Optional["CloudMapOptions"]:
        """The options for configuring an Amazon ECS service to use service discovery.

        default
        :default: - AWS Cloud Map service discovery is not enabled.

        stability
        :stability: experimental
        """
        return self._values.get('cloud_map_options')

    @builtins.property
    def deployment_controller(self) -> typing.Optional["DeploymentController"]:
        """Specifies which deployment controller to use for the service.

        For more information, see
        `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_

        default
        :default: - Rolling update (ECS)

        stability
        :stability: experimental
        """
        return self._values.get('deployment_controller')

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('desired_count')

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('enable_ecs_managed_tags')

    @builtins.property
    def health_check_grace_period(self) -> typing.Optional[_Duration_5170c158]:
        """The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        default
        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set

        stability
        :stability: experimental
        """
        return self._values.get('health_check_grace_period')

    @builtins.property
    def max_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment.

        default
        :default: - 100 if daemon, otherwise 200

        stability
        :stability: experimental
        """
        return self._values.get('max_healthy_percent')

    @builtins.property
    def min_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment.

        default
        :default: - 0 if daemon, otherwise 50

        stability
        :stability: experimental
        """
        return self._values.get('min_healthy_percent')

    @builtins.property
    def propagate_tags(self) -> typing.Optional["PropagatedTagSource"]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Valid values are: PropagatedTagSource.SERVICE, PropagatedTagSource.TASK_DEFINITION or PropagatedTagSource.NONE

        default
        :default: PropagatedTagSource.NONE

        stability
        :stability: experimental
        """
        return self._values.get('propagate_tags')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """The name of the service.

        default
        :default: - CloudFormation-generated name.

        stability
        :stability: experimental
        """
        return self._values.get('service_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BaseServiceOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.BaseServiceProps", jsii_struct_bases=[BaseServiceOptions], name_mapping={'cluster': 'cluster', 'cloud_map_options': 'cloudMapOptions', 'deployment_controller': 'deploymentController', 'desired_count': 'desiredCount', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'health_check_grace_period': 'healthCheckGracePeriod', 'max_healthy_percent': 'maxHealthyPercent', 'min_healthy_percent': 'minHealthyPercent', 'propagate_tags': 'propagateTags', 'service_name': 'serviceName', 'launch_type': 'launchType'})
class BaseServiceProps(BaseServiceOptions):
    def __init__(self, *, cluster: "ICluster", cloud_map_options: typing.Optional["CloudMapOptions"]=None, deployment_controller: typing.Optional["DeploymentController"]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[_Duration_5170c158]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional["PropagatedTagSource"]=None, service_name: typing.Optional[str]=None, launch_type: "LaunchType") -> None:
        """Complete base service properties that are required to be supplied by the implementation of the BaseService class.

        :param cluster: The name of the cluster that hosts the service.
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param deployment_controller: Specifies which deployment controller to use for the service. For more information, see `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_ Default: - Rolling update (ECS)
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Valid values are: PropagatedTagSource.SERVICE, PropagatedTagSource.TASK_DEFINITION or PropagatedTagSource.NONE Default: PropagatedTagSource.NONE
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param launch_type: The launch type on which to run your service. Valid values are: LaunchType.ECS or LaunchType.FARGATE

        stability
        :stability: experimental
        """
        if isinstance(cloud_map_options, dict): cloud_map_options = CloudMapOptions(**cloud_map_options)
        if isinstance(deployment_controller, dict): deployment_controller = DeploymentController(**deployment_controller)
        self._values = {
            'cluster': cluster,
            'launch_type': launch_type,
        }
        if cloud_map_options is not None: self._values["cloud_map_options"] = cloud_map_options
        if deployment_controller is not None: self._values["deployment_controller"] = deployment_controller
        if desired_count is not None: self._values["desired_count"] = desired_count
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None: self._values["health_check_grace_period"] = health_check_grace_period
        if max_healthy_percent is not None: self._values["max_healthy_percent"] = max_healthy_percent
        if min_healthy_percent is not None: self._values["min_healthy_percent"] = min_healthy_percent
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if service_name is not None: self._values["service_name"] = service_name

    @builtins.property
    def cluster(self) -> "ICluster":
        """The name of the cluster that hosts the service.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @builtins.property
    def cloud_map_options(self) -> typing.Optional["CloudMapOptions"]:
        """The options for configuring an Amazon ECS service to use service discovery.

        default
        :default: - AWS Cloud Map service discovery is not enabled.

        stability
        :stability: experimental
        """
        return self._values.get('cloud_map_options')

    @builtins.property
    def deployment_controller(self) -> typing.Optional["DeploymentController"]:
        """Specifies which deployment controller to use for the service.

        For more information, see
        `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_

        default
        :default: - Rolling update (ECS)

        stability
        :stability: experimental
        """
        return self._values.get('deployment_controller')

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('desired_count')

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('enable_ecs_managed_tags')

    @builtins.property
    def health_check_grace_period(self) -> typing.Optional[_Duration_5170c158]:
        """The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        default
        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set

        stability
        :stability: experimental
        """
        return self._values.get('health_check_grace_period')

    @builtins.property
    def max_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment.

        default
        :default: - 100 if daemon, otherwise 200

        stability
        :stability: experimental
        """
        return self._values.get('max_healthy_percent')

    @builtins.property
    def min_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment.

        default
        :default: - 0 if daemon, otherwise 50

        stability
        :stability: experimental
        """
        return self._values.get('min_healthy_percent')

    @builtins.property
    def propagate_tags(self) -> typing.Optional["PropagatedTagSource"]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Valid values are: PropagatedTagSource.SERVICE, PropagatedTagSource.TASK_DEFINITION or PropagatedTagSource.NONE

        default
        :default: PropagatedTagSource.NONE

        stability
        :stability: experimental
        """
        return self._values.get('propagate_tags')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """The name of the service.

        default
        :default: - CloudFormation-generated name.

        stability
        :stability: experimental
        """
        return self._values.get('service_name')

    @builtins.property
    def launch_type(self) -> "LaunchType":
        """The launch type on which to run your service.

        Valid values are: LaunchType.ECS or LaunchType.FARGATE

        stability
        :stability: experimental
        """
        return self._values.get('launch_type')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BaseServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.aws_ecs.BinPackResource")
class BinPackResource(enum.Enum):
    """Instance resource used for bin packing.

    stability
    :stability: experimental
    """
    CPU = "CPU"
    """Fill up hosts' CPU allocations first.

    stability
    :stability: experimental
    """
    MEMORY = "MEMORY"
    """Fill up hosts' memory allocations first.

    stability
    :stability: experimental
    """

class BuiltInAttributes(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs.BuiltInAttributes"):
    """The built-in container instance attributes.

    stability
    :stability: experimental
    """
    def __init__(self) -> None:
        jsii.create(BuiltInAttributes, self, [])

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMI_ID")
    def AMI_ID(cls) -> str:
        """The AMI id the instance is using.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "AMI_ID")

    @jsii.python.classproperty
    @jsii.member(jsii_name="AVAILABILITY_ZONE")
    def AVAILABILITY_ZONE(cls) -> str:
        """The AvailabilityZone where the instance is running in.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "AVAILABILITY_ZONE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="INSTANCE_ID")
    def INSTANCE_ID(cls) -> str:
        """The id of the instance.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "INSTANCE_ID")

    @jsii.python.classproperty
    @jsii.member(jsii_name="INSTANCE_TYPE")
    def INSTANCE_TYPE(cls) -> str:
        """The EC2 instance type.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "INSTANCE_TYPE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="OS_TYPE")
    def OS_TYPE(cls) -> str:
        """The operating system of the instance.

        Either 'linux' or 'windows'.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "OS_TYPE")


@jsii.enum(jsii_type="monocdk-experiment.aws_ecs.Capability")
class Capability(enum.Enum):
    """A Linux capability.

    stability
    :stability: experimental
    """
    ALL = "ALL"
    """
    stability
    :stability: experimental
    """
    AUDIT_CONTROL = "AUDIT_CONTROL"
    """
    stability
    :stability: experimental
    """
    AUDIT_WRITE = "AUDIT_WRITE"
    """
    stability
    :stability: experimental
    """
    BLOCK_SUSPEND = "BLOCK_SUSPEND"
    """
    stability
    :stability: experimental
    """
    CHOWN = "CHOWN"
    """
    stability
    :stability: experimental
    """
    DAC_OVERRIDE = "DAC_OVERRIDE"
    """
    stability
    :stability: experimental
    """
    DAC_READ_SEARCH = "DAC_READ_SEARCH"
    """
    stability
    :stability: experimental
    """
    FOWNER = "FOWNER"
    """
    stability
    :stability: experimental
    """
    FSETID = "FSETID"
    """
    stability
    :stability: experimental
    """
    IPC_LOCK = "IPC_LOCK"
    """
    stability
    :stability: experimental
    """
    IPC_OWNER = "IPC_OWNER"
    """
    stability
    :stability: experimental
    """
    KILL = "KILL"
    """
    stability
    :stability: experimental
    """
    LEASE = "LEASE"
    """
    stability
    :stability: experimental
    """
    LINUX_IMMUTABLE = "LINUX_IMMUTABLE"
    """
    stability
    :stability: experimental
    """
    MAC_ADMIN = "MAC_ADMIN"
    """
    stability
    :stability: experimental
    """
    MAC_OVERRIDE = "MAC_OVERRIDE"
    """
    stability
    :stability: experimental
    """
    MKNOD = "MKNOD"
    """
    stability
    :stability: experimental
    """
    NET_ADMIN = "NET_ADMIN"
    """
    stability
    :stability: experimental
    """
    NET_BIND_SERVICE = "NET_BIND_SERVICE"
    """
    stability
    :stability: experimental
    """
    NET_BROADCAST = "NET_BROADCAST"
    """
    stability
    :stability: experimental
    """
    NET_RAW = "NET_RAW"
    """
    stability
    :stability: experimental
    """
    SETFCAP = "SETFCAP"
    """
    stability
    :stability: experimental
    """
    SETGID = "SETGID"
    """
    stability
    :stability: experimental
    """
    SETPCAP = "SETPCAP"
    """
    stability
    :stability: experimental
    """
    SETUID = "SETUID"
    """
    stability
    :stability: experimental
    """
    SYS_ADMIN = "SYS_ADMIN"
    """
    stability
    :stability: experimental
    """
    SYS_BOOT = "SYS_BOOT"
    """
    stability
    :stability: experimental
    """
    SYS_CHROOT = "SYS_CHROOT"
    """
    stability
    :stability: experimental
    """
    SYS_MODULE = "SYS_MODULE"
    """
    stability
    :stability: experimental
    """
    SYS_NICE = "SYS_NICE"
    """
    stability
    :stability: experimental
    """
    SYS_PACCT = "SYS_PACCT"
    """
    stability
    :stability: experimental
    """
    SYS_PTRACE = "SYS_PTRACE"
    """
    stability
    :stability: experimental
    """
    SYS_RAWIO = "SYS_RAWIO"
    """
    stability
    :stability: experimental
    """
    SYS_RESOURCE = "SYS_RESOURCE"
    """
    stability
    :stability: experimental
    """
    SYS_TIME = "SYS_TIME"
    """
    stability
    :stability: experimental
    """
    SYS_TTY_CONFIG = "SYS_TTY_CONFIG"
    """
    stability
    :stability: experimental
    """
    SYSLOG = "SYSLOG"
    """
    stability
    :stability: experimental
    """
    WAKE_ALARM = "WAKE_ALARM"
    """
    stability
    :stability: experimental
    """

@jsii.implements(_IInspectable_051e6ed8)
class CfnCapacityProvider(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs.CfnCapacityProvider"):
    """A CloudFormation ``AWS::ECS::CapacityProvider``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-capacityprovider.html
    cloudformationResource:
    :cloudformationResource:: AWS::ECS::CapacityProvider
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, auto_scaling_group_provider: typing.Union["AutoScalingGroupProviderProperty", _IResolvable_9ceae33e], name: typing.Optional[str]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Create a new ``AWS::ECS::CapacityProvider``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param auto_scaling_group_provider: ``AWS::ECS::CapacityProvider.AutoScalingGroupProvider``.
        :param name: ``AWS::ECS::CapacityProvider.Name``.
        :param tags: ``AWS::ECS::CapacityProvider.Tags``.
        """
        props = CfnCapacityProviderProps(auto_scaling_group_provider=auto_scaling_group_provider, name=name, tags=tags)

        jsii.create(CfnCapacityProvider, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnCapacityProvider":
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
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::ECS::CapacityProvider.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-capacityprovider.html#cfn-ecs-capacityprovider-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="autoScalingGroupProvider")
    def auto_scaling_group_provider(self) -> typing.Union["AutoScalingGroupProviderProperty", _IResolvable_9ceae33e]:
        """``AWS::ECS::CapacityProvider.AutoScalingGroupProvider``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-capacityprovider.html#cfn-ecs-capacityprovider-autoscalinggroupprovider
        """
        return jsii.get(self, "autoScalingGroupProvider")

    @auto_scaling_group_provider.setter
    def auto_scaling_group_provider(self, value: typing.Union["AutoScalingGroupProviderProperty", _IResolvable_9ceae33e]) -> None:
        jsii.set(self, "autoScalingGroupProvider", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::ECS::CapacityProvider.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-capacityprovider.html#cfn-ecs-capacityprovider-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "name", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnCapacityProvider.AutoScalingGroupProviderProperty", jsii_struct_bases=[], name_mapping={'auto_scaling_group_arn': 'autoScalingGroupArn', 'managed_scaling': 'managedScaling', 'managed_termination_protection': 'managedTerminationProtection'})
    class AutoScalingGroupProviderProperty():
        def __init__(self, *, auto_scaling_group_arn: str, managed_scaling: typing.Optional[typing.Union["CfnCapacityProvider.ManagedScalingProperty", _IResolvable_9ceae33e]]=None, managed_termination_protection: typing.Optional[str]=None) -> None:
            """
            :param auto_scaling_group_arn: ``CfnCapacityProvider.AutoScalingGroupProviderProperty.AutoScalingGroupArn``.
            :param managed_scaling: ``CfnCapacityProvider.AutoScalingGroupProviderProperty.ManagedScaling``.
            :param managed_termination_protection: ``CfnCapacityProvider.AutoScalingGroupProviderProperty.ManagedTerminationProtection``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-capacityprovider-autoscalinggroupprovider.html
            """
            self._values = {
                'auto_scaling_group_arn': auto_scaling_group_arn,
            }
            if managed_scaling is not None: self._values["managed_scaling"] = managed_scaling
            if managed_termination_protection is not None: self._values["managed_termination_protection"] = managed_termination_protection

        @builtins.property
        def auto_scaling_group_arn(self) -> str:
            """``CfnCapacityProvider.AutoScalingGroupProviderProperty.AutoScalingGroupArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-capacityprovider-autoscalinggroupprovider.html#cfn-ecs-capacityprovider-autoscalinggroupprovider-autoscalinggrouparn
            """
            return self._values.get('auto_scaling_group_arn')

        @builtins.property
        def managed_scaling(self) -> typing.Optional[typing.Union["CfnCapacityProvider.ManagedScalingProperty", _IResolvable_9ceae33e]]:
            """``CfnCapacityProvider.AutoScalingGroupProviderProperty.ManagedScaling``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-capacityprovider-autoscalinggroupprovider.html#cfn-ecs-capacityprovider-autoscalinggroupprovider-managedscaling
            """
            return self._values.get('managed_scaling')

        @builtins.property
        def managed_termination_protection(self) -> typing.Optional[str]:
            """``CfnCapacityProvider.AutoScalingGroupProviderProperty.ManagedTerminationProtection``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-capacityprovider-autoscalinggroupprovider.html#cfn-ecs-capacityprovider-autoscalinggroupprovider-managedterminationprotection
            """
            return self._values.get('managed_termination_protection')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AutoScalingGroupProviderProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnCapacityProvider.ManagedScalingProperty", jsii_struct_bases=[], name_mapping={'maximum_scaling_step_size': 'maximumScalingStepSize', 'minimum_scaling_step_size': 'minimumScalingStepSize', 'status': 'status', 'target_capacity': 'targetCapacity'})
    class ManagedScalingProperty():
        def __init__(self, *, maximum_scaling_step_size: typing.Optional[jsii.Number]=None, minimum_scaling_step_size: typing.Optional[jsii.Number]=None, status: typing.Optional[str]=None, target_capacity: typing.Optional[jsii.Number]=None) -> None:
            """
            :param maximum_scaling_step_size: ``CfnCapacityProvider.ManagedScalingProperty.MaximumScalingStepSize``.
            :param minimum_scaling_step_size: ``CfnCapacityProvider.ManagedScalingProperty.MinimumScalingStepSize``.
            :param status: ``CfnCapacityProvider.ManagedScalingProperty.Status``.
            :param target_capacity: ``CfnCapacityProvider.ManagedScalingProperty.TargetCapacity``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-capacityprovider-managedscaling.html
            """
            self._values = {
            }
            if maximum_scaling_step_size is not None: self._values["maximum_scaling_step_size"] = maximum_scaling_step_size
            if minimum_scaling_step_size is not None: self._values["minimum_scaling_step_size"] = minimum_scaling_step_size
            if status is not None: self._values["status"] = status
            if target_capacity is not None: self._values["target_capacity"] = target_capacity

        @builtins.property
        def maximum_scaling_step_size(self) -> typing.Optional[jsii.Number]:
            """``CfnCapacityProvider.ManagedScalingProperty.MaximumScalingStepSize``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-capacityprovider-managedscaling.html#cfn-ecs-capacityprovider-managedscaling-maximumscalingstepsize
            """
            return self._values.get('maximum_scaling_step_size')

        @builtins.property
        def minimum_scaling_step_size(self) -> typing.Optional[jsii.Number]:
            """``CfnCapacityProvider.ManagedScalingProperty.MinimumScalingStepSize``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-capacityprovider-managedscaling.html#cfn-ecs-capacityprovider-managedscaling-minimumscalingstepsize
            """
            return self._values.get('minimum_scaling_step_size')

        @builtins.property
        def status(self) -> typing.Optional[str]:
            """``CfnCapacityProvider.ManagedScalingProperty.Status``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-capacityprovider-managedscaling.html#cfn-ecs-capacityprovider-managedscaling-status
            """
            return self._values.get('status')

        @builtins.property
        def target_capacity(self) -> typing.Optional[jsii.Number]:
            """``CfnCapacityProvider.ManagedScalingProperty.TargetCapacity``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-capacityprovider-managedscaling.html#cfn-ecs-capacityprovider-managedscaling-targetcapacity
            """
            return self._values.get('target_capacity')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ManagedScalingProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnCapacityProviderProps", jsii_struct_bases=[], name_mapping={'auto_scaling_group_provider': 'autoScalingGroupProvider', 'name': 'name', 'tags': 'tags'})
class CfnCapacityProviderProps():
    def __init__(self, *, auto_scaling_group_provider: typing.Union["CfnCapacityProvider.AutoScalingGroupProviderProperty", _IResolvable_9ceae33e], name: typing.Optional[str]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Properties for defining a ``AWS::ECS::CapacityProvider``.

        :param auto_scaling_group_provider: ``AWS::ECS::CapacityProvider.AutoScalingGroupProvider``.
        :param name: ``AWS::ECS::CapacityProvider.Name``.
        :param tags: ``AWS::ECS::CapacityProvider.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-capacityprovider.html
        """
        self._values = {
            'auto_scaling_group_provider': auto_scaling_group_provider,
        }
        if name is not None: self._values["name"] = name
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def auto_scaling_group_provider(self) -> typing.Union["CfnCapacityProvider.AutoScalingGroupProviderProperty", _IResolvable_9ceae33e]:
        """``AWS::ECS::CapacityProvider.AutoScalingGroupProvider``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-capacityprovider.html#cfn-ecs-capacityprovider-autoscalinggroupprovider
        """
        return self._values.get('auto_scaling_group_provider')

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """``AWS::ECS::CapacityProvider.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-capacityprovider.html#cfn-ecs-capacityprovider-name
        """
        return self._values.get('name')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::ECS::CapacityProvider.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-capacityprovider.html#cfn-ecs-capacityprovider-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnCapacityProviderProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnCluster(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs.CfnCluster"):
    """A CloudFormation ``AWS::ECS::Cluster``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-cluster.html
    cloudformationResource:
    :cloudformationResource:: AWS::ECS::Cluster
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, capacity_providers: typing.Optional[typing.List[str]]=None, cluster_name: typing.Optional[str]=None, cluster_settings: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ClusterSettingsProperty", _IResolvable_9ceae33e]]]]=None, default_capacity_provider_strategy: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CapacityProviderStrategyItemProperty", _IResolvable_9ceae33e]]]]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Create a new ``AWS::ECS::Cluster``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param capacity_providers: ``AWS::ECS::Cluster.CapacityProviders``.
        :param cluster_name: ``AWS::ECS::Cluster.ClusterName``.
        :param cluster_settings: ``AWS::ECS::Cluster.ClusterSettings``.
        :param default_capacity_provider_strategy: ``AWS::ECS::Cluster.DefaultCapacityProviderStrategy``.
        :param tags: ``AWS::ECS::Cluster.Tags``.
        """
        props = CfnClusterProps(capacity_providers=capacity_providers, cluster_name=cluster_name, cluster_settings=cluster_settings, default_capacity_provider_strategy=default_capacity_provider_strategy, tags=tags)

        jsii.create(CfnCluster, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnCluster":
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
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Arn
        """
        return jsii.get(self, "attrArn")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::ECS::Cluster.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-cluster.html#cfn-ecs-cluster-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="capacityProviders")
    def capacity_providers(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ECS::Cluster.CapacityProviders``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-cluster.html#cfn-ecs-cluster-capacityproviders
        """
        return jsii.get(self, "capacityProviders")

    @capacity_providers.setter
    def capacity_providers(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "capacityProviders", value)

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> typing.Optional[str]:
        """``AWS::ECS::Cluster.ClusterName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-cluster.html#cfn-ecs-cluster-clustername
        """
        return jsii.get(self, "clusterName")

    @cluster_name.setter
    def cluster_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "clusterName", value)

    @builtins.property
    @jsii.member(jsii_name="clusterSettings")
    def cluster_settings(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ClusterSettingsProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::ECS::Cluster.ClusterSettings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-cluster.html#cfn-ecs-cluster-clustersettings
        """
        return jsii.get(self, "clusterSettings")

    @cluster_settings.setter
    def cluster_settings(self, value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ClusterSettingsProperty", _IResolvable_9ceae33e]]]]) -> None:
        jsii.set(self, "clusterSettings", value)

    @builtins.property
    @jsii.member(jsii_name="defaultCapacityProviderStrategy")
    def default_capacity_provider_strategy(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CapacityProviderStrategyItemProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::ECS::Cluster.DefaultCapacityProviderStrategy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-cluster.html#cfn-ecs-cluster-defaultcapacityproviderstrategy
        """
        return jsii.get(self, "defaultCapacityProviderStrategy")

    @default_capacity_provider_strategy.setter
    def default_capacity_provider_strategy(self, value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CapacityProviderStrategyItemProperty", _IResolvable_9ceae33e]]]]) -> None:
        jsii.set(self, "defaultCapacityProviderStrategy", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnCluster.CapacityProviderStrategyItemProperty", jsii_struct_bases=[], name_mapping={'base': 'base', 'capacity_provider': 'capacityProvider', 'weight': 'weight'})
    class CapacityProviderStrategyItemProperty():
        def __init__(self, *, base: typing.Optional[jsii.Number]=None, capacity_provider: typing.Optional[str]=None, weight: typing.Optional[jsii.Number]=None) -> None:
            """
            :param base: ``CfnCluster.CapacityProviderStrategyItemProperty.Base``.
            :param capacity_provider: ``CfnCluster.CapacityProviderStrategyItemProperty.CapacityProvider``.
            :param weight: ``CfnCluster.CapacityProviderStrategyItemProperty.Weight``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-cluster-capacityproviderstrategyitem.html
            """
            self._values = {
            }
            if base is not None: self._values["base"] = base
            if capacity_provider is not None: self._values["capacity_provider"] = capacity_provider
            if weight is not None: self._values["weight"] = weight

        @builtins.property
        def base(self) -> typing.Optional[jsii.Number]:
            """``CfnCluster.CapacityProviderStrategyItemProperty.Base``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-cluster-capacityproviderstrategyitem.html#cfn-ecs-cluster-capacityproviderstrategyitem-base
            """
            return self._values.get('base')

        @builtins.property
        def capacity_provider(self) -> typing.Optional[str]:
            """``CfnCluster.CapacityProviderStrategyItemProperty.CapacityProvider``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-cluster-capacityproviderstrategyitem.html#cfn-ecs-cluster-capacityproviderstrategyitem-capacityprovider
            """
            return self._values.get('capacity_provider')

        @builtins.property
        def weight(self) -> typing.Optional[jsii.Number]:
            """``CfnCluster.CapacityProviderStrategyItemProperty.Weight``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-cluster-capacityproviderstrategyitem.html#cfn-ecs-cluster-capacityproviderstrategyitem-weight
            """
            return self._values.get('weight')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CapacityProviderStrategyItemProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnCluster.ClusterSettingsProperty", jsii_struct_bases=[], name_mapping={'name': 'name', 'value': 'value'})
    class ClusterSettingsProperty():
        def __init__(self, *, name: typing.Optional[str]=None, value: typing.Optional[str]=None) -> None:
            """
            :param name: ``CfnCluster.ClusterSettingsProperty.Name``.
            :param value: ``CfnCluster.ClusterSettingsProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-cluster-clustersettings.html
            """
            self._values = {
            }
            if name is not None: self._values["name"] = name
            if value is not None: self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[str]:
            """``CfnCluster.ClusterSettingsProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-cluster-clustersettings.html#cfn-ecs-cluster-clustersettings-name
            """
            return self._values.get('name')

        @builtins.property
        def value(self) -> typing.Optional[str]:
            """``CfnCluster.ClusterSettingsProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-cluster-clustersettings.html#cfn-ecs-cluster-clustersettings-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ClusterSettingsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnClusterProps", jsii_struct_bases=[], name_mapping={'capacity_providers': 'capacityProviders', 'cluster_name': 'clusterName', 'cluster_settings': 'clusterSettings', 'default_capacity_provider_strategy': 'defaultCapacityProviderStrategy', 'tags': 'tags'})
class CfnClusterProps():
    def __init__(self, *, capacity_providers: typing.Optional[typing.List[str]]=None, cluster_name: typing.Optional[str]=None, cluster_settings: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnCluster.ClusterSettingsProperty", _IResolvable_9ceae33e]]]]=None, default_capacity_provider_strategy: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnCluster.CapacityProviderStrategyItemProperty", _IResolvable_9ceae33e]]]]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Properties for defining a ``AWS::ECS::Cluster``.

        :param capacity_providers: ``AWS::ECS::Cluster.CapacityProviders``.
        :param cluster_name: ``AWS::ECS::Cluster.ClusterName``.
        :param cluster_settings: ``AWS::ECS::Cluster.ClusterSettings``.
        :param default_capacity_provider_strategy: ``AWS::ECS::Cluster.DefaultCapacityProviderStrategy``.
        :param tags: ``AWS::ECS::Cluster.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-cluster.html
        """
        self._values = {
        }
        if capacity_providers is not None: self._values["capacity_providers"] = capacity_providers
        if cluster_name is not None: self._values["cluster_name"] = cluster_name
        if cluster_settings is not None: self._values["cluster_settings"] = cluster_settings
        if default_capacity_provider_strategy is not None: self._values["default_capacity_provider_strategy"] = default_capacity_provider_strategy
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def capacity_providers(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ECS::Cluster.CapacityProviders``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-cluster.html#cfn-ecs-cluster-capacityproviders
        """
        return self._values.get('capacity_providers')

    @builtins.property
    def cluster_name(self) -> typing.Optional[str]:
        """``AWS::ECS::Cluster.ClusterName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-cluster.html#cfn-ecs-cluster-clustername
        """
        return self._values.get('cluster_name')

    @builtins.property
    def cluster_settings(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnCluster.ClusterSettingsProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::ECS::Cluster.ClusterSettings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-cluster.html#cfn-ecs-cluster-clustersettings
        """
        return self._values.get('cluster_settings')

    @builtins.property
    def default_capacity_provider_strategy(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnCluster.CapacityProviderStrategyItemProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::ECS::Cluster.DefaultCapacityProviderStrategy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-cluster.html#cfn-ecs-cluster-defaultcapacityproviderstrategy
        """
        return self._values.get('default_capacity_provider_strategy')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::ECS::Cluster.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-cluster.html#cfn-ecs-cluster-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnClusterProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnPrimaryTaskSet(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs.CfnPrimaryTaskSet"):
    """A CloudFormation ``AWS::ECS::PrimaryTaskSet``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-primarytaskset.html
    cloudformationResource:
    :cloudformationResource:: AWS::ECS::PrimaryTaskSet
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, cluster: str, service: str, task_set_id: str) -> None:
        """Create a new ``AWS::ECS::PrimaryTaskSet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param cluster: ``AWS::ECS::PrimaryTaskSet.Cluster``.
        :param service: ``AWS::ECS::PrimaryTaskSet.Service``.
        :param task_set_id: ``AWS::ECS::PrimaryTaskSet.TaskSetId``.
        """
        props = CfnPrimaryTaskSetProps(cluster=cluster, service=service, task_set_id=task_set_id)

        jsii.create(CfnPrimaryTaskSet, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnPrimaryTaskSet":
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
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> str:
        """``AWS::ECS::PrimaryTaskSet.Cluster``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-primarytaskset.html#cfn-ecs-primarytaskset-cluster
        """
        return jsii.get(self, "cluster")

    @cluster.setter
    def cluster(self, value: str) -> None:
        jsii.set(self, "cluster", value)

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> str:
        """``AWS::ECS::PrimaryTaskSet.Service``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-primarytaskset.html#cfn-ecs-primarytaskset-service
        """
        return jsii.get(self, "service")

    @service.setter
    def service(self, value: str) -> None:
        jsii.set(self, "service", value)

    @builtins.property
    @jsii.member(jsii_name="taskSetId")
    def task_set_id(self) -> str:
        """``AWS::ECS::PrimaryTaskSet.TaskSetId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-primarytaskset.html#cfn-ecs-primarytaskset-tasksetid
        """
        return jsii.get(self, "taskSetId")

    @task_set_id.setter
    def task_set_id(self, value: str) -> None:
        jsii.set(self, "taskSetId", value)


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnPrimaryTaskSetProps", jsii_struct_bases=[], name_mapping={'cluster': 'cluster', 'service': 'service', 'task_set_id': 'taskSetId'})
class CfnPrimaryTaskSetProps():
    def __init__(self, *, cluster: str, service: str, task_set_id: str) -> None:
        """Properties for defining a ``AWS::ECS::PrimaryTaskSet``.

        :param cluster: ``AWS::ECS::PrimaryTaskSet.Cluster``.
        :param service: ``AWS::ECS::PrimaryTaskSet.Service``.
        :param task_set_id: ``AWS::ECS::PrimaryTaskSet.TaskSetId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-primarytaskset.html
        """
        self._values = {
            'cluster': cluster,
            'service': service,
            'task_set_id': task_set_id,
        }

    @builtins.property
    def cluster(self) -> str:
        """``AWS::ECS::PrimaryTaskSet.Cluster``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-primarytaskset.html#cfn-ecs-primarytaskset-cluster
        """
        return self._values.get('cluster')

    @builtins.property
    def service(self) -> str:
        """``AWS::ECS::PrimaryTaskSet.Service``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-primarytaskset.html#cfn-ecs-primarytaskset-service
        """
        return self._values.get('service')

    @builtins.property
    def task_set_id(self) -> str:
        """``AWS::ECS::PrimaryTaskSet.TaskSetId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-primarytaskset.html#cfn-ecs-primarytaskset-tasksetid
        """
        return self._values.get('task_set_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnPrimaryTaskSetProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnService(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs.CfnService"):
    """A CloudFormation ``AWS::ECS::Service``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html
    cloudformationResource:
    :cloudformationResource:: AWS::ECS::Service
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, cluster: typing.Optional[str]=None, deployment_configuration: typing.Optional[typing.Union["DeploymentConfigurationProperty", _IResolvable_9ceae33e]]=None, deployment_controller: typing.Optional[typing.Union["DeploymentControllerProperty", _IResolvable_9ceae33e]]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, health_check_grace_period_seconds: typing.Optional[jsii.Number]=None, launch_type: typing.Optional[str]=None, load_balancers: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["LoadBalancerProperty", _IResolvable_9ceae33e]]]]=None, network_configuration: typing.Optional[typing.Union["NetworkConfigurationProperty", _IResolvable_9ceae33e]]=None, placement_constraints: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["PlacementConstraintProperty", _IResolvable_9ceae33e]]]]=None, placement_strategies: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["PlacementStrategyProperty", _IResolvable_9ceae33e]]]]=None, platform_version: typing.Optional[str]=None, propagate_tags: typing.Optional[str]=None, role: typing.Optional[str]=None, scheduling_strategy: typing.Optional[str]=None, service_name: typing.Optional[str]=None, service_registries: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ServiceRegistryProperty", _IResolvable_9ceae33e]]]]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None, task_definition: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ECS::Service``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param cluster: ``AWS::ECS::Service.Cluster``.
        :param deployment_configuration: ``AWS::ECS::Service.DeploymentConfiguration``.
        :param deployment_controller: ``AWS::ECS::Service.DeploymentController``.
        :param desired_count: ``AWS::ECS::Service.DesiredCount``.
        :param enable_ecs_managed_tags: ``AWS::ECS::Service.EnableECSManagedTags``.
        :param health_check_grace_period_seconds: ``AWS::ECS::Service.HealthCheckGracePeriodSeconds``.
        :param launch_type: ``AWS::ECS::Service.LaunchType``.
        :param load_balancers: ``AWS::ECS::Service.LoadBalancers``.
        :param network_configuration: ``AWS::ECS::Service.NetworkConfiguration``.
        :param placement_constraints: ``AWS::ECS::Service.PlacementConstraints``.
        :param placement_strategies: ``AWS::ECS::Service.PlacementStrategies``.
        :param platform_version: ``AWS::ECS::Service.PlatformVersion``.
        :param propagate_tags: ``AWS::ECS::Service.PropagateTags``.
        :param role: ``AWS::ECS::Service.Role``.
        :param scheduling_strategy: ``AWS::ECS::Service.SchedulingStrategy``.
        :param service_name: ``AWS::ECS::Service.ServiceName``.
        :param service_registries: ``AWS::ECS::Service.ServiceRegistries``.
        :param tags: ``AWS::ECS::Service.Tags``.
        :param task_definition: ``AWS::ECS::Service.TaskDefinition``.
        """
        props = CfnServiceProps(cluster=cluster, deployment_configuration=deployment_configuration, deployment_controller=deployment_controller, desired_count=desired_count, enable_ecs_managed_tags=enable_ecs_managed_tags, health_check_grace_period_seconds=health_check_grace_period_seconds, launch_type=launch_type, load_balancers=load_balancers, network_configuration=network_configuration, placement_constraints=placement_constraints, placement_strategies=placement_strategies, platform_version=platform_version, propagate_tags=propagate_tags, role=role, scheduling_strategy=scheduling_strategy, service_name=service_name, service_registries=service_registries, tags=tags, task_definition=task_definition)

        jsii.create(CfnService, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnService":
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
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Name
        """
        return jsii.get(self, "attrName")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::ECS::Service.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.Cluster``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-cluster
        """
        return jsii.get(self, "cluster")

    @cluster.setter
    def cluster(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "cluster", value)

    @builtins.property
    @jsii.member(jsii_name="deploymentConfiguration")
    def deployment_configuration(self) -> typing.Optional[typing.Union["DeploymentConfigurationProperty", _IResolvable_9ceae33e]]:
        """``AWS::ECS::Service.DeploymentConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-deploymentconfiguration
        """
        return jsii.get(self, "deploymentConfiguration")

    @deployment_configuration.setter
    def deployment_configuration(self, value: typing.Optional[typing.Union["DeploymentConfigurationProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "deploymentConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="deploymentController")
    def deployment_controller(self) -> typing.Optional[typing.Union["DeploymentControllerProperty", _IResolvable_9ceae33e]]:
        """``AWS::ECS::Service.DeploymentController``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-deploymentcontroller
        """
        return jsii.get(self, "deploymentController")

    @deployment_controller.setter
    def deployment_controller(self, value: typing.Optional[typing.Union["DeploymentControllerProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "deploymentController", value)

    @builtins.property
    @jsii.member(jsii_name="desiredCount")
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """``AWS::ECS::Service.DesiredCount``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-desiredcount
        """
        return jsii.get(self, "desiredCount")

    @desired_count.setter
    def desired_count(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "desiredCount", value)

    @builtins.property
    @jsii.member(jsii_name="enableEcsManagedTags")
    def enable_ecs_managed_tags(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::ECS::Service.EnableECSManagedTags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-enableecsmanagedtags
        """
        return jsii.get(self, "enableEcsManagedTags")

    @enable_ecs_managed_tags.setter
    def enable_ecs_managed_tags(self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "enableEcsManagedTags", value)

    @builtins.property
    @jsii.member(jsii_name="healthCheckGracePeriodSeconds")
    def health_check_grace_period_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::ECS::Service.HealthCheckGracePeriodSeconds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-healthcheckgraceperiodseconds
        """
        return jsii.get(self, "healthCheckGracePeriodSeconds")

    @health_check_grace_period_seconds.setter
    def health_check_grace_period_seconds(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "healthCheckGracePeriodSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="launchType")
    def launch_type(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.LaunchType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-launchtype
        """
        return jsii.get(self, "launchType")

    @launch_type.setter
    def launch_type(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "launchType", value)

    @builtins.property
    @jsii.member(jsii_name="loadBalancers")
    def load_balancers(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["LoadBalancerProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::ECS::Service.LoadBalancers``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-loadbalancers
        """
        return jsii.get(self, "loadBalancers")

    @load_balancers.setter
    def load_balancers(self, value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["LoadBalancerProperty", _IResolvable_9ceae33e]]]]) -> None:
        jsii.set(self, "loadBalancers", value)

    @builtins.property
    @jsii.member(jsii_name="networkConfiguration")
    def network_configuration(self) -> typing.Optional[typing.Union["NetworkConfigurationProperty", _IResolvable_9ceae33e]]:
        """``AWS::ECS::Service.NetworkConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-networkconfiguration
        """
        return jsii.get(self, "networkConfiguration")

    @network_configuration.setter
    def network_configuration(self, value: typing.Optional[typing.Union["NetworkConfigurationProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "networkConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="placementConstraints")
    def placement_constraints(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["PlacementConstraintProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::ECS::Service.PlacementConstraints``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-placementconstraints
        """
        return jsii.get(self, "placementConstraints")

    @placement_constraints.setter
    def placement_constraints(self, value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["PlacementConstraintProperty", _IResolvable_9ceae33e]]]]) -> None:
        jsii.set(self, "placementConstraints", value)

    @builtins.property
    @jsii.member(jsii_name="placementStrategies")
    def placement_strategies(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["PlacementStrategyProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::ECS::Service.PlacementStrategies``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-placementstrategies
        """
        return jsii.get(self, "placementStrategies")

    @placement_strategies.setter
    def placement_strategies(self, value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["PlacementStrategyProperty", _IResolvable_9ceae33e]]]]) -> None:
        jsii.set(self, "placementStrategies", value)

    @builtins.property
    @jsii.member(jsii_name="platformVersion")
    def platform_version(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.PlatformVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-platformversion
        """
        return jsii.get(self, "platformVersion")

    @platform_version.setter
    def platform_version(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "platformVersion", value)

    @builtins.property
    @jsii.member(jsii_name="propagateTags")
    def propagate_tags(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.PropagateTags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-propagatetags
        """
        return jsii.get(self, "propagateTags")

    @propagate_tags.setter
    def propagate_tags(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "propagateTags", value)

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.Role``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-role
        """
        return jsii.get(self, "role")

    @role.setter
    def role(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "role", value)

    @builtins.property
    @jsii.member(jsii_name="schedulingStrategy")
    def scheduling_strategy(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.SchedulingStrategy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-schedulingstrategy
        """
        return jsii.get(self, "schedulingStrategy")

    @scheduling_strategy.setter
    def scheduling_strategy(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "schedulingStrategy", value)

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.ServiceName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-servicename
        """
        return jsii.get(self, "serviceName")

    @service_name.setter
    def service_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "serviceName", value)

    @builtins.property
    @jsii.member(jsii_name="serviceRegistries")
    def service_registries(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ServiceRegistryProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::ECS::Service.ServiceRegistries``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-serviceregistries
        """
        return jsii.get(self, "serviceRegistries")

    @service_registries.setter
    def service_registries(self, value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ServiceRegistryProperty", _IResolvable_9ceae33e]]]]) -> None:
        jsii.set(self, "serviceRegistries", value)

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.TaskDefinition``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-taskdefinition
        """
        return jsii.get(self, "taskDefinition")

    @task_definition.setter
    def task_definition(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "taskDefinition", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnService.AwsVpcConfigurationProperty", jsii_struct_bases=[], name_mapping={'subnets': 'subnets', 'assign_public_ip': 'assignPublicIp', 'security_groups': 'securityGroups'})
    class AwsVpcConfigurationProperty():
        def __init__(self, *, subnets: typing.List[str], assign_public_ip: typing.Optional[str]=None, security_groups: typing.Optional[typing.List[str]]=None) -> None:
            """
            :param subnets: ``CfnService.AwsVpcConfigurationProperty.Subnets``.
            :param assign_public_ip: ``CfnService.AwsVpcConfigurationProperty.AssignPublicIp``.
            :param security_groups: ``CfnService.AwsVpcConfigurationProperty.SecurityGroups``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-awsvpcconfiguration.html
            """
            self._values = {
                'subnets': subnets,
            }
            if assign_public_ip is not None: self._values["assign_public_ip"] = assign_public_ip
            if security_groups is not None: self._values["security_groups"] = security_groups

        @builtins.property
        def subnets(self) -> typing.List[str]:
            """``CfnService.AwsVpcConfigurationProperty.Subnets``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-awsvpcconfiguration.html#cfn-ecs-service-awsvpcconfiguration-subnets
            """
            return self._values.get('subnets')

        @builtins.property
        def assign_public_ip(self) -> typing.Optional[str]:
            """``CfnService.AwsVpcConfigurationProperty.AssignPublicIp``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-awsvpcconfiguration.html#cfn-ecs-service-awsvpcconfiguration-assignpublicip
            """
            return self._values.get('assign_public_ip')

        @builtins.property
        def security_groups(self) -> typing.Optional[typing.List[str]]:
            """``CfnService.AwsVpcConfigurationProperty.SecurityGroups``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-awsvpcconfiguration.html#cfn-ecs-service-awsvpcconfiguration-securitygroups
            """
            return self._values.get('security_groups')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AwsVpcConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnService.DeploymentConfigurationProperty", jsii_struct_bases=[], name_mapping={'maximum_percent': 'maximumPercent', 'minimum_healthy_percent': 'minimumHealthyPercent'})
    class DeploymentConfigurationProperty():
        def __init__(self, *, maximum_percent: typing.Optional[jsii.Number]=None, minimum_healthy_percent: typing.Optional[jsii.Number]=None) -> None:
            """
            :param maximum_percent: ``CfnService.DeploymentConfigurationProperty.MaximumPercent``.
            :param minimum_healthy_percent: ``CfnService.DeploymentConfigurationProperty.MinimumHealthyPercent``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-deploymentconfiguration.html
            """
            self._values = {
            }
            if maximum_percent is not None: self._values["maximum_percent"] = maximum_percent
            if minimum_healthy_percent is not None: self._values["minimum_healthy_percent"] = minimum_healthy_percent

        @builtins.property
        def maximum_percent(self) -> typing.Optional[jsii.Number]:
            """``CfnService.DeploymentConfigurationProperty.MaximumPercent``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-deploymentconfiguration.html#cfn-ecs-service-deploymentconfiguration-maximumpercent
            """
            return self._values.get('maximum_percent')

        @builtins.property
        def minimum_healthy_percent(self) -> typing.Optional[jsii.Number]:
            """``CfnService.DeploymentConfigurationProperty.MinimumHealthyPercent``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-deploymentconfiguration.html#cfn-ecs-service-deploymentconfiguration-minimumhealthypercent
            """
            return self._values.get('minimum_healthy_percent')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DeploymentConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnService.DeploymentControllerProperty", jsii_struct_bases=[], name_mapping={'type': 'type'})
    class DeploymentControllerProperty():
        def __init__(self, *, type: typing.Optional[str]=None) -> None:
            """
            :param type: ``CfnService.DeploymentControllerProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-deploymentcontroller.html
            """
            self._values = {
            }
            if type is not None: self._values["type"] = type

        @builtins.property
        def type(self) -> typing.Optional[str]:
            """``CfnService.DeploymentControllerProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-deploymentcontroller.html#cfn-ecs-service-deploymentcontroller-type
            """
            return self._values.get('type')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DeploymentControllerProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnService.LoadBalancerProperty", jsii_struct_bases=[], name_mapping={'container_port': 'containerPort', 'container_name': 'containerName', 'load_balancer_name': 'loadBalancerName', 'target_group_arn': 'targetGroupArn'})
    class LoadBalancerProperty():
        def __init__(self, *, container_port: jsii.Number, container_name: typing.Optional[str]=None, load_balancer_name: typing.Optional[str]=None, target_group_arn: typing.Optional[str]=None) -> None:
            """
            :param container_port: ``CfnService.LoadBalancerProperty.ContainerPort``.
            :param container_name: ``CfnService.LoadBalancerProperty.ContainerName``.
            :param load_balancer_name: ``CfnService.LoadBalancerProperty.LoadBalancerName``.
            :param target_group_arn: ``CfnService.LoadBalancerProperty.TargetGroupArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-loadbalancers.html
            """
            self._values = {
                'container_port': container_port,
            }
            if container_name is not None: self._values["container_name"] = container_name
            if load_balancer_name is not None: self._values["load_balancer_name"] = load_balancer_name
            if target_group_arn is not None: self._values["target_group_arn"] = target_group_arn

        @builtins.property
        def container_port(self) -> jsii.Number:
            """``CfnService.LoadBalancerProperty.ContainerPort``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-loadbalancers.html#cfn-ecs-service-loadbalancers-containerport
            """
            return self._values.get('container_port')

        @builtins.property
        def container_name(self) -> typing.Optional[str]:
            """``CfnService.LoadBalancerProperty.ContainerName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-loadbalancers.html#cfn-ecs-service-loadbalancers-containername
            """
            return self._values.get('container_name')

        @builtins.property
        def load_balancer_name(self) -> typing.Optional[str]:
            """``CfnService.LoadBalancerProperty.LoadBalancerName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-loadbalancers.html#cfn-ecs-service-loadbalancers-loadbalancername
            """
            return self._values.get('load_balancer_name')

        @builtins.property
        def target_group_arn(self) -> typing.Optional[str]:
            """``CfnService.LoadBalancerProperty.TargetGroupArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-loadbalancers.html#cfn-ecs-service-loadbalancers-targetgrouparn
            """
            return self._values.get('target_group_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LoadBalancerProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnService.NetworkConfigurationProperty", jsii_struct_bases=[], name_mapping={'awsvpc_configuration': 'awsvpcConfiguration'})
    class NetworkConfigurationProperty():
        def __init__(self, *, awsvpc_configuration: typing.Optional[typing.Union["CfnService.AwsVpcConfigurationProperty", _IResolvable_9ceae33e]]=None) -> None:
            """
            :param awsvpc_configuration: ``CfnService.NetworkConfigurationProperty.AwsvpcConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-networkconfiguration.html
            """
            self._values = {
            }
            if awsvpc_configuration is not None: self._values["awsvpc_configuration"] = awsvpc_configuration

        @builtins.property
        def awsvpc_configuration(self) -> typing.Optional[typing.Union["CfnService.AwsVpcConfigurationProperty", _IResolvable_9ceae33e]]:
            """``CfnService.NetworkConfigurationProperty.AwsvpcConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-networkconfiguration.html#cfn-ecs-service-networkconfiguration-awsvpcconfiguration
            """
            return self._values.get('awsvpc_configuration')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'NetworkConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnService.PlacementConstraintProperty", jsii_struct_bases=[], name_mapping={'type': 'type', 'expression': 'expression'})
    class PlacementConstraintProperty():
        def __init__(self, *, type: str, expression: typing.Optional[str]=None) -> None:
            """
            :param type: ``CfnService.PlacementConstraintProperty.Type``.
            :param expression: ``CfnService.PlacementConstraintProperty.Expression``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-placementconstraint.html
            """
            self._values = {
                'type': type,
            }
            if expression is not None: self._values["expression"] = expression

        @builtins.property
        def type(self) -> str:
            """``CfnService.PlacementConstraintProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-placementconstraint.html#cfn-ecs-service-placementconstraint-type
            """
            return self._values.get('type')

        @builtins.property
        def expression(self) -> typing.Optional[str]:
            """``CfnService.PlacementConstraintProperty.Expression``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-placementconstraint.html#cfn-ecs-service-placementconstraint-expression
            """
            return self._values.get('expression')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'PlacementConstraintProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnService.PlacementStrategyProperty", jsii_struct_bases=[], name_mapping={'type': 'type', 'field': 'field'})
    class PlacementStrategyProperty():
        def __init__(self, *, type: str, field: typing.Optional[str]=None) -> None:
            """
            :param type: ``CfnService.PlacementStrategyProperty.Type``.
            :param field: ``CfnService.PlacementStrategyProperty.Field``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-placementstrategy.html
            """
            self._values = {
                'type': type,
            }
            if field is not None: self._values["field"] = field

        @builtins.property
        def type(self) -> str:
            """``CfnService.PlacementStrategyProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-placementstrategy.html#cfn-ecs-service-placementstrategy-type
            """
            return self._values.get('type')

        @builtins.property
        def field(self) -> typing.Optional[str]:
            """``CfnService.PlacementStrategyProperty.Field``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-placementstrategy.html#cfn-ecs-service-placementstrategy-field
            """
            return self._values.get('field')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'PlacementStrategyProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnService.ServiceRegistryProperty", jsii_struct_bases=[], name_mapping={'container_name': 'containerName', 'container_port': 'containerPort', 'port': 'port', 'registry_arn': 'registryArn'})
    class ServiceRegistryProperty():
        def __init__(self, *, container_name: typing.Optional[str]=None, container_port: typing.Optional[jsii.Number]=None, port: typing.Optional[jsii.Number]=None, registry_arn: typing.Optional[str]=None) -> None:
            """
            :param container_name: ``CfnService.ServiceRegistryProperty.ContainerName``.
            :param container_port: ``CfnService.ServiceRegistryProperty.ContainerPort``.
            :param port: ``CfnService.ServiceRegistryProperty.Port``.
            :param registry_arn: ``CfnService.ServiceRegistryProperty.RegistryArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-serviceregistry.html
            """
            self._values = {
            }
            if container_name is not None: self._values["container_name"] = container_name
            if container_port is not None: self._values["container_port"] = container_port
            if port is not None: self._values["port"] = port
            if registry_arn is not None: self._values["registry_arn"] = registry_arn

        @builtins.property
        def container_name(self) -> typing.Optional[str]:
            """``CfnService.ServiceRegistryProperty.ContainerName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-serviceregistry.html#cfn-ecs-service-serviceregistry-containername
            """
            return self._values.get('container_name')

        @builtins.property
        def container_port(self) -> typing.Optional[jsii.Number]:
            """``CfnService.ServiceRegistryProperty.ContainerPort``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-serviceregistry.html#cfn-ecs-service-serviceregistry-containerport
            """
            return self._values.get('container_port')

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            """``CfnService.ServiceRegistryProperty.Port``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-serviceregistry.html#cfn-ecs-service-serviceregistry-port
            """
            return self._values.get('port')

        @builtins.property
        def registry_arn(self) -> typing.Optional[str]:
            """``CfnService.ServiceRegistryProperty.RegistryArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-serviceregistry.html#cfn-ecs-service-serviceregistry-registryarn
            """
            return self._values.get('registry_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ServiceRegistryProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnServiceProps", jsii_struct_bases=[], name_mapping={'cluster': 'cluster', 'deployment_configuration': 'deploymentConfiguration', 'deployment_controller': 'deploymentController', 'desired_count': 'desiredCount', 'enable_ecs_managed_tags': 'enableEcsManagedTags', 'health_check_grace_period_seconds': 'healthCheckGracePeriodSeconds', 'launch_type': 'launchType', 'load_balancers': 'loadBalancers', 'network_configuration': 'networkConfiguration', 'placement_constraints': 'placementConstraints', 'placement_strategies': 'placementStrategies', 'platform_version': 'platformVersion', 'propagate_tags': 'propagateTags', 'role': 'role', 'scheduling_strategy': 'schedulingStrategy', 'service_name': 'serviceName', 'service_registries': 'serviceRegistries', 'tags': 'tags', 'task_definition': 'taskDefinition'})
class CfnServiceProps():
    def __init__(self, *, cluster: typing.Optional[str]=None, deployment_configuration: typing.Optional[typing.Union["CfnService.DeploymentConfigurationProperty", _IResolvable_9ceae33e]]=None, deployment_controller: typing.Optional[typing.Union["CfnService.DeploymentControllerProperty", _IResolvable_9ceae33e]]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, health_check_grace_period_seconds: typing.Optional[jsii.Number]=None, launch_type: typing.Optional[str]=None, load_balancers: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnService.LoadBalancerProperty", _IResolvable_9ceae33e]]]]=None, network_configuration: typing.Optional[typing.Union["CfnService.NetworkConfigurationProperty", _IResolvable_9ceae33e]]=None, placement_constraints: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnService.PlacementConstraintProperty", _IResolvable_9ceae33e]]]]=None, placement_strategies: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnService.PlacementStrategyProperty", _IResolvable_9ceae33e]]]]=None, platform_version: typing.Optional[str]=None, propagate_tags: typing.Optional[str]=None, role: typing.Optional[str]=None, scheduling_strategy: typing.Optional[str]=None, service_name: typing.Optional[str]=None, service_registries: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnService.ServiceRegistryProperty", _IResolvable_9ceae33e]]]]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None, task_definition: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::ECS::Service``.

        :param cluster: ``AWS::ECS::Service.Cluster``.
        :param deployment_configuration: ``AWS::ECS::Service.DeploymentConfiguration``.
        :param deployment_controller: ``AWS::ECS::Service.DeploymentController``.
        :param desired_count: ``AWS::ECS::Service.DesiredCount``.
        :param enable_ecs_managed_tags: ``AWS::ECS::Service.EnableECSManagedTags``.
        :param health_check_grace_period_seconds: ``AWS::ECS::Service.HealthCheckGracePeriodSeconds``.
        :param launch_type: ``AWS::ECS::Service.LaunchType``.
        :param load_balancers: ``AWS::ECS::Service.LoadBalancers``.
        :param network_configuration: ``AWS::ECS::Service.NetworkConfiguration``.
        :param placement_constraints: ``AWS::ECS::Service.PlacementConstraints``.
        :param placement_strategies: ``AWS::ECS::Service.PlacementStrategies``.
        :param platform_version: ``AWS::ECS::Service.PlatformVersion``.
        :param propagate_tags: ``AWS::ECS::Service.PropagateTags``.
        :param role: ``AWS::ECS::Service.Role``.
        :param scheduling_strategy: ``AWS::ECS::Service.SchedulingStrategy``.
        :param service_name: ``AWS::ECS::Service.ServiceName``.
        :param service_registries: ``AWS::ECS::Service.ServiceRegistries``.
        :param tags: ``AWS::ECS::Service.Tags``.
        :param task_definition: ``AWS::ECS::Service.TaskDefinition``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html
        """
        self._values = {
        }
        if cluster is not None: self._values["cluster"] = cluster
        if deployment_configuration is not None: self._values["deployment_configuration"] = deployment_configuration
        if deployment_controller is not None: self._values["deployment_controller"] = deployment_controller
        if desired_count is not None: self._values["desired_count"] = desired_count
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period_seconds is not None: self._values["health_check_grace_period_seconds"] = health_check_grace_period_seconds
        if launch_type is not None: self._values["launch_type"] = launch_type
        if load_balancers is not None: self._values["load_balancers"] = load_balancers
        if network_configuration is not None: self._values["network_configuration"] = network_configuration
        if placement_constraints is not None: self._values["placement_constraints"] = placement_constraints
        if placement_strategies is not None: self._values["placement_strategies"] = placement_strategies
        if platform_version is not None: self._values["platform_version"] = platform_version
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if role is not None: self._values["role"] = role
        if scheduling_strategy is not None: self._values["scheduling_strategy"] = scheduling_strategy
        if service_name is not None: self._values["service_name"] = service_name
        if service_registries is not None: self._values["service_registries"] = service_registries
        if tags is not None: self._values["tags"] = tags
        if task_definition is not None: self._values["task_definition"] = task_definition

    @builtins.property
    def cluster(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.Cluster``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-cluster
        """
        return self._values.get('cluster')

    @builtins.property
    def deployment_configuration(self) -> typing.Optional[typing.Union["CfnService.DeploymentConfigurationProperty", _IResolvable_9ceae33e]]:
        """``AWS::ECS::Service.DeploymentConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-deploymentconfiguration
        """
        return self._values.get('deployment_configuration')

    @builtins.property
    def deployment_controller(self) -> typing.Optional[typing.Union["CfnService.DeploymentControllerProperty", _IResolvable_9ceae33e]]:
        """``AWS::ECS::Service.DeploymentController``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-deploymentcontroller
        """
        return self._values.get('deployment_controller')

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """``AWS::ECS::Service.DesiredCount``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-desiredcount
        """
        return self._values.get('desired_count')

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::ECS::Service.EnableECSManagedTags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-enableecsmanagedtags
        """
        return self._values.get('enable_ecs_managed_tags')

    @builtins.property
    def health_check_grace_period_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::ECS::Service.HealthCheckGracePeriodSeconds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-healthcheckgraceperiodseconds
        """
        return self._values.get('health_check_grace_period_seconds')

    @builtins.property
    def launch_type(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.LaunchType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-launchtype
        """
        return self._values.get('launch_type')

    @builtins.property
    def load_balancers(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnService.LoadBalancerProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::ECS::Service.LoadBalancers``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-loadbalancers
        """
        return self._values.get('load_balancers')

    @builtins.property
    def network_configuration(self) -> typing.Optional[typing.Union["CfnService.NetworkConfigurationProperty", _IResolvable_9ceae33e]]:
        """``AWS::ECS::Service.NetworkConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-networkconfiguration
        """
        return self._values.get('network_configuration')

    @builtins.property
    def placement_constraints(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnService.PlacementConstraintProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::ECS::Service.PlacementConstraints``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-placementconstraints
        """
        return self._values.get('placement_constraints')

    @builtins.property
    def placement_strategies(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnService.PlacementStrategyProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::ECS::Service.PlacementStrategies``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-placementstrategies
        """
        return self._values.get('placement_strategies')

    @builtins.property
    def platform_version(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.PlatformVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-platformversion
        """
        return self._values.get('platform_version')

    @builtins.property
    def propagate_tags(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.PropagateTags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-propagatetags
        """
        return self._values.get('propagate_tags')

    @builtins.property
    def role(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.Role``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-role
        """
        return self._values.get('role')

    @builtins.property
    def scheduling_strategy(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.SchedulingStrategy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-schedulingstrategy
        """
        return self._values.get('scheduling_strategy')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.ServiceName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-servicename
        """
        return self._values.get('service_name')

    @builtins.property
    def service_registries(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnService.ServiceRegistryProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::ECS::Service.ServiceRegistries``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-serviceregistries
        """
        return self._values.get('service_registries')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::ECS::Service.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-tags
        """
        return self._values.get('tags')

    @builtins.property
    def task_definition(self) -> typing.Optional[str]:
        """``AWS::ECS::Service.TaskDefinition``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-taskdefinition
        """
        return self._values.get('task_definition')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnTaskDefinition(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs.CfnTaskDefinition"):
    """A CloudFormation ``AWS::ECS::TaskDefinition``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html
    cloudformationResource:
    :cloudformationResource:: AWS::ECS::TaskDefinition
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, container_definitions: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ContainerDefinitionProperty", _IResolvable_9ceae33e]]]]=None, cpu: typing.Optional[str]=None, execution_role_arn: typing.Optional[str]=None, family: typing.Optional[str]=None, inference_accelerators: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["InferenceAcceleratorProperty", _IResolvable_9ceae33e]]]]=None, ipc_mode: typing.Optional[str]=None, memory: typing.Optional[str]=None, network_mode: typing.Optional[str]=None, pid_mode: typing.Optional[str]=None, placement_constraints: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["TaskDefinitionPlacementConstraintProperty", _IResolvable_9ceae33e]]]]=None, proxy_configuration: typing.Optional[typing.Union["ProxyConfigurationProperty", _IResolvable_9ceae33e]]=None, requires_compatibilities: typing.Optional[typing.List[str]]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None, task_role_arn: typing.Optional[str]=None, volumes: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["VolumeProperty", _IResolvable_9ceae33e]]]]=None) -> None:
        """Create a new ``AWS::ECS::TaskDefinition``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param container_definitions: ``AWS::ECS::TaskDefinition.ContainerDefinitions``.
        :param cpu: ``AWS::ECS::TaskDefinition.Cpu``.
        :param execution_role_arn: ``AWS::ECS::TaskDefinition.ExecutionRoleArn``.
        :param family: ``AWS::ECS::TaskDefinition.Family``.
        :param inference_accelerators: ``AWS::ECS::TaskDefinition.InferenceAccelerators``.
        :param ipc_mode: ``AWS::ECS::TaskDefinition.IpcMode``.
        :param memory: ``AWS::ECS::TaskDefinition.Memory``.
        :param network_mode: ``AWS::ECS::TaskDefinition.NetworkMode``.
        :param pid_mode: ``AWS::ECS::TaskDefinition.PidMode``.
        :param placement_constraints: ``AWS::ECS::TaskDefinition.PlacementConstraints``.
        :param proxy_configuration: ``AWS::ECS::TaskDefinition.ProxyConfiguration``.
        :param requires_compatibilities: ``AWS::ECS::TaskDefinition.RequiresCompatibilities``.
        :param tags: ``AWS::ECS::TaskDefinition.Tags``.
        :param task_role_arn: ``AWS::ECS::TaskDefinition.TaskRoleArn``.
        :param volumes: ``AWS::ECS::TaskDefinition.Volumes``.
        """
        props = CfnTaskDefinitionProps(container_definitions=container_definitions, cpu=cpu, execution_role_arn=execution_role_arn, family=family, inference_accelerators=inference_accelerators, ipc_mode=ipc_mode, memory=memory, network_mode=network_mode, pid_mode=pid_mode, placement_constraints=placement_constraints, proxy_configuration=proxy_configuration, requires_compatibilities=requires_compatibilities, tags=tags, task_role_arn=task_role_arn, volumes=volumes)

        jsii.create(CfnTaskDefinition, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnTaskDefinition":
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
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::ECS::TaskDefinition.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="containerDefinitions")
    def container_definitions(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ContainerDefinitionProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::ECS::TaskDefinition.ContainerDefinitions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-containerdefinitions
        """
        return jsii.get(self, "containerDefinitions")

    @container_definitions.setter
    def container_definitions(self, value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ContainerDefinitionProperty", _IResolvable_9ceae33e]]]]) -> None:
        jsii.set(self, "containerDefinitions", value)

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.Cpu``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-cpu
        """
        return jsii.get(self, "cpu")

    @cpu.setter
    def cpu(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "cpu", value)

    @builtins.property
    @jsii.member(jsii_name="executionRoleArn")
    def execution_role_arn(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.ExecutionRoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-executionrolearn
        """
        return jsii.get(self, "executionRoleArn")

    @execution_role_arn.setter
    def execution_role_arn(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "executionRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="family")
    def family(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.Family``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-family
        """
        return jsii.get(self, "family")

    @family.setter
    def family(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "family", value)

    @builtins.property
    @jsii.member(jsii_name="inferenceAccelerators")
    def inference_accelerators(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["InferenceAcceleratorProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::ECS::TaskDefinition.InferenceAccelerators``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-inferenceaccelerators
        """
        return jsii.get(self, "inferenceAccelerators")

    @inference_accelerators.setter
    def inference_accelerators(self, value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["InferenceAcceleratorProperty", _IResolvable_9ceae33e]]]]) -> None:
        jsii.set(self, "inferenceAccelerators", value)

    @builtins.property
    @jsii.member(jsii_name="ipcMode")
    def ipc_mode(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.IpcMode``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-ipcmode
        """
        return jsii.get(self, "ipcMode")

    @ipc_mode.setter
    def ipc_mode(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "ipcMode", value)

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.Memory``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-memory
        """
        return jsii.get(self, "memory")

    @memory.setter
    def memory(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "memory", value)

    @builtins.property
    @jsii.member(jsii_name="networkMode")
    def network_mode(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.NetworkMode``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-networkmode
        """
        return jsii.get(self, "networkMode")

    @network_mode.setter
    def network_mode(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "networkMode", value)

    @builtins.property
    @jsii.member(jsii_name="pidMode")
    def pid_mode(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.PidMode``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-pidmode
        """
        return jsii.get(self, "pidMode")

    @pid_mode.setter
    def pid_mode(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "pidMode", value)

    @builtins.property
    @jsii.member(jsii_name="placementConstraints")
    def placement_constraints(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["TaskDefinitionPlacementConstraintProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::ECS::TaskDefinition.PlacementConstraints``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-placementconstraints
        """
        return jsii.get(self, "placementConstraints")

    @placement_constraints.setter
    def placement_constraints(self, value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["TaskDefinitionPlacementConstraintProperty", _IResolvable_9ceae33e]]]]) -> None:
        jsii.set(self, "placementConstraints", value)

    @builtins.property
    @jsii.member(jsii_name="proxyConfiguration")
    def proxy_configuration(self) -> typing.Optional[typing.Union["ProxyConfigurationProperty", _IResolvable_9ceae33e]]:
        """``AWS::ECS::TaskDefinition.ProxyConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-proxyconfiguration
        """
        return jsii.get(self, "proxyConfiguration")

    @proxy_configuration.setter
    def proxy_configuration(self, value: typing.Optional[typing.Union["ProxyConfigurationProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "proxyConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="requiresCompatibilities")
    def requires_compatibilities(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ECS::TaskDefinition.RequiresCompatibilities``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-requirescompatibilities
        """
        return jsii.get(self, "requiresCompatibilities")

    @requires_compatibilities.setter
    def requires_compatibilities(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "requiresCompatibilities", value)

    @builtins.property
    @jsii.member(jsii_name="taskRoleArn")
    def task_role_arn(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.TaskRoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-taskrolearn
        """
        return jsii.get(self, "taskRoleArn")

    @task_role_arn.setter
    def task_role_arn(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "taskRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="volumes")
    def volumes(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["VolumeProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::ECS::TaskDefinition.Volumes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-volumes
        """
        return jsii.get(self, "volumes")

    @volumes.setter
    def volumes(self, value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["VolumeProperty", _IResolvable_9ceae33e]]]]) -> None:
        jsii.set(self, "volumes", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnTaskDefinition.ContainerDefinitionProperty", jsii_struct_bases=[], name_mapping={'command': 'command', 'cpu': 'cpu', 'depends_on': 'dependsOn', 'disable_networking': 'disableNetworking', 'dns_search_domains': 'dnsSearchDomains', 'dns_servers': 'dnsServers', 'docker_labels': 'dockerLabels', 'docker_security_options': 'dockerSecurityOptions', 'entry_point': 'entryPoint', 'environment': 'environment', 'essential': 'essential', 'extra_hosts': 'extraHosts', 'firelens_configuration': 'firelensConfiguration', 'health_check': 'healthCheck', 'hostname': 'hostname', 'image': 'image', 'interactive': 'interactive', 'links': 'links', 'linux_parameters': 'linuxParameters', 'log_configuration': 'logConfiguration', 'memory': 'memory', 'memory_reservation': 'memoryReservation', 'mount_points': 'mountPoints', 'name': 'name', 'port_mappings': 'portMappings', 'privileged': 'privileged', 'pseudo_terminal': 'pseudoTerminal', 'readonly_root_filesystem': 'readonlyRootFilesystem', 'repository_credentials': 'repositoryCredentials', 'resource_requirements': 'resourceRequirements', 'secrets': 'secrets', 'start_timeout': 'startTimeout', 'stop_timeout': 'stopTimeout', 'system_controls': 'systemControls', 'ulimits': 'ulimits', 'user': 'user', 'volumes_from': 'volumesFrom', 'working_directory': 'workingDirectory'})
    class ContainerDefinitionProperty():
        def __init__(self, *, command: typing.Optional[typing.List[str]]=None, cpu: typing.Optional[jsii.Number]=None, depends_on: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskDefinition.ContainerDependencyProperty", _IResolvable_9ceae33e]]]]=None, disable_networking: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, dns_search_domains: typing.Optional[typing.List[str]]=None, dns_servers: typing.Optional[typing.List[str]]=None, docker_labels: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[str, str]]]=None, docker_security_options: typing.Optional[typing.List[str]]=None, entry_point: typing.Optional[typing.List[str]]=None, environment: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskDefinition.KeyValuePairProperty", _IResolvable_9ceae33e]]]]=None, essential: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, extra_hosts: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskDefinition.HostEntryProperty", _IResolvable_9ceae33e]]]]=None, firelens_configuration: typing.Optional[typing.Union["CfnTaskDefinition.FirelensConfigurationProperty", _IResolvable_9ceae33e]]=None, health_check: typing.Optional[typing.Union["CfnTaskDefinition.HealthCheckProperty", _IResolvable_9ceae33e]]=None, hostname: typing.Optional[str]=None, image: typing.Optional[str]=None, interactive: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, links: typing.Optional[typing.List[str]]=None, linux_parameters: typing.Optional[typing.Union["CfnTaskDefinition.LinuxParametersProperty", _IResolvable_9ceae33e]]=None, log_configuration: typing.Optional[typing.Union["CfnTaskDefinition.LogConfigurationProperty", _IResolvable_9ceae33e]]=None, memory: typing.Optional[jsii.Number]=None, memory_reservation: typing.Optional[jsii.Number]=None, mount_points: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskDefinition.MountPointProperty", _IResolvable_9ceae33e]]]]=None, name: typing.Optional[str]=None, port_mappings: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskDefinition.PortMappingProperty", _IResolvable_9ceae33e]]]]=None, privileged: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, pseudo_terminal: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, readonly_root_filesystem: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, repository_credentials: typing.Optional[typing.Union["CfnTaskDefinition.RepositoryCredentialsProperty", _IResolvable_9ceae33e]]=None, resource_requirements: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskDefinition.ResourceRequirementProperty", _IResolvable_9ceae33e]]]]=None, secrets: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskDefinition.SecretProperty", _IResolvable_9ceae33e]]]]=None, start_timeout: typing.Optional[jsii.Number]=None, stop_timeout: typing.Optional[jsii.Number]=None, system_controls: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskDefinition.SystemControlProperty", _IResolvable_9ceae33e]]]]=None, ulimits: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskDefinition.UlimitProperty", _IResolvable_9ceae33e]]]]=None, user: typing.Optional[str]=None, volumes_from: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskDefinition.VolumeFromProperty", _IResolvable_9ceae33e]]]]=None, working_directory: typing.Optional[str]=None) -> None:
            """
            :param command: ``CfnTaskDefinition.ContainerDefinitionProperty.Command``.
            :param cpu: ``CfnTaskDefinition.ContainerDefinitionProperty.Cpu``.
            :param depends_on: ``CfnTaskDefinition.ContainerDefinitionProperty.DependsOn``.
            :param disable_networking: ``CfnTaskDefinition.ContainerDefinitionProperty.DisableNetworking``.
            :param dns_search_domains: ``CfnTaskDefinition.ContainerDefinitionProperty.DnsSearchDomains``.
            :param dns_servers: ``CfnTaskDefinition.ContainerDefinitionProperty.DnsServers``.
            :param docker_labels: ``CfnTaskDefinition.ContainerDefinitionProperty.DockerLabels``.
            :param docker_security_options: ``CfnTaskDefinition.ContainerDefinitionProperty.DockerSecurityOptions``.
            :param entry_point: ``CfnTaskDefinition.ContainerDefinitionProperty.EntryPoint``.
            :param environment: ``CfnTaskDefinition.ContainerDefinitionProperty.Environment``.
            :param essential: ``CfnTaskDefinition.ContainerDefinitionProperty.Essential``.
            :param extra_hosts: ``CfnTaskDefinition.ContainerDefinitionProperty.ExtraHosts``.
            :param firelens_configuration: ``CfnTaskDefinition.ContainerDefinitionProperty.FirelensConfiguration``.
            :param health_check: ``CfnTaskDefinition.ContainerDefinitionProperty.HealthCheck``.
            :param hostname: ``CfnTaskDefinition.ContainerDefinitionProperty.Hostname``.
            :param image: ``CfnTaskDefinition.ContainerDefinitionProperty.Image``.
            :param interactive: ``CfnTaskDefinition.ContainerDefinitionProperty.Interactive``.
            :param links: ``CfnTaskDefinition.ContainerDefinitionProperty.Links``.
            :param linux_parameters: ``CfnTaskDefinition.ContainerDefinitionProperty.LinuxParameters``.
            :param log_configuration: ``CfnTaskDefinition.ContainerDefinitionProperty.LogConfiguration``.
            :param memory: ``CfnTaskDefinition.ContainerDefinitionProperty.Memory``.
            :param memory_reservation: ``CfnTaskDefinition.ContainerDefinitionProperty.MemoryReservation``.
            :param mount_points: ``CfnTaskDefinition.ContainerDefinitionProperty.MountPoints``.
            :param name: ``CfnTaskDefinition.ContainerDefinitionProperty.Name``.
            :param port_mappings: ``CfnTaskDefinition.ContainerDefinitionProperty.PortMappings``.
            :param privileged: ``CfnTaskDefinition.ContainerDefinitionProperty.Privileged``.
            :param pseudo_terminal: ``CfnTaskDefinition.ContainerDefinitionProperty.PseudoTerminal``.
            :param readonly_root_filesystem: ``CfnTaskDefinition.ContainerDefinitionProperty.ReadonlyRootFilesystem``.
            :param repository_credentials: ``CfnTaskDefinition.ContainerDefinitionProperty.RepositoryCredentials``.
            :param resource_requirements: ``CfnTaskDefinition.ContainerDefinitionProperty.ResourceRequirements``.
            :param secrets: ``CfnTaskDefinition.ContainerDefinitionProperty.Secrets``.
            :param start_timeout: ``CfnTaskDefinition.ContainerDefinitionProperty.StartTimeout``.
            :param stop_timeout: ``CfnTaskDefinition.ContainerDefinitionProperty.StopTimeout``.
            :param system_controls: ``CfnTaskDefinition.ContainerDefinitionProperty.SystemControls``.
            :param ulimits: ``CfnTaskDefinition.ContainerDefinitionProperty.Ulimits``.
            :param user: ``CfnTaskDefinition.ContainerDefinitionProperty.User``.
            :param volumes_from: ``CfnTaskDefinition.ContainerDefinitionProperty.VolumesFrom``.
            :param working_directory: ``CfnTaskDefinition.ContainerDefinitionProperty.WorkingDirectory``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html
            """
            self._values = {
            }
            if command is not None: self._values["command"] = command
            if cpu is not None: self._values["cpu"] = cpu
            if depends_on is not None: self._values["depends_on"] = depends_on
            if disable_networking is not None: self._values["disable_networking"] = disable_networking
            if dns_search_domains is not None: self._values["dns_search_domains"] = dns_search_domains
            if dns_servers is not None: self._values["dns_servers"] = dns_servers
            if docker_labels is not None: self._values["docker_labels"] = docker_labels
            if docker_security_options is not None: self._values["docker_security_options"] = docker_security_options
            if entry_point is not None: self._values["entry_point"] = entry_point
            if environment is not None: self._values["environment"] = environment
            if essential is not None: self._values["essential"] = essential
            if extra_hosts is not None: self._values["extra_hosts"] = extra_hosts
            if firelens_configuration is not None: self._values["firelens_configuration"] = firelens_configuration
            if health_check is not None: self._values["health_check"] = health_check
            if hostname is not None: self._values["hostname"] = hostname
            if image is not None: self._values["image"] = image
            if interactive is not None: self._values["interactive"] = interactive
            if links is not None: self._values["links"] = links
            if linux_parameters is not None: self._values["linux_parameters"] = linux_parameters
            if log_configuration is not None: self._values["log_configuration"] = log_configuration
            if memory is not None: self._values["memory"] = memory
            if memory_reservation is not None: self._values["memory_reservation"] = memory_reservation
            if mount_points is not None: self._values["mount_points"] = mount_points
            if name is not None: self._values["name"] = name
            if port_mappings is not None: self._values["port_mappings"] = port_mappings
            if privileged is not None: self._values["privileged"] = privileged
            if pseudo_terminal is not None: self._values["pseudo_terminal"] = pseudo_terminal
            if readonly_root_filesystem is not None: self._values["readonly_root_filesystem"] = readonly_root_filesystem
            if repository_credentials is not None: self._values["repository_credentials"] = repository_credentials
            if resource_requirements is not None: self._values["resource_requirements"] = resource_requirements
            if secrets is not None: self._values["secrets"] = secrets
            if start_timeout is not None: self._values["start_timeout"] = start_timeout
            if stop_timeout is not None: self._values["stop_timeout"] = stop_timeout
            if system_controls is not None: self._values["system_controls"] = system_controls
            if ulimits is not None: self._values["ulimits"] = ulimits
            if user is not None: self._values["user"] = user
            if volumes_from is not None: self._values["volumes_from"] = volumes_from
            if working_directory is not None: self._values["working_directory"] = working_directory

        @builtins.property
        def command(self) -> typing.Optional[typing.List[str]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.Command``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-command
            """
            return self._values.get('command')

        @builtins.property
        def cpu(self) -> typing.Optional[jsii.Number]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.Cpu``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-cpu
            """
            return self._values.get('cpu')

        @builtins.property
        def depends_on(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskDefinition.ContainerDependencyProperty", _IResolvable_9ceae33e]]]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.DependsOn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-dependson
            """
            return self._values.get('depends_on')

        @builtins.property
        def disable_networking(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.DisableNetworking``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-disablenetworking
            """
            return self._values.get('disable_networking')

        @builtins.property
        def dns_search_domains(self) -> typing.Optional[typing.List[str]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.DnsSearchDomains``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-dnssearchdomains
            """
            return self._values.get('dns_search_domains')

        @builtins.property
        def dns_servers(self) -> typing.Optional[typing.List[str]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.DnsServers``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-dnsservers
            """
            return self._values.get('dns_servers')

        @builtins.property
        def docker_labels(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[str, str]]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.DockerLabels``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-dockerlabels
            """
            return self._values.get('docker_labels')

        @builtins.property
        def docker_security_options(self) -> typing.Optional[typing.List[str]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.DockerSecurityOptions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-dockersecurityoptions
            """
            return self._values.get('docker_security_options')

        @builtins.property
        def entry_point(self) -> typing.Optional[typing.List[str]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.EntryPoint``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-entrypoint
            """
            return self._values.get('entry_point')

        @builtins.property
        def environment(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskDefinition.KeyValuePairProperty", _IResolvable_9ceae33e]]]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.Environment``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-environment
            """
            return self._values.get('environment')

        @builtins.property
        def essential(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.Essential``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-essential
            """
            return self._values.get('essential')

        @builtins.property
        def extra_hosts(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskDefinition.HostEntryProperty", _IResolvable_9ceae33e]]]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.ExtraHosts``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-extrahosts
            """
            return self._values.get('extra_hosts')

        @builtins.property
        def firelens_configuration(self) -> typing.Optional[typing.Union["CfnTaskDefinition.FirelensConfigurationProperty", _IResolvable_9ceae33e]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.FirelensConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-firelensconfiguration
            """
            return self._values.get('firelens_configuration')

        @builtins.property
        def health_check(self) -> typing.Optional[typing.Union["CfnTaskDefinition.HealthCheckProperty", _IResolvable_9ceae33e]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.HealthCheck``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-healthcheck
            """
            return self._values.get('health_check')

        @builtins.property
        def hostname(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.Hostname``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-hostname
            """
            return self._values.get('hostname')

        @builtins.property
        def image(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.Image``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-image
            """
            return self._values.get('image')

        @builtins.property
        def interactive(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.Interactive``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-interactive
            """
            return self._values.get('interactive')

        @builtins.property
        def links(self) -> typing.Optional[typing.List[str]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.Links``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-links
            """
            return self._values.get('links')

        @builtins.property
        def linux_parameters(self) -> typing.Optional[typing.Union["CfnTaskDefinition.LinuxParametersProperty", _IResolvable_9ceae33e]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.LinuxParameters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-linuxparameters
            """
            return self._values.get('linux_parameters')

        @builtins.property
        def log_configuration(self) -> typing.Optional[typing.Union["CfnTaskDefinition.LogConfigurationProperty", _IResolvable_9ceae33e]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.LogConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-logconfiguration
            """
            return self._values.get('log_configuration')

        @builtins.property
        def memory(self) -> typing.Optional[jsii.Number]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.Memory``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-memory
            """
            return self._values.get('memory')

        @builtins.property
        def memory_reservation(self) -> typing.Optional[jsii.Number]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.MemoryReservation``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-memoryreservation
            """
            return self._values.get('memory_reservation')

        @builtins.property
        def mount_points(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskDefinition.MountPointProperty", _IResolvable_9ceae33e]]]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.MountPoints``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-mountpoints
            """
            return self._values.get('mount_points')

        @builtins.property
        def name(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-name
            """
            return self._values.get('name')

        @builtins.property
        def port_mappings(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskDefinition.PortMappingProperty", _IResolvable_9ceae33e]]]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.PortMappings``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-portmappings
            """
            return self._values.get('port_mappings')

        @builtins.property
        def privileged(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.Privileged``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-privileged
            """
            return self._values.get('privileged')

        @builtins.property
        def pseudo_terminal(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.PseudoTerminal``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-pseudoterminal
            """
            return self._values.get('pseudo_terminal')

        @builtins.property
        def readonly_root_filesystem(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.ReadonlyRootFilesystem``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-readonlyrootfilesystem
            """
            return self._values.get('readonly_root_filesystem')

        @builtins.property
        def repository_credentials(self) -> typing.Optional[typing.Union["CfnTaskDefinition.RepositoryCredentialsProperty", _IResolvable_9ceae33e]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.RepositoryCredentials``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-repositorycredentials
            """
            return self._values.get('repository_credentials')

        @builtins.property
        def resource_requirements(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskDefinition.ResourceRequirementProperty", _IResolvable_9ceae33e]]]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.ResourceRequirements``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-resourcerequirements
            """
            return self._values.get('resource_requirements')

        @builtins.property
        def secrets(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskDefinition.SecretProperty", _IResolvable_9ceae33e]]]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.Secrets``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-secrets
            """
            return self._values.get('secrets')

        @builtins.property
        def start_timeout(self) -> typing.Optional[jsii.Number]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.StartTimeout``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-starttimeout
            """
            return self._values.get('start_timeout')

        @builtins.property
        def stop_timeout(self) -> typing.Optional[jsii.Number]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.StopTimeout``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-stoptimeout
            """
            return self._values.get('stop_timeout')

        @builtins.property
        def system_controls(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskDefinition.SystemControlProperty", _IResolvable_9ceae33e]]]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.SystemControls``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-systemcontrols
            """
            return self._values.get('system_controls')

        @builtins.property
        def ulimits(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskDefinition.UlimitProperty", _IResolvable_9ceae33e]]]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.Ulimits``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-ulimits
            """
            return self._values.get('ulimits')

        @builtins.property
        def user(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.User``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-user
            """
            return self._values.get('user')

        @builtins.property
        def volumes_from(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskDefinition.VolumeFromProperty", _IResolvable_9ceae33e]]]]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.VolumesFrom``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-volumesfrom
            """
            return self._values.get('volumes_from')

        @builtins.property
        def working_directory(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.ContainerDefinitionProperty.WorkingDirectory``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-workingdirectory
            """
            return self._values.get('working_directory')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ContainerDefinitionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnTaskDefinition.ContainerDependencyProperty", jsii_struct_bases=[], name_mapping={'condition': 'condition', 'container_name': 'containerName'})
    class ContainerDependencyProperty():
        def __init__(self, *, condition: str, container_name: str) -> None:
            """
            :param condition: ``CfnTaskDefinition.ContainerDependencyProperty.Condition``.
            :param container_name: ``CfnTaskDefinition.ContainerDependencyProperty.ContainerName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdependency.html
            """
            self._values = {
                'condition': condition,
                'container_name': container_name,
            }

        @builtins.property
        def condition(self) -> str:
            """``CfnTaskDefinition.ContainerDependencyProperty.Condition``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdependency.html#cfn-ecs-taskdefinition-containerdependency-condition
            """
            return self._values.get('condition')

        @builtins.property
        def container_name(self) -> str:
            """``CfnTaskDefinition.ContainerDependencyProperty.ContainerName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdependency.html#cfn-ecs-taskdefinition-containerdependency-containername
            """
            return self._values.get('container_name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ContainerDependencyProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnTaskDefinition.DeviceProperty", jsii_struct_bases=[], name_mapping={'host_path': 'hostPath', 'container_path': 'containerPath', 'permissions': 'permissions'})
    class DeviceProperty():
        def __init__(self, *, host_path: str, container_path: typing.Optional[str]=None, permissions: typing.Optional[typing.List[str]]=None) -> None:
            """
            :param host_path: ``CfnTaskDefinition.DeviceProperty.HostPath``.
            :param container_path: ``CfnTaskDefinition.DeviceProperty.ContainerPath``.
            :param permissions: ``CfnTaskDefinition.DeviceProperty.Permissions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-device.html
            """
            self._values = {
                'host_path': host_path,
            }
            if container_path is not None: self._values["container_path"] = container_path
            if permissions is not None: self._values["permissions"] = permissions

        @builtins.property
        def host_path(self) -> str:
            """``CfnTaskDefinition.DeviceProperty.HostPath``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-device.html#cfn-ecs-taskdefinition-device-hostpath
            """
            return self._values.get('host_path')

        @builtins.property
        def container_path(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.DeviceProperty.ContainerPath``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-device.html#cfn-ecs-taskdefinition-device-containerpath
            """
            return self._values.get('container_path')

        @builtins.property
        def permissions(self) -> typing.Optional[typing.List[str]]:
            """``CfnTaskDefinition.DeviceProperty.Permissions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-device.html#cfn-ecs-taskdefinition-device-permissions
            """
            return self._values.get('permissions')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DeviceProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnTaskDefinition.DockerVolumeConfigurationProperty", jsii_struct_bases=[], name_mapping={'autoprovision': 'autoprovision', 'driver': 'driver', 'driver_opts': 'driverOpts', 'labels': 'labels', 'scope': 'scope'})
    class DockerVolumeConfigurationProperty():
        def __init__(self, *, autoprovision: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, driver: typing.Optional[str]=None, driver_opts: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[str, str]]]=None, labels: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[str, str]]]=None, scope: typing.Optional[str]=None) -> None:
            """
            :param autoprovision: ``CfnTaskDefinition.DockerVolumeConfigurationProperty.Autoprovision``.
            :param driver: ``CfnTaskDefinition.DockerVolumeConfigurationProperty.Driver``.
            :param driver_opts: ``CfnTaskDefinition.DockerVolumeConfigurationProperty.DriverOpts``.
            :param labels: ``CfnTaskDefinition.DockerVolumeConfigurationProperty.Labels``.
            :param scope: ``CfnTaskDefinition.DockerVolumeConfigurationProperty.Scope``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-dockervolumeconfiguration.html
            """
            self._values = {
            }
            if autoprovision is not None: self._values["autoprovision"] = autoprovision
            if driver is not None: self._values["driver"] = driver
            if driver_opts is not None: self._values["driver_opts"] = driver_opts
            if labels is not None: self._values["labels"] = labels
            if scope is not None: self._values["scope"] = scope

        @builtins.property
        def autoprovision(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnTaskDefinition.DockerVolumeConfigurationProperty.Autoprovision``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-dockervolumeconfiguration.html#cfn-ecs-taskdefinition-dockervolumeconfiguration-autoprovision
            """
            return self._values.get('autoprovision')

        @builtins.property
        def driver(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.DockerVolumeConfigurationProperty.Driver``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-dockervolumeconfiguration.html#cfn-ecs-taskdefinition-dockervolumeconfiguration-driver
            """
            return self._values.get('driver')

        @builtins.property
        def driver_opts(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[str, str]]]:
            """``CfnTaskDefinition.DockerVolumeConfigurationProperty.DriverOpts``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-dockervolumeconfiguration.html#cfn-ecs-taskdefinition-dockervolumeconfiguration-driveropts
            """
            return self._values.get('driver_opts')

        @builtins.property
        def labels(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[str, str]]]:
            """``CfnTaskDefinition.DockerVolumeConfigurationProperty.Labels``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-dockervolumeconfiguration.html#cfn-ecs-taskdefinition-dockervolumeconfiguration-labels
            """
            return self._values.get('labels')

        @builtins.property
        def scope(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.DockerVolumeConfigurationProperty.Scope``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-dockervolumeconfiguration.html#cfn-ecs-taskdefinition-dockervolumeconfiguration-scope
            """
            return self._values.get('scope')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DockerVolumeConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnTaskDefinition.FirelensConfigurationProperty", jsii_struct_bases=[], name_mapping={'type': 'type', 'options': 'options'})
    class FirelensConfigurationProperty():
        def __init__(self, *, type: str, options: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[str, str]]]=None) -> None:
            """
            :param type: ``CfnTaskDefinition.FirelensConfigurationProperty.Type``.
            :param options: ``CfnTaskDefinition.FirelensConfigurationProperty.Options``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-firelensconfiguration.html
            """
            self._values = {
                'type': type,
            }
            if options is not None: self._values["options"] = options

        @builtins.property
        def type(self) -> str:
            """``CfnTaskDefinition.FirelensConfigurationProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-firelensconfiguration.html#cfn-ecs-taskdefinition-firelensconfiguration-type
            """
            return self._values.get('type')

        @builtins.property
        def options(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[str, str]]]:
            """``CfnTaskDefinition.FirelensConfigurationProperty.Options``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-firelensconfiguration.html#cfn-ecs-taskdefinition-firelensconfiguration-options
            """
            return self._values.get('options')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'FirelensConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnTaskDefinition.HealthCheckProperty", jsii_struct_bases=[], name_mapping={'command': 'command', 'interval': 'interval', 'retries': 'retries', 'start_period': 'startPeriod', 'timeout': 'timeout'})
    class HealthCheckProperty():
        def __init__(self, *, command: typing.List[str], interval: typing.Optional[jsii.Number]=None, retries: typing.Optional[jsii.Number]=None, start_period: typing.Optional[jsii.Number]=None, timeout: typing.Optional[jsii.Number]=None) -> None:
            """
            :param command: ``CfnTaskDefinition.HealthCheckProperty.Command``.
            :param interval: ``CfnTaskDefinition.HealthCheckProperty.Interval``.
            :param retries: ``CfnTaskDefinition.HealthCheckProperty.Retries``.
            :param start_period: ``CfnTaskDefinition.HealthCheckProperty.StartPeriod``.
            :param timeout: ``CfnTaskDefinition.HealthCheckProperty.Timeout``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-healthcheck.html
            """
            self._values = {
                'command': command,
            }
            if interval is not None: self._values["interval"] = interval
            if retries is not None: self._values["retries"] = retries
            if start_period is not None: self._values["start_period"] = start_period
            if timeout is not None: self._values["timeout"] = timeout

        @builtins.property
        def command(self) -> typing.List[str]:
            """``CfnTaskDefinition.HealthCheckProperty.Command``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-healthcheck.html#cfn-ecs-taskdefinition-healthcheck-command
            """
            return self._values.get('command')

        @builtins.property
        def interval(self) -> typing.Optional[jsii.Number]:
            """``CfnTaskDefinition.HealthCheckProperty.Interval``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-healthcheck.html#cfn-ecs-taskdefinition-healthcheck-interval
            """
            return self._values.get('interval')

        @builtins.property
        def retries(self) -> typing.Optional[jsii.Number]:
            """``CfnTaskDefinition.HealthCheckProperty.Retries``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-healthcheck.html#cfn-ecs-taskdefinition-healthcheck-retries
            """
            return self._values.get('retries')

        @builtins.property
        def start_period(self) -> typing.Optional[jsii.Number]:
            """``CfnTaskDefinition.HealthCheckProperty.StartPeriod``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-healthcheck.html#cfn-ecs-taskdefinition-healthcheck-startperiod
            """
            return self._values.get('start_period')

        @builtins.property
        def timeout(self) -> typing.Optional[jsii.Number]:
            """``CfnTaskDefinition.HealthCheckProperty.Timeout``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-healthcheck.html#cfn-ecs-taskdefinition-healthcheck-timeout
            """
            return self._values.get('timeout')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'HealthCheckProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnTaskDefinition.HostEntryProperty", jsii_struct_bases=[], name_mapping={'hostname': 'hostname', 'ip_address': 'ipAddress'})
    class HostEntryProperty():
        def __init__(self, *, hostname: str, ip_address: str) -> None:
            """
            :param hostname: ``CfnTaskDefinition.HostEntryProperty.Hostname``.
            :param ip_address: ``CfnTaskDefinition.HostEntryProperty.IpAddress``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-hostentry.html
            """
            self._values = {
                'hostname': hostname,
                'ip_address': ip_address,
            }

        @builtins.property
        def hostname(self) -> str:
            """``CfnTaskDefinition.HostEntryProperty.Hostname``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-hostentry.html#cfn-ecs-taskdefinition-containerdefinition-hostentry-hostname
            """
            return self._values.get('hostname')

        @builtins.property
        def ip_address(self) -> str:
            """``CfnTaskDefinition.HostEntryProperty.IpAddress``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-hostentry.html#cfn-ecs-taskdefinition-containerdefinition-hostentry-ipaddress
            """
            return self._values.get('ip_address')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'HostEntryProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnTaskDefinition.HostVolumePropertiesProperty", jsii_struct_bases=[], name_mapping={'source_path': 'sourcePath'})
    class HostVolumePropertiesProperty():
        def __init__(self, *, source_path: typing.Optional[str]=None) -> None:
            """
            :param source_path: ``CfnTaskDefinition.HostVolumePropertiesProperty.SourcePath``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-volumes-host.html
            """
            self._values = {
            }
            if source_path is not None: self._values["source_path"] = source_path

        @builtins.property
        def source_path(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.HostVolumePropertiesProperty.SourcePath``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-volumes-host.html#cfn-ecs-taskdefinition-volumes-host-sourcepath
            """
            return self._values.get('source_path')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'HostVolumePropertiesProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnTaskDefinition.InferenceAcceleratorProperty", jsii_struct_bases=[], name_mapping={'device_name': 'deviceName', 'device_type': 'deviceType'})
    class InferenceAcceleratorProperty():
        def __init__(self, *, device_name: typing.Optional[str]=None, device_type: typing.Optional[str]=None) -> None:
            """
            :param device_name: ``CfnTaskDefinition.InferenceAcceleratorProperty.DeviceName``.
            :param device_type: ``CfnTaskDefinition.InferenceAcceleratorProperty.DeviceType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-inferenceaccelerator.html
            """
            self._values = {
            }
            if device_name is not None: self._values["device_name"] = device_name
            if device_type is not None: self._values["device_type"] = device_type

        @builtins.property
        def device_name(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.InferenceAcceleratorProperty.DeviceName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-inferenceaccelerator.html#cfn-ecs-taskdefinition-inferenceaccelerator-devicename
            """
            return self._values.get('device_name')

        @builtins.property
        def device_type(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.InferenceAcceleratorProperty.DeviceType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-inferenceaccelerator.html#cfn-ecs-taskdefinition-inferenceaccelerator-devicetype
            """
            return self._values.get('device_type')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'InferenceAcceleratorProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnTaskDefinition.KernelCapabilitiesProperty", jsii_struct_bases=[], name_mapping={'add': 'add', 'drop': 'drop'})
    class KernelCapabilitiesProperty():
        def __init__(self, *, add: typing.Optional[typing.List[str]]=None, drop: typing.Optional[typing.List[str]]=None) -> None:
            """
            :param add: ``CfnTaskDefinition.KernelCapabilitiesProperty.Add``.
            :param drop: ``CfnTaskDefinition.KernelCapabilitiesProperty.Drop``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-kernelcapabilities.html
            """
            self._values = {
            }
            if add is not None: self._values["add"] = add
            if drop is not None: self._values["drop"] = drop

        @builtins.property
        def add(self) -> typing.Optional[typing.List[str]]:
            """``CfnTaskDefinition.KernelCapabilitiesProperty.Add``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-kernelcapabilities.html#cfn-ecs-taskdefinition-kernelcapabilities-add
            """
            return self._values.get('add')

        @builtins.property
        def drop(self) -> typing.Optional[typing.List[str]]:
            """``CfnTaskDefinition.KernelCapabilitiesProperty.Drop``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-kernelcapabilities.html#cfn-ecs-taskdefinition-kernelcapabilities-drop
            """
            return self._values.get('drop')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'KernelCapabilitiesProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnTaskDefinition.KeyValuePairProperty", jsii_struct_bases=[], name_mapping={'name': 'name', 'value': 'value'})
    class KeyValuePairProperty():
        def __init__(self, *, name: typing.Optional[str]=None, value: typing.Optional[str]=None) -> None:
            """
            :param name: ``CfnTaskDefinition.KeyValuePairProperty.Name``.
            :param value: ``CfnTaskDefinition.KeyValuePairProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-environment.html
            """
            self._values = {
            }
            if name is not None: self._values["name"] = name
            if value is not None: self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.KeyValuePairProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-environment.html#cfn-ecs-taskdefinition-containerdefinition-environment-name
            """
            return self._values.get('name')

        @builtins.property
        def value(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.KeyValuePairProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-environment.html#cfn-ecs-taskdefinition-containerdefinition-environment-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'KeyValuePairProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnTaskDefinition.LinuxParametersProperty", jsii_struct_bases=[], name_mapping={'capabilities': 'capabilities', 'devices': 'devices', 'init_process_enabled': 'initProcessEnabled', 'max_swap': 'maxSwap', 'shared_memory_size': 'sharedMemorySize', 'swappiness': 'swappiness', 'tmpfs': 'tmpfs'})
    class LinuxParametersProperty():
        def __init__(self, *, capabilities: typing.Optional[typing.Union["CfnTaskDefinition.KernelCapabilitiesProperty", _IResolvable_9ceae33e]]=None, devices: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskDefinition.DeviceProperty", _IResolvable_9ceae33e]]]]=None, init_process_enabled: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, max_swap: typing.Optional[jsii.Number]=None, shared_memory_size: typing.Optional[jsii.Number]=None, swappiness: typing.Optional[jsii.Number]=None, tmpfs: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskDefinition.TmpfsProperty", _IResolvable_9ceae33e]]]]=None) -> None:
            """
            :param capabilities: ``CfnTaskDefinition.LinuxParametersProperty.Capabilities``.
            :param devices: ``CfnTaskDefinition.LinuxParametersProperty.Devices``.
            :param init_process_enabled: ``CfnTaskDefinition.LinuxParametersProperty.InitProcessEnabled``.
            :param max_swap: ``CfnTaskDefinition.LinuxParametersProperty.MaxSwap``.
            :param shared_memory_size: ``CfnTaskDefinition.LinuxParametersProperty.SharedMemorySize``.
            :param swappiness: ``CfnTaskDefinition.LinuxParametersProperty.Swappiness``.
            :param tmpfs: ``CfnTaskDefinition.LinuxParametersProperty.Tmpfs``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-linuxparameters.html
            """
            self._values = {
            }
            if capabilities is not None: self._values["capabilities"] = capabilities
            if devices is not None: self._values["devices"] = devices
            if init_process_enabled is not None: self._values["init_process_enabled"] = init_process_enabled
            if max_swap is not None: self._values["max_swap"] = max_swap
            if shared_memory_size is not None: self._values["shared_memory_size"] = shared_memory_size
            if swappiness is not None: self._values["swappiness"] = swappiness
            if tmpfs is not None: self._values["tmpfs"] = tmpfs

        @builtins.property
        def capabilities(self) -> typing.Optional[typing.Union["CfnTaskDefinition.KernelCapabilitiesProperty", _IResolvable_9ceae33e]]:
            """``CfnTaskDefinition.LinuxParametersProperty.Capabilities``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-linuxparameters.html#cfn-ecs-taskdefinition-linuxparameters-capabilities
            """
            return self._values.get('capabilities')

        @builtins.property
        def devices(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskDefinition.DeviceProperty", _IResolvable_9ceae33e]]]]:
            """``CfnTaskDefinition.LinuxParametersProperty.Devices``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-linuxparameters.html#cfn-ecs-taskdefinition-linuxparameters-devices
            """
            return self._values.get('devices')

        @builtins.property
        def init_process_enabled(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnTaskDefinition.LinuxParametersProperty.InitProcessEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-linuxparameters.html#cfn-ecs-taskdefinition-linuxparameters-initprocessenabled
            """
            return self._values.get('init_process_enabled')

        @builtins.property
        def max_swap(self) -> typing.Optional[jsii.Number]:
            """``CfnTaskDefinition.LinuxParametersProperty.MaxSwap``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-linuxparameters.html#cfn-ecs-taskdefinition-linuxparameters-maxswap
            """
            return self._values.get('max_swap')

        @builtins.property
        def shared_memory_size(self) -> typing.Optional[jsii.Number]:
            """``CfnTaskDefinition.LinuxParametersProperty.SharedMemorySize``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-linuxparameters.html#cfn-ecs-taskdefinition-linuxparameters-sharedmemorysize
            """
            return self._values.get('shared_memory_size')

        @builtins.property
        def swappiness(self) -> typing.Optional[jsii.Number]:
            """``CfnTaskDefinition.LinuxParametersProperty.Swappiness``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-linuxparameters.html#cfn-ecs-taskdefinition-linuxparameters-swappiness
            """
            return self._values.get('swappiness')

        @builtins.property
        def tmpfs(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskDefinition.TmpfsProperty", _IResolvable_9ceae33e]]]]:
            """``CfnTaskDefinition.LinuxParametersProperty.Tmpfs``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-linuxparameters.html#cfn-ecs-taskdefinition-linuxparameters-tmpfs
            """
            return self._values.get('tmpfs')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LinuxParametersProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnTaskDefinition.LogConfigurationProperty", jsii_struct_bases=[], name_mapping={'log_driver': 'logDriver', 'options': 'options', 'secret_options': 'secretOptions'})
    class LogConfigurationProperty():
        def __init__(self, *, log_driver: str, options: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[str, str]]]=None, secret_options: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskDefinition.SecretProperty", _IResolvable_9ceae33e]]]]=None) -> None:
            """
            :param log_driver: ``CfnTaskDefinition.LogConfigurationProperty.LogDriver``.
            :param options: ``CfnTaskDefinition.LogConfigurationProperty.Options``.
            :param secret_options: ``CfnTaskDefinition.LogConfigurationProperty.SecretOptions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-logconfiguration.html
            """
            self._values = {
                'log_driver': log_driver,
            }
            if options is not None: self._values["options"] = options
            if secret_options is not None: self._values["secret_options"] = secret_options

        @builtins.property
        def log_driver(self) -> str:
            """``CfnTaskDefinition.LogConfigurationProperty.LogDriver``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-logconfiguration.html#cfn-ecs-taskdefinition-containerdefinition-logconfiguration-logdriver
            """
            return self._values.get('log_driver')

        @builtins.property
        def options(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[str, str]]]:
            """``CfnTaskDefinition.LogConfigurationProperty.Options``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-logconfiguration.html#cfn-ecs-taskdefinition-containerdefinition-logconfiguration-options
            """
            return self._values.get('options')

        @builtins.property
        def secret_options(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskDefinition.SecretProperty", _IResolvable_9ceae33e]]]]:
            """``CfnTaskDefinition.LogConfigurationProperty.SecretOptions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-logconfiguration.html#cfn-ecs-taskdefinition-logconfiguration-secretoptions
            """
            return self._values.get('secret_options')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LogConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnTaskDefinition.MountPointProperty", jsii_struct_bases=[], name_mapping={'container_path': 'containerPath', 'read_only': 'readOnly', 'source_volume': 'sourceVolume'})
    class MountPointProperty():
        def __init__(self, *, container_path: typing.Optional[str]=None, read_only: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, source_volume: typing.Optional[str]=None) -> None:
            """
            :param container_path: ``CfnTaskDefinition.MountPointProperty.ContainerPath``.
            :param read_only: ``CfnTaskDefinition.MountPointProperty.ReadOnly``.
            :param source_volume: ``CfnTaskDefinition.MountPointProperty.SourceVolume``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-mountpoints.html
            """
            self._values = {
            }
            if container_path is not None: self._values["container_path"] = container_path
            if read_only is not None: self._values["read_only"] = read_only
            if source_volume is not None: self._values["source_volume"] = source_volume

        @builtins.property
        def container_path(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.MountPointProperty.ContainerPath``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-mountpoints.html#cfn-ecs-taskdefinition-containerdefinition-mountpoints-containerpath
            """
            return self._values.get('container_path')

        @builtins.property
        def read_only(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnTaskDefinition.MountPointProperty.ReadOnly``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-mountpoints.html#cfn-ecs-taskdefinition-containerdefinition-mountpoints-readonly
            """
            return self._values.get('read_only')

        @builtins.property
        def source_volume(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.MountPointProperty.SourceVolume``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-mountpoints.html#cfn-ecs-taskdefinition-containerdefinition-mountpoints-sourcevolume
            """
            return self._values.get('source_volume')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'MountPointProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnTaskDefinition.PortMappingProperty", jsii_struct_bases=[], name_mapping={'container_port': 'containerPort', 'host_port': 'hostPort', 'protocol': 'protocol'})
    class PortMappingProperty():
        def __init__(self, *, container_port: typing.Optional[jsii.Number]=None, host_port: typing.Optional[jsii.Number]=None, protocol: typing.Optional[str]=None) -> None:
            """
            :param container_port: ``CfnTaskDefinition.PortMappingProperty.ContainerPort``.
            :param host_port: ``CfnTaskDefinition.PortMappingProperty.HostPort``.
            :param protocol: ``CfnTaskDefinition.PortMappingProperty.Protocol``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-portmappings.html
            """
            self._values = {
            }
            if container_port is not None: self._values["container_port"] = container_port
            if host_port is not None: self._values["host_port"] = host_port
            if protocol is not None: self._values["protocol"] = protocol

        @builtins.property
        def container_port(self) -> typing.Optional[jsii.Number]:
            """``CfnTaskDefinition.PortMappingProperty.ContainerPort``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-portmappings.html#cfn-ecs-taskdefinition-containerdefinition-portmappings-containerport
            """
            return self._values.get('container_port')

        @builtins.property
        def host_port(self) -> typing.Optional[jsii.Number]:
            """``CfnTaskDefinition.PortMappingProperty.HostPort``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-portmappings.html#cfn-ecs-taskdefinition-containerdefinition-portmappings-readonly
            """
            return self._values.get('host_port')

        @builtins.property
        def protocol(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.PortMappingProperty.Protocol``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-portmappings.html#cfn-ecs-taskdefinition-containerdefinition-portmappings-sourcevolume
            """
            return self._values.get('protocol')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'PortMappingProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnTaskDefinition.ProxyConfigurationProperty", jsii_struct_bases=[], name_mapping={'container_name': 'containerName', 'proxy_configuration_properties': 'proxyConfigurationProperties', 'type': 'type'})
    class ProxyConfigurationProperty():
        def __init__(self, *, container_name: str, proxy_configuration_properties: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskDefinition.KeyValuePairProperty", _IResolvable_9ceae33e]]]]=None, type: typing.Optional[str]=None) -> None:
            """
            :param container_name: ``CfnTaskDefinition.ProxyConfigurationProperty.ContainerName``.
            :param proxy_configuration_properties: ``CfnTaskDefinition.ProxyConfigurationProperty.ProxyConfigurationProperties``.
            :param type: ``CfnTaskDefinition.ProxyConfigurationProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-proxyconfiguration.html
            """
            self._values = {
                'container_name': container_name,
            }
            if proxy_configuration_properties is not None: self._values["proxy_configuration_properties"] = proxy_configuration_properties
            if type is not None: self._values["type"] = type

        @builtins.property
        def container_name(self) -> str:
            """``CfnTaskDefinition.ProxyConfigurationProperty.ContainerName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-proxyconfiguration.html#cfn-ecs-taskdefinition-proxyconfiguration-containername
            """
            return self._values.get('container_name')

        @builtins.property
        def proxy_configuration_properties(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskDefinition.KeyValuePairProperty", _IResolvable_9ceae33e]]]]:
            """``CfnTaskDefinition.ProxyConfigurationProperty.ProxyConfigurationProperties``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-proxyconfiguration.html#cfn-ecs-taskdefinition-proxyconfiguration-proxyconfigurationproperties
            """
            return self._values.get('proxy_configuration_properties')

        @builtins.property
        def type(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.ProxyConfigurationProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-proxyconfiguration.html#cfn-ecs-taskdefinition-proxyconfiguration-type
            """
            return self._values.get('type')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ProxyConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnTaskDefinition.RepositoryCredentialsProperty", jsii_struct_bases=[], name_mapping={'credentials_parameter': 'credentialsParameter'})
    class RepositoryCredentialsProperty():
        def __init__(self, *, credentials_parameter: typing.Optional[str]=None) -> None:
            """
            :param credentials_parameter: ``CfnTaskDefinition.RepositoryCredentialsProperty.CredentialsParameter``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-repositorycredentials.html
            """
            self._values = {
            }
            if credentials_parameter is not None: self._values["credentials_parameter"] = credentials_parameter

        @builtins.property
        def credentials_parameter(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.RepositoryCredentialsProperty.CredentialsParameter``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-repositorycredentials.html#cfn-ecs-taskdefinition-repositorycredentials-credentialsparameter
            """
            return self._values.get('credentials_parameter')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'RepositoryCredentialsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnTaskDefinition.ResourceRequirementProperty", jsii_struct_bases=[], name_mapping={'type': 'type', 'value': 'value'})
    class ResourceRequirementProperty():
        def __init__(self, *, type: str, value: str) -> None:
            """
            :param type: ``CfnTaskDefinition.ResourceRequirementProperty.Type``.
            :param value: ``CfnTaskDefinition.ResourceRequirementProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-resourcerequirement.html
            """
            self._values = {
                'type': type,
                'value': value,
            }

        @builtins.property
        def type(self) -> str:
            """``CfnTaskDefinition.ResourceRequirementProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-resourcerequirement.html#cfn-ecs-taskdefinition-resourcerequirement-type
            """
            return self._values.get('type')

        @builtins.property
        def value(self) -> str:
            """``CfnTaskDefinition.ResourceRequirementProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-resourcerequirement.html#cfn-ecs-taskdefinition-resourcerequirement-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ResourceRequirementProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnTaskDefinition.SecretProperty", jsii_struct_bases=[], name_mapping={'name': 'name', 'value_from': 'valueFrom'})
    class SecretProperty():
        def __init__(self, *, name: str, value_from: str) -> None:
            """
            :param name: ``CfnTaskDefinition.SecretProperty.Name``.
            :param value_from: ``CfnTaskDefinition.SecretProperty.ValueFrom``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-secret.html
            """
            self._values = {
                'name': name,
                'value_from': value_from,
            }

        @builtins.property
        def name(self) -> str:
            """``CfnTaskDefinition.SecretProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-secret.html#cfn-ecs-taskdefinition-secret-name
            """
            return self._values.get('name')

        @builtins.property
        def value_from(self) -> str:
            """``CfnTaskDefinition.SecretProperty.ValueFrom``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-secret.html#cfn-ecs-taskdefinition-secret-valuefrom
            """
            return self._values.get('value_from')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SecretProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnTaskDefinition.SystemControlProperty", jsii_struct_bases=[], name_mapping={'namespace': 'namespace', 'value': 'value'})
    class SystemControlProperty():
        def __init__(self, *, namespace: str, value: str) -> None:
            """
            :param namespace: ``CfnTaskDefinition.SystemControlProperty.Namespace``.
            :param value: ``CfnTaskDefinition.SystemControlProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-systemcontrol.html
            """
            self._values = {
                'namespace': namespace,
                'value': value,
            }

        @builtins.property
        def namespace(self) -> str:
            """``CfnTaskDefinition.SystemControlProperty.Namespace``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-systemcontrol.html#cfn-ecs-taskdefinition-systemcontrol-namespace
            """
            return self._values.get('namespace')

        @builtins.property
        def value(self) -> str:
            """``CfnTaskDefinition.SystemControlProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-systemcontrol.html#cfn-ecs-taskdefinition-systemcontrol-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SystemControlProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnTaskDefinition.TaskDefinitionPlacementConstraintProperty", jsii_struct_bases=[], name_mapping={'type': 'type', 'expression': 'expression'})
    class TaskDefinitionPlacementConstraintProperty():
        def __init__(self, *, type: str, expression: typing.Optional[str]=None) -> None:
            """
            :param type: ``CfnTaskDefinition.TaskDefinitionPlacementConstraintProperty.Type``.
            :param expression: ``CfnTaskDefinition.TaskDefinitionPlacementConstraintProperty.Expression``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-taskdefinitionplacementconstraint.html
            """
            self._values = {
                'type': type,
            }
            if expression is not None: self._values["expression"] = expression

        @builtins.property
        def type(self) -> str:
            """``CfnTaskDefinition.TaskDefinitionPlacementConstraintProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-taskdefinitionplacementconstraint.html#cfn-ecs-taskdefinition-taskdefinitionplacementconstraint-type
            """
            return self._values.get('type')

        @builtins.property
        def expression(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.TaskDefinitionPlacementConstraintProperty.Expression``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-taskdefinitionplacementconstraint.html#cfn-ecs-taskdefinition-taskdefinitionplacementconstraint-expression
            """
            return self._values.get('expression')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TaskDefinitionPlacementConstraintProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnTaskDefinition.TmpfsProperty", jsii_struct_bases=[], name_mapping={'size': 'size', 'container_path': 'containerPath', 'mount_options': 'mountOptions'})
    class TmpfsProperty():
        def __init__(self, *, size: jsii.Number, container_path: typing.Optional[str]=None, mount_options: typing.Optional[typing.List[str]]=None) -> None:
            """
            :param size: ``CfnTaskDefinition.TmpfsProperty.Size``.
            :param container_path: ``CfnTaskDefinition.TmpfsProperty.ContainerPath``.
            :param mount_options: ``CfnTaskDefinition.TmpfsProperty.MountOptions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-tmpfs.html
            """
            self._values = {
                'size': size,
            }
            if container_path is not None: self._values["container_path"] = container_path
            if mount_options is not None: self._values["mount_options"] = mount_options

        @builtins.property
        def size(self) -> jsii.Number:
            """``CfnTaskDefinition.TmpfsProperty.Size``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-tmpfs.html#cfn-ecs-taskdefinition-tmpfs-size
            """
            return self._values.get('size')

        @builtins.property
        def container_path(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.TmpfsProperty.ContainerPath``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-tmpfs.html#cfn-ecs-taskdefinition-tmpfs-containerpath
            """
            return self._values.get('container_path')

        @builtins.property
        def mount_options(self) -> typing.Optional[typing.List[str]]:
            """``CfnTaskDefinition.TmpfsProperty.MountOptions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-tmpfs.html#cfn-ecs-taskdefinition-tmpfs-mountoptions
            """
            return self._values.get('mount_options')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TmpfsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnTaskDefinition.UlimitProperty", jsii_struct_bases=[], name_mapping={'hard_limit': 'hardLimit', 'name': 'name', 'soft_limit': 'softLimit'})
    class UlimitProperty():
        def __init__(self, *, hard_limit: jsii.Number, name: str, soft_limit: jsii.Number) -> None:
            """
            :param hard_limit: ``CfnTaskDefinition.UlimitProperty.HardLimit``.
            :param name: ``CfnTaskDefinition.UlimitProperty.Name``.
            :param soft_limit: ``CfnTaskDefinition.UlimitProperty.SoftLimit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-ulimit.html
            """
            self._values = {
                'hard_limit': hard_limit,
                'name': name,
                'soft_limit': soft_limit,
            }

        @builtins.property
        def hard_limit(self) -> jsii.Number:
            """``CfnTaskDefinition.UlimitProperty.HardLimit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-ulimit.html#cfn-ecs-taskdefinition-containerdefinition-ulimit-hardlimit
            """
            return self._values.get('hard_limit')

        @builtins.property
        def name(self) -> str:
            """``CfnTaskDefinition.UlimitProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-ulimit.html#cfn-ecs-taskdefinition-containerdefinition-ulimit-name
            """
            return self._values.get('name')

        @builtins.property
        def soft_limit(self) -> jsii.Number:
            """``CfnTaskDefinition.UlimitProperty.SoftLimit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-ulimit.html#cfn-ecs-taskdefinition-containerdefinition-ulimit-softlimit
            """
            return self._values.get('soft_limit')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'UlimitProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnTaskDefinition.VolumeFromProperty", jsii_struct_bases=[], name_mapping={'read_only': 'readOnly', 'source_container': 'sourceContainer'})
    class VolumeFromProperty():
        def __init__(self, *, read_only: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, source_container: typing.Optional[str]=None) -> None:
            """
            :param read_only: ``CfnTaskDefinition.VolumeFromProperty.ReadOnly``.
            :param source_container: ``CfnTaskDefinition.VolumeFromProperty.SourceContainer``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-volumesfrom.html
            """
            self._values = {
            }
            if read_only is not None: self._values["read_only"] = read_only
            if source_container is not None: self._values["source_container"] = source_container

        @builtins.property
        def read_only(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnTaskDefinition.VolumeFromProperty.ReadOnly``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-volumesfrom.html#cfn-ecs-taskdefinition-containerdefinition-volumesfrom-readonly
            """
            return self._values.get('read_only')

        @builtins.property
        def source_container(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.VolumeFromProperty.SourceContainer``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions-volumesfrom.html#cfn-ecs-taskdefinition-containerdefinition-volumesfrom-sourcecontainer
            """
            return self._values.get('source_container')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'VolumeFromProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnTaskDefinition.VolumeProperty", jsii_struct_bases=[], name_mapping={'docker_volume_configuration': 'dockerVolumeConfiguration', 'host': 'host', 'name': 'name'})
    class VolumeProperty():
        def __init__(self, *, docker_volume_configuration: typing.Optional[typing.Union["CfnTaskDefinition.DockerVolumeConfigurationProperty", _IResolvable_9ceae33e]]=None, host: typing.Optional[typing.Union["CfnTaskDefinition.HostVolumePropertiesProperty", _IResolvable_9ceae33e]]=None, name: typing.Optional[str]=None) -> None:
            """
            :param docker_volume_configuration: ``CfnTaskDefinition.VolumeProperty.DockerVolumeConfiguration``.
            :param host: ``CfnTaskDefinition.VolumeProperty.Host``.
            :param name: ``CfnTaskDefinition.VolumeProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-volumes.html
            """
            self._values = {
            }
            if docker_volume_configuration is not None: self._values["docker_volume_configuration"] = docker_volume_configuration
            if host is not None: self._values["host"] = host
            if name is not None: self._values["name"] = name

        @builtins.property
        def docker_volume_configuration(self) -> typing.Optional[typing.Union["CfnTaskDefinition.DockerVolumeConfigurationProperty", _IResolvable_9ceae33e]]:
            """``CfnTaskDefinition.VolumeProperty.DockerVolumeConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-volumes.html#cfn-ecs-taskdefinition-volume-dockervolumeconfiguration
            """
            return self._values.get('docker_volume_configuration')

        @builtins.property
        def host(self) -> typing.Optional[typing.Union["CfnTaskDefinition.HostVolumePropertiesProperty", _IResolvable_9ceae33e]]:
            """``CfnTaskDefinition.VolumeProperty.Host``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-volumes.html#cfn-ecs-taskdefinition-volumes-host
            """
            return self._values.get('host')

        @builtins.property
        def name(self) -> typing.Optional[str]:
            """``CfnTaskDefinition.VolumeProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-volumes.html#cfn-ecs-taskdefinition-volumes-name
            """
            return self._values.get('name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'VolumeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnTaskDefinitionProps", jsii_struct_bases=[], name_mapping={'container_definitions': 'containerDefinitions', 'cpu': 'cpu', 'execution_role_arn': 'executionRoleArn', 'family': 'family', 'inference_accelerators': 'inferenceAccelerators', 'ipc_mode': 'ipcMode', 'memory': 'memory', 'network_mode': 'networkMode', 'pid_mode': 'pidMode', 'placement_constraints': 'placementConstraints', 'proxy_configuration': 'proxyConfiguration', 'requires_compatibilities': 'requiresCompatibilities', 'tags': 'tags', 'task_role_arn': 'taskRoleArn', 'volumes': 'volumes'})
class CfnTaskDefinitionProps():
    def __init__(self, *, container_definitions: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskDefinition.ContainerDefinitionProperty", _IResolvable_9ceae33e]]]]=None, cpu: typing.Optional[str]=None, execution_role_arn: typing.Optional[str]=None, family: typing.Optional[str]=None, inference_accelerators: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskDefinition.InferenceAcceleratorProperty", _IResolvable_9ceae33e]]]]=None, ipc_mode: typing.Optional[str]=None, memory: typing.Optional[str]=None, network_mode: typing.Optional[str]=None, pid_mode: typing.Optional[str]=None, placement_constraints: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskDefinition.TaskDefinitionPlacementConstraintProperty", _IResolvable_9ceae33e]]]]=None, proxy_configuration: typing.Optional[typing.Union["CfnTaskDefinition.ProxyConfigurationProperty", _IResolvable_9ceae33e]]=None, requires_compatibilities: typing.Optional[typing.List[str]]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None, task_role_arn: typing.Optional[str]=None, volumes: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskDefinition.VolumeProperty", _IResolvable_9ceae33e]]]]=None) -> None:
        """Properties for defining a ``AWS::ECS::TaskDefinition``.

        :param container_definitions: ``AWS::ECS::TaskDefinition.ContainerDefinitions``.
        :param cpu: ``AWS::ECS::TaskDefinition.Cpu``.
        :param execution_role_arn: ``AWS::ECS::TaskDefinition.ExecutionRoleArn``.
        :param family: ``AWS::ECS::TaskDefinition.Family``.
        :param inference_accelerators: ``AWS::ECS::TaskDefinition.InferenceAccelerators``.
        :param ipc_mode: ``AWS::ECS::TaskDefinition.IpcMode``.
        :param memory: ``AWS::ECS::TaskDefinition.Memory``.
        :param network_mode: ``AWS::ECS::TaskDefinition.NetworkMode``.
        :param pid_mode: ``AWS::ECS::TaskDefinition.PidMode``.
        :param placement_constraints: ``AWS::ECS::TaskDefinition.PlacementConstraints``.
        :param proxy_configuration: ``AWS::ECS::TaskDefinition.ProxyConfiguration``.
        :param requires_compatibilities: ``AWS::ECS::TaskDefinition.RequiresCompatibilities``.
        :param tags: ``AWS::ECS::TaskDefinition.Tags``.
        :param task_role_arn: ``AWS::ECS::TaskDefinition.TaskRoleArn``.
        :param volumes: ``AWS::ECS::TaskDefinition.Volumes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html
        """
        self._values = {
        }
        if container_definitions is not None: self._values["container_definitions"] = container_definitions
        if cpu is not None: self._values["cpu"] = cpu
        if execution_role_arn is not None: self._values["execution_role_arn"] = execution_role_arn
        if family is not None: self._values["family"] = family
        if inference_accelerators is not None: self._values["inference_accelerators"] = inference_accelerators
        if ipc_mode is not None: self._values["ipc_mode"] = ipc_mode
        if memory is not None: self._values["memory"] = memory
        if network_mode is not None: self._values["network_mode"] = network_mode
        if pid_mode is not None: self._values["pid_mode"] = pid_mode
        if placement_constraints is not None: self._values["placement_constraints"] = placement_constraints
        if proxy_configuration is not None: self._values["proxy_configuration"] = proxy_configuration
        if requires_compatibilities is not None: self._values["requires_compatibilities"] = requires_compatibilities
        if tags is not None: self._values["tags"] = tags
        if task_role_arn is not None: self._values["task_role_arn"] = task_role_arn
        if volumes is not None: self._values["volumes"] = volumes

    @builtins.property
    def container_definitions(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskDefinition.ContainerDefinitionProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::ECS::TaskDefinition.ContainerDefinitions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-containerdefinitions
        """
        return self._values.get('container_definitions')

    @builtins.property
    def cpu(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.Cpu``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-cpu
        """
        return self._values.get('cpu')

    @builtins.property
    def execution_role_arn(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.ExecutionRoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-executionrolearn
        """
        return self._values.get('execution_role_arn')

    @builtins.property
    def family(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.Family``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-family
        """
        return self._values.get('family')

    @builtins.property
    def inference_accelerators(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskDefinition.InferenceAcceleratorProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::ECS::TaskDefinition.InferenceAccelerators``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-inferenceaccelerators
        """
        return self._values.get('inference_accelerators')

    @builtins.property
    def ipc_mode(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.IpcMode``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-ipcmode
        """
        return self._values.get('ipc_mode')

    @builtins.property
    def memory(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.Memory``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-memory
        """
        return self._values.get('memory')

    @builtins.property
    def network_mode(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.NetworkMode``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-networkmode
        """
        return self._values.get('network_mode')

    @builtins.property
    def pid_mode(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.PidMode``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-pidmode
        """
        return self._values.get('pid_mode')

    @builtins.property
    def placement_constraints(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskDefinition.TaskDefinitionPlacementConstraintProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::ECS::TaskDefinition.PlacementConstraints``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-placementconstraints
        """
        return self._values.get('placement_constraints')

    @builtins.property
    def proxy_configuration(self) -> typing.Optional[typing.Union["CfnTaskDefinition.ProxyConfigurationProperty", _IResolvable_9ceae33e]]:
        """``AWS::ECS::TaskDefinition.ProxyConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-proxyconfiguration
        """
        return self._values.get('proxy_configuration')

    @builtins.property
    def requires_compatibilities(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ECS::TaskDefinition.RequiresCompatibilities``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-requirescompatibilities
        """
        return self._values.get('requires_compatibilities')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::ECS::TaskDefinition.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-tags
        """
        return self._values.get('tags')

    @builtins.property
    def task_role_arn(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskDefinition.TaskRoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-taskrolearn
        """
        return self._values.get('task_role_arn')

    @builtins.property
    def volumes(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskDefinition.VolumeProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::ECS::TaskDefinition.Volumes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-volumes
        """
        return self._values.get('volumes')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnTaskDefinitionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnTaskSet(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs.CfnTaskSet"):
    """A CloudFormation ``AWS::ECS::TaskSet``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskset.html
    cloudformationResource:
    :cloudformationResource:: AWS::ECS::TaskSet
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, cluster: str, service: str, task_definition: str, external_id: typing.Optional[str]=None, launch_type: typing.Optional[str]=None, load_balancers: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["LoadBalancerProperty", _IResolvable_9ceae33e]]]]=None, network_configuration: typing.Optional[typing.Union["NetworkConfigurationProperty", _IResolvable_9ceae33e]]=None, platform_version: typing.Optional[str]=None, scale: typing.Optional[typing.Union["ScaleProperty", _IResolvable_9ceae33e]]=None, service_registries: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ServiceRegistryProperty", _IResolvable_9ceae33e]]]]=None) -> None:
        """Create a new ``AWS::ECS::TaskSet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param cluster: ``AWS::ECS::TaskSet.Cluster``.
        :param service: ``AWS::ECS::TaskSet.Service``.
        :param task_definition: ``AWS::ECS::TaskSet.TaskDefinition``.
        :param external_id: ``AWS::ECS::TaskSet.ExternalId``.
        :param launch_type: ``AWS::ECS::TaskSet.LaunchType``.
        :param load_balancers: ``AWS::ECS::TaskSet.LoadBalancers``.
        :param network_configuration: ``AWS::ECS::TaskSet.NetworkConfiguration``.
        :param platform_version: ``AWS::ECS::TaskSet.PlatformVersion``.
        :param scale: ``AWS::ECS::TaskSet.Scale``.
        :param service_registries: ``AWS::ECS::TaskSet.ServiceRegistries``.
        """
        props = CfnTaskSetProps(cluster=cluster, service=service, task_definition=task_definition, external_id=external_id, launch_type=launch_type, load_balancers=load_balancers, network_configuration=network_configuration, platform_version=platform_version, scale=scale, service_registries=service_registries)

        jsii.create(CfnTaskSet, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnTaskSet":
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
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Id
        """
        return jsii.get(self, "attrId")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> str:
        """``AWS::ECS::TaskSet.Cluster``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskset.html#cfn-ecs-taskset-cluster
        """
        return jsii.get(self, "cluster")

    @cluster.setter
    def cluster(self, value: str) -> None:
        jsii.set(self, "cluster", value)

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> str:
        """``AWS::ECS::TaskSet.Service``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskset.html#cfn-ecs-taskset-service
        """
        return jsii.get(self, "service")

    @service.setter
    def service(self, value: str) -> None:
        jsii.set(self, "service", value)

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> str:
        """``AWS::ECS::TaskSet.TaskDefinition``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskset.html#cfn-ecs-taskset-taskdefinition
        """
        return jsii.get(self, "taskDefinition")

    @task_definition.setter
    def task_definition(self, value: str) -> None:
        jsii.set(self, "taskDefinition", value)

    @builtins.property
    @jsii.member(jsii_name="externalId")
    def external_id(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskSet.ExternalId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskset.html#cfn-ecs-taskset-externalid
        """
        return jsii.get(self, "externalId")

    @external_id.setter
    def external_id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "externalId", value)

    @builtins.property
    @jsii.member(jsii_name="launchType")
    def launch_type(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskSet.LaunchType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskset.html#cfn-ecs-taskset-launchtype
        """
        return jsii.get(self, "launchType")

    @launch_type.setter
    def launch_type(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "launchType", value)

    @builtins.property
    @jsii.member(jsii_name="loadBalancers")
    def load_balancers(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["LoadBalancerProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::ECS::TaskSet.LoadBalancers``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskset.html#cfn-ecs-taskset-loadbalancers
        """
        return jsii.get(self, "loadBalancers")

    @load_balancers.setter
    def load_balancers(self, value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["LoadBalancerProperty", _IResolvable_9ceae33e]]]]) -> None:
        jsii.set(self, "loadBalancers", value)

    @builtins.property
    @jsii.member(jsii_name="networkConfiguration")
    def network_configuration(self) -> typing.Optional[typing.Union["NetworkConfigurationProperty", _IResolvable_9ceae33e]]:
        """``AWS::ECS::TaskSet.NetworkConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskset.html#cfn-ecs-taskset-networkconfiguration
        """
        return jsii.get(self, "networkConfiguration")

    @network_configuration.setter
    def network_configuration(self, value: typing.Optional[typing.Union["NetworkConfigurationProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "networkConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="platformVersion")
    def platform_version(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskSet.PlatformVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskset.html#cfn-ecs-taskset-platformversion
        """
        return jsii.get(self, "platformVersion")

    @platform_version.setter
    def platform_version(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "platformVersion", value)

    @builtins.property
    @jsii.member(jsii_name="scale")
    def scale(self) -> typing.Optional[typing.Union["ScaleProperty", _IResolvable_9ceae33e]]:
        """``AWS::ECS::TaskSet.Scale``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskset.html#cfn-ecs-taskset-scale
        """
        return jsii.get(self, "scale")

    @scale.setter
    def scale(self, value: typing.Optional[typing.Union["ScaleProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "scale", value)

    @builtins.property
    @jsii.member(jsii_name="serviceRegistries")
    def service_registries(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ServiceRegistryProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::ECS::TaskSet.ServiceRegistries``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskset.html#cfn-ecs-taskset-serviceregistries
        """
        return jsii.get(self, "serviceRegistries")

    @service_registries.setter
    def service_registries(self, value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ServiceRegistryProperty", _IResolvable_9ceae33e]]]]) -> None:
        jsii.set(self, "serviceRegistries", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnTaskSet.AwsVpcConfigurationProperty", jsii_struct_bases=[], name_mapping={'subnets': 'subnets', 'assign_public_ip': 'assignPublicIp', 'security_groups': 'securityGroups'})
    class AwsVpcConfigurationProperty():
        def __init__(self, *, subnets: typing.List[str], assign_public_ip: typing.Optional[str]=None, security_groups: typing.Optional[typing.List[str]]=None) -> None:
            """
            :param subnets: ``CfnTaskSet.AwsVpcConfigurationProperty.Subnets``.
            :param assign_public_ip: ``CfnTaskSet.AwsVpcConfigurationProperty.AssignPublicIp``.
            :param security_groups: ``CfnTaskSet.AwsVpcConfigurationProperty.SecurityGroups``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskset-awsvpcconfiguration.html
            """
            self._values = {
                'subnets': subnets,
            }
            if assign_public_ip is not None: self._values["assign_public_ip"] = assign_public_ip
            if security_groups is not None: self._values["security_groups"] = security_groups

        @builtins.property
        def subnets(self) -> typing.List[str]:
            """``CfnTaskSet.AwsVpcConfigurationProperty.Subnets``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskset-awsvpcconfiguration.html#cfn-ecs-taskset-awsvpcconfiguration-subnets
            """
            return self._values.get('subnets')

        @builtins.property
        def assign_public_ip(self) -> typing.Optional[str]:
            """``CfnTaskSet.AwsVpcConfigurationProperty.AssignPublicIp``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskset-awsvpcconfiguration.html#cfn-ecs-taskset-awsvpcconfiguration-assignpublicip
            """
            return self._values.get('assign_public_ip')

        @builtins.property
        def security_groups(self) -> typing.Optional[typing.List[str]]:
            """``CfnTaskSet.AwsVpcConfigurationProperty.SecurityGroups``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskset-awsvpcconfiguration.html#cfn-ecs-taskset-awsvpcconfiguration-securitygroups
            """
            return self._values.get('security_groups')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AwsVpcConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnTaskSet.LoadBalancerProperty", jsii_struct_bases=[], name_mapping={'container_name': 'containerName', 'container_port': 'containerPort', 'load_balancer_name': 'loadBalancerName', 'target_group_arn': 'targetGroupArn'})
    class LoadBalancerProperty():
        def __init__(self, *, container_name: typing.Optional[str]=None, container_port: typing.Optional[jsii.Number]=None, load_balancer_name: typing.Optional[str]=None, target_group_arn: typing.Optional[str]=None) -> None:
            """
            :param container_name: ``CfnTaskSet.LoadBalancerProperty.ContainerName``.
            :param container_port: ``CfnTaskSet.LoadBalancerProperty.ContainerPort``.
            :param load_balancer_name: ``CfnTaskSet.LoadBalancerProperty.LoadBalancerName``.
            :param target_group_arn: ``CfnTaskSet.LoadBalancerProperty.TargetGroupArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskset-loadbalancer.html
            """
            self._values = {
            }
            if container_name is not None: self._values["container_name"] = container_name
            if container_port is not None: self._values["container_port"] = container_port
            if load_balancer_name is not None: self._values["load_balancer_name"] = load_balancer_name
            if target_group_arn is not None: self._values["target_group_arn"] = target_group_arn

        @builtins.property
        def container_name(self) -> typing.Optional[str]:
            """``CfnTaskSet.LoadBalancerProperty.ContainerName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskset-loadbalancer.html#cfn-ecs-taskset-loadbalancer-containername
            """
            return self._values.get('container_name')

        @builtins.property
        def container_port(self) -> typing.Optional[jsii.Number]:
            """``CfnTaskSet.LoadBalancerProperty.ContainerPort``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskset-loadbalancer.html#cfn-ecs-taskset-loadbalancer-containerport
            """
            return self._values.get('container_port')

        @builtins.property
        def load_balancer_name(self) -> typing.Optional[str]:
            """``CfnTaskSet.LoadBalancerProperty.LoadBalancerName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskset-loadbalancer.html#cfn-ecs-taskset-loadbalancer-loadbalancername
            """
            return self._values.get('load_balancer_name')

        @builtins.property
        def target_group_arn(self) -> typing.Optional[str]:
            """``CfnTaskSet.LoadBalancerProperty.TargetGroupArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskset-loadbalancer.html#cfn-ecs-taskset-loadbalancer-targetgrouparn
            """
            return self._values.get('target_group_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LoadBalancerProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnTaskSet.NetworkConfigurationProperty", jsii_struct_bases=[], name_mapping={'aws_vpc_configuration': 'awsVpcConfiguration'})
    class NetworkConfigurationProperty():
        def __init__(self, *, aws_vpc_configuration: typing.Optional[typing.Union["CfnTaskSet.AwsVpcConfigurationProperty", _IResolvable_9ceae33e]]=None) -> None:
            """
            :param aws_vpc_configuration: ``CfnTaskSet.NetworkConfigurationProperty.AwsVpcConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskset-networkconfiguration.html
            """
            self._values = {
            }
            if aws_vpc_configuration is not None: self._values["aws_vpc_configuration"] = aws_vpc_configuration

        @builtins.property
        def aws_vpc_configuration(self) -> typing.Optional[typing.Union["CfnTaskSet.AwsVpcConfigurationProperty", _IResolvable_9ceae33e]]:
            """``CfnTaskSet.NetworkConfigurationProperty.AwsVpcConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskset-networkconfiguration.html#cfn-ecs-taskset-networkconfiguration-awsvpcconfiguration
            """
            return self._values.get('aws_vpc_configuration')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'NetworkConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnTaskSet.ScaleProperty", jsii_struct_bases=[], name_mapping={'unit': 'unit', 'value': 'value'})
    class ScaleProperty():
        def __init__(self, *, unit: typing.Optional[str]=None, value: typing.Optional[jsii.Number]=None) -> None:
            """
            :param unit: ``CfnTaskSet.ScaleProperty.Unit``.
            :param value: ``CfnTaskSet.ScaleProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskset-scale.html
            """
            self._values = {
            }
            if unit is not None: self._values["unit"] = unit
            if value is not None: self._values["value"] = value

        @builtins.property
        def unit(self) -> typing.Optional[str]:
            """``CfnTaskSet.ScaleProperty.Unit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskset-scale.html#cfn-ecs-taskset-scale-unit
            """
            return self._values.get('unit')

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            """``CfnTaskSet.ScaleProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskset-scale.html#cfn-ecs-taskset-scale-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ScaleProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnTaskSet.ServiceRegistryProperty", jsii_struct_bases=[], name_mapping={'container_name': 'containerName', 'container_port': 'containerPort', 'port': 'port', 'registry_arn': 'registryArn'})
    class ServiceRegistryProperty():
        def __init__(self, *, container_name: typing.Optional[str]=None, container_port: typing.Optional[jsii.Number]=None, port: typing.Optional[jsii.Number]=None, registry_arn: typing.Optional[str]=None) -> None:
            """
            :param container_name: ``CfnTaskSet.ServiceRegistryProperty.ContainerName``.
            :param container_port: ``CfnTaskSet.ServiceRegistryProperty.ContainerPort``.
            :param port: ``CfnTaskSet.ServiceRegistryProperty.Port``.
            :param registry_arn: ``CfnTaskSet.ServiceRegistryProperty.RegistryArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskset-serviceregistry.html
            """
            self._values = {
            }
            if container_name is not None: self._values["container_name"] = container_name
            if container_port is not None: self._values["container_port"] = container_port
            if port is not None: self._values["port"] = port
            if registry_arn is not None: self._values["registry_arn"] = registry_arn

        @builtins.property
        def container_name(self) -> typing.Optional[str]:
            """``CfnTaskSet.ServiceRegistryProperty.ContainerName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskset-serviceregistry.html#cfn-ecs-taskset-serviceregistry-containername
            """
            return self._values.get('container_name')

        @builtins.property
        def container_port(self) -> typing.Optional[jsii.Number]:
            """``CfnTaskSet.ServiceRegistryProperty.ContainerPort``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskset-serviceregistry.html#cfn-ecs-taskset-serviceregistry-containerport
            """
            return self._values.get('container_port')

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            """``CfnTaskSet.ServiceRegistryProperty.Port``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskset-serviceregistry.html#cfn-ecs-taskset-serviceregistry-port
            """
            return self._values.get('port')

        @builtins.property
        def registry_arn(self) -> typing.Optional[str]:
            """``CfnTaskSet.ServiceRegistryProperty.RegistryArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskset-serviceregistry.html#cfn-ecs-taskset-serviceregistry-registryarn
            """
            return self._values.get('registry_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ServiceRegistryProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CfnTaskSetProps", jsii_struct_bases=[], name_mapping={'cluster': 'cluster', 'service': 'service', 'task_definition': 'taskDefinition', 'external_id': 'externalId', 'launch_type': 'launchType', 'load_balancers': 'loadBalancers', 'network_configuration': 'networkConfiguration', 'platform_version': 'platformVersion', 'scale': 'scale', 'service_registries': 'serviceRegistries'})
class CfnTaskSetProps():
    def __init__(self, *, cluster: str, service: str, task_definition: str, external_id: typing.Optional[str]=None, launch_type: typing.Optional[str]=None, load_balancers: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskSet.LoadBalancerProperty", _IResolvable_9ceae33e]]]]=None, network_configuration: typing.Optional[typing.Union["CfnTaskSet.NetworkConfigurationProperty", _IResolvable_9ceae33e]]=None, platform_version: typing.Optional[str]=None, scale: typing.Optional[typing.Union["CfnTaskSet.ScaleProperty", _IResolvable_9ceae33e]]=None, service_registries: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskSet.ServiceRegistryProperty", _IResolvable_9ceae33e]]]]=None) -> None:
        """Properties for defining a ``AWS::ECS::TaskSet``.

        :param cluster: ``AWS::ECS::TaskSet.Cluster``.
        :param service: ``AWS::ECS::TaskSet.Service``.
        :param task_definition: ``AWS::ECS::TaskSet.TaskDefinition``.
        :param external_id: ``AWS::ECS::TaskSet.ExternalId``.
        :param launch_type: ``AWS::ECS::TaskSet.LaunchType``.
        :param load_balancers: ``AWS::ECS::TaskSet.LoadBalancers``.
        :param network_configuration: ``AWS::ECS::TaskSet.NetworkConfiguration``.
        :param platform_version: ``AWS::ECS::TaskSet.PlatformVersion``.
        :param scale: ``AWS::ECS::TaskSet.Scale``.
        :param service_registries: ``AWS::ECS::TaskSet.ServiceRegistries``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskset.html
        """
        self._values = {
            'cluster': cluster,
            'service': service,
            'task_definition': task_definition,
        }
        if external_id is not None: self._values["external_id"] = external_id
        if launch_type is not None: self._values["launch_type"] = launch_type
        if load_balancers is not None: self._values["load_balancers"] = load_balancers
        if network_configuration is not None: self._values["network_configuration"] = network_configuration
        if platform_version is not None: self._values["platform_version"] = platform_version
        if scale is not None: self._values["scale"] = scale
        if service_registries is not None: self._values["service_registries"] = service_registries

    @builtins.property
    def cluster(self) -> str:
        """``AWS::ECS::TaskSet.Cluster``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskset.html#cfn-ecs-taskset-cluster
        """
        return self._values.get('cluster')

    @builtins.property
    def service(self) -> str:
        """``AWS::ECS::TaskSet.Service``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskset.html#cfn-ecs-taskset-service
        """
        return self._values.get('service')

    @builtins.property
    def task_definition(self) -> str:
        """``AWS::ECS::TaskSet.TaskDefinition``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskset.html#cfn-ecs-taskset-taskdefinition
        """
        return self._values.get('task_definition')

    @builtins.property
    def external_id(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskSet.ExternalId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskset.html#cfn-ecs-taskset-externalid
        """
        return self._values.get('external_id')

    @builtins.property
    def launch_type(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskSet.LaunchType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskset.html#cfn-ecs-taskset-launchtype
        """
        return self._values.get('launch_type')

    @builtins.property
    def load_balancers(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskSet.LoadBalancerProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::ECS::TaskSet.LoadBalancers``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskset.html#cfn-ecs-taskset-loadbalancers
        """
        return self._values.get('load_balancers')

    @builtins.property
    def network_configuration(self) -> typing.Optional[typing.Union["CfnTaskSet.NetworkConfigurationProperty", _IResolvable_9ceae33e]]:
        """``AWS::ECS::TaskSet.NetworkConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskset.html#cfn-ecs-taskset-networkconfiguration
        """
        return self._values.get('network_configuration')

    @builtins.property
    def platform_version(self) -> typing.Optional[str]:
        """``AWS::ECS::TaskSet.PlatformVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskset.html#cfn-ecs-taskset-platformversion
        """
        return self._values.get('platform_version')

    @builtins.property
    def scale(self) -> typing.Optional[typing.Union["CfnTaskSet.ScaleProperty", _IResolvable_9ceae33e]]:
        """``AWS::ECS::TaskSet.Scale``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskset.html#cfn-ecs-taskset-scale
        """
        return self._values.get('scale')

    @builtins.property
    def service_registries(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnTaskSet.ServiceRegistryProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::ECS::TaskSet.ServiceRegistries``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskset.html#cfn-ecs-taskset-serviceregistries
        """
        return self._values.get('service_registries')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnTaskSetProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CloudMapNamespaceOptions", jsii_struct_bases=[], name_mapping={'name': 'name', 'type': 'type', 'vpc': 'vpc'})
class CloudMapNamespaceOptions():
    def __init__(self, *, name: str, type: typing.Optional[_NamespaceType_df1ca402]=None, vpc: typing.Optional[_IVpc_3795853f]=None) -> None:
        """The options for creating an AWS Cloud Map namespace.

        :param name: The name of the namespace, such as example.com.
        :param type: The type of CloudMap Namespace to create. Default: PrivateDns
        :param vpc: The VPC to associate the namespace with. This property is required for private DNS namespaces. Default: VPC of the cluster for Private DNS Namespace, otherwise none

        stability
        :stability: experimental
        """
        self._values = {
            'name': name,
        }
        if type is not None: self._values["type"] = type
        if vpc is not None: self._values["vpc"] = vpc

    @builtins.property
    def name(self) -> str:
        """The name of the namespace, such as example.com.

        stability
        :stability: experimental
        """
        return self._values.get('name')

    @builtins.property
    def type(self) -> typing.Optional[_NamespaceType_df1ca402]:
        """The type of CloudMap Namespace to create.

        default
        :default: PrivateDns

        stability
        :stability: experimental
        """
        return self._values.get('type')

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """The VPC to associate the namespace with.

        This property is required for private DNS namespaces.

        default
        :default: VPC of the cluster for Private DNS Namespace, otherwise none

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CloudMapNamespaceOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CloudMapOptions", jsii_struct_bases=[], name_mapping={'cloud_map_namespace': 'cloudMapNamespace', 'dns_record_type': 'dnsRecordType', 'dns_ttl': 'dnsTtl', 'failure_threshold': 'failureThreshold', 'name': 'name'})
class CloudMapOptions():
    def __init__(self, *, cloud_map_namespace: typing.Optional[_INamespace_2b56a022]=None, dns_record_type: typing.Optional[_DnsRecordType_acb5afbb]=None, dns_ttl: typing.Optional[_Duration_5170c158]=None, failure_threshold: typing.Optional[jsii.Number]=None, name: typing.Optional[str]=None) -> None:
        """The options to enabling AWS Cloud Map for an Amazon ECS service.

        :param cloud_map_namespace: The service discovery namespace for the Cloud Map service to attach to the ECS service. Default: - the defaultCloudMapNamespace associated to the cluster
        :param dns_record_type: The DNS record type that you want AWS Cloud Map to create. The supported record types are A or SRV. Default: DnsRecordType.A
        :param dns_ttl: The amount of time that you want DNS resolvers to cache the settings for this record. Default: 60
        :param failure_threshold: The number of 30-second intervals that you want Cloud Map to wait after receiving an UpdateInstanceCustomHealthStatus request before it changes the health status of a service instance. NOTE: This is used for HealthCheckCustomConfig
        :param name: The name of the Cloud Map service to attach to the ECS service. Default: CloudFormation-generated name

        stability
        :stability: experimental
        """
        self._values = {
        }
        if cloud_map_namespace is not None: self._values["cloud_map_namespace"] = cloud_map_namespace
        if dns_record_type is not None: self._values["dns_record_type"] = dns_record_type
        if dns_ttl is not None: self._values["dns_ttl"] = dns_ttl
        if failure_threshold is not None: self._values["failure_threshold"] = failure_threshold
        if name is not None: self._values["name"] = name

    @builtins.property
    def cloud_map_namespace(self) -> typing.Optional[_INamespace_2b56a022]:
        """The service discovery namespace for the Cloud Map service to attach to the ECS service.

        default
        :default: - the defaultCloudMapNamespace associated to the cluster

        stability
        :stability: experimental
        """
        return self._values.get('cloud_map_namespace')

    @builtins.property
    def dns_record_type(self) -> typing.Optional[_DnsRecordType_acb5afbb]:
        """The DNS record type that you want AWS Cloud Map to create.

        The supported record types are A or SRV.

        default
        :default: DnsRecordType.A

        stability
        :stability: experimental
        """
        return self._values.get('dns_record_type')

    @builtins.property
    def dns_ttl(self) -> typing.Optional[_Duration_5170c158]:
        """The amount of time that you want DNS resolvers to cache the settings for this record.

        default
        :default: 60

        stability
        :stability: experimental
        """
        return self._values.get('dns_ttl')

    @builtins.property
    def failure_threshold(self) -> typing.Optional[jsii.Number]:
        """The number of 30-second intervals that you want Cloud Map to wait after receiving an UpdateInstanceCustomHealthStatus request before it changes the health status of a service instance.

        NOTE: This is used for HealthCheckCustomConfig

        stability
        :stability: experimental
        """
        return self._values.get('failure_threshold')

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """The name of the Cloud Map service to attach to the ECS service.

        default
        :default: CloudFormation-generated name

        stability
        :stability: experimental
        """
        return self._values.get('name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CloudMapOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.ClusterAttributes", jsii_struct_bases=[], name_mapping={'cluster_name': 'clusterName', 'security_groups': 'securityGroups', 'vpc': 'vpc', 'autoscaling_group': 'autoscalingGroup', 'cluster_arn': 'clusterArn', 'default_cloud_map_namespace': 'defaultCloudMapNamespace', 'has_ec2_capacity': 'hasEc2Capacity'})
class ClusterAttributes():
    def __init__(self, *, cluster_name: str, security_groups: typing.List[_ISecurityGroup_d72ab8e8], vpc: _IVpc_3795853f, autoscaling_group: typing.Optional[_IAutoScalingGroup_a753dc94]=None, cluster_arn: typing.Optional[str]=None, default_cloud_map_namespace: typing.Optional[_INamespace_2b56a022]=None, has_ec2_capacity: typing.Optional[bool]=None) -> None:
        """The properties to import from the ECS cluster.

        :param cluster_name: The name of the cluster.
        :param security_groups: The security groups associated with the container instances registered to the cluster.
        :param vpc: The VPC associated with the cluster.
        :param autoscaling_group: Autoscaling group added to the cluster if capacity is added. Default: - No default autoscaling group
        :param cluster_arn: The Amazon Resource Name (ARN) that identifies the cluster. Default: Derived from clusterName
        :param default_cloud_map_namespace: The AWS Cloud Map namespace to associate with the cluster. Default: - No default namespace
        :param has_ec2_capacity: Specifies whether the cluster has EC2 instance capacity. Default: true

        stability
        :stability: experimental
        """
        self._values = {
            'cluster_name': cluster_name,
            'security_groups': security_groups,
            'vpc': vpc,
        }
        if autoscaling_group is not None: self._values["autoscaling_group"] = autoscaling_group
        if cluster_arn is not None: self._values["cluster_arn"] = cluster_arn
        if default_cloud_map_namespace is not None: self._values["default_cloud_map_namespace"] = default_cloud_map_namespace
        if has_ec2_capacity is not None: self._values["has_ec2_capacity"] = has_ec2_capacity

    @builtins.property
    def cluster_name(self) -> str:
        """The name of the cluster.

        stability
        :stability: experimental
        """
        return self._values.get('cluster_name')

    @builtins.property
    def security_groups(self) -> typing.List[_ISecurityGroup_d72ab8e8]:
        """The security groups associated with the container instances registered to the cluster.

        stability
        :stability: experimental
        """
        return self._values.get('security_groups')

    @builtins.property
    def vpc(self) -> _IVpc_3795853f:
        """The VPC associated with the cluster.

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    @builtins.property
    def autoscaling_group(self) -> typing.Optional[_IAutoScalingGroup_a753dc94]:
        """Autoscaling group added to the cluster if capacity is added.

        default
        :default: - No default autoscaling group

        stability
        :stability: experimental
        """
        return self._values.get('autoscaling_group')

    @builtins.property
    def cluster_arn(self) -> typing.Optional[str]:
        """The Amazon Resource Name (ARN) that identifies the cluster.

        default
        :default: Derived from clusterName

        stability
        :stability: experimental
        """
        return self._values.get('cluster_arn')

    @builtins.property
    def default_cloud_map_namespace(self) -> typing.Optional[_INamespace_2b56a022]:
        """The AWS Cloud Map namespace to associate with the cluster.

        default
        :default: - No default namespace

        stability
        :stability: experimental
        """
        return self._values.get('default_cloud_map_namespace')

    @builtins.property
    def has_ec2_capacity(self) -> typing.Optional[bool]:
        """Specifies whether the cluster has EC2 instance capacity.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('has_ec2_capacity')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ClusterAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.ClusterProps", jsii_struct_bases=[], name_mapping={'capacity': 'capacity', 'cluster_name': 'clusterName', 'container_insights': 'containerInsights', 'default_cloud_map_namespace': 'defaultCloudMapNamespace', 'vpc': 'vpc'})
class ClusterProps():
    def __init__(self, *, capacity: typing.Optional["AddCapacityOptions"]=None, cluster_name: typing.Optional[str]=None, container_insights: typing.Optional[bool]=None, default_cloud_map_namespace: typing.Optional["CloudMapNamespaceOptions"]=None, vpc: typing.Optional[_IVpc_3795853f]=None) -> None:
        """The properties used to define an ECS cluster.

        :param capacity: The ec2 capacity to add to the cluster. Default: - no EC2 capacity will be added, you can use ``addCapacity`` to add capacity later.
        :param cluster_name: The name for the cluster. Default: CloudFormation-generated name
        :param container_insights: If true CloudWatch Container Insights will be enabled for the cluster. Default: - Container Insights will be disabled for this cluser.
        :param default_cloud_map_namespace: The service discovery namespace created in this cluster. Default: - no service discovery namespace created, you can use ``addDefaultCloudMapNamespace`` to add a default service discovery namespace later.
        :param vpc: The VPC where your ECS instances will be running or your ENIs will be deployed. Default: - creates a new VPC with two AZs

        stability
        :stability: experimental
        """
        if isinstance(capacity, dict): capacity = AddCapacityOptions(**capacity)
        if isinstance(default_cloud_map_namespace, dict): default_cloud_map_namespace = CloudMapNamespaceOptions(**default_cloud_map_namespace)
        self._values = {
        }
        if capacity is not None: self._values["capacity"] = capacity
        if cluster_name is not None: self._values["cluster_name"] = cluster_name
        if container_insights is not None: self._values["container_insights"] = container_insights
        if default_cloud_map_namespace is not None: self._values["default_cloud_map_namespace"] = default_cloud_map_namespace
        if vpc is not None: self._values["vpc"] = vpc

    @builtins.property
    def capacity(self) -> typing.Optional["AddCapacityOptions"]:
        """The ec2 capacity to add to the cluster.

        default
        :default: - no EC2 capacity will be added, you can use ``addCapacity`` to add capacity later.

        stability
        :stability: experimental
        """
        return self._values.get('capacity')

    @builtins.property
    def cluster_name(self) -> typing.Optional[str]:
        """The name for the cluster.

        default
        :default: CloudFormation-generated name

        stability
        :stability: experimental
        """
        return self._values.get('cluster_name')

    @builtins.property
    def container_insights(self) -> typing.Optional[bool]:
        """If true CloudWatch Container Insights will be enabled for the cluster.

        default
        :default: - Container Insights will be disabled for this cluser.

        stability
        :stability: experimental
        """
        return self._values.get('container_insights')

    @builtins.property
    def default_cloud_map_namespace(self) -> typing.Optional["CloudMapNamespaceOptions"]:
        """The service discovery namespace created in this cluster.

        default
        :default:

        - no service discovery namespace created, you can use ``addDefaultCloudMapNamespace`` to add a
          default service discovery namespace later.

        stability
        :stability: experimental
        """
        return self._values.get('default_cloud_map_namespace')

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """The VPC where your ECS instances will be running or your ENIs will be deployed.

        default
        :default: - creates a new VPC with two AZs

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ClusterProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CommonTaskDefinitionProps", jsii_struct_bases=[], name_mapping={'execution_role': 'executionRole', 'family': 'family', 'proxy_configuration': 'proxyConfiguration', 'task_role': 'taskRole', 'volumes': 'volumes'})
class CommonTaskDefinitionProps():
    def __init__(self, *, execution_role: typing.Optional[_IRole_e69bbae4]=None, family: typing.Optional[str]=None, proxy_configuration: typing.Optional["ProxyConfiguration"]=None, task_role: typing.Optional[_IRole_e69bbae4]=None, volumes: typing.Optional[typing.List["Volume"]]=None) -> None:
        """The common properties for all task definitions.

        For more information, see
        `Task Definition Parameters <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definition_parameters.html>`_.

        :param execution_role: The name of the IAM task execution role that grants the ECS agent to call AWS APIs on your behalf. The role will be used to retrieve container images from ECR and create CloudWatch log groups. Default: - An execution role will be automatically created if you use ECR images in your task definition.
        :param family: The name of a family that this task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param proxy_configuration: The configuration details for the App Mesh proxy. Default: - No proxy configuration.
        :param task_role: The name of the IAM role that grants containers in the task permission to call AWS APIs on your behalf. Default: - A task role is automatically created for you.
        :param volumes: The list of volume definitions for the task. For more information, see `Task Definition Parameter Volumes <https://docs.aws.amazon.com/AmazonECS/latest/developerguide//task_definition_parameters.html#volumes>`_. Default: - No volumes are passed to the Docker daemon on a container instance.

        stability
        :stability: experimental
        """
        self._values = {
        }
        if execution_role is not None: self._values["execution_role"] = execution_role
        if family is not None: self._values["family"] = family
        if proxy_configuration is not None: self._values["proxy_configuration"] = proxy_configuration
        if task_role is not None: self._values["task_role"] = task_role
        if volumes is not None: self._values["volumes"] = volumes

    @builtins.property
    def execution_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The name of the IAM task execution role that grants the ECS agent to call AWS APIs on your behalf.

        The role will be used to retrieve container images from ECR and create CloudWatch log groups.

        default
        :default: - An execution role will be automatically created if you use ECR images in your task definition.

        stability
        :stability: experimental
        """
        return self._values.get('execution_role')

    @builtins.property
    def family(self) -> typing.Optional[str]:
        """The name of a family that this task definition is registered to.

        A family groups multiple versions of a task definition.

        default
        :default: - Automatically generated name.

        stability
        :stability: experimental
        """
        return self._values.get('family')

    @builtins.property
    def proxy_configuration(self) -> typing.Optional["ProxyConfiguration"]:
        """The configuration details for the App Mesh proxy.

        default
        :default: - No proxy configuration.

        stability
        :stability: experimental
        """
        return self._values.get('proxy_configuration')

    @builtins.property
    def task_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The name of the IAM role that grants containers in the task permission to call AWS APIs on your behalf.

        default
        :default: - A task role is automatically created for you.

        stability
        :stability: experimental
        """
        return self._values.get('task_role')

    @builtins.property
    def volumes(self) -> typing.Optional[typing.List["Volume"]]:
        """The list of volume definitions for the task.

        For more information, see
        `Task Definition Parameter Volumes <https://docs.aws.amazon.com/AmazonECS/latest/developerguide//task_definition_parameters.html#volumes>`_.

        default
        :default: - No volumes are passed to the Docker daemon on a container instance.

        stability
        :stability: experimental
        """
        return self._values.get('volumes')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CommonTaskDefinitionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.aws_ecs.Compatibility")
class Compatibility(enum.Enum):
    """The task launch type compatibility requirement.

    stability
    :stability: experimental
    """
    EC2 = "EC2"
    """The task should specify the EC2 launch type.

    stability
    :stability: experimental
    """
    FARGATE = "FARGATE"
    """The task should specify the Fargate launch type.

    stability
    :stability: experimental
    """
    EC2_AND_FARGATE = "EC2_AND_FARGATE"
    """The task can specify either the EC2 or Fargate launch types.

    stability
    :stability: experimental
    """

class ContainerDefinition(_Construct_f50a3f53, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs.ContainerDefinition"):
    """A container definition is used in a task definition to describe the containers that are launched as part of a task.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, task_definition: "TaskDefinition", image: "ContainerImage", command: typing.Optional[typing.List[str]]=None, cpu: typing.Optional[jsii.Number]=None, disable_networking: typing.Optional[bool]=None, dns_search_domains: typing.Optional[typing.List[str]]=None, dns_servers: typing.Optional[typing.List[str]]=None, docker_labels: typing.Optional[typing.Mapping[str, str]]=None, docker_security_options: typing.Optional[typing.List[str]]=None, entry_point: typing.Optional[typing.List[str]]=None, environment: typing.Optional[typing.Mapping[str, str]]=None, essential: typing.Optional[bool]=None, extra_hosts: typing.Optional[typing.Mapping[str, str]]=None, gpu_count: typing.Optional[jsii.Number]=None, health_check: typing.Optional["HealthCheck"]=None, hostname: typing.Optional[str]=None, linux_parameters: typing.Optional["LinuxParameters"]=None, logging: typing.Optional["LogDriver"]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None, privileged: typing.Optional[bool]=None, readonly_root_filesystem: typing.Optional[bool]=None, secrets: typing.Optional[typing.Mapping[str, "Secret"]]=None, start_timeout: typing.Optional[_Duration_5170c158]=None, stop_timeout: typing.Optional[_Duration_5170c158]=None, user: typing.Optional[str]=None, working_directory: typing.Optional[str]=None) -> None:
        """Constructs a new instance of the ContainerDefinition class.

        :param scope: -
        :param id: -
        :param task_definition: The name of the task definition that includes this container definition. [disable-awslint:ref-via-interface]
        :param image: The image used to start a container. This string is passed directly to the Docker daemon. Images in the Docker Hub registry are available by default. Other repositories are specified with either repository-url/image:tag or repository-url/image@digest. TODO: Update these to specify using classes of IContainerImage
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param cpu: The minimum number of CPU units to reserve for the container. Default: - No minimum CPU units reserved.
        :param disable_networking: Specifies whether networking is disabled within the container. When this parameter is true, networking is disabled within the container. Default: false
        :param dns_search_domains: A list of DNS search domains that are presented to the container. Default: - No search domains.
        :param dns_servers: A list of DNS servers that are presented to the container. Default: - Default DNS servers.
        :param docker_labels: A key/value map of labels to add to the container. Default: - No labels.
        :param docker_security_options: A list of strings to provide custom labels for SELinux and AppArmor multi-level security systems. Default: - No security labels.
        :param entry_point: The ENTRYPOINT value to pass to the container. Default: - Entry point configured in container.
        :param environment: The environment variables to pass to the container. Default: - No environment variables.
        :param essential: Specifies whether the container is marked essential. If the essential parameter of a container is marked as true, and that container fails or stops for any reason, all other containers that are part of the task are stopped. If the essential parameter of a container is marked as false, then its failure does not affect the rest of the containers in a task. All tasks must have at least one essential container. If this parameter is omitted, a container is assumed to be essential. Default: true
        :param extra_hosts: A list of hostnames and IP address mappings to append to the /etc/hosts file on the container. Default: - No extra hosts.
        :param gpu_count: The number of GPUs assigned to the container. Default: - No GPUs assigned.
        :param health_check: The health check command and associated configuration parameters for the container. Default: - Health check configuration from container.
        :param hostname: The hostname to use for your container. Default: - Automatic hostname.
        :param linux_parameters: Linux-specific modifications that are applied to the container, such as Linux kernel capabilities. For more information see `KernelCapabilities <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_KernelCapabilities.html>`_. Default: - No Linux parameters.
        :param logging: The log configuration specification for the container. Default: - Containers use the same logging driver that the Docker daemon uses.
        :param memory_limit_mib: The amount (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under heavy contention, Docker attempts to keep the container memory to this soft limit. However, your container can consume more memory when it needs to, up to either the hard limit specified with the memory parameter (if applicable), or all of the available memory on the container instance, whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory reserved.
        :param privileged: Specifies whether the container is marked as privileged. When this parameter is true, the container is given elevated privileges on the host container instance (similar to the root user). Default: false
        :param readonly_root_filesystem: When this parameter is true, the container is given read-only access to its root file system. Default: false
        :param secrets: The secret environment variables to pass to the container. Default: - No secret environment variables.
        :param start_timeout: Time duration (in seconds) to wait before giving up on resolving dependencies for a container. Default: - none
        :param stop_timeout: Time duration (in seconds) to wait before the container is forcefully killed if it doesn't exit normally on its own. Default: - none
        :param user: The user name to use inside the container. Default: root
        :param working_directory: The working directory in which to run commands inside the container. Default: /

        stability
        :stability: experimental
        """
        props = ContainerDefinitionProps(task_definition=task_definition, image=image, command=command, cpu=cpu, disable_networking=disable_networking, dns_search_domains=dns_search_domains, dns_servers=dns_servers, docker_labels=docker_labels, docker_security_options=docker_security_options, entry_point=entry_point, environment=environment, essential=essential, extra_hosts=extra_hosts, gpu_count=gpu_count, health_check=health_check, hostname=hostname, linux_parameters=linux_parameters, logging=logging, memory_limit_mib=memory_limit_mib, memory_reservation_mib=memory_reservation_mib, privileged=privileged, readonly_root_filesystem=readonly_root_filesystem, secrets=secrets, start_timeout=start_timeout, stop_timeout=stop_timeout, user=user, working_directory=working_directory)

        jsii.create(ContainerDefinition, self, [scope, id, props])

    @jsii.member(jsii_name="addContainerDependencies")
    def add_container_dependencies(self, *container_dependencies: "ContainerDependency") -> None:
        """This method adds one or more container dependencies to the container.

        :param container_dependencies: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addContainerDependencies", [*container_dependencies])

    @jsii.member(jsii_name="addLink")
    def add_link(self, container: "ContainerDefinition", alias: typing.Optional[str]=None) -> None:
        """This method adds a link which allows containers to communicate with each other without the need for port mappings.

        This parameter is only supported if the task definition is using the bridge network mode.
        Warning: The --link flag is a legacy feature of Docker. It may eventually be removed.

        :param container: -
        :param alias: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addLink", [container, alias])

    @jsii.member(jsii_name="addMountPoints")
    def add_mount_points(self, *mount_points: "MountPoint") -> None:
        """This method adds one or more mount points for data volumes to the container.

        :param mount_points: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addMountPoints", [*mount_points])

    @jsii.member(jsii_name="addPortMappings")
    def add_port_mappings(self, *port_mappings: "PortMapping") -> None:
        """This method adds one or more port mappings to the container.

        :param port_mappings: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addPortMappings", [*port_mappings])

    @jsii.member(jsii_name="addScratch")
    def add_scratch(self, *, container_path: str, name: str, read_only: bool, source_path: str) -> None:
        """This method mounts temporary disk space to the container.

        This adds the correct container mountPoint and task definition volume.

        :param container_path: The path on the container to mount the scratch volume at.
        :param name: The name of the scratch volume to mount. Must be a volume name referenced in the name parameter of task definition volume.
        :param read_only: Specifies whether to give the container read-only access to the scratch volume. If this value is true, the container has read-only access to the scratch volume. If this value is false, then the container can write to the scratch volume.
        :param source_path: 

        stability
        :stability: experimental
        """
        scratch = ScratchSpace(container_path=container_path, name=name, read_only=read_only, source_path=source_path)

        return jsii.invoke(self, "addScratch", [scratch])

    @jsii.member(jsii_name="addToExecutionPolicy")
    def add_to_execution_policy(self, statement: _PolicyStatement_f75dc775) -> None:
        """This method adds the specified statement to the IAM task execution policy in the task definition.

        :param statement: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addToExecutionPolicy", [statement])

    @jsii.member(jsii_name="addUlimits")
    def add_ulimits(self, *ulimits: "Ulimit") -> None:
        """This method adds one or more ulimits to the container.

        :param ulimits: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addUlimits", [*ulimits])

    @jsii.member(jsii_name="addVolumesFrom")
    def add_volumes_from(self, *volumes_from: "VolumeFrom") -> None:
        """This method adds one or more volumes to the container.

        :param volumes_from: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addVolumesFrom", [*volumes_from])

    @jsii.member(jsii_name="findPortMapping")
    def find_port_mapping(self, container_port: jsii.Number, protocol: "Protocol") -> typing.Optional["PortMapping"]:
        """Returns the host port for the requested container port if it exists.

        :param container_port: -
        :param protocol: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "findPortMapping", [container_port, protocol])

    @jsii.member(jsii_name="renderContainerDefinition")
    def render_container_definition(self, _task_definition: typing.Optional["TaskDefinition"]=None) -> "CfnTaskDefinition.ContainerDefinitionProperty":
        """Render this container definition to a CloudFormation object.

        :param _task_definition: [disable-awslint:ref-via-interface] (unused but kept to avoid breaking change).

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "renderContainerDefinition", [_task_definition])

    @builtins.property
    @jsii.member(jsii_name="containerDependencies")
    def container_dependencies(self) -> typing.List["ContainerDependency"]:
        """An array dependencies defined for container startup and shutdown.

        stability
        :stability: experimental
        """
        return jsii.get(self, "containerDependencies")

    @builtins.property
    @jsii.member(jsii_name="containerName")
    def container_name(self) -> str:
        """The name of this container.

        stability
        :stability: experimental
        """
        return jsii.get(self, "containerName")

    @builtins.property
    @jsii.member(jsii_name="containerPort")
    def container_port(self) -> jsii.Number:
        """The port the container will listen on.

        stability
        :stability: experimental
        """
        return jsii.get(self, "containerPort")

    @builtins.property
    @jsii.member(jsii_name="essential")
    def essential(self) -> bool:
        """Specifies whether the container will be marked essential.

        If the essential parameter of a container is marked as true, and that container
        fails or stops for any reason, all other containers that are part of the task are
        stopped. If the essential parameter of a container is marked as false, then its
        failure does not affect the rest of the containers in a task.

        If this parameter isomitted, a container is assumed to be essential.

        stability
        :stability: experimental
        """
        return jsii.get(self, "essential")

    @builtins.property
    @jsii.member(jsii_name="ingressPort")
    def ingress_port(self) -> jsii.Number:
        """The inbound rules associated with the security group the task or service will use.

        This property is only used for tasks that use the awsvpc network mode.

        stability
        :stability: experimental
        """
        return jsii.get(self, "ingressPort")

    @builtins.property
    @jsii.member(jsii_name="memoryLimitSpecified")
    def memory_limit_specified(self) -> bool:
        """Whether there was at least one memory limit specified in this definition.

        stability
        :stability: experimental
        """
        return jsii.get(self, "memoryLimitSpecified")

    @builtins.property
    @jsii.member(jsii_name="mountPoints")
    def mount_points(self) -> typing.List["MountPoint"]:
        """The mount points for data volumes in your container.

        stability
        :stability: experimental
        """
        return jsii.get(self, "mountPoints")

    @builtins.property
    @jsii.member(jsii_name="portMappings")
    def port_mappings(self) -> typing.List["PortMapping"]:
        """The list of port mappings for the container.

        Port mappings allow containers to access ports
        on the host container instance to send or receive traffic.

        stability
        :stability: experimental
        """
        return jsii.get(self, "portMappings")

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> "TaskDefinition":
        """The name of the task definition that includes this container definition.

        stability
        :stability: experimental
        """
        return jsii.get(self, "taskDefinition")

    @builtins.property
    @jsii.member(jsii_name="ulimits")
    def ulimits(self) -> typing.List["Ulimit"]:
        """An array of ulimits to set in the container.

        stability
        :stability: experimental
        """
        return jsii.get(self, "ulimits")

    @builtins.property
    @jsii.member(jsii_name="volumesFrom")
    def volumes_from(self) -> typing.List["VolumeFrom"]:
        """The data volumes to mount from another container in the same task definition.

        stability
        :stability: experimental
        """
        return jsii.get(self, "volumesFrom")

    @builtins.property
    @jsii.member(jsii_name="linuxParameters")
    def linux_parameters(self) -> typing.Optional["LinuxParameters"]:
        """The Linux-specific modifications that are applied to the container, such as Linux kernel capabilities.

        stability
        :stability: experimental
        """
        return jsii.get(self, "linuxParameters")

    @builtins.property
    @jsii.member(jsii_name="logDriverConfig")
    def log_driver_config(self) -> typing.Optional["LogDriverConfig"]:
        """The log configuration specification for the container.

        stability
        :stability: experimental
        """
        return jsii.get(self, "logDriverConfig")


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.ContainerDefinitionOptions", jsii_struct_bases=[], name_mapping={'image': 'image', 'command': 'command', 'cpu': 'cpu', 'disable_networking': 'disableNetworking', 'dns_search_domains': 'dnsSearchDomains', 'dns_servers': 'dnsServers', 'docker_labels': 'dockerLabels', 'docker_security_options': 'dockerSecurityOptions', 'entry_point': 'entryPoint', 'environment': 'environment', 'essential': 'essential', 'extra_hosts': 'extraHosts', 'gpu_count': 'gpuCount', 'health_check': 'healthCheck', 'hostname': 'hostname', 'linux_parameters': 'linuxParameters', 'logging': 'logging', 'memory_limit_mib': 'memoryLimitMiB', 'memory_reservation_mib': 'memoryReservationMiB', 'privileged': 'privileged', 'readonly_root_filesystem': 'readonlyRootFilesystem', 'secrets': 'secrets', 'start_timeout': 'startTimeout', 'stop_timeout': 'stopTimeout', 'user': 'user', 'working_directory': 'workingDirectory'})
class ContainerDefinitionOptions():
    def __init__(self, *, image: "ContainerImage", command: typing.Optional[typing.List[str]]=None, cpu: typing.Optional[jsii.Number]=None, disable_networking: typing.Optional[bool]=None, dns_search_domains: typing.Optional[typing.List[str]]=None, dns_servers: typing.Optional[typing.List[str]]=None, docker_labels: typing.Optional[typing.Mapping[str, str]]=None, docker_security_options: typing.Optional[typing.List[str]]=None, entry_point: typing.Optional[typing.List[str]]=None, environment: typing.Optional[typing.Mapping[str, str]]=None, essential: typing.Optional[bool]=None, extra_hosts: typing.Optional[typing.Mapping[str, str]]=None, gpu_count: typing.Optional[jsii.Number]=None, health_check: typing.Optional["HealthCheck"]=None, hostname: typing.Optional[str]=None, linux_parameters: typing.Optional["LinuxParameters"]=None, logging: typing.Optional["LogDriver"]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None, privileged: typing.Optional[bool]=None, readonly_root_filesystem: typing.Optional[bool]=None, secrets: typing.Optional[typing.Mapping[str, "Secret"]]=None, start_timeout: typing.Optional[_Duration_5170c158]=None, stop_timeout: typing.Optional[_Duration_5170c158]=None, user: typing.Optional[str]=None, working_directory: typing.Optional[str]=None) -> None:
        """
        :param image: The image used to start a container. This string is passed directly to the Docker daemon. Images in the Docker Hub registry are available by default. Other repositories are specified with either repository-url/image:tag or repository-url/image@digest. TODO: Update these to specify using classes of IContainerImage
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param cpu: The minimum number of CPU units to reserve for the container. Default: - No minimum CPU units reserved.
        :param disable_networking: Specifies whether networking is disabled within the container. When this parameter is true, networking is disabled within the container. Default: false
        :param dns_search_domains: A list of DNS search domains that are presented to the container. Default: - No search domains.
        :param dns_servers: A list of DNS servers that are presented to the container. Default: - Default DNS servers.
        :param docker_labels: A key/value map of labels to add to the container. Default: - No labels.
        :param docker_security_options: A list of strings to provide custom labels for SELinux and AppArmor multi-level security systems. Default: - No security labels.
        :param entry_point: The ENTRYPOINT value to pass to the container. Default: - Entry point configured in container.
        :param environment: The environment variables to pass to the container. Default: - No environment variables.
        :param essential: Specifies whether the container is marked essential. If the essential parameter of a container is marked as true, and that container fails or stops for any reason, all other containers that are part of the task are stopped. If the essential parameter of a container is marked as false, then its failure does not affect the rest of the containers in a task. All tasks must have at least one essential container. If this parameter is omitted, a container is assumed to be essential. Default: true
        :param extra_hosts: A list of hostnames and IP address mappings to append to the /etc/hosts file on the container. Default: - No extra hosts.
        :param gpu_count: The number of GPUs assigned to the container. Default: - No GPUs assigned.
        :param health_check: The health check command and associated configuration parameters for the container. Default: - Health check configuration from container.
        :param hostname: The hostname to use for your container. Default: - Automatic hostname.
        :param linux_parameters: Linux-specific modifications that are applied to the container, such as Linux kernel capabilities. For more information see `KernelCapabilities <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_KernelCapabilities.html>`_. Default: - No Linux parameters.
        :param logging: The log configuration specification for the container. Default: - Containers use the same logging driver that the Docker daemon uses.
        :param memory_limit_mib: The amount (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under heavy contention, Docker attempts to keep the container memory to this soft limit. However, your container can consume more memory when it needs to, up to either the hard limit specified with the memory parameter (if applicable), or all of the available memory on the container instance, whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory reserved.
        :param privileged: Specifies whether the container is marked as privileged. When this parameter is true, the container is given elevated privileges on the host container instance (similar to the root user). Default: false
        :param readonly_root_filesystem: When this parameter is true, the container is given read-only access to its root file system. Default: false
        :param secrets: The secret environment variables to pass to the container. Default: - No secret environment variables.
        :param start_timeout: Time duration (in seconds) to wait before giving up on resolving dependencies for a container. Default: - none
        :param stop_timeout: Time duration (in seconds) to wait before the container is forcefully killed if it doesn't exit normally on its own. Default: - none
        :param user: The user name to use inside the container. Default: root
        :param working_directory: The working directory in which to run commands inside the container. Default: /

        stability
        :stability: experimental
        """
        if isinstance(health_check, dict): health_check = HealthCheck(**health_check)
        self._values = {
            'image': image,
        }
        if command is not None: self._values["command"] = command
        if cpu is not None: self._values["cpu"] = cpu
        if disable_networking is not None: self._values["disable_networking"] = disable_networking
        if dns_search_domains is not None: self._values["dns_search_domains"] = dns_search_domains
        if dns_servers is not None: self._values["dns_servers"] = dns_servers
        if docker_labels is not None: self._values["docker_labels"] = docker_labels
        if docker_security_options is not None: self._values["docker_security_options"] = docker_security_options
        if entry_point is not None: self._values["entry_point"] = entry_point
        if environment is not None: self._values["environment"] = environment
        if essential is not None: self._values["essential"] = essential
        if extra_hosts is not None: self._values["extra_hosts"] = extra_hosts
        if gpu_count is not None: self._values["gpu_count"] = gpu_count
        if health_check is not None: self._values["health_check"] = health_check
        if hostname is not None: self._values["hostname"] = hostname
        if linux_parameters is not None: self._values["linux_parameters"] = linux_parameters
        if logging is not None: self._values["logging"] = logging
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib
        if memory_reservation_mib is not None: self._values["memory_reservation_mib"] = memory_reservation_mib
        if privileged is not None: self._values["privileged"] = privileged
        if readonly_root_filesystem is not None: self._values["readonly_root_filesystem"] = readonly_root_filesystem
        if secrets is not None: self._values["secrets"] = secrets
        if start_timeout is not None: self._values["start_timeout"] = start_timeout
        if stop_timeout is not None: self._values["stop_timeout"] = stop_timeout
        if user is not None: self._values["user"] = user
        if working_directory is not None: self._values["working_directory"] = working_directory

    @builtins.property
    def image(self) -> "ContainerImage":
        """The image used to start a container.

        This string is passed directly to the Docker daemon.
        Images in the Docker Hub registry are available by default.
        Other repositories are specified with either repository-url/image:tag or repository-url/image@digest.
        TODO: Update these to specify using classes of IContainerImage

        stability
        :stability: experimental
        """
        return self._values.get('image')

    @builtins.property
    def command(self) -> typing.Optional[typing.List[str]]:
        """The command that is passed to the container.

        If you provide a shell command as a single string, you have to quote command-line arguments.

        default
        :default: - CMD value built into container image.

        stability
        :stability: experimental
        """
        return self._values.get('command')

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The minimum number of CPU units to reserve for the container.

        default
        :default: - No minimum CPU units reserved.

        stability
        :stability: experimental
        """
        return self._values.get('cpu')

    @builtins.property
    def disable_networking(self) -> typing.Optional[bool]:
        """Specifies whether networking is disabled within the container.

        When this parameter is true, networking is disabled within the container.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('disable_networking')

    @builtins.property
    def dns_search_domains(self) -> typing.Optional[typing.List[str]]:
        """A list of DNS search domains that are presented to the container.

        default
        :default: - No search domains.

        stability
        :stability: experimental
        """
        return self._values.get('dns_search_domains')

    @builtins.property
    def dns_servers(self) -> typing.Optional[typing.List[str]]:
        """A list of DNS servers that are presented to the container.

        default
        :default: - Default DNS servers.

        stability
        :stability: experimental
        """
        return self._values.get('dns_servers')

    @builtins.property
    def docker_labels(self) -> typing.Optional[typing.Mapping[str, str]]:
        """A key/value map of labels to add to the container.

        default
        :default: - No labels.

        stability
        :stability: experimental
        """
        return self._values.get('docker_labels')

    @builtins.property
    def docker_security_options(self) -> typing.Optional[typing.List[str]]:
        """A list of strings to provide custom labels for SELinux and AppArmor multi-level security systems.

        default
        :default: - No security labels.

        stability
        :stability: experimental
        """
        return self._values.get('docker_security_options')

    @builtins.property
    def entry_point(self) -> typing.Optional[typing.List[str]]:
        """The ENTRYPOINT value to pass to the container.

        default
        :default: - Entry point configured in container.

        see
        :see: https://docs.docker.com/engine/reference/builder/#entrypoint
        stability
        :stability: experimental
        """
        return self._values.get('entry_point')

    @builtins.property
    def environment(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The environment variables to pass to the container.

        default
        :default: - No environment variables.

        stability
        :stability: experimental
        """
        return self._values.get('environment')

    @builtins.property
    def essential(self) -> typing.Optional[bool]:
        """Specifies whether the container is marked essential.

        If the essential parameter of a container is marked as true, and that container fails
        or stops for any reason, all other containers that are part of the task are stopped.
        If the essential parameter of a container is marked as false, then its failure does not
        affect the rest of the containers in a task. All tasks must have at least one essential container.

        If this parameter is omitted, a container is assumed to be essential.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('essential')

    @builtins.property
    def extra_hosts(self) -> typing.Optional[typing.Mapping[str, str]]:
        """A list of hostnames and IP address mappings to append to the /etc/hosts file on the container.

        default
        :default: - No extra hosts.

        stability
        :stability: experimental
        """
        return self._values.get('extra_hosts')

    @builtins.property
    def gpu_count(self) -> typing.Optional[jsii.Number]:
        """The number of GPUs assigned to the container.

        default
        :default: - No GPUs assigned.

        stability
        :stability: experimental
        """
        return self._values.get('gpu_count')

    @builtins.property
    def health_check(self) -> typing.Optional["HealthCheck"]:
        """The health check command and associated configuration parameters for the container.

        default
        :default: - Health check configuration from container.

        stability
        :stability: experimental
        """
        return self._values.get('health_check')

    @builtins.property
    def hostname(self) -> typing.Optional[str]:
        """The hostname to use for your container.

        default
        :default: - Automatic hostname.

        stability
        :stability: experimental
        """
        return self._values.get('hostname')

    @builtins.property
    def linux_parameters(self) -> typing.Optional["LinuxParameters"]:
        """Linux-specific modifications that are applied to the container, such as Linux kernel capabilities.

        For more information see `KernelCapabilities <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_KernelCapabilities.html>`_.

        default
        :default: - No Linux parameters.

        stability
        :stability: experimental
        """
        return self._values.get('linux_parameters')

    @builtins.property
    def logging(self) -> typing.Optional["LogDriver"]:
        """The log configuration specification for the container.

        default
        :default: - Containers use the same logging driver that the Docker daemon uses.

        stability
        :stability: experimental
        """
        return self._values.get('logging')

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The amount (in MiB) of memory to present to the container.

        If your container attempts to exceed the allocated memory, the container
        is terminated.

        At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

        default
        :default: - No memory limit.

        stability
        :stability: experimental
        """
        return self._values.get('memory_limit_mib')

    @builtins.property
    def memory_reservation_mib(self) -> typing.Optional[jsii.Number]:
        """The soft limit (in MiB) of memory to reserve for the container.

        When system memory is under heavy contention, Docker attempts to keep the
        container memory to this soft limit. However, your container can consume more
        memory when it needs to, up to either the hard limit specified with the memory
        parameter (if applicable), or all of the available memory on the container
        instance, whichever comes first.

        At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

        default
        :default: - No memory reserved.

        stability
        :stability: experimental
        """
        return self._values.get('memory_reservation_mib')

    @builtins.property
    def privileged(self) -> typing.Optional[bool]:
        """Specifies whether the container is marked as privileged.

        When this parameter is true, the container is given elevated privileges on the host container instance (similar to the root user).

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('privileged')

    @builtins.property
    def readonly_root_filesystem(self) -> typing.Optional[bool]:
        """When this parameter is true, the container is given read-only access to its root file system.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('readonly_root_filesystem')

    @builtins.property
    def secrets(self) -> typing.Optional[typing.Mapping[str, "Secret"]]:
        """The secret environment variables to pass to the container.

        default
        :default: - No secret environment variables.

        stability
        :stability: experimental
        """
        return self._values.get('secrets')

    @builtins.property
    def start_timeout(self) -> typing.Optional[_Duration_5170c158]:
        """Time duration (in seconds) to wait before giving up on resolving dependencies for a container.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('start_timeout')

    @builtins.property
    def stop_timeout(self) -> typing.Optional[_Duration_5170c158]:
        """Time duration (in seconds) to wait before the container is forcefully killed if it doesn't exit normally on its own.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('stop_timeout')

    @builtins.property
    def user(self) -> typing.Optional[str]:
        """The user name to use inside the container.

        default
        :default: root

        stability
        :stability: experimental
        """
        return self._values.get('user')

    @builtins.property
    def working_directory(self) -> typing.Optional[str]:
        """The working directory in which to run commands inside the container.

        default
        :default: /

        stability
        :stability: experimental
        """
        return self._values.get('working_directory')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ContainerDefinitionOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.ContainerDefinitionProps", jsii_struct_bases=[ContainerDefinitionOptions], name_mapping={'image': 'image', 'command': 'command', 'cpu': 'cpu', 'disable_networking': 'disableNetworking', 'dns_search_domains': 'dnsSearchDomains', 'dns_servers': 'dnsServers', 'docker_labels': 'dockerLabels', 'docker_security_options': 'dockerSecurityOptions', 'entry_point': 'entryPoint', 'environment': 'environment', 'essential': 'essential', 'extra_hosts': 'extraHosts', 'gpu_count': 'gpuCount', 'health_check': 'healthCheck', 'hostname': 'hostname', 'linux_parameters': 'linuxParameters', 'logging': 'logging', 'memory_limit_mib': 'memoryLimitMiB', 'memory_reservation_mib': 'memoryReservationMiB', 'privileged': 'privileged', 'readonly_root_filesystem': 'readonlyRootFilesystem', 'secrets': 'secrets', 'start_timeout': 'startTimeout', 'stop_timeout': 'stopTimeout', 'user': 'user', 'working_directory': 'workingDirectory', 'task_definition': 'taskDefinition'})
class ContainerDefinitionProps(ContainerDefinitionOptions):
    def __init__(self, *, image: "ContainerImage", command: typing.Optional[typing.List[str]]=None, cpu: typing.Optional[jsii.Number]=None, disable_networking: typing.Optional[bool]=None, dns_search_domains: typing.Optional[typing.List[str]]=None, dns_servers: typing.Optional[typing.List[str]]=None, docker_labels: typing.Optional[typing.Mapping[str, str]]=None, docker_security_options: typing.Optional[typing.List[str]]=None, entry_point: typing.Optional[typing.List[str]]=None, environment: typing.Optional[typing.Mapping[str, str]]=None, essential: typing.Optional[bool]=None, extra_hosts: typing.Optional[typing.Mapping[str, str]]=None, gpu_count: typing.Optional[jsii.Number]=None, health_check: typing.Optional["HealthCheck"]=None, hostname: typing.Optional[str]=None, linux_parameters: typing.Optional["LinuxParameters"]=None, logging: typing.Optional["LogDriver"]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None, privileged: typing.Optional[bool]=None, readonly_root_filesystem: typing.Optional[bool]=None, secrets: typing.Optional[typing.Mapping[str, "Secret"]]=None, start_timeout: typing.Optional[_Duration_5170c158]=None, stop_timeout: typing.Optional[_Duration_5170c158]=None, user: typing.Optional[str]=None, working_directory: typing.Optional[str]=None, task_definition: "TaskDefinition") -> None:
        """The properties in a container definition.

        :param image: The image used to start a container. This string is passed directly to the Docker daemon. Images in the Docker Hub registry are available by default. Other repositories are specified with either repository-url/image:tag or repository-url/image@digest. TODO: Update these to specify using classes of IContainerImage
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param cpu: The minimum number of CPU units to reserve for the container. Default: - No minimum CPU units reserved.
        :param disable_networking: Specifies whether networking is disabled within the container. When this parameter is true, networking is disabled within the container. Default: false
        :param dns_search_domains: A list of DNS search domains that are presented to the container. Default: - No search domains.
        :param dns_servers: A list of DNS servers that are presented to the container. Default: - Default DNS servers.
        :param docker_labels: A key/value map of labels to add to the container. Default: - No labels.
        :param docker_security_options: A list of strings to provide custom labels for SELinux and AppArmor multi-level security systems. Default: - No security labels.
        :param entry_point: The ENTRYPOINT value to pass to the container. Default: - Entry point configured in container.
        :param environment: The environment variables to pass to the container. Default: - No environment variables.
        :param essential: Specifies whether the container is marked essential. If the essential parameter of a container is marked as true, and that container fails or stops for any reason, all other containers that are part of the task are stopped. If the essential parameter of a container is marked as false, then its failure does not affect the rest of the containers in a task. All tasks must have at least one essential container. If this parameter is omitted, a container is assumed to be essential. Default: true
        :param extra_hosts: A list of hostnames and IP address mappings to append to the /etc/hosts file on the container. Default: - No extra hosts.
        :param gpu_count: The number of GPUs assigned to the container. Default: - No GPUs assigned.
        :param health_check: The health check command and associated configuration parameters for the container. Default: - Health check configuration from container.
        :param hostname: The hostname to use for your container. Default: - Automatic hostname.
        :param linux_parameters: Linux-specific modifications that are applied to the container, such as Linux kernel capabilities. For more information see `KernelCapabilities <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_KernelCapabilities.html>`_. Default: - No Linux parameters.
        :param logging: The log configuration specification for the container. Default: - Containers use the same logging driver that the Docker daemon uses.
        :param memory_limit_mib: The amount (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under heavy contention, Docker attempts to keep the container memory to this soft limit. However, your container can consume more memory when it needs to, up to either the hard limit specified with the memory parameter (if applicable), or all of the available memory on the container instance, whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory reserved.
        :param privileged: Specifies whether the container is marked as privileged. When this parameter is true, the container is given elevated privileges on the host container instance (similar to the root user). Default: false
        :param readonly_root_filesystem: When this parameter is true, the container is given read-only access to its root file system. Default: false
        :param secrets: The secret environment variables to pass to the container. Default: - No secret environment variables.
        :param start_timeout: Time duration (in seconds) to wait before giving up on resolving dependencies for a container. Default: - none
        :param stop_timeout: Time duration (in seconds) to wait before the container is forcefully killed if it doesn't exit normally on its own. Default: - none
        :param user: The user name to use inside the container. Default: root
        :param working_directory: The working directory in which to run commands inside the container. Default: /
        :param task_definition: The name of the task definition that includes this container definition. [disable-awslint:ref-via-interface]

        stability
        :stability: experimental
        """
        if isinstance(health_check, dict): health_check = HealthCheck(**health_check)
        self._values = {
            'image': image,
            'task_definition': task_definition,
        }
        if command is not None: self._values["command"] = command
        if cpu is not None: self._values["cpu"] = cpu
        if disable_networking is not None: self._values["disable_networking"] = disable_networking
        if dns_search_domains is not None: self._values["dns_search_domains"] = dns_search_domains
        if dns_servers is not None: self._values["dns_servers"] = dns_servers
        if docker_labels is not None: self._values["docker_labels"] = docker_labels
        if docker_security_options is not None: self._values["docker_security_options"] = docker_security_options
        if entry_point is not None: self._values["entry_point"] = entry_point
        if environment is not None: self._values["environment"] = environment
        if essential is not None: self._values["essential"] = essential
        if extra_hosts is not None: self._values["extra_hosts"] = extra_hosts
        if gpu_count is not None: self._values["gpu_count"] = gpu_count
        if health_check is not None: self._values["health_check"] = health_check
        if hostname is not None: self._values["hostname"] = hostname
        if linux_parameters is not None: self._values["linux_parameters"] = linux_parameters
        if logging is not None: self._values["logging"] = logging
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib
        if memory_reservation_mib is not None: self._values["memory_reservation_mib"] = memory_reservation_mib
        if privileged is not None: self._values["privileged"] = privileged
        if readonly_root_filesystem is not None: self._values["readonly_root_filesystem"] = readonly_root_filesystem
        if secrets is not None: self._values["secrets"] = secrets
        if start_timeout is not None: self._values["start_timeout"] = start_timeout
        if stop_timeout is not None: self._values["stop_timeout"] = stop_timeout
        if user is not None: self._values["user"] = user
        if working_directory is not None: self._values["working_directory"] = working_directory

    @builtins.property
    def image(self) -> "ContainerImage":
        """The image used to start a container.

        This string is passed directly to the Docker daemon.
        Images in the Docker Hub registry are available by default.
        Other repositories are specified with either repository-url/image:tag or repository-url/image@digest.
        TODO: Update these to specify using classes of IContainerImage

        stability
        :stability: experimental
        """
        return self._values.get('image')

    @builtins.property
    def command(self) -> typing.Optional[typing.List[str]]:
        """The command that is passed to the container.

        If you provide a shell command as a single string, you have to quote command-line arguments.

        default
        :default: - CMD value built into container image.

        stability
        :stability: experimental
        """
        return self._values.get('command')

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The minimum number of CPU units to reserve for the container.

        default
        :default: - No minimum CPU units reserved.

        stability
        :stability: experimental
        """
        return self._values.get('cpu')

    @builtins.property
    def disable_networking(self) -> typing.Optional[bool]:
        """Specifies whether networking is disabled within the container.

        When this parameter is true, networking is disabled within the container.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('disable_networking')

    @builtins.property
    def dns_search_domains(self) -> typing.Optional[typing.List[str]]:
        """A list of DNS search domains that are presented to the container.

        default
        :default: - No search domains.

        stability
        :stability: experimental
        """
        return self._values.get('dns_search_domains')

    @builtins.property
    def dns_servers(self) -> typing.Optional[typing.List[str]]:
        """A list of DNS servers that are presented to the container.

        default
        :default: - Default DNS servers.

        stability
        :stability: experimental
        """
        return self._values.get('dns_servers')

    @builtins.property
    def docker_labels(self) -> typing.Optional[typing.Mapping[str, str]]:
        """A key/value map of labels to add to the container.

        default
        :default: - No labels.

        stability
        :stability: experimental
        """
        return self._values.get('docker_labels')

    @builtins.property
    def docker_security_options(self) -> typing.Optional[typing.List[str]]:
        """A list of strings to provide custom labels for SELinux and AppArmor multi-level security systems.

        default
        :default: - No security labels.

        stability
        :stability: experimental
        """
        return self._values.get('docker_security_options')

    @builtins.property
    def entry_point(self) -> typing.Optional[typing.List[str]]:
        """The ENTRYPOINT value to pass to the container.

        default
        :default: - Entry point configured in container.

        see
        :see: https://docs.docker.com/engine/reference/builder/#entrypoint
        stability
        :stability: experimental
        """
        return self._values.get('entry_point')

    @builtins.property
    def environment(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The environment variables to pass to the container.

        default
        :default: - No environment variables.

        stability
        :stability: experimental
        """
        return self._values.get('environment')

    @builtins.property
    def essential(self) -> typing.Optional[bool]:
        """Specifies whether the container is marked essential.

        If the essential parameter of a container is marked as true, and that container fails
        or stops for any reason, all other containers that are part of the task are stopped.
        If the essential parameter of a container is marked as false, then its failure does not
        affect the rest of the containers in a task. All tasks must have at least one essential container.

        If this parameter is omitted, a container is assumed to be essential.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('essential')

    @builtins.property
    def extra_hosts(self) -> typing.Optional[typing.Mapping[str, str]]:
        """A list of hostnames and IP address mappings to append to the /etc/hosts file on the container.

        default
        :default: - No extra hosts.

        stability
        :stability: experimental
        """
        return self._values.get('extra_hosts')

    @builtins.property
    def gpu_count(self) -> typing.Optional[jsii.Number]:
        """The number of GPUs assigned to the container.

        default
        :default: - No GPUs assigned.

        stability
        :stability: experimental
        """
        return self._values.get('gpu_count')

    @builtins.property
    def health_check(self) -> typing.Optional["HealthCheck"]:
        """The health check command and associated configuration parameters for the container.

        default
        :default: - Health check configuration from container.

        stability
        :stability: experimental
        """
        return self._values.get('health_check')

    @builtins.property
    def hostname(self) -> typing.Optional[str]:
        """The hostname to use for your container.

        default
        :default: - Automatic hostname.

        stability
        :stability: experimental
        """
        return self._values.get('hostname')

    @builtins.property
    def linux_parameters(self) -> typing.Optional["LinuxParameters"]:
        """Linux-specific modifications that are applied to the container, such as Linux kernel capabilities.

        For more information see `KernelCapabilities <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_KernelCapabilities.html>`_.

        default
        :default: - No Linux parameters.

        stability
        :stability: experimental
        """
        return self._values.get('linux_parameters')

    @builtins.property
    def logging(self) -> typing.Optional["LogDriver"]:
        """The log configuration specification for the container.

        default
        :default: - Containers use the same logging driver that the Docker daemon uses.

        stability
        :stability: experimental
        """
        return self._values.get('logging')

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The amount (in MiB) of memory to present to the container.

        If your container attempts to exceed the allocated memory, the container
        is terminated.

        At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

        default
        :default: - No memory limit.

        stability
        :stability: experimental
        """
        return self._values.get('memory_limit_mib')

    @builtins.property
    def memory_reservation_mib(self) -> typing.Optional[jsii.Number]:
        """The soft limit (in MiB) of memory to reserve for the container.

        When system memory is under heavy contention, Docker attempts to keep the
        container memory to this soft limit. However, your container can consume more
        memory when it needs to, up to either the hard limit specified with the memory
        parameter (if applicable), or all of the available memory on the container
        instance, whichever comes first.

        At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

        default
        :default: - No memory reserved.

        stability
        :stability: experimental
        """
        return self._values.get('memory_reservation_mib')

    @builtins.property
    def privileged(self) -> typing.Optional[bool]:
        """Specifies whether the container is marked as privileged.

        When this parameter is true, the container is given elevated privileges on the host container instance (similar to the root user).

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('privileged')

    @builtins.property
    def readonly_root_filesystem(self) -> typing.Optional[bool]:
        """When this parameter is true, the container is given read-only access to its root file system.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('readonly_root_filesystem')

    @builtins.property
    def secrets(self) -> typing.Optional[typing.Mapping[str, "Secret"]]:
        """The secret environment variables to pass to the container.

        default
        :default: - No secret environment variables.

        stability
        :stability: experimental
        """
        return self._values.get('secrets')

    @builtins.property
    def start_timeout(self) -> typing.Optional[_Duration_5170c158]:
        """Time duration (in seconds) to wait before giving up on resolving dependencies for a container.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('start_timeout')

    @builtins.property
    def stop_timeout(self) -> typing.Optional[_Duration_5170c158]:
        """Time duration (in seconds) to wait before the container is forcefully killed if it doesn't exit normally on its own.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('stop_timeout')

    @builtins.property
    def user(self) -> typing.Optional[str]:
        """The user name to use inside the container.

        default
        :default: root

        stability
        :stability: experimental
        """
        return self._values.get('user')

    @builtins.property
    def working_directory(self) -> typing.Optional[str]:
        """The working directory in which to run commands inside the container.

        default
        :default: /

        stability
        :stability: experimental
        """
        return self._values.get('working_directory')

    @builtins.property
    def task_definition(self) -> "TaskDefinition":
        """The name of the task definition that includes this container definition.

        [disable-awslint:ref-via-interface]

        stability
        :stability: experimental
        """
        return self._values.get('task_definition')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ContainerDefinitionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.ContainerDependency", jsii_struct_bases=[], name_mapping={'container': 'container', 'condition': 'condition'})
class ContainerDependency():
    def __init__(self, *, container: "ContainerDefinition", condition: typing.Optional["ContainerDependencyCondition"]=None) -> None:
        """The details of a dependency on another container in the task definition.

        :param container: The container to depend on.
        :param condition: The state the container needs to be in to satisfy the dependency and proceed with startup. Valid values are ContainerDependencyCondition.START, ContainerDependencyCondition.COMPLETE, ContainerDependencyCondition.SUCCESS and ContainerDependencyCondition.HEALTHY. Default: ContainerDependencyCondition.HEALTHY

        see
        :see: https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_ContainerDependency.html
        stability
        :stability: experimental
        """
        self._values = {
            'container': container,
        }
        if condition is not None: self._values["condition"] = condition

    @builtins.property
    def container(self) -> "ContainerDefinition":
        """The container to depend on.

        stability
        :stability: experimental
        """
        return self._values.get('container')

    @builtins.property
    def condition(self) -> typing.Optional["ContainerDependencyCondition"]:
        """The state the container needs to be in to satisfy the dependency and proceed with startup.

        Valid values are ContainerDependencyCondition.START, ContainerDependencyCondition.COMPLETE,
        ContainerDependencyCondition.SUCCESS and ContainerDependencyCondition.HEALTHY.

        default
        :default: ContainerDependencyCondition.HEALTHY

        stability
        :stability: experimental
        """
        return self._values.get('condition')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ContainerDependency(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.aws_ecs.ContainerDependencyCondition")
class ContainerDependencyCondition(enum.Enum):
    """
    stability
    :stability: experimental
    """
    START = "START"
    """This condition emulates the behavior of links and volumes today.

    It validates that a dependent container is started before permitting other containers to start.

    stability
    :stability: experimental
    """
    COMPLETE = "COMPLETE"
    """This condition validates that a dependent container runs to completion (exits) before permitting other containers to start.

    This can be useful for nonessential containers that run a script and then exit.

    stability
    :stability: experimental
    """
    SUCCESS = "SUCCESS"
    """This condition is the same as COMPLETE, but it also requires that the container exits with a zero status.

    stability
    :stability: experimental
    """
    HEALTHY = "HEALTHY"
    """This condition validates that the dependent container passes its Docker health check before permitting other containers to start.

    This requires that the dependent container has health checks configured. This condition is confirmed only at task startup.

    stability
    :stability: experimental
    """

class ContainerImage(metaclass=jsii.JSIIAbstractClass, jsii_type="monocdk-experiment.aws_ecs.ContainerImage"):
    """Constructs for types of container images.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ContainerImageProxy

    def __init__(self) -> None:
        jsii.create(ContainerImage, self, [])

    @jsii.member(jsii_name="fromAsset")
    @builtins.classmethod
    def from_asset(cls, directory: str, *, build_args: typing.Optional[typing.Mapping[str, str]]=None, file: typing.Optional[str]=None, repository_name: typing.Optional[str]=None, target: typing.Optional[str]=None, extra_hash: typing.Optional[str]=None, exclude: typing.Optional[typing.List[str]]=None, follow: typing.Optional[_FollowMode_f74e7125]=None) -> "AssetImage":
        """Reference an image that's constructed directly from sources on disk.

        If you already have a ``DockerImageAsset`` instance, you can use the
        ``ContainerImage.fromDockerImageAsset`` method instead.

        :param directory: The directory containing the Dockerfile.
        :param build_args: Build args to pass to the ``docker build`` command. Since Docker build arguments are resolved before deployment, keys and values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or ``queue.queueUrl``). Default: - no build args are passed
        :param file: Path to the Dockerfile (relative to the directory). Default: 'Dockerfile'
        :param repository_name: ECR repository name. Specify this property if you need to statically address the image, e.g. from a Kubernetes Pod. Note, this is only the repository name, without the registry and the tag parts. Default: - the default ECR repository for CDK assets
        :param target: Docker target to build to. Default: - no target
        :param extra_hash: Extra information to encode into the fingerprint (e.g. build instructions and other inputs). Default: - hash is only based on source content
        :param exclude: Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: Never

        stability
        :stability: experimental
        """
        props = AssetImageProps(build_args=build_args, file=file, repository_name=repository_name, target=target, extra_hash=extra_hash, exclude=exclude, follow=follow)

        return jsii.sinvoke(cls, "fromAsset", [directory, props])

    @jsii.member(jsii_name="fromDockerImageAsset")
    @builtins.classmethod
    def from_docker_image_asset(cls, asset: _DockerImageAsset_e5a78fae) -> "ContainerImage":
        """Use an existing ``DockerImageAsset`` for this container image.

        :param asset: The ``DockerImageAsset`` to use for this container definition.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromDockerImageAsset", [asset])

    @jsii.member(jsii_name="fromEcrRepository")
    @builtins.classmethod
    def from_ecr_repository(cls, repository: _IRepository_aa6e452c, tag: typing.Optional[str]=None) -> "EcrImage":
        """Reference an image in an ECR repository.

        :param repository: -
        :param tag: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromEcrRepository", [repository, tag])

    @jsii.member(jsii_name="fromRegistry")
    @builtins.classmethod
    def from_registry(cls, name: str, *, credentials: typing.Optional[_ISecret_75279d36]=None) -> "RepositoryImage":
        """Reference an image on DockerHub or another online registry.

        :param name: -
        :param credentials: The secret to expose to the container that contains the credentials for the image repository. The supported value is the full ARN of an AWS Secrets Manager secret.

        stability
        :stability: experimental
        """
        props = RepositoryImageProps(credentials=credentials)

        return jsii.sinvoke(cls, "fromRegistry", [name, props])

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, scope: _Construct_f50a3f53, container_definition: "ContainerDefinition") -> "ContainerImageConfig":
        """Called when the image is used by a ContainerDefinition.

        :param scope: -
        :param container_definition: -

        stability
        :stability: experimental
        """
        ...


class _ContainerImageProxy(ContainerImage):
    @jsii.member(jsii_name="bind")
    def bind(self, scope: _Construct_f50a3f53, container_definition: "ContainerDefinition") -> "ContainerImageConfig":
        """Called when the image is used by a ContainerDefinition.

        :param scope: -
        :param container_definition: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [scope, container_definition])


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.ContainerImageConfig", jsii_struct_bases=[], name_mapping={'image_name': 'imageName', 'repository_credentials': 'repositoryCredentials'})
class ContainerImageConfig():
    def __init__(self, *, image_name: str, repository_credentials: typing.Optional["CfnTaskDefinition.RepositoryCredentialsProperty"]=None) -> None:
        """The configuration for creating a container image.

        :param image_name: Specifies the name of the container image.
        :param repository_credentials: Specifies the credentials used to access the image repository.

        stability
        :stability: experimental
        """
        if isinstance(repository_credentials, dict): repository_credentials = CfnTaskDefinition.RepositoryCredentialsProperty(**repository_credentials)
        self._values = {
            'image_name': image_name,
        }
        if repository_credentials is not None: self._values["repository_credentials"] = repository_credentials

    @builtins.property
    def image_name(self) -> str:
        """Specifies the name of the container image.

        stability
        :stability: experimental
        """
        return self._values.get('image_name')

    @builtins.property
    def repository_credentials(self) -> typing.Optional["CfnTaskDefinition.RepositoryCredentialsProperty"]:
        """Specifies the credentials used to access the image repository.

        stability
        :stability: experimental
        """
        return self._values.get('repository_credentials')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ContainerImageConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.CpuUtilizationScalingProps", jsii_struct_bases=[_BaseTargetTrackingProps_3d6586ed], name_mapping={'disable_scale_in': 'disableScaleIn', 'policy_name': 'policyName', 'scale_in_cooldown': 'scaleInCooldown', 'scale_out_cooldown': 'scaleOutCooldown', 'target_utilization_percent': 'targetUtilizationPercent'})
class CpuUtilizationScalingProps(_BaseTargetTrackingProps_3d6586ed):
    def __init__(self, *, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown: typing.Optional[_Duration_5170c158]=None, scale_out_cooldown: typing.Optional[_Duration_5170c158]=None, target_utilization_percent: jsii.Number) -> None:
        """The properties for enabling scaling based on CPU utilization.

        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. Default: false
        :param policy_name: A name for the scaling policy. Default: - Automatically generated name.
        :param scale_in_cooldown: Period after a scale in activity completes before another scale in activity can start. Default: Duration.seconds(300) for the following scalable targets: ECS services, Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters, Amazon SageMaker endpoint variants, Custom resources. For all other scalable targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB global secondary indexes, Amazon Comprehend document classification endpoints, Lambda provisioned concurrency
        :param scale_out_cooldown: Period after a scale out activity completes before another scale out activity can start. Default: Duration.seconds(300) for the following scalable targets: ECS services, Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters, Amazon SageMaker endpoint variants, Custom resources. For all other scalable targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB global secondary indexes, Amazon Comprehend document classification endpoints, Lambda provisioned concurrency
        :param target_utilization_percent: The target value for CPU utilization across all tasks in the service.

        stability
        :stability: experimental
        """
        self._values = {
            'target_utilization_percent': target_utilization_percent,
        }
        if disable_scale_in is not None: self._values["disable_scale_in"] = disable_scale_in
        if policy_name is not None: self._values["policy_name"] = policy_name
        if scale_in_cooldown is not None: self._values["scale_in_cooldown"] = scale_in_cooldown
        if scale_out_cooldown is not None: self._values["scale_out_cooldown"] = scale_out_cooldown

    @builtins.property
    def disable_scale_in(self) -> typing.Optional[bool]:
        """Indicates whether scale in by the target tracking policy is disabled.

        If the value is true, scale in is disabled and the target tracking policy
        won't remove capacity from the scalable resource. Otherwise, scale in is
        enabled and the target tracking policy can remove capacity from the
        scalable resource.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('disable_scale_in')

    @builtins.property
    def policy_name(self) -> typing.Optional[str]:
        """A name for the scaling policy.

        default
        :default: - Automatically generated name.

        stability
        :stability: experimental
        """
        return self._values.get('policy_name')

    @builtins.property
    def scale_in_cooldown(self) -> typing.Optional[_Duration_5170c158]:
        """Period after a scale in activity completes before another scale in activity can start.

        default
        :default:

        Duration.seconds(300) for the following scalable targets: ECS services,
        Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters,
        Amazon SageMaker endpoint variants, Custom resources. For all other scalable
        targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB
        global secondary indexes, Amazon Comprehend document classification endpoints,
        Lambda provisioned concurrency

        stability
        :stability: experimental
        """
        return self._values.get('scale_in_cooldown')

    @builtins.property
    def scale_out_cooldown(self) -> typing.Optional[_Duration_5170c158]:
        """Period after a scale out activity completes before another scale out activity can start.

        default
        :default:

        Duration.seconds(300) for the following scalable targets: ECS services,
        Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters,
        Amazon SageMaker endpoint variants, Custom resources. For all other scalable
        targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB
        global secondary indexes, Amazon Comprehend document classification endpoints,
        Lambda provisioned concurrency

        stability
        :stability: experimental
        """
        return self._values.get('scale_out_cooldown')

    @builtins.property
    def target_utilization_percent(self) -> jsii.Number:
        """The target value for CPU utilization across all tasks in the service.

        stability
        :stability: experimental
        """
        return self._values.get('target_utilization_percent')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CpuUtilizationScalingProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.DeploymentController", jsii_struct_bases=[], name_mapping={'type': 'type'})
class DeploymentController():
    def __init__(self, *, type: typing.Optional["DeploymentControllerType"]=None) -> None:
        """The deployment controller to use for the service.

        :param type: The deployment controller type to use. Default: DeploymentControllerType.ECS

        stability
        :stability: experimental
        """
        self._values = {
        }
        if type is not None: self._values["type"] = type

    @builtins.property
    def type(self) -> typing.Optional["DeploymentControllerType"]:
        """The deployment controller type to use.

        default
        :default: DeploymentControllerType.ECS

        stability
        :stability: experimental
        """
        return self._values.get('type')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DeploymentController(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.aws_ecs.DeploymentControllerType")
class DeploymentControllerType(enum.Enum):
    """The deployment controller type to use for the service.

    stability
    :stability: experimental
    """
    ECS = "ECS"
    """The rolling update (ECS) deployment type involves replacing the current running version of the container with the latest version.

    stability
    :stability: experimental
    """
    CODE_DEPLOY = "CODE_DEPLOY"
    """The blue/green (CODE_DEPLOY) deployment type uses the blue/green deployment model powered by AWS CodeDeploy.

    stability
    :stability: experimental
    """
    EXTERNAL = "EXTERNAL"
    """The external (EXTERNAL) deployment type enables you to use any third-party deployment controller.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.Device", jsii_struct_bases=[], name_mapping={'host_path': 'hostPath', 'container_path': 'containerPath', 'permissions': 'permissions'})
class Device():
    def __init__(self, *, host_path: str, container_path: typing.Optional[str]=None, permissions: typing.Optional[typing.List["DevicePermission"]]=None) -> None:
        """A container instance host device.

        :param host_path: The path for the device on the host container instance.
        :param container_path: The path inside the container at which to expose the host device. Default: Same path as the host
        :param permissions: The explicit permissions to provide to the container for the device. By default, the container has permissions for read, write, and mknod for the device. Default: Readonly

        stability
        :stability: experimental
        """
        self._values = {
            'host_path': host_path,
        }
        if container_path is not None: self._values["container_path"] = container_path
        if permissions is not None: self._values["permissions"] = permissions

    @builtins.property
    def host_path(self) -> str:
        """The path for the device on the host container instance.

        stability
        :stability: experimental
        """
        return self._values.get('host_path')

    @builtins.property
    def container_path(self) -> typing.Optional[str]:
        """The path inside the container at which to expose the host device.

        default
        :default: Same path as the host

        stability
        :stability: experimental
        """
        return self._values.get('container_path')

    @builtins.property
    def permissions(self) -> typing.Optional[typing.List["DevicePermission"]]:
        """The explicit permissions to provide to the container for the device.

        By default, the container has permissions for read, write, and mknod for the device.

        default
        :default: Readonly

        stability
        :stability: experimental
        """
        return self._values.get('permissions')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'Device(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.aws_ecs.DevicePermission")
class DevicePermission(enum.Enum):
    """Permissions for device access.

    stability
    :stability: experimental
    """
    READ = "READ"
    """Read.

    stability
    :stability: experimental
    """
    WRITE = "WRITE"
    """Write.

    stability
    :stability: experimental
    """
    MKNOD = "MKNOD"
    """Make a node.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.DockerVolumeConfiguration", jsii_struct_bases=[], name_mapping={'driver': 'driver', 'scope': 'scope', 'autoprovision': 'autoprovision', 'driver_opts': 'driverOpts', 'labels': 'labels'})
class DockerVolumeConfiguration():
    def __init__(self, *, driver: str, scope: "Scope", autoprovision: typing.Optional[bool]=None, driver_opts: typing.Optional[typing.Mapping[str, str]]=None, labels: typing.Optional[typing.List[str]]=None) -> None:
        """The configuration for a Docker volume.

        Docker volumes are only supported when you are using the EC2 launch type.

        :param driver: The Docker volume driver to use.
        :param scope: The scope for the Docker volume that determines its lifecycle.
        :param autoprovision: Specifies whether the Docker volume should be created if it does not already exist. If true is specified, the Docker volume will be created for you. Default: false
        :param driver_opts: A map of Docker driver-specific options passed through. Default: No options
        :param labels: Custom metadata to add to your Docker volume. Default: No labels

        stability
        :stability: experimental
        """
        self._values = {
            'driver': driver,
            'scope': scope,
        }
        if autoprovision is not None: self._values["autoprovision"] = autoprovision
        if driver_opts is not None: self._values["driver_opts"] = driver_opts
        if labels is not None: self._values["labels"] = labels

    @builtins.property
    def driver(self) -> str:
        """The Docker volume driver to use.

        stability
        :stability: experimental
        """
        return self._values.get('driver')

    @builtins.property
    def scope(self) -> "Scope":
        """The scope for the Docker volume that determines its lifecycle.

        stability
        :stability: experimental
        """
        return self._values.get('scope')

    @builtins.property
    def autoprovision(self) -> typing.Optional[bool]:
        """Specifies whether the Docker volume should be created if it does not already exist.

        If true is specified, the Docker volume will be created for you.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('autoprovision')

    @builtins.property
    def driver_opts(self) -> typing.Optional[typing.Mapping[str, str]]:
        """A map of Docker driver-specific options passed through.

        default
        :default: No options

        stability
        :stability: experimental
        """
        return self._values.get('driver_opts')

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[str]]:
        """Custom metadata to add to your Docker volume.

        default
        :default: No labels

        stability
        :stability: experimental
        """
        return self._values.get('labels')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DockerVolumeConfiguration(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.Ec2ServiceAttributes", jsii_struct_bases=[], name_mapping={'cluster': 'cluster', 'service_arn': 'serviceArn', 'service_name': 'serviceName'})
class Ec2ServiceAttributes():
    def __init__(self, *, cluster: "ICluster", service_arn: typing.Optional[str]=None, service_name: typing.Optional[str]=None) -> None:
        """The properties to import from the service using the EC2 launch type.

        :param cluster: The cluster that hosts the service.
        :param service_arn: The service ARN. Default: - either this, or {@link serviceName}, is required
        :param service_name: The name of the service. Default: - either this, or {@link serviceArn}, is required

        stability
        :stability: experimental
        """
        self._values = {
            'cluster': cluster,
        }
        if service_arn is not None: self._values["service_arn"] = service_arn
        if service_name is not None: self._values["service_name"] = service_name

    @builtins.property
    def cluster(self) -> "ICluster":
        """The cluster that hosts the service.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @builtins.property
    def service_arn(self) -> typing.Optional[str]:
        """The service ARN.

        default
        :default: - either this, or {@link serviceName}, is required

        stability
        :stability: experimental
        """
        return self._values.get('service_arn')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """The name of the service.

        default
        :default: - either this, or {@link serviceArn}, is required

        stability
        :stability: experimental
        """
        return self._values.get('service_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'Ec2ServiceAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.Ec2ServiceProps", jsii_struct_bases=[BaseServiceOptions], name_mapping={'cluster': 'cluster', 'cloud_map_options': 'cloudMapOptions', 'deployment_controller': 'deploymentController', 'desired_count': 'desiredCount', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'health_check_grace_period': 'healthCheckGracePeriod', 'max_healthy_percent': 'maxHealthyPercent', 'min_healthy_percent': 'minHealthyPercent', 'propagate_tags': 'propagateTags', 'service_name': 'serviceName', 'task_definition': 'taskDefinition', 'assign_public_ip': 'assignPublicIp', 'daemon': 'daemon', 'placement_constraints': 'placementConstraints', 'placement_strategies': 'placementStrategies', 'propagate_task_tags_from': 'propagateTaskTagsFrom', 'security_group': 'securityGroup', 'security_groups': 'securityGroups', 'vpc_subnets': 'vpcSubnets'})
class Ec2ServiceProps(BaseServiceOptions):
    def __init__(self, *, cluster: "ICluster", cloud_map_options: typing.Optional["CloudMapOptions"]=None, deployment_controller: typing.Optional["DeploymentController"]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[_Duration_5170c158]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional["PropagatedTagSource"]=None, service_name: typing.Optional[str]=None, task_definition: "TaskDefinition", assign_public_ip: typing.Optional[bool]=None, daemon: typing.Optional[bool]=None, placement_constraints: typing.Optional[typing.List["PlacementConstraint"]]=None, placement_strategies: typing.Optional[typing.List["PlacementStrategy"]]=None, propagate_task_tags_from: typing.Optional["PropagatedTagSource"]=None, security_group: typing.Optional[_ISecurityGroup_d72ab8e8]=None, security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]]=None, vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6]=None) -> None:
        """The properties for defining a service using the EC2 launch type.

        :param cluster: The name of the cluster that hosts the service.
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param deployment_controller: Specifies which deployment controller to use for the service. For more information, see `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_ Default: - Rolling update (ECS)
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Valid values are: PropagatedTagSource.SERVICE, PropagatedTagSource.TASK_DEFINITION or PropagatedTagSource.NONE Default: PropagatedTagSource.NONE
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param task_definition: The task definition to use for tasks in the service. [disable-awslint:ref-via-interface]
        :param assign_public_ip: Specifies whether the task's elastic network interface receives a public IP address. If true, each task will receive a public IP address. This property is only used for tasks that use the awsvpc network mode. Default: false
        :param daemon: Specifies whether the service will use the daemon scheduling strategy. If true, the service scheduler deploys exactly one task on each container instance in your cluster. When you are using this strategy, do not specify a desired number of tasks orany task placement strategies. Default: false
        :param placement_constraints: The placement constraints to use for tasks in the service. For more information, see `Amazon ECS Task Placement Constraints <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-constraints.html>`_. Default: - No constraints.
        :param placement_strategies: The placement strategies to use for tasks in the service. For more information, see `Amazon ECS Task Placement Strategies <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-strategies.html>`_. Default: - No strategies.
        :param propagate_task_tags_from: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: PropagatedTagSource.NONE
        :param security_group: The security groups to associate with the service. If you do not specify a security group, the default security group for the VPC is used. This property is only used for tasks that use the awsvpc network mode. Default: - A new security group is created.
        :param security_groups: The security groups to associate with the service. If you do not specify a security group, the default security group for the VPC is used. This property is only used for tasks that use the awsvpc network mode. Default: - A new security group is created.
        :param vpc_subnets: The subnets to associate with the service. This property is only used for tasks that use the awsvpc network mode. Default: - Public subnets if ``assignPublicIp`` is set, otherwise the first available one of Private, Isolated, Public, in that order.

        stability
        :stability: experimental
        """
        if isinstance(cloud_map_options, dict): cloud_map_options = CloudMapOptions(**cloud_map_options)
        if isinstance(deployment_controller, dict): deployment_controller = DeploymentController(**deployment_controller)
        if isinstance(vpc_subnets, dict): vpc_subnets = _SubnetSelection_36a13cd6(**vpc_subnets)
        self._values = {
            'cluster': cluster,
            'task_definition': task_definition,
        }
        if cloud_map_options is not None: self._values["cloud_map_options"] = cloud_map_options
        if deployment_controller is not None: self._values["deployment_controller"] = deployment_controller
        if desired_count is not None: self._values["desired_count"] = desired_count
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None: self._values["health_check_grace_period"] = health_check_grace_period
        if max_healthy_percent is not None: self._values["max_healthy_percent"] = max_healthy_percent
        if min_healthy_percent is not None: self._values["min_healthy_percent"] = min_healthy_percent
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if service_name is not None: self._values["service_name"] = service_name
        if assign_public_ip is not None: self._values["assign_public_ip"] = assign_public_ip
        if daemon is not None: self._values["daemon"] = daemon
        if placement_constraints is not None: self._values["placement_constraints"] = placement_constraints
        if placement_strategies is not None: self._values["placement_strategies"] = placement_strategies
        if propagate_task_tags_from is not None: self._values["propagate_task_tags_from"] = propagate_task_tags_from
        if security_group is not None: self._values["security_group"] = security_group
        if security_groups is not None: self._values["security_groups"] = security_groups
        if vpc_subnets is not None: self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def cluster(self) -> "ICluster":
        """The name of the cluster that hosts the service.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @builtins.property
    def cloud_map_options(self) -> typing.Optional["CloudMapOptions"]:
        """The options for configuring an Amazon ECS service to use service discovery.

        default
        :default: - AWS Cloud Map service discovery is not enabled.

        stability
        :stability: experimental
        """
        return self._values.get('cloud_map_options')

    @builtins.property
    def deployment_controller(self) -> typing.Optional["DeploymentController"]:
        """Specifies which deployment controller to use for the service.

        For more information, see
        `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_

        default
        :default: - Rolling update (ECS)

        stability
        :stability: experimental
        """
        return self._values.get('deployment_controller')

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('desired_count')

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('enable_ecs_managed_tags')

    @builtins.property
    def health_check_grace_period(self) -> typing.Optional[_Duration_5170c158]:
        """The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        default
        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set

        stability
        :stability: experimental
        """
        return self._values.get('health_check_grace_period')

    @builtins.property
    def max_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment.

        default
        :default: - 100 if daemon, otherwise 200

        stability
        :stability: experimental
        """
        return self._values.get('max_healthy_percent')

    @builtins.property
    def min_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment.

        default
        :default: - 0 if daemon, otherwise 50

        stability
        :stability: experimental
        """
        return self._values.get('min_healthy_percent')

    @builtins.property
    def propagate_tags(self) -> typing.Optional["PropagatedTagSource"]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Valid values are: PropagatedTagSource.SERVICE, PropagatedTagSource.TASK_DEFINITION or PropagatedTagSource.NONE

        default
        :default: PropagatedTagSource.NONE

        stability
        :stability: experimental
        """
        return self._values.get('propagate_tags')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """The name of the service.

        default
        :default: - CloudFormation-generated name.

        stability
        :stability: experimental
        """
        return self._values.get('service_name')

    @builtins.property
    def task_definition(self) -> "TaskDefinition":
        """The task definition to use for tasks in the service.

        [disable-awslint:ref-via-interface]

        stability
        :stability: experimental
        """
        return self._values.get('task_definition')

    @builtins.property
    def assign_public_ip(self) -> typing.Optional[bool]:
        """Specifies whether the task's elastic network interface receives a public IP address.

        If true, each task will receive a public IP address.

        This property is only used for tasks that use the awsvpc network mode.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('assign_public_ip')

    @builtins.property
    def daemon(self) -> typing.Optional[bool]:
        """Specifies whether the service will use the daemon scheduling strategy.

        If true, the service scheduler deploys exactly one task on each container instance in your cluster.

        When you are using this strategy, do not specify a desired number of tasks orany task placement strategies.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('daemon')

    @builtins.property
    def placement_constraints(self) -> typing.Optional[typing.List["PlacementConstraint"]]:
        """The placement constraints to use for tasks in the service.

        For more information, see
        `Amazon ECS Task Placement Constraints <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-constraints.html>`_.

        default
        :default: - No constraints.

        stability
        :stability: experimental
        """
        return self._values.get('placement_constraints')

    @builtins.property
    def placement_strategies(self) -> typing.Optional[typing.List["PlacementStrategy"]]:
        """The placement strategies to use for tasks in the service.

        For more information, see
        `Amazon ECS Task Placement Strategies <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-strategies.html>`_.

        default
        :default: - No strategies.

        stability
        :stability: experimental
        """
        return self._values.get('placement_strategies')

    @builtins.property
    def propagate_task_tags_from(self) -> typing.Optional["PropagatedTagSource"]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        default
        :default: PropagatedTagSource.NONE

        deprecated
        :deprecated: Use ``propagateTags`` instead.

        stability
        :stability: deprecated
        """
        return self._values.get('propagate_task_tags_from')

    @builtins.property
    def security_group(self) -> typing.Optional[_ISecurityGroup_d72ab8e8]:
        """The security groups to associate with the service.

        If you do not specify a security group, the default security group for the VPC is used.

        This property is only used for tasks that use the awsvpc network mode.

        default
        :default: - A new security group is created.

        deprecated
        :deprecated: use securityGroups instead.

        stability
        :stability: deprecated
        """
        return self._values.get('security_group')

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]]:
        """The security groups to associate with the service.

        If you do not specify a security group, the default security group for the VPC is used.

        This property is only used for tasks that use the awsvpc network mode.

        default
        :default: - A new security group is created.

        stability
        :stability: experimental
        """
        return self._values.get('security_groups')

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_36a13cd6]:
        """The subnets to associate with the service.

        This property is only used for tasks that use the awsvpc network mode.

        default
        :default: - Public subnets if ``assignPublicIp`` is set, otherwise the first available one of Private, Isolated, Public, in that order.

        stability
        :stability: experimental
        """
        return self._values.get('vpc_subnets')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'Ec2ServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.Ec2TaskDefinitionProps", jsii_struct_bases=[CommonTaskDefinitionProps], name_mapping={'execution_role': 'executionRole', 'family': 'family', 'proxy_configuration': 'proxyConfiguration', 'task_role': 'taskRole', 'volumes': 'volumes', 'ipc_mode': 'ipcMode', 'network_mode': 'networkMode', 'pid_mode': 'pidMode', 'placement_constraints': 'placementConstraints'})
class Ec2TaskDefinitionProps(CommonTaskDefinitionProps):
    def __init__(self, *, execution_role: typing.Optional[_IRole_e69bbae4]=None, family: typing.Optional[str]=None, proxy_configuration: typing.Optional["ProxyConfiguration"]=None, task_role: typing.Optional[_IRole_e69bbae4]=None, volumes: typing.Optional[typing.List["Volume"]]=None, ipc_mode: typing.Optional["IpcMode"]=None, network_mode: typing.Optional["NetworkMode"]=None, pid_mode: typing.Optional["PidMode"]=None, placement_constraints: typing.Optional[typing.List["PlacementConstraint"]]=None) -> None:
        """The properties for a task definition run on an EC2 cluster.

        :param execution_role: The name of the IAM task execution role that grants the ECS agent to call AWS APIs on your behalf. The role will be used to retrieve container images from ECR and create CloudWatch log groups. Default: - An execution role will be automatically created if you use ECR images in your task definition.
        :param family: The name of a family that this task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param proxy_configuration: The configuration details for the App Mesh proxy. Default: - No proxy configuration.
        :param task_role: The name of the IAM role that grants containers in the task permission to call AWS APIs on your behalf. Default: - A task role is automatically created for you.
        :param volumes: The list of volume definitions for the task. For more information, see `Task Definition Parameter Volumes <https://docs.aws.amazon.com/AmazonECS/latest/developerguide//task_definition_parameters.html#volumes>`_. Default: - No volumes are passed to the Docker daemon on a container instance.
        :param ipc_mode: The IPC resource namespace to use for the containers in the task. Not supported in Fargate and Windows containers. Default: - IpcMode used by the task is not specified
        :param network_mode: The Docker networking mode to use for the containers in the task. The valid values are none, bridge, awsvpc, and host. Default: - NetworkMode.Bridge for EC2 tasks, AwsVpc for Fargate tasks.
        :param pid_mode: The process namespace to use for the containers in the task. Not supported in Fargate and Windows containers. Default: - PidMode used by the task is not specified
        :param placement_constraints: An array of placement constraint objects to use for the task. You can specify a maximum of 10 constraints per task (this limit includes constraints in the task definition and those specified at run time). Default: - No placement constraints.

        stability
        :stability: experimental
        """
        self._values = {
        }
        if execution_role is not None: self._values["execution_role"] = execution_role
        if family is not None: self._values["family"] = family
        if proxy_configuration is not None: self._values["proxy_configuration"] = proxy_configuration
        if task_role is not None: self._values["task_role"] = task_role
        if volumes is not None: self._values["volumes"] = volumes
        if ipc_mode is not None: self._values["ipc_mode"] = ipc_mode
        if network_mode is not None: self._values["network_mode"] = network_mode
        if pid_mode is not None: self._values["pid_mode"] = pid_mode
        if placement_constraints is not None: self._values["placement_constraints"] = placement_constraints

    @builtins.property
    def execution_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The name of the IAM task execution role that grants the ECS agent to call AWS APIs on your behalf.

        The role will be used to retrieve container images from ECR and create CloudWatch log groups.

        default
        :default: - An execution role will be automatically created if you use ECR images in your task definition.

        stability
        :stability: experimental
        """
        return self._values.get('execution_role')

    @builtins.property
    def family(self) -> typing.Optional[str]:
        """The name of a family that this task definition is registered to.

        A family groups multiple versions of a task definition.

        default
        :default: - Automatically generated name.

        stability
        :stability: experimental
        """
        return self._values.get('family')

    @builtins.property
    def proxy_configuration(self) -> typing.Optional["ProxyConfiguration"]:
        """The configuration details for the App Mesh proxy.

        default
        :default: - No proxy configuration.

        stability
        :stability: experimental
        """
        return self._values.get('proxy_configuration')

    @builtins.property
    def task_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The name of the IAM role that grants containers in the task permission to call AWS APIs on your behalf.

        default
        :default: - A task role is automatically created for you.

        stability
        :stability: experimental
        """
        return self._values.get('task_role')

    @builtins.property
    def volumes(self) -> typing.Optional[typing.List["Volume"]]:
        """The list of volume definitions for the task.

        For more information, see
        `Task Definition Parameter Volumes <https://docs.aws.amazon.com/AmazonECS/latest/developerguide//task_definition_parameters.html#volumes>`_.

        default
        :default: - No volumes are passed to the Docker daemon on a container instance.

        stability
        :stability: experimental
        """
        return self._values.get('volumes')

    @builtins.property
    def ipc_mode(self) -> typing.Optional["IpcMode"]:
        """The IPC resource namespace to use for the containers in the task.

        Not supported in Fargate and Windows containers.

        default
        :default: - IpcMode used by the task is not specified

        stability
        :stability: experimental
        """
        return self._values.get('ipc_mode')

    @builtins.property
    def network_mode(self) -> typing.Optional["NetworkMode"]:
        """The Docker networking mode to use for the containers in the task.

        The valid values are none, bridge, awsvpc, and host.

        default
        :default: - NetworkMode.Bridge for EC2 tasks, AwsVpc for Fargate tasks.

        stability
        :stability: experimental
        """
        return self._values.get('network_mode')

    @builtins.property
    def pid_mode(self) -> typing.Optional["PidMode"]:
        """The process namespace to use for the containers in the task.

        Not supported in Fargate and Windows containers.

        default
        :default: - PidMode used by the task is not specified

        stability
        :stability: experimental
        """
        return self._values.get('pid_mode')

    @builtins.property
    def placement_constraints(self) -> typing.Optional[typing.List["PlacementConstraint"]]:
        """An array of placement constraint objects to use for the task.

        You can
        specify a maximum of 10 constraints per task (this limit includes
        constraints in the task definition and those specified at run time).

        default
        :default: - No placement constraints.

        stability
        :stability: experimental
        """
        return self._values.get('placement_constraints')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'Ec2TaskDefinitionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class EcrImage(ContainerImage, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs.EcrImage"):
    """An image from an Amazon ECR repository.

    stability
    :stability: experimental
    """
    def __init__(self, repository: _IRepository_aa6e452c, tag: str) -> None:
        """Constructs a new instance of the EcrImage class.

        :param repository: -
        :param tag: -

        stability
        :stability: experimental
        """
        jsii.create(EcrImage, self, [repository, tag])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _Construct_f50a3f53, container_definition: "ContainerDefinition") -> "ContainerImageConfig":
        """Called when the image is used by a ContainerDefinition.

        :param _scope: -
        :param container_definition: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_scope, container_definition])

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> str:
        """The image name. Images in Amazon ECR repositories can be specified by either using the full registry/repository:tag or registry/repository@digest.

        For example, 012345678910.dkr.ecr..amazonaws.com/:latest or
        012345678910.dkr.ecr..amazonaws.com/@sha256:94afd1f2e64d908bc90dbca0035a5b567EXAMPLE.

        stability
        :stability: experimental
        """
        return jsii.get(self, "imageName")


@jsii.implements(_IMachineImage_d5cd7b45)
class EcsOptimizedAmi(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs.EcsOptimizedAmi"):
    """Construct a Linux or Windows machine image from the latest ECS Optimized AMI published in SSM.

    deprecated
    :deprecated: see {@link EcsOptimizedImage#amazonLinux}, {@link EcsOptimizedImage#amazonLinux} and {@link EcsOptimizedImage#windows}

    stability
    :stability: deprecated
    """
    def __init__(self, *, generation: typing.Optional[_AmazonLinuxGeneration_f5d20aaa]=None, hardware_type: typing.Optional["AmiHardwareType"]=None, windows_version: typing.Optional["WindowsOptimizedVersion"]=None) -> None:
        """Constructs a new instance of the EcsOptimizedAmi class.

        :param generation: The Amazon Linux generation to use. Default: AmazonLinuxGeneration.AmazonLinux2
        :param hardware_type: The ECS-optimized AMI variant to use. Default: AmiHardwareType.Standard
        :param windows_version: The Windows Server version to use. Default: none, uses Linux generation

        stability
        :stability: deprecated
        """
        props = EcsOptimizedAmiProps(generation=generation, hardware_type=hardware_type, windows_version=windows_version)

        jsii.create(EcsOptimizedAmi, self, [props])

    @jsii.member(jsii_name="getImage")
    def get_image(self, scope: _Construct_f50a3f53) -> _MachineImageConfig_815fc1b9:
        """Return the correct image.

        :param scope: -

        stability
        :stability: deprecated
        """
        return jsii.invoke(self, "getImage", [scope])


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.EcsOptimizedAmiProps", jsii_struct_bases=[], name_mapping={'generation': 'generation', 'hardware_type': 'hardwareType', 'windows_version': 'windowsVersion'})
class EcsOptimizedAmiProps():
    def __init__(self, *, generation: typing.Optional[_AmazonLinuxGeneration_f5d20aaa]=None, hardware_type: typing.Optional["AmiHardwareType"]=None, windows_version: typing.Optional["WindowsOptimizedVersion"]=None) -> None:
        """The properties that define which ECS-optimized AMI is used.

        :param generation: The Amazon Linux generation to use. Default: AmazonLinuxGeneration.AmazonLinux2
        :param hardware_type: The ECS-optimized AMI variant to use. Default: AmiHardwareType.Standard
        :param windows_version: The Windows Server version to use. Default: none, uses Linux generation

        deprecated
        :deprecated: see {@link EcsOptimizedImage}

        stability
        :stability: deprecated
        """
        self._values = {
        }
        if generation is not None: self._values["generation"] = generation
        if hardware_type is not None: self._values["hardware_type"] = hardware_type
        if windows_version is not None: self._values["windows_version"] = windows_version

    @builtins.property
    def generation(self) -> typing.Optional[_AmazonLinuxGeneration_f5d20aaa]:
        """The Amazon Linux generation to use.

        default
        :default: AmazonLinuxGeneration.AmazonLinux2

        stability
        :stability: deprecated
        """
        return self._values.get('generation')

    @builtins.property
    def hardware_type(self) -> typing.Optional["AmiHardwareType"]:
        """The ECS-optimized AMI variant to use.

        default
        :default: AmiHardwareType.Standard

        stability
        :stability: deprecated
        """
        return self._values.get('hardware_type')

    @builtins.property
    def windows_version(self) -> typing.Optional["WindowsOptimizedVersion"]:
        """The Windows Server version to use.

        default
        :default: none, uses Linux generation

        stability
        :stability: deprecated
        """
        return self._values.get('windows_version')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EcsOptimizedAmiProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IMachineImage_d5cd7b45)
class EcsOptimizedImage(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs.EcsOptimizedImage"):
    """Construct a Linux or Windows machine image from the latest ECS Optimized AMI published in SSM.

    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="amazonLinux")
    @builtins.classmethod
    def amazon_linux(cls) -> "EcsOptimizedImage":
        """Construct an Amazon Linux AMI image from the latest ECS Optimized AMI published in SSM.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "amazonLinux", [])

    @jsii.member(jsii_name="amazonLinux2")
    @builtins.classmethod
    def amazon_linux2(cls, hardware_type: typing.Optional["AmiHardwareType"]=None) -> "EcsOptimizedImage":
        """Construct an Amazon Linux 2 image from the latest ECS Optimized AMI published in SSM.

        :param hardware_type: ECS-optimized AMI variant to use.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "amazonLinux2", [hardware_type])

    @jsii.member(jsii_name="windows")
    @builtins.classmethod
    def windows(cls, windows_version: "WindowsOptimizedVersion") -> "EcsOptimizedImage":
        """Construct a Windows image from the latest ECS Optimized AMI published in SSM.

        :param windows_version: Windows Version to use.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "windows", [windows_version])

    @jsii.member(jsii_name="getImage")
    def get_image(self, scope: _Construct_f50a3f53) -> _MachineImageConfig_815fc1b9:
        """Return the correct image.

        :param scope: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getImage", [scope])


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.EcsTarget", jsii_struct_bases=[], name_mapping={'container_name': 'containerName', 'listener': 'listener', 'new_target_group_id': 'newTargetGroupId', 'container_port': 'containerPort', 'protocol': 'protocol'})
class EcsTarget():
    def __init__(self, *, container_name: str, listener: "ListenerConfig", new_target_group_id: str, container_port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["Protocol"]=None) -> None:
        """
        :param container_name: The name of the container.
        :param listener: Listener and properties for adding target group to the listener.
        :param new_target_group_id: ID for a target group to be created.
        :param container_port: The port number of the container. Only applicable when using application/network load balancers. Default: - Container port of the first added port mapping.
        :param protocol: The protocol used for the port mapping. Only applicable when using application load balancers. Default: Protocol.TCP

        stability
        :stability: experimental
        """
        self._values = {
            'container_name': container_name,
            'listener': listener,
            'new_target_group_id': new_target_group_id,
        }
        if container_port is not None: self._values["container_port"] = container_port
        if protocol is not None: self._values["protocol"] = protocol

    @builtins.property
    def container_name(self) -> str:
        """The name of the container.

        stability
        :stability: experimental
        """
        return self._values.get('container_name')

    @builtins.property
    def listener(self) -> "ListenerConfig":
        """Listener and properties for adding target group to the listener.

        stability
        :stability: experimental
        """
        return self._values.get('listener')

    @builtins.property
    def new_target_group_id(self) -> str:
        """ID for a target group to be created.

        stability
        :stability: experimental
        """
        return self._values.get('new_target_group_id')

    @builtins.property
    def container_port(self) -> typing.Optional[jsii.Number]:
        """The port number of the container.

        Only applicable when using application/network load balancers.

        default
        :default: - Container port of the first added port mapping.

        stability
        :stability: experimental
        """
        return self._values.get('container_port')

    @builtins.property
    def protocol(self) -> typing.Optional["Protocol"]:
        """The protocol used for the port mapping.

        Only applicable when using application load balancers.

        default
        :default: Protocol.TCP

        stability
        :stability: experimental
        """
        return self._values.get('protocol')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EcsTarget(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.aws_ecs.FargatePlatformVersion")
class FargatePlatformVersion(enum.Enum):
    """The platform version on which to run your service.

    see
    :see: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html
    stability
    :stability: experimental
    """
    LATEST = "LATEST"
    """The latest, recommended platform version.

    stability
    :stability: experimental
    """
    VERSION1_4 = "VERSION1_4"
    """Version 1.4.0.

    Supports EFS endpoints, CAP_SYS_PTRACE Linux capability,
    network performance metrics in CloudWatch Container Insights,
    consolidated 20 GB ephemeral volume.

    stability
    :stability: experimental
    """
    VERSION1_3 = "VERSION1_3"
    """Version 1.3.0.

    Supports secrets, task recycling.

    stability
    :stability: experimental
    """
    VERSION1_2 = "VERSION1_2"
    """Version 1.2.0.

    Supports private registries.

    stability
    :stability: experimental
    """
    VERSION1_1 = "VERSION1_1"
    """Version 1.1.0.

    Supports task metadata, health checks, service discovery.

    stability
    :stability: experimental
    """
    VERSION1_0 = "VERSION1_0"
    """Initial release.

    Based on Amazon Linux 2017.09.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.FargateServiceAttributes", jsii_struct_bases=[], name_mapping={'cluster': 'cluster', 'service_arn': 'serviceArn', 'service_name': 'serviceName'})
class FargateServiceAttributes():
    def __init__(self, *, cluster: "ICluster", service_arn: typing.Optional[str]=None, service_name: typing.Optional[str]=None) -> None:
        """The properties to import from the service using the Fargate launch type.

        :param cluster: The cluster that hosts the service.
        :param service_arn: The service ARN. Default: - either this, or {@link serviceName}, is required
        :param service_name: The name of the service. Default: - either this, or {@link serviceArn}, is required

        stability
        :stability: experimental
        """
        self._values = {
            'cluster': cluster,
        }
        if service_arn is not None: self._values["service_arn"] = service_arn
        if service_name is not None: self._values["service_name"] = service_name

    @builtins.property
    def cluster(self) -> "ICluster":
        """The cluster that hosts the service.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @builtins.property
    def service_arn(self) -> typing.Optional[str]:
        """The service ARN.

        default
        :default: - either this, or {@link serviceName}, is required

        stability
        :stability: experimental
        """
        return self._values.get('service_arn')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """The name of the service.

        default
        :default: - either this, or {@link serviceArn}, is required

        stability
        :stability: experimental
        """
        return self._values.get('service_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FargateServiceAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.FargateServiceProps", jsii_struct_bases=[BaseServiceOptions], name_mapping={'cluster': 'cluster', 'cloud_map_options': 'cloudMapOptions', 'deployment_controller': 'deploymentController', 'desired_count': 'desiredCount', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'health_check_grace_period': 'healthCheckGracePeriod', 'max_healthy_percent': 'maxHealthyPercent', 'min_healthy_percent': 'minHealthyPercent', 'propagate_tags': 'propagateTags', 'service_name': 'serviceName', 'task_definition': 'taskDefinition', 'assign_public_ip': 'assignPublicIp', 'platform_version': 'platformVersion', 'propagate_task_tags_from': 'propagateTaskTagsFrom', 'security_group': 'securityGroup', 'security_groups': 'securityGroups', 'vpc_subnets': 'vpcSubnets'})
class FargateServiceProps(BaseServiceOptions):
    def __init__(self, *, cluster: "ICluster", cloud_map_options: typing.Optional["CloudMapOptions"]=None, deployment_controller: typing.Optional["DeploymentController"]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[_Duration_5170c158]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional["PropagatedTagSource"]=None, service_name: typing.Optional[str]=None, task_definition: "TaskDefinition", assign_public_ip: typing.Optional[bool]=None, platform_version: typing.Optional["FargatePlatformVersion"]=None, propagate_task_tags_from: typing.Optional["PropagatedTagSource"]=None, security_group: typing.Optional[_ISecurityGroup_d72ab8e8]=None, security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]]=None, vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6]=None) -> None:
        """The properties for defining a service using the Fargate launch type.

        :param cluster: The name of the cluster that hosts the service.
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param deployment_controller: Specifies which deployment controller to use for the service. For more information, see `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_ Default: - Rolling update (ECS)
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Valid values are: PropagatedTagSource.SERVICE, PropagatedTagSource.TASK_DEFINITION or PropagatedTagSource.NONE Default: PropagatedTagSource.NONE
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param task_definition: The task definition to use for tasks in the service. [disable-awslint:ref-via-interface]
        :param assign_public_ip: Specifies whether the task's elastic network interface receives a public IP address. If true, each task will receive a public IP address. Default: false
        :param platform_version: The platform version on which to run your service. If one is not specified, the LATEST platform version is used by default. For more information, see `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_ in the Amazon Elastic Container Service Developer Guide. Default: Latest
        :param propagate_task_tags_from: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: PropagatedTagSource.NONE
        :param security_group: The security groups to associate with the service. If you do not specify a security group, the default security group for the VPC is used. Default: - A new security group is created.
        :param security_groups: The security groups to associate with the service. If you do not specify a security group, the default security group for the VPC is used. Default: - A new security group is created.
        :param vpc_subnets: The subnets to associate with the service. Default: - Public subnets if ``assignPublicIp`` is set, otherwise the first available one of Private, Isolated, Public, in that order.

        stability
        :stability: experimental
        """
        if isinstance(cloud_map_options, dict): cloud_map_options = CloudMapOptions(**cloud_map_options)
        if isinstance(deployment_controller, dict): deployment_controller = DeploymentController(**deployment_controller)
        if isinstance(vpc_subnets, dict): vpc_subnets = _SubnetSelection_36a13cd6(**vpc_subnets)
        self._values = {
            'cluster': cluster,
            'task_definition': task_definition,
        }
        if cloud_map_options is not None: self._values["cloud_map_options"] = cloud_map_options
        if deployment_controller is not None: self._values["deployment_controller"] = deployment_controller
        if desired_count is not None: self._values["desired_count"] = desired_count
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None: self._values["health_check_grace_period"] = health_check_grace_period
        if max_healthy_percent is not None: self._values["max_healthy_percent"] = max_healthy_percent
        if min_healthy_percent is not None: self._values["min_healthy_percent"] = min_healthy_percent
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if service_name is not None: self._values["service_name"] = service_name
        if assign_public_ip is not None: self._values["assign_public_ip"] = assign_public_ip
        if platform_version is not None: self._values["platform_version"] = platform_version
        if propagate_task_tags_from is not None: self._values["propagate_task_tags_from"] = propagate_task_tags_from
        if security_group is not None: self._values["security_group"] = security_group
        if security_groups is not None: self._values["security_groups"] = security_groups
        if vpc_subnets is not None: self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def cluster(self) -> "ICluster":
        """The name of the cluster that hosts the service.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @builtins.property
    def cloud_map_options(self) -> typing.Optional["CloudMapOptions"]:
        """The options for configuring an Amazon ECS service to use service discovery.

        default
        :default: - AWS Cloud Map service discovery is not enabled.

        stability
        :stability: experimental
        """
        return self._values.get('cloud_map_options')

    @builtins.property
    def deployment_controller(self) -> typing.Optional["DeploymentController"]:
        """Specifies which deployment controller to use for the service.

        For more information, see
        `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_

        default
        :default: - Rolling update (ECS)

        stability
        :stability: experimental
        """
        return self._values.get('deployment_controller')

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('desired_count')

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('enable_ecs_managed_tags')

    @builtins.property
    def health_check_grace_period(self) -> typing.Optional[_Duration_5170c158]:
        """The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        default
        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set

        stability
        :stability: experimental
        """
        return self._values.get('health_check_grace_period')

    @builtins.property
    def max_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment.

        default
        :default: - 100 if daemon, otherwise 200

        stability
        :stability: experimental
        """
        return self._values.get('max_healthy_percent')

    @builtins.property
    def min_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment.

        default
        :default: - 0 if daemon, otherwise 50

        stability
        :stability: experimental
        """
        return self._values.get('min_healthy_percent')

    @builtins.property
    def propagate_tags(self) -> typing.Optional["PropagatedTagSource"]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Valid values are: PropagatedTagSource.SERVICE, PropagatedTagSource.TASK_DEFINITION or PropagatedTagSource.NONE

        default
        :default: PropagatedTagSource.NONE

        stability
        :stability: experimental
        """
        return self._values.get('propagate_tags')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """The name of the service.

        default
        :default: - CloudFormation-generated name.

        stability
        :stability: experimental
        """
        return self._values.get('service_name')

    @builtins.property
    def task_definition(self) -> "TaskDefinition":
        """The task definition to use for tasks in the service.

        [disable-awslint:ref-via-interface]

        stability
        :stability: experimental
        """
        return self._values.get('task_definition')

    @builtins.property
    def assign_public_ip(self) -> typing.Optional[bool]:
        """Specifies whether the task's elastic network interface receives a public IP address.

        If true, each task will receive a public IP address.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('assign_public_ip')

    @builtins.property
    def platform_version(self) -> typing.Optional["FargatePlatformVersion"]:
        """The platform version on which to run your service.

        If one is not specified, the LATEST platform version is used by default. For more information, see
        `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_
        in the Amazon Elastic Container Service Developer Guide.

        default
        :default: Latest

        stability
        :stability: experimental
        """
        return self._values.get('platform_version')

    @builtins.property
    def propagate_task_tags_from(self) -> typing.Optional["PropagatedTagSource"]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        default
        :default: PropagatedTagSource.NONE

        deprecated
        :deprecated: Use ``propagateTags`` instead.

        stability
        :stability: deprecated
        """
        return self._values.get('propagate_task_tags_from')

    @builtins.property
    def security_group(self) -> typing.Optional[_ISecurityGroup_d72ab8e8]:
        """The security groups to associate with the service.

        If you do not specify a security group, the default security group for the VPC is used.

        default
        :default: - A new security group is created.

        deprecated
        :deprecated: use securityGroups instead.

        stability
        :stability: deprecated
        """
        return self._values.get('security_group')

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]]:
        """The security groups to associate with the service.

        If you do not specify a security group, the default security group for the VPC is used.

        default
        :default: - A new security group is created.

        stability
        :stability: experimental
        """
        return self._values.get('security_groups')

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_36a13cd6]:
        """The subnets to associate with the service.

        default
        :default: - Public subnets if ``assignPublicIp`` is set, otherwise the first available one of Private, Isolated, Public, in that order.

        stability
        :stability: experimental
        """
        return self._values.get('vpc_subnets')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FargateServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.FargateTaskDefinitionProps", jsii_struct_bases=[CommonTaskDefinitionProps], name_mapping={'execution_role': 'executionRole', 'family': 'family', 'proxy_configuration': 'proxyConfiguration', 'task_role': 'taskRole', 'volumes': 'volumes', 'cpu': 'cpu', 'memory_limit_mib': 'memoryLimitMiB'})
class FargateTaskDefinitionProps(CommonTaskDefinitionProps):
    def __init__(self, *, execution_role: typing.Optional[_IRole_e69bbae4]=None, family: typing.Optional[str]=None, proxy_configuration: typing.Optional["ProxyConfiguration"]=None, task_role: typing.Optional[_IRole_e69bbae4]=None, volumes: typing.Optional[typing.List["Volume"]]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None) -> None:
        """The properties for a task definition.

        :param execution_role: The name of the IAM task execution role that grants the ECS agent to call AWS APIs on your behalf. The role will be used to retrieve container images from ECR and create CloudWatch log groups. Default: - An execution role will be automatically created if you use ECR images in your task definition.
        :param family: The name of a family that this task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param proxy_configuration: The configuration details for the App Mesh proxy. Default: - No proxy configuration.
        :param task_role: The name of the IAM role that grants containers in the task permission to call AWS APIs on your behalf. Default: - A task role is automatically created for you.
        :param volumes: The list of volume definitions for the task. For more information, see `Task Definition Parameter Volumes <https://docs.aws.amazon.com/AmazonECS/latest/developerguide//task_definition_parameters.html#volumes>`_. Default: - No volumes are passed to the Docker daemon on a container instance.
        :param cpu: The number of cpu units used by the task. For tasks using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) 512 (.5 vCPU) - Available memory values: 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) 1024 (1 vCPU) - Available memory values: 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) 2048 (2 vCPU) - Available memory values: Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) 4096 (4 vCPU) - Available memory values: Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) Default: 256
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. For tasks using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) Default: 512

        stability
        :stability: experimental
        """
        self._values = {
        }
        if execution_role is not None: self._values["execution_role"] = execution_role
        if family is not None: self._values["family"] = family
        if proxy_configuration is not None: self._values["proxy_configuration"] = proxy_configuration
        if task_role is not None: self._values["task_role"] = task_role
        if volumes is not None: self._values["volumes"] = volumes
        if cpu is not None: self._values["cpu"] = cpu
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib

    @builtins.property
    def execution_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The name of the IAM task execution role that grants the ECS agent to call AWS APIs on your behalf.

        The role will be used to retrieve container images from ECR and create CloudWatch log groups.

        default
        :default: - An execution role will be automatically created if you use ECR images in your task definition.

        stability
        :stability: experimental
        """
        return self._values.get('execution_role')

    @builtins.property
    def family(self) -> typing.Optional[str]:
        """The name of a family that this task definition is registered to.

        A family groups multiple versions of a task definition.

        default
        :default: - Automatically generated name.

        stability
        :stability: experimental
        """
        return self._values.get('family')

    @builtins.property
    def proxy_configuration(self) -> typing.Optional["ProxyConfiguration"]:
        """The configuration details for the App Mesh proxy.

        default
        :default: - No proxy configuration.

        stability
        :stability: experimental
        """
        return self._values.get('proxy_configuration')

    @builtins.property
    def task_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The name of the IAM role that grants containers in the task permission to call AWS APIs on your behalf.

        default
        :default: - A task role is automatically created for you.

        stability
        :stability: experimental
        """
        return self._values.get('task_role')

    @builtins.property
    def volumes(self) -> typing.Optional[typing.List["Volume"]]:
        """The list of volume definitions for the task.

        For more information, see
        `Task Definition Parameter Volumes <https://docs.aws.amazon.com/AmazonECS/latest/developerguide//task_definition_parameters.html#volumes>`_.

        default
        :default: - No volumes are passed to the Docker daemon on a container instance.

        stability
        :stability: experimental
        """
        return self._values.get('volumes')

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The number of cpu units used by the task.

        For tasks using the Fargate launch type,
        this field is required and you must use one of the following values,
        which determines your range of valid values for the memory parameter:

        256 (.25 vCPU) - Available memory values: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB)
        512 (.5 vCPU) - Available memory values: 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB)
        1024 (1 vCPU) - Available memory values: 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB)
        2048 (2 vCPU) - Available memory values: Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB)
        4096 (4 vCPU) - Available memory values: Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB)

        default
        :default: 256

        stability
        :stability: experimental
        """
        return self._values.get('cpu')

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The amount (in MiB) of memory used by the task.

        For tasks using the Fargate launch type,
        this field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter:

        512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU)
        1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU)
        2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU)
        Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU)
        Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU)

        default
        :default: 512

        stability
        :stability: experimental
        """
        return self._values.get('memory_limit_mib')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FargateTaskDefinitionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.FireLensLogDriverProps", jsii_struct_bases=[BaseLogDriverProps], name_mapping={'env': 'env', 'env_regex': 'envRegex', 'labels': 'labels', 'tag': 'tag', 'options': 'options'})
class FireLensLogDriverProps(BaseLogDriverProps):
    def __init__(self, *, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None, options: typing.Optional[typing.Mapping[str, str]]=None) -> None:
        """Specifies the firelens log driver configuration options.

        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID
        :param options: The configuration options to send to the log driver. Default: - the log driver options

        stability
        :stability: experimental
        """
        self._values = {
        }
        if env is not None: self._values["env"] = env
        if env_regex is not None: self._values["env_regex"] = env_regex
        if labels is not None: self._values["labels"] = labels
        if tag is not None: self._values["tag"] = tag
        if options is not None: self._values["options"] = options

    @builtins.property
    def env(self) -> typing.Optional[typing.List[str]]:
        """The env option takes an array of keys.

        If there is collision between
        label and env keys, the value of the env takes precedence. Adds additional fields
        to the extra attributes of a logging message.

        default
        :default: - No env

        stability
        :stability: experimental
        """
        return self._values.get('env')

    @builtins.property
    def env_regex(self) -> typing.Optional[str]:
        """The env-regex option is similar to and compatible with env.

        Its value is a regular
        expression to match logging-related environment variables. It is used for advanced
        log tag options.

        default
        :default: - No envRegex

        stability
        :stability: experimental
        """
        return self._values.get('env_regex')

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[str]]:
        """The labels option takes an array of keys.

        If there is collision
        between label and env keys, the value of the env takes precedence. Adds additional
        fields to the extra attributes of a logging message.

        default
        :default: - No labels

        stability
        :stability: experimental
        """
        return self._values.get('labels')

    @builtins.property
    def tag(self) -> typing.Optional[str]:
        """By default, Docker uses the first 12 characters of the container ID to tag log messages.

        Refer to the log tag option documentation for customizing the
        log tag format.

        default
        :default: - The first 12 characters of the container ID

        stability
        :stability: experimental
        """
        return self._values.get('tag')

    @builtins.property
    def options(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The configuration options to send to the log driver.

        default
        :default: - the log driver options

        stability
        :stability: experimental
        """
        return self._values.get('options')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FireLensLogDriverProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.FirelensConfig", jsii_struct_bases=[], name_mapping={'type': 'type', 'options': 'options'})
class FirelensConfig():
    def __init__(self, *, type: "FirelensLogRouterType", options: typing.Optional["FirelensOptions"]=None) -> None:
        """Firelens Configuration https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_firelens.html#firelens-taskdef.

        :param type: The log router to use. Default: - fluentbit
        :param options: Firelens options. Default: - no additional options

        stability
        :stability: experimental
        """
        if isinstance(options, dict): options = FirelensOptions(**options)
        self._values = {
            'type': type,
        }
        if options is not None: self._values["options"] = options

    @builtins.property
    def type(self) -> "FirelensLogRouterType":
        """The log router to use.

        default
        :default: - fluentbit

        stability
        :stability: experimental
        """
        return self._values.get('type')

    @builtins.property
    def options(self) -> typing.Optional["FirelensOptions"]:
        """Firelens options.

        default
        :default: - no additional options

        stability
        :stability: experimental
        """
        return self._values.get('options')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FirelensConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.aws_ecs.FirelensConfigFileType")
class FirelensConfigFileType(enum.Enum):
    """Firelens configuration file type, s3 or file path.

    https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_firelens.html#firelens-taskdef-customconfig

    stability
    :stability: experimental
    """
    S3 = "S3"
    """s3.

    stability
    :stability: experimental
    """
    FILE = "FILE"
    """fluentd.

    stability
    :stability: experimental
    """

class FirelensLogRouter(ContainerDefinition, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs.FirelensLogRouter"):
    """Firelens log router.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, firelens_config: "FirelensConfig", task_definition: "TaskDefinition", image: "ContainerImage", command: typing.Optional[typing.List[str]]=None, cpu: typing.Optional[jsii.Number]=None, disable_networking: typing.Optional[bool]=None, dns_search_domains: typing.Optional[typing.List[str]]=None, dns_servers: typing.Optional[typing.List[str]]=None, docker_labels: typing.Optional[typing.Mapping[str, str]]=None, docker_security_options: typing.Optional[typing.List[str]]=None, entry_point: typing.Optional[typing.List[str]]=None, environment: typing.Optional[typing.Mapping[str, str]]=None, essential: typing.Optional[bool]=None, extra_hosts: typing.Optional[typing.Mapping[str, str]]=None, gpu_count: typing.Optional[jsii.Number]=None, health_check: typing.Optional["HealthCheck"]=None, hostname: typing.Optional[str]=None, linux_parameters: typing.Optional["LinuxParameters"]=None, logging: typing.Optional["LogDriver"]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None, privileged: typing.Optional[bool]=None, readonly_root_filesystem: typing.Optional[bool]=None, secrets: typing.Optional[typing.Mapping[str, "Secret"]]=None, start_timeout: typing.Optional[_Duration_5170c158]=None, stop_timeout: typing.Optional[_Duration_5170c158]=None, user: typing.Optional[str]=None, working_directory: typing.Optional[str]=None) -> None:
        """Constructs a new instance of the FirelensLogRouter class.

        :param scope: -
        :param id: -
        :param firelens_config: Firelens configuration.
        :param task_definition: The name of the task definition that includes this container definition. [disable-awslint:ref-via-interface]
        :param image: The image used to start a container. This string is passed directly to the Docker daemon. Images in the Docker Hub registry are available by default. Other repositories are specified with either repository-url/image:tag or repository-url/image@digest. TODO: Update these to specify using classes of IContainerImage
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param cpu: The minimum number of CPU units to reserve for the container. Default: - No minimum CPU units reserved.
        :param disable_networking: Specifies whether networking is disabled within the container. When this parameter is true, networking is disabled within the container. Default: false
        :param dns_search_domains: A list of DNS search domains that are presented to the container. Default: - No search domains.
        :param dns_servers: A list of DNS servers that are presented to the container. Default: - Default DNS servers.
        :param docker_labels: A key/value map of labels to add to the container. Default: - No labels.
        :param docker_security_options: A list of strings to provide custom labels for SELinux and AppArmor multi-level security systems. Default: - No security labels.
        :param entry_point: The ENTRYPOINT value to pass to the container. Default: - Entry point configured in container.
        :param environment: The environment variables to pass to the container. Default: - No environment variables.
        :param essential: Specifies whether the container is marked essential. If the essential parameter of a container is marked as true, and that container fails or stops for any reason, all other containers that are part of the task are stopped. If the essential parameter of a container is marked as false, then its failure does not affect the rest of the containers in a task. All tasks must have at least one essential container. If this parameter is omitted, a container is assumed to be essential. Default: true
        :param extra_hosts: A list of hostnames and IP address mappings to append to the /etc/hosts file on the container. Default: - No extra hosts.
        :param gpu_count: The number of GPUs assigned to the container. Default: - No GPUs assigned.
        :param health_check: The health check command and associated configuration parameters for the container. Default: - Health check configuration from container.
        :param hostname: The hostname to use for your container. Default: - Automatic hostname.
        :param linux_parameters: Linux-specific modifications that are applied to the container, such as Linux kernel capabilities. For more information see `KernelCapabilities <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_KernelCapabilities.html>`_. Default: - No Linux parameters.
        :param logging: The log configuration specification for the container. Default: - Containers use the same logging driver that the Docker daemon uses.
        :param memory_limit_mib: The amount (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under heavy contention, Docker attempts to keep the container memory to this soft limit. However, your container can consume more memory when it needs to, up to either the hard limit specified with the memory parameter (if applicable), or all of the available memory on the container instance, whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory reserved.
        :param privileged: Specifies whether the container is marked as privileged. When this parameter is true, the container is given elevated privileges on the host container instance (similar to the root user). Default: false
        :param readonly_root_filesystem: When this parameter is true, the container is given read-only access to its root file system. Default: false
        :param secrets: The secret environment variables to pass to the container. Default: - No secret environment variables.
        :param start_timeout: Time duration (in seconds) to wait before giving up on resolving dependencies for a container. Default: - none
        :param stop_timeout: Time duration (in seconds) to wait before the container is forcefully killed if it doesn't exit normally on its own. Default: - none
        :param user: The user name to use inside the container. Default: root
        :param working_directory: The working directory in which to run commands inside the container. Default: /

        stability
        :stability: experimental
        """
        props = FirelensLogRouterProps(firelens_config=firelens_config, task_definition=task_definition, image=image, command=command, cpu=cpu, disable_networking=disable_networking, dns_search_domains=dns_search_domains, dns_servers=dns_servers, docker_labels=docker_labels, docker_security_options=docker_security_options, entry_point=entry_point, environment=environment, essential=essential, extra_hosts=extra_hosts, gpu_count=gpu_count, health_check=health_check, hostname=hostname, linux_parameters=linux_parameters, logging=logging, memory_limit_mib=memory_limit_mib, memory_reservation_mib=memory_reservation_mib, privileged=privileged, readonly_root_filesystem=readonly_root_filesystem, secrets=secrets, start_timeout=start_timeout, stop_timeout=stop_timeout, user=user, working_directory=working_directory)

        jsii.create(FirelensLogRouter, self, [scope, id, props])

    @jsii.member(jsii_name="renderContainerDefinition")
    def render_container_definition(self, _task_definition: typing.Optional["TaskDefinition"]=None) -> "CfnTaskDefinition.ContainerDefinitionProperty":
        """Render this container definition to a CloudFormation object.

        :param _task_definition: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "renderContainerDefinition", [_task_definition])

    @builtins.property
    @jsii.member(jsii_name="firelensConfig")
    def firelens_config(self) -> "FirelensConfig":
        """Firelens configuration.

        stability
        :stability: experimental
        """
        return jsii.get(self, "firelensConfig")


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.FirelensLogRouterDefinitionOptions", jsii_struct_bases=[ContainerDefinitionOptions], name_mapping={'image': 'image', 'command': 'command', 'cpu': 'cpu', 'disable_networking': 'disableNetworking', 'dns_search_domains': 'dnsSearchDomains', 'dns_servers': 'dnsServers', 'docker_labels': 'dockerLabels', 'docker_security_options': 'dockerSecurityOptions', 'entry_point': 'entryPoint', 'environment': 'environment', 'essential': 'essential', 'extra_hosts': 'extraHosts', 'gpu_count': 'gpuCount', 'health_check': 'healthCheck', 'hostname': 'hostname', 'linux_parameters': 'linuxParameters', 'logging': 'logging', 'memory_limit_mib': 'memoryLimitMiB', 'memory_reservation_mib': 'memoryReservationMiB', 'privileged': 'privileged', 'readonly_root_filesystem': 'readonlyRootFilesystem', 'secrets': 'secrets', 'start_timeout': 'startTimeout', 'stop_timeout': 'stopTimeout', 'user': 'user', 'working_directory': 'workingDirectory', 'firelens_config': 'firelensConfig'})
class FirelensLogRouterDefinitionOptions(ContainerDefinitionOptions):
    def __init__(self, *, image: "ContainerImage", command: typing.Optional[typing.List[str]]=None, cpu: typing.Optional[jsii.Number]=None, disable_networking: typing.Optional[bool]=None, dns_search_domains: typing.Optional[typing.List[str]]=None, dns_servers: typing.Optional[typing.List[str]]=None, docker_labels: typing.Optional[typing.Mapping[str, str]]=None, docker_security_options: typing.Optional[typing.List[str]]=None, entry_point: typing.Optional[typing.List[str]]=None, environment: typing.Optional[typing.Mapping[str, str]]=None, essential: typing.Optional[bool]=None, extra_hosts: typing.Optional[typing.Mapping[str, str]]=None, gpu_count: typing.Optional[jsii.Number]=None, health_check: typing.Optional["HealthCheck"]=None, hostname: typing.Optional[str]=None, linux_parameters: typing.Optional["LinuxParameters"]=None, logging: typing.Optional["LogDriver"]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None, privileged: typing.Optional[bool]=None, readonly_root_filesystem: typing.Optional[bool]=None, secrets: typing.Optional[typing.Mapping[str, "Secret"]]=None, start_timeout: typing.Optional[_Duration_5170c158]=None, stop_timeout: typing.Optional[_Duration_5170c158]=None, user: typing.Optional[str]=None, working_directory: typing.Optional[str]=None, firelens_config: "FirelensConfig") -> None:
        """The options for creating a firelens log router.

        :param image: The image used to start a container. This string is passed directly to the Docker daemon. Images in the Docker Hub registry are available by default. Other repositories are specified with either repository-url/image:tag or repository-url/image@digest. TODO: Update these to specify using classes of IContainerImage
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param cpu: The minimum number of CPU units to reserve for the container. Default: - No minimum CPU units reserved.
        :param disable_networking: Specifies whether networking is disabled within the container. When this parameter is true, networking is disabled within the container. Default: false
        :param dns_search_domains: A list of DNS search domains that are presented to the container. Default: - No search domains.
        :param dns_servers: A list of DNS servers that are presented to the container. Default: - Default DNS servers.
        :param docker_labels: A key/value map of labels to add to the container. Default: - No labels.
        :param docker_security_options: A list of strings to provide custom labels for SELinux and AppArmor multi-level security systems. Default: - No security labels.
        :param entry_point: The ENTRYPOINT value to pass to the container. Default: - Entry point configured in container.
        :param environment: The environment variables to pass to the container. Default: - No environment variables.
        :param essential: Specifies whether the container is marked essential. If the essential parameter of a container is marked as true, and that container fails or stops for any reason, all other containers that are part of the task are stopped. If the essential parameter of a container is marked as false, then its failure does not affect the rest of the containers in a task. All tasks must have at least one essential container. If this parameter is omitted, a container is assumed to be essential. Default: true
        :param extra_hosts: A list of hostnames and IP address mappings to append to the /etc/hosts file on the container. Default: - No extra hosts.
        :param gpu_count: The number of GPUs assigned to the container. Default: - No GPUs assigned.
        :param health_check: The health check command and associated configuration parameters for the container. Default: - Health check configuration from container.
        :param hostname: The hostname to use for your container. Default: - Automatic hostname.
        :param linux_parameters: Linux-specific modifications that are applied to the container, such as Linux kernel capabilities. For more information see `KernelCapabilities <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_KernelCapabilities.html>`_. Default: - No Linux parameters.
        :param logging: The log configuration specification for the container. Default: - Containers use the same logging driver that the Docker daemon uses.
        :param memory_limit_mib: The amount (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under heavy contention, Docker attempts to keep the container memory to this soft limit. However, your container can consume more memory when it needs to, up to either the hard limit specified with the memory parameter (if applicable), or all of the available memory on the container instance, whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory reserved.
        :param privileged: Specifies whether the container is marked as privileged. When this parameter is true, the container is given elevated privileges on the host container instance (similar to the root user). Default: false
        :param readonly_root_filesystem: When this parameter is true, the container is given read-only access to its root file system. Default: false
        :param secrets: The secret environment variables to pass to the container. Default: - No secret environment variables.
        :param start_timeout: Time duration (in seconds) to wait before giving up on resolving dependencies for a container. Default: - none
        :param stop_timeout: Time duration (in seconds) to wait before the container is forcefully killed if it doesn't exit normally on its own. Default: - none
        :param user: The user name to use inside the container. Default: root
        :param working_directory: The working directory in which to run commands inside the container. Default: /
        :param firelens_config: Firelens configuration.

        stability
        :stability: experimental
        """
        if isinstance(health_check, dict): health_check = HealthCheck(**health_check)
        if isinstance(firelens_config, dict): firelens_config = FirelensConfig(**firelens_config)
        self._values = {
            'image': image,
            'firelens_config': firelens_config,
        }
        if command is not None: self._values["command"] = command
        if cpu is not None: self._values["cpu"] = cpu
        if disable_networking is not None: self._values["disable_networking"] = disable_networking
        if dns_search_domains is not None: self._values["dns_search_domains"] = dns_search_domains
        if dns_servers is not None: self._values["dns_servers"] = dns_servers
        if docker_labels is not None: self._values["docker_labels"] = docker_labels
        if docker_security_options is not None: self._values["docker_security_options"] = docker_security_options
        if entry_point is not None: self._values["entry_point"] = entry_point
        if environment is not None: self._values["environment"] = environment
        if essential is not None: self._values["essential"] = essential
        if extra_hosts is not None: self._values["extra_hosts"] = extra_hosts
        if gpu_count is not None: self._values["gpu_count"] = gpu_count
        if health_check is not None: self._values["health_check"] = health_check
        if hostname is not None: self._values["hostname"] = hostname
        if linux_parameters is not None: self._values["linux_parameters"] = linux_parameters
        if logging is not None: self._values["logging"] = logging
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib
        if memory_reservation_mib is not None: self._values["memory_reservation_mib"] = memory_reservation_mib
        if privileged is not None: self._values["privileged"] = privileged
        if readonly_root_filesystem is not None: self._values["readonly_root_filesystem"] = readonly_root_filesystem
        if secrets is not None: self._values["secrets"] = secrets
        if start_timeout is not None: self._values["start_timeout"] = start_timeout
        if stop_timeout is not None: self._values["stop_timeout"] = stop_timeout
        if user is not None: self._values["user"] = user
        if working_directory is not None: self._values["working_directory"] = working_directory

    @builtins.property
    def image(self) -> "ContainerImage":
        """The image used to start a container.

        This string is passed directly to the Docker daemon.
        Images in the Docker Hub registry are available by default.
        Other repositories are specified with either repository-url/image:tag or repository-url/image@digest.
        TODO: Update these to specify using classes of IContainerImage

        stability
        :stability: experimental
        """
        return self._values.get('image')

    @builtins.property
    def command(self) -> typing.Optional[typing.List[str]]:
        """The command that is passed to the container.

        If you provide a shell command as a single string, you have to quote command-line arguments.

        default
        :default: - CMD value built into container image.

        stability
        :stability: experimental
        """
        return self._values.get('command')

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The minimum number of CPU units to reserve for the container.

        default
        :default: - No minimum CPU units reserved.

        stability
        :stability: experimental
        """
        return self._values.get('cpu')

    @builtins.property
    def disable_networking(self) -> typing.Optional[bool]:
        """Specifies whether networking is disabled within the container.

        When this parameter is true, networking is disabled within the container.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('disable_networking')

    @builtins.property
    def dns_search_domains(self) -> typing.Optional[typing.List[str]]:
        """A list of DNS search domains that are presented to the container.

        default
        :default: - No search domains.

        stability
        :stability: experimental
        """
        return self._values.get('dns_search_domains')

    @builtins.property
    def dns_servers(self) -> typing.Optional[typing.List[str]]:
        """A list of DNS servers that are presented to the container.

        default
        :default: - Default DNS servers.

        stability
        :stability: experimental
        """
        return self._values.get('dns_servers')

    @builtins.property
    def docker_labels(self) -> typing.Optional[typing.Mapping[str, str]]:
        """A key/value map of labels to add to the container.

        default
        :default: - No labels.

        stability
        :stability: experimental
        """
        return self._values.get('docker_labels')

    @builtins.property
    def docker_security_options(self) -> typing.Optional[typing.List[str]]:
        """A list of strings to provide custom labels for SELinux and AppArmor multi-level security systems.

        default
        :default: - No security labels.

        stability
        :stability: experimental
        """
        return self._values.get('docker_security_options')

    @builtins.property
    def entry_point(self) -> typing.Optional[typing.List[str]]:
        """The ENTRYPOINT value to pass to the container.

        default
        :default: - Entry point configured in container.

        see
        :see: https://docs.docker.com/engine/reference/builder/#entrypoint
        stability
        :stability: experimental
        """
        return self._values.get('entry_point')

    @builtins.property
    def environment(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The environment variables to pass to the container.

        default
        :default: - No environment variables.

        stability
        :stability: experimental
        """
        return self._values.get('environment')

    @builtins.property
    def essential(self) -> typing.Optional[bool]:
        """Specifies whether the container is marked essential.

        If the essential parameter of a container is marked as true, and that container fails
        or stops for any reason, all other containers that are part of the task are stopped.
        If the essential parameter of a container is marked as false, then its failure does not
        affect the rest of the containers in a task. All tasks must have at least one essential container.

        If this parameter is omitted, a container is assumed to be essential.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('essential')

    @builtins.property
    def extra_hosts(self) -> typing.Optional[typing.Mapping[str, str]]:
        """A list of hostnames and IP address mappings to append to the /etc/hosts file on the container.

        default
        :default: - No extra hosts.

        stability
        :stability: experimental
        """
        return self._values.get('extra_hosts')

    @builtins.property
    def gpu_count(self) -> typing.Optional[jsii.Number]:
        """The number of GPUs assigned to the container.

        default
        :default: - No GPUs assigned.

        stability
        :stability: experimental
        """
        return self._values.get('gpu_count')

    @builtins.property
    def health_check(self) -> typing.Optional["HealthCheck"]:
        """The health check command and associated configuration parameters for the container.

        default
        :default: - Health check configuration from container.

        stability
        :stability: experimental
        """
        return self._values.get('health_check')

    @builtins.property
    def hostname(self) -> typing.Optional[str]:
        """The hostname to use for your container.

        default
        :default: - Automatic hostname.

        stability
        :stability: experimental
        """
        return self._values.get('hostname')

    @builtins.property
    def linux_parameters(self) -> typing.Optional["LinuxParameters"]:
        """Linux-specific modifications that are applied to the container, such as Linux kernel capabilities.

        For more information see `KernelCapabilities <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_KernelCapabilities.html>`_.

        default
        :default: - No Linux parameters.

        stability
        :stability: experimental
        """
        return self._values.get('linux_parameters')

    @builtins.property
    def logging(self) -> typing.Optional["LogDriver"]:
        """The log configuration specification for the container.

        default
        :default: - Containers use the same logging driver that the Docker daemon uses.

        stability
        :stability: experimental
        """
        return self._values.get('logging')

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The amount (in MiB) of memory to present to the container.

        If your container attempts to exceed the allocated memory, the container
        is terminated.

        At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

        default
        :default: - No memory limit.

        stability
        :stability: experimental
        """
        return self._values.get('memory_limit_mib')

    @builtins.property
    def memory_reservation_mib(self) -> typing.Optional[jsii.Number]:
        """The soft limit (in MiB) of memory to reserve for the container.

        When system memory is under heavy contention, Docker attempts to keep the
        container memory to this soft limit. However, your container can consume more
        memory when it needs to, up to either the hard limit specified with the memory
        parameter (if applicable), or all of the available memory on the container
        instance, whichever comes first.

        At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

        default
        :default: - No memory reserved.

        stability
        :stability: experimental
        """
        return self._values.get('memory_reservation_mib')

    @builtins.property
    def privileged(self) -> typing.Optional[bool]:
        """Specifies whether the container is marked as privileged.

        When this parameter is true, the container is given elevated privileges on the host container instance (similar to the root user).

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('privileged')

    @builtins.property
    def readonly_root_filesystem(self) -> typing.Optional[bool]:
        """When this parameter is true, the container is given read-only access to its root file system.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('readonly_root_filesystem')

    @builtins.property
    def secrets(self) -> typing.Optional[typing.Mapping[str, "Secret"]]:
        """The secret environment variables to pass to the container.

        default
        :default: - No secret environment variables.

        stability
        :stability: experimental
        """
        return self._values.get('secrets')

    @builtins.property
    def start_timeout(self) -> typing.Optional[_Duration_5170c158]:
        """Time duration (in seconds) to wait before giving up on resolving dependencies for a container.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('start_timeout')

    @builtins.property
    def stop_timeout(self) -> typing.Optional[_Duration_5170c158]:
        """Time duration (in seconds) to wait before the container is forcefully killed if it doesn't exit normally on its own.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('stop_timeout')

    @builtins.property
    def user(self) -> typing.Optional[str]:
        """The user name to use inside the container.

        default
        :default: root

        stability
        :stability: experimental
        """
        return self._values.get('user')

    @builtins.property
    def working_directory(self) -> typing.Optional[str]:
        """The working directory in which to run commands inside the container.

        default
        :default: /

        stability
        :stability: experimental
        """
        return self._values.get('working_directory')

    @builtins.property
    def firelens_config(self) -> "FirelensConfig":
        """Firelens configuration.

        stability
        :stability: experimental
        """
        return self._values.get('firelens_config')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FirelensLogRouterDefinitionOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.FirelensLogRouterProps", jsii_struct_bases=[ContainerDefinitionProps], name_mapping={'image': 'image', 'command': 'command', 'cpu': 'cpu', 'disable_networking': 'disableNetworking', 'dns_search_domains': 'dnsSearchDomains', 'dns_servers': 'dnsServers', 'docker_labels': 'dockerLabels', 'docker_security_options': 'dockerSecurityOptions', 'entry_point': 'entryPoint', 'environment': 'environment', 'essential': 'essential', 'extra_hosts': 'extraHosts', 'gpu_count': 'gpuCount', 'health_check': 'healthCheck', 'hostname': 'hostname', 'linux_parameters': 'linuxParameters', 'logging': 'logging', 'memory_limit_mib': 'memoryLimitMiB', 'memory_reservation_mib': 'memoryReservationMiB', 'privileged': 'privileged', 'readonly_root_filesystem': 'readonlyRootFilesystem', 'secrets': 'secrets', 'start_timeout': 'startTimeout', 'stop_timeout': 'stopTimeout', 'user': 'user', 'working_directory': 'workingDirectory', 'task_definition': 'taskDefinition', 'firelens_config': 'firelensConfig'})
class FirelensLogRouterProps(ContainerDefinitionProps):
    def __init__(self, *, image: "ContainerImage", command: typing.Optional[typing.List[str]]=None, cpu: typing.Optional[jsii.Number]=None, disable_networking: typing.Optional[bool]=None, dns_search_domains: typing.Optional[typing.List[str]]=None, dns_servers: typing.Optional[typing.List[str]]=None, docker_labels: typing.Optional[typing.Mapping[str, str]]=None, docker_security_options: typing.Optional[typing.List[str]]=None, entry_point: typing.Optional[typing.List[str]]=None, environment: typing.Optional[typing.Mapping[str, str]]=None, essential: typing.Optional[bool]=None, extra_hosts: typing.Optional[typing.Mapping[str, str]]=None, gpu_count: typing.Optional[jsii.Number]=None, health_check: typing.Optional["HealthCheck"]=None, hostname: typing.Optional[str]=None, linux_parameters: typing.Optional["LinuxParameters"]=None, logging: typing.Optional["LogDriver"]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None, privileged: typing.Optional[bool]=None, readonly_root_filesystem: typing.Optional[bool]=None, secrets: typing.Optional[typing.Mapping[str, "Secret"]]=None, start_timeout: typing.Optional[_Duration_5170c158]=None, stop_timeout: typing.Optional[_Duration_5170c158]=None, user: typing.Optional[str]=None, working_directory: typing.Optional[str]=None, task_definition: "TaskDefinition", firelens_config: "FirelensConfig") -> None:
        """The properties in a firelens log router.

        :param image: The image used to start a container. This string is passed directly to the Docker daemon. Images in the Docker Hub registry are available by default. Other repositories are specified with either repository-url/image:tag or repository-url/image@digest. TODO: Update these to specify using classes of IContainerImage
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param cpu: The minimum number of CPU units to reserve for the container. Default: - No minimum CPU units reserved.
        :param disable_networking: Specifies whether networking is disabled within the container. When this parameter is true, networking is disabled within the container. Default: false
        :param dns_search_domains: A list of DNS search domains that are presented to the container. Default: - No search domains.
        :param dns_servers: A list of DNS servers that are presented to the container. Default: - Default DNS servers.
        :param docker_labels: A key/value map of labels to add to the container. Default: - No labels.
        :param docker_security_options: A list of strings to provide custom labels for SELinux and AppArmor multi-level security systems. Default: - No security labels.
        :param entry_point: The ENTRYPOINT value to pass to the container. Default: - Entry point configured in container.
        :param environment: The environment variables to pass to the container. Default: - No environment variables.
        :param essential: Specifies whether the container is marked essential. If the essential parameter of a container is marked as true, and that container fails or stops for any reason, all other containers that are part of the task are stopped. If the essential parameter of a container is marked as false, then its failure does not affect the rest of the containers in a task. All tasks must have at least one essential container. If this parameter is omitted, a container is assumed to be essential. Default: true
        :param extra_hosts: A list of hostnames and IP address mappings to append to the /etc/hosts file on the container. Default: - No extra hosts.
        :param gpu_count: The number of GPUs assigned to the container. Default: - No GPUs assigned.
        :param health_check: The health check command and associated configuration parameters for the container. Default: - Health check configuration from container.
        :param hostname: The hostname to use for your container. Default: - Automatic hostname.
        :param linux_parameters: Linux-specific modifications that are applied to the container, such as Linux kernel capabilities. For more information see `KernelCapabilities <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_KernelCapabilities.html>`_. Default: - No Linux parameters.
        :param logging: The log configuration specification for the container. Default: - Containers use the same logging driver that the Docker daemon uses.
        :param memory_limit_mib: The amount (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under heavy contention, Docker attempts to keep the container memory to this soft limit. However, your container can consume more memory when it needs to, up to either the hard limit specified with the memory parameter (if applicable), or all of the available memory on the container instance, whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory reserved.
        :param privileged: Specifies whether the container is marked as privileged. When this parameter is true, the container is given elevated privileges on the host container instance (similar to the root user). Default: false
        :param readonly_root_filesystem: When this parameter is true, the container is given read-only access to its root file system. Default: false
        :param secrets: The secret environment variables to pass to the container. Default: - No secret environment variables.
        :param start_timeout: Time duration (in seconds) to wait before giving up on resolving dependencies for a container. Default: - none
        :param stop_timeout: Time duration (in seconds) to wait before the container is forcefully killed if it doesn't exit normally on its own. Default: - none
        :param user: The user name to use inside the container. Default: root
        :param working_directory: The working directory in which to run commands inside the container. Default: /
        :param task_definition: The name of the task definition that includes this container definition. [disable-awslint:ref-via-interface]
        :param firelens_config: Firelens configuration.

        stability
        :stability: experimental
        """
        if isinstance(health_check, dict): health_check = HealthCheck(**health_check)
        if isinstance(firelens_config, dict): firelens_config = FirelensConfig(**firelens_config)
        self._values = {
            'image': image,
            'task_definition': task_definition,
            'firelens_config': firelens_config,
        }
        if command is not None: self._values["command"] = command
        if cpu is not None: self._values["cpu"] = cpu
        if disable_networking is not None: self._values["disable_networking"] = disable_networking
        if dns_search_domains is not None: self._values["dns_search_domains"] = dns_search_domains
        if dns_servers is not None: self._values["dns_servers"] = dns_servers
        if docker_labels is not None: self._values["docker_labels"] = docker_labels
        if docker_security_options is not None: self._values["docker_security_options"] = docker_security_options
        if entry_point is not None: self._values["entry_point"] = entry_point
        if environment is not None: self._values["environment"] = environment
        if essential is not None: self._values["essential"] = essential
        if extra_hosts is not None: self._values["extra_hosts"] = extra_hosts
        if gpu_count is not None: self._values["gpu_count"] = gpu_count
        if health_check is not None: self._values["health_check"] = health_check
        if hostname is not None: self._values["hostname"] = hostname
        if linux_parameters is not None: self._values["linux_parameters"] = linux_parameters
        if logging is not None: self._values["logging"] = logging
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib
        if memory_reservation_mib is not None: self._values["memory_reservation_mib"] = memory_reservation_mib
        if privileged is not None: self._values["privileged"] = privileged
        if readonly_root_filesystem is not None: self._values["readonly_root_filesystem"] = readonly_root_filesystem
        if secrets is not None: self._values["secrets"] = secrets
        if start_timeout is not None: self._values["start_timeout"] = start_timeout
        if stop_timeout is not None: self._values["stop_timeout"] = stop_timeout
        if user is not None: self._values["user"] = user
        if working_directory is not None: self._values["working_directory"] = working_directory

    @builtins.property
    def image(self) -> "ContainerImage":
        """The image used to start a container.

        This string is passed directly to the Docker daemon.
        Images in the Docker Hub registry are available by default.
        Other repositories are specified with either repository-url/image:tag or repository-url/image@digest.
        TODO: Update these to specify using classes of IContainerImage

        stability
        :stability: experimental
        """
        return self._values.get('image')

    @builtins.property
    def command(self) -> typing.Optional[typing.List[str]]:
        """The command that is passed to the container.

        If you provide a shell command as a single string, you have to quote command-line arguments.

        default
        :default: - CMD value built into container image.

        stability
        :stability: experimental
        """
        return self._values.get('command')

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The minimum number of CPU units to reserve for the container.

        default
        :default: - No minimum CPU units reserved.

        stability
        :stability: experimental
        """
        return self._values.get('cpu')

    @builtins.property
    def disable_networking(self) -> typing.Optional[bool]:
        """Specifies whether networking is disabled within the container.

        When this parameter is true, networking is disabled within the container.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('disable_networking')

    @builtins.property
    def dns_search_domains(self) -> typing.Optional[typing.List[str]]:
        """A list of DNS search domains that are presented to the container.

        default
        :default: - No search domains.

        stability
        :stability: experimental
        """
        return self._values.get('dns_search_domains')

    @builtins.property
    def dns_servers(self) -> typing.Optional[typing.List[str]]:
        """A list of DNS servers that are presented to the container.

        default
        :default: - Default DNS servers.

        stability
        :stability: experimental
        """
        return self._values.get('dns_servers')

    @builtins.property
    def docker_labels(self) -> typing.Optional[typing.Mapping[str, str]]:
        """A key/value map of labels to add to the container.

        default
        :default: - No labels.

        stability
        :stability: experimental
        """
        return self._values.get('docker_labels')

    @builtins.property
    def docker_security_options(self) -> typing.Optional[typing.List[str]]:
        """A list of strings to provide custom labels for SELinux and AppArmor multi-level security systems.

        default
        :default: - No security labels.

        stability
        :stability: experimental
        """
        return self._values.get('docker_security_options')

    @builtins.property
    def entry_point(self) -> typing.Optional[typing.List[str]]:
        """The ENTRYPOINT value to pass to the container.

        default
        :default: - Entry point configured in container.

        see
        :see: https://docs.docker.com/engine/reference/builder/#entrypoint
        stability
        :stability: experimental
        """
        return self._values.get('entry_point')

    @builtins.property
    def environment(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The environment variables to pass to the container.

        default
        :default: - No environment variables.

        stability
        :stability: experimental
        """
        return self._values.get('environment')

    @builtins.property
    def essential(self) -> typing.Optional[bool]:
        """Specifies whether the container is marked essential.

        If the essential parameter of a container is marked as true, and that container fails
        or stops for any reason, all other containers that are part of the task are stopped.
        If the essential parameter of a container is marked as false, then its failure does not
        affect the rest of the containers in a task. All tasks must have at least one essential container.

        If this parameter is omitted, a container is assumed to be essential.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('essential')

    @builtins.property
    def extra_hosts(self) -> typing.Optional[typing.Mapping[str, str]]:
        """A list of hostnames and IP address mappings to append to the /etc/hosts file on the container.

        default
        :default: - No extra hosts.

        stability
        :stability: experimental
        """
        return self._values.get('extra_hosts')

    @builtins.property
    def gpu_count(self) -> typing.Optional[jsii.Number]:
        """The number of GPUs assigned to the container.

        default
        :default: - No GPUs assigned.

        stability
        :stability: experimental
        """
        return self._values.get('gpu_count')

    @builtins.property
    def health_check(self) -> typing.Optional["HealthCheck"]:
        """The health check command and associated configuration parameters for the container.

        default
        :default: - Health check configuration from container.

        stability
        :stability: experimental
        """
        return self._values.get('health_check')

    @builtins.property
    def hostname(self) -> typing.Optional[str]:
        """The hostname to use for your container.

        default
        :default: - Automatic hostname.

        stability
        :stability: experimental
        """
        return self._values.get('hostname')

    @builtins.property
    def linux_parameters(self) -> typing.Optional["LinuxParameters"]:
        """Linux-specific modifications that are applied to the container, such as Linux kernel capabilities.

        For more information see `KernelCapabilities <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_KernelCapabilities.html>`_.

        default
        :default: - No Linux parameters.

        stability
        :stability: experimental
        """
        return self._values.get('linux_parameters')

    @builtins.property
    def logging(self) -> typing.Optional["LogDriver"]:
        """The log configuration specification for the container.

        default
        :default: - Containers use the same logging driver that the Docker daemon uses.

        stability
        :stability: experimental
        """
        return self._values.get('logging')

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The amount (in MiB) of memory to present to the container.

        If your container attempts to exceed the allocated memory, the container
        is terminated.

        At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

        default
        :default: - No memory limit.

        stability
        :stability: experimental
        """
        return self._values.get('memory_limit_mib')

    @builtins.property
    def memory_reservation_mib(self) -> typing.Optional[jsii.Number]:
        """The soft limit (in MiB) of memory to reserve for the container.

        When system memory is under heavy contention, Docker attempts to keep the
        container memory to this soft limit. However, your container can consume more
        memory when it needs to, up to either the hard limit specified with the memory
        parameter (if applicable), or all of the available memory on the container
        instance, whichever comes first.

        At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

        default
        :default: - No memory reserved.

        stability
        :stability: experimental
        """
        return self._values.get('memory_reservation_mib')

    @builtins.property
    def privileged(self) -> typing.Optional[bool]:
        """Specifies whether the container is marked as privileged.

        When this parameter is true, the container is given elevated privileges on the host container instance (similar to the root user).

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('privileged')

    @builtins.property
    def readonly_root_filesystem(self) -> typing.Optional[bool]:
        """When this parameter is true, the container is given read-only access to its root file system.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('readonly_root_filesystem')

    @builtins.property
    def secrets(self) -> typing.Optional[typing.Mapping[str, "Secret"]]:
        """The secret environment variables to pass to the container.

        default
        :default: - No secret environment variables.

        stability
        :stability: experimental
        """
        return self._values.get('secrets')

    @builtins.property
    def start_timeout(self) -> typing.Optional[_Duration_5170c158]:
        """Time duration (in seconds) to wait before giving up on resolving dependencies for a container.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('start_timeout')

    @builtins.property
    def stop_timeout(self) -> typing.Optional[_Duration_5170c158]:
        """Time duration (in seconds) to wait before the container is forcefully killed if it doesn't exit normally on its own.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('stop_timeout')

    @builtins.property
    def user(self) -> typing.Optional[str]:
        """The user name to use inside the container.

        default
        :default: root

        stability
        :stability: experimental
        """
        return self._values.get('user')

    @builtins.property
    def working_directory(self) -> typing.Optional[str]:
        """The working directory in which to run commands inside the container.

        default
        :default: /

        stability
        :stability: experimental
        """
        return self._values.get('working_directory')

    @builtins.property
    def task_definition(self) -> "TaskDefinition":
        """The name of the task definition that includes this container definition.

        [disable-awslint:ref-via-interface]

        stability
        :stability: experimental
        """
        return self._values.get('task_definition')

    @builtins.property
    def firelens_config(self) -> "FirelensConfig":
        """Firelens configuration.

        stability
        :stability: experimental
        """
        return self._values.get('firelens_config')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FirelensLogRouterProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.aws_ecs.FirelensLogRouterType")
class FirelensLogRouterType(enum.Enum):
    """Firelens log router type, fluentbit or fluentd.

    https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_firelens.html

    stability
    :stability: experimental
    """
    FLUENTBIT = "FLUENTBIT"
    """fluentbit.

    stability
    :stability: experimental
    """
    FLUENTD = "FLUENTD"
    """fluentd.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.FirelensOptions", jsii_struct_bases=[], name_mapping={'config_file_value': 'configFileValue', 'config_file_type': 'configFileType', 'enable_ecs_log_metadata': 'enableECSLogMetadata'})
class FirelensOptions():
    def __init__(self, *, config_file_value: str, config_file_type: typing.Optional["FirelensConfigFileType"]=None, enable_ecs_log_metadata: typing.Optional[bool]=None) -> None:
        """The options for firelens log router https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_firelens.html#firelens-taskdef-customconfig.

        :param config_file_value: Custom configuration file, S3 ARN or a file path.
        :param config_file_type: Custom configuration file, s3 or file. Default: - determined by checking configFileValue with S3 ARN.
        :param enable_ecs_log_metadata: By default, Amazon ECS adds additional fields in your log entries that help identify the source of the logs. You can disable this action by setting enable-ecs-log-metadata to false. Default: - true

        stability
        :stability: experimental
        """
        self._values = {
            'config_file_value': config_file_value,
        }
        if config_file_type is not None: self._values["config_file_type"] = config_file_type
        if enable_ecs_log_metadata is not None: self._values["enable_ecs_log_metadata"] = enable_ecs_log_metadata

    @builtins.property
    def config_file_value(self) -> str:
        """Custom configuration file, S3 ARN or a file path.

        stability
        :stability: experimental
        """
        return self._values.get('config_file_value')

    @builtins.property
    def config_file_type(self) -> typing.Optional["FirelensConfigFileType"]:
        """Custom configuration file, s3 or file.

        default
        :default: - determined by checking configFileValue with S3 ARN.

        stability
        :stability: experimental
        """
        return self._values.get('config_file_type')

    @builtins.property
    def enable_ecs_log_metadata(self) -> typing.Optional[bool]:
        """By default, Amazon ECS adds additional fields in your log entries that help identify the source of the logs.

        You can disable this action by setting enable-ecs-log-metadata to false.

        default
        :default: - true

        stability
        :stability: experimental
        """
        return self._values.get('enable_ecs_log_metadata')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FirelensOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.FluentdLogDriverProps", jsii_struct_bases=[BaseLogDriverProps], name_mapping={'env': 'env', 'env_regex': 'envRegex', 'labels': 'labels', 'tag': 'tag', 'address': 'address', 'async_connect': 'asyncConnect', 'buffer_limit': 'bufferLimit', 'max_retries': 'maxRetries', 'retry_wait': 'retryWait', 'sub_second_precision': 'subSecondPrecision'})
class FluentdLogDriverProps(BaseLogDriverProps):
    def __init__(self, *, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None, address: typing.Optional[str]=None, async_connect: typing.Optional[bool]=None, buffer_limit: typing.Optional[jsii.Number]=None, max_retries: typing.Optional[jsii.Number]=None, retry_wait: typing.Optional[_Duration_5170c158]=None, sub_second_precision: typing.Optional[bool]=None) -> None:
        """Specifies the fluentd log driver configuration options.

        `Source <https://docs.docker.com/config/containers/logging/fluentd/>`_

        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID
        :param address: By default, the logging driver connects to localhost:24224. Supply the address option to connect to a different address. tcp(default) and unix sockets are supported. Default: - address not set.
        :param async_connect: Docker connects to Fluentd in the background. Messages are buffered until the connection is established. Default: - false
        :param buffer_limit: The amount of data to buffer before flushing to disk. Default: - The amount of RAM available to the container.
        :param max_retries: The maximum number of retries. Default: - 4294967295 (2**32 - 1).
        :param retry_wait: How long to wait between retries. Default: - 1 second
        :param sub_second_precision: Generates event logs in nanosecond resolution. Default: - false

        stability
        :stability: experimental
        """
        self._values = {
        }
        if env is not None: self._values["env"] = env
        if env_regex is not None: self._values["env_regex"] = env_regex
        if labels is not None: self._values["labels"] = labels
        if tag is not None: self._values["tag"] = tag
        if address is not None: self._values["address"] = address
        if async_connect is not None: self._values["async_connect"] = async_connect
        if buffer_limit is not None: self._values["buffer_limit"] = buffer_limit
        if max_retries is not None: self._values["max_retries"] = max_retries
        if retry_wait is not None: self._values["retry_wait"] = retry_wait
        if sub_second_precision is not None: self._values["sub_second_precision"] = sub_second_precision

    @builtins.property
    def env(self) -> typing.Optional[typing.List[str]]:
        """The env option takes an array of keys.

        If there is collision between
        label and env keys, the value of the env takes precedence. Adds additional fields
        to the extra attributes of a logging message.

        default
        :default: - No env

        stability
        :stability: experimental
        """
        return self._values.get('env')

    @builtins.property
    def env_regex(self) -> typing.Optional[str]:
        """The env-regex option is similar to and compatible with env.

        Its value is a regular
        expression to match logging-related environment variables. It is used for advanced
        log tag options.

        default
        :default: - No envRegex

        stability
        :stability: experimental
        """
        return self._values.get('env_regex')

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[str]]:
        """The labels option takes an array of keys.

        If there is collision
        between label and env keys, the value of the env takes precedence. Adds additional
        fields to the extra attributes of a logging message.

        default
        :default: - No labels

        stability
        :stability: experimental
        """
        return self._values.get('labels')

    @builtins.property
    def tag(self) -> typing.Optional[str]:
        """By default, Docker uses the first 12 characters of the container ID to tag log messages.

        Refer to the log tag option documentation for customizing the
        log tag format.

        default
        :default: - The first 12 characters of the container ID

        stability
        :stability: experimental
        """
        return self._values.get('tag')

    @builtins.property
    def address(self) -> typing.Optional[str]:
        """By default, the logging driver connects to localhost:24224.

        Supply the
        address option to connect to a different address. tcp(default) and unix
        sockets are supported.

        default
        :default: - address not set.

        stability
        :stability: experimental
        """
        return self._values.get('address')

    @builtins.property
    def async_connect(self) -> typing.Optional[bool]:
        """Docker connects to Fluentd in the background.

        Messages are buffered until
        the connection is established.

        default
        :default: - false

        stability
        :stability: experimental
        """
        return self._values.get('async_connect')

    @builtins.property
    def buffer_limit(self) -> typing.Optional[jsii.Number]:
        """The amount of data to buffer before flushing to disk.

        default
        :default: - The amount of RAM available to the container.

        stability
        :stability: experimental
        """
        return self._values.get('buffer_limit')

    @builtins.property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        """The maximum number of retries.

        default
        :default: - 4294967295 (2**32 - 1).

        stability
        :stability: experimental
        """
        return self._values.get('max_retries')

    @builtins.property
    def retry_wait(self) -> typing.Optional[_Duration_5170c158]:
        """How long to wait between retries.

        default
        :default: - 1 second

        stability
        :stability: experimental
        """
        return self._values.get('retry_wait')

    @builtins.property
    def sub_second_precision(self) -> typing.Optional[bool]:
        """Generates event logs in nanosecond resolution.

        default
        :default: - false

        stability
        :stability: experimental
        """
        return self._values.get('sub_second_precision')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FluentdLogDriverProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.aws_ecs.GelfCompressionType")
class GelfCompressionType(enum.Enum):
    """The type of compression the GELF driver uses to compress each log message.

    stability
    :stability: experimental
    """
    GZIP = "GZIP"
    """
    stability
    :stability: experimental
    """
    ZLIB = "ZLIB"
    """
    stability
    :stability: experimental
    """
    NONE = "NONE"
    """
    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.GelfLogDriverProps", jsii_struct_bases=[BaseLogDriverProps], name_mapping={'env': 'env', 'env_regex': 'envRegex', 'labels': 'labels', 'tag': 'tag', 'address': 'address', 'compression_level': 'compressionLevel', 'compression_type': 'compressionType', 'tcp_max_reconnect': 'tcpMaxReconnect', 'tcp_reconnect_delay': 'tcpReconnectDelay'})
class GelfLogDriverProps(BaseLogDriverProps):
    def __init__(self, *, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None, address: str, compression_level: typing.Optional[jsii.Number]=None, compression_type: typing.Optional["GelfCompressionType"]=None, tcp_max_reconnect: typing.Optional[jsii.Number]=None, tcp_reconnect_delay: typing.Optional[_Duration_5170c158]=None) -> None:
        """Specifies the journald log driver configuration options.

        `Source <https://docs.docker.com/config/containers/logging/gelf/>`_

        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID
        :param address: The address of the GELF server. tcp and udp are the only supported URI specifier and you must specify the port.
        :param compression_level: UDP Only The level of compression when gzip or zlib is the gelf-compression-type. An integer in the range of -1 to 9 (BestCompression). Higher levels provide more compression at lower speed. Either -1 or 0 disables compression. Default: - 1
        :param compression_type: UDP Only The type of compression the GELF driver uses to compress each log message. Allowed values are gzip, zlib and none. Default: - gzip
        :param tcp_max_reconnect: TCP Only The maximum number of reconnection attempts when the connection drop. A positive integer. Default: - 3
        :param tcp_reconnect_delay: TCP Only The number of seconds to wait between reconnection attempts. A positive integer. Default: - 1

        stability
        :stability: experimental
        """
        self._values = {
            'address': address,
        }
        if env is not None: self._values["env"] = env
        if env_regex is not None: self._values["env_regex"] = env_regex
        if labels is not None: self._values["labels"] = labels
        if tag is not None: self._values["tag"] = tag
        if compression_level is not None: self._values["compression_level"] = compression_level
        if compression_type is not None: self._values["compression_type"] = compression_type
        if tcp_max_reconnect is not None: self._values["tcp_max_reconnect"] = tcp_max_reconnect
        if tcp_reconnect_delay is not None: self._values["tcp_reconnect_delay"] = tcp_reconnect_delay

    @builtins.property
    def env(self) -> typing.Optional[typing.List[str]]:
        """The env option takes an array of keys.

        If there is collision between
        label and env keys, the value of the env takes precedence. Adds additional fields
        to the extra attributes of a logging message.

        default
        :default: - No env

        stability
        :stability: experimental
        """
        return self._values.get('env')

    @builtins.property
    def env_regex(self) -> typing.Optional[str]:
        """The env-regex option is similar to and compatible with env.

        Its value is a regular
        expression to match logging-related environment variables. It is used for advanced
        log tag options.

        default
        :default: - No envRegex

        stability
        :stability: experimental
        """
        return self._values.get('env_regex')

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[str]]:
        """The labels option takes an array of keys.

        If there is collision
        between label and env keys, the value of the env takes precedence. Adds additional
        fields to the extra attributes of a logging message.

        default
        :default: - No labels

        stability
        :stability: experimental
        """
        return self._values.get('labels')

    @builtins.property
    def tag(self) -> typing.Optional[str]:
        """By default, Docker uses the first 12 characters of the container ID to tag log messages.

        Refer to the log tag option documentation for customizing the
        log tag format.

        default
        :default: - The first 12 characters of the container ID

        stability
        :stability: experimental
        """
        return self._values.get('tag')

    @builtins.property
    def address(self) -> str:
        """The address of the GELF server.

        tcp and udp are the only supported URI
        specifier and you must specify the port.

        stability
        :stability: experimental
        """
        return self._values.get('address')

    @builtins.property
    def compression_level(self) -> typing.Optional[jsii.Number]:
        """UDP Only The level of compression when gzip or zlib is the gelf-compression-type.

        An integer in the range of -1 to 9 (BestCompression). Higher levels provide more
        compression at lower speed. Either -1 or 0 disables compression.

        default
        :default: - 1

        stability
        :stability: experimental
        """
        return self._values.get('compression_level')

    @builtins.property
    def compression_type(self) -> typing.Optional["GelfCompressionType"]:
        """UDP Only The type of compression the GELF driver uses to compress each log message.

        Allowed values are gzip, zlib and none.

        default
        :default: - gzip

        stability
        :stability: experimental
        """
        return self._values.get('compression_type')

    @builtins.property
    def tcp_max_reconnect(self) -> typing.Optional[jsii.Number]:
        """TCP Only The maximum number of reconnection attempts when the connection drop.

        A positive integer.

        default
        :default: - 3

        stability
        :stability: experimental
        """
        return self._values.get('tcp_max_reconnect')

    @builtins.property
    def tcp_reconnect_delay(self) -> typing.Optional[_Duration_5170c158]:
        """TCP Only The number of seconds to wait between reconnection attempts.

        A positive integer.

        default
        :default: - 1

        stability
        :stability: experimental
        """
        return self._values.get('tcp_reconnect_delay')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'GelfLogDriverProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.HealthCheck", jsii_struct_bases=[], name_mapping={'command': 'command', 'interval': 'interval', 'retries': 'retries', 'start_period': 'startPeriod', 'timeout': 'timeout'})
class HealthCheck():
    def __init__(self, *, command: typing.List[str], interval: typing.Optional[_Duration_5170c158]=None, retries: typing.Optional[jsii.Number]=None, start_period: typing.Optional[_Duration_5170c158]=None, timeout: typing.Optional[_Duration_5170c158]=None) -> None:
        """The health check command and associated configuration parameters for the container.

        :param command: A string array representing the command that the container runs to determine if it is healthy. The string array must start with CMD to execute the command arguments directly, or CMD-SHELL to run the command with the container's default shell. For example: [ "CMD-SHELL", "curl -f http://localhost/ || exit 1" ]
        :param interval: The time period in seconds between each health check execution. You may specify between 5 and 300 seconds. Default: Duration.seconds(30)
        :param retries: The number of times to retry a failed health check before the container is considered unhealthy. You may specify between 1 and 10 retries. Default: 3
        :param start_period: The optional grace period within which to provide containers time to bootstrap before failed health checks count towards the maximum number of retries. You may specify between 0 and 300 seconds. Default: No start period
        :param timeout: The time period in seconds to wait for a health check to succeed before it is considered a failure. You may specify between 2 and 60 seconds. Default: Duration.seconds(5)

        stability
        :stability: experimental
        """
        self._values = {
            'command': command,
        }
        if interval is not None: self._values["interval"] = interval
        if retries is not None: self._values["retries"] = retries
        if start_period is not None: self._values["start_period"] = start_period
        if timeout is not None: self._values["timeout"] = timeout

    @builtins.property
    def command(self) -> typing.List[str]:
        """A string array representing the command that the container runs to determine if it is healthy.

        The string array must start with CMD to execute the command arguments directly, or
        CMD-SHELL to run the command with the container's default shell.

        For example: [ "CMD-SHELL", "curl -f http://localhost/ || exit 1" ]

        stability
        :stability: experimental
        """
        return self._values.get('command')

    @builtins.property
    def interval(self) -> typing.Optional[_Duration_5170c158]:
        """The time period in seconds between each health check execution.

        You may specify between 5 and 300 seconds.

        default
        :default: Duration.seconds(30)

        stability
        :stability: experimental
        """
        return self._values.get('interval')

    @builtins.property
    def retries(self) -> typing.Optional[jsii.Number]:
        """The number of times to retry a failed health check before the container is considered unhealthy.

        You may specify between 1 and 10 retries.

        default
        :default: 3

        stability
        :stability: experimental
        """
        return self._values.get('retries')

    @builtins.property
    def start_period(self) -> typing.Optional[_Duration_5170c158]:
        """The optional grace period within which to provide containers time to bootstrap before failed health checks count towards the maximum number of retries.

        You may specify between 0 and 300 seconds.

        default
        :default: No start period

        stability
        :stability: experimental
        """
        return self._values.get('start_period')

    @builtins.property
    def timeout(self) -> typing.Optional[_Duration_5170c158]:
        """The time period in seconds to wait for a health check to succeed before it is considered a failure.

        You may specify between 2 and 60 seconds.

        default
        :default: Duration.seconds(5)

        stability
        :stability: experimental
        """
        return self._values.get('timeout')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'HealthCheck(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.Host", jsii_struct_bases=[], name_mapping={'source_path': 'sourcePath'})
class Host():
    def __init__(self, *, source_path: typing.Optional[str]=None) -> None:
        """The details on a container instance bind mount host volume.

        :param source_path: Specifies the path on the host container instance that is presented to the container. If the sourcePath value does not exist on the host container instance, the Docker daemon creates it. If the location does exist, the contents of the source path folder are exported. This property is not supported for tasks that use the Fargate launch type.

        stability
        :stability: experimental
        """
        self._values = {
        }
        if source_path is not None: self._values["source_path"] = source_path

    @builtins.property
    def source_path(self) -> typing.Optional[str]:
        """Specifies the path on the host container instance that is presented to the container.

        If the sourcePath value does not exist on the host container instance, the Docker daemon creates it.
        If the location does exist, the contents of the source path folder are exported.

        This property is not supported for tasks that use the Fargate launch type.

        stability
        :stability: experimental
        """
        return self._values.get('source_path')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'Host(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="monocdk-experiment.aws_ecs.ICluster")
class ICluster(_IResource_72f7ee7e, jsii.compat.Protocol):
    """A regional grouping of one or more container instances on which you can run tasks and services.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IClusterProxy

    @builtins.property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> str:
        """The Amazon Resource Name (ARN) that identifies the cluster.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        """The name of the cluster.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _Connections_231f38b5:
        """Manage the allowed network connections for the cluster with Security Groups.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="hasEc2Capacity")
    def has_ec2_capacity(self) -> bool:
        """Specifies whether the cluster has EC2 instance capacity.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _IVpc_3795853f:
        """The VPC associated with the cluster.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="autoscalingGroup")
    def autoscaling_group(self) -> typing.Optional[_IAutoScalingGroup_a753dc94]:
        """The autoscaling group added to the cluster if capacity is associated to the cluster.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="defaultCloudMapNamespace")
    def default_cloud_map_namespace(self) -> typing.Optional[_INamespace_2b56a022]:
        """The AWS Cloud Map namespace to associate with the cluster.

        stability
        :stability: experimental
        """
        ...


class _IClusterProxy(jsii.proxy_for(_IResource_72f7ee7e)):
    """A regional grouping of one or more container instances on which you can run tasks and services.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_ecs.ICluster"
    @builtins.property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> str:
        """The Amazon Resource Name (ARN) that identifies the cluster.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "clusterArn")

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        """The name of the cluster.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "clusterName")

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _Connections_231f38b5:
        """Manage the allowed network connections for the cluster with Security Groups.

        stability
        :stability: experimental
        """
        return jsii.get(self, "connections")

    @builtins.property
    @jsii.member(jsii_name="hasEc2Capacity")
    def has_ec2_capacity(self) -> bool:
        """Specifies whether the cluster has EC2 instance capacity.

        stability
        :stability: experimental
        """
        return jsii.get(self, "hasEc2Capacity")

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _IVpc_3795853f:
        """The VPC associated with the cluster.

        stability
        :stability: experimental
        """
        return jsii.get(self, "vpc")

    @builtins.property
    @jsii.member(jsii_name="autoscalingGroup")
    def autoscaling_group(self) -> typing.Optional[_IAutoScalingGroup_a753dc94]:
        """The autoscaling group added to the cluster if capacity is associated to the cluster.

        stability
        :stability: experimental
        """
        return jsii.get(self, "autoscalingGroup")

    @builtins.property
    @jsii.member(jsii_name="defaultCloudMapNamespace")
    def default_cloud_map_namespace(self) -> typing.Optional[_INamespace_2b56a022]:
        """The AWS Cloud Map namespace to associate with the cluster.

        stability
        :stability: experimental
        """
        return jsii.get(self, "defaultCloudMapNamespace")


@jsii.interface(jsii_type="monocdk-experiment.aws_ecs.IEcsLoadBalancerTarget")
class IEcsLoadBalancerTarget(_IApplicationLoadBalancerTarget_079c540c, _INetworkLoadBalancerTarget_c44e1c1e, _ILoadBalancerTarget_87ce58b8, jsii.compat.Protocol):
    """Interface for ECS load balancer target.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IEcsLoadBalancerTargetProxy

    pass

class _IEcsLoadBalancerTargetProxy(jsii.proxy_for(_IApplicationLoadBalancerTarget_079c540c), jsii.proxy_for(_INetworkLoadBalancerTarget_c44e1c1e), jsii.proxy_for(_ILoadBalancerTarget_87ce58b8)):
    """Interface for ECS load balancer target.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_ecs.IEcsLoadBalancerTarget"
    pass

@jsii.interface(jsii_type="monocdk-experiment.aws_ecs.IService")
class IService(_IResource_72f7ee7e, jsii.compat.Protocol):
    """The interface for a service.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IServiceProxy

    @builtins.property
    @jsii.member(jsii_name="serviceArn")
    def service_arn(self) -> str:
        """The Amazon Resource Name (ARN) of the service.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> str:
        """The name of the service.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _IServiceProxy(jsii.proxy_for(_IResource_72f7ee7e)):
    """The interface for a service.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_ecs.IService"
    @builtins.property
    @jsii.member(jsii_name="serviceArn")
    def service_arn(self) -> str:
        """The Amazon Resource Name (ARN) of the service.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "serviceArn")

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> str:
        """The name of the service.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "serviceName")


@jsii.interface(jsii_type="monocdk-experiment.aws_ecs.ITaskDefinition")
class ITaskDefinition(_IResource_72f7ee7e, jsii.compat.Protocol):
    """The interface for all task definitions.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ITaskDefinitionProxy

    @builtins.property
    @jsii.member(jsii_name="compatibility")
    def compatibility(self) -> "Compatibility":
        """What launch types this task definition should be compatible with.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="isEc2Compatible")
    def is_ec2_compatible(self) -> bool:
        """Return true if the task definition can be run on an EC2 cluster.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="isFargateCompatible")
    def is_fargate_compatible(self) -> bool:
        """Return true if the task definition can be run on a Fargate cluster.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="taskDefinitionArn")
    def task_definition_arn(self) -> str:
        """ARN of this task definition.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="executionRole")
    def execution_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """Execution role for this task definition.

        stability
        :stability: experimental
        """
        ...


class _ITaskDefinitionProxy(jsii.proxy_for(_IResource_72f7ee7e)):
    """The interface for all task definitions.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_ecs.ITaskDefinition"
    @builtins.property
    @jsii.member(jsii_name="compatibility")
    def compatibility(self) -> "Compatibility":
        """What launch types this task definition should be compatible with.

        stability
        :stability: experimental
        """
        return jsii.get(self, "compatibility")

    @builtins.property
    @jsii.member(jsii_name="isEc2Compatible")
    def is_ec2_compatible(self) -> bool:
        """Return true if the task definition can be run on an EC2 cluster.

        stability
        :stability: experimental
        """
        return jsii.get(self, "isEc2Compatible")

    @builtins.property
    @jsii.member(jsii_name="isFargateCompatible")
    def is_fargate_compatible(self) -> bool:
        """Return true if the task definition can be run on a Fargate cluster.

        stability
        :stability: experimental
        """
        return jsii.get(self, "isFargateCompatible")

    @builtins.property
    @jsii.member(jsii_name="taskDefinitionArn")
    def task_definition_arn(self) -> str:
        """ARN of this task definition.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "taskDefinitionArn")

    @builtins.property
    @jsii.member(jsii_name="executionRole")
    def execution_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """Execution role for this task definition.

        stability
        :stability: experimental
        """
        return jsii.get(self, "executionRole")


@jsii.interface(jsii_type="monocdk-experiment.aws_ecs.ITaskDefinitionExtension")
class ITaskDefinitionExtension(jsii.compat.Protocol):
    """An extension for Task Definitions.

    Classes that want to make changes to a TaskDefinition (such as
    adding helper containers) can implement this interface, and can
    then be "added" to a TaskDefinition like so::

       taskDefinition.addExtension(new MyExtension("some_parameter"));

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ITaskDefinitionExtensionProxy

    @jsii.member(jsii_name="extend")
    def extend(self, task_definition: "TaskDefinition") -> None:
        """Apply the extension to the given TaskDefinition.

        :param task_definition: [disable-awslint:ref-via-interface].

        stability
        :stability: experimental
        """
        ...


class _ITaskDefinitionExtensionProxy():
    """An extension for Task Definitions.

    Classes that want to make changes to a TaskDefinition (such as
    adding helper containers) can implement this interface, and can
    then be "added" to a TaskDefinition like so::

       taskDefinition.addExtension(new MyExtension("some_parameter"));

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_ecs.ITaskDefinitionExtension"
    @jsii.member(jsii_name="extend")
    def extend(self, task_definition: "TaskDefinition") -> None:
        """Apply the extension to the given TaskDefinition.

        :param task_definition: [disable-awslint:ref-via-interface].

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "extend", [task_definition])


@jsii.enum(jsii_type="monocdk-experiment.aws_ecs.IpcMode")
class IpcMode(enum.Enum):
    """The IPC resource namespace to use for the containers in the task.

    stability
    :stability: experimental
    """
    NONE = "NONE"
    """If none is specified, then IPC resources within the containers of a task are private and not shared with other containers in a task or on the container instance.

    stability
    :stability: experimental
    """
    HOST = "HOST"
    """If host is specified, then all containers within the tasks that specified the host IPC mode on the same container instance share the same IPC resources with the host Amazon EC2 instance.

    stability
    :stability: experimental
    """
    TASK = "TASK"
    """If task is specified, all containers within the specified task share the same IPC resources.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.JournaldLogDriverProps", jsii_struct_bases=[BaseLogDriverProps], name_mapping={'env': 'env', 'env_regex': 'envRegex', 'labels': 'labels', 'tag': 'tag'})
class JournaldLogDriverProps(BaseLogDriverProps):
    def __init__(self, *, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None) -> None:
        """Specifies the journald log driver configuration options.

        `Source <https://docs.docker.com/config/containers/logging/journald/>`_

        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID

        stability
        :stability: experimental
        """
        self._values = {
        }
        if env is not None: self._values["env"] = env
        if env_regex is not None: self._values["env_regex"] = env_regex
        if labels is not None: self._values["labels"] = labels
        if tag is not None: self._values["tag"] = tag

    @builtins.property
    def env(self) -> typing.Optional[typing.List[str]]:
        """The env option takes an array of keys.

        If there is collision between
        label and env keys, the value of the env takes precedence. Adds additional fields
        to the extra attributes of a logging message.

        default
        :default: - No env

        stability
        :stability: experimental
        """
        return self._values.get('env')

    @builtins.property
    def env_regex(self) -> typing.Optional[str]:
        """The env-regex option is similar to and compatible with env.

        Its value is a regular
        expression to match logging-related environment variables. It is used for advanced
        log tag options.

        default
        :default: - No envRegex

        stability
        :stability: experimental
        """
        return self._values.get('env_regex')

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[str]]:
        """The labels option takes an array of keys.

        If there is collision
        between label and env keys, the value of the env takes precedence. Adds additional
        fields to the extra attributes of a logging message.

        default
        :default: - No labels

        stability
        :stability: experimental
        """
        return self._values.get('labels')

    @builtins.property
    def tag(self) -> typing.Optional[str]:
        """By default, Docker uses the first 12 characters of the container ID to tag log messages.

        Refer to the log tag option documentation for customizing the
        log tag format.

        default
        :default: - The first 12 characters of the container ID

        stability
        :stability: experimental
        """
        return self._values.get('tag')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'JournaldLogDriverProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.JsonFileLogDriverProps", jsii_struct_bases=[BaseLogDriverProps], name_mapping={'env': 'env', 'env_regex': 'envRegex', 'labels': 'labels', 'tag': 'tag', 'compress': 'compress', 'max_file': 'maxFile', 'max_size': 'maxSize'})
class JsonFileLogDriverProps(BaseLogDriverProps):
    def __init__(self, *, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None, compress: typing.Optional[bool]=None, max_file: typing.Optional[jsii.Number]=None, max_size: typing.Optional[str]=None) -> None:
        """Specifies the json-file log driver configuration options.

        `Source <https://docs.docker.com/config/containers/logging/json-file/>`_

        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID
        :param compress: Toggles compression for rotated logs. Default: - false
        :param max_file: The maximum number of log files that can be present. If rolling the logs creates excess files, the oldest file is removed. Only effective when max-size is also set. A positive integer. Default: - 1
        :param max_size: The maximum size of the log before it is rolled. A positive integer plus a modifier representing the unit of measure (k, m, or g). Default: - -1 (unlimited)

        stability
        :stability: experimental
        """
        self._values = {
        }
        if env is not None: self._values["env"] = env
        if env_regex is not None: self._values["env_regex"] = env_regex
        if labels is not None: self._values["labels"] = labels
        if tag is not None: self._values["tag"] = tag
        if compress is not None: self._values["compress"] = compress
        if max_file is not None: self._values["max_file"] = max_file
        if max_size is not None: self._values["max_size"] = max_size

    @builtins.property
    def env(self) -> typing.Optional[typing.List[str]]:
        """The env option takes an array of keys.

        If there is collision between
        label and env keys, the value of the env takes precedence. Adds additional fields
        to the extra attributes of a logging message.

        default
        :default: - No env

        stability
        :stability: experimental
        """
        return self._values.get('env')

    @builtins.property
    def env_regex(self) -> typing.Optional[str]:
        """The env-regex option is similar to and compatible with env.

        Its value is a regular
        expression to match logging-related environment variables. It is used for advanced
        log tag options.

        default
        :default: - No envRegex

        stability
        :stability: experimental
        """
        return self._values.get('env_regex')

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[str]]:
        """The labels option takes an array of keys.

        If there is collision
        between label and env keys, the value of the env takes precedence. Adds additional
        fields to the extra attributes of a logging message.

        default
        :default: - No labels

        stability
        :stability: experimental
        """
        return self._values.get('labels')

    @builtins.property
    def tag(self) -> typing.Optional[str]:
        """By default, Docker uses the first 12 characters of the container ID to tag log messages.

        Refer to the log tag option documentation for customizing the
        log tag format.

        default
        :default: - The first 12 characters of the container ID

        stability
        :stability: experimental
        """
        return self._values.get('tag')

    @builtins.property
    def compress(self) -> typing.Optional[bool]:
        """Toggles compression for rotated logs.

        default
        :default: - false

        stability
        :stability: experimental
        """
        return self._values.get('compress')

    @builtins.property
    def max_file(self) -> typing.Optional[jsii.Number]:
        """The maximum number of log files that can be present.

        If rolling the logs creates
        excess files, the oldest file is removed. Only effective when max-size is also set.
        A positive integer.

        default
        :default: - 1

        stability
        :stability: experimental
        """
        return self._values.get('max_file')

    @builtins.property
    def max_size(self) -> typing.Optional[str]:
        """The maximum size of the log before it is rolled.

        A positive integer plus a modifier
        representing the unit of measure (k, m, or g).

        default
        :default: - -1 (unlimited)

        stability
        :stability: experimental
        """
        return self._values.get('max_size')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'JsonFileLogDriverProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.aws_ecs.LaunchType")
class LaunchType(enum.Enum):
    """The launch type of an ECS service.

    stability
    :stability: experimental
    """
    EC2 = "EC2"
    """The service will be launched using the EC2 launch type.

    stability
    :stability: experimental
    """
    FARGATE = "FARGATE"
    """The service will be launched using the FARGATE launch type.

    stability
    :stability: experimental
    """

class LinuxParameters(_Construct_f50a3f53, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs.LinuxParameters"):
    """Linux-specific options that are applied to the container.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, init_process_enabled: typing.Optional[bool]=None, shared_memory_size: typing.Optional[jsii.Number]=None) -> None:
        """Constructs a new instance of the LinuxParameters class.

        :param scope: -
        :param id: -
        :param init_process_enabled: Specifies whether to run an init process inside the container that forwards signals and reaps processes. Default: false
        :param shared_memory_size: The value for the size (in MiB) of the /dev/shm volume. Default: No shared memory.

        stability
        :stability: experimental
        """
        props = LinuxParametersProps(init_process_enabled=init_process_enabled, shared_memory_size=shared_memory_size)

        jsii.create(LinuxParameters, self, [scope, id, props])

    @jsii.member(jsii_name="addCapabilities")
    def add_capabilities(self, *cap: "Capability") -> None:
        """Adds one or more Linux capabilities to the Docker configuration of a container.

        Only works with EC2 launch type.

        :param cap: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addCapabilities", [*cap])

    @jsii.member(jsii_name="addDevices")
    def add_devices(self, *device: "Device") -> None:
        """Adds one or more host devices to a container.

        :param device: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addDevices", [*device])

    @jsii.member(jsii_name="addTmpfs")
    def add_tmpfs(self, *tmpfs: "Tmpfs") -> None:
        """Specifies the container path, mount options, and size (in MiB) of the tmpfs mount for a container.

        Only works with EC2 launch type.

        :param tmpfs: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addTmpfs", [*tmpfs])

    @jsii.member(jsii_name="dropCapabilities")
    def drop_capabilities(self, *cap: "Capability") -> None:
        """Removes one or more Linux capabilities to the Docker configuration of a container.

        Only works with EC2 launch type.

        :param cap: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "dropCapabilities", [*cap])

    @jsii.member(jsii_name="renderLinuxParameters")
    def render_linux_parameters(self) -> "CfnTaskDefinition.LinuxParametersProperty":
        """Renders the Linux parameters to a CloudFormation object.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "renderLinuxParameters", [])


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.LinuxParametersProps", jsii_struct_bases=[], name_mapping={'init_process_enabled': 'initProcessEnabled', 'shared_memory_size': 'sharedMemorySize'})
class LinuxParametersProps():
    def __init__(self, *, init_process_enabled: typing.Optional[bool]=None, shared_memory_size: typing.Optional[jsii.Number]=None) -> None:
        """The properties for defining Linux-specific options that are applied to the container.

        :param init_process_enabled: Specifies whether to run an init process inside the container that forwards signals and reaps processes. Default: false
        :param shared_memory_size: The value for the size (in MiB) of the /dev/shm volume. Default: No shared memory.

        stability
        :stability: experimental
        """
        self._values = {
        }
        if init_process_enabled is not None: self._values["init_process_enabled"] = init_process_enabled
        if shared_memory_size is not None: self._values["shared_memory_size"] = shared_memory_size

    @builtins.property
    def init_process_enabled(self) -> typing.Optional[bool]:
        """Specifies whether to run an init process inside the container that forwards signals and reaps processes.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('init_process_enabled')

    @builtins.property
    def shared_memory_size(self) -> typing.Optional[jsii.Number]:
        """The value for the size (in MiB) of the /dev/shm volume.

        default
        :default: No shared memory.

        stability
        :stability: experimental
        """
        return self._values.get('shared_memory_size')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LinuxParametersProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class ListenerConfig(metaclass=jsii.JSIIAbstractClass, jsii_type="monocdk-experiment.aws_ecs.ListenerConfig"):
    """Base class for configuring listener when registering targets.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ListenerConfigProxy

    def __init__(self) -> None:
        jsii.create(ListenerConfig, self, [])

    @jsii.member(jsii_name="applicationListener")
    @builtins.classmethod
    def application_listener(cls, listener: _ApplicationListener_58c10c5c, *, deregistration_delay: typing.Optional[_Duration_5170c158]=None, health_check: typing.Optional[_HealthCheck_87e0be77]=None, port: typing.Optional[jsii.Number]=None, protocol: typing.Optional[_ApplicationProtocol_60c416f7]=None, slow_start: typing.Optional[_Duration_5170c158]=None, stickiness_cookie_duration: typing.Optional[_Duration_5170c158]=None, target_group_name: typing.Optional[str]=None, targets: typing.Optional[typing.List[_IApplicationLoadBalancerTarget_079c540c]]=None, conditions: typing.Optional[typing.List[_ListenerCondition_1d53573e]]=None, host_header: typing.Optional[str]=None, path_pattern: typing.Optional[str]=None, path_patterns: typing.Optional[typing.List[str]]=None, priority: typing.Optional[jsii.Number]=None) -> "ListenerConfig":
        """Create a config for adding target group to ALB listener.

        :param listener: -
        :param deregistration_delay: The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: Duration.minutes(5)
        :param health_check: Health check configuration. Default: No health check
        :param port: The port on which the listener listens for requests. Default: Determined from protocol if known
        :param protocol: The protocol to use. Default: Determined from port if known
        :param slow_start: The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic to the target group. The range is 30-900 seconds (15 minutes). Default: 0
        :param stickiness_cookie_duration: The stickiness cookie expiration period. Setting this value enables load balancer stickiness. After this period, the cookie is considered stale. The minimum value is 1 second and the maximum value is 7 days (604800 seconds). Default: Stickiness disabled
        :param target_group_name: The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: Automatically generated
        :param targets: The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. All target must be of the same type.
        :param conditions: Rule applies if matches the conditions. Default: - No conditions.
        :param host_header: Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
        :param path_pattern: Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
        :param path_patterns: Rule applies if the requested path matches any of the given patterns. May contain up to three '*' wildcards. Requires that priority is set. Default: - No path condition.
        :param priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults

        stability
        :stability: experimental
        """
        props = _AddApplicationTargetsProps_a8f3da0a(deregistration_delay=deregistration_delay, health_check=health_check, port=port, protocol=protocol, slow_start=slow_start, stickiness_cookie_duration=stickiness_cookie_duration, target_group_name=target_group_name, targets=targets, conditions=conditions, host_header=host_header, path_pattern=path_pattern, path_patterns=path_patterns, priority=priority)

        return jsii.sinvoke(cls, "applicationListener", [listener, props])

    @jsii.member(jsii_name="networkListener")
    @builtins.classmethod
    def network_listener(cls, listener: _NetworkListener_921cec4b, *, port: jsii.Number, deregistration_delay: typing.Optional[_Duration_5170c158]=None, health_check: typing.Optional[_HealthCheck_87e0be77]=None, proxy_protocol_v2: typing.Optional[bool]=None, target_group_name: typing.Optional[str]=None, targets: typing.Optional[typing.List[_INetworkLoadBalancerTarget_c44e1c1e]]=None) -> "ListenerConfig":
        """Create a config for adding target group to NLB listener.

        :param listener: -
        :param port: The port on which the listener listens for requests. Default: Determined from protocol if known
        :param deregistration_delay: The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: Duration.minutes(5)
        :param health_check: Health check configuration. Default: No health check
        :param proxy_protocol_v2: Indicates whether Proxy Protocol version 2 is enabled. Default: false
        :param target_group_name: The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: Automatically generated
        :param targets: The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. If you use either ``Instance`` or ``IPAddress`` as targets, all target must be of the same type.

        stability
        :stability: experimental
        """
        props = _AddNetworkTargetsProps_c9bbd436(port=port, deregistration_delay=deregistration_delay, health_check=health_check, proxy_protocol_v2=proxy_protocol_v2, target_group_name=target_group_name, targets=targets)

        return jsii.sinvoke(cls, "networkListener", [listener, props])

    @jsii.member(jsii_name="addTargets")
    @abc.abstractmethod
    def add_targets(self, id: str, target: "LoadBalancerTargetOptions", service: "BaseService") -> None:
        """Create and attach a target group to listener.

        :param id: -
        :param target: -
        :param service: -

        stability
        :stability: experimental
        """
        ...


class _ListenerConfigProxy(ListenerConfig):
    @jsii.member(jsii_name="addTargets")
    def add_targets(self, id: str, target: "LoadBalancerTargetOptions", service: "BaseService") -> None:
        """Create and attach a target group to listener.

        :param id: -
        :param target: -
        :param service: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addTargets", [id, target, service])


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.LoadBalancerTargetOptions", jsii_struct_bases=[], name_mapping={'container_name': 'containerName', 'container_port': 'containerPort', 'protocol': 'protocol'})
class LoadBalancerTargetOptions():
    def __init__(self, *, container_name: str, container_port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["Protocol"]=None) -> None:
        """Properties for defining an ECS target.

        The port mapping for it must already have been created through addPortMapping().

        :param container_name: The name of the container.
        :param container_port: The port number of the container. Only applicable when using application/network load balancers. Default: - Container port of the first added port mapping.
        :param protocol: The protocol used for the port mapping. Only applicable when using application load balancers. Default: Protocol.TCP

        stability
        :stability: experimental
        """
        self._values = {
            'container_name': container_name,
        }
        if container_port is not None: self._values["container_port"] = container_port
        if protocol is not None: self._values["protocol"] = protocol

    @builtins.property
    def container_name(self) -> str:
        """The name of the container.

        stability
        :stability: experimental
        """
        return self._values.get('container_name')

    @builtins.property
    def container_port(self) -> typing.Optional[jsii.Number]:
        """The port number of the container.

        Only applicable when using application/network load balancers.

        default
        :default: - Container port of the first added port mapping.

        stability
        :stability: experimental
        """
        return self._values.get('container_port')

    @builtins.property
    def protocol(self) -> typing.Optional["Protocol"]:
        """The protocol used for the port mapping.

        Only applicable when using application load balancers.

        default
        :default: Protocol.TCP

        stability
        :stability: experimental
        """
        return self._values.get('protocol')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LoadBalancerTargetOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class LogDriver(metaclass=jsii.JSIIAbstractClass, jsii_type="monocdk-experiment.aws_ecs.LogDriver"):
    """The base class for log drivers.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _LogDriverProxy

    def __init__(self) -> None:
        jsii.create(LogDriver, self, [])

    @jsii.member(jsii_name="awsLogs")
    @builtins.classmethod
    def aws_logs(cls, *, stream_prefix: str, datetime_format: typing.Optional[str]=None, log_group: typing.Optional[_ILogGroup_6b54c8e1]=None, log_retention: typing.Optional[_RetentionDays_bdc7ad1f]=None, multiline_pattern: typing.Optional[str]=None) -> "LogDriver":
        """Creates a log driver configuration that sends log information to CloudWatch Logs.

        :param stream_prefix: Prefix for the log streams. The awslogs-stream-prefix option allows you to associate a log stream with the specified prefix, the container name, and the ID of the Amazon ECS task to which the container belongs. If you specify a prefix with this option, then the log stream takes the following format:: prefix-name/container-name/ecs-task-id
        :param datetime_format: This option defines a multiline start pattern in Python strftime format. A log message consists of a line that matches the pattern and any following lines that don’t match the pattern. Thus the matched line is the delimiter between log messages. Default: - No multiline matching.
        :param log_group: The log group to log to. Default: - A log group is automatically created.
        :param log_retention: The number of days log events are kept in CloudWatch Logs when the log group is automatically created by this construct. Default: - Logs never expire.
        :param multiline_pattern: This option defines a multiline start pattern using a regular expression. A log message consists of a line that matches the pattern and any following lines that don’t match the pattern. Thus the matched line is the delimiter between log messages. This option is ignored if datetimeFormat is also configured. Default: - No multiline matching.

        stability
        :stability: experimental
        """
        props = AwsLogDriverProps(stream_prefix=stream_prefix, datetime_format=datetime_format, log_group=log_group, log_retention=log_retention, multiline_pattern=multiline_pattern)

        return jsii.sinvoke(cls, "awsLogs", [props])

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, scope: _Construct_f50a3f53, container_definition: "ContainerDefinition") -> "LogDriverConfig":
        """Called when the log driver is configured on a container.

        :param scope: -
        :param container_definition: -

        stability
        :stability: experimental
        """
        ...


class _LogDriverProxy(LogDriver):
    @jsii.member(jsii_name="bind")
    def bind(self, scope: _Construct_f50a3f53, container_definition: "ContainerDefinition") -> "LogDriverConfig":
        """Called when the log driver is configured on a container.

        :param scope: -
        :param container_definition: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [scope, container_definition])


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.LogDriverConfig", jsii_struct_bases=[], name_mapping={'log_driver': 'logDriver', 'options': 'options'})
class LogDriverConfig():
    def __init__(self, *, log_driver: str, options: typing.Optional[typing.Mapping[str, str]]=None) -> None:
        """The configuration to use when creating a log driver.

        :param log_driver: The log driver to use for the container. The valid values listed for this parameter are log drivers that the Amazon ECS container agent can communicate with by default. For tasks using the Fargate launch type, the supported log drivers are awslogs, splunk, and awsfirelens. For tasks using the EC2 launch type, the supported log drivers are awslogs, fluentd, gelf, json-file, journald, logentries,syslog, splunk, and awsfirelens. For more information about using the awslogs log driver, see `Using the awslogs Log Driver <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_awslogs.html>`_ in the Amazon Elastic Container Service Developer Guide. For more information about using the awsfirelens log driver, see `Custom Log Routing <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_firelens.html>`_ in the Amazon Elastic Container Service Developer Guide.
        :param options: The configuration options to send to the log driver.

        stability
        :stability: experimental
        """
        self._values = {
            'log_driver': log_driver,
        }
        if options is not None: self._values["options"] = options

    @builtins.property
    def log_driver(self) -> str:
        """The log driver to use for the container.

        The valid values listed for this parameter are log drivers
        that the Amazon ECS container agent can communicate with by default.

        For tasks using the Fargate launch type, the supported log drivers are awslogs, splunk, and awsfirelens.
        For tasks using the EC2 launch type, the supported log drivers are awslogs, fluentd, gelf, json-file, journald,
        logentries,syslog, splunk, and awsfirelens.

        For more information about using the awslogs log driver, see
        `Using the awslogs Log Driver <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_awslogs.html>`_
        in the Amazon Elastic Container Service Developer Guide.

        For more information about using the awsfirelens log driver, see
        `Custom Log Routing <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_firelens.html>`_
        in the Amazon Elastic Container Service Developer Guide.

        stability
        :stability: experimental
        """
        return self._values.get('log_driver')

    @builtins.property
    def options(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The configuration options to send to the log driver.

        stability
        :stability: experimental
        """
        return self._values.get('options')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LogDriverConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class LogDrivers(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs.LogDrivers"):
    """The base class for log drivers.

    stability
    :stability: experimental
    """
    def __init__(self) -> None:
        jsii.create(LogDrivers, self, [])

    @jsii.member(jsii_name="awsLogs")
    @builtins.classmethod
    def aws_logs(cls, *, stream_prefix: str, datetime_format: typing.Optional[str]=None, log_group: typing.Optional[_ILogGroup_6b54c8e1]=None, log_retention: typing.Optional[_RetentionDays_bdc7ad1f]=None, multiline_pattern: typing.Optional[str]=None) -> "LogDriver":
        """Creates a log driver configuration that sends log information to CloudWatch Logs.

        :param stream_prefix: Prefix for the log streams. The awslogs-stream-prefix option allows you to associate a log stream with the specified prefix, the container name, and the ID of the Amazon ECS task to which the container belongs. If you specify a prefix with this option, then the log stream takes the following format:: prefix-name/container-name/ecs-task-id
        :param datetime_format: This option defines a multiline start pattern in Python strftime format. A log message consists of a line that matches the pattern and any following lines that don’t match the pattern. Thus the matched line is the delimiter between log messages. Default: - No multiline matching.
        :param log_group: The log group to log to. Default: - A log group is automatically created.
        :param log_retention: The number of days log events are kept in CloudWatch Logs when the log group is automatically created by this construct. Default: - Logs never expire.
        :param multiline_pattern: This option defines a multiline start pattern using a regular expression. A log message consists of a line that matches the pattern and any following lines that don’t match the pattern. Thus the matched line is the delimiter between log messages. This option is ignored if datetimeFormat is also configured. Default: - No multiline matching.

        stability
        :stability: experimental
        """
        props = AwsLogDriverProps(stream_prefix=stream_prefix, datetime_format=datetime_format, log_group=log_group, log_retention=log_retention, multiline_pattern=multiline_pattern)

        return jsii.sinvoke(cls, "awsLogs", [props])

    @jsii.member(jsii_name="firelens")
    @builtins.classmethod
    def firelens(cls, *, options: typing.Optional[typing.Mapping[str, str]]=None, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None) -> "LogDriver":
        """Creates a log driver configuration that sends log information to firelens log router.

        For detail configurations, please refer to Amazon ECS FireLens Examples:
        https://github.com/aws-samples/amazon-ecs-firelens-examples

        :param options: The configuration options to send to the log driver. Default: - the log driver options
        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID

        stability
        :stability: experimental
        """
        props = FireLensLogDriverProps(options=options, env=env, env_regex=env_regex, labels=labels, tag=tag)

        return jsii.sinvoke(cls, "firelens", [props])

    @jsii.member(jsii_name="fluentd")
    @builtins.classmethod
    def fluentd(cls, *, address: typing.Optional[str]=None, async_connect: typing.Optional[bool]=None, buffer_limit: typing.Optional[jsii.Number]=None, max_retries: typing.Optional[jsii.Number]=None, retry_wait: typing.Optional[_Duration_5170c158]=None, sub_second_precision: typing.Optional[bool]=None, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None) -> "LogDriver":
        """Creates a log driver configuration that sends log information to fluentd Logs.

        :param address: By default, the logging driver connects to localhost:24224. Supply the address option to connect to a different address. tcp(default) and unix sockets are supported. Default: - address not set.
        :param async_connect: Docker connects to Fluentd in the background. Messages are buffered until the connection is established. Default: - false
        :param buffer_limit: The amount of data to buffer before flushing to disk. Default: - The amount of RAM available to the container.
        :param max_retries: The maximum number of retries. Default: - 4294967295 (2**32 - 1).
        :param retry_wait: How long to wait between retries. Default: - 1 second
        :param sub_second_precision: Generates event logs in nanosecond resolution. Default: - false
        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID

        stability
        :stability: experimental
        """
        props = FluentdLogDriverProps(address=address, async_connect=async_connect, buffer_limit=buffer_limit, max_retries=max_retries, retry_wait=retry_wait, sub_second_precision=sub_second_precision, env=env, env_regex=env_regex, labels=labels, tag=tag)

        return jsii.sinvoke(cls, "fluentd", [props])

    @jsii.member(jsii_name="gelf")
    @builtins.classmethod
    def gelf(cls, *, address: str, compression_level: typing.Optional[jsii.Number]=None, compression_type: typing.Optional["GelfCompressionType"]=None, tcp_max_reconnect: typing.Optional[jsii.Number]=None, tcp_reconnect_delay: typing.Optional[_Duration_5170c158]=None, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None) -> "LogDriver":
        """Creates a log driver configuration that sends log information to gelf Logs.

        :param address: The address of the GELF server. tcp and udp are the only supported URI specifier and you must specify the port.
        :param compression_level: UDP Only The level of compression when gzip or zlib is the gelf-compression-type. An integer in the range of -1 to 9 (BestCompression). Higher levels provide more compression at lower speed. Either -1 or 0 disables compression. Default: - 1
        :param compression_type: UDP Only The type of compression the GELF driver uses to compress each log message. Allowed values are gzip, zlib and none. Default: - gzip
        :param tcp_max_reconnect: TCP Only The maximum number of reconnection attempts when the connection drop. A positive integer. Default: - 3
        :param tcp_reconnect_delay: TCP Only The number of seconds to wait between reconnection attempts. A positive integer. Default: - 1
        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID

        stability
        :stability: experimental
        """
        props = GelfLogDriverProps(address=address, compression_level=compression_level, compression_type=compression_type, tcp_max_reconnect=tcp_max_reconnect, tcp_reconnect_delay=tcp_reconnect_delay, env=env, env_regex=env_regex, labels=labels, tag=tag)

        return jsii.sinvoke(cls, "gelf", [props])

    @jsii.member(jsii_name="journald")
    @builtins.classmethod
    def journald(cls, *, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None) -> "LogDriver":
        """Creates a log driver configuration that sends log information to journald Logs.

        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID

        stability
        :stability: experimental
        """
        props = JournaldLogDriverProps(env=env, env_regex=env_regex, labels=labels, tag=tag)

        return jsii.sinvoke(cls, "journald", [props])

    @jsii.member(jsii_name="jsonFile")
    @builtins.classmethod
    def json_file(cls, *, compress: typing.Optional[bool]=None, max_file: typing.Optional[jsii.Number]=None, max_size: typing.Optional[str]=None, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None) -> "LogDriver":
        """Creates a log driver configuration that sends log information to json-file Logs.

        :param compress: Toggles compression for rotated logs. Default: - false
        :param max_file: The maximum number of log files that can be present. If rolling the logs creates excess files, the oldest file is removed. Only effective when max-size is also set. A positive integer. Default: - 1
        :param max_size: The maximum size of the log before it is rolled. A positive integer plus a modifier representing the unit of measure (k, m, or g). Default: - -1 (unlimited)
        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID

        stability
        :stability: experimental
        """
        props = JsonFileLogDriverProps(compress=compress, max_file=max_file, max_size=max_size, env=env, env_regex=env_regex, labels=labels, tag=tag)

        return jsii.sinvoke(cls, "jsonFile", [props])

    @jsii.member(jsii_name="splunk")
    @builtins.classmethod
    def splunk(cls, *, token: _SecretValue_99478b8b, url: str, ca_name: typing.Optional[str]=None, ca_path: typing.Optional[str]=None, format: typing.Optional["SplunkLogFormat"]=None, gzip: typing.Optional[bool]=None, gzip_level: typing.Optional[jsii.Number]=None, index: typing.Optional[str]=None, insecure_skip_verify: typing.Optional[str]=None, source: typing.Optional[str]=None, source_type: typing.Optional[str]=None, verify_connection: typing.Optional[bool]=None, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None) -> "LogDriver":
        """Creates a log driver configuration that sends log information to splunk Logs.

        :param token: Splunk HTTP Event Collector token.
        :param url: Path to your Splunk Enterprise, self-service Splunk Cloud instance, or Splunk Cloud managed cluster (including port and scheme used by HTTP Event Collector) in one of the following formats: https://your_splunk_instance:8088 or https://input-prd-p-XXXXXXX.cloud.splunk.com:8088 or https://http-inputs-XXXXXXXX.splunkcloud.com.
        :param ca_name: Name to use for validating server certificate. Default: - The hostname of the splunk-url
        :param ca_path: Path to root certificate. Default: - caPath not set.
        :param format: Message format. Can be inline, json or raw. Default: - inline
        :param gzip: Enable/disable gzip compression to send events to Splunk Enterprise or Splunk Cloud instance. Default: - false
        :param gzip_level: Set compression level for gzip. Valid values are -1 (default), 0 (no compression), 1 (best speed) ... 9 (best compression). Default: - -1 (Default Compression)
        :param index: Event index. Default: - index not set.
        :param insecure_skip_verify: Ignore server certificate validation. Default: - insecureSkipVerify not set.
        :param source: Event source. Default: - source not set.
        :param source_type: Event source type. Default: - sourceType not set.
        :param verify_connection: Verify on start, that docker can connect to Splunk server. Default: - true
        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID

        stability
        :stability: experimental
        """
        props = SplunkLogDriverProps(token=token, url=url, ca_name=ca_name, ca_path=ca_path, format=format, gzip=gzip, gzip_level=gzip_level, index=index, insecure_skip_verify=insecure_skip_verify, source=source, source_type=source_type, verify_connection=verify_connection, env=env, env_regex=env_regex, labels=labels, tag=tag)

        return jsii.sinvoke(cls, "splunk", [props])

    @jsii.member(jsii_name="syslog")
    @builtins.classmethod
    def syslog(cls, *, address: typing.Optional[str]=None, facility: typing.Optional[str]=None, format: typing.Optional[str]=None, tls_ca_cert: typing.Optional[str]=None, tls_cert: typing.Optional[str]=None, tls_key: typing.Optional[str]=None, tls_skip_verify: typing.Optional[bool]=None, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None) -> "LogDriver":
        """Creates a log driver configuration that sends log information to syslog Logs.

        :param address: The address of an external syslog server. The URI specifier may be [tcp|udp|tcp+tls]://host:port, unix://path, or unixgram://path. Default: - If the transport is tcp, udp, or tcp+tls, the default port is 514.
        :param facility: The syslog facility to use. Can be the number or name for any valid syslog facility. See the syslog documentation: https://tools.ietf.org/html/rfc5424#section-6.2.1. Default: - facility not set
        :param format: The syslog message format to use. If not specified the local UNIX syslog format is used, without a specified hostname. Specify rfc3164 for the RFC-3164 compatible format, rfc5424 for RFC-5424 compatible format, or rfc5424micro for RFC-5424 compatible format with microsecond timestamp resolution. Default: - format not set
        :param tls_ca_cert: The absolute path to the trust certificates signed by the CA. Ignored if the address protocol is not tcp+tls. Default: - tlsCaCert not set
        :param tls_cert: The absolute path to the TLS certificate file. Ignored if the address protocol is not tcp+tls. Default: - tlsCert not set
        :param tls_key: The absolute path to the TLS key file. Ignored if the address protocol is not tcp+tls. Default: - tlsKey not set
        :param tls_skip_verify: If set to true, TLS verification is skipped when connecting to the syslog daemon. Ignored if the address protocol is not tcp+tls. Default: - false
        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID

        stability
        :stability: experimental
        """
        props = SyslogLogDriverProps(address=address, facility=facility, format=format, tls_ca_cert=tls_ca_cert, tls_cert=tls_cert, tls_key=tls_key, tls_skip_verify=tls_skip_verify, env=env, env_regex=env_regex, labels=labels, tag=tag)

        return jsii.sinvoke(cls, "syslog", [props])


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.MemoryUtilizationScalingProps", jsii_struct_bases=[_BaseTargetTrackingProps_3d6586ed], name_mapping={'disable_scale_in': 'disableScaleIn', 'policy_name': 'policyName', 'scale_in_cooldown': 'scaleInCooldown', 'scale_out_cooldown': 'scaleOutCooldown', 'target_utilization_percent': 'targetUtilizationPercent'})
class MemoryUtilizationScalingProps(_BaseTargetTrackingProps_3d6586ed):
    def __init__(self, *, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown: typing.Optional[_Duration_5170c158]=None, scale_out_cooldown: typing.Optional[_Duration_5170c158]=None, target_utilization_percent: jsii.Number) -> None:
        """The properties for enabling scaling based on memory utilization.

        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. Default: false
        :param policy_name: A name for the scaling policy. Default: - Automatically generated name.
        :param scale_in_cooldown: Period after a scale in activity completes before another scale in activity can start. Default: Duration.seconds(300) for the following scalable targets: ECS services, Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters, Amazon SageMaker endpoint variants, Custom resources. For all other scalable targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB global secondary indexes, Amazon Comprehend document classification endpoints, Lambda provisioned concurrency
        :param scale_out_cooldown: Period after a scale out activity completes before another scale out activity can start. Default: Duration.seconds(300) for the following scalable targets: ECS services, Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters, Amazon SageMaker endpoint variants, Custom resources. For all other scalable targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB global secondary indexes, Amazon Comprehend document classification endpoints, Lambda provisioned concurrency
        :param target_utilization_percent: The target value for memory utilization across all tasks in the service.

        stability
        :stability: experimental
        """
        self._values = {
            'target_utilization_percent': target_utilization_percent,
        }
        if disable_scale_in is not None: self._values["disable_scale_in"] = disable_scale_in
        if policy_name is not None: self._values["policy_name"] = policy_name
        if scale_in_cooldown is not None: self._values["scale_in_cooldown"] = scale_in_cooldown
        if scale_out_cooldown is not None: self._values["scale_out_cooldown"] = scale_out_cooldown

    @builtins.property
    def disable_scale_in(self) -> typing.Optional[bool]:
        """Indicates whether scale in by the target tracking policy is disabled.

        If the value is true, scale in is disabled and the target tracking policy
        won't remove capacity from the scalable resource. Otherwise, scale in is
        enabled and the target tracking policy can remove capacity from the
        scalable resource.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('disable_scale_in')

    @builtins.property
    def policy_name(self) -> typing.Optional[str]:
        """A name for the scaling policy.

        default
        :default: - Automatically generated name.

        stability
        :stability: experimental
        """
        return self._values.get('policy_name')

    @builtins.property
    def scale_in_cooldown(self) -> typing.Optional[_Duration_5170c158]:
        """Period after a scale in activity completes before another scale in activity can start.

        default
        :default:

        Duration.seconds(300) for the following scalable targets: ECS services,
        Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters,
        Amazon SageMaker endpoint variants, Custom resources. For all other scalable
        targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB
        global secondary indexes, Amazon Comprehend document classification endpoints,
        Lambda provisioned concurrency

        stability
        :stability: experimental
        """
        return self._values.get('scale_in_cooldown')

    @builtins.property
    def scale_out_cooldown(self) -> typing.Optional[_Duration_5170c158]:
        """Period after a scale out activity completes before another scale out activity can start.

        default
        :default:

        Duration.seconds(300) for the following scalable targets: ECS services,
        Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters,
        Amazon SageMaker endpoint variants, Custom resources. For all other scalable
        targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB
        global secondary indexes, Amazon Comprehend document classification endpoints,
        Lambda provisioned concurrency

        stability
        :stability: experimental
        """
        return self._values.get('scale_out_cooldown')

    @builtins.property
    def target_utilization_percent(self) -> jsii.Number:
        """The target value for memory utilization across all tasks in the service.

        stability
        :stability: experimental
        """
        return self._values.get('target_utilization_percent')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'MemoryUtilizationScalingProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.MountPoint", jsii_struct_bases=[], name_mapping={'container_path': 'containerPath', 'read_only': 'readOnly', 'source_volume': 'sourceVolume'})
class MountPoint():
    def __init__(self, *, container_path: str, read_only: bool, source_volume: str) -> None:
        """The details of data volume mount points for a container.

        :param container_path: The path on the container to mount the host volume at.
        :param read_only: Specifies whether to give the container read-only access to the volume. If this value is true, the container has read-only access to the volume. If this value is false, then the container can write to the volume.
        :param source_volume: The name of the volume to mount. Must be a volume name referenced in the name parameter of task definition volume.

        stability
        :stability: experimental
        """
        self._values = {
            'container_path': container_path,
            'read_only': read_only,
            'source_volume': source_volume,
        }

    @builtins.property
    def container_path(self) -> str:
        """The path on the container to mount the host volume at.

        stability
        :stability: experimental
        """
        return self._values.get('container_path')

    @builtins.property
    def read_only(self) -> bool:
        """Specifies whether to give the container read-only access to the volume.

        If this value is true, the container has read-only access to the volume.
        If this value is false, then the container can write to the volume.

        stability
        :stability: experimental
        """
        return self._values.get('read_only')

    @builtins.property
    def source_volume(self) -> str:
        """The name of the volume to mount.

        Must be a volume name referenced in the name parameter of task definition volume.

        stability
        :stability: experimental
        """
        return self._values.get('source_volume')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'MountPoint(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.aws_ecs.NetworkMode")
class NetworkMode(enum.Enum):
    """The networking mode to use for the containers in the task.

    stability
    :stability: experimental
    """
    NONE = "NONE"
    """The task's containers do not have external connectivity and port mappings can't be specified in the container definition.

    stability
    :stability: experimental
    """
    BRIDGE = "BRIDGE"
    """The task utilizes Docker's built-in virtual network which runs inside each container instance.

    stability
    :stability: experimental
    """
    AWS_VPC = "AWS_VPC"
    """The task is allocated an elastic network interface.

    stability
    :stability: experimental
    """
    HOST = "HOST"
    """The task bypasses Docker's built-in virtual network and maps container ports directly to the EC2 instance's network interface directly.

    In this mode, you can't run multiple instantiations of the same task on a
    single container instance when port mappings are used.

    stability
    :stability: experimental
    """
    NAT = "NAT"
    """The task utilizes NAT network mode required by Windows containers.

    This is the only supported network mode for Windows containers. For more information, see
    `Task Definition Parameters <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definition_parameters.html#network_mode>`_.

    stability
    :stability: experimental
    """

@jsii.enum(jsii_type="monocdk-experiment.aws_ecs.PidMode")
class PidMode(enum.Enum):
    """The process namespace to use for the containers in the task.

    stability
    :stability: experimental
    """
    HOST = "HOST"
    """If host is specified, then all containers within the tasks that specified the host PID mode on the same container instance share the same process namespace with the host Amazon EC2 instance.

    stability
    :stability: experimental
    """
    TASK = "TASK"
    """If task is specified, all containers within the specified task share the same process namespace.

    stability
    :stability: experimental
    """

class PlacementConstraint(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs.PlacementConstraint"):
    """The placement constraints to use for tasks in the service. For more information, see `Amazon ECS Task Placement Constraints <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-constraints.html>`_.

    Tasks will only be placed on instances that match these rules.

    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="distinctInstances")
    @builtins.classmethod
    def distinct_instances(cls) -> "PlacementConstraint":
        """Use distinctInstance to ensure that each task in a particular group is running on a different container instance.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "distinctInstances", [])

    @jsii.member(jsii_name="memberOf")
    @builtins.classmethod
    def member_of(cls, *expressions: str) -> "PlacementConstraint":
        """Use memberOf to restrict the selection to a group of valid candidates specified by a query expression.

        Multiple expressions can be specified. For more information, see
        `Cluster Query Language <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/cluster-query-language.html>`_.

        You can specify multiple expressions in one call. The tasks will only be placed on instances matching all expressions.

        :param expressions: -

        see
        :see: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/cluster-query-language.html
        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "memberOf", [*expressions])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List["CfnService.PlacementConstraintProperty"]:
        """Return the placement JSON.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toJson", [])


class PlacementStrategy(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs.PlacementStrategy"):
    """The placement strategies to use for tasks in the service. For more information, see `Amazon ECS Task Placement Strategies <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-strategies.html>`_.

    Tasks will preferentially be placed on instances that match these rules.

    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="packedBy")
    @builtins.classmethod
    def packed_by(cls, resource: "BinPackResource") -> "PlacementStrategy":
        """Places tasks on the container instances with the least available capacity of the specified resource.

        :param resource: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "packedBy", [resource])

    @jsii.member(jsii_name="packedByCpu")
    @builtins.classmethod
    def packed_by_cpu(cls) -> "PlacementStrategy":
        """Places tasks on container instances with the least available amount of CPU capacity.

        This minimizes the number of instances in use.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "packedByCpu", [])

    @jsii.member(jsii_name="packedByMemory")
    @builtins.classmethod
    def packed_by_memory(cls) -> "PlacementStrategy":
        """Places tasks on container instances with the least available amount of memory capacity.

        This minimizes the number of instances in use.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "packedByMemory", [])

    @jsii.member(jsii_name="randomly")
    @builtins.classmethod
    def randomly(cls) -> "PlacementStrategy":
        """Places tasks randomly.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "randomly", [])

    @jsii.member(jsii_name="spreadAcross")
    @builtins.classmethod
    def spread_across(cls, *fields: str) -> "PlacementStrategy":
        """Places tasks evenly based on the specified value.

        You can use one of the built-in attributes found on ``BuiltInAttributes``
        or supply your own custom instance attributes. If more than one attribute
        is supplied, spreading is done in order.

        :param fields: -

        default
        :default: attributes instanceId

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "spreadAcross", [*fields])

    @jsii.member(jsii_name="spreadAcrossInstances")
    @builtins.classmethod
    def spread_across_instances(cls) -> "PlacementStrategy":
        """Places tasks evenly across all container instances in the cluster.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "spreadAcrossInstances", [])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List["CfnService.PlacementStrategyProperty"]:
        """Return the placement JSON.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toJson", [])


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.PortMapping", jsii_struct_bases=[], name_mapping={'container_port': 'containerPort', 'host_port': 'hostPort', 'protocol': 'protocol'})
class PortMapping():
    def __init__(self, *, container_port: jsii.Number, host_port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["Protocol"]=None) -> None:
        """Port mappings allow containers to access ports on the host container instance to send or receive traffic.

        :param container_port: The port number on the container that is bound to the user-specified or automatically assigned host port. If you are using containers in a task with the awsvpc or host network mode, exposed ports should be specified using containerPort. If you are using containers in a task with the bridge network mode and you specify a container port and not a host port, your container automatically receives a host port in the ephemeral port range. For more information, see hostPort. Port mappings that are automatically assigned in this way do not count toward the 100 reserved ports limit of a container instance.
        :param host_port: The port number on the container instance to reserve for your container. If you are using containers in a task with the awsvpc or host network mode, the hostPort can either be left blank or set to the same value as the containerPort. If you are using containers in a task with the bridge network mode, you can specify a non-reserved host port for your container port mapping, or you can omit the hostPort (or set it to 0) while specifying a containerPort and your container automatically receives a port in the ephemeral port range for your container instance operating system and Docker version.
        :param protocol: The protocol used for the port mapping. Valid values are Protocol.TCP and Protocol.UDP. Default: TCP

        stability
        :stability: experimental
        """
        self._values = {
            'container_port': container_port,
        }
        if host_port is not None: self._values["host_port"] = host_port
        if protocol is not None: self._values["protocol"] = protocol

    @builtins.property
    def container_port(self) -> jsii.Number:
        """The port number on the container that is bound to the user-specified or automatically assigned host port.

        If you are using containers in a task with the awsvpc or host network mode, exposed ports should be specified using containerPort.
        If you are using containers in a task with the bridge network mode and you specify a container port and not a host port,
        your container automatically receives a host port in the ephemeral port range.

        For more information, see hostPort.
        Port mappings that are automatically assigned in this way do not count toward the 100 reserved ports limit of a container instance.

        stability
        :stability: experimental
        """
        return self._values.get('container_port')

    @builtins.property
    def host_port(self) -> typing.Optional[jsii.Number]:
        """The port number on the container instance to reserve for your container.

        If you are using containers in a task with the awsvpc or host network mode,
        the hostPort can either be left blank or set to the same value as the containerPort.

        If you are using containers in a task with the bridge network mode,
        you can specify a non-reserved host port for your container port mapping, or
        you can omit the hostPort (or set it to 0) while specifying a containerPort and
        your container automatically receives a port in the ephemeral port range for
        your container instance operating system and Docker version.

        stability
        :stability: experimental
        """
        return self._values.get('host_port')

    @builtins.property
    def protocol(self) -> typing.Optional["Protocol"]:
        """The protocol used for the port mapping.

        Valid values are Protocol.TCP and Protocol.UDP.

        default
        :default: TCP

        stability
        :stability: experimental
        """
        return self._values.get('protocol')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'PortMapping(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.aws_ecs.PropagatedTagSource")
class PropagatedTagSource(enum.Enum):
    """Propagate tags from either service or task definition.

    stability
    :stability: experimental
    """
    SERVICE = "SERVICE"
    """Propagate tags from service.

    stability
    :stability: experimental
    """
    TASK_DEFINITION = "TASK_DEFINITION"
    """Propagate tags from task definition.

    stability
    :stability: experimental
    """
    NONE = "NONE"
    """Do not propagate.

    stability
    :stability: experimental
    """

@jsii.enum(jsii_type="monocdk-experiment.aws_ecs.Protocol")
class Protocol(enum.Enum):
    """Network protocol.

    stability
    :stability: experimental
    """
    TCP = "TCP"
    """TCP.

    stability
    :stability: experimental
    """
    UDP = "UDP"
    """UDP.

    stability
    :stability: experimental
    """

class ProxyConfiguration(metaclass=jsii.JSIIAbstractClass, jsii_type="monocdk-experiment.aws_ecs.ProxyConfiguration"):
    """The base class for proxy configurations.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ProxyConfigurationProxy

    def __init__(self) -> None:
        jsii.create(ProxyConfiguration, self, [])

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, _scope: _Construct_f50a3f53, _task_definition: "TaskDefinition") -> "CfnTaskDefinition.ProxyConfigurationProperty":
        """Called when the proxy configuration is configured on a task definition.

        :param _scope: -
        :param _task_definition: -

        stability
        :stability: experimental
        """
        ...


class _ProxyConfigurationProxy(ProxyConfiguration):
    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _Construct_f50a3f53, _task_definition: "TaskDefinition") -> "CfnTaskDefinition.ProxyConfigurationProperty":
        """Called when the proxy configuration is configured on a task definition.

        :param _scope: -
        :param _task_definition: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_scope, _task_definition])


class ProxyConfigurations(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs.ProxyConfigurations"):
    """The base class for proxy configurations.

    stability
    :stability: experimental
    """
    def __init__(self) -> None:
        jsii.create(ProxyConfigurations, self, [])

    @jsii.member(jsii_name="appMeshProxyConfiguration")
    @builtins.classmethod
    def app_mesh_proxy_configuration(cls, *, container_name: str, properties: "AppMeshProxyConfigurationProps") -> "ProxyConfiguration":
        """Constructs a new instance of the ProxyConfiguration class.

        :param container_name: The name of the container that will serve as the App Mesh proxy.
        :param properties: The set of network configuration parameters to provide the Container Network Interface (CNI) plugin.

        stability
        :stability: experimental
        """
        props = AppMeshProxyConfigurationConfigProps(container_name=container_name, properties=properties)

        return jsii.sinvoke(cls, "appMeshProxyConfiguration", [props])


class RepositoryImage(ContainerImage, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs.RepositoryImage"):
    """An image hosted in a public or private repository.

    For images hosted in Amazon ECR, see
    `EcrImage <https://docs.aws.amazon.com/AmazonECR/latest/userguide/images.html>`_.

    stability
    :stability: experimental
    """
    def __init__(self, image_name: str, *, credentials: typing.Optional[_ISecret_75279d36]=None) -> None:
        """Constructs a new instance of the RepositoryImage class.

        :param image_name: -
        :param credentials: The secret to expose to the container that contains the credentials for the image repository. The supported value is the full ARN of an AWS Secrets Manager secret.

        stability
        :stability: experimental
        """
        props = RepositoryImageProps(credentials=credentials)

        jsii.create(RepositoryImage, self, [image_name, props])

    @jsii.member(jsii_name="bind")
    def bind(self, scope: _Construct_f50a3f53, container_definition: "ContainerDefinition") -> "ContainerImageConfig":
        """Called when the image is used by a ContainerDefinition.

        :param scope: -
        :param container_definition: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [scope, container_definition])


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.RepositoryImageProps", jsii_struct_bases=[], name_mapping={'credentials': 'credentials'})
class RepositoryImageProps():
    def __init__(self, *, credentials: typing.Optional[_ISecret_75279d36]=None) -> None:
        """The properties for an image hosted in a public or private repository.

        :param credentials: The secret to expose to the container that contains the credentials for the image repository. The supported value is the full ARN of an AWS Secrets Manager secret.

        stability
        :stability: experimental
        """
        self._values = {
        }
        if credentials is not None: self._values["credentials"] = credentials

    @builtins.property
    def credentials(self) -> typing.Optional[_ISecret_75279d36]:
        """The secret to expose to the container that contains the credentials for the image repository.

        The supported value is the full ARN of an AWS Secrets Manager secret.

        stability
        :stability: experimental
        """
        return self._values.get('credentials')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RepositoryImageProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.RequestCountScalingProps", jsii_struct_bases=[_BaseTargetTrackingProps_3d6586ed], name_mapping={'disable_scale_in': 'disableScaleIn', 'policy_name': 'policyName', 'scale_in_cooldown': 'scaleInCooldown', 'scale_out_cooldown': 'scaleOutCooldown', 'requests_per_target': 'requestsPerTarget', 'target_group': 'targetGroup'})
class RequestCountScalingProps(_BaseTargetTrackingProps_3d6586ed):
    def __init__(self, *, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown: typing.Optional[_Duration_5170c158]=None, scale_out_cooldown: typing.Optional[_Duration_5170c158]=None, requests_per_target: jsii.Number, target_group: _ApplicationTargetGroup_7d0a8d54) -> None:
        """The properties for enabling scaling based on Application Load Balancer (ALB) request counts.

        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. Default: false
        :param policy_name: A name for the scaling policy. Default: - Automatically generated name.
        :param scale_in_cooldown: Period after a scale in activity completes before another scale in activity can start. Default: Duration.seconds(300) for the following scalable targets: ECS services, Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters, Amazon SageMaker endpoint variants, Custom resources. For all other scalable targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB global secondary indexes, Amazon Comprehend document classification endpoints, Lambda provisioned concurrency
        :param scale_out_cooldown: Period after a scale out activity completes before another scale out activity can start. Default: Duration.seconds(300) for the following scalable targets: ECS services, Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters, Amazon SageMaker endpoint variants, Custom resources. For all other scalable targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB global secondary indexes, Amazon Comprehend document classification endpoints, Lambda provisioned concurrency
        :param requests_per_target: The number of ALB requests per target.
        :param target_group: The ALB target group name.

        stability
        :stability: experimental
        """
        self._values = {
            'requests_per_target': requests_per_target,
            'target_group': target_group,
        }
        if disable_scale_in is not None: self._values["disable_scale_in"] = disable_scale_in
        if policy_name is not None: self._values["policy_name"] = policy_name
        if scale_in_cooldown is not None: self._values["scale_in_cooldown"] = scale_in_cooldown
        if scale_out_cooldown is not None: self._values["scale_out_cooldown"] = scale_out_cooldown

    @builtins.property
    def disable_scale_in(self) -> typing.Optional[bool]:
        """Indicates whether scale in by the target tracking policy is disabled.

        If the value is true, scale in is disabled and the target tracking policy
        won't remove capacity from the scalable resource. Otherwise, scale in is
        enabled and the target tracking policy can remove capacity from the
        scalable resource.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('disable_scale_in')

    @builtins.property
    def policy_name(self) -> typing.Optional[str]:
        """A name for the scaling policy.

        default
        :default: - Automatically generated name.

        stability
        :stability: experimental
        """
        return self._values.get('policy_name')

    @builtins.property
    def scale_in_cooldown(self) -> typing.Optional[_Duration_5170c158]:
        """Period after a scale in activity completes before another scale in activity can start.

        default
        :default:

        Duration.seconds(300) for the following scalable targets: ECS services,
        Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters,
        Amazon SageMaker endpoint variants, Custom resources. For all other scalable
        targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB
        global secondary indexes, Amazon Comprehend document classification endpoints,
        Lambda provisioned concurrency

        stability
        :stability: experimental
        """
        return self._values.get('scale_in_cooldown')

    @builtins.property
    def scale_out_cooldown(self) -> typing.Optional[_Duration_5170c158]:
        """Period after a scale out activity completes before another scale out activity can start.

        default
        :default:

        Duration.seconds(300) for the following scalable targets: ECS services,
        Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters,
        Amazon SageMaker endpoint variants, Custom resources. For all other scalable
        targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB
        global secondary indexes, Amazon Comprehend document classification endpoints,
        Lambda provisioned concurrency

        stability
        :stability: experimental
        """
        return self._values.get('scale_out_cooldown')

    @builtins.property
    def requests_per_target(self) -> jsii.Number:
        """The number of ALB requests per target.

        stability
        :stability: experimental
        """
        return self._values.get('requests_per_target')

    @builtins.property
    def target_group(self) -> _ApplicationTargetGroup_7d0a8d54:
        """The ALB target group name.

        stability
        :stability: experimental
        """
        return self._values.get('target_group')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RequestCountScalingProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class ScalableTaskCount(_BaseScalableAttribute_ba74233b, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs.ScalableTaskCount"):
    """The scalable attribute representing task count.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, dimension: str, resource_id: str, role: _IRole_e69bbae4, service_namespace: _ServiceNamespace_23356894, max_capacity: jsii.Number, min_capacity: typing.Optional[jsii.Number]=None) -> None:
        """Constructs a new instance of the ScalableTaskCount class.

        :param scope: -
        :param id: -
        :param dimension: Scalable dimension of the attribute.
        :param resource_id: Resource ID of the attribute.
        :param role: Role to use for scaling.
        :param service_namespace: Service namespace of the scalable attribute.
        :param max_capacity: Maximum capacity to scale to.
        :param min_capacity: Minimum capacity to scale to. Default: 1

        stability
        :stability: experimental
        """
        props = ScalableTaskCountProps(dimension=dimension, resource_id=resource_id, role=role, service_namespace=service_namespace, max_capacity=max_capacity, min_capacity=min_capacity)

        jsii.create(ScalableTaskCount, self, [scope, id, props])

    @jsii.member(jsii_name="scaleOnCpuUtilization")
    def scale_on_cpu_utilization(self, id: str, *, target_utilization_percent: jsii.Number, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown: typing.Optional[_Duration_5170c158]=None, scale_out_cooldown: typing.Optional[_Duration_5170c158]=None) -> None:
        """Scales in or out to achieve a target CPU utilization.

        :param id: -
        :param target_utilization_percent: The target value for CPU utilization across all tasks in the service.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. Default: false
        :param policy_name: A name for the scaling policy. Default: - Automatically generated name.
        :param scale_in_cooldown: Period after a scale in activity completes before another scale in activity can start. Default: Duration.seconds(300) for the following scalable targets: ECS services, Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters, Amazon SageMaker endpoint variants, Custom resources. For all other scalable targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB global secondary indexes, Amazon Comprehend document classification endpoints, Lambda provisioned concurrency
        :param scale_out_cooldown: Period after a scale out activity completes before another scale out activity can start. Default: Duration.seconds(300) for the following scalable targets: ECS services, Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters, Amazon SageMaker endpoint variants, Custom resources. For all other scalable targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB global secondary indexes, Amazon Comprehend document classification endpoints, Lambda provisioned concurrency

        stability
        :stability: experimental
        """
        props = CpuUtilizationScalingProps(target_utilization_percent=target_utilization_percent, disable_scale_in=disable_scale_in, policy_name=policy_name, scale_in_cooldown=scale_in_cooldown, scale_out_cooldown=scale_out_cooldown)

        return jsii.invoke(self, "scaleOnCpuUtilization", [id, props])

    @jsii.member(jsii_name="scaleOnMemoryUtilization")
    def scale_on_memory_utilization(self, id: str, *, target_utilization_percent: jsii.Number, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown: typing.Optional[_Duration_5170c158]=None, scale_out_cooldown: typing.Optional[_Duration_5170c158]=None) -> None:
        """Scales in or out to achieve a target memory utilization.

        :param id: -
        :param target_utilization_percent: The target value for memory utilization across all tasks in the service.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. Default: false
        :param policy_name: A name for the scaling policy. Default: - Automatically generated name.
        :param scale_in_cooldown: Period after a scale in activity completes before another scale in activity can start. Default: Duration.seconds(300) for the following scalable targets: ECS services, Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters, Amazon SageMaker endpoint variants, Custom resources. For all other scalable targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB global secondary indexes, Amazon Comprehend document classification endpoints, Lambda provisioned concurrency
        :param scale_out_cooldown: Period after a scale out activity completes before another scale out activity can start. Default: Duration.seconds(300) for the following scalable targets: ECS services, Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters, Amazon SageMaker endpoint variants, Custom resources. For all other scalable targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB global secondary indexes, Amazon Comprehend document classification endpoints, Lambda provisioned concurrency

        stability
        :stability: experimental
        """
        props = MemoryUtilizationScalingProps(target_utilization_percent=target_utilization_percent, disable_scale_in=disable_scale_in, policy_name=policy_name, scale_in_cooldown=scale_in_cooldown, scale_out_cooldown=scale_out_cooldown)

        return jsii.invoke(self, "scaleOnMemoryUtilization", [id, props])

    @jsii.member(jsii_name="scaleOnMetric")
    def scale_on_metric(self, id: str, *, metric: _IMetric_bfdc01fe, scaling_steps: typing.List[_ScalingInterval_fac05118], adjustment_type: typing.Optional[_AdjustmentType_868b49bf]=None, cooldown: typing.Optional[_Duration_5170c158]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None) -> None:
        """Scales in or out based on a specified metric value.

        :param id: -
        :param metric: Metric to scale on.
        :param scaling_steps: The intervals for scaling. Maps a range of metric values to a particular scaling behavior.
        :param adjustment_type: How the adjustment numbers inside 'intervals' are interpreted. Default: ChangeInCapacity
        :param cooldown: Grace period after scaling activity. Subsequent scale outs during the cooldown period are squashed so that only the biggest scale out happens. Subsequent scale ins during the cooldown period are ignored. Default: No cooldown period
        :param min_adjustment_magnitude: Minimum absolute number to adjust capacity with as result of percentage scaling. Only when using AdjustmentType = PercentChangeInCapacity, this number controls the minimum absolute effect size. Default: No minimum scaling effect

        stability
        :stability: experimental
        """
        props = _BasicStepScalingPolicyProps_548d6784(metric=metric, scaling_steps=scaling_steps, adjustment_type=adjustment_type, cooldown=cooldown, min_adjustment_magnitude=min_adjustment_magnitude)

        return jsii.invoke(self, "scaleOnMetric", [id, props])

    @jsii.member(jsii_name="scaleOnRequestCount")
    def scale_on_request_count(self, id: str, *, requests_per_target: jsii.Number, target_group: _ApplicationTargetGroup_7d0a8d54, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown: typing.Optional[_Duration_5170c158]=None, scale_out_cooldown: typing.Optional[_Duration_5170c158]=None) -> None:
        """Scales in or out to achieve a target Application Load Balancer request count per target.

        :param id: -
        :param requests_per_target: The number of ALB requests per target.
        :param target_group: The ALB target group name.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. Default: false
        :param policy_name: A name for the scaling policy. Default: - Automatically generated name.
        :param scale_in_cooldown: Period after a scale in activity completes before another scale in activity can start. Default: Duration.seconds(300) for the following scalable targets: ECS services, Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters, Amazon SageMaker endpoint variants, Custom resources. For all other scalable targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB global secondary indexes, Amazon Comprehend document classification endpoints, Lambda provisioned concurrency
        :param scale_out_cooldown: Period after a scale out activity completes before another scale out activity can start. Default: Duration.seconds(300) for the following scalable targets: ECS services, Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters, Amazon SageMaker endpoint variants, Custom resources. For all other scalable targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB global secondary indexes, Amazon Comprehend document classification endpoints, Lambda provisioned concurrency

        stability
        :stability: experimental
        """
        props = RequestCountScalingProps(requests_per_target=requests_per_target, target_group=target_group, disable_scale_in=disable_scale_in, policy_name=policy_name, scale_in_cooldown=scale_in_cooldown, scale_out_cooldown=scale_out_cooldown)

        return jsii.invoke(self, "scaleOnRequestCount", [id, props])

    @jsii.member(jsii_name="scaleOnSchedule")
    def scale_on_schedule(self, id: str, *, schedule: _Schedule_6cd13e0d, end_time: typing.Optional[datetime.datetime]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, start_time: typing.Optional[datetime.datetime]=None) -> None:
        """Scales in or out based on a specified scheduled time.

        :param id: -
        :param schedule: When to perform this action.
        :param end_time: When this scheduled action expires. Default: The rule never expires.
        :param max_capacity: The new maximum capacity. During the scheduled time, the current capacity is above the maximum capacity, Application Auto Scaling scales in to the maximum capacity. At least one of maxCapacity and minCapacity must be supplied. Default: No new maximum capacity
        :param min_capacity: The new minimum capacity. During the scheduled time, if the current capacity is below the minimum capacity, Application Auto Scaling scales out to the minimum capacity. At least one of maxCapacity and minCapacity must be supplied. Default: No new minimum capacity
        :param start_time: When this scheduled action becomes active. Default: The rule is activate immediately

        stability
        :stability: experimental
        """
        props = _ScalingSchedule_c85ff455(schedule=schedule, end_time=end_time, max_capacity=max_capacity, min_capacity=min_capacity, start_time=start_time)

        return jsii.invoke(self, "scaleOnSchedule", [id, props])

    @jsii.member(jsii_name="scaleToTrackCustomMetric")
    def scale_to_track_custom_metric(self, id: str, *, metric: _IMetric_bfdc01fe, target_value: jsii.Number, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown: typing.Optional[_Duration_5170c158]=None, scale_out_cooldown: typing.Optional[_Duration_5170c158]=None) -> None:
        """Scales in or out to achieve a target on a custom metric.

        :param id: -
        :param metric: The custom CloudWatch metric to track. The metric must represent utilization; that is, you will always get the following behavior: - metric > targetValue => scale out - metric < targetValue => scale in
        :param target_value: The target value for the custom CloudWatch metric.
        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. Default: false
        :param policy_name: A name for the scaling policy. Default: - Automatically generated name.
        :param scale_in_cooldown: Period after a scale in activity completes before another scale in activity can start. Default: Duration.seconds(300) for the following scalable targets: ECS services, Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters, Amazon SageMaker endpoint variants, Custom resources. For all other scalable targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB global secondary indexes, Amazon Comprehend document classification endpoints, Lambda provisioned concurrency
        :param scale_out_cooldown: Period after a scale out activity completes before another scale out activity can start. Default: Duration.seconds(300) for the following scalable targets: ECS services, Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters, Amazon SageMaker endpoint variants, Custom resources. For all other scalable targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB global secondary indexes, Amazon Comprehend document classification endpoints, Lambda provisioned concurrency

        stability
        :stability: experimental
        """
        props = TrackCustomMetricProps(metric=metric, target_value=target_value, disable_scale_in=disable_scale_in, policy_name=policy_name, scale_in_cooldown=scale_in_cooldown, scale_out_cooldown=scale_out_cooldown)

        return jsii.invoke(self, "scaleToTrackCustomMetric", [id, props])


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.ScalableTaskCountProps", jsii_struct_bases=[_BaseScalableAttributeProps_c3394117], name_mapping={'max_capacity': 'maxCapacity', 'min_capacity': 'minCapacity', 'dimension': 'dimension', 'resource_id': 'resourceId', 'role': 'role', 'service_namespace': 'serviceNamespace'})
class ScalableTaskCountProps(_BaseScalableAttributeProps_c3394117):
    def __init__(self, *, max_capacity: jsii.Number, min_capacity: typing.Optional[jsii.Number]=None, dimension: str, resource_id: str, role: _IRole_e69bbae4, service_namespace: _ServiceNamespace_23356894) -> None:
        """The properties of a scalable attribute representing task count.

        :param max_capacity: Maximum capacity to scale to.
        :param min_capacity: Minimum capacity to scale to. Default: 1
        :param dimension: Scalable dimension of the attribute.
        :param resource_id: Resource ID of the attribute.
        :param role: Role to use for scaling.
        :param service_namespace: Service namespace of the scalable attribute.

        stability
        :stability: experimental
        """
        self._values = {
            'max_capacity': max_capacity,
            'dimension': dimension,
            'resource_id': resource_id,
            'role': role,
            'service_namespace': service_namespace,
        }
        if min_capacity is not None: self._values["min_capacity"] = min_capacity

    @builtins.property
    def max_capacity(self) -> jsii.Number:
        """Maximum capacity to scale to.

        stability
        :stability: experimental
        """
        return self._values.get('max_capacity')

    @builtins.property
    def min_capacity(self) -> typing.Optional[jsii.Number]:
        """Minimum capacity to scale to.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('min_capacity')

    @builtins.property
    def dimension(self) -> str:
        """Scalable dimension of the attribute.

        stability
        :stability: experimental
        """
        return self._values.get('dimension')

    @builtins.property
    def resource_id(self) -> str:
        """Resource ID of the attribute.

        stability
        :stability: experimental
        """
        return self._values.get('resource_id')

    @builtins.property
    def role(self) -> _IRole_e69bbae4:
        """Role to use for scaling.

        stability
        :stability: experimental
        """
        return self._values.get('role')

    @builtins.property
    def service_namespace(self) -> _ServiceNamespace_23356894:
        """Service namespace of the scalable attribute.

        stability
        :stability: experimental
        """
        return self._values.get('service_namespace')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ScalableTaskCountProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.aws_ecs.Scope")
class Scope(enum.Enum):
    """The scope for the Docker volume that determines its lifecycle.

    Docker volumes that are scoped to a task are automatically provisioned when the task starts and destroyed when the task stops.
    Docker volumes that are scoped as shared persist after the task stops.

    stability
    :stability: experimental
    """
    TASK = "TASK"
    """Docker volumes that are scoped to a task are automatically provisioned when the task starts and destroyed when the task stops.

    stability
    :stability: experimental
    """
    SHARED = "SHARED"
    """Docker volumes that are scoped as shared persist after the task stops.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.ScratchSpace", jsii_struct_bases=[], name_mapping={'container_path': 'containerPath', 'name': 'name', 'read_only': 'readOnly', 'source_path': 'sourcePath'})
class ScratchSpace():
    def __init__(self, *, container_path: str, name: str, read_only: bool, source_path: str) -> None:
        """The temporary disk space mounted to the container.

        :param container_path: The path on the container to mount the scratch volume at.
        :param name: The name of the scratch volume to mount. Must be a volume name referenced in the name parameter of task definition volume.
        :param read_only: Specifies whether to give the container read-only access to the scratch volume. If this value is true, the container has read-only access to the scratch volume. If this value is false, then the container can write to the scratch volume.
        :param source_path: 

        stability
        :stability: experimental
        """
        self._values = {
            'container_path': container_path,
            'name': name,
            'read_only': read_only,
            'source_path': source_path,
        }

    @builtins.property
    def container_path(self) -> str:
        """The path on the container to mount the scratch volume at.

        stability
        :stability: experimental
        """
        return self._values.get('container_path')

    @builtins.property
    def name(self) -> str:
        """The name of the scratch volume to mount.

        Must be a volume name referenced in the name parameter of task definition volume.

        stability
        :stability: experimental
        """
        return self._values.get('name')

    @builtins.property
    def read_only(self) -> bool:
        """Specifies whether to give the container read-only access to the scratch volume.

        If this value is true, the container has read-only access to the scratch volume.
        If this value is false, then the container can write to the scratch volume.

        stability
        :stability: experimental
        """
        return self._values.get('read_only')

    @builtins.property
    def source_path(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get('source_path')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ScratchSpace(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class Secret(metaclass=jsii.JSIIAbstractClass, jsii_type="monocdk-experiment.aws_ecs.Secret"):
    """A secret environment variable.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _SecretProxy

    def __init__(self) -> None:
        jsii.create(Secret, self, [])

    @jsii.member(jsii_name="fromSecretsManager")
    @builtins.classmethod
    def from_secrets_manager(cls, secret: _ISecret_75279d36, field: typing.Optional[str]=None) -> "Secret":
        """Creates a environment variable value from a secret stored in AWS Secrets Manager.

        :param secret: the secret stored in AWS Secrets Manager.
        :param field: the name of the field with the value that you want to set as the environment variable value. Only values in JSON format are supported. If you do not specify a JSON field, then the full content of the secret is used.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromSecretsManager", [secret, field])

    @jsii.member(jsii_name="fromSsmParameter")
    @builtins.classmethod
    def from_ssm_parameter(cls, parameter: _IParameter_f25c9bbf) -> "Secret":
        """Creates an environment variable value from a parameter stored in AWS Systems Manager Parameter Store.

        :param parameter: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromSsmParameter", [parameter])

    @jsii.member(jsii_name="grantRead")
    @abc.abstractmethod
    def grant_read(self, grantee: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Grants reading the secret to a principal.

        :param grantee: -

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="arn")
    @abc.abstractmethod
    def arn(self) -> str:
        """The ARN of the secret.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="hasField")
    @abc.abstractmethod
    def has_field(self) -> typing.Optional[bool]:
        """Whether this secret uses a specific JSON field.

        stability
        :stability: experimental
        """
        ...


class _SecretProxy(Secret):
    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Grants reading the secret to a principal.

        :param grantee: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantRead", [grantee])

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> str:
        """The ARN of the secret.

        stability
        :stability: experimental
        """
        return jsii.get(self, "arn")

    @builtins.property
    @jsii.member(jsii_name="hasField")
    def has_field(self) -> typing.Optional[bool]:
        """Whether this secret uses a specific JSON field.

        stability
        :stability: experimental
        """
        return jsii.get(self, "hasField")


class SplunkLogDriver(LogDriver, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs.SplunkLogDriver"):
    """A log driver that sends log information to splunk Logs.

    stability
    :stability: experimental
    """
    def __init__(self, *, token: _SecretValue_99478b8b, url: str, ca_name: typing.Optional[str]=None, ca_path: typing.Optional[str]=None, format: typing.Optional["SplunkLogFormat"]=None, gzip: typing.Optional[bool]=None, gzip_level: typing.Optional[jsii.Number]=None, index: typing.Optional[str]=None, insecure_skip_verify: typing.Optional[str]=None, source: typing.Optional[str]=None, source_type: typing.Optional[str]=None, verify_connection: typing.Optional[bool]=None, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None) -> None:
        """Constructs a new instance of the SplunkLogDriver class.

        :param token: Splunk HTTP Event Collector token.
        :param url: Path to your Splunk Enterprise, self-service Splunk Cloud instance, or Splunk Cloud managed cluster (including port and scheme used by HTTP Event Collector) in one of the following formats: https://your_splunk_instance:8088 or https://input-prd-p-XXXXXXX.cloud.splunk.com:8088 or https://http-inputs-XXXXXXXX.splunkcloud.com.
        :param ca_name: Name to use for validating server certificate. Default: - The hostname of the splunk-url
        :param ca_path: Path to root certificate. Default: - caPath not set.
        :param format: Message format. Can be inline, json or raw. Default: - inline
        :param gzip: Enable/disable gzip compression to send events to Splunk Enterprise or Splunk Cloud instance. Default: - false
        :param gzip_level: Set compression level for gzip. Valid values are -1 (default), 0 (no compression), 1 (best speed) ... 9 (best compression). Default: - -1 (Default Compression)
        :param index: Event index. Default: - index not set.
        :param insecure_skip_verify: Ignore server certificate validation. Default: - insecureSkipVerify not set.
        :param source: Event source. Default: - source not set.
        :param source_type: Event source type. Default: - sourceType not set.
        :param verify_connection: Verify on start, that docker can connect to Splunk server. Default: - true
        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID

        stability
        :stability: experimental
        """
        props = SplunkLogDriverProps(token=token, url=url, ca_name=ca_name, ca_path=ca_path, format=format, gzip=gzip, gzip_level=gzip_level, index=index, insecure_skip_verify=insecure_skip_verify, source=source, source_type=source_type, verify_connection=verify_connection, env=env, env_regex=env_regex, labels=labels, tag=tag)

        jsii.create(SplunkLogDriver, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _Construct_f50a3f53, _container_definition: "ContainerDefinition") -> "LogDriverConfig":
        """Called when the log driver is configured on a container.

        :param _scope: -
        :param _container_definition: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_scope, _container_definition])


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.SplunkLogDriverProps", jsii_struct_bases=[BaseLogDriverProps], name_mapping={'env': 'env', 'env_regex': 'envRegex', 'labels': 'labels', 'tag': 'tag', 'token': 'token', 'url': 'url', 'ca_name': 'caName', 'ca_path': 'caPath', 'format': 'format', 'gzip': 'gzip', 'gzip_level': 'gzipLevel', 'index': 'index', 'insecure_skip_verify': 'insecureSkipVerify', 'source': 'source', 'source_type': 'sourceType', 'verify_connection': 'verifyConnection'})
class SplunkLogDriverProps(BaseLogDriverProps):
    def __init__(self, *, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None, token: _SecretValue_99478b8b, url: str, ca_name: typing.Optional[str]=None, ca_path: typing.Optional[str]=None, format: typing.Optional["SplunkLogFormat"]=None, gzip: typing.Optional[bool]=None, gzip_level: typing.Optional[jsii.Number]=None, index: typing.Optional[str]=None, insecure_skip_verify: typing.Optional[str]=None, source: typing.Optional[str]=None, source_type: typing.Optional[str]=None, verify_connection: typing.Optional[bool]=None) -> None:
        """Specifies the splunk log driver configuration options.

        `Source <https://docs.docker.com/config/containers/logging/splunk/>`_

        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID
        :param token: Splunk HTTP Event Collector token.
        :param url: Path to your Splunk Enterprise, self-service Splunk Cloud instance, or Splunk Cloud managed cluster (including port and scheme used by HTTP Event Collector) in one of the following formats: https://your_splunk_instance:8088 or https://input-prd-p-XXXXXXX.cloud.splunk.com:8088 or https://http-inputs-XXXXXXXX.splunkcloud.com.
        :param ca_name: Name to use for validating server certificate. Default: - The hostname of the splunk-url
        :param ca_path: Path to root certificate. Default: - caPath not set.
        :param format: Message format. Can be inline, json or raw. Default: - inline
        :param gzip: Enable/disable gzip compression to send events to Splunk Enterprise or Splunk Cloud instance. Default: - false
        :param gzip_level: Set compression level for gzip. Valid values are -1 (default), 0 (no compression), 1 (best speed) ... 9 (best compression). Default: - -1 (Default Compression)
        :param index: Event index. Default: - index not set.
        :param insecure_skip_verify: Ignore server certificate validation. Default: - insecureSkipVerify not set.
        :param source: Event source. Default: - source not set.
        :param source_type: Event source type. Default: - sourceType not set.
        :param verify_connection: Verify on start, that docker can connect to Splunk server. Default: - true

        stability
        :stability: experimental
        """
        self._values = {
            'token': token,
            'url': url,
        }
        if env is not None: self._values["env"] = env
        if env_regex is not None: self._values["env_regex"] = env_regex
        if labels is not None: self._values["labels"] = labels
        if tag is not None: self._values["tag"] = tag
        if ca_name is not None: self._values["ca_name"] = ca_name
        if ca_path is not None: self._values["ca_path"] = ca_path
        if format is not None: self._values["format"] = format
        if gzip is not None: self._values["gzip"] = gzip
        if gzip_level is not None: self._values["gzip_level"] = gzip_level
        if index is not None: self._values["index"] = index
        if insecure_skip_verify is not None: self._values["insecure_skip_verify"] = insecure_skip_verify
        if source is not None: self._values["source"] = source
        if source_type is not None: self._values["source_type"] = source_type
        if verify_connection is not None: self._values["verify_connection"] = verify_connection

    @builtins.property
    def env(self) -> typing.Optional[typing.List[str]]:
        """The env option takes an array of keys.

        If there is collision between
        label and env keys, the value of the env takes precedence. Adds additional fields
        to the extra attributes of a logging message.

        default
        :default: - No env

        stability
        :stability: experimental
        """
        return self._values.get('env')

    @builtins.property
    def env_regex(self) -> typing.Optional[str]:
        """The env-regex option is similar to and compatible with env.

        Its value is a regular
        expression to match logging-related environment variables. It is used for advanced
        log tag options.

        default
        :default: - No envRegex

        stability
        :stability: experimental
        """
        return self._values.get('env_regex')

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[str]]:
        """The labels option takes an array of keys.

        If there is collision
        between label and env keys, the value of the env takes precedence. Adds additional
        fields to the extra attributes of a logging message.

        default
        :default: - No labels

        stability
        :stability: experimental
        """
        return self._values.get('labels')

    @builtins.property
    def tag(self) -> typing.Optional[str]:
        """By default, Docker uses the first 12 characters of the container ID to tag log messages.

        Refer to the log tag option documentation for customizing the
        log tag format.

        default
        :default: - The first 12 characters of the container ID

        stability
        :stability: experimental
        """
        return self._values.get('tag')

    @builtins.property
    def token(self) -> _SecretValue_99478b8b:
        """Splunk HTTP Event Collector token.

        stability
        :stability: experimental
        """
        return self._values.get('token')

    @builtins.property
    def url(self) -> str:
        """Path to your Splunk Enterprise, self-service Splunk Cloud instance, or Splunk Cloud managed cluster (including port and scheme used by HTTP Event Collector) in one of the following formats: https://your_splunk_instance:8088 or https://input-prd-p-XXXXXXX.cloud.splunk.com:8088 or https://http-inputs-XXXXXXXX.splunkcloud.com.

        stability
        :stability: experimental
        """
        return self._values.get('url')

    @builtins.property
    def ca_name(self) -> typing.Optional[str]:
        """Name to use for validating server certificate.

        default
        :default: - The hostname of the splunk-url

        stability
        :stability: experimental
        """
        return self._values.get('ca_name')

    @builtins.property
    def ca_path(self) -> typing.Optional[str]:
        """Path to root certificate.

        default
        :default: - caPath not set.

        stability
        :stability: experimental
        """
        return self._values.get('ca_path')

    @builtins.property
    def format(self) -> typing.Optional["SplunkLogFormat"]:
        """Message format.

        Can be inline, json or raw.

        default
        :default: - inline

        stability
        :stability: experimental
        """
        return self._values.get('format')

    @builtins.property
    def gzip(self) -> typing.Optional[bool]:
        """Enable/disable gzip compression to send events to Splunk Enterprise or Splunk Cloud instance.

        default
        :default: - false

        stability
        :stability: experimental
        """
        return self._values.get('gzip')

    @builtins.property
    def gzip_level(self) -> typing.Optional[jsii.Number]:
        """Set compression level for gzip.

        Valid values are -1 (default), 0 (no compression),
        1 (best speed) ... 9 (best compression).

        default
        :default: - -1 (Default Compression)

        stability
        :stability: experimental
        """
        return self._values.get('gzip_level')

    @builtins.property
    def index(self) -> typing.Optional[str]:
        """Event index.

        default
        :default: - index not set.

        stability
        :stability: experimental
        """
        return self._values.get('index')

    @builtins.property
    def insecure_skip_verify(self) -> typing.Optional[str]:
        """Ignore server certificate validation.

        default
        :default: - insecureSkipVerify not set.

        stability
        :stability: experimental
        """
        return self._values.get('insecure_skip_verify')

    @builtins.property
    def source(self) -> typing.Optional[str]:
        """Event source.

        default
        :default: - source not set.

        stability
        :stability: experimental
        """
        return self._values.get('source')

    @builtins.property
    def source_type(self) -> typing.Optional[str]:
        """Event source type.

        default
        :default: - sourceType not set.

        stability
        :stability: experimental
        """
        return self._values.get('source_type')

    @builtins.property
    def verify_connection(self) -> typing.Optional[bool]:
        """Verify on start, that docker can connect to Splunk server.

        default
        :default: - true

        stability
        :stability: experimental
        """
        return self._values.get('verify_connection')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SplunkLogDriverProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.aws_ecs.SplunkLogFormat")
class SplunkLogFormat(enum.Enum):
    """Log Message Format.

    stability
    :stability: experimental
    """
    INLINE = "INLINE"
    """
    stability
    :stability: experimental
    """
    JSON = "JSON"
    """
    stability
    :stability: experimental
    """
    RAW = "RAW"
    """
    stability
    :stability: experimental
    """

class SyslogLogDriver(LogDriver, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs.SyslogLogDriver"):
    """A log driver that sends log information to syslog Logs.

    stability
    :stability: experimental
    """
    def __init__(self, *, address: typing.Optional[str]=None, facility: typing.Optional[str]=None, format: typing.Optional[str]=None, tls_ca_cert: typing.Optional[str]=None, tls_cert: typing.Optional[str]=None, tls_key: typing.Optional[str]=None, tls_skip_verify: typing.Optional[bool]=None, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None) -> None:
        """Constructs a new instance of the SyslogLogDriver class.

        :param address: The address of an external syslog server. The URI specifier may be [tcp|udp|tcp+tls]://host:port, unix://path, or unixgram://path. Default: - If the transport is tcp, udp, or tcp+tls, the default port is 514.
        :param facility: The syslog facility to use. Can be the number or name for any valid syslog facility. See the syslog documentation: https://tools.ietf.org/html/rfc5424#section-6.2.1. Default: - facility not set
        :param format: The syslog message format to use. If not specified the local UNIX syslog format is used, without a specified hostname. Specify rfc3164 for the RFC-3164 compatible format, rfc5424 for RFC-5424 compatible format, or rfc5424micro for RFC-5424 compatible format with microsecond timestamp resolution. Default: - format not set
        :param tls_ca_cert: The absolute path to the trust certificates signed by the CA. Ignored if the address protocol is not tcp+tls. Default: - tlsCaCert not set
        :param tls_cert: The absolute path to the TLS certificate file. Ignored if the address protocol is not tcp+tls. Default: - tlsCert not set
        :param tls_key: The absolute path to the TLS key file. Ignored if the address protocol is not tcp+tls. Default: - tlsKey not set
        :param tls_skip_verify: If set to true, TLS verification is skipped when connecting to the syslog daemon. Ignored if the address protocol is not tcp+tls. Default: - false
        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID

        stability
        :stability: experimental
        """
        props = SyslogLogDriverProps(address=address, facility=facility, format=format, tls_ca_cert=tls_ca_cert, tls_cert=tls_cert, tls_key=tls_key, tls_skip_verify=tls_skip_verify, env=env, env_regex=env_regex, labels=labels, tag=tag)

        jsii.create(SyslogLogDriver, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _Construct_f50a3f53, _container_definition: "ContainerDefinition") -> "LogDriverConfig":
        """Called when the log driver is configured on a container.

        :param _scope: -
        :param _container_definition: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_scope, _container_definition])


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.SyslogLogDriverProps", jsii_struct_bases=[BaseLogDriverProps], name_mapping={'env': 'env', 'env_regex': 'envRegex', 'labels': 'labels', 'tag': 'tag', 'address': 'address', 'facility': 'facility', 'format': 'format', 'tls_ca_cert': 'tlsCaCert', 'tls_cert': 'tlsCert', 'tls_key': 'tlsKey', 'tls_skip_verify': 'tlsSkipVerify'})
class SyslogLogDriverProps(BaseLogDriverProps):
    def __init__(self, *, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None, address: typing.Optional[str]=None, facility: typing.Optional[str]=None, format: typing.Optional[str]=None, tls_ca_cert: typing.Optional[str]=None, tls_cert: typing.Optional[str]=None, tls_key: typing.Optional[str]=None, tls_skip_verify: typing.Optional[bool]=None) -> None:
        """Specifies the syslog log driver configuration options.

        `Source <https://docs.docker.com/config/containers/logging/syslog/>`_

        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID
        :param address: The address of an external syslog server. The URI specifier may be [tcp|udp|tcp+tls]://host:port, unix://path, or unixgram://path. Default: - If the transport is tcp, udp, or tcp+tls, the default port is 514.
        :param facility: The syslog facility to use. Can be the number or name for any valid syslog facility. See the syslog documentation: https://tools.ietf.org/html/rfc5424#section-6.2.1. Default: - facility not set
        :param format: The syslog message format to use. If not specified the local UNIX syslog format is used, without a specified hostname. Specify rfc3164 for the RFC-3164 compatible format, rfc5424 for RFC-5424 compatible format, or rfc5424micro for RFC-5424 compatible format with microsecond timestamp resolution. Default: - format not set
        :param tls_ca_cert: The absolute path to the trust certificates signed by the CA. Ignored if the address protocol is not tcp+tls. Default: - tlsCaCert not set
        :param tls_cert: The absolute path to the TLS certificate file. Ignored if the address protocol is not tcp+tls. Default: - tlsCert not set
        :param tls_key: The absolute path to the TLS key file. Ignored if the address protocol is not tcp+tls. Default: - tlsKey not set
        :param tls_skip_verify: If set to true, TLS verification is skipped when connecting to the syslog daemon. Ignored if the address protocol is not tcp+tls. Default: - false

        stability
        :stability: experimental
        """
        self._values = {
        }
        if env is not None: self._values["env"] = env
        if env_regex is not None: self._values["env_regex"] = env_regex
        if labels is not None: self._values["labels"] = labels
        if tag is not None: self._values["tag"] = tag
        if address is not None: self._values["address"] = address
        if facility is not None: self._values["facility"] = facility
        if format is not None: self._values["format"] = format
        if tls_ca_cert is not None: self._values["tls_ca_cert"] = tls_ca_cert
        if tls_cert is not None: self._values["tls_cert"] = tls_cert
        if tls_key is not None: self._values["tls_key"] = tls_key
        if tls_skip_verify is not None: self._values["tls_skip_verify"] = tls_skip_verify

    @builtins.property
    def env(self) -> typing.Optional[typing.List[str]]:
        """The env option takes an array of keys.

        If there is collision between
        label and env keys, the value of the env takes precedence. Adds additional fields
        to the extra attributes of a logging message.

        default
        :default: - No env

        stability
        :stability: experimental
        """
        return self._values.get('env')

    @builtins.property
    def env_regex(self) -> typing.Optional[str]:
        """The env-regex option is similar to and compatible with env.

        Its value is a regular
        expression to match logging-related environment variables. It is used for advanced
        log tag options.

        default
        :default: - No envRegex

        stability
        :stability: experimental
        """
        return self._values.get('env_regex')

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[str]]:
        """The labels option takes an array of keys.

        If there is collision
        between label and env keys, the value of the env takes precedence. Adds additional
        fields to the extra attributes of a logging message.

        default
        :default: - No labels

        stability
        :stability: experimental
        """
        return self._values.get('labels')

    @builtins.property
    def tag(self) -> typing.Optional[str]:
        """By default, Docker uses the first 12 characters of the container ID to tag log messages.

        Refer to the log tag option documentation for customizing the
        log tag format.

        default
        :default: - The first 12 characters of the container ID

        stability
        :stability: experimental
        """
        return self._values.get('tag')

    @builtins.property
    def address(self) -> typing.Optional[str]:
        """The address of an external syslog server.

        The URI specifier may be
        [tcp|udp|tcp+tls]://host:port, unix://path, or unixgram://path.

        default
        :default: - If the transport is tcp, udp, or tcp+tls, the default port is 514.

        stability
        :stability: experimental
        """
        return self._values.get('address')

    @builtins.property
    def facility(self) -> typing.Optional[str]:
        """The syslog facility to use.

        Can be the number or name for any valid
        syslog facility. See the syslog documentation:
        https://tools.ietf.org/html/rfc5424#section-6.2.1.

        default
        :default: - facility not set

        stability
        :stability: experimental
        """
        return self._values.get('facility')

    @builtins.property
    def format(self) -> typing.Optional[str]:
        """The syslog message format to use.

        If not specified the local UNIX syslog
        format is used, without a specified hostname. Specify rfc3164 for the RFC-3164
        compatible format, rfc5424 for RFC-5424 compatible format, or rfc5424micro
        for RFC-5424 compatible format with microsecond timestamp resolution.

        default
        :default: - format not set

        stability
        :stability: experimental
        """
        return self._values.get('format')

    @builtins.property
    def tls_ca_cert(self) -> typing.Optional[str]:
        """The absolute path to the trust certificates signed by the CA.

        Ignored
        if the address protocol is not tcp+tls.

        default
        :default: - tlsCaCert not set

        stability
        :stability: experimental
        """
        return self._values.get('tls_ca_cert')

    @builtins.property
    def tls_cert(self) -> typing.Optional[str]:
        """The absolute path to the TLS certificate file.

        Ignored if the address
        protocol is not tcp+tls.

        default
        :default: - tlsCert not set

        stability
        :stability: experimental
        """
        return self._values.get('tls_cert')

    @builtins.property
    def tls_key(self) -> typing.Optional[str]:
        """The absolute path to the TLS key file.

        Ignored if the address protocol
        is not tcp+tls.

        default
        :default: - tlsKey not set

        stability
        :stability: experimental
        """
        return self._values.get('tls_key')

    @builtins.property
    def tls_skip_verify(self) -> typing.Optional[bool]:
        """If set to true, TLS verification is skipped when connecting to the syslog daemon.

        Ignored if the address protocol is not tcp+tls.

        default
        :default: - false

        stability
        :stability: experimental
        """
        return self._values.get('tls_skip_verify')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SyslogLogDriverProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(ITaskDefinition)
class TaskDefinition(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs.TaskDefinition"):
    """The base class for all task definitions.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, compatibility: "Compatibility", cpu: typing.Optional[str]=None, ipc_mode: typing.Optional["IpcMode"]=None, memory_mib: typing.Optional[str]=None, network_mode: typing.Optional["NetworkMode"]=None, pid_mode: typing.Optional["PidMode"]=None, placement_constraints: typing.Optional[typing.List["PlacementConstraint"]]=None, execution_role: typing.Optional[_IRole_e69bbae4]=None, family: typing.Optional[str]=None, proxy_configuration: typing.Optional["ProxyConfiguration"]=None, task_role: typing.Optional[_IRole_e69bbae4]=None, volumes: typing.Optional[typing.List["Volume"]]=None) -> None:
        """Constructs a new instance of the TaskDefinition class.

        :param scope: -
        :param id: -
        :param compatibility: The task launch type compatiblity requirement.
        :param cpu: The number of cpu units used by the task. If you are using the EC2 launch type, this field is optional and any value can be used. If you are using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) 512 (.5 vCPU) - Available memory values: 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) 1024 (1 vCPU) - Available memory values: 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) 2048 (2 vCPU) - Available memory values: Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) 4096 (4 vCPU) - Available memory values: Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) Default: - CPU units are not specified.
        :param ipc_mode: The IPC resource namespace to use for the containers in the task. Not supported in Fargate and Windows containers. Default: - IpcMode used by the task is not specified
        :param memory_mib: The amount (in MiB) of memory used by the task. If using the EC2 launch type, this field is optional and any value can be used. If using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) Default: - Memory used by task is not specified.
        :param network_mode: The networking mode to use for the containers in the task. On Fargate, the only supported networking mode is AwsVpc. Default: - NetworkMode.Bridge for EC2 tasks, AwsVpc for Fargate tasks.
        :param pid_mode: The process namespace to use for the containers in the task. Not supported in Fargate and Windows containers. Default: - PidMode used by the task is not specified
        :param placement_constraints: The placement constraints to use for tasks in the service. You can specify a maximum of 10 constraints per task (this limit includes constraints in the task definition and those specified at run time). Not supported in Fargate. Default: - No placement constraints.
        :param execution_role: The name of the IAM task execution role that grants the ECS agent to call AWS APIs on your behalf. The role will be used to retrieve container images from ECR and create CloudWatch log groups. Default: - An execution role will be automatically created if you use ECR images in your task definition.
        :param family: The name of a family that this task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param proxy_configuration: The configuration details for the App Mesh proxy. Default: - No proxy configuration.
        :param task_role: The name of the IAM role that grants containers in the task permission to call AWS APIs on your behalf. Default: - A task role is automatically created for you.
        :param volumes: The list of volume definitions for the task. For more information, see `Task Definition Parameter Volumes <https://docs.aws.amazon.com/AmazonECS/latest/developerguide//task_definition_parameters.html#volumes>`_. Default: - No volumes are passed to the Docker daemon on a container instance.

        stability
        :stability: experimental
        """
        props = TaskDefinitionProps(compatibility=compatibility, cpu=cpu, ipc_mode=ipc_mode, memory_mib=memory_mib, network_mode=network_mode, pid_mode=pid_mode, placement_constraints=placement_constraints, execution_role=execution_role, family=family, proxy_configuration=proxy_configuration, task_role=task_role, volumes=volumes)

        jsii.create(TaskDefinition, self, [scope, id, props])

    @jsii.member(jsii_name="fromTaskDefinitionArn")
    @builtins.classmethod
    def from_task_definition_arn(cls, scope: _Construct_f50a3f53, id: str, task_definition_arn: str) -> "ITaskDefinition":
        """Imports a task definition from the specified task definition ARN.

        The task will have a compatibility of EC2+Fargate.

        :param scope: -
        :param id: -
        :param task_definition_arn: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromTaskDefinitionArn", [scope, id, task_definition_arn])

    @jsii.member(jsii_name="addContainer")
    def add_container(self, id: str, *, image: "ContainerImage", command: typing.Optional[typing.List[str]]=None, cpu: typing.Optional[jsii.Number]=None, disable_networking: typing.Optional[bool]=None, dns_search_domains: typing.Optional[typing.List[str]]=None, dns_servers: typing.Optional[typing.List[str]]=None, docker_labels: typing.Optional[typing.Mapping[str, str]]=None, docker_security_options: typing.Optional[typing.List[str]]=None, entry_point: typing.Optional[typing.List[str]]=None, environment: typing.Optional[typing.Mapping[str, str]]=None, essential: typing.Optional[bool]=None, extra_hosts: typing.Optional[typing.Mapping[str, str]]=None, gpu_count: typing.Optional[jsii.Number]=None, health_check: typing.Optional["HealthCheck"]=None, hostname: typing.Optional[str]=None, linux_parameters: typing.Optional["LinuxParameters"]=None, logging: typing.Optional["LogDriver"]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None, privileged: typing.Optional[bool]=None, readonly_root_filesystem: typing.Optional[bool]=None, secrets: typing.Optional[typing.Mapping[str, "Secret"]]=None, start_timeout: typing.Optional[_Duration_5170c158]=None, stop_timeout: typing.Optional[_Duration_5170c158]=None, user: typing.Optional[str]=None, working_directory: typing.Optional[str]=None) -> "ContainerDefinition":
        """Adds a new container to the task definition.

        :param id: -
        :param image: The image used to start a container. This string is passed directly to the Docker daemon. Images in the Docker Hub registry are available by default. Other repositories are specified with either repository-url/image:tag or repository-url/image@digest. TODO: Update these to specify using classes of IContainerImage
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param cpu: The minimum number of CPU units to reserve for the container. Default: - No minimum CPU units reserved.
        :param disable_networking: Specifies whether networking is disabled within the container. When this parameter is true, networking is disabled within the container. Default: false
        :param dns_search_domains: A list of DNS search domains that are presented to the container. Default: - No search domains.
        :param dns_servers: A list of DNS servers that are presented to the container. Default: - Default DNS servers.
        :param docker_labels: A key/value map of labels to add to the container. Default: - No labels.
        :param docker_security_options: A list of strings to provide custom labels for SELinux and AppArmor multi-level security systems. Default: - No security labels.
        :param entry_point: The ENTRYPOINT value to pass to the container. Default: - Entry point configured in container.
        :param environment: The environment variables to pass to the container. Default: - No environment variables.
        :param essential: Specifies whether the container is marked essential. If the essential parameter of a container is marked as true, and that container fails or stops for any reason, all other containers that are part of the task are stopped. If the essential parameter of a container is marked as false, then its failure does not affect the rest of the containers in a task. All tasks must have at least one essential container. If this parameter is omitted, a container is assumed to be essential. Default: true
        :param extra_hosts: A list of hostnames and IP address mappings to append to the /etc/hosts file on the container. Default: - No extra hosts.
        :param gpu_count: The number of GPUs assigned to the container. Default: - No GPUs assigned.
        :param health_check: The health check command and associated configuration parameters for the container. Default: - Health check configuration from container.
        :param hostname: The hostname to use for your container. Default: - Automatic hostname.
        :param linux_parameters: Linux-specific modifications that are applied to the container, such as Linux kernel capabilities. For more information see `KernelCapabilities <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_KernelCapabilities.html>`_. Default: - No Linux parameters.
        :param logging: The log configuration specification for the container. Default: - Containers use the same logging driver that the Docker daemon uses.
        :param memory_limit_mib: The amount (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under heavy contention, Docker attempts to keep the container memory to this soft limit. However, your container can consume more memory when it needs to, up to either the hard limit specified with the memory parameter (if applicable), or all of the available memory on the container instance, whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory reserved.
        :param privileged: Specifies whether the container is marked as privileged. When this parameter is true, the container is given elevated privileges on the host container instance (similar to the root user). Default: false
        :param readonly_root_filesystem: When this parameter is true, the container is given read-only access to its root file system. Default: false
        :param secrets: The secret environment variables to pass to the container. Default: - No secret environment variables.
        :param start_timeout: Time duration (in seconds) to wait before giving up on resolving dependencies for a container. Default: - none
        :param stop_timeout: Time duration (in seconds) to wait before the container is forcefully killed if it doesn't exit normally on its own. Default: - none
        :param user: The user name to use inside the container. Default: root
        :param working_directory: The working directory in which to run commands inside the container. Default: /

        stability
        :stability: experimental
        """
        props = ContainerDefinitionOptions(image=image, command=command, cpu=cpu, disable_networking=disable_networking, dns_search_domains=dns_search_domains, dns_servers=dns_servers, docker_labels=docker_labels, docker_security_options=docker_security_options, entry_point=entry_point, environment=environment, essential=essential, extra_hosts=extra_hosts, gpu_count=gpu_count, health_check=health_check, hostname=hostname, linux_parameters=linux_parameters, logging=logging, memory_limit_mib=memory_limit_mib, memory_reservation_mib=memory_reservation_mib, privileged=privileged, readonly_root_filesystem=readonly_root_filesystem, secrets=secrets, start_timeout=start_timeout, stop_timeout=stop_timeout, user=user, working_directory=working_directory)

        return jsii.invoke(self, "addContainer", [id, props])

    @jsii.member(jsii_name="addExtension")
    def add_extension(self, extension: "ITaskDefinitionExtension") -> None:
        """Adds the specified extention to the task definition.

        Extension can be used to apply a packaged modification to
        a task definition.

        :param extension: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addExtension", [extension])

    @jsii.member(jsii_name="addFirelensLogRouter")
    def add_firelens_log_router(self, id: str, *, firelens_config: "FirelensConfig", image: "ContainerImage", command: typing.Optional[typing.List[str]]=None, cpu: typing.Optional[jsii.Number]=None, disable_networking: typing.Optional[bool]=None, dns_search_domains: typing.Optional[typing.List[str]]=None, dns_servers: typing.Optional[typing.List[str]]=None, docker_labels: typing.Optional[typing.Mapping[str, str]]=None, docker_security_options: typing.Optional[typing.List[str]]=None, entry_point: typing.Optional[typing.List[str]]=None, environment: typing.Optional[typing.Mapping[str, str]]=None, essential: typing.Optional[bool]=None, extra_hosts: typing.Optional[typing.Mapping[str, str]]=None, gpu_count: typing.Optional[jsii.Number]=None, health_check: typing.Optional["HealthCheck"]=None, hostname: typing.Optional[str]=None, linux_parameters: typing.Optional["LinuxParameters"]=None, logging: typing.Optional["LogDriver"]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None, privileged: typing.Optional[bool]=None, readonly_root_filesystem: typing.Optional[bool]=None, secrets: typing.Optional[typing.Mapping[str, "Secret"]]=None, start_timeout: typing.Optional[_Duration_5170c158]=None, stop_timeout: typing.Optional[_Duration_5170c158]=None, user: typing.Optional[str]=None, working_directory: typing.Optional[str]=None) -> "FirelensLogRouter":
        """Adds a firelens log router to the task definition.

        :param id: -
        :param firelens_config: Firelens configuration.
        :param image: The image used to start a container. This string is passed directly to the Docker daemon. Images in the Docker Hub registry are available by default. Other repositories are specified with either repository-url/image:tag or repository-url/image@digest. TODO: Update these to specify using classes of IContainerImage
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param cpu: The minimum number of CPU units to reserve for the container. Default: - No minimum CPU units reserved.
        :param disable_networking: Specifies whether networking is disabled within the container. When this parameter is true, networking is disabled within the container. Default: false
        :param dns_search_domains: A list of DNS search domains that are presented to the container. Default: - No search domains.
        :param dns_servers: A list of DNS servers that are presented to the container. Default: - Default DNS servers.
        :param docker_labels: A key/value map of labels to add to the container. Default: - No labels.
        :param docker_security_options: A list of strings to provide custom labels for SELinux and AppArmor multi-level security systems. Default: - No security labels.
        :param entry_point: The ENTRYPOINT value to pass to the container. Default: - Entry point configured in container.
        :param environment: The environment variables to pass to the container. Default: - No environment variables.
        :param essential: Specifies whether the container is marked essential. If the essential parameter of a container is marked as true, and that container fails or stops for any reason, all other containers that are part of the task are stopped. If the essential parameter of a container is marked as false, then its failure does not affect the rest of the containers in a task. All tasks must have at least one essential container. If this parameter is omitted, a container is assumed to be essential. Default: true
        :param extra_hosts: A list of hostnames and IP address mappings to append to the /etc/hosts file on the container. Default: - No extra hosts.
        :param gpu_count: The number of GPUs assigned to the container. Default: - No GPUs assigned.
        :param health_check: The health check command and associated configuration parameters for the container. Default: - Health check configuration from container.
        :param hostname: The hostname to use for your container. Default: - Automatic hostname.
        :param linux_parameters: Linux-specific modifications that are applied to the container, such as Linux kernel capabilities. For more information see `KernelCapabilities <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_KernelCapabilities.html>`_. Default: - No Linux parameters.
        :param logging: The log configuration specification for the container. Default: - Containers use the same logging driver that the Docker daemon uses.
        :param memory_limit_mib: The amount (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under heavy contention, Docker attempts to keep the container memory to this soft limit. However, your container can consume more memory when it needs to, up to either the hard limit specified with the memory parameter (if applicable), or all of the available memory on the container instance, whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory reserved.
        :param privileged: Specifies whether the container is marked as privileged. When this parameter is true, the container is given elevated privileges on the host container instance (similar to the root user). Default: false
        :param readonly_root_filesystem: When this parameter is true, the container is given read-only access to its root file system. Default: false
        :param secrets: The secret environment variables to pass to the container. Default: - No secret environment variables.
        :param start_timeout: Time duration (in seconds) to wait before giving up on resolving dependencies for a container. Default: - none
        :param stop_timeout: Time duration (in seconds) to wait before the container is forcefully killed if it doesn't exit normally on its own. Default: - none
        :param user: The user name to use inside the container. Default: root
        :param working_directory: The working directory in which to run commands inside the container. Default: /

        stability
        :stability: experimental
        """
        props = FirelensLogRouterDefinitionOptions(firelens_config=firelens_config, image=image, command=command, cpu=cpu, disable_networking=disable_networking, dns_search_domains=dns_search_domains, dns_servers=dns_servers, docker_labels=docker_labels, docker_security_options=docker_security_options, entry_point=entry_point, environment=environment, essential=essential, extra_hosts=extra_hosts, gpu_count=gpu_count, health_check=health_check, hostname=hostname, linux_parameters=linux_parameters, logging=logging, memory_limit_mib=memory_limit_mib, memory_reservation_mib=memory_reservation_mib, privileged=privileged, readonly_root_filesystem=readonly_root_filesystem, secrets=secrets, start_timeout=start_timeout, stop_timeout=stop_timeout, user=user, working_directory=working_directory)

        return jsii.invoke(self, "addFirelensLogRouter", [id, props])

    @jsii.member(jsii_name="addPlacementConstraint")
    def add_placement_constraint(self, constraint: "PlacementConstraint") -> None:
        """Adds the specified placement constraint to the task definition.

        :param constraint: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addPlacementConstraint", [constraint])

    @jsii.member(jsii_name="addToExecutionRolePolicy")
    def add_to_execution_role_policy(self, statement: _PolicyStatement_f75dc775) -> None:
        """Adds a policy statement to the task execution IAM role.

        :param statement: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addToExecutionRolePolicy", [statement])

    @jsii.member(jsii_name="addToTaskRolePolicy")
    def add_to_task_role_policy(self, statement: _PolicyStatement_f75dc775) -> None:
        """Adds a policy statement to the task IAM role.

        :param statement: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addToTaskRolePolicy", [statement])

    @jsii.member(jsii_name="addVolume")
    def add_volume(self, *, name: str, docker_volume_configuration: typing.Optional["DockerVolumeConfiguration"]=None, host: typing.Optional["Host"]=None) -> None:
        """Adds a volume to the task definition.

        :param name: The name of the volume. Up to 255 letters (uppercase and lowercase), numbers, and hyphens are allowed. This name is referenced in the sourceVolume parameter of container definition mountPoints.
        :param docker_volume_configuration: This property is specified when you are using Docker volumes. Docker volumes are only supported when you are using the EC2 launch type. Windows containers only support the use of the local driver. To use bind mounts, specify a host instead.
        :param host: This property is specified when you are using bind mount host volumes. Bind mount host volumes are supported when you are using either the EC2 or Fargate launch types. The contents of the host parameter determine whether your bind mount host volume persists on the host container instance and where it is stored. If the host parameter is empty, then the Docker daemon assigns a host path for your data volume. However, the data is not guaranteed to persist after the containers associated with it stop running.

        stability
        :stability: experimental
        """
        volume = Volume(name=name, docker_volume_configuration=docker_volume_configuration, host=host)

        return jsii.invoke(self, "addVolume", [volume])

    @jsii.member(jsii_name="obtainExecutionRole")
    def obtain_execution_role(self) -> _IRole_e69bbae4:
        """Creates the task execution IAM role if it doesn't already exist.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "obtainExecutionRole", [])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Validates the task definition.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "validate", [])

    @builtins.property
    @jsii.member(jsii_name="compatibility")
    def compatibility(self) -> "Compatibility":
        """The task launch type compatiblity requirement.

        stability
        :stability: experimental
        """
        return jsii.get(self, "compatibility")

    @builtins.property
    @jsii.member(jsii_name="containers")
    def _containers(self) -> typing.List["ContainerDefinition"]:
        """The container definitions.

        stability
        :stability: experimental
        """
        return jsii.get(self, "containers")

    @builtins.property
    @jsii.member(jsii_name="family")
    def family(self) -> str:
        """The name of a family that this task definition is registered to.

        A family groups multiple versions of a task definition.

        stability
        :stability: experimental
        """
        return jsii.get(self, "family")

    @builtins.property
    @jsii.member(jsii_name="isEc2Compatible")
    def is_ec2_compatible(self) -> bool:
        """Return true if the task definition can be run on an EC2 cluster.

        stability
        :stability: experimental
        """
        return jsii.get(self, "isEc2Compatible")

    @builtins.property
    @jsii.member(jsii_name="isFargateCompatible")
    def is_fargate_compatible(self) -> bool:
        """Return true if the task definition can be run on a Fargate cluster.

        stability
        :stability: experimental
        """
        return jsii.get(self, "isFargateCompatible")

    @builtins.property
    @jsii.member(jsii_name="networkMode")
    def network_mode(self) -> "NetworkMode":
        """The networking mode to use for the containers in the task.

        stability
        :stability: experimental
        """
        return jsii.get(self, "networkMode")

    @builtins.property
    @jsii.member(jsii_name="taskDefinitionArn")
    def task_definition_arn(self) -> str:
        """The full Amazon Resource Name (ARN) of the task definition.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "taskDefinitionArn")

    @builtins.property
    @jsii.member(jsii_name="taskRole")
    def task_role(self) -> _IRole_e69bbae4:
        """The name of the IAM role that grants containers in the task permission to call AWS APIs on your behalf.

        stability
        :stability: experimental
        """
        return jsii.get(self, "taskRole")

    @builtins.property
    @jsii.member(jsii_name="executionRole")
    def execution_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """Execution role for this task definition.

        stability
        :stability: experimental
        """
        return jsii.get(self, "executionRole")

    @builtins.property
    @jsii.member(jsii_name="defaultContainer")
    def default_container(self) -> typing.Optional["ContainerDefinition"]:
        """Default container for this task.

        Load balancers will send traffic to this container. The first
        essential container that is added to this task will become the default
        container.

        stability
        :stability: experimental
        """
        return jsii.get(self, "defaultContainer")

    @default_container.setter
    def default_container(self, value: typing.Optional["ContainerDefinition"]) -> None:
        jsii.set(self, "defaultContainer", value)


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.TaskDefinitionProps", jsii_struct_bases=[CommonTaskDefinitionProps], name_mapping={'execution_role': 'executionRole', 'family': 'family', 'proxy_configuration': 'proxyConfiguration', 'task_role': 'taskRole', 'volumes': 'volumes', 'compatibility': 'compatibility', 'cpu': 'cpu', 'ipc_mode': 'ipcMode', 'memory_mib': 'memoryMiB', 'network_mode': 'networkMode', 'pid_mode': 'pidMode', 'placement_constraints': 'placementConstraints'})
class TaskDefinitionProps(CommonTaskDefinitionProps):
    def __init__(self, *, execution_role: typing.Optional[_IRole_e69bbae4]=None, family: typing.Optional[str]=None, proxy_configuration: typing.Optional["ProxyConfiguration"]=None, task_role: typing.Optional[_IRole_e69bbae4]=None, volumes: typing.Optional[typing.List["Volume"]]=None, compatibility: "Compatibility", cpu: typing.Optional[str]=None, ipc_mode: typing.Optional["IpcMode"]=None, memory_mib: typing.Optional[str]=None, network_mode: typing.Optional["NetworkMode"]=None, pid_mode: typing.Optional["PidMode"]=None, placement_constraints: typing.Optional[typing.List["PlacementConstraint"]]=None) -> None:
        """The properties for task definitions.

        :param execution_role: The name of the IAM task execution role that grants the ECS agent to call AWS APIs on your behalf. The role will be used to retrieve container images from ECR and create CloudWatch log groups. Default: - An execution role will be automatically created if you use ECR images in your task definition.
        :param family: The name of a family that this task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param proxy_configuration: The configuration details for the App Mesh proxy. Default: - No proxy configuration.
        :param task_role: The name of the IAM role that grants containers in the task permission to call AWS APIs on your behalf. Default: - A task role is automatically created for you.
        :param volumes: The list of volume definitions for the task. For more information, see `Task Definition Parameter Volumes <https://docs.aws.amazon.com/AmazonECS/latest/developerguide//task_definition_parameters.html#volumes>`_. Default: - No volumes are passed to the Docker daemon on a container instance.
        :param compatibility: The task launch type compatiblity requirement.
        :param cpu: The number of cpu units used by the task. If you are using the EC2 launch type, this field is optional and any value can be used. If you are using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) 512 (.5 vCPU) - Available memory values: 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) 1024 (1 vCPU) - Available memory values: 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) 2048 (2 vCPU) - Available memory values: Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) 4096 (4 vCPU) - Available memory values: Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) Default: - CPU units are not specified.
        :param ipc_mode: The IPC resource namespace to use for the containers in the task. Not supported in Fargate and Windows containers. Default: - IpcMode used by the task is not specified
        :param memory_mib: The amount (in MiB) of memory used by the task. If using the EC2 launch type, this field is optional and any value can be used. If using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) Default: - Memory used by task is not specified.
        :param network_mode: The networking mode to use for the containers in the task. On Fargate, the only supported networking mode is AwsVpc. Default: - NetworkMode.Bridge for EC2 tasks, AwsVpc for Fargate tasks.
        :param pid_mode: The process namespace to use for the containers in the task. Not supported in Fargate and Windows containers. Default: - PidMode used by the task is not specified
        :param placement_constraints: The placement constraints to use for tasks in the service. You can specify a maximum of 10 constraints per task (this limit includes constraints in the task definition and those specified at run time). Not supported in Fargate. Default: - No placement constraints.

        stability
        :stability: experimental
        """
        self._values = {
            'compatibility': compatibility,
        }
        if execution_role is not None: self._values["execution_role"] = execution_role
        if family is not None: self._values["family"] = family
        if proxy_configuration is not None: self._values["proxy_configuration"] = proxy_configuration
        if task_role is not None: self._values["task_role"] = task_role
        if volumes is not None: self._values["volumes"] = volumes
        if cpu is not None: self._values["cpu"] = cpu
        if ipc_mode is not None: self._values["ipc_mode"] = ipc_mode
        if memory_mib is not None: self._values["memory_mib"] = memory_mib
        if network_mode is not None: self._values["network_mode"] = network_mode
        if pid_mode is not None: self._values["pid_mode"] = pid_mode
        if placement_constraints is not None: self._values["placement_constraints"] = placement_constraints

    @builtins.property
    def execution_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The name of the IAM task execution role that grants the ECS agent to call AWS APIs on your behalf.

        The role will be used to retrieve container images from ECR and create CloudWatch log groups.

        default
        :default: - An execution role will be automatically created if you use ECR images in your task definition.

        stability
        :stability: experimental
        """
        return self._values.get('execution_role')

    @builtins.property
    def family(self) -> typing.Optional[str]:
        """The name of a family that this task definition is registered to.

        A family groups multiple versions of a task definition.

        default
        :default: - Automatically generated name.

        stability
        :stability: experimental
        """
        return self._values.get('family')

    @builtins.property
    def proxy_configuration(self) -> typing.Optional["ProxyConfiguration"]:
        """The configuration details for the App Mesh proxy.

        default
        :default: - No proxy configuration.

        stability
        :stability: experimental
        """
        return self._values.get('proxy_configuration')

    @builtins.property
    def task_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The name of the IAM role that grants containers in the task permission to call AWS APIs on your behalf.

        default
        :default: - A task role is automatically created for you.

        stability
        :stability: experimental
        """
        return self._values.get('task_role')

    @builtins.property
    def volumes(self) -> typing.Optional[typing.List["Volume"]]:
        """The list of volume definitions for the task.

        For more information, see
        `Task Definition Parameter Volumes <https://docs.aws.amazon.com/AmazonECS/latest/developerguide//task_definition_parameters.html#volumes>`_.

        default
        :default: - No volumes are passed to the Docker daemon on a container instance.

        stability
        :stability: experimental
        """
        return self._values.get('volumes')

    @builtins.property
    def compatibility(self) -> "Compatibility":
        """The task launch type compatiblity requirement.

        stability
        :stability: experimental
        """
        return self._values.get('compatibility')

    @builtins.property
    def cpu(self) -> typing.Optional[str]:
        """The number of cpu units used by the task.

        If you are using the EC2 launch type, this field is optional and any value can be used.
        If you are using the Fargate launch type, this field is required and you must use one of the following values,
        which determines your range of valid values for the memory parameter:

        256 (.25 vCPU) - Available memory values: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB)
        512 (.5 vCPU) - Available memory values: 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB)
        1024 (1 vCPU) - Available memory values: 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB)
        2048 (2 vCPU) - Available memory values: Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB)
        4096 (4 vCPU) - Available memory values: Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB)

        default
        :default: - CPU units are not specified.

        stability
        :stability: experimental
        """
        return self._values.get('cpu')

    @builtins.property
    def ipc_mode(self) -> typing.Optional["IpcMode"]:
        """The IPC resource namespace to use for the containers in the task.

        Not supported in Fargate and Windows containers.

        default
        :default: - IpcMode used by the task is not specified

        stability
        :stability: experimental
        """
        return self._values.get('ipc_mode')

    @builtins.property
    def memory_mib(self) -> typing.Optional[str]:
        """The amount (in MiB) of memory used by the task.

        If using the EC2 launch type, this field is optional and any value can be used.
        If using the Fargate launch type, this field is required and you must use one of the following values,
        which determines your range of valid values for the cpu parameter:

        512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU)
        1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU)
        2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU)
        Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU)
        Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU)

        default
        :default: - Memory used by task is not specified.

        stability
        :stability: experimental
        """
        return self._values.get('memory_mib')

    @builtins.property
    def network_mode(self) -> typing.Optional["NetworkMode"]:
        """The networking mode to use for the containers in the task.

        On Fargate, the only supported networking mode is AwsVpc.

        default
        :default: - NetworkMode.Bridge for EC2 tasks, AwsVpc for Fargate tasks.

        stability
        :stability: experimental
        """
        return self._values.get('network_mode')

    @builtins.property
    def pid_mode(self) -> typing.Optional["PidMode"]:
        """The process namespace to use for the containers in the task.

        Not supported in Fargate and Windows containers.

        default
        :default: - PidMode used by the task is not specified

        stability
        :stability: experimental
        """
        return self._values.get('pid_mode')

    @builtins.property
    def placement_constraints(self) -> typing.Optional[typing.List["PlacementConstraint"]]:
        """The placement constraints to use for tasks in the service.

        You can specify a maximum of 10 constraints per task (this limit includes
        constraints in the task definition and those specified at run time).

        Not supported in Fargate.

        default
        :default: - No placement constraints.

        stability
        :stability: experimental
        """
        return self._values.get('placement_constraints')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TaskDefinitionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.Tmpfs", jsii_struct_bases=[], name_mapping={'container_path': 'containerPath', 'size': 'size', 'mount_options': 'mountOptions'})
class Tmpfs():
    def __init__(self, *, container_path: str, size: jsii.Number, mount_options: typing.Optional[typing.List["TmpfsMountOption"]]=None) -> None:
        """The details of a tmpfs mount for a container.

        :param container_path: The absolute file path where the tmpfs volume is to be mounted.
        :param size: The size (in MiB) of the tmpfs volume.
        :param mount_options: The list of tmpfs volume mount options. For more information, see `TmpfsMountOptions <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_Tmpfs.html>`_.

        stability
        :stability: experimental
        """
        self._values = {
            'container_path': container_path,
            'size': size,
        }
        if mount_options is not None: self._values["mount_options"] = mount_options

    @builtins.property
    def container_path(self) -> str:
        """The absolute file path where the tmpfs volume is to be mounted.

        stability
        :stability: experimental
        """
        return self._values.get('container_path')

    @builtins.property
    def size(self) -> jsii.Number:
        """The size (in MiB) of the tmpfs volume.

        stability
        :stability: experimental
        """
        return self._values.get('size')

    @builtins.property
    def mount_options(self) -> typing.Optional[typing.List["TmpfsMountOption"]]:
        """The list of tmpfs volume mount options.

        For more information, see
        `TmpfsMountOptions <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_Tmpfs.html>`_.

        stability
        :stability: experimental
        """
        return self._values.get('mount_options')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'Tmpfs(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.aws_ecs.TmpfsMountOption")
class TmpfsMountOption(enum.Enum):
    """The supported options for a tmpfs mount for a container.

    stability
    :stability: experimental
    """
    DEFAULTS = "DEFAULTS"
    """
    stability
    :stability: experimental
    """
    RO = "RO"
    """
    stability
    :stability: experimental
    """
    RW = "RW"
    """
    stability
    :stability: experimental
    """
    SUID = "SUID"
    """
    stability
    :stability: experimental
    """
    NOSUID = "NOSUID"
    """
    stability
    :stability: experimental
    """
    DEV = "DEV"
    """
    stability
    :stability: experimental
    """
    NODEV = "NODEV"
    """
    stability
    :stability: experimental
    """
    EXEC = "EXEC"
    """
    stability
    :stability: experimental
    """
    NOEXEC = "NOEXEC"
    """
    stability
    :stability: experimental
    """
    SYNC = "SYNC"
    """
    stability
    :stability: experimental
    """
    ASYNC = "ASYNC"
    """
    stability
    :stability: experimental
    """
    DIRSYNC = "DIRSYNC"
    """
    stability
    :stability: experimental
    """
    REMOUNT = "REMOUNT"
    """
    stability
    :stability: experimental
    """
    MAND = "MAND"
    """
    stability
    :stability: experimental
    """
    NOMAND = "NOMAND"
    """
    stability
    :stability: experimental
    """
    ATIME = "ATIME"
    """
    stability
    :stability: experimental
    """
    NOATIME = "NOATIME"
    """
    stability
    :stability: experimental
    """
    DIRATIME = "DIRATIME"
    """
    stability
    :stability: experimental
    """
    NODIRATIME = "NODIRATIME"
    """
    stability
    :stability: experimental
    """
    BIND = "BIND"
    """
    stability
    :stability: experimental
    """
    RBIND = "RBIND"
    """
    stability
    :stability: experimental
    """
    UNBINDABLE = "UNBINDABLE"
    """
    stability
    :stability: experimental
    """
    RUNBINDABLE = "RUNBINDABLE"
    """
    stability
    :stability: experimental
    """
    PRIVATE = "PRIVATE"
    """
    stability
    :stability: experimental
    """
    RPRIVATE = "RPRIVATE"
    """
    stability
    :stability: experimental
    """
    SHARED = "SHARED"
    """
    stability
    :stability: experimental
    """
    RSHARED = "RSHARED"
    """
    stability
    :stability: experimental
    """
    SLAVE = "SLAVE"
    """
    stability
    :stability: experimental
    """
    RSLAVE = "RSLAVE"
    """
    stability
    :stability: experimental
    """
    RELATIME = "RELATIME"
    """
    stability
    :stability: experimental
    """
    NORELATIME = "NORELATIME"
    """
    stability
    :stability: experimental
    """
    STRICTATIME = "STRICTATIME"
    """
    stability
    :stability: experimental
    """
    NOSTRICTATIME = "NOSTRICTATIME"
    """
    stability
    :stability: experimental
    """
    MODE = "MODE"
    """
    stability
    :stability: experimental
    """
    UID = "UID"
    """
    stability
    :stability: experimental
    """
    GID = "GID"
    """
    stability
    :stability: experimental
    """
    NR_INODES = "NR_INODES"
    """
    stability
    :stability: experimental
    """
    NR_BLOCKS = "NR_BLOCKS"
    """
    stability
    :stability: experimental
    """
    MPOL = "MPOL"
    """
    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.TrackCustomMetricProps", jsii_struct_bases=[_BaseTargetTrackingProps_3d6586ed], name_mapping={'disable_scale_in': 'disableScaleIn', 'policy_name': 'policyName', 'scale_in_cooldown': 'scaleInCooldown', 'scale_out_cooldown': 'scaleOutCooldown', 'metric': 'metric', 'target_value': 'targetValue'})
class TrackCustomMetricProps(_BaseTargetTrackingProps_3d6586ed):
    def __init__(self, *, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown: typing.Optional[_Duration_5170c158]=None, scale_out_cooldown: typing.Optional[_Duration_5170c158]=None, metric: _IMetric_bfdc01fe, target_value: jsii.Number) -> None:
        """The properties for enabling target tracking scaling based on a custom CloudWatch metric.

        :param disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. Default: false
        :param policy_name: A name for the scaling policy. Default: - Automatically generated name.
        :param scale_in_cooldown: Period after a scale in activity completes before another scale in activity can start. Default: Duration.seconds(300) for the following scalable targets: ECS services, Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters, Amazon SageMaker endpoint variants, Custom resources. For all other scalable targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB global secondary indexes, Amazon Comprehend document classification endpoints, Lambda provisioned concurrency
        :param scale_out_cooldown: Period after a scale out activity completes before another scale out activity can start. Default: Duration.seconds(300) for the following scalable targets: ECS services, Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters, Amazon SageMaker endpoint variants, Custom resources. For all other scalable targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB global secondary indexes, Amazon Comprehend document classification endpoints, Lambda provisioned concurrency
        :param metric: The custom CloudWatch metric to track. The metric must represent utilization; that is, you will always get the following behavior: - metric > targetValue => scale out - metric < targetValue => scale in
        :param target_value: The target value for the custom CloudWatch metric.

        stability
        :stability: experimental
        """
        self._values = {
            'metric': metric,
            'target_value': target_value,
        }
        if disable_scale_in is not None: self._values["disable_scale_in"] = disable_scale_in
        if policy_name is not None: self._values["policy_name"] = policy_name
        if scale_in_cooldown is not None: self._values["scale_in_cooldown"] = scale_in_cooldown
        if scale_out_cooldown is not None: self._values["scale_out_cooldown"] = scale_out_cooldown

    @builtins.property
    def disable_scale_in(self) -> typing.Optional[bool]:
        """Indicates whether scale in by the target tracking policy is disabled.

        If the value is true, scale in is disabled and the target tracking policy
        won't remove capacity from the scalable resource. Otherwise, scale in is
        enabled and the target tracking policy can remove capacity from the
        scalable resource.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('disable_scale_in')

    @builtins.property
    def policy_name(self) -> typing.Optional[str]:
        """A name for the scaling policy.

        default
        :default: - Automatically generated name.

        stability
        :stability: experimental
        """
        return self._values.get('policy_name')

    @builtins.property
    def scale_in_cooldown(self) -> typing.Optional[_Duration_5170c158]:
        """Period after a scale in activity completes before another scale in activity can start.

        default
        :default:

        Duration.seconds(300) for the following scalable targets: ECS services,
        Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters,
        Amazon SageMaker endpoint variants, Custom resources. For all other scalable
        targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB
        global secondary indexes, Amazon Comprehend document classification endpoints,
        Lambda provisioned concurrency

        stability
        :stability: experimental
        """
        return self._values.get('scale_in_cooldown')

    @builtins.property
    def scale_out_cooldown(self) -> typing.Optional[_Duration_5170c158]:
        """Period after a scale out activity completes before another scale out activity can start.

        default
        :default:

        Duration.seconds(300) for the following scalable targets: ECS services,
        Spot Fleet requests, EMR clusters, AppStream 2.0 fleets, Aurora DB clusters,
        Amazon SageMaker endpoint variants, Custom resources. For all other scalable
        targets, the default value is Duration.seconds(0): DynamoDB tables, DynamoDB
        global secondary indexes, Amazon Comprehend document classification endpoints,
        Lambda provisioned concurrency

        stability
        :stability: experimental
        """
        return self._values.get('scale_out_cooldown')

    @builtins.property
    def metric(self) -> _IMetric_bfdc01fe:
        """The custom CloudWatch metric to track.

        The metric must represent utilization; that is, you will always get the following behavior:

        - metric > targetValue => scale out
        - metric < targetValue => scale in

        stability
        :stability: experimental
        """
        return self._values.get('metric')

    @builtins.property
    def target_value(self) -> jsii.Number:
        """The target value for the custom CloudWatch metric.

        stability
        :stability: experimental
        """
        return self._values.get('target_value')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TrackCustomMetricProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.Ulimit", jsii_struct_bases=[], name_mapping={'hard_limit': 'hardLimit', 'name': 'name', 'soft_limit': 'softLimit'})
class Ulimit():
    def __init__(self, *, hard_limit: jsii.Number, name: "UlimitName", soft_limit: jsii.Number) -> None:
        """The ulimit settings to pass to the container.

        NOTE: Does not work for Windows containers.

        :param hard_limit: The hard limit for the ulimit type.
        :param name: The type of the ulimit. For more information, see `UlimitName <https://docs.aws.amazon.com/cdk/api/latest/typescript/api/aws-ecs/ulimitname.html#aws_ecs_UlimitName>`_.
        :param soft_limit: The soft limit for the ulimit type.

        stability
        :stability: experimental
        """
        self._values = {
            'hard_limit': hard_limit,
            'name': name,
            'soft_limit': soft_limit,
        }

    @builtins.property
    def hard_limit(self) -> jsii.Number:
        """The hard limit for the ulimit type.

        stability
        :stability: experimental
        """
        return self._values.get('hard_limit')

    @builtins.property
    def name(self) -> "UlimitName":
        """The type of the ulimit.

        For more information, see `UlimitName <https://docs.aws.amazon.com/cdk/api/latest/typescript/api/aws-ecs/ulimitname.html#aws_ecs_UlimitName>`_.

        stability
        :stability: experimental
        """
        return self._values.get('name')

    @builtins.property
    def soft_limit(self) -> jsii.Number:
        """The soft limit for the ulimit type.

        stability
        :stability: experimental
        """
        return self._values.get('soft_limit')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'Ulimit(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.aws_ecs.UlimitName")
class UlimitName(enum.Enum):
    """Type of resource to set a limit on.

    stability
    :stability: experimental
    """
    CORE = "CORE"
    """
    stability
    :stability: experimental
    """
    CPU = "CPU"
    """
    stability
    :stability: experimental
    """
    DATA = "DATA"
    """
    stability
    :stability: experimental
    """
    FSIZE = "FSIZE"
    """
    stability
    :stability: experimental
    """
    LOCKS = "LOCKS"
    """
    stability
    :stability: experimental
    """
    MEMLOCK = "MEMLOCK"
    """
    stability
    :stability: experimental
    """
    MSGQUEUE = "MSGQUEUE"
    """
    stability
    :stability: experimental
    """
    NICE = "NICE"
    """
    stability
    :stability: experimental
    """
    NOFILE = "NOFILE"
    """
    stability
    :stability: experimental
    """
    NPROC = "NPROC"
    """
    stability
    :stability: experimental
    """
    RSS = "RSS"
    """
    stability
    :stability: experimental
    """
    RTPRIO = "RTPRIO"
    """
    stability
    :stability: experimental
    """
    RTTIME = "RTTIME"
    """
    stability
    :stability: experimental
    """
    SIGPENDING = "SIGPENDING"
    """
    stability
    :stability: experimental
    """
    STACK = "STACK"
    """
    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.Volume", jsii_struct_bases=[], name_mapping={'name': 'name', 'docker_volume_configuration': 'dockerVolumeConfiguration', 'host': 'host'})
class Volume():
    def __init__(self, *, name: str, docker_volume_configuration: typing.Optional["DockerVolumeConfiguration"]=None, host: typing.Optional["Host"]=None) -> None:
        """A data volume used in a task definition.

        For tasks that use a Docker volume, specify a DockerVolumeConfiguration.
        For tasks that use a bind mount host volume, specify a host and optional sourcePath.

        For more information, see `Using Data Volumes in Tasks <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_data_volumes.html>`_.

        :param name: The name of the volume. Up to 255 letters (uppercase and lowercase), numbers, and hyphens are allowed. This name is referenced in the sourceVolume parameter of container definition mountPoints.
        :param docker_volume_configuration: This property is specified when you are using Docker volumes. Docker volumes are only supported when you are using the EC2 launch type. Windows containers only support the use of the local driver. To use bind mounts, specify a host instead.
        :param host: This property is specified when you are using bind mount host volumes. Bind mount host volumes are supported when you are using either the EC2 or Fargate launch types. The contents of the host parameter determine whether your bind mount host volume persists on the host container instance and where it is stored. If the host parameter is empty, then the Docker daemon assigns a host path for your data volume. However, the data is not guaranteed to persist after the containers associated with it stop running.

        stability
        :stability: experimental
        """
        if isinstance(docker_volume_configuration, dict): docker_volume_configuration = DockerVolumeConfiguration(**docker_volume_configuration)
        if isinstance(host, dict): host = Host(**host)
        self._values = {
            'name': name,
        }
        if docker_volume_configuration is not None: self._values["docker_volume_configuration"] = docker_volume_configuration
        if host is not None: self._values["host"] = host

    @builtins.property
    def name(self) -> str:
        """The name of the volume.

        Up to 255 letters (uppercase and lowercase), numbers, and hyphens are allowed.
        This name is referenced in the sourceVolume parameter of container definition mountPoints.

        stability
        :stability: experimental
        """
        return self._values.get('name')

    @builtins.property
    def docker_volume_configuration(self) -> typing.Optional["DockerVolumeConfiguration"]:
        """This property is specified when you are using Docker volumes.

        Docker volumes are only supported when you are using the EC2 launch type.
        Windows containers only support the use of the local driver.
        To use bind mounts, specify a host instead.

        stability
        :stability: experimental
        """
        return self._values.get('docker_volume_configuration')

    @builtins.property
    def host(self) -> typing.Optional["Host"]:
        """This property is specified when you are using bind mount host volumes.

        Bind mount host volumes are supported when you are using either the EC2 or Fargate launch types.
        The contents of the host parameter determine whether your bind mount host volume persists on the
        host container instance and where it is stored. If the host parameter is empty, then the Docker
        daemon assigns a host path for your data volume. However, the data is not guaranteed to persist
        after the containers associated with it stop running.

        stability
        :stability: experimental
        """
        return self._values.get('host')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'Volume(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_ecs.VolumeFrom", jsii_struct_bases=[], name_mapping={'read_only': 'readOnly', 'source_container': 'sourceContainer'})
class VolumeFrom():
    def __init__(self, *, read_only: bool, source_container: str) -> None:
        """The details on a data volume from another container in the same task definition.

        :param read_only: Specifies whether the container has read-only access to the volume. If this value is true, the container has read-only access to the volume. If this value is false, then the container can write to the volume.
        :param source_container: The name of another container within the same task definition from which to mount volumes.

        stability
        :stability: experimental
        """
        self._values = {
            'read_only': read_only,
            'source_container': source_container,
        }

    @builtins.property
    def read_only(self) -> bool:
        """Specifies whether the container has read-only access to the volume.

        If this value is true, the container has read-only access to the volume.
        If this value is false, then the container can write to the volume.

        stability
        :stability: experimental
        """
        return self._values.get('read_only')

    @builtins.property
    def source_container(self) -> str:
        """The name of another container within the same task definition from which to mount volumes.

        stability
        :stability: experimental
        """
        return self._values.get('source_container')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'VolumeFrom(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.aws_ecs.WindowsOptimizedVersion")
class WindowsOptimizedVersion(enum.Enum):
    """ECS-optimized Windows version list.

    stability
    :stability: experimental
    """
    SERVER_2019 = "SERVER_2019"
    """
    stability
    :stability: experimental
    """
    SERVER_2016 = "SERVER_2016"
    """
    stability
    :stability: experimental
    """

class AppMeshProxyConfiguration(ProxyConfiguration, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs.AppMeshProxyConfiguration"):
    """The class for App Mesh proxy configurations.

    For tasks using the EC2 launch type, the container instances require at least version 1.26.0 of the container agent and at least version
    1.26.0-1 of the ecs-init package to enable a proxy configuration. If your container instances are launched from the Amazon ECS-optimized
    AMI version 20190301 or later, then they contain the required versions of the container agent and ecs-init.
    For more information, see `Amazon ECS-optimized AMIs <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html>`_.

    For tasks using the Fargate launch type, the task or service requires platform version 1.3.0 or later.

    stability
    :stability: experimental
    """
    def __init__(self, *, container_name: str, properties: "AppMeshProxyConfigurationProps") -> None:
        """Constructs a new instance of the AppMeshProxyConfiguration class.

        :param container_name: The name of the container that will serve as the App Mesh proxy.
        :param properties: The set of network configuration parameters to provide the Container Network Interface (CNI) plugin.

        stability
        :stability: experimental
        """
        props = AppMeshProxyConfigurationConfigProps(container_name=container_name, properties=properties)

        jsii.create(AppMeshProxyConfiguration, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _Construct_f50a3f53, _task_definition: "TaskDefinition") -> "CfnTaskDefinition.ProxyConfigurationProperty":
        """Called when the proxy configuration is configured on a task definition.

        :param _scope: -
        :param _task_definition: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_scope, _task_definition])


class AssetImage(ContainerImage, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs.AssetImage"):
    """An image that will be built from a local directory with a Dockerfile.

    stability
    :stability: experimental
    """
    def __init__(self, directory: str, *, build_args: typing.Optional[typing.Mapping[str, str]]=None, file: typing.Optional[str]=None, repository_name: typing.Optional[str]=None, target: typing.Optional[str]=None, extra_hash: typing.Optional[str]=None, exclude: typing.Optional[typing.List[str]]=None, follow: typing.Optional[_FollowMode_f74e7125]=None) -> None:
        """Constructs a new instance of the AssetImage class.

        :param directory: The directory containing the Dockerfile.
        :param build_args: Build args to pass to the ``docker build`` command. Since Docker build arguments are resolved before deployment, keys and values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or ``queue.queueUrl``). Default: - no build args are passed
        :param file: Path to the Dockerfile (relative to the directory). Default: 'Dockerfile'
        :param repository_name: ECR repository name. Specify this property if you need to statically address the image, e.g. from a Kubernetes Pod. Note, this is only the repository name, without the registry and the tag parts. Default: - the default ECR repository for CDK assets
        :param target: Docker target to build to. Default: - no target
        :param extra_hash: Extra information to encode into the fingerprint (e.g. build instructions and other inputs). Default: - hash is only based on source content
        :param exclude: Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: Never

        stability
        :stability: experimental
        """
        props = AssetImageProps(build_args=build_args, file=file, repository_name=repository_name, target=target, extra_hash=extra_hash, exclude=exclude, follow=follow)

        jsii.create(AssetImage, self, [directory, props])

    @jsii.member(jsii_name="bind")
    def bind(self, scope: _Construct_f50a3f53, container_definition: "ContainerDefinition") -> "ContainerImageConfig":
        """Called when the image is used by a ContainerDefinition.

        :param scope: -
        :param container_definition: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [scope, container_definition])


class AwsLogDriver(LogDriver, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs.AwsLogDriver"):
    """A log driver that sends log information to CloudWatch Logs.

    stability
    :stability: experimental
    """
    def __init__(self, *, stream_prefix: str, datetime_format: typing.Optional[str]=None, log_group: typing.Optional[_ILogGroup_6b54c8e1]=None, log_retention: typing.Optional[_RetentionDays_bdc7ad1f]=None, multiline_pattern: typing.Optional[str]=None) -> None:
        """Constructs a new instance of the AwsLogDriver class.

        :param stream_prefix: Prefix for the log streams. The awslogs-stream-prefix option allows you to associate a log stream with the specified prefix, the container name, and the ID of the Amazon ECS task to which the container belongs. If you specify a prefix with this option, then the log stream takes the following format:: prefix-name/container-name/ecs-task-id
        :param datetime_format: This option defines a multiline start pattern in Python strftime format. A log message consists of a line that matches the pattern and any following lines that don’t match the pattern. Thus the matched line is the delimiter between log messages. Default: - No multiline matching.
        :param log_group: The log group to log to. Default: - A log group is automatically created.
        :param log_retention: The number of days log events are kept in CloudWatch Logs when the log group is automatically created by this construct. Default: - Logs never expire.
        :param multiline_pattern: This option defines a multiline start pattern using a regular expression. A log message consists of a line that matches the pattern and any following lines that don’t match the pattern. Thus the matched line is the delimiter between log messages. This option is ignored if datetimeFormat is also configured. Default: - No multiline matching.

        stability
        :stability: experimental
        """
        props = AwsLogDriverProps(stream_prefix=stream_prefix, datetime_format=datetime_format, log_group=log_group, log_retention=log_retention, multiline_pattern=multiline_pattern)

        jsii.create(AwsLogDriver, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, scope: _Construct_f50a3f53, container_definition: "ContainerDefinition") -> "LogDriverConfig":
        """Called when the log driver is configured on a container.

        :param scope: -
        :param container_definition: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [scope, container_definition])

    @builtins.property
    @jsii.member(jsii_name="logGroup")
    def log_group(self) -> typing.Optional[_ILogGroup_6b54c8e1]:
        """The log group to send log streams to.

        Only available after the LogDriver has been bound to a ContainerDefinition.

        stability
        :stability: experimental
        """
        return jsii.get(self, "logGroup")

    @log_group.setter
    def log_group(self, value: typing.Optional[_ILogGroup_6b54c8e1]) -> None:
        jsii.set(self, "logGroup", value)


@jsii.implements(ICluster)
class Cluster(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs.Cluster"):
    """A regional grouping of one or more container instances on which you can run tasks and services.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, capacity: typing.Optional["AddCapacityOptions"]=None, cluster_name: typing.Optional[str]=None, container_insights: typing.Optional[bool]=None, default_cloud_map_namespace: typing.Optional["CloudMapNamespaceOptions"]=None, vpc: typing.Optional[_IVpc_3795853f]=None) -> None:
        """Constructs a new instance of the Cluster class.

        :param scope: -
        :param id: -
        :param capacity: The ec2 capacity to add to the cluster. Default: - no EC2 capacity will be added, you can use ``addCapacity`` to add capacity later.
        :param cluster_name: The name for the cluster. Default: CloudFormation-generated name
        :param container_insights: If true CloudWatch Container Insights will be enabled for the cluster. Default: - Container Insights will be disabled for this cluser.
        :param default_cloud_map_namespace: The service discovery namespace created in this cluster. Default: - no service discovery namespace created, you can use ``addDefaultCloudMapNamespace`` to add a default service discovery namespace later.
        :param vpc: The VPC where your ECS instances will be running or your ENIs will be deployed. Default: - creates a new VPC with two AZs

        stability
        :stability: experimental
        """
        props = ClusterProps(capacity=capacity, cluster_name=cluster_name, container_insights=container_insights, default_cloud_map_namespace=default_cloud_map_namespace, vpc=vpc)

        jsii.create(Cluster, self, [scope, id, props])

    @jsii.member(jsii_name="fromClusterAttributes")
    @builtins.classmethod
    def from_cluster_attributes(cls, scope: _Construct_f50a3f53, id: str, *, cluster_name: str, security_groups: typing.List[_ISecurityGroup_d72ab8e8], vpc: _IVpc_3795853f, autoscaling_group: typing.Optional[_IAutoScalingGroup_a753dc94]=None, cluster_arn: typing.Optional[str]=None, default_cloud_map_namespace: typing.Optional[_INamespace_2b56a022]=None, has_ec2_capacity: typing.Optional[bool]=None) -> "ICluster":
        """Import an existing cluster to the stack from its attributes.

        :param scope: -
        :param id: -
        :param cluster_name: The name of the cluster.
        :param security_groups: The security groups associated with the container instances registered to the cluster.
        :param vpc: The VPC associated with the cluster.
        :param autoscaling_group: Autoscaling group added to the cluster if capacity is added. Default: - No default autoscaling group
        :param cluster_arn: The Amazon Resource Name (ARN) that identifies the cluster. Default: Derived from clusterName
        :param default_cloud_map_namespace: The AWS Cloud Map namespace to associate with the cluster. Default: - No default namespace
        :param has_ec2_capacity: Specifies whether the cluster has EC2 instance capacity. Default: true

        stability
        :stability: experimental
        """
        attrs = ClusterAttributes(cluster_name=cluster_name, security_groups=security_groups, vpc=vpc, autoscaling_group=autoscaling_group, cluster_arn=cluster_arn, default_cloud_map_namespace=default_cloud_map_namespace, has_ec2_capacity=has_ec2_capacity)

        return jsii.sinvoke(cls, "fromClusterAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="addAutoScalingGroup")
    def add_auto_scaling_group(self, auto_scaling_group: _AutoScalingGroup_003d0b84, *, can_containers_access_instance_role: typing.Optional[bool]=None, spot_instance_draining: typing.Optional[bool]=None, task_drain_time: typing.Optional[_Duration_5170c158]=None) -> None:
        """This method adds compute capacity to a cluster using the specified AutoScalingGroup.

        :param auto_scaling_group: the ASG to add to this cluster. [disable-awslint:ref-via-interface] is needed in order to install the ECS agent by updating the ASGs user data.
        :param can_containers_access_instance_role: Specifies whether the containers can access the container instance role. Default: false
        :param spot_instance_draining: Specify whether to enable Automated Draining for Spot Instances running Amazon ECS Services. For more information, see `Using Spot Instances <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/container-instance-spot.html>`_. Default: false
        :param task_drain_time: The time period to wait before force terminating an instance that is draining. This creates a Lambda function that is used by a lifecycle hook for the AutoScalingGroup that will delay instance termination until all ECS tasks have drained from the instance. Set to 0 to disable task draining. Set to 0 to disable task draining. Default: Duration.minutes(5)

        stability
        :stability: experimental
        """
        options = AddAutoScalingGroupCapacityOptions(can_containers_access_instance_role=can_containers_access_instance_role, spot_instance_draining=spot_instance_draining, task_drain_time=task_drain_time)

        return jsii.invoke(self, "addAutoScalingGroup", [auto_scaling_group, options])

    @jsii.member(jsii_name="addCapacity")
    def add_capacity(self, id: str, *, instance_type: _InstanceType_85a97b30, machine_image: typing.Optional[_IMachineImage_d5cd7b45]=None, can_containers_access_instance_role: typing.Optional[bool]=None, spot_instance_draining: typing.Optional[bool]=None, task_drain_time: typing.Optional[_Duration_5170c158]=None, allow_all_outbound: typing.Optional[bool]=None, associate_public_ip_address: typing.Optional[bool]=None, block_devices: typing.Optional[typing.List[_BlockDevice_6b64cf0c]]=None, cooldown: typing.Optional[_Duration_5170c158]=None, desired_capacity: typing.Optional[jsii.Number]=None, health_check: typing.Optional[_HealthCheck_ed599e14]=None, ignore_unmodified_size_properties: typing.Optional[bool]=None, instance_monitoring: typing.Optional[_Monitoring_11cb7f01]=None, key_name: typing.Optional[str]=None, max_capacity: typing.Optional[jsii.Number]=None, max_instance_lifetime: typing.Optional[_Duration_5170c158]=None, min_capacity: typing.Optional[jsii.Number]=None, notifications: typing.Optional[typing.List[_NotificationConfiguration_396b88c6]]=None, notifications_topic: typing.Optional[_ITopic_ef0ebe0e]=None, replacing_update_min_successful_instances_percent: typing.Optional[jsii.Number]=None, resource_signal_count: typing.Optional[jsii.Number]=None, resource_signal_timeout: typing.Optional[_Duration_5170c158]=None, rolling_update_configuration: typing.Optional[_RollingUpdateConfiguration_c96dd49e]=None, spot_price: typing.Optional[str]=None, update_type: typing.Optional[_UpdateType_7a2ac17e]=None, vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6]=None) -> _AutoScalingGroup_003d0b84:
        """This method adds compute capacity to a cluster by creating an AutoScalingGroup with the specified options.

        Returns the AutoScalingGroup so you can add autoscaling settings to it.

        :param id: -
        :param instance_type: The EC2 instance type to use when launching instances into the AutoScalingGroup.
        :param machine_image: The ECS-optimized AMI variant to use. For more information, see `Amazon ECS-optimized AMIs <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html>`_. Default: - Amazon Linux 2
        :param can_containers_access_instance_role: Specifies whether the containers can access the container instance role. Default: false
        :param spot_instance_draining: Specify whether to enable Automated Draining for Spot Instances running Amazon ECS Services. For more information, see `Using Spot Instances <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/container-instance-spot.html>`_. Default: false
        :param task_drain_time: The time period to wait before force terminating an instance that is draining. This creates a Lambda function that is used by a lifecycle hook for the AutoScalingGroup that will delay instance termination until all ECS tasks have drained from the instance. Set to 0 to disable task draining. Set to 0 to disable task draining. Default: Duration.minutes(5)
        :param allow_all_outbound: Whether the instances can initiate connections to anywhere by default. Default: true
        :param associate_public_ip_address: Whether instances in the Auto Scaling Group should have public IP addresses associated with them. Default: - Use subnet setting.
        :param block_devices: Specifies how block devices are exposed to the instance. You can specify virtual devices and EBS volumes. Each instance that is launched has an associated root device volume, either an Amazon EBS volume or an instance store volume. You can use block device mappings to specify additional EBS volumes or instance store volumes to attach to an instance when it is launched. Default: - Uses the block device mapping of the AMI
        :param cooldown: Default scaling cooldown for this AutoScalingGroup. Default: Duration.minutes(5)
        :param desired_capacity: Initial amount of instances in the fleet. If this is set to a number, every deployment will reset the amount of instances to this number. It is recommended to leave this value blank. Default: minCapacity, and leave unchanged during deployment
        :param health_check: Configuration for health checks. Default: - HealthCheck.ec2 with no grace period
        :param ignore_unmodified_size_properties: If the ASG has scheduled actions, don't reset unchanged group sizes. Only used if the ASG has scheduled actions (which may scale your ASG up or down regardless of cdk deployments). If true, the size of the group will only be reset if it has been changed in the CDK app. If false, the sizes will always be changed back to what they were in the CDK app on deployment. Default: true
        :param instance_monitoring: Controls whether instances in this group are launched with detailed or basic monitoring. When detailed monitoring is enabled, Amazon CloudWatch generates metrics every minute and your account is charged a fee. When you disable detailed monitoring, CloudWatch generates metrics every 5 minutes. Default: - Monitoring.DETAILED
        :param key_name: Name of SSH keypair to grant access to instances. Default: - No SSH access will be possible.
        :param max_capacity: Maximum number of instances in the fleet. Default: desiredCapacity
        :param max_instance_lifetime: The maximum amount of time that an instance can be in service. The maximum duration applies to all current and future instances in the group. As an instance approaches its maximum duration, it is terminated and replaced, and cannot be used again. You must specify a value of at least 604,800 seconds (7 days). To clear a previously set value, simply leave this property undefinied. Default: none
        :param min_capacity: Minimum number of instances in the fleet. Default: 1
        :param notifications: Configure autoscaling group to send notifications about fleet changes to an SNS topic(s). Default: - No fleet change notifications will be sent.
        :param notifications_topic: SNS topic to send notifications about fleet changes. Default: - No fleet change notifications will be sent.
        :param replacing_update_min_successful_instances_percent: Configuration for replacing updates. Only used if updateType == UpdateType.ReplacingUpdate. Specifies how many instances must signal success for the update to succeed. Default: minSuccessfulInstancesPercent
        :param resource_signal_count: How many ResourceSignal calls CloudFormation expects before the resource is considered created. Default: 1
        :param resource_signal_timeout: The length of time to wait for the resourceSignalCount. The maximum value is 43200 (12 hours). Default: Duration.minutes(5)
        :param rolling_update_configuration: Configuration for rolling updates. Only used if updateType == UpdateType.RollingUpdate. Default: - RollingUpdateConfiguration with defaults.
        :param spot_price: The maximum hourly price (in USD) to be paid for any Spot Instance launched to fulfill the request. Spot Instances are launched when the price you specify exceeds the current Spot market price. Default: none
        :param update_type: What to do when an AutoScalingGroup's instance configuration is changed. This is applied when any of the settings on the ASG are changed that affect how the instances should be created (VPC, instance type, startup scripts, etc.). It indicates how the existing instances should be replaced with new instances matching the new config. By default, nothing is done and only new instances are launched with the new config. Default: UpdateType.None
        :param vpc_subnets: Where to place instances within the VPC. Default: - All Private subnets.

        stability
        :stability: experimental
        """
        options = AddCapacityOptions(instance_type=instance_type, machine_image=machine_image, can_containers_access_instance_role=can_containers_access_instance_role, spot_instance_draining=spot_instance_draining, task_drain_time=task_drain_time, allow_all_outbound=allow_all_outbound, associate_public_ip_address=associate_public_ip_address, block_devices=block_devices, cooldown=cooldown, desired_capacity=desired_capacity, health_check=health_check, ignore_unmodified_size_properties=ignore_unmodified_size_properties, instance_monitoring=instance_monitoring, key_name=key_name, max_capacity=max_capacity, max_instance_lifetime=max_instance_lifetime, min_capacity=min_capacity, notifications=notifications, notifications_topic=notifications_topic, replacing_update_min_successful_instances_percent=replacing_update_min_successful_instances_percent, resource_signal_count=resource_signal_count, resource_signal_timeout=resource_signal_timeout, rolling_update_configuration=rolling_update_configuration, spot_price=spot_price, update_type=update_type, vpc_subnets=vpc_subnets)

        return jsii.invoke(self, "addCapacity", [id, options])

    @jsii.member(jsii_name="addDefaultCloudMapNamespace")
    def add_default_cloud_map_namespace(self, *, name: str, type: typing.Optional[_NamespaceType_df1ca402]=None, vpc: typing.Optional[_IVpc_3795853f]=None) -> _INamespace_2b56a022:
        """Add an AWS Cloud Map DNS namespace for this cluster.

        NOTE: HttpNamespaces are not supported, as ECS always requires a DNSConfig when registering an instance to a Cloud
        Map service.

        :param name: The name of the namespace, such as example.com.
        :param type: The type of CloudMap Namespace to create. Default: PrivateDns
        :param vpc: The VPC to associate the namespace with. This property is required for private DNS namespaces. Default: VPC of the cluster for Private DNS Namespace, otherwise none

        stability
        :stability: experimental
        """
        options = CloudMapNamespaceOptions(name=name, type=type, vpc=vpc)

        return jsii.invoke(self, "addDefaultCloudMapNamespace", [options])

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[_Duration_5170c158]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[_Unit_e1b74f3c]=None) -> _Metric_53e89548:
        """This method returns the specifed CloudWatch metric for this cluster.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricCpuReservation")
    def metric_cpu_reservation(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[_Duration_5170c158]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[_Unit_e1b74f3c]=None) -> _Metric_53e89548:
        """This method returns the CloudWatch metric for this clusters CPU reservation.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: average over 5 minutes

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricCpuReservation", [props])

    @jsii.member(jsii_name="metricMemoryReservation")
    def metric_memory_reservation(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[_Duration_5170c158]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[_Unit_e1b74f3c]=None) -> _Metric_53e89548:
        """This method returns the CloudWatch metric for this clusters memory reservation.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: average over 5 minutes

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricMemoryReservation", [props])

    @builtins.property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> str:
        """The Amazon Resource Name (ARN) that identifies the cluster.

        stability
        :stability: experimental
        """
        return jsii.get(self, "clusterArn")

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        """The name of the cluster.

        stability
        :stability: experimental
        """
        return jsii.get(self, "clusterName")

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _Connections_231f38b5:
        """Manage the allowed network connections for the cluster with Security Groups.

        stability
        :stability: experimental
        """
        return jsii.get(self, "connections")

    @builtins.property
    @jsii.member(jsii_name="hasEc2Capacity")
    def has_ec2_capacity(self) -> bool:
        """Whether the cluster has EC2 capacity associated with it.

        stability
        :stability: experimental
        """
        return jsii.get(self, "hasEc2Capacity")

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _IVpc_3795853f:
        """The VPC associated with the cluster.

        stability
        :stability: experimental
        """
        return jsii.get(self, "vpc")

    @builtins.property
    @jsii.member(jsii_name="autoscalingGroup")
    def autoscaling_group(self) -> typing.Optional[_IAutoScalingGroup_a753dc94]:
        """Getter for autoscaling group added to cluster.

        stability
        :stability: experimental
        """
        return jsii.get(self, "autoscalingGroup")

    @builtins.property
    @jsii.member(jsii_name="defaultCloudMapNamespace")
    def default_cloud_map_namespace(self) -> typing.Optional[_INamespace_2b56a022]:
        """Getter for namespace added to cluster.

        stability
        :stability: experimental
        """
        return jsii.get(self, "defaultCloudMapNamespace")


class FireLensLogDriver(LogDriver, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs.FireLensLogDriver"):
    """FireLens enables you to use task definition parameters to route logs to an AWS service   or AWS Partner Network (APN) destination for log storage and analytics.

    stability
    :stability: experimental
    """
    def __init__(self, *, options: typing.Optional[typing.Mapping[str, str]]=None, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None) -> None:
        """Constructs a new instance of the FireLensLogDriver class.

        :param options: The configuration options to send to the log driver. Default: - the log driver options
        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID

        stability
        :stability: experimental
        """
        props = FireLensLogDriverProps(options=options, env=env, env_regex=env_regex, labels=labels, tag=tag)

        jsii.create(FireLensLogDriver, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _Construct_f50a3f53, _container_definition: "ContainerDefinition") -> "LogDriverConfig":
        """Called when the log driver is configured on a container.

        :param _scope: -
        :param _container_definition: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_scope, _container_definition])


class FluentdLogDriver(LogDriver, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs.FluentdLogDriver"):
    """A log driver that sends log information to journald Logs.

    stability
    :stability: experimental
    """
    def __init__(self, *, address: typing.Optional[str]=None, async_connect: typing.Optional[bool]=None, buffer_limit: typing.Optional[jsii.Number]=None, max_retries: typing.Optional[jsii.Number]=None, retry_wait: typing.Optional[_Duration_5170c158]=None, sub_second_precision: typing.Optional[bool]=None, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None) -> None:
        """Constructs a new instance of the FluentdLogDriver class.

        :param address: By default, the logging driver connects to localhost:24224. Supply the address option to connect to a different address. tcp(default) and unix sockets are supported. Default: - address not set.
        :param async_connect: Docker connects to Fluentd in the background. Messages are buffered until the connection is established. Default: - false
        :param buffer_limit: The amount of data to buffer before flushing to disk. Default: - The amount of RAM available to the container.
        :param max_retries: The maximum number of retries. Default: - 4294967295 (2**32 - 1).
        :param retry_wait: How long to wait between retries. Default: - 1 second
        :param sub_second_precision: Generates event logs in nanosecond resolution. Default: - false
        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID

        stability
        :stability: experimental
        """
        props = FluentdLogDriverProps(address=address, async_connect=async_connect, buffer_limit=buffer_limit, max_retries=max_retries, retry_wait=retry_wait, sub_second_precision=sub_second_precision, env=env, env_regex=env_regex, labels=labels, tag=tag)

        jsii.create(FluentdLogDriver, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _Construct_f50a3f53, _container_definition: "ContainerDefinition") -> "LogDriverConfig":
        """Called when the log driver is configured on a container.

        :param _scope: -
        :param _container_definition: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_scope, _container_definition])


class GelfLogDriver(LogDriver, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs.GelfLogDriver"):
    """A log driver that sends log information to journald Logs.

    stability
    :stability: experimental
    """
    def __init__(self, *, address: str, compression_level: typing.Optional[jsii.Number]=None, compression_type: typing.Optional["GelfCompressionType"]=None, tcp_max_reconnect: typing.Optional[jsii.Number]=None, tcp_reconnect_delay: typing.Optional[_Duration_5170c158]=None, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None) -> None:
        """Constructs a new instance of the GelfLogDriver class.

        :param address: The address of the GELF server. tcp and udp are the only supported URI specifier and you must specify the port.
        :param compression_level: UDP Only The level of compression when gzip or zlib is the gelf-compression-type. An integer in the range of -1 to 9 (BestCompression). Higher levels provide more compression at lower speed. Either -1 or 0 disables compression. Default: - 1
        :param compression_type: UDP Only The type of compression the GELF driver uses to compress each log message. Allowed values are gzip, zlib and none. Default: - gzip
        :param tcp_max_reconnect: TCP Only The maximum number of reconnection attempts when the connection drop. A positive integer. Default: - 3
        :param tcp_reconnect_delay: TCP Only The number of seconds to wait between reconnection attempts. A positive integer. Default: - 1
        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID

        stability
        :stability: experimental
        """
        props = GelfLogDriverProps(address=address, compression_level=compression_level, compression_type=compression_type, tcp_max_reconnect=tcp_max_reconnect, tcp_reconnect_delay=tcp_reconnect_delay, env=env, env_regex=env_regex, labels=labels, tag=tag)

        jsii.create(GelfLogDriver, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _Construct_f50a3f53, _container_definition: "ContainerDefinition") -> "LogDriverConfig":
        """Called when the log driver is configured on a container.

        :param _scope: -
        :param _container_definition: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_scope, _container_definition])


@jsii.interface(jsii_type="monocdk-experiment.aws_ecs.IBaseService")
class IBaseService(IService, jsii.compat.Protocol):
    """The interface for BaseService.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IBaseServiceProxy

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> "ICluster":
        """The cluster that hosts the service.

        stability
        :stability: experimental
        """
        ...


class _IBaseServiceProxy(jsii.proxy_for(IService)):
    """The interface for BaseService.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_ecs.IBaseService"
    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> "ICluster":
        """The cluster that hosts the service.

        stability
        :stability: experimental
        """
        return jsii.get(self, "cluster")


@jsii.interface(jsii_type="monocdk-experiment.aws_ecs.IEc2Service")
class IEc2Service(IService, jsii.compat.Protocol):
    """The interface for a service using the EC2 launch type on an ECS cluster.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IEc2ServiceProxy

    pass

class _IEc2ServiceProxy(jsii.proxy_for(IService)):
    """The interface for a service using the EC2 launch type on an ECS cluster.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_ecs.IEc2Service"
    pass

@jsii.interface(jsii_type="monocdk-experiment.aws_ecs.IEc2TaskDefinition")
class IEc2TaskDefinition(ITaskDefinition, jsii.compat.Protocol):
    """The interface of a task definition run on an EC2 cluster.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IEc2TaskDefinitionProxy

    pass

class _IEc2TaskDefinitionProxy(jsii.proxy_for(ITaskDefinition)):
    """The interface of a task definition run on an EC2 cluster.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_ecs.IEc2TaskDefinition"
    pass

@jsii.interface(jsii_type="monocdk-experiment.aws_ecs.IFargateService")
class IFargateService(IService, jsii.compat.Protocol):
    """The interface for a service using the Fargate launch type on an ECS cluster.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IFargateServiceProxy

    pass

class _IFargateServiceProxy(jsii.proxy_for(IService)):
    """The interface for a service using the Fargate launch type on an ECS cluster.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_ecs.IFargateService"
    pass

@jsii.interface(jsii_type="monocdk-experiment.aws_ecs.IFargateTaskDefinition")
class IFargateTaskDefinition(ITaskDefinition, jsii.compat.Protocol):
    """The interface of a task definition run on a Fargate cluster.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IFargateTaskDefinitionProxy

    pass

class _IFargateTaskDefinitionProxy(jsii.proxy_for(ITaskDefinition)):
    """The interface of a task definition run on a Fargate cluster.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_ecs.IFargateTaskDefinition"
    pass

class JournaldLogDriver(LogDriver, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs.JournaldLogDriver"):
    """A log driver that sends log information to journald Logs.

    stability
    :stability: experimental
    """
    def __init__(self, *, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None) -> None:
        """Constructs a new instance of the JournaldLogDriver class.

        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID

        stability
        :stability: experimental
        """
        props = JournaldLogDriverProps(env=env, env_regex=env_regex, labels=labels, tag=tag)

        jsii.create(JournaldLogDriver, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _Construct_f50a3f53, _container_definition: "ContainerDefinition") -> "LogDriverConfig":
        """Called when the log driver is configured on a container.

        :param _scope: -
        :param _container_definition: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_scope, _container_definition])


class JsonFileLogDriver(LogDriver, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs.JsonFileLogDriver"):
    """A log driver that sends log information to json-file Logs.

    stability
    :stability: experimental
    """
    def __init__(self, *, compress: typing.Optional[bool]=None, max_file: typing.Optional[jsii.Number]=None, max_size: typing.Optional[str]=None, env: typing.Optional[typing.List[str]]=None, env_regex: typing.Optional[str]=None, labels: typing.Optional[typing.List[str]]=None, tag: typing.Optional[str]=None) -> None:
        """Constructs a new instance of the JsonFileLogDriver class.

        :param compress: Toggles compression for rotated logs. Default: - false
        :param max_file: The maximum number of log files that can be present. If rolling the logs creates excess files, the oldest file is removed. Only effective when max-size is also set. A positive integer. Default: - 1
        :param max_size: The maximum size of the log before it is rolled. A positive integer plus a modifier representing the unit of measure (k, m, or g). Default: - -1 (unlimited)
        :param env: The env option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No env
        :param env_regex: The env-regex option is similar to and compatible with env. Its value is a regular expression to match logging-related environment variables. It is used for advanced log tag options. Default: - No envRegex
        :param labels: The labels option takes an array of keys. If there is collision between label and env keys, the value of the env takes precedence. Adds additional fields to the extra attributes of a logging message. Default: - No labels
        :param tag: By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the log tag option documentation for customizing the log tag format. Default: - The first 12 characters of the container ID

        stability
        :stability: experimental
        """
        props = JsonFileLogDriverProps(compress=compress, max_file=max_file, max_size=max_size, env=env, env_regex=env_regex, labels=labels, tag=tag)

        jsii.create(JsonFileLogDriver, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _Construct_f50a3f53, _container_definition: "ContainerDefinition") -> "LogDriverConfig":
        """Called when the log driver is configured on a container.

        :param _scope: -
        :param _container_definition: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_scope, _container_definition])


@jsii.implements(IBaseService, _IApplicationLoadBalancerTarget_079c540c, _INetworkLoadBalancerTarget_c44e1c1e, _ILoadBalancerTarget_87ce58b8)
class BaseService(_Resource_884d0774, metaclass=jsii.JSIIAbstractClass, jsii_type="monocdk-experiment.aws_ecs.BaseService"):
    """The base class for Ec2Service and FargateService services.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _BaseServiceProxy

    def __init__(self, scope: _Construct_f50a3f53, id: str, props: "BaseServiceProps", additional_props: typing.Any, task_definition: "TaskDefinition") -> None:
        """Constructs a new instance of the BaseService class.

        :param scope: -
        :param id: -
        :param props: -
        :param additional_props: -
        :param task_definition: -

        stability
        :stability: experimental
        """
        jsii.create(BaseService, self, [scope, id, props, additional_props, task_definition])

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(self, target_group: _IApplicationTargetGroup_1bf77cc5) -> _LoadBalancerTargetProps_80dbd4a5:
        """This method is called to attach this service to an Application Load Balancer.

        Don't call this function directly. Instead, call ``listener.addTargets()``
        to add this service to a load balancer.

        :param target_group: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "attachToApplicationTargetGroup", [target_group])

    @jsii.member(jsii_name="attachToClassicLB")
    def attach_to_classic_lb(self, load_balancer: _LoadBalancer_6d00b4b8) -> None:
        """Registers the service as a target of a Classic Load Balancer (CLB).

        Don't call this. Call ``loadBalancer.addTarget()`` instead.

        :param load_balancer: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "attachToClassicLB", [load_balancer])

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(self, target_group: _INetworkTargetGroup_1183b98f) -> _LoadBalancerTargetProps_80dbd4a5:
        """This method is called to attach this service to a Network Load Balancer.

        Don't call this function directly. Instead, call ``listener.addTargets()``
        to add this service to a load balancer.

        :param target_group: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "attachToNetworkTargetGroup", [target_group])

    @jsii.member(jsii_name="autoScaleTaskCount")
    def auto_scale_task_count(self, *, max_capacity: jsii.Number, min_capacity: typing.Optional[jsii.Number]=None) -> "ScalableTaskCount":
        """An attribute representing the minimum and maximum task count for an AutoScalingGroup.

        :param max_capacity: Maximum capacity to scale to.
        :param min_capacity: Minimum capacity to scale to. Default: 1

        stability
        :stability: experimental
        """
        props = _EnableScalingProps_5e50c056(max_capacity=max_capacity, min_capacity=min_capacity)

        return jsii.invoke(self, "autoScaleTaskCount", [props])

    @jsii.member(jsii_name="configureAwsVpcNetworking")
    def _configure_aws_vpc_networking(self, vpc: _IVpc_3795853f, assign_public_ip: typing.Optional[bool]=None, vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6]=None, security_group: typing.Optional[_ISecurityGroup_d72ab8e8]=None) -> None:
        """This method is called to create a networkConfiguration.

        :param vpc: -
        :param assign_public_ip: -
        :param vpc_subnets: -
        :param security_group: -

        deprecated
        :deprecated: use configureAwsVpcNetworkingWithSecurityGroups instead.

        stability
        :stability: deprecated
        """
        return jsii.invoke(self, "configureAwsVpcNetworking", [vpc, assign_public_ip, vpc_subnets, security_group])

    @jsii.member(jsii_name="configureAwsVpcNetworkingWithSecurityGroups")
    def _configure_aws_vpc_networking_with_security_groups(self, vpc: _IVpc_3795853f, assign_public_ip: typing.Optional[bool]=None, vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6]=None, security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]]=None) -> None:
        """This method is called to create a networkConfiguration.

        :param vpc: -
        :param assign_public_ip: -
        :param vpc_subnets: -
        :param security_groups: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "configureAwsVpcNetworkingWithSecurityGroups", [vpc, assign_public_ip, vpc_subnets, security_groups])

    @jsii.member(jsii_name="enableCloudMap")
    def enable_cloud_map(self, *, cloud_map_namespace: typing.Optional[_INamespace_2b56a022]=None, dns_record_type: typing.Optional[_DnsRecordType_acb5afbb]=None, dns_ttl: typing.Optional[_Duration_5170c158]=None, failure_threshold: typing.Optional[jsii.Number]=None, name: typing.Optional[str]=None) -> _Service_4702d1e5:
        """Enable CloudMap service discovery for the service.

        :param cloud_map_namespace: The service discovery namespace for the Cloud Map service to attach to the ECS service. Default: - the defaultCloudMapNamespace associated to the cluster
        :param dns_record_type: The DNS record type that you want AWS Cloud Map to create. The supported record types are A or SRV. Default: DnsRecordType.A
        :param dns_ttl: The amount of time that you want DNS resolvers to cache the settings for this record. Default: 60
        :param failure_threshold: The number of 30-second intervals that you want Cloud Map to wait after receiving an UpdateInstanceCustomHealthStatus request before it changes the health status of a service instance. NOTE: This is used for HealthCheckCustomConfig
        :param name: The name of the Cloud Map service to attach to the ECS service. Default: CloudFormation-generated name

        return
        :return: The created CloudMap service

        stability
        :stability: experimental
        """
        options = CloudMapOptions(cloud_map_namespace=cloud_map_namespace, dns_record_type=dns_record_type, dns_ttl=dns_ttl, failure_threshold=failure_threshold, name=name)

        return jsii.invoke(self, "enableCloudMap", [options])

    @jsii.member(jsii_name="loadBalancerTarget")
    def load_balancer_target(self, *, container_name: str, container_port: typing.Optional[jsii.Number]=None, protocol: typing.Optional["Protocol"]=None) -> "IEcsLoadBalancerTarget":
        """Return a load balancing target for a specific container and port.

        Use this function to create a load balancer target if you want to load balance to
        another container than the first essential container or the first mapped port on
        the container.

        Use the return value of this function where you would normally use a load balancer
        target, instead of the ``Service`` object itself.

        :param container_name: The name of the container.
        :param container_port: The port number of the container. Only applicable when using application/network load balancers. Default: - Container port of the first added port mapping.
        :param protocol: The protocol used for the port mapping. Only applicable when using application load balancers. Default: Protocol.TCP

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            listener.add_targets("ECS",
                port=80,
                targets=[service.load_balancer_target(
                    container_name="MyContainer",
                    container_port=1234
                )]
            )
        """
        options = LoadBalancerTargetOptions(container_name=container_name, container_port=container_port, protocol=protocol)

        return jsii.invoke(self, "loadBalancerTarget", [options])

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[_Duration_5170c158]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[_Unit_e1b74f3c]=None) -> _Metric_53e89548:
        """This method returns the specified CloudWatch metric name for this service.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricCpuUtilization")
    def metric_cpu_utilization(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[_Duration_5170c158]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[_Unit_e1b74f3c]=None) -> _Metric_53e89548:
        """This method returns the CloudWatch metric for this clusters CPU utilization.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: average over 5 minutes

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricCpuUtilization", [props])

    @jsii.member(jsii_name="metricMemoryUtilization")
    def metric_memory_utilization(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[_Duration_5170c158]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[_Unit_e1b74f3c]=None) -> _Metric_53e89548:
        """This method returns the CloudWatch metric for this clusters memory utilization.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: average over 5 minutes

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricMemoryUtilization", [props])

    @jsii.member(jsii_name="registerLoadBalancerTargets")
    def register_load_balancer_targets(self, *targets: "EcsTarget") -> None:
        """Use this function to create all load balancer targets to be registered in this service, add them to target groups, and attach target groups to listeners accordingly.

        Alternatively, you can use ``listener.addTargets()`` to create targets and add them to target groups.

        :param targets: -

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            service.register_load_balancer_targets(
                container_name="web",
                container_port=80,
                new_target_group_id="ECS",
                listener=ecs.ListenerConfig.application_listener(listener,
                    protocol=elbv2.ApplicationProtocol.HTTPS
                )
            )
        """
        return jsii.invoke(self, "registerLoadBalancerTargets", [*targets])

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> "ICluster":
        """The cluster that hosts the service.

        stability
        :stability: experimental
        """
        return jsii.get(self, "cluster")

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _Connections_231f38b5:
        """The security groups which manage the allowed network traffic for the service.

        stability
        :stability: experimental
        """
        return jsii.get(self, "connections")

    @builtins.property
    @jsii.member(jsii_name="serviceArn")
    def service_arn(self) -> str:
        """The Amazon Resource Name (ARN) of the service.

        stability
        :stability: experimental
        """
        return jsii.get(self, "serviceArn")

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> str:
        """The name of the service.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "serviceName")

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> "TaskDefinition":
        """The task definition to use for tasks in the service.

        stability
        :stability: experimental
        """
        return jsii.get(self, "taskDefinition")

    @builtins.property
    @jsii.member(jsii_name="cloudMapService")
    def cloud_map_service(self) -> typing.Optional[_IService_f28ba3c9]:
        """The CloudMap service created for this service, if any.

        stability
        :stability: experimental
        """
        return jsii.get(self, "cloudMapService")

    @builtins.property
    @jsii.member(jsii_name="loadBalancers")
    def _load_balancers(self) -> typing.List["CfnService.LoadBalancerProperty"]:
        """A list of Elastic Load Balancing load balancer objects, containing the load balancer name, the container name (as it appears in a container definition), and the container port to access from the load balancer.

        stability
        :stability: experimental
        """
        return jsii.get(self, "loadBalancers")

    @_load_balancers.setter
    def _load_balancers(self, value: typing.List["CfnService.LoadBalancerProperty"]) -> None:
        jsii.set(self, "loadBalancers", value)

    @builtins.property
    @jsii.member(jsii_name="serviceRegistries")
    def _service_registries(self) -> typing.List["CfnService.ServiceRegistryProperty"]:
        """The details of the service discovery registries to assign to this service.

        For more information, see Service Discovery.

        stability
        :stability: experimental
        """
        return jsii.get(self, "serviceRegistries")

    @_service_registries.setter
    def _service_registries(self, value: typing.List["CfnService.ServiceRegistryProperty"]) -> None:
        jsii.set(self, "serviceRegistries", value)

    @builtins.property
    @jsii.member(jsii_name="cloudmapService")
    def _cloudmap_service(self) -> typing.Optional[_Service_4702d1e5]:
        """The details of the AWS Cloud Map service.

        stability
        :stability: experimental
        """
        return jsii.get(self, "cloudmapService")

    @_cloudmap_service.setter
    def _cloudmap_service(self, value: typing.Optional[_Service_4702d1e5]) -> None:
        jsii.set(self, "cloudmapService", value)

    @builtins.property
    @jsii.member(jsii_name="networkConfiguration")
    def _network_configuration(self) -> typing.Optional["CfnService.NetworkConfigurationProperty"]:
        """A list of Elastic Load Balancing load balancer objects, containing the load balancer name, the container name (as it appears in a container definition), and the container port to access from the load balancer.

        stability
        :stability: experimental
        """
        return jsii.get(self, "networkConfiguration")

    @_network_configuration.setter
    def _network_configuration(self, value: typing.Optional["CfnService.NetworkConfigurationProperty"]) -> None:
        jsii.set(self, "networkConfiguration", value)


class _BaseServiceProxy(BaseService, jsii.proxy_for(_Resource_884d0774)):
    pass

@jsii.implements(IEc2Service)
class Ec2Service(BaseService, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs.Ec2Service"):
    """This creates a service using the EC2 launch type on an ECS cluster.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::ECS::Service
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, task_definition: "TaskDefinition", assign_public_ip: typing.Optional[bool]=None, daemon: typing.Optional[bool]=None, placement_constraints: typing.Optional[typing.List["PlacementConstraint"]]=None, placement_strategies: typing.Optional[typing.List["PlacementStrategy"]]=None, propagate_task_tags_from: typing.Optional["PropagatedTagSource"]=None, security_group: typing.Optional[_ISecurityGroup_d72ab8e8]=None, security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]]=None, vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6]=None, cluster: "ICluster", cloud_map_options: typing.Optional["CloudMapOptions"]=None, deployment_controller: typing.Optional["DeploymentController"]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[_Duration_5170c158]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional["PropagatedTagSource"]=None, service_name: typing.Optional[str]=None) -> None:
        """Constructs a new instance of the Ec2Service class.

        :param scope: -
        :param id: -
        :param task_definition: The task definition to use for tasks in the service. [disable-awslint:ref-via-interface]
        :param assign_public_ip: Specifies whether the task's elastic network interface receives a public IP address. If true, each task will receive a public IP address. This property is only used for tasks that use the awsvpc network mode. Default: false
        :param daemon: Specifies whether the service will use the daemon scheduling strategy. If true, the service scheduler deploys exactly one task on each container instance in your cluster. When you are using this strategy, do not specify a desired number of tasks orany task placement strategies. Default: false
        :param placement_constraints: The placement constraints to use for tasks in the service. For more information, see `Amazon ECS Task Placement Constraints <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-constraints.html>`_. Default: - No constraints.
        :param placement_strategies: The placement strategies to use for tasks in the service. For more information, see `Amazon ECS Task Placement Strategies <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-strategies.html>`_. Default: - No strategies.
        :param propagate_task_tags_from: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: PropagatedTagSource.NONE
        :param security_group: The security groups to associate with the service. If you do not specify a security group, the default security group for the VPC is used. This property is only used for tasks that use the awsvpc network mode. Default: - A new security group is created.
        :param security_groups: The security groups to associate with the service. If you do not specify a security group, the default security group for the VPC is used. This property is only used for tasks that use the awsvpc network mode. Default: - A new security group is created.
        :param vpc_subnets: The subnets to associate with the service. This property is only used for tasks that use the awsvpc network mode. Default: - Public subnets if ``assignPublicIp`` is set, otherwise the first available one of Private, Isolated, Public, in that order.
        :param cluster: The name of the cluster that hosts the service.
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param deployment_controller: Specifies which deployment controller to use for the service. For more information, see `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_ Default: - Rolling update (ECS)
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Valid values are: PropagatedTagSource.SERVICE, PropagatedTagSource.TASK_DEFINITION or PropagatedTagSource.NONE Default: PropagatedTagSource.NONE
        :param service_name: The name of the service. Default: - CloudFormation-generated name.

        stability
        :stability: experimental
        """
        props = Ec2ServiceProps(task_definition=task_definition, assign_public_ip=assign_public_ip, daemon=daemon, placement_constraints=placement_constraints, placement_strategies=placement_strategies, propagate_task_tags_from=propagate_task_tags_from, security_group=security_group, security_groups=security_groups, vpc_subnets=vpc_subnets, cluster=cluster, cloud_map_options=cloud_map_options, deployment_controller=deployment_controller, desired_count=desired_count, enable_ecs_managed_tags=enable_ecs_managed_tags, health_check_grace_period=health_check_grace_period, max_healthy_percent=max_healthy_percent, min_healthy_percent=min_healthy_percent, propagate_tags=propagate_tags, service_name=service_name)

        jsii.create(Ec2Service, self, [scope, id, props])

    @jsii.member(jsii_name="fromEc2ServiceArn")
    @builtins.classmethod
    def from_ec2_service_arn(cls, scope: _Construct_f50a3f53, id: str, ec2_service_arn: str) -> "IEc2Service":
        """Imports from the specified service ARN.

        :param scope: -
        :param id: -
        :param ec2_service_arn: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromEc2ServiceArn", [scope, id, ec2_service_arn])

    @jsii.member(jsii_name="fromEc2ServiceAttributes")
    @builtins.classmethod
    def from_ec2_service_attributes(cls, scope: _Construct_f50a3f53, id: str, *, cluster: "ICluster", service_arn: typing.Optional[str]=None, service_name: typing.Optional[str]=None) -> "IBaseService":
        """Imports from the specified service attrributes.

        :param scope: -
        :param id: -
        :param cluster: The cluster that hosts the service.
        :param service_arn: The service ARN. Default: - either this, or {@link serviceName}, is required
        :param service_name: The name of the service. Default: - either this, or {@link serviceArn}, is required

        stability
        :stability: experimental
        """
        attrs = Ec2ServiceAttributes(cluster=cluster, service_arn=service_arn, service_name=service_name)

        return jsii.sinvoke(cls, "fromEc2ServiceAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="addPlacementConstraints")
    def add_placement_constraints(self, *constraints: "PlacementConstraint") -> None:
        """Adds one or more placement strategies to use for tasks in the service.

        For more information, see
        `Amazon ECS Task Placement Constraints <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-constraints.html>`_.

        :param constraints: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addPlacementConstraints", [*constraints])

    @jsii.member(jsii_name="addPlacementStrategies")
    def add_placement_strategies(self, *strategies: "PlacementStrategy") -> None:
        """Adds one or more placement strategies to use for tasks in the service.

        For more information, see
        `Amazon ECS Task Placement Strategies <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-strategies.html>`_.

        :param strategies: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addPlacementStrategies", [*strategies])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Validates this Ec2Service.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "validate", [])


@jsii.implements(IEc2TaskDefinition)
class Ec2TaskDefinition(TaskDefinition, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs.Ec2TaskDefinition"):
    """The details of a task definition run on an EC2 cluster.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::ECS::TaskDefinition
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, ipc_mode: typing.Optional["IpcMode"]=None, network_mode: typing.Optional["NetworkMode"]=None, pid_mode: typing.Optional["PidMode"]=None, placement_constraints: typing.Optional[typing.List["PlacementConstraint"]]=None, execution_role: typing.Optional[_IRole_e69bbae4]=None, family: typing.Optional[str]=None, proxy_configuration: typing.Optional["ProxyConfiguration"]=None, task_role: typing.Optional[_IRole_e69bbae4]=None, volumes: typing.Optional[typing.List["Volume"]]=None) -> None:
        """Constructs a new instance of the Ec2TaskDefinition class.

        :param scope: -
        :param id: -
        :param ipc_mode: The IPC resource namespace to use for the containers in the task. Not supported in Fargate and Windows containers. Default: - IpcMode used by the task is not specified
        :param network_mode: The Docker networking mode to use for the containers in the task. The valid values are none, bridge, awsvpc, and host. Default: - NetworkMode.Bridge for EC2 tasks, AwsVpc for Fargate tasks.
        :param pid_mode: The process namespace to use for the containers in the task. Not supported in Fargate and Windows containers. Default: - PidMode used by the task is not specified
        :param placement_constraints: An array of placement constraint objects to use for the task. You can specify a maximum of 10 constraints per task (this limit includes constraints in the task definition and those specified at run time). Default: - No placement constraints.
        :param execution_role: The name of the IAM task execution role that grants the ECS agent to call AWS APIs on your behalf. The role will be used to retrieve container images from ECR and create CloudWatch log groups. Default: - An execution role will be automatically created if you use ECR images in your task definition.
        :param family: The name of a family that this task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param proxy_configuration: The configuration details for the App Mesh proxy. Default: - No proxy configuration.
        :param task_role: The name of the IAM role that grants containers in the task permission to call AWS APIs on your behalf. Default: - A task role is automatically created for you.
        :param volumes: The list of volume definitions for the task. For more information, see `Task Definition Parameter Volumes <https://docs.aws.amazon.com/AmazonECS/latest/developerguide//task_definition_parameters.html#volumes>`_. Default: - No volumes are passed to the Docker daemon on a container instance.

        stability
        :stability: experimental
        """
        props = Ec2TaskDefinitionProps(ipc_mode=ipc_mode, network_mode=network_mode, pid_mode=pid_mode, placement_constraints=placement_constraints, execution_role=execution_role, family=family, proxy_configuration=proxy_configuration, task_role=task_role, volumes=volumes)

        jsii.create(Ec2TaskDefinition, self, [scope, id, props])

    @jsii.member(jsii_name="fromEc2TaskDefinitionArn")
    @builtins.classmethod
    def from_ec2_task_definition_arn(cls, scope: _Construct_f50a3f53, id: str, ec2_task_definition_arn: str) -> "IEc2TaskDefinition":
        """Imports a task definition from the specified task definition ARN.

        :param scope: -
        :param id: -
        :param ec2_task_definition_arn: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromEc2TaskDefinitionArn", [scope, id, ec2_task_definition_arn])


@jsii.implements(IFargateService)
class FargateService(BaseService, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs.FargateService"):
    """This creates a service using the Fargate launch type on an ECS cluster.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::ECS::Service
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, task_definition: "TaskDefinition", assign_public_ip: typing.Optional[bool]=None, platform_version: typing.Optional["FargatePlatformVersion"]=None, propagate_task_tags_from: typing.Optional["PropagatedTagSource"]=None, security_group: typing.Optional[_ISecurityGroup_d72ab8e8]=None, security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]]=None, vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6]=None, cluster: "ICluster", cloud_map_options: typing.Optional["CloudMapOptions"]=None, deployment_controller: typing.Optional["DeploymentController"]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[_Duration_5170c158]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional["PropagatedTagSource"]=None, service_name: typing.Optional[str]=None) -> None:
        """Constructs a new instance of the FargateService class.

        :param scope: -
        :param id: -
        :param task_definition: The task definition to use for tasks in the service. [disable-awslint:ref-via-interface]
        :param assign_public_ip: Specifies whether the task's elastic network interface receives a public IP address. If true, each task will receive a public IP address. Default: false
        :param platform_version: The platform version on which to run your service. If one is not specified, the LATEST platform version is used by default. For more information, see `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_ in the Amazon Elastic Container Service Developer Guide. Default: Latest
        :param propagate_task_tags_from: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: PropagatedTagSource.NONE
        :param security_group: The security groups to associate with the service. If you do not specify a security group, the default security group for the VPC is used. Default: - A new security group is created.
        :param security_groups: The security groups to associate with the service. If you do not specify a security group, the default security group for the VPC is used. Default: - A new security group is created.
        :param vpc_subnets: The subnets to associate with the service. Default: - Public subnets if ``assignPublicIp`` is set, otherwise the first available one of Private, Isolated, Public, in that order.
        :param cluster: The name of the cluster that hosts the service.
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param deployment_controller: Specifies which deployment controller to use for the service. For more information, see `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_ Default: - Rolling update (ECS)
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Valid values are: PropagatedTagSource.SERVICE, PropagatedTagSource.TASK_DEFINITION or PropagatedTagSource.NONE Default: PropagatedTagSource.NONE
        :param service_name: The name of the service. Default: - CloudFormation-generated name.

        stability
        :stability: experimental
        """
        props = FargateServiceProps(task_definition=task_definition, assign_public_ip=assign_public_ip, platform_version=platform_version, propagate_task_tags_from=propagate_task_tags_from, security_group=security_group, security_groups=security_groups, vpc_subnets=vpc_subnets, cluster=cluster, cloud_map_options=cloud_map_options, deployment_controller=deployment_controller, desired_count=desired_count, enable_ecs_managed_tags=enable_ecs_managed_tags, health_check_grace_period=health_check_grace_period, max_healthy_percent=max_healthy_percent, min_healthy_percent=min_healthy_percent, propagate_tags=propagate_tags, service_name=service_name)

        jsii.create(FargateService, self, [scope, id, props])

    @jsii.member(jsii_name="fromFargateServiceArn")
    @builtins.classmethod
    def from_fargate_service_arn(cls, scope: _Construct_f50a3f53, id: str, fargate_service_arn: str) -> "IFargateService":
        """Imports from the specified service ARN.

        :param scope: -
        :param id: -
        :param fargate_service_arn: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromFargateServiceArn", [scope, id, fargate_service_arn])

    @jsii.member(jsii_name="fromFargateServiceAttributes")
    @builtins.classmethod
    def from_fargate_service_attributes(cls, scope: _Construct_f50a3f53, id: str, *, cluster: "ICluster", service_arn: typing.Optional[str]=None, service_name: typing.Optional[str]=None) -> "IBaseService":
        """Imports from the specified service attrributes.

        :param scope: -
        :param id: -
        :param cluster: The cluster that hosts the service.
        :param service_arn: The service ARN. Default: - either this, or {@link serviceName}, is required
        :param service_name: The name of the service. Default: - either this, or {@link serviceArn}, is required

        stability
        :stability: experimental
        """
        attrs = FargateServiceAttributes(cluster=cluster, service_arn=service_arn, service_name=service_name)

        return jsii.sinvoke(cls, "fromFargateServiceAttributes", [scope, id, attrs])


@jsii.implements(IFargateTaskDefinition)
class FargateTaskDefinition(TaskDefinition, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ecs.FargateTaskDefinition"):
    """The details of a task definition run on a Fargate cluster.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::ECS::TaskDefinition
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, execution_role: typing.Optional[_IRole_e69bbae4]=None, family: typing.Optional[str]=None, proxy_configuration: typing.Optional["ProxyConfiguration"]=None, task_role: typing.Optional[_IRole_e69bbae4]=None, volumes: typing.Optional[typing.List["Volume"]]=None) -> None:
        """Constructs a new instance of the FargateTaskDefinition class.

        :param scope: -
        :param id: -
        :param cpu: The number of cpu units used by the task. For tasks using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) 512 (.5 vCPU) - Available memory values: 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) 1024 (1 vCPU) - Available memory values: 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) 2048 (2 vCPU) - Available memory values: Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) 4096 (4 vCPU) - Available memory values: Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) Default: 256
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. For tasks using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) Default: 512
        :param execution_role: The name of the IAM task execution role that grants the ECS agent to call AWS APIs on your behalf. The role will be used to retrieve container images from ECR and create CloudWatch log groups. Default: - An execution role will be automatically created if you use ECR images in your task definition.
        :param family: The name of a family that this task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param proxy_configuration: The configuration details for the App Mesh proxy. Default: - No proxy configuration.
        :param task_role: The name of the IAM role that grants containers in the task permission to call AWS APIs on your behalf. Default: - A task role is automatically created for you.
        :param volumes: The list of volume definitions for the task. For more information, see `Task Definition Parameter Volumes <https://docs.aws.amazon.com/AmazonECS/latest/developerguide//task_definition_parameters.html#volumes>`_. Default: - No volumes are passed to the Docker daemon on a container instance.

        stability
        :stability: experimental
        """
        props = FargateTaskDefinitionProps(cpu=cpu, memory_limit_mib=memory_limit_mib, execution_role=execution_role, family=family, proxy_configuration=proxy_configuration, task_role=task_role, volumes=volumes)

        jsii.create(FargateTaskDefinition, self, [scope, id, props])

    @jsii.member(jsii_name="fromFargateTaskDefinitionArn")
    @builtins.classmethod
    def from_fargate_task_definition_arn(cls, scope: _Construct_f50a3f53, id: str, fargate_task_definition_arn: str) -> "IFargateTaskDefinition":
        """Imports a task definition from the specified task definition ARN.

        :param scope: -
        :param id: -
        :param fargate_task_definition_arn: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromFargateTaskDefinitionArn", [scope, id, fargate_task_definition_arn])

    @builtins.property
    @jsii.member(jsii_name="networkMode")
    def network_mode(self) -> "NetworkMode":
        """The Docker networking mode to use for the containers in the task.

        Fargate tasks require the awsvpc network mode.

        stability
        :stability: experimental
        """
        return jsii.get(self, "networkMode")


__all__ = [
    "AddAutoScalingGroupCapacityOptions",
    "AddCapacityOptions",
    "AmiHardwareType",
    "AppMeshProxyConfiguration",
    "AppMeshProxyConfigurationConfigProps",
    "AppMeshProxyConfigurationProps",
    "AssetImage",
    "AssetImageProps",
    "AwsLogDriver",
    "AwsLogDriverProps",
    "BaseLogDriverProps",
    "BaseService",
    "BaseServiceOptions",
    "BaseServiceProps",
    "BinPackResource",
    "BuiltInAttributes",
    "Capability",
    "CfnCapacityProvider",
    "CfnCapacityProviderProps",
    "CfnCluster",
    "CfnClusterProps",
    "CfnPrimaryTaskSet",
    "CfnPrimaryTaskSetProps",
    "CfnService",
    "CfnServiceProps",
    "CfnTaskDefinition",
    "CfnTaskDefinitionProps",
    "CfnTaskSet",
    "CfnTaskSetProps",
    "CloudMapNamespaceOptions",
    "CloudMapOptions",
    "Cluster",
    "ClusterAttributes",
    "ClusterProps",
    "CommonTaskDefinitionProps",
    "Compatibility",
    "ContainerDefinition",
    "ContainerDefinitionOptions",
    "ContainerDefinitionProps",
    "ContainerDependency",
    "ContainerDependencyCondition",
    "ContainerImage",
    "ContainerImageConfig",
    "CpuUtilizationScalingProps",
    "DeploymentController",
    "DeploymentControllerType",
    "Device",
    "DevicePermission",
    "DockerVolumeConfiguration",
    "Ec2Service",
    "Ec2ServiceAttributes",
    "Ec2ServiceProps",
    "Ec2TaskDefinition",
    "Ec2TaskDefinitionProps",
    "EcrImage",
    "EcsOptimizedAmi",
    "EcsOptimizedAmiProps",
    "EcsOptimizedImage",
    "EcsTarget",
    "FargatePlatformVersion",
    "FargateService",
    "FargateServiceAttributes",
    "FargateServiceProps",
    "FargateTaskDefinition",
    "FargateTaskDefinitionProps",
    "FireLensLogDriver",
    "FireLensLogDriverProps",
    "FirelensConfig",
    "FirelensConfigFileType",
    "FirelensLogRouter",
    "FirelensLogRouterDefinitionOptions",
    "FirelensLogRouterProps",
    "FirelensLogRouterType",
    "FirelensOptions",
    "FluentdLogDriver",
    "FluentdLogDriverProps",
    "GelfCompressionType",
    "GelfLogDriver",
    "GelfLogDriverProps",
    "HealthCheck",
    "Host",
    "IBaseService",
    "ICluster",
    "IEc2Service",
    "IEc2TaskDefinition",
    "IEcsLoadBalancerTarget",
    "IFargateService",
    "IFargateTaskDefinition",
    "IService",
    "ITaskDefinition",
    "ITaskDefinitionExtension",
    "IpcMode",
    "JournaldLogDriver",
    "JournaldLogDriverProps",
    "JsonFileLogDriver",
    "JsonFileLogDriverProps",
    "LaunchType",
    "LinuxParameters",
    "LinuxParametersProps",
    "ListenerConfig",
    "LoadBalancerTargetOptions",
    "LogDriver",
    "LogDriverConfig",
    "LogDrivers",
    "MemoryUtilizationScalingProps",
    "MountPoint",
    "NetworkMode",
    "PidMode",
    "PlacementConstraint",
    "PlacementStrategy",
    "PortMapping",
    "PropagatedTagSource",
    "Protocol",
    "ProxyConfiguration",
    "ProxyConfigurations",
    "RepositoryImage",
    "RepositoryImageProps",
    "RequestCountScalingProps",
    "ScalableTaskCount",
    "ScalableTaskCountProps",
    "Scope",
    "ScratchSpace",
    "Secret",
    "SplunkLogDriver",
    "SplunkLogDriverProps",
    "SplunkLogFormat",
    "SyslogLogDriver",
    "SyslogLogDriverProps",
    "TaskDefinition",
    "TaskDefinitionProps",
    "Tmpfs",
    "TmpfsMountOption",
    "TrackCustomMetricProps",
    "Ulimit",
    "UlimitName",
    "Volume",
    "VolumeFrom",
    "WindowsOptimizedVersion",
]

publication.publish()
