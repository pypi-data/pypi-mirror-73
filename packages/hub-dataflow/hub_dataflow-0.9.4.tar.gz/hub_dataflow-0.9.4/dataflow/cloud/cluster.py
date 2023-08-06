import weakref
from dask_cloudprovider.providers.aws.helper import dict_to_aws

from dask_cloudprovider import ECSCluster
import boto3


class Cluster(ECSCluster):
    """Deploy a cluster using Fargate on ECS

    This creates a dask scheduler and workers on a Fargate powered ECS cluster.
    If you do not configure a cluster one will be created for you with sensible
    defaults.

    Parameters
    ----------
    kwargs: dict
        Keyword arguments to be passed to :class:`ECSCluster`.

    """

    def __init__(
        self,
        name="snark2",
        aws_access_key_id=None,
        aws_secret_access_key=None,
        region=None,
        **kwargs,
    ):
        session = boto3.session.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        if region is None:
            self.region = session.region_name

        self.client = session.client(service_name="ecr", region_name=self.region,)
        self.aws_account = session.client("sts").get_caller_identity().get("Account")

        # cluster_arn = f"arn:aws:ecs:{self.region}:{self.aws_account}:cluster/{name}"
        task_role_policies = [
            "arn:aws:iam::aws:policy/AmazonS3FullAccess",
            "arn:aws:iam::aws:policy/SecretsManagerReadWrite",
        ]

        super().__init__(
            fargate_scheduler=True,
            fargate_workers=True,
            # scheduler_cpu=2048,
            # scheduler_mem=16384,
            # worker_cpu=4096,
            # worker_mem=16384,
            scheduler_timeout="10 minutes",
            task_role_policies=task_role_policies,
            **kwargs,
        )

    async def _create_execution_role(self):
        async with self._client("iam") as iam:
            response = await iam.create_role(
                RoleName=self._execution_role_name,
                AssumeRolePolicyDocument="""{
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                        "Effect": "Allow",
                        "Principal": {
                            "Service": "ecs-tasks.amazonaws.com"
                        },
                        "Action": "sts:AssumeRole"
                        }
                    ]
                    }""",
                Description="A role for ECS to use when executing",
                Tags=dict_to_aws(self.tags, upper=True),
            )
            await iam.attach_role_policy(
                RoleName=self._execution_role_name,
                PolicyArn="arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly",
            )
            await iam.attach_role_policy(
                RoleName=self._execution_role_name,
                PolicyArn="arn:aws:iam::aws:policy/CloudWatchLogsFullAccess",
            )
            await iam.attach_role_policy(
                RoleName=self._execution_role_name,
                PolicyArn="arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceRole",
            )

            await iam.attach_role_policy(
                RoleName=self._execution_role_name,
                PolicyArn="arn:aws:iam::aws:policy/SecretsManagerReadWrite",
            )

            weakref.finalize(
                self, self.sync, self._delete_role, self._execution_role_name
            )
            return response["Role"]["Arn"]

    async def _create_scheduler_task_definition_arn(self):

        async with self._client("ecs") as ecs:
            response = await ecs.register_task_definition(
                family="{}-{}".format(self.cluster_name, "scheduler"),
                taskRoleArn=self._task_role_arn,
                executionRoleArn=self._execution_role_arn,
                networkMode="awsvpc",
                containerDefinitions=[
                    {
                        "name": "dask-scheduler",
                        "image": self.image,
                        "cpu": self._scheduler_cpu,
                        "memory": self._scheduler_mem,
                        "memoryReservation": self._scheduler_mem,
                        "repositoryCredentials": {
                            "credentialsParameter": "snark_docker"
                        },
                        "essential": True,
                        "command": [
                            "dask-scheduler",
                            "--idle-timeout",
                            self._scheduler_timeout,
                        ],
                        # + (
                        #    list()
                        #    if not self._scheduler_extra_args
                        #    else self._scheduler_extra_args
                        # ),
                        "logConfiguration": {
                            "logDriver": "awslogs",
                            "options": {
                                "awslogs-region": ecs.meta.region_name,
                                "awslogs-group": self.cloudwatch_logs_group,
                                "awslogs-stream-prefix": self._cloudwatch_logs_stream_prefix,
                                "awslogs-create-group": "true",
                            },
                        },
                    }
                ],
                volumes=[],
                requiresCompatibilities=["FARGATE"] if self._fargate_scheduler else [],
                cpu=str(self._scheduler_cpu),
                memory=str(self._scheduler_mem),
                tags=dict_to_aws(self.tags),
            )
        weakref.finalize(self, self.sync, self._delete_scheduler_task_definition_arn)
        return response["taskDefinition"]["taskDefinitionArn"]

    async def _create_worker_task_definition_arn(self):
        resource_requirements = []
        if self._worker_gpu:
            resource_requirements.append(
                {"type": "GPU", "value": str(self._worker_gpu)}
            )
        async with self._client("ecs") as ecs:
            response = await ecs.register_task_definition(
                family="{}-{}".format(self.cluster_name, "worker"),
                taskRoleArn=self._task_role_arn,
                executionRoleArn=self._execution_role_arn,
                networkMode="awsvpc",
                containerDefinitions=[
                    {
                        "name": "dask-worker",
                        "image": self.image,
                        "cpu": self._worker_cpu,
                        "memory": self._worker_mem,
                        "memoryReservation": self._worker_mem,
                        "resourceRequirements": resource_requirements,
                        "repositoryCredentials": {
                            "credentialsParameter": "snark_docker"
                        },
                        "essential": True,
                        "command": [
                            "dask-cuda-worker" if self._worker_gpu else "dask-worker",
                            "--nprocs",  # nthreads
                            "{}".format(max(int(self._worker_cpu / 1024), 1)),
                            "--memory-limit",
                            "{}MB".format(int(self._worker_mem)),
                            "--death-timeout",
                            "60",
                        ],
                        # + (
                        #    list()
                        #    if not self._worker_extra_args
                        #    else self._worker_extra_args
                        # ),
                        "logConfiguration": {
                            "logDriver": "awslogs",
                            "options": {
                                "awslogs-region": ecs.meta.region_name,
                                "awslogs-group": self.cloudwatch_logs_group,
                                "awslogs-stream-prefix": self._cloudwatch_logs_stream_prefix,
                                "awslogs-create-group": "true",
                            },
                        },
                    }
                ],
                volumes=[],
                requiresCompatibilities=["FARGATE"] if self._fargate_workers else [],
                cpu=str(self._worker_cpu),
                memory=str(self._worker_mem),
                tags=dict_to_aws(self.tags),
            )
        weakref.finalize(self, self.sync, self._delete_worker_task_definition_arn)
        return response["taskDefinition"]["taskDefinitionArn"]
