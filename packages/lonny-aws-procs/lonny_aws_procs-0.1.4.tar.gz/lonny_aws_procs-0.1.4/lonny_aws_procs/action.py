import boto3
from .logger import logger

client_ecs = boto3.client("ecs")
my_session = boto3.session.Session()

SECRET_ENV = "PROC_SECRETS"

def _get_service_arns(*, cluster, next_token = None):
    data = client_ecs.list_services( ** dict(
        cluster = cluster,
        ** dict() if next_token is None else dict(nextToken = next_token)
    ))
    for arn in data["serviceArns"]:
        yield arn
    next_token = data.get("nextToken")
    if next_token is None:
        return
    for arn in _get_service_arns(cluster = cluster, next_token = next_token):
        yield arn

def _get_services(*, cluster):
    for arn in _get_service_arns(cluster = cluster):
        yield client_ecs.describe_services(
            cluster = cluster, 
            services = [arn]
        )["services"][0]

def _delete_service(*, cluster, name):
    client_ecs.update_service(cluster = cluster, service = name, desiredCount = 0)
    client_ecs.delete_service(cluster = cluster, service = name)

def _update_service(*, proc_set, proc, task_definition_arn):
    client_ecs.update_service(
        cluster = proc_set.cluster,
        service = proc.name,
        desiredCount = proc.instances,
        taskDefinition = task_definition_arn,
        forceNewDeployment = True
    )

def _create_service(*, proc_set, proc, task_definition_arn):
    client_ecs.create_service(
        cluster = proc_set.cluster,
        serviceName = proc.name,
        launchType = "FARGATE",
        taskDefinition = task_definition_arn,
        loadBalancers = list() if proc.target_group is None else [dict(
            targetGroupArn = proc.target_group,
            containerName = proc.name,
            containerPort = proc.port
        )],
        desiredCount = proc.instances,
        networkConfiguration = dict(
            awsvpcConfiguration = dict(
                subnets = [proc_set.subnet_a, proc_set.subnet_b],
                securityGroups = [proc_set.security_group],
                assignPublicIp = "ENABLED"
            )
        )
    )

def _register_task_definition(*, proc_set, proc):
    return client_ecs.register_task_definition(
        family = proc.name,
        taskRoleArn = proc_set.role,
        executionRoleArn = proc_set.role,
        networkMode = "awsvpc",
        requiresCompatibilities = ["FARGATE"],
        cpu = str(proc.machine.value[0]),
        memory = str(proc.machine.value[1]),
        containerDefinitions = [dict(
            name = proc.name,
            entryPoint = proc.entry,
            secrets = list() if proc_set.secret is None else [dict(
                name = SECRET_ENV,
                valueFrom = proc_set.secret
            )],
            logConfiguration = dict(
                logDriver = "awslogs",
                options = {
                    "awslogs-group": proc.log_group,
                    "awslogs-region": my_session.region_name,
                    "awslogs-stream-prefix": proc.name
                }
            ),
            image = proc.image,
            portMappings = list() if proc.target_group is None else [dict(
                containerPort = proc.port,
                hostPort = proc.port
            )]
        )]
    )["taskDefinition"]["taskDefinitionArn"]

def sync(proc_set):
    service_map = { x["serviceName"] : x for x in _get_services(cluster = proc_set.cluster) }
    for name, service in service_map.items():
        if name not in proc_set.procs:
            logger.info(f"Proc: {name} is not specified in most recent configuration. Destroying.")
            _delete_service(cluster = proc_set.cluster, name = name)

    for proc in proc_set.procs.values():
        logger.info(f"Registering a task definition for proc: {proc.name}.")
        task_def_arn = _register_task_definition(
            proc_set = proc_set,
            proc = proc
        )
        if proc.name in service_map:
            logger.info(f"Service for proc: {proc.name} already exists. Updating.")
            _update_service(
                proc = proc,
                proc_set = proc_set,
                task_definition_arn = task_def_arn,
            )
        else:
            logger.info(f"Service for proc: {proc.name} doesn't exist. Creating.")
            _create_service(
                proc = proc,
                proc_set = proc_set,
                task_definition_arn = task_def_arn
            )