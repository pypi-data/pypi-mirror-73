from argparse import ArgumentParser
from os import getenv
from json import loads
from .type import Proc, ProcSet, Machine
from .action import sync
from .logger import logger
from logging import StreamHandler, INFO

WEB_PROC = "web"

parser = ArgumentParser()
parser.add_argument("--procs_f", default = "procs.json")
parser.add_argument("--cluster", default = getenv("PROCS_CLUSTER"))
parser.add_argument("--security_group", default = getenv("PROCS_SECURITY_GROUP"))
parser.add_argument("--image", default = getenv("PROCS_IMAGE"))
parser.add_argument("--subnet_a", default = getenv("PROCS_SUBNET_A"))
parser.add_argument("--subnet_b", default = getenv("PROCS_SUBNET_B"))
parser.add_argument("--role", default = getenv("PROCS_ROLE"))
parser.add_argument("--secret", default = getenv("PROCS_SECRET"))
parser.add_argument("--namespace", default = "lonny-procs-")
parser.add_argument("--target_group", default = getenv("PROCS_TARGET_GROUP"))
parser.add_argument("--port", default = getenv("PROCS_PORT", 8080))

logger.setLevel(INFO)
logger.addHandler(StreamHandler())

args = parser.parse_args()

proc_set = ProcSet(
    cluster = args.cluster,
    security_group = args.security_group,
    subnet_a = args.subnet_a,
    subnet_b = args.subnet_b,
    role = args.role,
    secret = args.secret
)

with open(args.procs_f) as f:
    for name, proc_def in loads(f.read()).items():
        if name == WEB_PROC and args.target_group is None:
            raise RuntimeError("Target group is required")
        proc_set.add_proc(Proc(
            name = f"{args.namespace}{name}",
            machine = Machine[proc_def["machine"]],
            image = args.image,
            instances = proc_def["instances"],
            target_group = args.target_group if name == WEB_PROC else None,
            port = args.port,
            entry = proc_def["entry"]
        ))

sync(proc_set)

