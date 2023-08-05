from enum import Enum

WEB_PROC = "web"

class Machine(Enum):
        lean = (256, 512)
        lean_x2 = (256, 1024)
        standard = (512, 1024)
        standard_x2 = (512, 2048)
        heavy = (1024, 2048)
        heavy_x2 = (1024, 4096)

class Proc:
    def __init__(self, ** kwargs):
        self.name = kwargs["name"]
        self.machine = kwargs.get("machine", Machine.lean)
        self.instances = kwargs.get("instances", 1)
        self.target_group = kwargs.get("target_group")
        self.port = kwargs.get("port", 8080)
        self.entry = kwargs["entry"]
        self.image = kwargs["image"]
        if self.name == WEB_PROC and self.target_group is None:
            raise ValueError("A web proc must have the target group specified")

class ProcSet:
    def __init__(self, ** kwargs):
        self.cluster = kwargs["cluster"]
        self.security_group = kwargs["security_group"]
        self.subnet_a = kwargs["subnet_a"]
        self.subnet_b = kwargs["subnet_b"]
        self.role = kwargs["role"]
        self.secret = kwargs.get("secret")
        self.procs = dict()

    def add_proc(self, proc):
        self.procs[proc.name] = proc