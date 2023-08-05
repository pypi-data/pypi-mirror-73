"""
## Amazon EKS Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development. They are subject to non-backward compatible changes or removal in any future version. These are not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be announced in the release notes. This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This construct library allows you to define [Amazon Elastic Container Service
for Kubernetes (EKS)](https://aws.amazon.com/eks/) clusters programmatically.
This library also supports programmatically defining Kubernetes resource
manifests within EKS clusters.

This example defines an Amazon EKS cluster with the following configuration:

* Managed nodegroup with 2x **m5.large** instances (this instance type suits most common use-cases, and is good value for money)
* Dedicated VPC with default configuration (see [ec2.Vpc](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-ec2-readme.html#vpc))
* A Kubernetes pod with a container based on the [paulbouwer/hello-kubernetes](https://github.com/paulbouwer/hello-kubernetes) image.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster = eks.Cluster(self, "hello-eks")

cluster.add_resource("mypod",
    api_version="v1",
    kind="Pod",
    metadata={"name": "mypod"},
    spec={
        "containers": [{
            "name": "hello",
            "image": "paulbouwer/hello-kubernetes:1.5",
            "ports": [{"container_port": 8080}]
        }
        ]
    }
)
```

### Capacity

By default, `eks.Cluster` is created with a managed nodegroup with x2 `m5.large` instances.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
eks.Cluster(self, "cluster-two-m5-large")
```

To use the traditional self-managed Amazon EC2 instances instead, set `defaultCapacityType` to `DefaultCapacityType.EC2`

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster = eks.Cluster(self, "cluster-self-managed-ec2",
    default_capacity_type=eks.DefaultCapacityType.EC2
)
```

The quantity and instance type for the default capacity can be specified through
the `defaultCapacity` and `defaultCapacityInstance` props:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
eks.Cluster(self, "cluster",
    default_capacity=10,
    default_capacity_instance=ec2.InstanceType("m2.xlarge")
)
```

To disable the default capacity, simply set `defaultCapacity` to `0`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
eks.Cluster(self, "cluster-with-no-capacity", default_capacity=0)
```

The `cluster.defaultCapacity` property will reference the `AutoScalingGroup`
resource for the default capacity. It will be `undefined` if `defaultCapacity`
is set to `0` or `defaultCapacityType` is either `NODEGROUP` or undefined.

And the `cluster.defaultNodegroup` property will reference the `Nodegroup`
resource for the default capacity. It will be `undefined` if `defaultCapacity`
is set to `0` or `defaultCapacityType` is `EC2`.

You can add `AutoScalingGroup` resource as customized capacity through `cluster.addCapacity()` or
`cluster.addAutoScalingGroup()`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster.add_capacity("frontend-nodes",
    instance_type=ec2.InstanceType("t2.medium"),
    min_capacity=3,
    vpc_subnets={"subnet_type": ec2.SubnetType.PUBLIC}
)
```

### Managed Node Groups

Amazon EKS managed node groups automate the provisioning and lifecycle management of nodes (Amazon EC2 instances)
for Amazon EKS Kubernetes clusters. By default, `eks.Nodegroup` create a nodegroup with x2 `t3.medium` instances.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
eks.Nodegroup(stack, "nodegroup", cluster=cluster)
```

You can add customized node group through `cluster.addNodegroup()`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster.add_nodegroup("nodegroup",
    instance_type=ec2.InstanceType("m5.large"),
    min_size=4
)
```

### Fargate

AWS Fargate is a technology that provides on-demand, right-sized compute
capacity for containers. With AWS Fargate, you no longer have to provision,
configure, or scale groups of virtual machines to run containers. This removes
the need to choose server types, decide when to scale your node groups, or
optimize cluster packing.

You can control which pods start on Fargate and how they run with Fargate
Profiles, which are defined as part of your Amazon EKS cluster.

See [Fargate
Considerations](https://docs.aws.amazon.com/eks/latest/userguide/fargate.html#fargate-considerations)
in the AWS EKS User Guide.

You can add Fargate Profiles to any EKS cluster defined in your CDK app
through the `addFargateProfile()` method. The following example adds a profile
that will match all pods from the "default" namespace:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster.add_fargate_profile("MyProfile",
    selectors=[{"namespace": "default"}]
)
```

To create an EKS cluster that **only** uses Fargate capacity, you can use
`FargateCluster`.

The following code defines an Amazon EKS cluster without EC2 capacity and a default
Fargate Profile that matches all pods from the "kube-system" and "default" namespaces. It is also configured to [run CoreDNS on Fargate](https://docs.aws.amazon.com/eks/latest/userguide/fargate-getting-started.html#fargate-gs-coredns) through the `coreDnsComputeType` cluster option.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster = eks.FargateCluster(self, "MyCluster")

# apply k8s resources on this cluster
cluster.add_resource(...)
```

**NOTE**: Classic Load Balancers and Network Load Balancers are not supported on
pods running on Fargate. For ingress, we recommend that you use the [ALB Ingress
Controller](https://docs.aws.amazon.com/eks/latest/userguide/alb-ingress.html)
on Amazon EKS (minimum version v1.1.4).

### Spot Capacity

If `spotPrice` is specified, the capacity will be purchased from spot instances:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster.add_capacity("spot",
    spot_price="0.1094",
    instance_type=ec2.InstanceType("t3.large"),
    max_capacity=10
)
```

Spot instance nodes will be labeled with `lifecycle=Ec2Spot` and tainted with `PreferNoSchedule`.

The [AWS Node Termination Handler](https://github.com/aws/aws-node-termination-handler)
DaemonSet will be installed from [
Amazon EKS Helm chart repository
](https://github.com/aws/eks-charts/tree/master/stable/aws-node-termination-handler) on these nodes. The termination handler ensures that the Kubernetes control plane responds appropriately to events that can cause your EC2 instance to become unavailable, such as [EC2 maintenance events](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/monitoring-instances-status-check_sched.html) and [EC2 Spot interruptions](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-interruptions.html) and helps gracefully stop all pods running on spot nodes that are about to be
terminated.

### Bootstrapping

When adding capacity, you can specify options for
[/etc/eks/boostrap.sh](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh)
which is responsible for associating the node to the EKS cluster. For example,
you can use `kubeletExtraArgs` to add custom node labels or taints.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# up to ten spot instances
cluster.add_capacity("spot",
    instance_type=ec2.InstanceType("t3.large"),
    min_capacity=2,
    bootstrap_options={
        "kubelet_extra_args": "--node-labels foo=bar,goo=far",
        "aws_api_retry_attempts": 5
    }
)
```

To disable bootstrapping altogether (i.e. to fully customize user-data), set `bootstrapEnabled` to `false` when you add
the capacity.

### Masters Role

The Amazon EKS construct library allows you to specify an IAM role that will be
granted `system:masters` privileges on your cluster.

Without specifying a `mastersRole`, you will not be able to interact manually
with the cluster.

The following example defines an IAM role that can be assumed by all users
in the account and shows how to use the `mastersRole` property to map this
role to the Kubernetes `system:masters` group:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# first define the role
cluster_admin = iam.Role(self, "AdminRole",
    assumed_by=iam.AccountRootPrincipal()
)

# now define the cluster and map role to "masters" RBAC group
eks.Cluster(self, "Cluster",
    masters_role=cluster_admin
)
```

When you `cdk deploy` this CDK app, you will notice that an output will be printed
with the `update-kubeconfig` command.

Something like this:

```
Outputs:
eks-integ-defaults.ClusterConfigCommand43AAE40F = aws eks update-kubeconfig --name cluster-ba7c166b-c4f3-421c-bf8a-6812e4036a33 --role-arn arn:aws:iam::112233445566:role/eks-integ-defaults-Role1ABCC5F0-1EFK2W5ZJD98Y
```

Copy & paste the "`aws eks update-kubeconfig ...`" command to your shell in
order to connect to your EKS cluster with the "masters" role.

Now, given [AWS CLI](https://aws.amazon.com/cli/) is configured to use AWS
credentials for a user that is trusted by the masters role, you should be able
to interact with your cluster through `kubectl` (the above example will trust
all users in the account).

For example:

```console
$ aws eks update-kubeconfig --name cluster-ba7c166b-c4f3-421c-bf8a-6812e4036a33 --role-arn arn:aws:iam::112233445566:role/eks-integ-defaults-Role1ABCC5F0-1EFK2W5ZJD98Y
Added new context arn:aws:eks:eu-west-2:112233445566:cluster/cluster-ba7c166b-c4f3-421c-bf8a-6812e4036a33 to /Users/boom/.kube/config

$ kubectl get nodes # list all nodes
NAME                                         STATUS   ROLES    AGE   VERSION
ip-10-0-147-66.eu-west-2.compute.internal    Ready    <none>   21m   v1.13.7-eks-c57ff8
ip-10-0-169-151.eu-west-2.compute.internal   Ready    <none>   21m   v1.13.7-eks-c57ff8

$ kubectl get all -n kube-system
NAME                           READY   STATUS    RESTARTS   AGE
pod/aws-node-fpmwv             1/1     Running   0          21m
pod/aws-node-m9htf             1/1     Running   0          21m
pod/coredns-5cb4fb54c7-q222j   1/1     Running   0          23m
pod/coredns-5cb4fb54c7-v9nxx   1/1     Running   0          23m
pod/kube-proxy-d4jrh           1/1     Running   0          21m
pod/kube-proxy-q7hh7           1/1     Running   0          21m

NAME               TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)         AGE
service/kube-dns   ClusterIP   172.20.0.10   <none>        53/UDP,53/TCP   23m

NAME                        DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
daemonset.apps/aws-node     2         2         2       2            2           <none>          23m
daemonset.apps/kube-proxy   2         2         2       2            2           <none>          23m

NAME                      READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/coredns   2/2     2            2           23m

NAME                                 DESIRED   CURRENT   READY   AGE
replicaset.apps/coredns-5cb4fb54c7   2         2         2       23m
```

For your convenience, an AWS CloudFormation output will automatically be
included in your template and will be printed when running `cdk deploy`.

**NOTE**: if the cluster is configured with `kubectlEnabled: false`, it
will be created with the role/user that created the AWS CloudFormation
stack. See [Kubectl Support](#kubectl-support) for details.

### Kubernetes Resources

The `KubernetesResource` construct or `cluster.addResource` method can be used
to apply Kubernetes resource manifests to this cluster.

The following examples will deploy the [paulbouwer/hello-kubernetes](https://github.com/paulbouwer/hello-kubernetes)
service on the cluster:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
app_label = {"app": "hello-kubernetes"}

deployment = {
    "api_version": "apps/v1",
    "kind": "Deployment",
    "metadata": {"name": "hello-kubernetes"},
    "spec": {
        "replicas": 3,
        "selector": {"match_labels": app_label},
        "template": {
            "metadata": {"labels": app_label},
            "spec": {
                "containers": [{
                    "name": "hello-kubernetes",
                    "image": "paulbouwer/hello-kubernetes:1.5",
                    "ports": [{"container_port": 8080}]
                }
                ]
            }
        }
    }
}

service = {
    "api_version": "v1",
    "kind": "Service",
    "metadata": {"name": "hello-kubernetes"},
    "spec": {
        "type": "LoadBalancer",
        "ports": [{"port": 80, "target_port": 8080}],
        "selector": app_label
    }
}

# option 1: use a construct
KubernetesResource(self, "hello-kub",
    cluster=cluster,
    manifest=[deployment, service]
)

# or, option2: use `addResource`
cluster.add_resource("hello-kub", service, deployment)
```

Since Kubernetes resources are implemented as CloudFormation resources in the
CDK. This means that if the resource is deleted from your code (or the stack is
deleted), the next `cdk deploy` will issue a `kubectl delete` command and the
Kubernetes resources will be deleted.

#### Dependencies

There are cases where Kubernetes resources must be deployed in a specific order.
For example, you cannot define a resource in a Kubernetes namespace before the
namespace was created.

You can represent dependencies between `KubernetesResource`s using
`resource.node.addDependency()`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
namespace = cluster.add_resource("my-namespace",
    api_version="v1",
    kind="Namespace",
    metadata={"name": "my-app"}
)

service = cluster.add_resource("my-service",
    metadata={
        "name": "myservice",
        "namespace": "my-app"
    },
    spec=
)

service.node.add_dependency(namespace)
```

NOTE: when a `KubernetesResource` includes multiple resources (either directly
or through `cluster.addResource()`) (e.g. `cluster.addResource('foo', r1, r2, r3,...))`), these resources will be applied as a single manifest via `kubectl`
and will be applied sequentially (the standard behavior in `kubectl`).

### Patching Kubernetes Resources

The KubernetesPatch construct can be used to update existing kubernetes
resources. The following example can be used to patch the `hello-kubernetes`
deployment from the example above with 5 replicas.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
KubernetesPatch(self, "hello-kub-deployment-label",
    cluster=cluster,
    resource_name="deployment/hello-kubernetes",
    apply_patch={"spec": {"replicas": 5}},
    restore_patch={"spec": {"replicas": 3}}
)
```

### AWS IAM Mapping

As described in the [Amazon EKS User Guide](https://docs.aws.amazon.com/en_us/eks/latest/userguide/add-user-role.html),
you can map AWS IAM users and roles to [Kubernetes Role-based access control (RBAC)](https://kubernetes.io/docs/reference/access-authn-authz/rbac).

The Amazon EKS construct manages the **aws-auth ConfigMap** Kubernetes resource
on your behalf and exposes an API through the `cluster.awsAuth` for mapping
users, roles and accounts.

Furthermore, when auto-scaling capacity is added to the cluster (through
`cluster.addCapacity` or `cluster.addAutoScalingGroup`), the IAM instance role
of the auto-scaling group will be automatically mapped to RBAC so nodes can
connect to the cluster. No manual mapping is required any longer.

> NOTE: `cluster.awsAuth` will throw an error if your cluster is created with `kubectlEnabled: false`.

For example, let's say you want to grant an IAM user administrative privileges
on your cluster:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
admin_user = iam.User(self, "Admin")
cluster.aws_auth.add_user_mapping(admin_user, groups=["system:masters"])
```

A convenience method for mapping a role to the `system:masters` group is also available:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster.aws_auth.add_masters_role(role)
```

### Cluster Security Group

When you create an Amazon EKS cluster, a
[cluster security group](https://docs.aws.amazon.com/eks/latest/userguide/sec-group-reqs.html)
is automatically created as well. This security group is designed to allow
all traffic from the control plane and managed node groups to flow freely
between each other.

The ID for that security group can be retrieved after creating the cluster.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster_security_group_id = cluster.cluster_security_group_id
```

### Cluster Encryption Configuration

When you create an Amazon EKS cluster, envelope encryption of
Kubernetes secrets using the AWS Key Management Service (AWS KMS) can be enabled. The documentation
on [creating a cluster](https://docs.aws.amazon.com/eks/latest/userguide/create-cluster.html)
can provide more details about the customer master key (CMK) that can be used for the encryption.

The Amazon Resource Name (ARN) for that CMK can be retrieved.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster_encryption_config_key_arn = cluster.cluster_encryption_config_key_arn
```

### Node ssh Access

If you want to be able to SSH into your worker nodes, you must already
have an SSH key in the region you're connecting to and pass it, and you must
be able to connect to the hosts (meaning they must have a public IP and you
should be allowed to connect to them on port 22):

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
asg = cluster.add_capacity("Nodes",
    instance_type=ec2.InstanceType("t2.medium"),
    vpc_subnets=SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
    key_name="my-key-name"
)

# Replace with desired IP
asg.connections.allow_from(ec2.Peer.ipv4("1.2.3.4/32"), ec2.Port.tcp(22))
```

If you want to SSH into nodes in a private subnet, you should set up a
bastion host in a public subnet. That setup is recommended, but is
unfortunately beyond the scope of this documentation.

### kubectl Support

When you create an Amazon EKS cluster, the IAM entity user or role, such as a
[federated user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers.html)
that creates the cluster, is automatically granted `system:masters` permissions
in the cluster's RBAC configuration.

In order to allow programmatically defining **Kubernetes resources** in your AWS
CDK app and provisioning them through AWS CloudFormation, we will need to assume
this "masters" role every time we want to issue `kubectl` operations against your
cluster.

At the moment, the [AWS::EKS::Cluster](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html)
AWS CloudFormation resource does not support this behavior, so in order to
support "programmatic kubectl", such as applying manifests
and mapping IAM roles from within your CDK application, the Amazon EKS
construct library uses a custom resource for provisioning the cluster.
This custom resource is executed with an IAM role that we can then use
to issue `kubectl` commands.

The default behavior of this library is to use this custom resource in order
to retain programmatic control over the cluster. In other words: to allow
you to define Kubernetes resources in your CDK code instead of having to
manage your Kubernetes applications through a separate system.

One of the implications of this design is that, by default, the user who
provisioned the AWS CloudFormation stack (executed `cdk deploy`) will
not have administrative privileges on the EKS cluster.

1. Additional resources will be synthesized into your template (the AWS Lambda
   function, the role and policy).
2. As described in [Interacting with Your Cluster](#interacting-with-your-cluster),
   if you wish to be able to manually interact with your cluster, you will need
   to map an IAM role or user to the `system:masters` group. This can be either
   done by specifying a `mastersRole` when the cluster is defined, calling
   `cluster.awsAuth.addMastersRole` or explicitly mapping an IAM role or IAM user to the
   relevant Kubernetes RBAC groups using `cluster.addRoleMapping` and/or
   `cluster.addUserMapping`.

If you wish to disable the programmatic kubectl behavior and use the standard
AWS::EKS::Cluster resource, you can specify `kubectlEnabled: false` when you define
the cluster:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
eks.Cluster(self, "cluster",
    kubectl_enabled=False
)
```

**Take care**: a change in this property will cause the cluster to be destroyed
and a new cluster to be created.

When kubectl is disabled, you should be aware of the following:

1. When you log-in to your cluster, you don't need to specify `--role-arn` as
   long as you are using the same user that created the cluster.
2. As described in the Amazon EKS User Guide, you will need to manually
   edit the [aws-auth ConfigMap](https://docs.aws.amazon.com/eks/latest/userguide/add-user-role.html)
   when you add capacity in order to map the IAM instance role to RBAC to allow nodes to join the cluster.
3. Any `eks.Cluster` APIs that depend on programmatic kubectl support will fail
   with an error: `cluster.addResource`, `cluster.addChart`, `cluster.awsAuth`, `props.mastersRole`.

### Helm Charts

The `HelmChart` construct or `cluster.addChart` method can be used
to add Kubernetes resources to this cluster using Helm.

The following example will install the [NGINX Ingress Controller](https://kubernetes.github.io/ingress-nginx/)
to you cluster using Helm.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# option 1: use a construct
HelmChart(self, "NginxIngress",
    cluster=cluster,
    chart="nginx-ingress",
    repository="https://helm.nginx.com/stable",
    namespace="kube-system"
)

# or, option2: use `addChart`
cluster.add_chart("NginxIngress",
    chart="nginx-ingress",
    repository="https://helm.nginx.com/stable",
    namespace="kube-system"
)
```

Helm charts will be installed and updated using `helm upgrade --install`, where a few parameters
are being passed down (such as `repo`, `values`, `version`, `namespace`, `wait`, `timeout`, etc).
This means that if the chart is added to CDK with the same release name, it will try to update
the chart in the cluster. The chart will exists as CloudFormation resource.

Helm charts are implemented as CloudFormation resources in CDK.
This means that if the chart is deleted from your code (or the stack is
deleted), the next `cdk deploy` will issue a `helm uninstall` command and the
Helm chart will be deleted.

When there is no `release` defined, the chart will be installed using the `node.uniqueId`,
which will be lower cased and truncated to the last 63 characters.

By default, all Helm charts will be installed concurrently. In some cases, this
could cause race conditions where two Helm charts attempt to deploy the same
resource or if Helm charts depend on each other. You can use
`chart.node.addDependency()` in order to declare a dependency order between
charts:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
chart1 = cluster.add_chart(...)
chart2 = cluster.add_chart(...)

chart2.node.add_dependency(chart1)
```

### Bottlerocket

[Bottlerocket](https://aws.amazon.com/bottlerocket/) is a Linux-based open-source operating system that is purpose-built by Amazon Web Services for running containers on virtual machines or bare metal hosts. At this moment the managed nodegroup only supports Amazon EKS-optimized AMI but it's possible to create a capacity of self-managed `AutoScalingGroup` running with bottlerocket Linux AMI.

> **NOTICE**: Bottlerocket is in public preview and only available in [some supported AWS regions](https://github.com/bottlerocket-os/bottlerocket/blob/develop/QUICKSTART.md#finding-an-ami).

The following example will create a capacity with self-managed Amazon EC2 capacity of 2 `t3.small` Linux instances running with `Bottlerocket` AMI.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# add bottlerocket nodes
cluster.add_capacity("BottlerocketNodes",
    instance_type=ec2.InstanceType("t3.small"),
    min_capacity=2,
    machine_image_type=eks.MachineImageType.BOTTLEROCKET
)
```

To define only Bottlerocket capacity in your cluster, set `defaultCapacity` to `0` when you define the cluster as described above.

Please note Bottlerocket does not allow to customize bootstrap options and `bootstrapOptions` properties is not supported when you create the `Bottlerocket` capacity.

### Service Accounts

With services account you can provide Kubernetes Pods access to AWS resources.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# add service account
sa = cluster.add_service_account("MyServiceAccount")

bucket = Bucket(self, "Bucket")
bucket.grant_read_write(service_account)

mypod = cluster.add_resource("mypod",
    api_version="v1",
    kind="Pod",
    metadata={"name": "mypod"},
    spec={
        "service_account_name": sa.service_account_name,
        "containers": [{
            "name": "hello",
            "image": "paulbouwer/hello-kubernetes:1.5",
            "ports": [{"container_port": 8080}]
        }
        ]
    }
)

# create the resource after the service account
mypod.node.add_dependency(sa)

# print the IAM role arn for this service account
cdk.CfnOutput(self, "ServiceAccountIamRole", value=sa.role.role_arn)
```

### Roadmap

* [ ] AutoScaling (combine EC2 and Kubernetes scaling)
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from ._jsii import *

import aws_cdk.aws_autoscaling
import aws_cdk.aws_ec2
import aws_cdk.aws_iam
import aws_cdk.aws_sns
import aws_cdk.core


@jsii.data_type(jsii_type="@aws-cdk/aws-eks.AutoScalingGroupOptions", jsii_struct_bases=[], name_mapping={'bootstrap_enabled': 'bootstrapEnabled', 'bootstrap_options': 'bootstrapOptions', 'machine_image_type': 'machineImageType', 'map_role': 'mapRole'})
class AutoScalingGroupOptions():
    def __init__(self, *, bootstrap_enabled: typing.Optional[bool]=None, bootstrap_options: typing.Optional["BootstrapOptions"]=None, machine_image_type: typing.Optional["MachineImageType"]=None, map_role: typing.Optional[bool]=None) -> None:
        """Options for adding an AutoScalingGroup as capacity.

        :param bootstrap_enabled: Configures the EC2 user-data script for instances in this autoscaling group to bootstrap the node (invoke ``/etc/eks/bootstrap.sh``) and associate it with the EKS cluster. If you wish to provide a custom user data script, set this to ``false`` and manually invoke ``autoscalingGroup.addUserData()``. Default: true
        :param bootstrap_options: Allows options for node bootstrapping through EC2 user data. Default: - default options
        :param machine_image_type: Allow options to specify different machine image type. Default: MachineImageType.AMAZON_LINUX_2
        :param map_role: Will automatically update the aws-auth ConfigMap to map the IAM instance role to RBAC. This cannot be explicitly set to ``true`` if the cluster has kubectl disabled. Default: - true if the cluster has kubectl enabled (which is the default).

        stability
        :stability: experimental
        """
        if isinstance(bootstrap_options, dict): bootstrap_options = BootstrapOptions(**bootstrap_options)
        self._values = {
        }
        if bootstrap_enabled is not None: self._values["bootstrap_enabled"] = bootstrap_enabled
        if bootstrap_options is not None: self._values["bootstrap_options"] = bootstrap_options
        if machine_image_type is not None: self._values["machine_image_type"] = machine_image_type
        if map_role is not None: self._values["map_role"] = map_role

    @builtins.property
    def bootstrap_enabled(self) -> typing.Optional[bool]:
        """Configures the EC2 user-data script for instances in this autoscaling group to bootstrap the node (invoke ``/etc/eks/bootstrap.sh``) and associate it with the EKS cluster.

        If you wish to provide a custom user data script, set this to ``false`` and
        manually invoke ``autoscalingGroup.addUserData()``.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('bootstrap_enabled')

    @builtins.property
    def bootstrap_options(self) -> typing.Optional["BootstrapOptions"]:
        """Allows options for node bootstrapping through EC2 user data.

        default
        :default: - default options

        stability
        :stability: experimental
        """
        return self._values.get('bootstrap_options')

    @builtins.property
    def machine_image_type(self) -> typing.Optional["MachineImageType"]:
        """Allow options to specify different machine image type.

        default
        :default: MachineImageType.AMAZON_LINUX_2

        stability
        :stability: experimental
        """
        return self._values.get('machine_image_type')

    @builtins.property
    def map_role(self) -> typing.Optional[bool]:
        """Will automatically update the aws-auth ConfigMap to map the IAM instance role to RBAC.

        This cannot be explicitly set to ``true`` if the cluster has kubectl disabled.

        default
        :default: - true if the cluster has kubectl enabled (which is the default).

        stability
        :stability: experimental
        """
        return self._values.get('map_role')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AutoScalingGroupOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class AwsAuth(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-eks.AwsAuth"):
    """Manages mapping between IAM users and roles to Kubernetes RBAC configuration.

    see
    :see: https://docs.aws.amazon.com/en_us/eks/latest/userguide/add-user-role.html
    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, cluster: "Cluster") -> None:
        """
        :param scope: -
        :param id: -
        :param cluster: The EKS cluster to apply this configuration to. [disable-awslint:ref-via-interface]

        stability
        :stability: experimental
        """
        props = AwsAuthProps(cluster=cluster)

        jsii.create(AwsAuth, self, [scope, id, props])

    @jsii.member(jsii_name="addAccount")
    def add_account(self, account_id: str) -> None:
        """Additional AWS account to add to the aws-auth configmap.

        :param account_id: account number.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addAccount", [account_id])

    @jsii.member(jsii_name="addMastersRole")
    def add_masters_role(self, role: aws_cdk.aws_iam.IRole, username: typing.Optional[str]=None) -> None:
        """Adds the specified IAM role to the ``system:masters`` RBAC group, which means that anyone that can assume it will be able to administer this Kubernetes system.

        :param role: The IAM role to add.
        :param username: Optional user (defaults to the role ARN).

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addMastersRole", [role, username])

    @jsii.member(jsii_name="addRoleMapping")
    def add_role_mapping(self, role: aws_cdk.aws_iam.IRole, *, groups: typing.List[str], username: typing.Optional[str]=None) -> None:
        """Adds a mapping between an IAM role to a Kubernetes user and groups.

        :param role: The IAM role to map.
        :param groups: A list of groups within Kubernetes to which the role is mapped.
        :param username: The user name within Kubernetes to map to the IAM role. Default: - By default, the user name is the ARN of the IAM role.

        stability
        :stability: experimental
        """
        mapping = AwsAuthMapping(groups=groups, username=username)

        return jsii.invoke(self, "addRoleMapping", [role, mapping])

    @jsii.member(jsii_name="addUserMapping")
    def add_user_mapping(self, user: aws_cdk.aws_iam.IUser, *, groups: typing.List[str], username: typing.Optional[str]=None) -> None:
        """Adds a mapping between an IAM user to a Kubernetes user and groups.

        :param user: The IAM user to map.
        :param groups: A list of groups within Kubernetes to which the role is mapped.
        :param username: The user name within Kubernetes to map to the IAM role. Default: - By default, the user name is the ARN of the IAM role.

        stability
        :stability: experimental
        """
        mapping = AwsAuthMapping(groups=groups, username=username)

        return jsii.invoke(self, "addUserMapping", [user, mapping])


@jsii.data_type(jsii_type="@aws-cdk/aws-eks.AwsAuthMapping", jsii_struct_bases=[], name_mapping={'groups': 'groups', 'username': 'username'})
class AwsAuthMapping():
    def __init__(self, *, groups: typing.List[str], username: typing.Optional[str]=None) -> None:
        """AwsAuth mapping.

        :param groups: A list of groups within Kubernetes to which the role is mapped.
        :param username: The user name within Kubernetes to map to the IAM role. Default: - By default, the user name is the ARN of the IAM role.

        stability
        :stability: experimental
        """
        self._values = {
            'groups': groups,
        }
        if username is not None: self._values["username"] = username

    @builtins.property
    def groups(self) -> typing.List[str]:
        """A list of groups within Kubernetes to which the role is mapped.

        see
        :see: https://kubernetes.io/docs/reference/access-authn-authz/rbac/#default-roles-and-role-bindings
        stability
        :stability: experimental
        """
        return self._values.get('groups')

    @builtins.property
    def username(self) -> typing.Optional[str]:
        """The user name within Kubernetes to map to the IAM role.

        default
        :default: - By default, the user name is the ARN of the IAM role.

        stability
        :stability: experimental
        """
        return self._values.get('username')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AwsAuthMapping(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-eks.AwsAuthProps", jsii_struct_bases=[], name_mapping={'cluster': 'cluster'})
class AwsAuthProps():
    def __init__(self, *, cluster: "Cluster") -> None:
        """Configuration props for the AwsAuth construct.

        :param cluster: The EKS cluster to apply this configuration to. [disable-awslint:ref-via-interface]

        stability
        :stability: experimental
        """
        self._values = {
            'cluster': cluster,
        }

    @builtins.property
    def cluster(self) -> "Cluster":
        """The EKS cluster to apply this configuration to.

        [disable-awslint:ref-via-interface]

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AwsAuthProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-eks.BootstrapOptions", jsii_struct_bases=[], name_mapping={'additional_args': 'additionalArgs', 'aws_api_retry_attempts': 'awsApiRetryAttempts', 'docker_config_json': 'dockerConfigJson', 'enable_docker_bridge': 'enableDockerBridge', 'kubelet_extra_args': 'kubeletExtraArgs', 'use_max_pods': 'useMaxPods'})
class BootstrapOptions():
    def __init__(self, *, additional_args: typing.Optional[str]=None, aws_api_retry_attempts: typing.Optional[jsii.Number]=None, docker_config_json: typing.Optional[str]=None, enable_docker_bridge: typing.Optional[bool]=None, kubelet_extra_args: typing.Optional[str]=None, use_max_pods: typing.Optional[bool]=None) -> None:
        """EKS node bootstrapping options.

        :param additional_args: Additional command line arguments to pass to the ``/etc/eks/bootstrap.sh`` command. Default: - none
        :param aws_api_retry_attempts: Number of retry attempts for AWS API call (DescribeCluster). Default: 3
        :param docker_config_json: The contents of the ``/etc/docker/daemon.json`` file. Useful if you want a custom config differing from the default one in the EKS AMI. Default: - none
        :param enable_docker_bridge: Restores the docker default bridge network. Default: false
        :param kubelet_extra_args: Extra arguments to add to the kubelet. Useful for adding labels or taints. Default: - none
        :param use_max_pods: Sets ``--max-pods`` for the kubelet based on the capacity of the EC2 instance. Default: true

        stability
        :stability: experimental
        """
        self._values = {
        }
        if additional_args is not None: self._values["additional_args"] = additional_args
        if aws_api_retry_attempts is not None: self._values["aws_api_retry_attempts"] = aws_api_retry_attempts
        if docker_config_json is not None: self._values["docker_config_json"] = docker_config_json
        if enable_docker_bridge is not None: self._values["enable_docker_bridge"] = enable_docker_bridge
        if kubelet_extra_args is not None: self._values["kubelet_extra_args"] = kubelet_extra_args
        if use_max_pods is not None: self._values["use_max_pods"] = use_max_pods

    @builtins.property
    def additional_args(self) -> typing.Optional[str]:
        """Additional command line arguments to pass to the ``/etc/eks/bootstrap.sh`` command.

        default
        :default: - none

        see
        :see: https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh
        stability
        :stability: experimental
        """
        return self._values.get('additional_args')

    @builtins.property
    def aws_api_retry_attempts(self) -> typing.Optional[jsii.Number]:
        """Number of retry attempts for AWS API call (DescribeCluster).

        default
        :default: 3

        stability
        :stability: experimental
        """
        return self._values.get('aws_api_retry_attempts')

    @builtins.property
    def docker_config_json(self) -> typing.Optional[str]:
        """The contents of the ``/etc/docker/daemon.json`` file. Useful if you want a custom config differing from the default one in the EKS AMI.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('docker_config_json')

    @builtins.property
    def enable_docker_bridge(self) -> typing.Optional[bool]:
        """Restores the docker default bridge network.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('enable_docker_bridge')

    @builtins.property
    def kubelet_extra_args(self) -> typing.Optional[str]:
        """Extra arguments to add to the kubelet.

        Useful for adding labels or taints.

        default
        :default: - none

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            --node - labelsfoo = bar , goo = far
        """
        return self._values.get('kubelet_extra_args')

    @builtins.property
    def use_max_pods(self) -> typing.Optional[bool]:
        """Sets ``--max-pods`` for the kubelet based on the capacity of the EC2 instance.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('use_max_pods')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BootstrapOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-eks.CapacityOptions", jsii_struct_bases=[aws_cdk.aws_autoscaling.CommonAutoScalingGroupProps], name_mapping={'allow_all_outbound': 'allowAllOutbound', 'associate_public_ip_address': 'associatePublicIpAddress', 'block_devices': 'blockDevices', 'cooldown': 'cooldown', 'desired_capacity': 'desiredCapacity', 'health_check': 'healthCheck', 'ignore_unmodified_size_properties': 'ignoreUnmodifiedSizeProperties', 'instance_monitoring': 'instanceMonitoring', 'key_name': 'keyName', 'max_capacity': 'maxCapacity', 'max_instance_lifetime': 'maxInstanceLifetime', 'min_capacity': 'minCapacity', 'notifications': 'notifications', 'notifications_topic': 'notificationsTopic', 'replacing_update_min_successful_instances_percent': 'replacingUpdateMinSuccessfulInstancesPercent', 'resource_signal_count': 'resourceSignalCount', 'resource_signal_timeout': 'resourceSignalTimeout', 'rolling_update_configuration': 'rollingUpdateConfiguration', 'spot_price': 'spotPrice', 'update_type': 'updateType', 'vpc_subnets': 'vpcSubnets', 'instance_type': 'instanceType', 'bootstrap_enabled': 'bootstrapEnabled', 'bootstrap_options': 'bootstrapOptions', 'machine_image_type': 'machineImageType', 'map_role': 'mapRole'})
class CapacityOptions(aws_cdk.aws_autoscaling.CommonAutoScalingGroupProps):
    def __init__(self, *, allow_all_outbound: typing.Optional[bool]=None, associate_public_ip_address: typing.Optional[bool]=None, block_devices: typing.Optional[typing.List[aws_cdk.aws_autoscaling.BlockDevice]]=None, cooldown: typing.Optional[aws_cdk.core.Duration]=None, desired_capacity: typing.Optional[jsii.Number]=None, health_check: typing.Optional[aws_cdk.aws_autoscaling.HealthCheck]=None, ignore_unmodified_size_properties: typing.Optional[bool]=None, instance_monitoring: typing.Optional[aws_cdk.aws_autoscaling.Monitoring]=None, key_name: typing.Optional[str]=None, max_capacity: typing.Optional[jsii.Number]=None, max_instance_lifetime: typing.Optional[aws_cdk.core.Duration]=None, min_capacity: typing.Optional[jsii.Number]=None, notifications: typing.Optional[typing.List[aws_cdk.aws_autoscaling.NotificationConfiguration]]=None, notifications_topic: typing.Optional[aws_cdk.aws_sns.ITopic]=None, replacing_update_min_successful_instances_percent: typing.Optional[jsii.Number]=None, resource_signal_count: typing.Optional[jsii.Number]=None, resource_signal_timeout: typing.Optional[aws_cdk.core.Duration]=None, rolling_update_configuration: typing.Optional[aws_cdk.aws_autoscaling.RollingUpdateConfiguration]=None, spot_price: typing.Optional[str]=None, update_type: typing.Optional[aws_cdk.aws_autoscaling.UpdateType]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, instance_type: aws_cdk.aws_ec2.InstanceType, bootstrap_enabled: typing.Optional[bool]=None, bootstrap_options: typing.Optional["BootstrapOptions"]=None, machine_image_type: typing.Optional["MachineImageType"]=None, map_role: typing.Optional[bool]=None) -> None:
        """Options for adding worker nodes.

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
        :param instance_type: Instance type of the instances to start.
        :param bootstrap_enabled: Configures the EC2 user-data script for instances in this autoscaling group to bootstrap the node (invoke ``/etc/eks/bootstrap.sh``) and associate it with the EKS cluster. If you wish to provide a custom user data script, set this to ``false`` and manually invoke ``autoscalingGroup.addUserData()``. Default: true
        :param bootstrap_options: EKS node bootstrapping options. Default: - none
        :param machine_image_type: Machine image type. Default: MachineImageType.AMAZON_LINUX_2
        :param map_role: Will automatically update the aws-auth ConfigMap to map the IAM instance role to RBAC. This cannot be explicitly set to ``true`` if the cluster has kubectl disabled. Default: - true if the cluster has kubectl enabled (which is the default).

        stability
        :stability: experimental
        """
        if isinstance(rolling_update_configuration, dict): rolling_update_configuration = aws_cdk.aws_autoscaling.RollingUpdateConfiguration(**rolling_update_configuration)
        if isinstance(vpc_subnets, dict): vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        if isinstance(bootstrap_options, dict): bootstrap_options = BootstrapOptions(**bootstrap_options)
        self._values = {
            'instance_type': instance_type,
        }
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
        if bootstrap_enabled is not None: self._values["bootstrap_enabled"] = bootstrap_enabled
        if bootstrap_options is not None: self._values["bootstrap_options"] = bootstrap_options
        if machine_image_type is not None: self._values["machine_image_type"] = machine_image_type
        if map_role is not None: self._values["map_role"] = map_role

    @builtins.property
    def allow_all_outbound(self) -> typing.Optional[bool]:
        """Whether the instances can initiate connections to anywhere by default.

        default
        :default: true
        """
        return self._values.get('allow_all_outbound')

    @builtins.property
    def associate_public_ip_address(self) -> typing.Optional[bool]:
        """Whether instances in the Auto Scaling Group should have public IP addresses associated with them.

        default
        :default: - Use subnet setting.
        """
        return self._values.get('associate_public_ip_address')

    @builtins.property
    def block_devices(self) -> typing.Optional[typing.List[aws_cdk.aws_autoscaling.BlockDevice]]:
        """Specifies how block devices are exposed to the instance. You can specify virtual devices and EBS volumes.

        Each instance that is launched has an associated root device volume,
        either an Amazon EBS volume or an instance store volume.
        You can use block device mappings to specify additional EBS volumes or
        instance store volumes to attach to an instance when it is launched.

        default
        :default: - Uses the block device mapping of the AMI

        see
        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/block-device-mapping-concepts.html
        """
        return self._values.get('block_devices')

    @builtins.property
    def cooldown(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Default scaling cooldown for this AutoScalingGroup.

        default
        :default: Duration.minutes(5)
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
        """
        return self._values.get('desired_capacity')

    @builtins.property
    def health_check(self) -> typing.Optional[aws_cdk.aws_autoscaling.HealthCheck]:
        """Configuration for health checks.

        default
        :default: - HealthCheck.ec2 with no grace period
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
        """
        return self._values.get('ignore_unmodified_size_properties')

    @builtins.property
    def instance_monitoring(self) -> typing.Optional[aws_cdk.aws_autoscaling.Monitoring]:
        """Controls whether instances in this group are launched with detailed or basic monitoring.

        When detailed monitoring is enabled, Amazon CloudWatch generates metrics every minute and your account
        is charged a fee. When you disable detailed monitoring, CloudWatch generates metrics every 5 minutes.

        default
        :default: - Monitoring.DETAILED

        see
        :see: https://docs.aws.amazon.com/autoscaling/latest/userguide/as-instance-monitoring.html#enable-as-instance-metrics
        """
        return self._values.get('instance_monitoring')

    @builtins.property
    def key_name(self) -> typing.Optional[str]:
        """Name of SSH keypair to grant access to instances.

        default
        :default: - No SSH access will be possible.
        """
        return self._values.get('key_name')

    @builtins.property
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        """Maximum number of instances in the fleet.

        default
        :default: desiredCapacity
        """
        return self._values.get('max_capacity')

    @builtins.property
    def max_instance_lifetime(self) -> typing.Optional[aws_cdk.core.Duration]:
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
        """
        return self._values.get('max_instance_lifetime')

    @builtins.property
    def min_capacity(self) -> typing.Optional[jsii.Number]:
        """Minimum number of instances in the fleet.

        default
        :default: 1
        """
        return self._values.get('min_capacity')

    @builtins.property
    def notifications(self) -> typing.Optional[typing.List[aws_cdk.aws_autoscaling.NotificationConfiguration]]:
        """Configure autoscaling group to send notifications about fleet changes to an SNS topic(s).

        default
        :default: - No fleet change notifications will be sent.

        see
        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-notificationconfigurations
        """
        return self._values.get('notifications')

    @builtins.property
    def notifications_topic(self) -> typing.Optional[aws_cdk.aws_sns.ITopic]:
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
        """
        return self._values.get('replacing_update_min_successful_instances_percent')

    @builtins.property
    def resource_signal_count(self) -> typing.Optional[jsii.Number]:
        """How many ResourceSignal calls CloudFormation expects before the resource is considered created.

        default
        :default: 1
        """
        return self._values.get('resource_signal_count')

    @builtins.property
    def resource_signal_timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The length of time to wait for the resourceSignalCount.

        The maximum value is 43200 (12 hours).

        default
        :default: Duration.minutes(5)
        """
        return self._values.get('resource_signal_timeout')

    @builtins.property
    def rolling_update_configuration(self) -> typing.Optional[aws_cdk.aws_autoscaling.RollingUpdateConfiguration]:
        """Configuration for rolling updates.

        Only used if updateType == UpdateType.RollingUpdate.

        default
        :default: - RollingUpdateConfiguration with defaults.
        """
        return self._values.get('rolling_update_configuration')

    @builtins.property
    def spot_price(self) -> typing.Optional[str]:
        """The maximum hourly price (in USD) to be paid for any Spot Instance launched to fulfill the request.

        Spot Instances are
        launched when the price you specify exceeds the current Spot market price.

        default
        :default: none
        """
        return self._values.get('spot_price')

    @builtins.property
    def update_type(self) -> typing.Optional[aws_cdk.aws_autoscaling.UpdateType]:
        """What to do when an AutoScalingGroup's instance configuration is changed.

        This is applied when any of the settings on the ASG are changed that
        affect how the instances should be created (VPC, instance type, startup
        scripts, etc.). It indicates how the existing instances should be
        replaced with new instances matching the new config. By default, nothing
        is done and only new instances are launched with the new config.

        default
        :default: UpdateType.None
        """
        return self._values.get('update_type')

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """Where to place instances within the VPC.

        default
        :default: - All Private subnets.
        """
        return self._values.get('vpc_subnets')

    @builtins.property
    def instance_type(self) -> aws_cdk.aws_ec2.InstanceType:
        """Instance type of the instances to start.

        stability
        :stability: experimental
        """
        return self._values.get('instance_type')

    @builtins.property
    def bootstrap_enabled(self) -> typing.Optional[bool]:
        """Configures the EC2 user-data script for instances in this autoscaling group to bootstrap the node (invoke ``/etc/eks/bootstrap.sh``) and associate it with the EKS cluster.

        If you wish to provide a custom user data script, set this to ``false`` and
        manually invoke ``autoscalingGroup.addUserData()``.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('bootstrap_enabled')

    @builtins.property
    def bootstrap_options(self) -> typing.Optional["BootstrapOptions"]:
        """EKS node bootstrapping options.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('bootstrap_options')

    @builtins.property
    def machine_image_type(self) -> typing.Optional["MachineImageType"]:
        """Machine image type.

        default
        :default: MachineImageType.AMAZON_LINUX_2

        stability
        :stability: experimental
        """
        return self._values.get('machine_image_type')

    @builtins.property
    def map_role(self) -> typing.Optional[bool]:
        """Will automatically update the aws-auth ConfigMap to map the IAM instance role to RBAC.

        This cannot be explicitly set to ``true`` if the cluster has kubectl disabled.

        default
        :default: - true if the cluster has kubectl enabled (which is the default).

        stability
        :stability: experimental
        """
        return self._values.get('map_role')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CapacityOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnCluster(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-eks.CfnCluster"):
    """A CloudFormation ``AWS::EKS::Cluster``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html
    cloudformationResource:
    :cloudformationResource:: AWS::EKS::Cluster
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, resources_vpc_config: typing.Union["ResourcesVpcConfigProperty", aws_cdk.core.IResolvable], role_arn: str, encryption_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "EncryptionConfigProperty"]]]]=None, name: typing.Optional[str]=None, version: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::EKS::Cluster``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param resources_vpc_config: ``AWS::EKS::Cluster.ResourcesVpcConfig``.
        :param role_arn: ``AWS::EKS::Cluster.RoleArn``.
        :param encryption_config: ``AWS::EKS::Cluster.EncryptionConfig``.
        :param name: ``AWS::EKS::Cluster.Name``.
        :param version: ``AWS::EKS::Cluster.Version``.
        """
        props = CfnClusterProps(resources_vpc_config=resources_vpc_config, role_arn=role_arn, encryption_config=encryption_config, name=name, version=version)

        jsii.create(CfnCluster, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnCluster":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
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
    @jsii.member(jsii_name="attrCertificateAuthorityData")
    def attr_certificate_authority_data(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: CertificateAuthorityData
        """
        return jsii.get(self, "attrCertificateAuthorityData")

    @builtins.property
    @jsii.member(jsii_name="attrClusterSecurityGroupId")
    def attr_cluster_security_group_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ClusterSecurityGroupId
        """
        return jsii.get(self, "attrClusterSecurityGroupId")

    @builtins.property
    @jsii.member(jsii_name="attrEncryptionConfigKeyArn")
    def attr_encryption_config_key_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: EncryptionConfigKeyArn
        """
        return jsii.get(self, "attrEncryptionConfigKeyArn")

    @builtins.property
    @jsii.member(jsii_name="attrEndpoint")
    def attr_endpoint(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Endpoint
        """
        return jsii.get(self, "attrEndpoint")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="resourcesVpcConfig")
    def resources_vpc_config(self) -> typing.Union["ResourcesVpcConfigProperty", aws_cdk.core.IResolvable]:
        """``AWS::EKS::Cluster.ResourcesVpcConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-resourcesvpcconfig
        """
        return jsii.get(self, "resourcesVpcConfig")

    @resources_vpc_config.setter
    def resources_vpc_config(self, value: typing.Union["ResourcesVpcConfigProperty", aws_cdk.core.IResolvable]) -> None:
        jsii.set(self, "resourcesVpcConfig", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> str:
        """``AWS::EKS::Cluster.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-rolearn
        """
        return jsii.get(self, "roleArn")

    @role_arn.setter
    def role_arn(self, value: str) -> None:
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="encryptionConfig")
    def encryption_config(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "EncryptionConfigProperty"]]]]:
        """``AWS::EKS::Cluster.EncryptionConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-encryptionconfig
        """
        return jsii.get(self, "encryptionConfig")

    @encryption_config.setter
    def encryption_config(self, value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "EncryptionConfigProperty"]]]]) -> None:
        jsii.set(self, "encryptionConfig", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::EKS::Cluster.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> typing.Optional[str]:
        """``AWS::EKS::Cluster.Version``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-version
        """
        return jsii.get(self, "version")

    @version.setter
    def version(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "version", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-eks.CfnCluster.EncryptionConfigProperty", jsii_struct_bases=[], name_mapping={'provider': 'provider', 'resources': 'resources'})
    class EncryptionConfigProperty():
        def __init__(self, *, provider: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCluster.ProviderProperty"]]=None, resources: typing.Optional[typing.List[str]]=None) -> None:
            """
            :param provider: ``CfnCluster.EncryptionConfigProperty.Provider``.
            :param resources: ``CfnCluster.EncryptionConfigProperty.Resources``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-encryptionconfig.html
            """
            self._values = {
            }
            if provider is not None: self._values["provider"] = provider
            if resources is not None: self._values["resources"] = resources

        @builtins.property
        def provider(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCluster.ProviderProperty"]]:
            """``CfnCluster.EncryptionConfigProperty.Provider``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-encryptionconfig.html#cfn-eks-cluster-encryptionconfig-provider
            """
            return self._values.get('provider')

        @builtins.property
        def resources(self) -> typing.Optional[typing.List[str]]:
            """``CfnCluster.EncryptionConfigProperty.Resources``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-encryptionconfig.html#cfn-eks-cluster-encryptionconfig-resources
            """
            return self._values.get('resources')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'EncryptionConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-eks.CfnCluster.ProviderProperty", jsii_struct_bases=[], name_mapping={'key_arn': 'keyArn'})
    class ProviderProperty():
        def __init__(self, *, key_arn: typing.Optional[str]=None) -> None:
            """
            :param key_arn: ``CfnCluster.ProviderProperty.KeyArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-provider.html
            """
            self._values = {
            }
            if key_arn is not None: self._values["key_arn"] = key_arn

        @builtins.property
        def key_arn(self) -> typing.Optional[str]:
            """``CfnCluster.ProviderProperty.KeyArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-provider.html#cfn-eks-cluster-provider-keyarn
            """
            return self._values.get('key_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ProviderProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-eks.CfnCluster.ResourcesVpcConfigProperty", jsii_struct_bases=[], name_mapping={'subnet_ids': 'subnetIds', 'security_group_ids': 'securityGroupIds'})
    class ResourcesVpcConfigProperty():
        def __init__(self, *, subnet_ids: typing.List[str], security_group_ids: typing.Optional[typing.List[str]]=None) -> None:
            """
            :param subnet_ids: ``CfnCluster.ResourcesVpcConfigProperty.SubnetIds``.
            :param security_group_ids: ``CfnCluster.ResourcesVpcConfigProperty.SecurityGroupIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-resourcesvpcconfig.html
            """
            self._values = {
                'subnet_ids': subnet_ids,
            }
            if security_group_ids is not None: self._values["security_group_ids"] = security_group_ids

        @builtins.property
        def subnet_ids(self) -> typing.List[str]:
            """``CfnCluster.ResourcesVpcConfigProperty.SubnetIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-resourcesvpcconfig.html#cfn-eks-cluster-resourcesvpcconfig-subnetids
            """
            return self._values.get('subnet_ids')

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[str]]:
            """``CfnCluster.ResourcesVpcConfigProperty.SecurityGroupIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-resourcesvpcconfig.html#cfn-eks-cluster-resourcesvpcconfig-securitygroupids
            """
            return self._values.get('security_group_ids')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ResourcesVpcConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-eks.CfnClusterProps", jsii_struct_bases=[], name_mapping={'resources_vpc_config': 'resourcesVpcConfig', 'role_arn': 'roleArn', 'encryption_config': 'encryptionConfig', 'name': 'name', 'version': 'version'})
class CfnClusterProps():
    def __init__(self, *, resources_vpc_config: typing.Union["CfnCluster.ResourcesVpcConfigProperty", aws_cdk.core.IResolvable], role_arn: str, encryption_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnCluster.EncryptionConfigProperty"]]]]=None, name: typing.Optional[str]=None, version: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::EKS::Cluster``.

        :param resources_vpc_config: ``AWS::EKS::Cluster.ResourcesVpcConfig``.
        :param role_arn: ``AWS::EKS::Cluster.RoleArn``.
        :param encryption_config: ``AWS::EKS::Cluster.EncryptionConfig``.
        :param name: ``AWS::EKS::Cluster.Name``.
        :param version: ``AWS::EKS::Cluster.Version``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html
        """
        self._values = {
            'resources_vpc_config': resources_vpc_config,
            'role_arn': role_arn,
        }
        if encryption_config is not None: self._values["encryption_config"] = encryption_config
        if name is not None: self._values["name"] = name
        if version is not None: self._values["version"] = version

    @builtins.property
    def resources_vpc_config(self) -> typing.Union["CfnCluster.ResourcesVpcConfigProperty", aws_cdk.core.IResolvable]:
        """``AWS::EKS::Cluster.ResourcesVpcConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-resourcesvpcconfig
        """
        return self._values.get('resources_vpc_config')

    @builtins.property
    def role_arn(self) -> str:
        """``AWS::EKS::Cluster.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-rolearn
        """
        return self._values.get('role_arn')

    @builtins.property
    def encryption_config(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnCluster.EncryptionConfigProperty"]]]]:
        """``AWS::EKS::Cluster.EncryptionConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-encryptionconfig
        """
        return self._values.get('encryption_config')

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """``AWS::EKS::Cluster.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-name
        """
        return self._values.get('name')

    @builtins.property
    def version(self) -> typing.Optional[str]:
        """``AWS::EKS::Cluster.Version``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-version
        """
        return self._values.get('version')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnClusterProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnNodegroup(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-eks.CfnNodegroup"):
    """A CloudFormation ``AWS::EKS::Nodegroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html
    cloudformationResource:
    :cloudformationResource:: AWS::EKS::Nodegroup
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, cluster_name: str, node_role: str, subnets: typing.List[str], ami_type: typing.Optional[str]=None, disk_size: typing.Optional[jsii.Number]=None, force_update_enabled: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]=None, instance_types: typing.Optional[typing.List[str]]=None, labels: typing.Any=None, nodegroup_name: typing.Optional[str]=None, release_version: typing.Optional[str]=None, remote_access: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "RemoteAccessProperty"]]=None, scaling_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "ScalingConfigProperty"]]=None, tags: typing.Any=None, version: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::EKS::Nodegroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param cluster_name: ``AWS::EKS::Nodegroup.ClusterName``.
        :param node_role: ``AWS::EKS::Nodegroup.NodeRole``.
        :param subnets: ``AWS::EKS::Nodegroup.Subnets``.
        :param ami_type: ``AWS::EKS::Nodegroup.AmiType``.
        :param disk_size: ``AWS::EKS::Nodegroup.DiskSize``.
        :param force_update_enabled: ``AWS::EKS::Nodegroup.ForceUpdateEnabled``.
        :param instance_types: ``AWS::EKS::Nodegroup.InstanceTypes``.
        :param labels: ``AWS::EKS::Nodegroup.Labels``.
        :param nodegroup_name: ``AWS::EKS::Nodegroup.NodegroupName``.
        :param release_version: ``AWS::EKS::Nodegroup.ReleaseVersion``.
        :param remote_access: ``AWS::EKS::Nodegroup.RemoteAccess``.
        :param scaling_config: ``AWS::EKS::Nodegroup.ScalingConfig``.
        :param tags: ``AWS::EKS::Nodegroup.Tags``.
        :param version: ``AWS::EKS::Nodegroup.Version``.
        """
        props = CfnNodegroupProps(cluster_name=cluster_name, node_role=node_role, subnets=subnets, ami_type=ami_type, disk_size=disk_size, force_update_enabled=force_update_enabled, instance_types=instance_types, labels=labels, nodegroup_name=nodegroup_name, release_version=release_version, remote_access=remote_access, scaling_config=scaling_config, tags=tags, version=version)

        jsii.create(CfnNodegroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnNodegroup":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
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
    @jsii.member(jsii_name="attrClusterName")
    def attr_cluster_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ClusterName
        """
        return jsii.get(self, "attrClusterName")

    @builtins.property
    @jsii.member(jsii_name="attrNodegroupName")
    def attr_nodegroup_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: NodegroupName
        """
        return jsii.get(self, "attrNodegroupName")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::EKS::Nodegroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        """``AWS::EKS::Nodegroup.ClusterName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-clustername
        """
        return jsii.get(self, "clusterName")

    @cluster_name.setter
    def cluster_name(self, value: str) -> None:
        jsii.set(self, "clusterName", value)

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Any:
        """``AWS::EKS::Nodegroup.Labels``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-labels
        """
        return jsii.get(self, "labels")

    @labels.setter
    def labels(self, value: typing.Any) -> None:
        jsii.set(self, "labels", value)

    @builtins.property
    @jsii.member(jsii_name="nodeRole")
    def node_role(self) -> str:
        """``AWS::EKS::Nodegroup.NodeRole``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-noderole
        """
        return jsii.get(self, "nodeRole")

    @node_role.setter
    def node_role(self, value: str) -> None:
        jsii.set(self, "nodeRole", value)

    @builtins.property
    @jsii.member(jsii_name="subnets")
    def subnets(self) -> typing.List[str]:
        """``AWS::EKS::Nodegroup.Subnets``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-subnets
        """
        return jsii.get(self, "subnets")

    @subnets.setter
    def subnets(self, value: typing.List[str]) -> None:
        jsii.set(self, "subnets", value)

    @builtins.property
    @jsii.member(jsii_name="amiType")
    def ami_type(self) -> typing.Optional[str]:
        """``AWS::EKS::Nodegroup.AmiType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-amitype
        """
        return jsii.get(self, "amiType")

    @ami_type.setter
    def ami_type(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "amiType", value)

    @builtins.property
    @jsii.member(jsii_name="diskSize")
    def disk_size(self) -> typing.Optional[jsii.Number]:
        """``AWS::EKS::Nodegroup.DiskSize``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-disksize
        """
        return jsii.get(self, "diskSize")

    @disk_size.setter
    def disk_size(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "diskSize", value)

    @builtins.property
    @jsii.member(jsii_name="forceUpdateEnabled")
    def force_update_enabled(self) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
        """``AWS::EKS::Nodegroup.ForceUpdateEnabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-forceupdateenabled
        """
        return jsii.get(self, "forceUpdateEnabled")

    @force_update_enabled.setter
    def force_update_enabled(self, value: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]) -> None:
        jsii.set(self, "forceUpdateEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="instanceTypes")
    def instance_types(self) -> typing.Optional[typing.List[str]]:
        """``AWS::EKS::Nodegroup.InstanceTypes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-instancetypes
        """
        return jsii.get(self, "instanceTypes")

    @instance_types.setter
    def instance_types(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "instanceTypes", value)

    @builtins.property
    @jsii.member(jsii_name="nodegroupName")
    def nodegroup_name(self) -> typing.Optional[str]:
        """``AWS::EKS::Nodegroup.NodegroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-nodegroupname
        """
        return jsii.get(self, "nodegroupName")

    @nodegroup_name.setter
    def nodegroup_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "nodegroupName", value)

    @builtins.property
    @jsii.member(jsii_name="releaseVersion")
    def release_version(self) -> typing.Optional[str]:
        """``AWS::EKS::Nodegroup.ReleaseVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-releaseversion
        """
        return jsii.get(self, "releaseVersion")

    @release_version.setter
    def release_version(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "releaseVersion", value)

    @builtins.property
    @jsii.member(jsii_name="remoteAccess")
    def remote_access(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "RemoteAccessProperty"]]:
        """``AWS::EKS::Nodegroup.RemoteAccess``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-remoteaccess
        """
        return jsii.get(self, "remoteAccess")

    @remote_access.setter
    def remote_access(self, value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "RemoteAccessProperty"]]) -> None:
        jsii.set(self, "remoteAccess", value)

    @builtins.property
    @jsii.member(jsii_name="scalingConfig")
    def scaling_config(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "ScalingConfigProperty"]]:
        """``AWS::EKS::Nodegroup.ScalingConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-scalingconfig
        """
        return jsii.get(self, "scalingConfig")

    @scaling_config.setter
    def scaling_config(self, value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "ScalingConfigProperty"]]) -> None:
        jsii.set(self, "scalingConfig", value)

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> typing.Optional[str]:
        """``AWS::EKS::Nodegroup.Version``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-version
        """
        return jsii.get(self, "version")

    @version.setter
    def version(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "version", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-eks.CfnNodegroup.RemoteAccessProperty", jsii_struct_bases=[], name_mapping={'ec2_ssh_key': 'ec2SshKey', 'source_security_groups': 'sourceSecurityGroups'})
    class RemoteAccessProperty():
        def __init__(self, *, ec2_ssh_key: str, source_security_groups: typing.Optional[typing.List[str]]=None) -> None:
            """
            :param ec2_ssh_key: ``CfnNodegroup.RemoteAccessProperty.Ec2SshKey``.
            :param source_security_groups: ``CfnNodegroup.RemoteAccessProperty.SourceSecurityGroups``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-remoteaccess.html
            """
            self._values = {
                'ec2_ssh_key': ec2_ssh_key,
            }
            if source_security_groups is not None: self._values["source_security_groups"] = source_security_groups

        @builtins.property
        def ec2_ssh_key(self) -> str:
            """``CfnNodegroup.RemoteAccessProperty.Ec2SshKey``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-remoteaccess.html#cfn-eks-nodegroup-remoteaccess-ec2sshkey
            """
            return self._values.get('ec2_ssh_key')

        @builtins.property
        def source_security_groups(self) -> typing.Optional[typing.List[str]]:
            """``CfnNodegroup.RemoteAccessProperty.SourceSecurityGroups``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-remoteaccess.html#cfn-eks-nodegroup-remoteaccess-sourcesecuritygroups
            """
            return self._values.get('source_security_groups')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'RemoteAccessProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-eks.CfnNodegroup.ScalingConfigProperty", jsii_struct_bases=[], name_mapping={'desired_size': 'desiredSize', 'max_size': 'maxSize', 'min_size': 'minSize'})
    class ScalingConfigProperty():
        def __init__(self, *, desired_size: typing.Optional[jsii.Number]=None, max_size: typing.Optional[jsii.Number]=None, min_size: typing.Optional[jsii.Number]=None) -> None:
            """
            :param desired_size: ``CfnNodegroup.ScalingConfigProperty.DesiredSize``.
            :param max_size: ``CfnNodegroup.ScalingConfigProperty.MaxSize``.
            :param min_size: ``CfnNodegroup.ScalingConfigProperty.MinSize``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-scalingconfig.html
            """
            self._values = {
            }
            if desired_size is not None: self._values["desired_size"] = desired_size
            if max_size is not None: self._values["max_size"] = max_size
            if min_size is not None: self._values["min_size"] = min_size

        @builtins.property
        def desired_size(self) -> typing.Optional[jsii.Number]:
            """``CfnNodegroup.ScalingConfigProperty.DesiredSize``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-scalingconfig.html#cfn-eks-nodegroup-scalingconfig-desiredsize
            """
            return self._values.get('desired_size')

        @builtins.property
        def max_size(self) -> typing.Optional[jsii.Number]:
            """``CfnNodegroup.ScalingConfigProperty.MaxSize``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-scalingconfig.html#cfn-eks-nodegroup-scalingconfig-maxsize
            """
            return self._values.get('max_size')

        @builtins.property
        def min_size(self) -> typing.Optional[jsii.Number]:
            """``CfnNodegroup.ScalingConfigProperty.MinSize``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-scalingconfig.html#cfn-eks-nodegroup-scalingconfig-minsize
            """
            return self._values.get('min_size')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ScalingConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-eks.CfnNodegroupProps", jsii_struct_bases=[], name_mapping={'cluster_name': 'clusterName', 'node_role': 'nodeRole', 'subnets': 'subnets', 'ami_type': 'amiType', 'disk_size': 'diskSize', 'force_update_enabled': 'forceUpdateEnabled', 'instance_types': 'instanceTypes', 'labels': 'labels', 'nodegroup_name': 'nodegroupName', 'release_version': 'releaseVersion', 'remote_access': 'remoteAccess', 'scaling_config': 'scalingConfig', 'tags': 'tags', 'version': 'version'})
class CfnNodegroupProps():
    def __init__(self, *, cluster_name: str, node_role: str, subnets: typing.List[str], ami_type: typing.Optional[str]=None, disk_size: typing.Optional[jsii.Number]=None, force_update_enabled: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]=None, instance_types: typing.Optional[typing.List[str]]=None, labels: typing.Any=None, nodegroup_name: typing.Optional[str]=None, release_version: typing.Optional[str]=None, remote_access: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnNodegroup.RemoteAccessProperty"]]=None, scaling_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnNodegroup.ScalingConfigProperty"]]=None, tags: typing.Any=None, version: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::EKS::Nodegroup``.

        :param cluster_name: ``AWS::EKS::Nodegroup.ClusterName``.
        :param node_role: ``AWS::EKS::Nodegroup.NodeRole``.
        :param subnets: ``AWS::EKS::Nodegroup.Subnets``.
        :param ami_type: ``AWS::EKS::Nodegroup.AmiType``.
        :param disk_size: ``AWS::EKS::Nodegroup.DiskSize``.
        :param force_update_enabled: ``AWS::EKS::Nodegroup.ForceUpdateEnabled``.
        :param instance_types: ``AWS::EKS::Nodegroup.InstanceTypes``.
        :param labels: ``AWS::EKS::Nodegroup.Labels``.
        :param nodegroup_name: ``AWS::EKS::Nodegroup.NodegroupName``.
        :param release_version: ``AWS::EKS::Nodegroup.ReleaseVersion``.
        :param remote_access: ``AWS::EKS::Nodegroup.RemoteAccess``.
        :param scaling_config: ``AWS::EKS::Nodegroup.ScalingConfig``.
        :param tags: ``AWS::EKS::Nodegroup.Tags``.
        :param version: ``AWS::EKS::Nodegroup.Version``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html
        """
        self._values = {
            'cluster_name': cluster_name,
            'node_role': node_role,
            'subnets': subnets,
        }
        if ami_type is not None: self._values["ami_type"] = ami_type
        if disk_size is not None: self._values["disk_size"] = disk_size
        if force_update_enabled is not None: self._values["force_update_enabled"] = force_update_enabled
        if instance_types is not None: self._values["instance_types"] = instance_types
        if labels is not None: self._values["labels"] = labels
        if nodegroup_name is not None: self._values["nodegroup_name"] = nodegroup_name
        if release_version is not None: self._values["release_version"] = release_version
        if remote_access is not None: self._values["remote_access"] = remote_access
        if scaling_config is not None: self._values["scaling_config"] = scaling_config
        if tags is not None: self._values["tags"] = tags
        if version is not None: self._values["version"] = version

    @builtins.property
    def cluster_name(self) -> str:
        """``AWS::EKS::Nodegroup.ClusterName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-clustername
        """
        return self._values.get('cluster_name')

    @builtins.property
    def node_role(self) -> str:
        """``AWS::EKS::Nodegroup.NodeRole``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-noderole
        """
        return self._values.get('node_role')

    @builtins.property
    def subnets(self) -> typing.List[str]:
        """``AWS::EKS::Nodegroup.Subnets``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-subnets
        """
        return self._values.get('subnets')

    @builtins.property
    def ami_type(self) -> typing.Optional[str]:
        """``AWS::EKS::Nodegroup.AmiType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-amitype
        """
        return self._values.get('ami_type')

    @builtins.property
    def disk_size(self) -> typing.Optional[jsii.Number]:
        """``AWS::EKS::Nodegroup.DiskSize``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-disksize
        """
        return self._values.get('disk_size')

    @builtins.property
    def force_update_enabled(self) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
        """``AWS::EKS::Nodegroup.ForceUpdateEnabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-forceupdateenabled
        """
        return self._values.get('force_update_enabled')

    @builtins.property
    def instance_types(self) -> typing.Optional[typing.List[str]]:
        """``AWS::EKS::Nodegroup.InstanceTypes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-instancetypes
        """
        return self._values.get('instance_types')

    @builtins.property
    def labels(self) -> typing.Any:
        """``AWS::EKS::Nodegroup.Labels``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-labels
        """
        return self._values.get('labels')

    @builtins.property
    def nodegroup_name(self) -> typing.Optional[str]:
        """``AWS::EKS::Nodegroup.NodegroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-nodegroupname
        """
        return self._values.get('nodegroup_name')

    @builtins.property
    def release_version(self) -> typing.Optional[str]:
        """``AWS::EKS::Nodegroup.ReleaseVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-releaseversion
        """
        return self._values.get('release_version')

    @builtins.property
    def remote_access(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnNodegroup.RemoteAccessProperty"]]:
        """``AWS::EKS::Nodegroup.RemoteAccess``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-remoteaccess
        """
        return self._values.get('remote_access')

    @builtins.property
    def scaling_config(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnNodegroup.ScalingConfigProperty"]]:
        """``AWS::EKS::Nodegroup.ScalingConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-scalingconfig
        """
        return self._values.get('scaling_config')

    @builtins.property
    def tags(self) -> typing.Any:
        """``AWS::EKS::Nodegroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-tags
        """
        return self._values.get('tags')

    @builtins.property
    def version(self) -> typing.Optional[str]:
        """``AWS::EKS::Nodegroup.Version``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-version
        """
        return self._values.get('version')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnNodegroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-eks.ClusterAttributes", jsii_struct_bases=[], name_mapping={'cluster_arn': 'clusterArn', 'cluster_certificate_authority_data': 'clusterCertificateAuthorityData', 'cluster_encryption_config_key_arn': 'clusterEncryptionConfigKeyArn', 'cluster_endpoint': 'clusterEndpoint', 'cluster_name': 'clusterName', 'cluster_security_group_id': 'clusterSecurityGroupId', 'security_groups': 'securityGroups', 'vpc': 'vpc'})
class ClusterAttributes():
    def __init__(self, *, cluster_arn: str, cluster_certificate_authority_data: str, cluster_encryption_config_key_arn: str, cluster_endpoint: str, cluster_name: str, cluster_security_group_id: str, security_groups: typing.List[aws_cdk.aws_ec2.ISecurityGroup], vpc: aws_cdk.aws_ec2.IVpc) -> None:
        """Attributes for EKS clusters.

        :param cluster_arn: The unique ARN assigned to the service by AWS in the form of arn:aws:eks:.
        :param cluster_certificate_authority_data: The certificate-authority-data for your cluster.
        :param cluster_encryption_config_key_arn: Amazon Resource Name (ARN) or alias of the customer master key (CMK).
        :param cluster_endpoint: The API Server endpoint URL.
        :param cluster_name: The physical name of the Cluster.
        :param cluster_security_group_id: The cluster security group that was created by Amazon EKS for the cluster.
        :param security_groups: The security groups associated with this cluster.
        :param vpc: The VPC in which this Cluster was created.

        stability
        :stability: experimental
        """
        self._values = {
            'cluster_arn': cluster_arn,
            'cluster_certificate_authority_data': cluster_certificate_authority_data,
            'cluster_encryption_config_key_arn': cluster_encryption_config_key_arn,
            'cluster_endpoint': cluster_endpoint,
            'cluster_name': cluster_name,
            'cluster_security_group_id': cluster_security_group_id,
            'security_groups': security_groups,
            'vpc': vpc,
        }

    @builtins.property
    def cluster_arn(self) -> str:
        """The unique ARN assigned to the service by AWS in the form of arn:aws:eks:.

        stability
        :stability: experimental
        """
        return self._values.get('cluster_arn')

    @builtins.property
    def cluster_certificate_authority_data(self) -> str:
        """The certificate-authority-data for your cluster.

        stability
        :stability: experimental
        """
        return self._values.get('cluster_certificate_authority_data')

    @builtins.property
    def cluster_encryption_config_key_arn(self) -> str:
        """Amazon Resource Name (ARN) or alias of the customer master key (CMK).

        stability
        :stability: experimental
        """
        return self._values.get('cluster_encryption_config_key_arn')

    @builtins.property
    def cluster_endpoint(self) -> str:
        """The API Server endpoint URL.

        stability
        :stability: experimental
        """
        return self._values.get('cluster_endpoint')

    @builtins.property
    def cluster_name(self) -> str:
        """The physical name of the Cluster.

        stability
        :stability: experimental
        """
        return self._values.get('cluster_name')

    @builtins.property
    def cluster_security_group_id(self) -> str:
        """The cluster security group that was created by Amazon EKS for the cluster.

        stability
        :stability: experimental
        """
        return self._values.get('cluster_security_group_id')

    @builtins.property
    def security_groups(self) -> typing.List[aws_cdk.aws_ec2.ISecurityGroup]:
        """The security groups associated with this cluster.

        stability
        :stability: experimental
        """
        return self._values.get('security_groups')

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """The VPC in which this Cluster was created.

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ClusterAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-eks.ClusterOptions", jsii_struct_bases=[], name_mapping={'cluster_name': 'clusterName', 'core_dns_compute_type': 'coreDnsComputeType', 'masters_role': 'mastersRole', 'output_cluster_name': 'outputClusterName', 'output_config_command': 'outputConfigCommand', 'output_masters_role_arn': 'outputMastersRoleArn', 'role': 'role', 'security_group': 'securityGroup', 'version': 'version', 'vpc': 'vpc', 'vpc_subnets': 'vpcSubnets'})
class ClusterOptions():
    def __init__(self, *, cluster_name: typing.Optional[str]=None, core_dns_compute_type: typing.Optional["CoreDnsComputeType"]=None, masters_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, output_cluster_name: typing.Optional[bool]=None, output_config_command: typing.Optional[bool]=None, output_masters_role_arn: typing.Optional[bool]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None, version: typing.Optional[str]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None, vpc_subnets: typing.Optional[typing.List[aws_cdk.aws_ec2.SubnetSelection]]=None) -> None:
        """Options for configuring an EKS cluster.

        :param cluster_name: Name for the cluster. Default: - Automatically generated name
        :param core_dns_compute_type: Controls the "eks.amazonaws.com/compute-type" annotation in the CoreDNS configuration on your cluster to determine which compute type to use for CoreDNS. Default: CoreDnsComputeType.EC2 (for ``FargateCluster`` the default is FARGATE)
        :param masters_role: An IAM role that will be added to the ``system:masters`` Kubernetes RBAC group. Default: - By default, it will only possible to update this Kubernetes system by adding resources to this cluster via ``addResource`` or by defining ``KubernetesResource`` resources in your AWS CDK app. Use this if you wish to grant cluster administration privileges to another role.
        :param output_cluster_name: Determines whether a CloudFormation output with the name of the cluster will be synthesized. Default: false
        :param output_config_command: Determines whether a CloudFormation output with the ``aws eks update-kubeconfig`` command will be synthesized. This command will include the cluster name and, if applicable, the ARN of the masters IAM role. Default: true
        :param output_masters_role_arn: Determines whether a CloudFormation output with the ARN of the "masters" IAM role will be synthesized (if ``mastersRole`` is specified). Default: false
        :param role: Role that provides permissions for the Kubernetes control plane to make calls to AWS API operations on your behalf. Default: - A role is automatically created for you
        :param security_group: Security Group to use for Control Plane ENIs. Default: - A security group is automatically created
        :param version: The Kubernetes version to run in the cluster. Default: - If not supplied, will use Amazon default version
        :param vpc: The VPC in which to create the Cluster. Default: - a VPC with default configuration will be created and can be accessed through ``cluster.vpc``.
        :param vpc_subnets: Where to place EKS Control Plane ENIs. If you want to create public load balancers, this must include public subnets. For example, to only select private subnets, supply the following:: vpcSubnets: [ { subnetType: ec2.SubnetType.Private } ] Default: - All public and private subnets

        stability
        :stability: experimental
        """
        self._values = {
        }
        if cluster_name is not None: self._values["cluster_name"] = cluster_name
        if core_dns_compute_type is not None: self._values["core_dns_compute_type"] = core_dns_compute_type
        if masters_role is not None: self._values["masters_role"] = masters_role
        if output_cluster_name is not None: self._values["output_cluster_name"] = output_cluster_name
        if output_config_command is not None: self._values["output_config_command"] = output_config_command
        if output_masters_role_arn is not None: self._values["output_masters_role_arn"] = output_masters_role_arn
        if role is not None: self._values["role"] = role
        if security_group is not None: self._values["security_group"] = security_group
        if version is not None: self._values["version"] = version
        if vpc is not None: self._values["vpc"] = vpc
        if vpc_subnets is not None: self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def cluster_name(self) -> typing.Optional[str]:
        """Name for the cluster.

        default
        :default: - Automatically generated name

        stability
        :stability: experimental
        """
        return self._values.get('cluster_name')

    @builtins.property
    def core_dns_compute_type(self) -> typing.Optional["CoreDnsComputeType"]:
        """Controls the "eks.amazonaws.com/compute-type" annotation in the CoreDNS configuration on your cluster to determine which compute type to use for CoreDNS.

        default
        :default: CoreDnsComputeType.EC2 (for ``FargateCluster`` the default is FARGATE)

        stability
        :stability: experimental
        """
        return self._values.get('core_dns_compute_type')

    @builtins.property
    def masters_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """An IAM role that will be added to the ``system:masters`` Kubernetes RBAC group.

        default
        :default:

        - By default, it will only possible to update this Kubernetes
          system by adding resources to this cluster via ``addResource`` or
          by defining ``KubernetesResource`` resources in your AWS CDK app.
          Use this if you wish to grant cluster administration privileges
          to another role.

        see
        :see: https://kubernetes.io/docs/reference/access-authn-authz/rbac/#default-roles-and-role-bindings
        stability
        :stability: experimental
        """
        return self._values.get('masters_role')

    @builtins.property
    def output_cluster_name(self) -> typing.Optional[bool]:
        """Determines whether a CloudFormation output with the name of the cluster will be synthesized.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('output_cluster_name')

    @builtins.property
    def output_config_command(self) -> typing.Optional[bool]:
        """Determines whether a CloudFormation output with the ``aws eks update-kubeconfig`` command will be synthesized.

        This command will include
        the cluster name and, if applicable, the ARN of the masters IAM role.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('output_config_command')

    @builtins.property
    def output_masters_role_arn(self) -> typing.Optional[bool]:
        """Determines whether a CloudFormation output with the ARN of the "masters" IAM role will be synthesized (if ``mastersRole`` is specified).

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('output_masters_role_arn')

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """Role that provides permissions for the Kubernetes control plane to make calls to AWS API operations on your behalf.

        default
        :default: - A role is automatically created for you

        stability
        :stability: experimental
        """
        return self._values.get('role')

    @builtins.property
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        """Security Group to use for Control Plane ENIs.

        default
        :default: - A security group is automatically created

        stability
        :stability: experimental
        """
        return self._values.get('security_group')

    @builtins.property
    def version(self) -> typing.Optional[str]:
        """The Kubernetes version to run in the cluster.

        default
        :default: - If not supplied, will use Amazon default version

        stability
        :stability: experimental
        """
        return self._values.get('version')

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC in which to create the Cluster.

        default
        :default: - a VPC with default configuration will be created and can be accessed through ``cluster.vpc``.

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[typing.List[aws_cdk.aws_ec2.SubnetSelection]]:
        """Where to place EKS Control Plane ENIs.

        If you want to create public load balancers, this must include public subnets.

        For example, to only select private subnets, supply the following::

           # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
           vpcSubnets: [
              { subnetType: ec2.SubnetType.Private }
           ]

        default
        :default: - All public and private subnets

        stability
        :stability: experimental
        """
        return self._values.get('vpc_subnets')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ClusterOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-eks.ClusterProps", jsii_struct_bases=[ClusterOptions], name_mapping={'cluster_name': 'clusterName', 'core_dns_compute_type': 'coreDnsComputeType', 'masters_role': 'mastersRole', 'output_cluster_name': 'outputClusterName', 'output_config_command': 'outputConfigCommand', 'output_masters_role_arn': 'outputMastersRoleArn', 'role': 'role', 'security_group': 'securityGroup', 'version': 'version', 'vpc': 'vpc', 'vpc_subnets': 'vpcSubnets', 'default_capacity': 'defaultCapacity', 'default_capacity_instance': 'defaultCapacityInstance', 'default_capacity_type': 'defaultCapacityType', 'kubectl_enabled': 'kubectlEnabled'})
class ClusterProps(ClusterOptions):
    def __init__(self, *, cluster_name: typing.Optional[str]=None, core_dns_compute_type: typing.Optional["CoreDnsComputeType"]=None, masters_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, output_cluster_name: typing.Optional[bool]=None, output_config_command: typing.Optional[bool]=None, output_masters_role_arn: typing.Optional[bool]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None, version: typing.Optional[str]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None, vpc_subnets: typing.Optional[typing.List[aws_cdk.aws_ec2.SubnetSelection]]=None, default_capacity: typing.Optional[jsii.Number]=None, default_capacity_instance: typing.Optional[aws_cdk.aws_ec2.InstanceType]=None, default_capacity_type: typing.Optional["DefaultCapacityType"]=None, kubectl_enabled: typing.Optional[bool]=None) -> None:
        """Configuration props for EKS clusters.

        :param cluster_name: Name for the cluster. Default: - Automatically generated name
        :param core_dns_compute_type: Controls the "eks.amazonaws.com/compute-type" annotation in the CoreDNS configuration on your cluster to determine which compute type to use for CoreDNS. Default: CoreDnsComputeType.EC2 (for ``FargateCluster`` the default is FARGATE)
        :param masters_role: An IAM role that will be added to the ``system:masters`` Kubernetes RBAC group. Default: - By default, it will only possible to update this Kubernetes system by adding resources to this cluster via ``addResource`` or by defining ``KubernetesResource`` resources in your AWS CDK app. Use this if you wish to grant cluster administration privileges to another role.
        :param output_cluster_name: Determines whether a CloudFormation output with the name of the cluster will be synthesized. Default: false
        :param output_config_command: Determines whether a CloudFormation output with the ``aws eks update-kubeconfig`` command will be synthesized. This command will include the cluster name and, if applicable, the ARN of the masters IAM role. Default: true
        :param output_masters_role_arn: Determines whether a CloudFormation output with the ARN of the "masters" IAM role will be synthesized (if ``mastersRole`` is specified). Default: false
        :param role: Role that provides permissions for the Kubernetes control plane to make calls to AWS API operations on your behalf. Default: - A role is automatically created for you
        :param security_group: Security Group to use for Control Plane ENIs. Default: - A security group is automatically created
        :param version: The Kubernetes version to run in the cluster. Default: - If not supplied, will use Amazon default version
        :param vpc: The VPC in which to create the Cluster. Default: - a VPC with default configuration will be created and can be accessed through ``cluster.vpc``.
        :param vpc_subnets: Where to place EKS Control Plane ENIs. If you want to create public load balancers, this must include public subnets. For example, to only select private subnets, supply the following:: vpcSubnets: [ { subnetType: ec2.SubnetType.Private } ] Default: - All public and private subnets
        :param default_capacity: Number of instances to allocate as an initial capacity for this cluster. Instance type can be configured through ``defaultCapacityInstanceType``, which defaults to ``m5.large``. Use ``cluster.addCapacity`` to add additional customized capacity. Set this to ``0`` is you wish to avoid the initial capacity allocation. Default: 2
        :param default_capacity_instance: The instance type to use for the default capacity. This will only be taken into account if ``defaultCapacity`` is > 0. Default: m5.large
        :param default_capacity_type: The default capacity type for the cluster. Default: NODEGROUP
        :param kubectl_enabled: Allows defining ``kubectrl``-related resources on this cluster. If this is disabled, it will not be possible to use the following capabilities: - ``addResource`` - ``addRoleMapping`` - ``addUserMapping`` - ``addMastersRole`` and ``props.mastersRole`` If this is disabled, the cluster can only be managed by issuing ``kubectl`` commands from a session that uses the IAM role/user that created the account. *NOTE*: changing this value will destoy the cluster. This is because a managable cluster must be created using an AWS CloudFormation custom resource which executes with an IAM role owned by the CDK app. Default: true The cluster can be managed by the AWS CDK application.

        stability
        :stability: experimental
        """
        self._values = {
        }
        if cluster_name is not None: self._values["cluster_name"] = cluster_name
        if core_dns_compute_type is not None: self._values["core_dns_compute_type"] = core_dns_compute_type
        if masters_role is not None: self._values["masters_role"] = masters_role
        if output_cluster_name is not None: self._values["output_cluster_name"] = output_cluster_name
        if output_config_command is not None: self._values["output_config_command"] = output_config_command
        if output_masters_role_arn is not None: self._values["output_masters_role_arn"] = output_masters_role_arn
        if role is not None: self._values["role"] = role
        if security_group is not None: self._values["security_group"] = security_group
        if version is not None: self._values["version"] = version
        if vpc is not None: self._values["vpc"] = vpc
        if vpc_subnets is not None: self._values["vpc_subnets"] = vpc_subnets
        if default_capacity is not None: self._values["default_capacity"] = default_capacity
        if default_capacity_instance is not None: self._values["default_capacity_instance"] = default_capacity_instance
        if default_capacity_type is not None: self._values["default_capacity_type"] = default_capacity_type
        if kubectl_enabled is not None: self._values["kubectl_enabled"] = kubectl_enabled

    @builtins.property
    def cluster_name(self) -> typing.Optional[str]:
        """Name for the cluster.

        default
        :default: - Automatically generated name

        stability
        :stability: experimental
        """
        return self._values.get('cluster_name')

    @builtins.property
    def core_dns_compute_type(self) -> typing.Optional["CoreDnsComputeType"]:
        """Controls the "eks.amazonaws.com/compute-type" annotation in the CoreDNS configuration on your cluster to determine which compute type to use for CoreDNS.

        default
        :default: CoreDnsComputeType.EC2 (for ``FargateCluster`` the default is FARGATE)

        stability
        :stability: experimental
        """
        return self._values.get('core_dns_compute_type')

    @builtins.property
    def masters_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """An IAM role that will be added to the ``system:masters`` Kubernetes RBAC group.

        default
        :default:

        - By default, it will only possible to update this Kubernetes
          system by adding resources to this cluster via ``addResource`` or
          by defining ``KubernetesResource`` resources in your AWS CDK app.
          Use this if you wish to grant cluster administration privileges
          to another role.

        see
        :see: https://kubernetes.io/docs/reference/access-authn-authz/rbac/#default-roles-and-role-bindings
        stability
        :stability: experimental
        """
        return self._values.get('masters_role')

    @builtins.property
    def output_cluster_name(self) -> typing.Optional[bool]:
        """Determines whether a CloudFormation output with the name of the cluster will be synthesized.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('output_cluster_name')

    @builtins.property
    def output_config_command(self) -> typing.Optional[bool]:
        """Determines whether a CloudFormation output with the ``aws eks update-kubeconfig`` command will be synthesized.

        This command will include
        the cluster name and, if applicable, the ARN of the masters IAM role.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('output_config_command')

    @builtins.property
    def output_masters_role_arn(self) -> typing.Optional[bool]:
        """Determines whether a CloudFormation output with the ARN of the "masters" IAM role will be synthesized (if ``mastersRole`` is specified).

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('output_masters_role_arn')

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """Role that provides permissions for the Kubernetes control plane to make calls to AWS API operations on your behalf.

        default
        :default: - A role is automatically created for you

        stability
        :stability: experimental
        """
        return self._values.get('role')

    @builtins.property
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        """Security Group to use for Control Plane ENIs.

        default
        :default: - A security group is automatically created

        stability
        :stability: experimental
        """
        return self._values.get('security_group')

    @builtins.property
    def version(self) -> typing.Optional[str]:
        """The Kubernetes version to run in the cluster.

        default
        :default: - If not supplied, will use Amazon default version

        stability
        :stability: experimental
        """
        return self._values.get('version')

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC in which to create the Cluster.

        default
        :default: - a VPC with default configuration will be created and can be accessed through ``cluster.vpc``.

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[typing.List[aws_cdk.aws_ec2.SubnetSelection]]:
        """Where to place EKS Control Plane ENIs.

        If you want to create public load balancers, this must include public subnets.

        For example, to only select private subnets, supply the following::

           # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
           vpcSubnets: [
              { subnetType: ec2.SubnetType.Private }
           ]

        default
        :default: - All public and private subnets

        stability
        :stability: experimental
        """
        return self._values.get('vpc_subnets')

    @builtins.property
    def default_capacity(self) -> typing.Optional[jsii.Number]:
        """Number of instances to allocate as an initial capacity for this cluster.

        Instance type can be configured through ``defaultCapacityInstanceType``,
        which defaults to ``m5.large``.

        Use ``cluster.addCapacity`` to add additional customized capacity. Set this
        to ``0`` is you wish to avoid the initial capacity allocation.

        default
        :default: 2

        stability
        :stability: experimental
        """
        return self._values.get('default_capacity')

    @builtins.property
    def default_capacity_instance(self) -> typing.Optional[aws_cdk.aws_ec2.InstanceType]:
        """The instance type to use for the default capacity.

        This will only be taken
        into account if ``defaultCapacity`` is > 0.

        default
        :default: m5.large

        stability
        :stability: experimental
        """
        return self._values.get('default_capacity_instance')

    @builtins.property
    def default_capacity_type(self) -> typing.Optional["DefaultCapacityType"]:
        """The default capacity type for the cluster.

        default
        :default: NODEGROUP

        stability
        :stability: experimental
        """
        return self._values.get('default_capacity_type')

    @builtins.property
    def kubectl_enabled(self) -> typing.Optional[bool]:
        """Allows defining ``kubectrl``-related resources on this cluster.

        If this is disabled, it will not be possible to use the following
        capabilities:

        - ``addResource``
        - ``addRoleMapping``
        - ``addUserMapping``
        - ``addMastersRole`` and ``props.mastersRole``

        If this is disabled, the cluster can only be managed by issuing ``kubectl``
        commands from a session that uses the IAM role/user that created the
        account.

        *NOTE*: changing this value will destoy the cluster. This is because a
        managable cluster must be created using an AWS CloudFormation custom
        resource which executes with an IAM role owned by the CDK app.

        default
        :default: true The cluster can be managed by the AWS CDK application.

        stability
        :stability: experimental
        """
        return self._values.get('kubectl_enabled')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ClusterProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-eks.CoreDnsComputeType")
class CoreDnsComputeType(enum.Enum):
    """The type of compute resources to use for CoreDNS.

    stability
    :stability: experimental
    """
    EC2 = "EC2"
    """Deploy CoreDNS on EC2 instances.

    stability
    :stability: experimental
    """
    FARGATE = "FARGATE"
    """Deploy CoreDNS on Fargate-managed instances.

    stability
    :stability: experimental
    """

@jsii.enum(jsii_type="@aws-cdk/aws-eks.DefaultCapacityType")
class DefaultCapacityType(enum.Enum):
    """The default capacity type for the cluster.

    stability
    :stability: experimental
    """
    NODEGROUP = "NODEGROUP"
    """managed node group.

    stability
    :stability: experimental
    """
    EC2 = "EC2"
    """EC2 autoscaling group.

    stability
    :stability: experimental
    """

@jsii.implements(aws_cdk.aws_ec2.IMachineImage)
class EksOptimizedImage(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-eks.EksOptimizedImage"):
    """Construct an Amazon Linux 2 image from the latest EKS Optimized AMI published in SSM.

    stability
    :stability: experimental
    """
    def __init__(self, *, kubernetes_version: typing.Optional[str]=None, node_type: typing.Optional["NodeType"]=None) -> None:
        """Constructs a new instance of the EcsOptimizedAmi class.

        :param kubernetes_version: The Kubernetes version to use. Default: - The latest version
        :param node_type: What instance type to retrieve the image for (standard or GPU-optimized). Default: NodeType.STANDARD

        stability
        :stability: experimental
        """
        props = EksOptimizedImageProps(kubernetes_version=kubernetes_version, node_type=node_type)

        jsii.create(EksOptimizedImage, self, [props])

    @jsii.member(jsii_name="getImage")
    def get_image(self, scope: aws_cdk.core.Construct) -> aws_cdk.aws_ec2.MachineImageConfig:
        """Return the correct image.

        :param scope: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getImage", [scope])


@jsii.data_type(jsii_type="@aws-cdk/aws-eks.EksOptimizedImageProps", jsii_struct_bases=[], name_mapping={'kubernetes_version': 'kubernetesVersion', 'node_type': 'nodeType'})
class EksOptimizedImageProps():
    def __init__(self, *, kubernetes_version: typing.Optional[str]=None, node_type: typing.Optional["NodeType"]=None) -> None:
        """Properties for EksOptimizedImage.

        :param kubernetes_version: The Kubernetes version to use. Default: - The latest version
        :param node_type: What instance type to retrieve the image for (standard or GPU-optimized). Default: NodeType.STANDARD

        stability
        :stability: experimental
        """
        self._values = {
        }
        if kubernetes_version is not None: self._values["kubernetes_version"] = kubernetes_version
        if node_type is not None: self._values["node_type"] = node_type

    @builtins.property
    def kubernetes_version(self) -> typing.Optional[str]:
        """The Kubernetes version to use.

        default
        :default: - The latest version

        stability
        :stability: experimental
        """
        return self._values.get('kubernetes_version')

    @builtins.property
    def node_type(self) -> typing.Optional["NodeType"]:
        """What instance type to retrieve the image for (standard or GPU-optimized).

        default
        :default: NodeType.STANDARD

        stability
        :stability: experimental
        """
        return self._values.get('node_type')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EksOptimizedImageProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-eks.FargateClusterProps", jsii_struct_bases=[ClusterOptions], name_mapping={'cluster_name': 'clusterName', 'core_dns_compute_type': 'coreDnsComputeType', 'masters_role': 'mastersRole', 'output_cluster_name': 'outputClusterName', 'output_config_command': 'outputConfigCommand', 'output_masters_role_arn': 'outputMastersRoleArn', 'role': 'role', 'security_group': 'securityGroup', 'version': 'version', 'vpc': 'vpc', 'vpc_subnets': 'vpcSubnets', 'default_profile': 'defaultProfile'})
class FargateClusterProps(ClusterOptions):
    def __init__(self, *, cluster_name: typing.Optional[str]=None, core_dns_compute_type: typing.Optional["CoreDnsComputeType"]=None, masters_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, output_cluster_name: typing.Optional[bool]=None, output_config_command: typing.Optional[bool]=None, output_masters_role_arn: typing.Optional[bool]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None, version: typing.Optional[str]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None, vpc_subnets: typing.Optional[typing.List[aws_cdk.aws_ec2.SubnetSelection]]=None, default_profile: typing.Optional["FargateProfileOptions"]=None) -> None:
        """Configuration props for EKS Fargate.

        :param cluster_name: Name for the cluster. Default: - Automatically generated name
        :param core_dns_compute_type: Controls the "eks.amazonaws.com/compute-type" annotation in the CoreDNS configuration on your cluster to determine which compute type to use for CoreDNS. Default: CoreDnsComputeType.EC2 (for ``FargateCluster`` the default is FARGATE)
        :param masters_role: An IAM role that will be added to the ``system:masters`` Kubernetes RBAC group. Default: - By default, it will only possible to update this Kubernetes system by adding resources to this cluster via ``addResource`` or by defining ``KubernetesResource`` resources in your AWS CDK app. Use this if you wish to grant cluster administration privileges to another role.
        :param output_cluster_name: Determines whether a CloudFormation output with the name of the cluster will be synthesized. Default: false
        :param output_config_command: Determines whether a CloudFormation output with the ``aws eks update-kubeconfig`` command will be synthesized. This command will include the cluster name and, if applicable, the ARN of the masters IAM role. Default: true
        :param output_masters_role_arn: Determines whether a CloudFormation output with the ARN of the "masters" IAM role will be synthesized (if ``mastersRole`` is specified). Default: false
        :param role: Role that provides permissions for the Kubernetes control plane to make calls to AWS API operations on your behalf. Default: - A role is automatically created for you
        :param security_group: Security Group to use for Control Plane ENIs. Default: - A security group is automatically created
        :param version: The Kubernetes version to run in the cluster. Default: - If not supplied, will use Amazon default version
        :param vpc: The VPC in which to create the Cluster. Default: - a VPC with default configuration will be created and can be accessed through ``cluster.vpc``.
        :param vpc_subnets: Where to place EKS Control Plane ENIs. If you want to create public load balancers, this must include public subnets. For example, to only select private subnets, supply the following:: vpcSubnets: [ { subnetType: ec2.SubnetType.Private } ] Default: - All public and private subnets
        :param default_profile: Fargate Profile to create along with the cluster. Default: - A profile called "default" with 'default' and 'kube-system' selectors will be created if this is left undefined.

        stability
        :stability: experimental
        """
        if isinstance(default_profile, dict): default_profile = FargateProfileOptions(**default_profile)
        self._values = {
        }
        if cluster_name is not None: self._values["cluster_name"] = cluster_name
        if core_dns_compute_type is not None: self._values["core_dns_compute_type"] = core_dns_compute_type
        if masters_role is not None: self._values["masters_role"] = masters_role
        if output_cluster_name is not None: self._values["output_cluster_name"] = output_cluster_name
        if output_config_command is not None: self._values["output_config_command"] = output_config_command
        if output_masters_role_arn is not None: self._values["output_masters_role_arn"] = output_masters_role_arn
        if role is not None: self._values["role"] = role
        if security_group is not None: self._values["security_group"] = security_group
        if version is not None: self._values["version"] = version
        if vpc is not None: self._values["vpc"] = vpc
        if vpc_subnets is not None: self._values["vpc_subnets"] = vpc_subnets
        if default_profile is not None: self._values["default_profile"] = default_profile

    @builtins.property
    def cluster_name(self) -> typing.Optional[str]:
        """Name for the cluster.

        default
        :default: - Automatically generated name

        stability
        :stability: experimental
        """
        return self._values.get('cluster_name')

    @builtins.property
    def core_dns_compute_type(self) -> typing.Optional["CoreDnsComputeType"]:
        """Controls the "eks.amazonaws.com/compute-type" annotation in the CoreDNS configuration on your cluster to determine which compute type to use for CoreDNS.

        default
        :default: CoreDnsComputeType.EC2 (for ``FargateCluster`` the default is FARGATE)

        stability
        :stability: experimental
        """
        return self._values.get('core_dns_compute_type')

    @builtins.property
    def masters_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """An IAM role that will be added to the ``system:masters`` Kubernetes RBAC group.

        default
        :default:

        - By default, it will only possible to update this Kubernetes
          system by adding resources to this cluster via ``addResource`` or
          by defining ``KubernetesResource`` resources in your AWS CDK app.
          Use this if you wish to grant cluster administration privileges
          to another role.

        see
        :see: https://kubernetes.io/docs/reference/access-authn-authz/rbac/#default-roles-and-role-bindings
        stability
        :stability: experimental
        """
        return self._values.get('masters_role')

    @builtins.property
    def output_cluster_name(self) -> typing.Optional[bool]:
        """Determines whether a CloudFormation output with the name of the cluster will be synthesized.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('output_cluster_name')

    @builtins.property
    def output_config_command(self) -> typing.Optional[bool]:
        """Determines whether a CloudFormation output with the ``aws eks update-kubeconfig`` command will be synthesized.

        This command will include
        the cluster name and, if applicable, the ARN of the masters IAM role.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('output_config_command')

    @builtins.property
    def output_masters_role_arn(self) -> typing.Optional[bool]:
        """Determines whether a CloudFormation output with the ARN of the "masters" IAM role will be synthesized (if ``mastersRole`` is specified).

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('output_masters_role_arn')

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """Role that provides permissions for the Kubernetes control plane to make calls to AWS API operations on your behalf.

        default
        :default: - A role is automatically created for you

        stability
        :stability: experimental
        """
        return self._values.get('role')

    @builtins.property
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        """Security Group to use for Control Plane ENIs.

        default
        :default: - A security group is automatically created

        stability
        :stability: experimental
        """
        return self._values.get('security_group')

    @builtins.property
    def version(self) -> typing.Optional[str]:
        """The Kubernetes version to run in the cluster.

        default
        :default: - If not supplied, will use Amazon default version

        stability
        :stability: experimental
        """
        return self._values.get('version')

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC in which to create the Cluster.

        default
        :default: - a VPC with default configuration will be created and can be accessed through ``cluster.vpc``.

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[typing.List[aws_cdk.aws_ec2.SubnetSelection]]:
        """Where to place EKS Control Plane ENIs.

        If you want to create public load balancers, this must include public subnets.

        For example, to only select private subnets, supply the following::

           # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
           vpcSubnets: [
              { subnetType: ec2.SubnetType.Private }
           ]

        default
        :default: - All public and private subnets

        stability
        :stability: experimental
        """
        return self._values.get('vpc_subnets')

    @builtins.property
    def default_profile(self) -> typing.Optional["FargateProfileOptions"]:
        """Fargate Profile to create along with the cluster.

        default
        :default:

        - A profile called "default" with 'default' and 'kube-system'
          selectors will be created if this is left undefined.

        stability
        :stability: experimental
        """
        return self._values.get('default_profile')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FargateClusterProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.ITaggable)
class FargateProfile(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-eks.FargateProfile"):
    """Fargate profiles allows an administrator to declare which pods run on Fargate.

    This declaration is done through the profile’s selectors. Each
    profile can have up to five selectors that contain a namespace and optional
    labels. You must define a namespace for every selector. The label field
    consists of multiple optional key-value pairs. Pods that match a selector (by
    matching a namespace for the selector and all of the labels specified in the
    selector) are scheduled on Fargate. If a namespace selector is defined
    without any labels, Amazon EKS will attempt to schedule all pods that run in
    that namespace onto Fargate using the profile. If a to-be-scheduled pod
    matches any of the selectors in the Fargate profile, then that pod is
    scheduled on Fargate.

    If a pod matches multiple Fargate profiles, Amazon EKS picks one of the
    matches at random. In this case, you can specify which profile a pod should
    use by adding the following Kubernetes label to the pod specification:
    eks.amazonaws.com/fargate-profile: profile_name. However, the pod must still
    match a selector in that profile in order to be scheduled onto Fargate.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, cluster: "Cluster", selectors: typing.List["Selector"], fargate_profile_name: typing.Optional[str]=None, pod_execution_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, subnet_selection: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param cluster: The EKS cluster to apply the Fargate profile to. [disable-awslint:ref-via-interface]
        :param selectors: The selectors to match for pods to use this Fargate profile. Each selector must have an associated namespace. Optionally, you can also specify labels for a namespace. At least one selector is required and you may specify up to five selectors.
        :param fargate_profile_name: The name of the Fargate profile. Default: - generated
        :param pod_execution_role: The pod execution role to use for pods that match the selectors in the Fargate profile. The pod execution role allows Fargate infrastructure to register with your cluster as a node, and it provides read access to Amazon ECR image repositories. Default: - a role will be automatically created
        :param subnet_selection: Select which subnets to launch your pods into. At this time, pods running on Fargate are not assigned public IP addresses, so only private subnets (with no direct route to an Internet Gateway) are allowed. Default: - all private subnets of the VPC are selected.
        :param vpc: The VPC from which to select subnets to launch your pods into. By default, all private subnets are selected. You can customize this using ``subnetSelection``. Default: - all private subnets used by theEKS cluster

        stability
        :stability: experimental
        """
        props = FargateProfileProps(cluster=cluster, selectors=selectors, fargate_profile_name=fargate_profile_name, pod_execution_role=pod_execution_role, subnet_selection=subnet_selection, vpc=vpc)

        jsii.create(FargateProfile, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="fargateProfileArn")
    def fargate_profile_arn(self) -> str:
        """The full Amazon Resource Name (ARN) of the Fargate profile.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "fargateProfileArn")

    @builtins.property
    @jsii.member(jsii_name="fargateProfileName")
    def fargate_profile_name(self) -> str:
        """The name of the Fargate profile.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "fargateProfileName")

    @builtins.property
    @jsii.member(jsii_name="podExecutionRole")
    def pod_execution_role(self) -> aws_cdk.aws_iam.IRole:
        """The pod execution role to use for pods that match the selectors in the Fargate profile.

        The pod execution role allows Fargate infrastructure to
        register with your cluster as a node, and it provides read access to Amazon
        ECR image repositories.

        stability
        :stability: experimental
        """
        return jsii.get(self, "podExecutionRole")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """Resource tags.

        stability
        :stability: experimental
        """
        return jsii.get(self, "tags")


@jsii.data_type(jsii_type="@aws-cdk/aws-eks.FargateProfileOptions", jsii_struct_bases=[], name_mapping={'selectors': 'selectors', 'fargate_profile_name': 'fargateProfileName', 'pod_execution_role': 'podExecutionRole', 'subnet_selection': 'subnetSelection', 'vpc': 'vpc'})
class FargateProfileOptions():
    def __init__(self, *, selectors: typing.List["Selector"], fargate_profile_name: typing.Optional[str]=None, pod_execution_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, subnet_selection: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None) -> None:
        """Options for defining EKS Fargate Profiles.

        :param selectors: The selectors to match for pods to use this Fargate profile. Each selector must have an associated namespace. Optionally, you can also specify labels for a namespace. At least one selector is required and you may specify up to five selectors.
        :param fargate_profile_name: The name of the Fargate profile. Default: - generated
        :param pod_execution_role: The pod execution role to use for pods that match the selectors in the Fargate profile. The pod execution role allows Fargate infrastructure to register with your cluster as a node, and it provides read access to Amazon ECR image repositories. Default: - a role will be automatically created
        :param subnet_selection: Select which subnets to launch your pods into. At this time, pods running on Fargate are not assigned public IP addresses, so only private subnets (with no direct route to an Internet Gateway) are allowed. Default: - all private subnets of the VPC are selected.
        :param vpc: The VPC from which to select subnets to launch your pods into. By default, all private subnets are selected. You can customize this using ``subnetSelection``. Default: - all private subnets used by theEKS cluster

        stability
        :stability: experimental
        """
        if isinstance(subnet_selection, dict): subnet_selection = aws_cdk.aws_ec2.SubnetSelection(**subnet_selection)
        self._values = {
            'selectors': selectors,
        }
        if fargate_profile_name is not None: self._values["fargate_profile_name"] = fargate_profile_name
        if pod_execution_role is not None: self._values["pod_execution_role"] = pod_execution_role
        if subnet_selection is not None: self._values["subnet_selection"] = subnet_selection
        if vpc is not None: self._values["vpc"] = vpc

    @builtins.property
    def selectors(self) -> typing.List["Selector"]:
        """The selectors to match for pods to use this Fargate profile.

        Each selector
        must have an associated namespace. Optionally, you can also specify labels
        for a namespace.

        At least one selector is required and you may specify up to five selectors.

        stability
        :stability: experimental
        """
        return self._values.get('selectors')

    @builtins.property
    def fargate_profile_name(self) -> typing.Optional[str]:
        """The name of the Fargate profile.

        default
        :default: - generated

        stability
        :stability: experimental
        """
        return self._values.get('fargate_profile_name')

    @builtins.property
    def pod_execution_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The pod execution role to use for pods that match the selectors in the Fargate profile.

        The pod execution role allows Fargate infrastructure to
        register with your cluster as a node, and it provides read access to Amazon
        ECR image repositories.

        default
        :default: - a role will be automatically created

        see
        :see: https://docs.aws.amazon.com/eks/latest/userguide/pod-execution-role.html
        stability
        :stability: experimental
        """
        return self._values.get('pod_execution_role')

    @builtins.property
    def subnet_selection(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """Select which subnets to launch your pods into.

        At this time, pods running
        on Fargate are not assigned public IP addresses, so only private subnets
        (with no direct route to an Internet Gateway) are allowed.

        default
        :default: - all private subnets of the VPC are selected.

        stability
        :stability: experimental
        """
        return self._values.get('subnet_selection')

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC from which to select subnets to launch your pods into.

        By default, all private subnets are selected. You can customize this using
        ``subnetSelection``.

        default
        :default: - all private subnets used by theEKS cluster

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FargateProfileOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-eks.FargateProfileProps", jsii_struct_bases=[FargateProfileOptions], name_mapping={'selectors': 'selectors', 'fargate_profile_name': 'fargateProfileName', 'pod_execution_role': 'podExecutionRole', 'subnet_selection': 'subnetSelection', 'vpc': 'vpc', 'cluster': 'cluster'})
class FargateProfileProps(FargateProfileOptions):
    def __init__(self, *, selectors: typing.List["Selector"], fargate_profile_name: typing.Optional[str]=None, pod_execution_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, subnet_selection: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None, cluster: "Cluster") -> None:
        """Configuration props for EKS Fargate Profiles.

        :param selectors: The selectors to match for pods to use this Fargate profile. Each selector must have an associated namespace. Optionally, you can also specify labels for a namespace. At least one selector is required and you may specify up to five selectors.
        :param fargate_profile_name: The name of the Fargate profile. Default: - generated
        :param pod_execution_role: The pod execution role to use for pods that match the selectors in the Fargate profile. The pod execution role allows Fargate infrastructure to register with your cluster as a node, and it provides read access to Amazon ECR image repositories. Default: - a role will be automatically created
        :param subnet_selection: Select which subnets to launch your pods into. At this time, pods running on Fargate are not assigned public IP addresses, so only private subnets (with no direct route to an Internet Gateway) are allowed. Default: - all private subnets of the VPC are selected.
        :param vpc: The VPC from which to select subnets to launch your pods into. By default, all private subnets are selected. You can customize this using ``subnetSelection``. Default: - all private subnets used by theEKS cluster
        :param cluster: The EKS cluster to apply the Fargate profile to. [disable-awslint:ref-via-interface]

        stability
        :stability: experimental
        """
        if isinstance(subnet_selection, dict): subnet_selection = aws_cdk.aws_ec2.SubnetSelection(**subnet_selection)
        self._values = {
            'selectors': selectors,
            'cluster': cluster,
        }
        if fargate_profile_name is not None: self._values["fargate_profile_name"] = fargate_profile_name
        if pod_execution_role is not None: self._values["pod_execution_role"] = pod_execution_role
        if subnet_selection is not None: self._values["subnet_selection"] = subnet_selection
        if vpc is not None: self._values["vpc"] = vpc

    @builtins.property
    def selectors(self) -> typing.List["Selector"]:
        """The selectors to match for pods to use this Fargate profile.

        Each selector
        must have an associated namespace. Optionally, you can also specify labels
        for a namespace.

        At least one selector is required and you may specify up to five selectors.

        stability
        :stability: experimental
        """
        return self._values.get('selectors')

    @builtins.property
    def fargate_profile_name(self) -> typing.Optional[str]:
        """The name of the Fargate profile.

        default
        :default: - generated

        stability
        :stability: experimental
        """
        return self._values.get('fargate_profile_name')

    @builtins.property
    def pod_execution_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The pod execution role to use for pods that match the selectors in the Fargate profile.

        The pod execution role allows Fargate infrastructure to
        register with your cluster as a node, and it provides read access to Amazon
        ECR image repositories.

        default
        :default: - a role will be automatically created

        see
        :see: https://docs.aws.amazon.com/eks/latest/userguide/pod-execution-role.html
        stability
        :stability: experimental
        """
        return self._values.get('pod_execution_role')

    @builtins.property
    def subnet_selection(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """Select which subnets to launch your pods into.

        At this time, pods running
        on Fargate are not assigned public IP addresses, so only private subnets
        (with no direct route to an Internet Gateway) are allowed.

        default
        :default: - all private subnets of the VPC are selected.

        stability
        :stability: experimental
        """
        return self._values.get('subnet_selection')

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC from which to select subnets to launch your pods into.

        By default, all private subnets are selected. You can customize this using
        ``subnetSelection``.

        default
        :default: - all private subnets used by theEKS cluster

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    @builtins.property
    def cluster(self) -> "Cluster":
        """The EKS cluster to apply the Fargate profile to.

        [disable-awslint:ref-via-interface]

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FargateProfileProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class HelmChart(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-eks.HelmChart"):
    """Represents a helm chart within the Kubernetes system.

    Applies/deletes the resources using ``kubectl`` in sync with the resource.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, cluster: "Cluster", chart: str, create_namespace: typing.Optional[bool]=None, namespace: typing.Optional[str]=None, release: typing.Optional[str]=None, repository: typing.Optional[str]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None, values: typing.Optional[typing.Mapping[str, typing.Any]]=None, version: typing.Optional[str]=None, wait: typing.Optional[bool]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param cluster: The EKS cluster to apply this configuration to. [disable-awslint:ref-via-interface]
        :param chart: The name of the chart.
        :param create_namespace: create namespace if not exist. Default: true
        :param namespace: The Kubernetes namespace scope of the requests. Default: default
        :param release: The name of the release. Default: - If no release name is given, it will use the last 53 characters of the node's unique id.
        :param repository: The repository which contains the chart. For example: https://kubernetes-charts.storage.googleapis.com/ Default: - No repository will be used, which means that the chart needs to be an absolute URL.
        :param timeout: Amount of time to wait for any individual Kubernetes operation. Maximum 15 minutes. Default: Duration.minutes(5)
        :param values: The values to be used by the chart. Default: - No values are provided to the chart.
        :param version: The chart version to install. Default: - If this is not specified, the latest version is installed
        :param wait: Whether or not Helm should wait until all Pods, PVCs, Services, and minimum number of Pods of a Deployment, StatefulSet, or ReplicaSet are in a ready state before marking the release as successful. Default: - Helm will not wait before marking release as successful

        stability
        :stability: experimental
        """
        props = HelmChartProps(cluster=cluster, chart=chart, create_namespace=create_namespace, namespace=namespace, release=release, repository=repository, timeout=timeout, values=values, version=version, wait=wait)

        jsii.create(HelmChart, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="RESOURCE_TYPE")
    def RESOURCE_TYPE(cls) -> str:
        """The CloudFormation resource type.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "RESOURCE_TYPE")


@jsii.data_type(jsii_type="@aws-cdk/aws-eks.HelmChartOptions", jsii_struct_bases=[], name_mapping={'chart': 'chart', 'create_namespace': 'createNamespace', 'namespace': 'namespace', 'release': 'release', 'repository': 'repository', 'timeout': 'timeout', 'values': 'values', 'version': 'version', 'wait': 'wait'})
class HelmChartOptions():
    def __init__(self, *, chart: str, create_namespace: typing.Optional[bool]=None, namespace: typing.Optional[str]=None, release: typing.Optional[str]=None, repository: typing.Optional[str]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None, values: typing.Optional[typing.Mapping[str, typing.Any]]=None, version: typing.Optional[str]=None, wait: typing.Optional[bool]=None) -> None:
        """Helm Chart options.

        :param chart: The name of the chart.
        :param create_namespace: create namespace if not exist. Default: true
        :param namespace: The Kubernetes namespace scope of the requests. Default: default
        :param release: The name of the release. Default: - If no release name is given, it will use the last 53 characters of the node's unique id.
        :param repository: The repository which contains the chart. For example: https://kubernetes-charts.storage.googleapis.com/ Default: - No repository will be used, which means that the chart needs to be an absolute URL.
        :param timeout: Amount of time to wait for any individual Kubernetes operation. Maximum 15 minutes. Default: Duration.minutes(5)
        :param values: The values to be used by the chart. Default: - No values are provided to the chart.
        :param version: The chart version to install. Default: - If this is not specified, the latest version is installed
        :param wait: Whether or not Helm should wait until all Pods, PVCs, Services, and minimum number of Pods of a Deployment, StatefulSet, or ReplicaSet are in a ready state before marking the release as successful. Default: - Helm will not wait before marking release as successful

        stability
        :stability: experimental
        """
        self._values = {
            'chart': chart,
        }
        if create_namespace is not None: self._values["create_namespace"] = create_namespace
        if namespace is not None: self._values["namespace"] = namespace
        if release is not None: self._values["release"] = release
        if repository is not None: self._values["repository"] = repository
        if timeout is not None: self._values["timeout"] = timeout
        if values is not None: self._values["values"] = values
        if version is not None: self._values["version"] = version
        if wait is not None: self._values["wait"] = wait

    @builtins.property
    def chart(self) -> str:
        """The name of the chart.

        stability
        :stability: experimental
        """
        return self._values.get('chart')

    @builtins.property
    def create_namespace(self) -> typing.Optional[bool]:
        """create namespace if not exist.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('create_namespace')

    @builtins.property
    def namespace(self) -> typing.Optional[str]:
        """The Kubernetes namespace scope of the requests.

        default
        :default: default

        stability
        :stability: experimental
        """
        return self._values.get('namespace')

    @builtins.property
    def release(self) -> typing.Optional[str]:
        """The name of the release.

        default
        :default: - If no release name is given, it will use the last 53 characters of the node's unique id.

        stability
        :stability: experimental
        """
        return self._values.get('release')

    @builtins.property
    def repository(self) -> typing.Optional[str]:
        """The repository which contains the chart.

        For example: https://kubernetes-charts.storage.googleapis.com/

        default
        :default: - No repository will be used, which means that the chart needs to be an absolute URL.

        stability
        :stability: experimental
        """
        return self._values.get('repository')

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Amount of time to wait for any individual Kubernetes operation.

        Maximum 15 minutes.

        default
        :default: Duration.minutes(5)

        stability
        :stability: experimental
        """
        return self._values.get('timeout')

    @builtins.property
    def values(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """The values to be used by the chart.

        default
        :default: - No values are provided to the chart.

        stability
        :stability: experimental
        """
        return self._values.get('values')

    @builtins.property
    def version(self) -> typing.Optional[str]:
        """The chart version to install.

        default
        :default: - If this is not specified, the latest version is installed

        stability
        :stability: experimental
        """
        return self._values.get('version')

    @builtins.property
    def wait(self) -> typing.Optional[bool]:
        """Whether or not Helm should wait until all Pods, PVCs, Services, and minimum number of Pods of a Deployment, StatefulSet, or ReplicaSet are in a ready state before marking the release as successful.

        default
        :default: - Helm will not wait before marking release as successful

        stability
        :stability: experimental
        """
        return self._values.get('wait')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'HelmChartOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-eks.HelmChartProps", jsii_struct_bases=[HelmChartOptions], name_mapping={'chart': 'chart', 'create_namespace': 'createNamespace', 'namespace': 'namespace', 'release': 'release', 'repository': 'repository', 'timeout': 'timeout', 'values': 'values', 'version': 'version', 'wait': 'wait', 'cluster': 'cluster'})
class HelmChartProps(HelmChartOptions):
    def __init__(self, *, chart: str, create_namespace: typing.Optional[bool]=None, namespace: typing.Optional[str]=None, release: typing.Optional[str]=None, repository: typing.Optional[str]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None, values: typing.Optional[typing.Mapping[str, typing.Any]]=None, version: typing.Optional[str]=None, wait: typing.Optional[bool]=None, cluster: "Cluster") -> None:
        """Helm Chart properties.

        :param chart: The name of the chart.
        :param create_namespace: create namespace if not exist. Default: true
        :param namespace: The Kubernetes namespace scope of the requests. Default: default
        :param release: The name of the release. Default: - If no release name is given, it will use the last 53 characters of the node's unique id.
        :param repository: The repository which contains the chart. For example: https://kubernetes-charts.storage.googleapis.com/ Default: - No repository will be used, which means that the chart needs to be an absolute URL.
        :param timeout: Amount of time to wait for any individual Kubernetes operation. Maximum 15 minutes. Default: Duration.minutes(5)
        :param values: The values to be used by the chart. Default: - No values are provided to the chart.
        :param version: The chart version to install. Default: - If this is not specified, the latest version is installed
        :param wait: Whether or not Helm should wait until all Pods, PVCs, Services, and minimum number of Pods of a Deployment, StatefulSet, or ReplicaSet are in a ready state before marking the release as successful. Default: - Helm will not wait before marking release as successful
        :param cluster: The EKS cluster to apply this configuration to. [disable-awslint:ref-via-interface]

        stability
        :stability: experimental
        """
        self._values = {
            'chart': chart,
            'cluster': cluster,
        }
        if create_namespace is not None: self._values["create_namespace"] = create_namespace
        if namespace is not None: self._values["namespace"] = namespace
        if release is not None: self._values["release"] = release
        if repository is not None: self._values["repository"] = repository
        if timeout is not None: self._values["timeout"] = timeout
        if values is not None: self._values["values"] = values
        if version is not None: self._values["version"] = version
        if wait is not None: self._values["wait"] = wait

    @builtins.property
    def chart(self) -> str:
        """The name of the chart.

        stability
        :stability: experimental
        """
        return self._values.get('chart')

    @builtins.property
    def create_namespace(self) -> typing.Optional[bool]:
        """create namespace if not exist.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('create_namespace')

    @builtins.property
    def namespace(self) -> typing.Optional[str]:
        """The Kubernetes namespace scope of the requests.

        default
        :default: default

        stability
        :stability: experimental
        """
        return self._values.get('namespace')

    @builtins.property
    def release(self) -> typing.Optional[str]:
        """The name of the release.

        default
        :default: - If no release name is given, it will use the last 53 characters of the node's unique id.

        stability
        :stability: experimental
        """
        return self._values.get('release')

    @builtins.property
    def repository(self) -> typing.Optional[str]:
        """The repository which contains the chart.

        For example: https://kubernetes-charts.storage.googleapis.com/

        default
        :default: - No repository will be used, which means that the chart needs to be an absolute URL.

        stability
        :stability: experimental
        """
        return self._values.get('repository')

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Amount of time to wait for any individual Kubernetes operation.

        Maximum 15 minutes.

        default
        :default: Duration.minutes(5)

        stability
        :stability: experimental
        """
        return self._values.get('timeout')

    @builtins.property
    def values(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """The values to be used by the chart.

        default
        :default: - No values are provided to the chart.

        stability
        :stability: experimental
        """
        return self._values.get('values')

    @builtins.property
    def version(self) -> typing.Optional[str]:
        """The chart version to install.

        default
        :default: - If this is not specified, the latest version is installed

        stability
        :stability: experimental
        """
        return self._values.get('version')

    @builtins.property
    def wait(self) -> typing.Optional[bool]:
        """Whether or not Helm should wait until all Pods, PVCs, Services, and minimum number of Pods of a Deployment, StatefulSet, or ReplicaSet are in a ready state before marking the release as successful.

        default
        :default: - Helm will not wait before marking release as successful

        stability
        :stability: experimental
        """
        return self._values.get('wait')

    @builtins.property
    def cluster(self) -> "Cluster":
        """The EKS cluster to apply this configuration to.

        [disable-awslint:ref-via-interface]

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'HelmChartProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="@aws-cdk/aws-eks.ICluster")
class ICluster(aws_cdk.core.IResource, aws_cdk.aws_ec2.IConnectable, jsii.compat.Protocol):
    """An EKS cluster.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IClusterProxy

    @builtins.property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> str:
        """The unique ARN assigned to the service by AWS in the form of arn:aws:eks:.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="clusterCertificateAuthorityData")
    def cluster_certificate_authority_data(self) -> str:
        """The certificate-authority-data for your cluster.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="clusterEncryptionConfigKeyArn")
    def cluster_encryption_config_key_arn(self) -> str:
        """Amazon Resource Name (ARN) or alias of the customer master key (CMK).

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> str:
        """The API Server endpoint URL.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        """The physical name of the Cluster.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="clusterSecurityGroupId")
    def cluster_security_group_id(self) -> str:
        """The cluster security group that was created by Amazon EKS for the cluster.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """The VPC in which this Cluster was created.

        stability
        :stability: experimental
        """
        ...


class _IClusterProxy(jsii.proxy_for(aws_cdk.core.IResource), jsii.proxy_for(aws_cdk.aws_ec2.IConnectable)):
    """An EKS cluster.

    stability
    :stability: experimental
    """
    __jsii_type__ = "@aws-cdk/aws-eks.ICluster"
    @builtins.property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> str:
        """The unique ARN assigned to the service by AWS in the form of arn:aws:eks:.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "clusterArn")

    @builtins.property
    @jsii.member(jsii_name="clusterCertificateAuthorityData")
    def cluster_certificate_authority_data(self) -> str:
        """The certificate-authority-data for your cluster.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "clusterCertificateAuthorityData")

    @builtins.property
    @jsii.member(jsii_name="clusterEncryptionConfigKeyArn")
    def cluster_encryption_config_key_arn(self) -> str:
        """Amazon Resource Name (ARN) or alias of the customer master key (CMK).

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "clusterEncryptionConfigKeyArn")

    @builtins.property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> str:
        """The API Server endpoint URL.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "clusterEndpoint")

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        """The physical name of the Cluster.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "clusterName")

    @builtins.property
    @jsii.member(jsii_name="clusterSecurityGroupId")
    def cluster_security_group_id(self) -> str:
        """The cluster security group that was created by Amazon EKS for the cluster.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "clusterSecurityGroupId")

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """The VPC in which this Cluster was created.

        stability
        :stability: experimental
        """
        return jsii.get(self, "vpc")


@jsii.interface(jsii_type="@aws-cdk/aws-eks.INodegroup")
class INodegroup(aws_cdk.core.IResource, jsii.compat.Protocol):
    """NodeGroup interface.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _INodegroupProxy

    @builtins.property
    @jsii.member(jsii_name="nodegroupName")
    def nodegroup_name(self) -> str:
        """Name of the nodegroup.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _INodegroupProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """NodeGroup interface.

    stability
    :stability: experimental
    """
    __jsii_type__ = "@aws-cdk/aws-eks.INodegroup"
    @builtins.property
    @jsii.member(jsii_name="nodegroupName")
    def nodegroup_name(self) -> str:
        """Name of the nodegroup.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "nodegroupName")


class KubernetesPatch(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-eks.KubernetesPatch"):
    """A CloudFormation resource which applies/restores a JSON patch into a Kubernetes resource.

    see
    :see: https://kubernetes.io/docs/tasks/run-application/update-api-object-kubectl-patch/
    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, apply_patch: typing.Mapping[str, typing.Any], cluster: "Cluster", resource_name: str, restore_patch: typing.Mapping[str, typing.Any], patch_type: typing.Optional["PatchType"]=None, resource_namespace: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param apply_patch: The JSON object to pass to ``kubectl patch`` when the resource is created/updated.
        :param cluster: The cluster to apply the patch to. [disable-awslint:ref-via-interface]
        :param resource_name: The full name of the resource to patch (e.g. ``deployment/coredns``).
        :param restore_patch: The JSON object to pass to ``kubectl patch`` when the resource is removed.
        :param patch_type: The patch type to pass to ``kubectl patch``. The default type used by ``kubectl patch`` is "strategic". Default: PatchType.STRATEGIC
        :param resource_namespace: The kubernetes API namespace. Default: "default"

        stability
        :stability: experimental
        """
        props = KubernetesPatchProps(apply_patch=apply_patch, cluster=cluster, resource_name=resource_name, restore_patch=restore_patch, patch_type=patch_type, resource_namespace=resource_namespace)

        jsii.create(KubernetesPatch, self, [scope, id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-eks.KubernetesPatchProps", jsii_struct_bases=[], name_mapping={'apply_patch': 'applyPatch', 'cluster': 'cluster', 'resource_name': 'resourceName', 'restore_patch': 'restorePatch', 'patch_type': 'patchType', 'resource_namespace': 'resourceNamespace'})
class KubernetesPatchProps():
    def __init__(self, *, apply_patch: typing.Mapping[str, typing.Any], cluster: "Cluster", resource_name: str, restore_patch: typing.Mapping[str, typing.Any], patch_type: typing.Optional["PatchType"]=None, resource_namespace: typing.Optional[str]=None) -> None:
        """Properties for KubernetesPatch.

        :param apply_patch: The JSON object to pass to ``kubectl patch`` when the resource is created/updated.
        :param cluster: The cluster to apply the patch to. [disable-awslint:ref-via-interface]
        :param resource_name: The full name of the resource to patch (e.g. ``deployment/coredns``).
        :param restore_patch: The JSON object to pass to ``kubectl patch`` when the resource is removed.
        :param patch_type: The patch type to pass to ``kubectl patch``. The default type used by ``kubectl patch`` is "strategic". Default: PatchType.STRATEGIC
        :param resource_namespace: The kubernetes API namespace. Default: "default"

        stability
        :stability: experimental
        """
        self._values = {
            'apply_patch': apply_patch,
            'cluster': cluster,
            'resource_name': resource_name,
            'restore_patch': restore_patch,
        }
        if patch_type is not None: self._values["patch_type"] = patch_type
        if resource_namespace is not None: self._values["resource_namespace"] = resource_namespace

    @builtins.property
    def apply_patch(self) -> typing.Mapping[str, typing.Any]:
        """The JSON object to pass to ``kubectl patch`` when the resource is created/updated.

        stability
        :stability: experimental
        """
        return self._values.get('apply_patch')

    @builtins.property
    def cluster(self) -> "Cluster":
        """The cluster to apply the patch to.

        [disable-awslint:ref-via-interface]

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @builtins.property
    def resource_name(self) -> str:
        """The full name of the resource to patch (e.g. ``deployment/coredns``).

        stability
        :stability: experimental
        """
        return self._values.get('resource_name')

    @builtins.property
    def restore_patch(self) -> typing.Mapping[str, typing.Any]:
        """The JSON object to pass to ``kubectl patch`` when the resource is removed.

        stability
        :stability: experimental
        """
        return self._values.get('restore_patch')

    @builtins.property
    def patch_type(self) -> typing.Optional["PatchType"]:
        """The patch type to pass to ``kubectl patch``.

        The default type used by ``kubectl patch`` is "strategic".

        default
        :default: PatchType.STRATEGIC

        stability
        :stability: experimental
        """
        return self._values.get('patch_type')

    @builtins.property
    def resource_namespace(self) -> typing.Optional[str]:
        """The kubernetes API namespace.

        default
        :default: "default"

        stability
        :stability: experimental
        """
        return self._values.get('resource_namespace')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'KubernetesPatchProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class KubernetesResource(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-eks.KubernetesResource"):
    """Represents a resource within the Kubernetes system.

    Alternatively, you can use ``cluster.addResource(resource[, resource, ...])``
    to define resources on this cluster.

    Applies/deletes the resources using ``kubectl`` in sync with the resource.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, cluster: "Cluster", manifest: typing.List[typing.Any]) -> None:
        """
        :param scope: -
        :param id: -
        :param cluster: The EKS cluster to apply this configuration to. [disable-awslint:ref-via-interface]
        :param manifest: The resource manifest. Consists of any number of child resources. When the resource is created/updated, this manifest will be applied to the cluster through ``kubectl apply`` and when the resource or the stack is deleted, the manifest will be deleted through ``kubectl delete``.

        stability
        :stability: experimental
        """
        props = KubernetesResourceProps(cluster=cluster, manifest=manifest)

        jsii.create(KubernetesResource, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="RESOURCE_TYPE")
    def RESOURCE_TYPE(cls) -> str:
        """The CloudFormation reosurce type.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "RESOURCE_TYPE")


@jsii.data_type(jsii_type="@aws-cdk/aws-eks.KubernetesResourceProps", jsii_struct_bases=[], name_mapping={'cluster': 'cluster', 'manifest': 'manifest'})
class KubernetesResourceProps():
    def __init__(self, *, cluster: "Cluster", manifest: typing.List[typing.Any]) -> None:
        """Properties for KubernetesResources.

        :param cluster: The EKS cluster to apply this configuration to. [disable-awslint:ref-via-interface]
        :param manifest: The resource manifest. Consists of any number of child resources. When the resource is created/updated, this manifest will be applied to the cluster through ``kubectl apply`` and when the resource or the stack is deleted, the manifest will be deleted through ``kubectl delete``.

        stability
        :stability: experimental
        """
        self._values = {
            'cluster': cluster,
            'manifest': manifest,
        }

    @builtins.property
    def cluster(self) -> "Cluster":
        """The EKS cluster to apply this configuration to.

        [disable-awslint:ref-via-interface]

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @builtins.property
    def manifest(self) -> typing.List[typing.Any]:
        """The resource manifest.

        Consists of any number of child resources.

        When the resource is created/updated, this manifest will be applied to the
        cluster through ``kubectl apply`` and when the resource or the stack is
        deleted, the manifest will be deleted through ``kubectl delete``.

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            apiVersion: 'v1',
                  kind"Pod" , metadataname: 'mypod'spec: {
                    containers: [ { name: 'hello', image: 'paulbouwer/hello-kubernetes:1.5', ports: [ { containerPort: 8080 } ] } ]
                  }
        """
        return self._values.get('manifest')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'KubernetesResourceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-eks.MachineImageType")
class MachineImageType(enum.Enum):
    """The machine image type.

    stability
    :stability: experimental
    """
    AMAZON_LINUX_2 = "AMAZON_LINUX_2"
    """Amazon EKS-optimized Linux AMI.

    stability
    :stability: experimental
    """
    BOTTLEROCKET = "BOTTLEROCKET"
    """Bottlerocket AMI.

    stability
    :stability: experimental
    """

@jsii.enum(jsii_type="@aws-cdk/aws-eks.NodeType")
class NodeType(enum.Enum):
    """Whether the worker nodes should support GPU or just standard instances.

    stability
    :stability: experimental
    """
    STANDARD = "STANDARD"
    """Standard instances.

    stability
    :stability: experimental
    """
    GPU = "GPU"
    """GPU instances.

    stability
    :stability: experimental
    """
    INFERENTIA = "INFERENTIA"
    """Inferentia instances.

    stability
    :stability: experimental
    """

@jsii.implements(INodegroup)
class Nodegroup(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-eks.Nodegroup"):
    """The Nodegroup resource class.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, cluster: "Cluster", ami_type: typing.Optional["NodegroupAmiType"]=None, desired_size: typing.Optional[jsii.Number]=None, disk_size: typing.Optional[jsii.Number]=None, force_update: typing.Optional[bool]=None, instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType]=None, labels: typing.Optional[typing.Mapping[str, str]]=None, max_size: typing.Optional[jsii.Number]=None, min_size: typing.Optional[jsii.Number]=None, nodegroup_name: typing.Optional[str]=None, node_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, release_version: typing.Optional[str]=None, remote_access: typing.Optional["NodegroupRemoteAccess"]=None, subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, tags: typing.Optional[typing.Mapping[str, str]]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param cluster: Cluster resource [disable-awslint:ref-via-interface]".
        :param ami_type: The AMI type for your node group. Default: AL2_x86_64
        :param desired_size: The current number of worker nodes that the managed node group should maintain. If not specified, the nodewgroup will initially create ``minSize`` instances. Default: 2
        :param disk_size: The root device disk size (in GiB) for your node group instances. Default: 20
        :param force_update: Force the update if the existing node group's pods are unable to be drained due to a pod disruption budget issue. If an update fails because pods could not be drained, you can force the update after it fails to terminate the old node whether or not any pods are running on the node. Default: true
        :param instance_type: The instance type to use for your node group. Currently, you can specify a single instance type for a node group. The default value for this parameter is ``t3.medium``. If you choose a GPU instance type, be sure to specify the ``AL2_x86_64_GPU`` with the amiType parameter. Default: t3.medium
        :param labels: The Kubernetes labels to be applied to the nodes in the node group when they are created. Default: - None
        :param max_size: The maximum number of worker nodes that the managed node group can scale out to. Managed node groups can support up to 100 nodes by default. Default: - desiredSize
        :param min_size: The minimum number of worker nodes that the managed node group can scale in to. This number must be greater than zero. Default: 1
        :param nodegroup_name: Name of the Nodegroup. Default: - resource ID
        :param node_role: The IAM role to associate with your node group. The Amazon EKS worker node kubelet daemon makes calls to AWS APIs on your behalf. Worker nodes receive permissions for these API calls through an IAM instance profile and associated policies. Before you can launch worker nodes and register them into a cluster, you must create an IAM role for those worker nodes to use when they are launched. Default: - None. Auto-generated if not specified.
        :param release_version: The AMI version of the Amazon EKS-optimized AMI to use with your node group (for example, ``1.14.7-YYYYMMDD``). Default: - The latest available AMI version for the node group's current Kubernetes version is used.
        :param remote_access: The remote access (SSH) configuration to use with your node group. Disabled by default, however, if you specify an Amazon EC2 SSH key but do not specify a source security group when you create a managed node group, then port 22 on the worker nodes is opened to the internet (0.0.0.0/0) Default: - disabled
        :param subnets: The subnets to use for the Auto Scaling group that is created for your node group. By specifying the SubnetSelection, the selected subnets will automatically apply required tags i.e. ``kubernetes.io/cluster/CLUSTER_NAME`` with a value of ``shared``, where ``CLUSTER_NAME`` is replaced with the name of your cluster. Default: - private subnets
        :param tags: The metadata to apply to the node group to assist with categorization and organization. Each tag consists of a key and an optional value, both of which you define. Node group tags do not propagate to any other resources associated with the node group, such as the Amazon EC2 instances or subnets. Default: - None

        stability
        :stability: experimental
        """
        props = NodegroupProps(cluster=cluster, ami_type=ami_type, desired_size=desired_size, disk_size=disk_size, force_update=force_update, instance_type=instance_type, labels=labels, max_size=max_size, min_size=min_size, nodegroup_name=nodegroup_name, node_role=node_role, release_version=release_version, remote_access=remote_access, subnets=subnets, tags=tags)

        jsii.create(Nodegroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromNodegroupName")
    @builtins.classmethod
    def from_nodegroup_name(cls, scope: aws_cdk.core.Construct, id: str, nodegroup_name: str) -> "INodegroup":
        """Import the Nodegroup from attributes.

        :param scope: -
        :param id: -
        :param nodegroup_name: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromNodegroupName", [scope, id, nodegroup_name])

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> "Cluster":
        """the Amazon EKS cluster resource.

        stability
        :stability: experimental
        attribute:
        :attribute:: ClusterName
        """
        return jsii.get(self, "cluster")

    @builtins.property
    @jsii.member(jsii_name="nodegroupArn")
    def nodegroup_arn(self) -> str:
        """ARN of the nodegroup.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "nodegroupArn")

    @builtins.property
    @jsii.member(jsii_name="nodegroupName")
    def nodegroup_name(self) -> str:
        """Nodegroup name.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "nodegroupName")

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        """IAM role of the instance profile for the nodegroup.

        stability
        :stability: experimental
        """
        return jsii.get(self, "role")


@jsii.enum(jsii_type="@aws-cdk/aws-eks.NodegroupAmiType")
class NodegroupAmiType(enum.Enum):
    """The AMI type for your node group.

    GPU instance types should use the ``AL2_x86_64_GPU`` AMI type, which uses the
    Amazon EKS-optimized Linux AMI with GPU support. Non-GPU instances should use the ``AL2_x86_64`` AMI type, which
    uses the Amazon EKS-optimized Linux AMI.

    stability
    :stability: experimental
    """
    AL2_X86_64 = "AL2_X86_64"
    """Amazon Linux 2.

    stability
    :stability: experimental
    """
    AL2_X86_64_GPU = "AL2_X86_64_GPU"
    """Amazon Linux 2 with GPU support.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-eks.NodegroupOptions", jsii_struct_bases=[], name_mapping={'ami_type': 'amiType', 'desired_size': 'desiredSize', 'disk_size': 'diskSize', 'force_update': 'forceUpdate', 'instance_type': 'instanceType', 'labels': 'labels', 'max_size': 'maxSize', 'min_size': 'minSize', 'nodegroup_name': 'nodegroupName', 'node_role': 'nodeRole', 'release_version': 'releaseVersion', 'remote_access': 'remoteAccess', 'subnets': 'subnets', 'tags': 'tags'})
class NodegroupOptions():
    def __init__(self, *, ami_type: typing.Optional["NodegroupAmiType"]=None, desired_size: typing.Optional[jsii.Number]=None, disk_size: typing.Optional[jsii.Number]=None, force_update: typing.Optional[bool]=None, instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType]=None, labels: typing.Optional[typing.Mapping[str, str]]=None, max_size: typing.Optional[jsii.Number]=None, min_size: typing.Optional[jsii.Number]=None, nodegroup_name: typing.Optional[str]=None, node_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, release_version: typing.Optional[str]=None, remote_access: typing.Optional["NodegroupRemoteAccess"]=None, subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, tags: typing.Optional[typing.Mapping[str, str]]=None) -> None:
        """The Nodegroup Options for addNodeGroup() method.

        :param ami_type: The AMI type for your node group. Default: AL2_x86_64
        :param desired_size: The current number of worker nodes that the managed node group should maintain. If not specified, the nodewgroup will initially create ``minSize`` instances. Default: 2
        :param disk_size: The root device disk size (in GiB) for your node group instances. Default: 20
        :param force_update: Force the update if the existing node group's pods are unable to be drained due to a pod disruption budget issue. If an update fails because pods could not be drained, you can force the update after it fails to terminate the old node whether or not any pods are running on the node. Default: true
        :param instance_type: The instance type to use for your node group. Currently, you can specify a single instance type for a node group. The default value for this parameter is ``t3.medium``. If you choose a GPU instance type, be sure to specify the ``AL2_x86_64_GPU`` with the amiType parameter. Default: t3.medium
        :param labels: The Kubernetes labels to be applied to the nodes in the node group when they are created. Default: - None
        :param max_size: The maximum number of worker nodes that the managed node group can scale out to. Managed node groups can support up to 100 nodes by default. Default: - desiredSize
        :param min_size: The minimum number of worker nodes that the managed node group can scale in to. This number must be greater than zero. Default: 1
        :param nodegroup_name: Name of the Nodegroup. Default: - resource ID
        :param node_role: The IAM role to associate with your node group. The Amazon EKS worker node kubelet daemon makes calls to AWS APIs on your behalf. Worker nodes receive permissions for these API calls through an IAM instance profile and associated policies. Before you can launch worker nodes and register them into a cluster, you must create an IAM role for those worker nodes to use when they are launched. Default: - None. Auto-generated if not specified.
        :param release_version: The AMI version of the Amazon EKS-optimized AMI to use with your node group (for example, ``1.14.7-YYYYMMDD``). Default: - The latest available AMI version for the node group's current Kubernetes version is used.
        :param remote_access: The remote access (SSH) configuration to use with your node group. Disabled by default, however, if you specify an Amazon EC2 SSH key but do not specify a source security group when you create a managed node group, then port 22 on the worker nodes is opened to the internet (0.0.0.0/0) Default: - disabled
        :param subnets: The subnets to use for the Auto Scaling group that is created for your node group. By specifying the SubnetSelection, the selected subnets will automatically apply required tags i.e. ``kubernetes.io/cluster/CLUSTER_NAME`` with a value of ``shared``, where ``CLUSTER_NAME`` is replaced with the name of your cluster. Default: - private subnets
        :param tags: The metadata to apply to the node group to assist with categorization and organization. Each tag consists of a key and an optional value, both of which you define. Node group tags do not propagate to any other resources associated with the node group, such as the Amazon EC2 instances or subnets. Default: - None

        stability
        :stability: experimental
        """
        if isinstance(remote_access, dict): remote_access = NodegroupRemoteAccess(**remote_access)
        if isinstance(subnets, dict): subnets = aws_cdk.aws_ec2.SubnetSelection(**subnets)
        self._values = {
        }
        if ami_type is not None: self._values["ami_type"] = ami_type
        if desired_size is not None: self._values["desired_size"] = desired_size
        if disk_size is not None: self._values["disk_size"] = disk_size
        if force_update is not None: self._values["force_update"] = force_update
        if instance_type is not None: self._values["instance_type"] = instance_type
        if labels is not None: self._values["labels"] = labels
        if max_size is not None: self._values["max_size"] = max_size
        if min_size is not None: self._values["min_size"] = min_size
        if nodegroup_name is not None: self._values["nodegroup_name"] = nodegroup_name
        if node_role is not None: self._values["node_role"] = node_role
        if release_version is not None: self._values["release_version"] = release_version
        if remote_access is not None: self._values["remote_access"] = remote_access
        if subnets is not None: self._values["subnets"] = subnets
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def ami_type(self) -> typing.Optional["NodegroupAmiType"]:
        """The AMI type for your node group.

        default
        :default: AL2_x86_64

        stability
        :stability: experimental
        """
        return self._values.get('ami_type')

    @builtins.property
    def desired_size(self) -> typing.Optional[jsii.Number]:
        """The current number of worker nodes that the managed node group should maintain.

        If not specified,
        the nodewgroup will initially create ``minSize`` instances.

        default
        :default: 2

        stability
        :stability: experimental
        """
        return self._values.get('desired_size')

    @builtins.property
    def disk_size(self) -> typing.Optional[jsii.Number]:
        """The root device disk size (in GiB) for your node group instances.

        default
        :default: 20

        stability
        :stability: experimental
        """
        return self._values.get('disk_size')

    @builtins.property
    def force_update(self) -> typing.Optional[bool]:
        """Force the update if the existing node group's pods are unable to be drained due to a pod disruption budget issue.

        If an update fails because pods could not be drained, you can force the update after it fails to terminate the old
        node whether or not any pods are
        running on the node.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('force_update')

    @builtins.property
    def instance_type(self) -> typing.Optional[aws_cdk.aws_ec2.InstanceType]:
        """The instance type to use for your node group.

        Currently, you can specify a single instance type for a node group.
        The default value for this parameter is ``t3.medium``. If you choose a GPU instance type, be sure to specify the
        ``AL2_x86_64_GPU`` with the amiType parameter.

        default
        :default: t3.medium

        stability
        :stability: experimental
        """
        return self._values.get('instance_type')

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The Kubernetes labels to be applied to the nodes in the node group when they are created.

        default
        :default: - None

        stability
        :stability: experimental
        """
        return self._values.get('labels')

    @builtins.property
    def max_size(self) -> typing.Optional[jsii.Number]:
        """The maximum number of worker nodes that the managed node group can scale out to.

        Managed node groups can support up to 100 nodes by default.

        default
        :default: - desiredSize

        stability
        :stability: experimental
        """
        return self._values.get('max_size')

    @builtins.property
    def min_size(self) -> typing.Optional[jsii.Number]:
        """The minimum number of worker nodes that the managed node group can scale in to.

        This number must be greater than zero.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('min_size')

    @builtins.property
    def nodegroup_name(self) -> typing.Optional[str]:
        """Name of the Nodegroup.

        default
        :default: - resource ID

        stability
        :stability: experimental
        """
        return self._values.get('nodegroup_name')

    @builtins.property
    def node_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The IAM role to associate with your node group.

        The Amazon EKS worker node kubelet daemon
        makes calls to AWS APIs on your behalf. Worker nodes receive permissions for these API calls through
        an IAM instance profile and associated policies. Before you can launch worker nodes and register them
        into a cluster, you must create an IAM role for those worker nodes to use when they are launched.

        default
        :default: - None. Auto-generated if not specified.

        stability
        :stability: experimental
        """
        return self._values.get('node_role')

    @builtins.property
    def release_version(self) -> typing.Optional[str]:
        """The AMI version of the Amazon EKS-optimized AMI to use with your node group (for example, ``1.14.7-YYYYMMDD``).

        default
        :default: - The latest available AMI version for the node group's current Kubernetes version is used.

        stability
        :stability: experimental
        """
        return self._values.get('release_version')

    @builtins.property
    def remote_access(self) -> typing.Optional["NodegroupRemoteAccess"]:
        """The remote access (SSH) configuration to use with your node group.

        Disabled by default, however, if you
        specify an Amazon EC2 SSH key but do not specify a source security group when you create a managed node group,
        then port 22 on the worker nodes is opened to the internet (0.0.0.0/0)

        default
        :default: - disabled

        stability
        :stability: experimental
        """
        return self._values.get('remote_access')

    @builtins.property
    def subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """The subnets to use for the Auto Scaling group that is created for your node group.

        By specifying the
        SubnetSelection, the selected subnets will automatically apply required tags i.e.
        ``kubernetes.io/cluster/CLUSTER_NAME`` with a value of ``shared``, where ``CLUSTER_NAME`` is replaced with
        the name of your cluster.

        default
        :default: - private subnets

        stability
        :stability: experimental
        """
        return self._values.get('subnets')

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The metadata to apply to the node group to assist with categorization and organization.

        Each tag consists of
        a key and an optional value, both of which you define. Node group tags do not propagate to any other resources
        associated with the node group, such as the Amazon EC2 instances or subnets.

        default
        :default: - None

        stability
        :stability: experimental
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NodegroupOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-eks.NodegroupProps", jsii_struct_bases=[NodegroupOptions], name_mapping={'ami_type': 'amiType', 'desired_size': 'desiredSize', 'disk_size': 'diskSize', 'force_update': 'forceUpdate', 'instance_type': 'instanceType', 'labels': 'labels', 'max_size': 'maxSize', 'min_size': 'minSize', 'nodegroup_name': 'nodegroupName', 'node_role': 'nodeRole', 'release_version': 'releaseVersion', 'remote_access': 'remoteAccess', 'subnets': 'subnets', 'tags': 'tags', 'cluster': 'cluster'})
class NodegroupProps(NodegroupOptions):
    def __init__(self, *, ami_type: typing.Optional["NodegroupAmiType"]=None, desired_size: typing.Optional[jsii.Number]=None, disk_size: typing.Optional[jsii.Number]=None, force_update: typing.Optional[bool]=None, instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType]=None, labels: typing.Optional[typing.Mapping[str, str]]=None, max_size: typing.Optional[jsii.Number]=None, min_size: typing.Optional[jsii.Number]=None, nodegroup_name: typing.Optional[str]=None, node_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, release_version: typing.Optional[str]=None, remote_access: typing.Optional["NodegroupRemoteAccess"]=None, subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, tags: typing.Optional[typing.Mapping[str, str]]=None, cluster: "Cluster") -> None:
        """NodeGroup properties interface.

        :param ami_type: The AMI type for your node group. Default: AL2_x86_64
        :param desired_size: The current number of worker nodes that the managed node group should maintain. If not specified, the nodewgroup will initially create ``minSize`` instances. Default: 2
        :param disk_size: The root device disk size (in GiB) for your node group instances. Default: 20
        :param force_update: Force the update if the existing node group's pods are unable to be drained due to a pod disruption budget issue. If an update fails because pods could not be drained, you can force the update after it fails to terminate the old node whether or not any pods are running on the node. Default: true
        :param instance_type: The instance type to use for your node group. Currently, you can specify a single instance type for a node group. The default value for this parameter is ``t3.medium``. If you choose a GPU instance type, be sure to specify the ``AL2_x86_64_GPU`` with the amiType parameter. Default: t3.medium
        :param labels: The Kubernetes labels to be applied to the nodes in the node group when they are created. Default: - None
        :param max_size: The maximum number of worker nodes that the managed node group can scale out to. Managed node groups can support up to 100 nodes by default. Default: - desiredSize
        :param min_size: The minimum number of worker nodes that the managed node group can scale in to. This number must be greater than zero. Default: 1
        :param nodegroup_name: Name of the Nodegroup. Default: - resource ID
        :param node_role: The IAM role to associate with your node group. The Amazon EKS worker node kubelet daemon makes calls to AWS APIs on your behalf. Worker nodes receive permissions for these API calls through an IAM instance profile and associated policies. Before you can launch worker nodes and register them into a cluster, you must create an IAM role for those worker nodes to use when they are launched. Default: - None. Auto-generated if not specified.
        :param release_version: The AMI version of the Amazon EKS-optimized AMI to use with your node group (for example, ``1.14.7-YYYYMMDD``). Default: - The latest available AMI version for the node group's current Kubernetes version is used.
        :param remote_access: The remote access (SSH) configuration to use with your node group. Disabled by default, however, if you specify an Amazon EC2 SSH key but do not specify a source security group when you create a managed node group, then port 22 on the worker nodes is opened to the internet (0.0.0.0/0) Default: - disabled
        :param subnets: The subnets to use for the Auto Scaling group that is created for your node group. By specifying the SubnetSelection, the selected subnets will automatically apply required tags i.e. ``kubernetes.io/cluster/CLUSTER_NAME`` with a value of ``shared``, where ``CLUSTER_NAME`` is replaced with the name of your cluster. Default: - private subnets
        :param tags: The metadata to apply to the node group to assist with categorization and organization. Each tag consists of a key and an optional value, both of which you define. Node group tags do not propagate to any other resources associated with the node group, such as the Amazon EC2 instances or subnets. Default: - None
        :param cluster: Cluster resource [disable-awslint:ref-via-interface]".

        stability
        :stability: experimental
        """
        if isinstance(remote_access, dict): remote_access = NodegroupRemoteAccess(**remote_access)
        if isinstance(subnets, dict): subnets = aws_cdk.aws_ec2.SubnetSelection(**subnets)
        self._values = {
            'cluster': cluster,
        }
        if ami_type is not None: self._values["ami_type"] = ami_type
        if desired_size is not None: self._values["desired_size"] = desired_size
        if disk_size is not None: self._values["disk_size"] = disk_size
        if force_update is not None: self._values["force_update"] = force_update
        if instance_type is not None: self._values["instance_type"] = instance_type
        if labels is not None: self._values["labels"] = labels
        if max_size is not None: self._values["max_size"] = max_size
        if min_size is not None: self._values["min_size"] = min_size
        if nodegroup_name is not None: self._values["nodegroup_name"] = nodegroup_name
        if node_role is not None: self._values["node_role"] = node_role
        if release_version is not None: self._values["release_version"] = release_version
        if remote_access is not None: self._values["remote_access"] = remote_access
        if subnets is not None: self._values["subnets"] = subnets
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def ami_type(self) -> typing.Optional["NodegroupAmiType"]:
        """The AMI type for your node group.

        default
        :default: AL2_x86_64

        stability
        :stability: experimental
        """
        return self._values.get('ami_type')

    @builtins.property
    def desired_size(self) -> typing.Optional[jsii.Number]:
        """The current number of worker nodes that the managed node group should maintain.

        If not specified,
        the nodewgroup will initially create ``minSize`` instances.

        default
        :default: 2

        stability
        :stability: experimental
        """
        return self._values.get('desired_size')

    @builtins.property
    def disk_size(self) -> typing.Optional[jsii.Number]:
        """The root device disk size (in GiB) for your node group instances.

        default
        :default: 20

        stability
        :stability: experimental
        """
        return self._values.get('disk_size')

    @builtins.property
    def force_update(self) -> typing.Optional[bool]:
        """Force the update if the existing node group's pods are unable to be drained due to a pod disruption budget issue.

        If an update fails because pods could not be drained, you can force the update after it fails to terminate the old
        node whether or not any pods are
        running on the node.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('force_update')

    @builtins.property
    def instance_type(self) -> typing.Optional[aws_cdk.aws_ec2.InstanceType]:
        """The instance type to use for your node group.

        Currently, you can specify a single instance type for a node group.
        The default value for this parameter is ``t3.medium``. If you choose a GPU instance type, be sure to specify the
        ``AL2_x86_64_GPU`` with the amiType parameter.

        default
        :default: t3.medium

        stability
        :stability: experimental
        """
        return self._values.get('instance_type')

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The Kubernetes labels to be applied to the nodes in the node group when they are created.

        default
        :default: - None

        stability
        :stability: experimental
        """
        return self._values.get('labels')

    @builtins.property
    def max_size(self) -> typing.Optional[jsii.Number]:
        """The maximum number of worker nodes that the managed node group can scale out to.

        Managed node groups can support up to 100 nodes by default.

        default
        :default: - desiredSize

        stability
        :stability: experimental
        """
        return self._values.get('max_size')

    @builtins.property
    def min_size(self) -> typing.Optional[jsii.Number]:
        """The minimum number of worker nodes that the managed node group can scale in to.

        This number must be greater than zero.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('min_size')

    @builtins.property
    def nodegroup_name(self) -> typing.Optional[str]:
        """Name of the Nodegroup.

        default
        :default: - resource ID

        stability
        :stability: experimental
        """
        return self._values.get('nodegroup_name')

    @builtins.property
    def node_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The IAM role to associate with your node group.

        The Amazon EKS worker node kubelet daemon
        makes calls to AWS APIs on your behalf. Worker nodes receive permissions for these API calls through
        an IAM instance profile and associated policies. Before you can launch worker nodes and register them
        into a cluster, you must create an IAM role for those worker nodes to use when they are launched.

        default
        :default: - None. Auto-generated if not specified.

        stability
        :stability: experimental
        """
        return self._values.get('node_role')

    @builtins.property
    def release_version(self) -> typing.Optional[str]:
        """The AMI version of the Amazon EKS-optimized AMI to use with your node group (for example, ``1.14.7-YYYYMMDD``).

        default
        :default: - The latest available AMI version for the node group's current Kubernetes version is used.

        stability
        :stability: experimental
        """
        return self._values.get('release_version')

    @builtins.property
    def remote_access(self) -> typing.Optional["NodegroupRemoteAccess"]:
        """The remote access (SSH) configuration to use with your node group.

        Disabled by default, however, if you
        specify an Amazon EC2 SSH key but do not specify a source security group when you create a managed node group,
        then port 22 on the worker nodes is opened to the internet (0.0.0.0/0)

        default
        :default: - disabled

        stability
        :stability: experimental
        """
        return self._values.get('remote_access')

    @builtins.property
    def subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """The subnets to use for the Auto Scaling group that is created for your node group.

        By specifying the
        SubnetSelection, the selected subnets will automatically apply required tags i.e.
        ``kubernetes.io/cluster/CLUSTER_NAME`` with a value of ``shared``, where ``CLUSTER_NAME`` is replaced with
        the name of your cluster.

        default
        :default: - private subnets

        stability
        :stability: experimental
        """
        return self._values.get('subnets')

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The metadata to apply to the node group to assist with categorization and organization.

        Each tag consists of
        a key and an optional value, both of which you define. Node group tags do not propagate to any other resources
        associated with the node group, such as the Amazon EC2 instances or subnets.

        default
        :default: - None

        stability
        :stability: experimental
        """
        return self._values.get('tags')

    @builtins.property
    def cluster(self) -> "Cluster":
        """Cluster resource [disable-awslint:ref-via-interface]".

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NodegroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-eks.NodegroupRemoteAccess", jsii_struct_bases=[], name_mapping={'ssh_key_name': 'sshKeyName', 'source_security_groups': 'sourceSecurityGroups'})
class NodegroupRemoteAccess():
    def __init__(self, *, ssh_key_name: str, source_security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]=None) -> None:
        """The remote access (SSH) configuration to use with your node group.

        :param ssh_key_name: The Amazon EC2 SSH key that provides access for SSH communication with the worker nodes in the managed node group.
        :param source_security_groups: The security groups that are allowed SSH access (port 22) to the worker nodes. If you specify an Amazon EC2 SSH key but do not specify a source security group when you create a managed node group, then port 22 on the worker nodes is opened to the internet (0.0.0.0/0). Default: - port 22 on the worker nodes is opened to the internet (0.0.0.0/0)

        see
        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-remoteaccess.html
        stability
        :stability: experimental
        """
        self._values = {
            'ssh_key_name': ssh_key_name,
        }
        if source_security_groups is not None: self._values["source_security_groups"] = source_security_groups

    @builtins.property
    def ssh_key_name(self) -> str:
        """The Amazon EC2 SSH key that provides access for SSH communication with the worker nodes in the managed node group.

        stability
        :stability: experimental
        """
        return self._values.get('ssh_key_name')

    @builtins.property
    def source_security_groups(self) -> typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]:
        """The security groups that are allowed SSH access (port 22) to the worker nodes.

        If you specify an Amazon EC2 SSH
        key but do not specify a source security group when you create a managed node group, then port 22 on the worker
        nodes is opened to the internet (0.0.0.0/0).

        default
        :default: - port 22 on the worker nodes is opened to the internet (0.0.0.0/0)

        stability
        :stability: experimental
        """
        return self._values.get('source_security_groups')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NodegroupRemoteAccess(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-eks.PatchType")
class PatchType(enum.Enum):
    """Values for ``kubectl patch`` --type argument.

    stability
    :stability: experimental
    """
    JSON = "JSON"
    """JSON Patch, RFC 6902.

    stability
    :stability: experimental
    """
    MERGE = "MERGE"
    """JSON Merge patch.

    stability
    :stability: experimental
    """
    STRATEGIC = "STRATEGIC"
    """Strategic merge patch.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-eks.Selector", jsii_struct_bases=[], name_mapping={'namespace': 'namespace', 'labels': 'labels'})
class Selector():
    def __init__(self, *, namespace: str, labels: typing.Optional[typing.Mapping[str, str]]=None) -> None:
        """Fargate profile selector.

        :param namespace: The Kubernetes namespace that the selector should match. You must specify a namespace for a selector. The selector only matches pods that are created in this namespace, but you can create multiple selectors to target multiple namespaces.
        :param labels: The Kubernetes labels that the selector should match. A pod must contain all of the labels that are specified in the selector for it to be considered a match. Default: - all pods within the namespace will be selected.

        stability
        :stability: experimental
        """
        self._values = {
            'namespace': namespace,
        }
        if labels is not None: self._values["labels"] = labels

    @builtins.property
    def namespace(self) -> str:
        """The Kubernetes namespace that the selector should match.

        You must specify a namespace for a selector. The selector only matches pods
        that are created in this namespace, but you can create multiple selectors
        to target multiple namespaces.

        stability
        :stability: experimental
        """
        return self._values.get('namespace')

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The Kubernetes labels that the selector should match.

        A pod must contain
        all of the labels that are specified in the selector for it to be
        considered a match.

        default
        :default: - all pods within the namespace will be selected.

        stability
        :stability: experimental
        """
        return self._values.get('labels')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'Selector(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.aws_iam.IPrincipal)
class ServiceAccount(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-eks.ServiceAccount"):
    """Service Account.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, cluster: "Cluster", name: typing.Optional[str]=None, namespace: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param cluster: The cluster to apply the patch to. [disable-awslint:ref-via-interface]
        :param name: The name of the service account. Default: - If no name is given, it will use the id of the resource.
        :param namespace: The namespace of the service account. Default: "default"

        stability
        :stability: experimental
        """
        props = ServiceAccountProps(cluster=cluster, name=name, namespace=namespace)

        jsii.create(ServiceAccount, self, [scope, id, props])

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> bool:
        """Add to the policy of this principal.

        :param statement: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addToPolicy", [statement])

    @jsii.member(jsii_name="addToPrincipalPolicy")
    def add_to_principal_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> aws_cdk.aws_iam.AddToPrincipalPolicyResult:
        """Add to the policy of this principal.

        :param statement: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addToPrincipalPolicy", [statement])

    @builtins.property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> str:
        """When this Principal is used in an AssumeRole policy, the action to use.

        stability
        :stability: experimental
        """
        return jsii.get(self, "assumeRoleAction")

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> aws_cdk.aws_iam.IPrincipal:
        """The principal to grant permissions to.

        stability
        :stability: experimental
        """
        return jsii.get(self, "grantPrincipal")

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> aws_cdk.aws_iam.PrincipalPolicyFragment:
        """Return the policy fragment that identifies this principal in a Policy.

        stability
        :stability: experimental
        """
        return jsii.get(self, "policyFragment")

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        """The role which is linked to the service account.

        stability
        :stability: experimental
        """
        return jsii.get(self, "role")

    @builtins.property
    @jsii.member(jsii_name="serviceAccountName")
    def service_account_name(self) -> str:
        """The name of the service account.

        stability
        :stability: experimental
        """
        return jsii.get(self, "serviceAccountName")

    @builtins.property
    @jsii.member(jsii_name="serviceAccountNamespace")
    def service_account_namespace(self) -> str:
        """The namespace where the service account is located in.

        stability
        :stability: experimental
        """
        return jsii.get(self, "serviceAccountNamespace")


@jsii.data_type(jsii_type="@aws-cdk/aws-eks.ServiceAccountOptions", jsii_struct_bases=[], name_mapping={'name': 'name', 'namespace': 'namespace'})
class ServiceAccountOptions():
    def __init__(self, *, name: typing.Optional[str]=None, namespace: typing.Optional[str]=None) -> None:
        """Options for ``ServiceAccount``.

        :param name: The name of the service account. Default: - If no name is given, it will use the id of the resource.
        :param namespace: The namespace of the service account. Default: "default"

        stability
        :stability: experimental
        """
        self._values = {
        }
        if name is not None: self._values["name"] = name
        if namespace is not None: self._values["namespace"] = namespace

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """The name of the service account.

        default
        :default: - If no name is given, it will use the id of the resource.

        stability
        :stability: experimental
        """
        return self._values.get('name')

    @builtins.property
    def namespace(self) -> typing.Optional[str]:
        """The namespace of the service account.

        default
        :default: "default"

        stability
        :stability: experimental
        """
        return self._values.get('namespace')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ServiceAccountOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-eks.ServiceAccountProps", jsii_struct_bases=[ServiceAccountOptions], name_mapping={'name': 'name', 'namespace': 'namespace', 'cluster': 'cluster'})
class ServiceAccountProps(ServiceAccountOptions):
    def __init__(self, *, name: typing.Optional[str]=None, namespace: typing.Optional[str]=None, cluster: "Cluster") -> None:
        """Properties for defining service accounts.

        :param name: The name of the service account. Default: - If no name is given, it will use the id of the resource.
        :param namespace: The namespace of the service account. Default: "default"
        :param cluster: The cluster to apply the patch to. [disable-awslint:ref-via-interface]

        stability
        :stability: experimental
        """
        self._values = {
            'cluster': cluster,
        }
        if name is not None: self._values["name"] = name
        if namespace is not None: self._values["namespace"] = namespace

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """The name of the service account.

        default
        :default: - If no name is given, it will use the id of the resource.

        stability
        :stability: experimental
        """
        return self._values.get('name')

    @builtins.property
    def namespace(self) -> typing.Optional[str]:
        """The namespace of the service account.

        default
        :default: "default"

        stability
        :stability: experimental
        """
        return self._values.get('namespace')

    @builtins.property
    def cluster(self) -> "Cluster":
        """The cluster to apply the patch to.

        [disable-awslint:ref-via-interface]

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ServiceAccountProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(ICluster)
class Cluster(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-eks.Cluster"):
    """A Cluster represents a managed Kubernetes Service (EKS).

    This is a fully managed cluster of API Servers (control-plane)
    The user is still required to create the worker nodes.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, default_capacity: typing.Optional[jsii.Number]=None, default_capacity_instance: typing.Optional[aws_cdk.aws_ec2.InstanceType]=None, default_capacity_type: typing.Optional["DefaultCapacityType"]=None, kubectl_enabled: typing.Optional[bool]=None, cluster_name: typing.Optional[str]=None, core_dns_compute_type: typing.Optional["CoreDnsComputeType"]=None, masters_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, output_cluster_name: typing.Optional[bool]=None, output_config_command: typing.Optional[bool]=None, output_masters_role_arn: typing.Optional[bool]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None, version: typing.Optional[str]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None, vpc_subnets: typing.Optional[typing.List[aws_cdk.aws_ec2.SubnetSelection]]=None) -> None:
        """Initiates an EKS Cluster with the supplied arguments.

        :param scope: a Construct, most likely a cdk.Stack created.
        :param id: -
        :param default_capacity: Number of instances to allocate as an initial capacity for this cluster. Instance type can be configured through ``defaultCapacityInstanceType``, which defaults to ``m5.large``. Use ``cluster.addCapacity`` to add additional customized capacity. Set this to ``0`` is you wish to avoid the initial capacity allocation. Default: 2
        :param default_capacity_instance: The instance type to use for the default capacity. This will only be taken into account if ``defaultCapacity`` is > 0. Default: m5.large
        :param default_capacity_type: The default capacity type for the cluster. Default: NODEGROUP
        :param kubectl_enabled: Allows defining ``kubectrl``-related resources on this cluster. If this is disabled, it will not be possible to use the following capabilities: - ``addResource`` - ``addRoleMapping`` - ``addUserMapping`` - ``addMastersRole`` and ``props.mastersRole`` If this is disabled, the cluster can only be managed by issuing ``kubectl`` commands from a session that uses the IAM role/user that created the account. *NOTE*: changing this value will destoy the cluster. This is because a managable cluster must be created using an AWS CloudFormation custom resource which executes with an IAM role owned by the CDK app. Default: true The cluster can be managed by the AWS CDK application.
        :param cluster_name: Name for the cluster. Default: - Automatically generated name
        :param core_dns_compute_type: Controls the "eks.amazonaws.com/compute-type" annotation in the CoreDNS configuration on your cluster to determine which compute type to use for CoreDNS. Default: CoreDnsComputeType.EC2 (for ``FargateCluster`` the default is FARGATE)
        :param masters_role: An IAM role that will be added to the ``system:masters`` Kubernetes RBAC group. Default: - By default, it will only possible to update this Kubernetes system by adding resources to this cluster via ``addResource`` or by defining ``KubernetesResource`` resources in your AWS CDK app. Use this if you wish to grant cluster administration privileges to another role.
        :param output_cluster_name: Determines whether a CloudFormation output with the name of the cluster will be synthesized. Default: false
        :param output_config_command: Determines whether a CloudFormation output with the ``aws eks update-kubeconfig`` command will be synthesized. This command will include the cluster name and, if applicable, the ARN of the masters IAM role. Default: true
        :param output_masters_role_arn: Determines whether a CloudFormation output with the ARN of the "masters" IAM role will be synthesized (if ``mastersRole`` is specified). Default: false
        :param role: Role that provides permissions for the Kubernetes control plane to make calls to AWS API operations on your behalf. Default: - A role is automatically created for you
        :param security_group: Security Group to use for Control Plane ENIs. Default: - A security group is automatically created
        :param version: The Kubernetes version to run in the cluster. Default: - If not supplied, will use Amazon default version
        :param vpc: The VPC in which to create the Cluster. Default: - a VPC with default configuration will be created and can be accessed through ``cluster.vpc``.
        :param vpc_subnets: Where to place EKS Control Plane ENIs. If you want to create public load balancers, this must include public subnets. For example, to only select private subnets, supply the following:: vpcSubnets: [ { subnetType: ec2.SubnetType.Private } ] Default: - All public and private subnets

        stability
        :stability: experimental
        """
        props = ClusterProps(default_capacity=default_capacity, default_capacity_instance=default_capacity_instance, default_capacity_type=default_capacity_type, kubectl_enabled=kubectl_enabled, cluster_name=cluster_name, core_dns_compute_type=core_dns_compute_type, masters_role=masters_role, output_cluster_name=output_cluster_name, output_config_command=output_config_command, output_masters_role_arn=output_masters_role_arn, role=role, security_group=security_group, version=version, vpc=vpc, vpc_subnets=vpc_subnets)

        jsii.create(Cluster, self, [scope, id, props])

    @jsii.member(jsii_name="fromClusterAttributes")
    @builtins.classmethod
    def from_cluster_attributes(cls, scope: aws_cdk.core.Construct, id: str, *, cluster_arn: str, cluster_certificate_authority_data: str, cluster_encryption_config_key_arn: str, cluster_endpoint: str, cluster_name: str, cluster_security_group_id: str, security_groups: typing.List[aws_cdk.aws_ec2.ISecurityGroup], vpc: aws_cdk.aws_ec2.IVpc) -> "ICluster":
        """Import an existing cluster.

        :param scope: the construct scope, in most cases 'this'.
        :param id: the id or name to import as.
        :param cluster_arn: The unique ARN assigned to the service by AWS in the form of arn:aws:eks:.
        :param cluster_certificate_authority_data: The certificate-authority-data for your cluster.
        :param cluster_encryption_config_key_arn: Amazon Resource Name (ARN) or alias of the customer master key (CMK).
        :param cluster_endpoint: The API Server endpoint URL.
        :param cluster_name: The physical name of the Cluster.
        :param cluster_security_group_id: The cluster security group that was created by Amazon EKS for the cluster.
        :param security_groups: The security groups associated with this cluster.
        :param vpc: The VPC in which this Cluster was created.

        stability
        :stability: experimental
        """
        attrs = ClusterAttributes(cluster_arn=cluster_arn, cluster_certificate_authority_data=cluster_certificate_authority_data, cluster_encryption_config_key_arn=cluster_encryption_config_key_arn, cluster_endpoint=cluster_endpoint, cluster_name=cluster_name, cluster_security_group_id=cluster_security_group_id, security_groups=security_groups, vpc=vpc)

        return jsii.sinvoke(cls, "fromClusterAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="addAutoScalingGroup")
    def add_auto_scaling_group(self, auto_scaling_group: aws_cdk.aws_autoscaling.AutoScalingGroup, *, bootstrap_enabled: typing.Optional[bool]=None, bootstrap_options: typing.Optional["BootstrapOptions"]=None, machine_image_type: typing.Optional["MachineImageType"]=None, map_role: typing.Optional[bool]=None) -> None:
        """Add compute capacity to this EKS cluster in the form of an AutoScalingGroup.

        The AutoScalingGroup must be running an EKS-optimized AMI containing the
        /etc/eks/bootstrap.sh script. This method will configure Security Groups,
        add the right policies to the instance role, apply the right tags, and add
        the required user data to the instance's launch configuration.

        Spot instances will be labeled ``lifecycle=Ec2Spot`` and tainted with ``PreferNoSchedule``.
        If kubectl is enabled, the
        `spot interrupt handler <https://github.com/awslabs/ec2-spot-labs/tree/master/ec2-spot-eks-solution/spot-termination-handler>`_
        daemon will be installed on all spot instances to handle
        `EC2 Spot Instance Termination Notices <https://aws.amazon.com/blogs/aws/new-ec2-spot-instance-termination-notices/>`_.

        Prefer to use ``addCapacity`` if possible.

        :param auto_scaling_group: [disable-awslint:ref-via-interface].
        :param bootstrap_enabled: Configures the EC2 user-data script for instances in this autoscaling group to bootstrap the node (invoke ``/etc/eks/bootstrap.sh``) and associate it with the EKS cluster. If you wish to provide a custom user data script, set this to ``false`` and manually invoke ``autoscalingGroup.addUserData()``. Default: true
        :param bootstrap_options: Allows options for node bootstrapping through EC2 user data. Default: - default options
        :param machine_image_type: Allow options to specify different machine image type. Default: MachineImageType.AMAZON_LINUX_2
        :param map_role: Will automatically update the aws-auth ConfigMap to map the IAM instance role to RBAC. This cannot be explicitly set to ``true`` if the cluster has kubectl disabled. Default: - true if the cluster has kubectl enabled (which is the default).

        see
        :see: https://docs.aws.amazon.com/eks/latest/userguide/launch-workers.html
        stability
        :stability: experimental
        """
        options = AutoScalingGroupOptions(bootstrap_enabled=bootstrap_enabled, bootstrap_options=bootstrap_options, machine_image_type=machine_image_type, map_role=map_role)

        return jsii.invoke(self, "addAutoScalingGroup", [auto_scaling_group, options])

    @jsii.member(jsii_name="addCapacity")
    def add_capacity(self, id: str, *, instance_type: aws_cdk.aws_ec2.InstanceType, bootstrap_enabled: typing.Optional[bool]=None, bootstrap_options: typing.Optional["BootstrapOptions"]=None, machine_image_type: typing.Optional["MachineImageType"]=None, map_role: typing.Optional[bool]=None, allow_all_outbound: typing.Optional[bool]=None, associate_public_ip_address: typing.Optional[bool]=None, block_devices: typing.Optional[typing.List[aws_cdk.aws_autoscaling.BlockDevice]]=None, cooldown: typing.Optional[aws_cdk.core.Duration]=None, desired_capacity: typing.Optional[jsii.Number]=None, health_check: typing.Optional[aws_cdk.aws_autoscaling.HealthCheck]=None, ignore_unmodified_size_properties: typing.Optional[bool]=None, instance_monitoring: typing.Optional[aws_cdk.aws_autoscaling.Monitoring]=None, key_name: typing.Optional[str]=None, max_capacity: typing.Optional[jsii.Number]=None, max_instance_lifetime: typing.Optional[aws_cdk.core.Duration]=None, min_capacity: typing.Optional[jsii.Number]=None, notifications: typing.Optional[typing.List[aws_cdk.aws_autoscaling.NotificationConfiguration]]=None, notifications_topic: typing.Optional[aws_cdk.aws_sns.ITopic]=None, replacing_update_min_successful_instances_percent: typing.Optional[jsii.Number]=None, resource_signal_count: typing.Optional[jsii.Number]=None, resource_signal_timeout: typing.Optional[aws_cdk.core.Duration]=None, rolling_update_configuration: typing.Optional[aws_cdk.aws_autoscaling.RollingUpdateConfiguration]=None, spot_price: typing.Optional[str]=None, update_type: typing.Optional[aws_cdk.aws_autoscaling.UpdateType]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None) -> aws_cdk.aws_autoscaling.AutoScalingGroup:
        """Add nodes to this EKS cluster.

        The nodes will automatically be configured with the right VPC and AMI
        for the instance type and Kubernetes version.

        Spot instances will be labeled ``lifecycle=Ec2Spot`` and tainted with ``PreferNoSchedule``.
        If kubectl is enabled, the
        `spot interrupt handler <https://github.com/awslabs/ec2-spot-labs/tree/master/ec2-spot-eks-solution/spot-termination-handler>`_
        daemon will be installed on all spot instances to handle
        `EC2 Spot Instance Termination Notices <https://aws.amazon.com/blogs/aws/new-ec2-spot-instance-termination-notices/>`_.

        :param id: -
        :param instance_type: Instance type of the instances to start.
        :param bootstrap_enabled: Configures the EC2 user-data script for instances in this autoscaling group to bootstrap the node (invoke ``/etc/eks/bootstrap.sh``) and associate it with the EKS cluster. If you wish to provide a custom user data script, set this to ``false`` and manually invoke ``autoscalingGroup.addUserData()``. Default: true
        :param bootstrap_options: EKS node bootstrapping options. Default: - none
        :param machine_image_type: Machine image type. Default: MachineImageType.AMAZON_LINUX_2
        :param map_role: Will automatically update the aws-auth ConfigMap to map the IAM instance role to RBAC. This cannot be explicitly set to ``true`` if the cluster has kubectl disabled. Default: - true if the cluster has kubectl enabled (which is the default).
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
        options = CapacityOptions(instance_type=instance_type, bootstrap_enabled=bootstrap_enabled, bootstrap_options=bootstrap_options, machine_image_type=machine_image_type, map_role=map_role, allow_all_outbound=allow_all_outbound, associate_public_ip_address=associate_public_ip_address, block_devices=block_devices, cooldown=cooldown, desired_capacity=desired_capacity, health_check=health_check, ignore_unmodified_size_properties=ignore_unmodified_size_properties, instance_monitoring=instance_monitoring, key_name=key_name, max_capacity=max_capacity, max_instance_lifetime=max_instance_lifetime, min_capacity=min_capacity, notifications=notifications, notifications_topic=notifications_topic, replacing_update_min_successful_instances_percent=replacing_update_min_successful_instances_percent, resource_signal_count=resource_signal_count, resource_signal_timeout=resource_signal_timeout, rolling_update_configuration=rolling_update_configuration, spot_price=spot_price, update_type=update_type, vpc_subnets=vpc_subnets)

        return jsii.invoke(self, "addCapacity", [id, options])

    @jsii.member(jsii_name="addChart")
    def add_chart(self, id: str, *, chart: str, create_namespace: typing.Optional[bool]=None, namespace: typing.Optional[str]=None, release: typing.Optional[str]=None, repository: typing.Optional[str]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None, values: typing.Optional[typing.Mapping[str, typing.Any]]=None, version: typing.Optional[str]=None, wait: typing.Optional[bool]=None) -> "HelmChart":
        """Defines a Helm chart in this cluster.

        :param id: logical id of this chart.
        :param chart: The name of the chart.
        :param create_namespace: create namespace if not exist. Default: true
        :param namespace: The Kubernetes namespace scope of the requests. Default: default
        :param release: The name of the release. Default: - If no release name is given, it will use the last 53 characters of the node's unique id.
        :param repository: The repository which contains the chart. For example: https://kubernetes-charts.storage.googleapis.com/ Default: - No repository will be used, which means that the chart needs to be an absolute URL.
        :param timeout: Amount of time to wait for any individual Kubernetes operation. Maximum 15 minutes. Default: Duration.minutes(5)
        :param values: The values to be used by the chart. Default: - No values are provided to the chart.
        :param version: The chart version to install. Default: - If this is not specified, the latest version is installed
        :param wait: Whether or not Helm should wait until all Pods, PVCs, Services, and minimum number of Pods of a Deployment, StatefulSet, or ReplicaSet are in a ready state before marking the release as successful. Default: - Helm will not wait before marking release as successful

        return
        :return: a ``HelmChart`` object

        stability
        :stability: experimental
        throws:
        :throws:: If ``kubectlEnabled`` is ``false``
        """
        options = HelmChartOptions(chart=chart, create_namespace=create_namespace, namespace=namespace, release=release, repository=repository, timeout=timeout, values=values, version=version, wait=wait)

        return jsii.invoke(self, "addChart", [id, options])

    @jsii.member(jsii_name="addFargateProfile")
    def add_fargate_profile(self, id: str, *, selectors: typing.List["Selector"], fargate_profile_name: typing.Optional[str]=None, pod_execution_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, subnet_selection: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None) -> "FargateProfile":
        """Adds a Fargate profile to this cluster.

        :param id: the id of this profile.
        :param selectors: The selectors to match for pods to use this Fargate profile. Each selector must have an associated namespace. Optionally, you can also specify labels for a namespace. At least one selector is required and you may specify up to five selectors.
        :param fargate_profile_name: The name of the Fargate profile. Default: - generated
        :param pod_execution_role: The pod execution role to use for pods that match the selectors in the Fargate profile. The pod execution role allows Fargate infrastructure to register with your cluster as a node, and it provides read access to Amazon ECR image repositories. Default: - a role will be automatically created
        :param subnet_selection: Select which subnets to launch your pods into. At this time, pods running on Fargate are not assigned public IP addresses, so only private subnets (with no direct route to an Internet Gateway) are allowed. Default: - all private subnets of the VPC are selected.
        :param vpc: The VPC from which to select subnets to launch your pods into. By default, all private subnets are selected. You can customize this using ``subnetSelection``. Default: - all private subnets used by theEKS cluster

        see
        :see: https://docs.aws.amazon.com/eks/latest/userguide/fargate-profile.html
        stability
        :stability: experimental
        """
        options = FargateProfileOptions(selectors=selectors, fargate_profile_name=fargate_profile_name, pod_execution_role=pod_execution_role, subnet_selection=subnet_selection, vpc=vpc)

        return jsii.invoke(self, "addFargateProfile", [id, options])

    @jsii.member(jsii_name="addNodegroup")
    def add_nodegroup(self, id: str, *, ami_type: typing.Optional["NodegroupAmiType"]=None, desired_size: typing.Optional[jsii.Number]=None, disk_size: typing.Optional[jsii.Number]=None, force_update: typing.Optional[bool]=None, instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType]=None, labels: typing.Optional[typing.Mapping[str, str]]=None, max_size: typing.Optional[jsii.Number]=None, min_size: typing.Optional[jsii.Number]=None, nodegroup_name: typing.Optional[str]=None, node_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, release_version: typing.Optional[str]=None, remote_access: typing.Optional["NodegroupRemoteAccess"]=None, subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, tags: typing.Optional[typing.Mapping[str, str]]=None) -> "Nodegroup":
        """Add managed nodegroup to this Amazon EKS cluster.

        This method will create a new managed nodegroup and add into the capacity.

        :param id: The ID of the nodegroup.
        :param ami_type: The AMI type for your node group. Default: AL2_x86_64
        :param desired_size: The current number of worker nodes that the managed node group should maintain. If not specified, the nodewgroup will initially create ``minSize`` instances. Default: 2
        :param disk_size: The root device disk size (in GiB) for your node group instances. Default: 20
        :param force_update: Force the update if the existing node group's pods are unable to be drained due to a pod disruption budget issue. If an update fails because pods could not be drained, you can force the update after it fails to terminate the old node whether or not any pods are running on the node. Default: true
        :param instance_type: The instance type to use for your node group. Currently, you can specify a single instance type for a node group. The default value for this parameter is ``t3.medium``. If you choose a GPU instance type, be sure to specify the ``AL2_x86_64_GPU`` with the amiType parameter. Default: t3.medium
        :param labels: The Kubernetes labels to be applied to the nodes in the node group when they are created. Default: - None
        :param max_size: The maximum number of worker nodes that the managed node group can scale out to. Managed node groups can support up to 100 nodes by default. Default: - desiredSize
        :param min_size: The minimum number of worker nodes that the managed node group can scale in to. This number must be greater than zero. Default: 1
        :param nodegroup_name: Name of the Nodegroup. Default: - resource ID
        :param node_role: The IAM role to associate with your node group. The Amazon EKS worker node kubelet daemon makes calls to AWS APIs on your behalf. Worker nodes receive permissions for these API calls through an IAM instance profile and associated policies. Before you can launch worker nodes and register them into a cluster, you must create an IAM role for those worker nodes to use when they are launched. Default: - None. Auto-generated if not specified.
        :param release_version: The AMI version of the Amazon EKS-optimized AMI to use with your node group (for example, ``1.14.7-YYYYMMDD``). Default: - The latest available AMI version for the node group's current Kubernetes version is used.
        :param remote_access: The remote access (SSH) configuration to use with your node group. Disabled by default, however, if you specify an Amazon EC2 SSH key but do not specify a source security group when you create a managed node group, then port 22 on the worker nodes is opened to the internet (0.0.0.0/0) Default: - disabled
        :param subnets: The subnets to use for the Auto Scaling group that is created for your node group. By specifying the SubnetSelection, the selected subnets will automatically apply required tags i.e. ``kubernetes.io/cluster/CLUSTER_NAME`` with a value of ``shared``, where ``CLUSTER_NAME`` is replaced with the name of your cluster. Default: - private subnets
        :param tags: The metadata to apply to the node group to assist with categorization and organization. Each tag consists of a key and an optional value, both of which you define. Node group tags do not propagate to any other resources associated with the node group, such as the Amazon EC2 instances or subnets. Default: - None

        see
        :see: https://docs.aws.amazon.com/eks/latest/userguide/managed-node-groups.html
        stability
        :stability: experimental
        """
        options = NodegroupOptions(ami_type=ami_type, desired_size=desired_size, disk_size=disk_size, force_update=force_update, instance_type=instance_type, labels=labels, max_size=max_size, min_size=min_size, nodegroup_name=nodegroup_name, node_role=node_role, release_version=release_version, remote_access=remote_access, subnets=subnets, tags=tags)

        return jsii.invoke(self, "addNodegroup", [id, options])

    @jsii.member(jsii_name="addResource")
    def add_resource(self, id: str, *manifest: typing.Any) -> "KubernetesResource":
        """Defines a Kubernetes resource in this cluster.

        The manifest will be applied/deleted using kubectl as needed.

        :param id: logical id of this manifest.
        :param manifest: a list of Kubernetes resource specifications.

        return
        :return: a ``KubernetesResource`` object.

        stability
        :stability: experimental
        throws:
        :throws:: If ``kubectlEnabled`` is ``false``
        """
        return jsii.invoke(self, "addResource", [id, *manifest])

    @jsii.member(jsii_name="addServiceAccount")
    def add_service_account(self, id: str, *, name: typing.Optional[str]=None, namespace: typing.Optional[str]=None) -> "ServiceAccount":
        """Adds a service account to this cluster.

        :param id: the id of this service account.
        :param name: The name of the service account. Default: - If no name is given, it will use the id of the resource.
        :param namespace: The namespace of the service account. Default: "default"

        stability
        :stability: experimental
        """
        options = ServiceAccountOptions(name=name, namespace=namespace)

        return jsii.invoke(self, "addServiceAccount", [id, options])

    @builtins.property
    @jsii.member(jsii_name="awsAuth")
    def aws_auth(self) -> "AwsAuth":
        """Lazily creates the AwsAuth resource, which manages AWS authentication mapping.

        stability
        :stability: experimental
        """
        return jsii.get(self, "awsAuth")

    @builtins.property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> str:
        """The AWS generated ARN for the Cluster resource.

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            arn:aws:eks:us-west-2666666666666cluster / prod
        """
        return jsii.get(self, "clusterArn")

    @builtins.property
    @jsii.member(jsii_name="clusterCertificateAuthorityData")
    def cluster_certificate_authority_data(self) -> str:
        """The certificate-authority-data for your cluster.

        stability
        :stability: experimental
        """
        return jsii.get(self, "clusterCertificateAuthorityData")

    @builtins.property
    @jsii.member(jsii_name="clusterEncryptionConfigKeyArn")
    def cluster_encryption_config_key_arn(self) -> str:
        """Amazon Resource Name (ARN) or alias of the customer master key (CMK).

        stability
        :stability: experimental
        """
        return jsii.get(self, "clusterEncryptionConfigKeyArn")

    @builtins.property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> str:
        """The endpoint URL for the Cluster.

        This is the URL inside the kubeconfig file to use with kubectl

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            https:
        """
        return jsii.get(self, "clusterEndpoint")

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        """The Name of the created EKS Cluster.

        stability
        :stability: experimental
        """
        return jsii.get(self, "clusterName")

    @builtins.property
    @jsii.member(jsii_name="clusterOpenIdConnectIssuer")
    def cluster_open_id_connect_issuer(self) -> str:
        """If this cluster is kubectl-enabled, returns the OpenID Connect issuer.

        This is because the values is only be retrieved by the API and not exposed
        by CloudFormation. If this cluster is not kubectl-enabled (i.e. uses the
        stock ``CfnCluster``), this is ``undefined``.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "clusterOpenIdConnectIssuer")

    @builtins.property
    @jsii.member(jsii_name="clusterOpenIdConnectIssuerUrl")
    def cluster_open_id_connect_issuer_url(self) -> str:
        """If this cluster is kubectl-enabled, returns the OpenID Connect issuer url.

        This is because the values is only be retrieved by the API and not exposed
        by CloudFormation. If this cluster is not kubectl-enabled (i.e. uses the
        stock ``CfnCluster``), this is ``undefined``.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "clusterOpenIdConnectIssuerUrl")

    @builtins.property
    @jsii.member(jsii_name="clusterSecurityGroupId")
    def cluster_security_group_id(self) -> str:
        """The cluster security group that was created by Amazon EKS for the cluster.

        stability
        :stability: experimental
        """
        return jsii.get(self, "clusterSecurityGroupId")

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """Manages connection rules (Security Group Rules) for the cluster.

        stability
        :stability: experimental
        memberof:
        :memberof:: Cluster
        type:
        :type:: {ec2.Connections}
        """
        return jsii.get(self, "connections")

    @builtins.property
    @jsii.member(jsii_name="kubectlEnabled")
    def kubectl_enabled(self) -> bool:
        """Indicates if ``kubectl`` related operations can be performed on this cluster.

        stability
        :stability: experimental
        """
        return jsii.get(self, "kubectlEnabled")

    @builtins.property
    @jsii.member(jsii_name="openIdConnectProvider")
    def open_id_connect_provider(self) -> aws_cdk.aws_iam.OpenIdConnectProvider:
        """An ``OpenIdConnectProvider`` resource associated with this cluster, and which can be used to link this cluster to AWS IAM.

        A provider will only be defined if this property is accessed (lazy initialization).

        stability
        :stability: experimental
        """
        return jsii.get(self, "openIdConnectProvider")

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        """IAM role assumed by the EKS Control Plane.

        stability
        :stability: experimental
        """
        return jsii.get(self, "role")

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """The VPC in which this Cluster was created.

        stability
        :stability: experimental
        """
        return jsii.get(self, "vpc")

    @builtins.property
    @jsii.member(jsii_name="defaultCapacity")
    def default_capacity(self) -> typing.Optional[aws_cdk.aws_autoscaling.AutoScalingGroup]:
        """The auto scaling group that hosts the default capacity for this cluster.

        This will be ``undefined`` if the ``defaultCapacityType`` is not ``EC2`` or
        ``defaultCapacityType`` is ``EC2`` but default capacity is set to 0.

        stability
        :stability: experimental
        """
        return jsii.get(self, "defaultCapacity")

    @builtins.property
    @jsii.member(jsii_name="defaultNodegroup")
    def default_nodegroup(self) -> typing.Optional["Nodegroup"]:
        """The node group that hosts the default capacity for this cluster.

        This will be ``undefined`` if the ``defaultCapacityType`` is ``EC2`` or
        ``defaultCapacityType`` is ``NODEGROUP`` but default capacity is set to 0.

        stability
        :stability: experimental
        """
        return jsii.get(self, "defaultNodegroup")


class FargateCluster(Cluster, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-eks.FargateCluster"):
    """Defines an EKS cluster that runs entirely on AWS Fargate.

    The cluster is created with a default Fargate Profile that matches the
    "default" and "kube-system" namespaces. You can add additional profiles using
    ``addFargateProfile``.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, default_profile: typing.Optional["FargateProfileOptions"]=None, cluster_name: typing.Optional[str]=None, core_dns_compute_type: typing.Optional["CoreDnsComputeType"]=None, masters_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, output_cluster_name: typing.Optional[bool]=None, output_config_command: typing.Optional[bool]=None, output_masters_role_arn: typing.Optional[bool]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None, version: typing.Optional[str]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None, vpc_subnets: typing.Optional[typing.List[aws_cdk.aws_ec2.SubnetSelection]]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param default_profile: Fargate Profile to create along with the cluster. Default: - A profile called "default" with 'default' and 'kube-system' selectors will be created if this is left undefined.
        :param cluster_name: Name for the cluster. Default: - Automatically generated name
        :param core_dns_compute_type: Controls the "eks.amazonaws.com/compute-type" annotation in the CoreDNS configuration on your cluster to determine which compute type to use for CoreDNS. Default: CoreDnsComputeType.EC2 (for ``FargateCluster`` the default is FARGATE)
        :param masters_role: An IAM role that will be added to the ``system:masters`` Kubernetes RBAC group. Default: - By default, it will only possible to update this Kubernetes system by adding resources to this cluster via ``addResource`` or by defining ``KubernetesResource`` resources in your AWS CDK app. Use this if you wish to grant cluster administration privileges to another role.
        :param output_cluster_name: Determines whether a CloudFormation output with the name of the cluster will be synthesized. Default: false
        :param output_config_command: Determines whether a CloudFormation output with the ``aws eks update-kubeconfig`` command will be synthesized. This command will include the cluster name and, if applicable, the ARN of the masters IAM role. Default: true
        :param output_masters_role_arn: Determines whether a CloudFormation output with the ARN of the "masters" IAM role will be synthesized (if ``mastersRole`` is specified). Default: false
        :param role: Role that provides permissions for the Kubernetes control plane to make calls to AWS API operations on your behalf. Default: - A role is automatically created for you
        :param security_group: Security Group to use for Control Plane ENIs. Default: - A security group is automatically created
        :param version: The Kubernetes version to run in the cluster. Default: - If not supplied, will use Amazon default version
        :param vpc: The VPC in which to create the Cluster. Default: - a VPC with default configuration will be created and can be accessed through ``cluster.vpc``.
        :param vpc_subnets: Where to place EKS Control Plane ENIs. If you want to create public load balancers, this must include public subnets. For example, to only select private subnets, supply the following:: vpcSubnets: [ { subnetType: ec2.SubnetType.Private } ] Default: - All public and private subnets

        stability
        :stability: experimental
        """
        props = FargateClusterProps(default_profile=default_profile, cluster_name=cluster_name, core_dns_compute_type=core_dns_compute_type, masters_role=masters_role, output_cluster_name=output_cluster_name, output_config_command=output_config_command, output_masters_role_arn=output_masters_role_arn, role=role, security_group=security_group, version=version, vpc=vpc, vpc_subnets=vpc_subnets)

        jsii.create(FargateCluster, self, [scope, id, props])


__all__ = [
    "AutoScalingGroupOptions",
    "AwsAuth",
    "AwsAuthMapping",
    "AwsAuthProps",
    "BootstrapOptions",
    "CapacityOptions",
    "CfnCluster",
    "CfnClusterProps",
    "CfnNodegroup",
    "CfnNodegroupProps",
    "Cluster",
    "ClusterAttributes",
    "ClusterOptions",
    "ClusterProps",
    "CoreDnsComputeType",
    "DefaultCapacityType",
    "EksOptimizedImage",
    "EksOptimizedImageProps",
    "FargateCluster",
    "FargateClusterProps",
    "FargateProfile",
    "FargateProfileOptions",
    "FargateProfileProps",
    "HelmChart",
    "HelmChartOptions",
    "HelmChartProps",
    "ICluster",
    "INodegroup",
    "KubernetesPatch",
    "KubernetesPatchProps",
    "KubernetesResource",
    "KubernetesResourceProps",
    "MachineImageType",
    "NodeType",
    "Nodegroup",
    "NodegroupAmiType",
    "NodegroupOptions",
    "NodegroupProps",
    "NodegroupRemoteAccess",
    "PatchType",
    "Selector",
    "ServiceAccount",
    "ServiceAccountOptions",
    "ServiceAccountProps",
]

publication.publish()
