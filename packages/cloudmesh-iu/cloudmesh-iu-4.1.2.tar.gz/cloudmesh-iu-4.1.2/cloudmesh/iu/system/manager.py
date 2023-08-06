import os
from subprocess import check_output
from cloudmesh.common.Shell import Shell
from cloudmesh.common.Tabulate import Printer
from textwrap import indent
from cloudmesh.common.parameter import Parameter
from cloudmesh.common.console import Console
from cloudmesh.common.util import readfile
from cloudmesh.common.util import writefile
import textwrap
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.variables import Variables
import textwrap
from cloudmesh.common.Shell import Shell
import random
from cloudmesh.common.Printer import Printer
import webbrowser
import time


class Manager(object):
    """
    PARTITION  AVAIL  TIMELIMIT  NODES   GRES  STATE NODELIST
    romeo         up   infinite      4  gpu:8    mix r-[001-004]
    volta         up   infinite      2  gpu:8    mix r-[005-006]
    """

    def __init__(self, user=None):
        self.hostname = "juliet.futuresystems.org"
        self.host = "juliet"
        self.user = user
        variables = Variables()
        self.debug = variables["debug"]
        self.logfile = "jupyterlab.log"

        if user is not None:
            self.login = f"{user}@{self.host}"

    def DEBUG(self, *args):
        if self.debug:
            Console.info(" ".join(args))

    def setup(self, user=None):
        self.ssh_config_add("j", self.hostname, user)
        self.ssh_config_add("juliet", self.hostname, user)
        self.ssh_config_add("romeo", self.hostname, user)

    def ssh_config_add(self, label, host, user):
        config = readfile("~/.ssh/config")
        if f"Host {label}" in config:
            Console.warning(f"{label} is already in ~/.ssh/config")
        else:
            entry = textwrap.dedent(f"""
            Host {label}
                Hostname {host}
                User {user}
                IdentityFile ~/.ssh/id_rsa.pub
            """)
            Console.info(f"adding {label} to ~/.ssh/config\n" +
                         textwrap.indent(entry, prefix="    "))
            config = config + entry
            writefile("~/.ssh/config", config)

    def list(self, parameter):
        print("list", parameter)

    def login(self,
              user=None,
              host="romeo",
              node=1,
              gpus=1):

        command = f"ssh -t {self.host} " \
                  f" srun -p {host}" \
                  f" -w {node} --gres gpu:{gpus} --pty bash"
        print(command)
        os.system(command)

    def smart_login(self,
                    user=None,
                    host="romeo",
                    node=1,
                    gpus=1):

        status = self.queue(host=host, user=user)
        # VERBOSE(locals())

        print(Printer.attribute(status, header=["Node", "Used GPUs"]))

        #
        # Required node not available (down, drained or reserved)
        #

        reserved = self.reserved_nodes(user=user)

        def hostnames(host):
            if host == "volta":
                names = Parameter.expand("r-00[5-6]")
            else:
                names = Parameter.expand("r-00[3-4]")

            max_gpus = 8  # this is for now hard coded
            valid = []
            for name in names:
                if name not in reserved and status[name] + gpus <= max_gpus:
                    valid.append(name)
            return valid

        def find_random(host):
            names = hostnames(host)

            if len(names) == 0 or names is None:
                return None
            id = random.randint(0, len(host) - 1)
            return names[id]

        def find_first(host):

            names = hostnames(host)

            if names is None or len(names) == 0:
                return None
            else:
                return names[0]

        if node is None or node == "first":
            node = find_first(host)

        if node is None or node == "random":
            node = find_random(host)

        if node is not None:
            Console.ok(f"Login on node {host}: {node}")

            self.login(
                user=user,
                host=host,
                node=node,
                gpus=gpus)
        else:
            Console.error(f"not enough GPUs available: {host}: {node}")

    def reserved_nodes(self, user=None):

        reservation = self.reservations(user=user)

        _reserved_nodes = []
        for r in reservation:
            nodes = Parameter.expand(r["Nodes"])
            _reserved_nodes = _reserved_nodes + nodes

        return _reserved_nodes

    def status(self, user=None):

        reservation = self.reservations(user=user)
        VERBOSE(reservation)
        print(Printer.write(reservation,
                            order=[
                                'Nodes',
                                'ReservationName',
                                'State',
                                'Users',
                                'CoreCnt',
                                'Flags',
                                'NodeCnt'

                            ],
                            #header=[
                            #    'Nodes',
                            #    'Reservation',
                            #    'State',
                            #    'Allowed Users'
                            #    'Cores (CPUs)',
                            #    'Flags',
                            #    'No.Nodes'
                            #]
                            ))

        reserved = self.reserved_nodes(user=user)

        #
        # BUG check for date
        #

        # print (reserved)

        used = {}
        for host in ["romeo", "volta"]:
            status = self.queue(host=host, user=user)
            for key in status:
                used_gpu = status[key]
                used[key] = {
                    'name': key,
                    'used': status[key],
                    'domain': host
                }

        print(Printer.write(used,
                            order=["name", "domain", "used"],
                            header=["Host", "Domain", "Used GPUs"]))

        data = {}
        for host in ["romeo", "volta"]:
            users = self.users(host=host, user=user)
            users = ', '.join(users)
            data[host] = {
                "host": host,
                "users": users
            }
        print("\nActive Users")
        print(Printer.write(data,
                            order=["host", "users"],
                            header=["Host", "Users"]))

    def users(self, host=None, user=None):
        command = f"ssh -o LogLevel=QUIET -t {self.host} " \
                  f" squeue -p {host} -o \"%u\""
        r = check_output(command, shell=True).decode('ascii').split()[1:]
        r = sorted(set(r))
        return r

    def queue(self, host=None, user=None):
        command = f"ssh -o LogLevel=QUIET -t {self.host} " \
                  f" squeue -p {host}"

        self.DEBUG(command)

        lines = check_output(command, shell=True).decode('ascii') \
                    .splitlines()[1:]

        used = {}

        for line in lines:
            attributes = line.split()
            gpus = attributes[7]
            try:
                gpus = int(gpus.split(":")[1])
            except:
                gpus = 0
            host = attributes[8]
            if "Unavailable" in host:
                continue
            if host not in used:
                used[host] = 0
            used[host] += gpus
            # print (attributes)

        return used

    def reservations(self, user=None):
        command = f"ssh -o LogLevel=QUIET -t {self.host} " \
                  f" scontrol -a -d -o show res"
        result = check_output(command, shell=True).decode('ascii').splitlines()
        r = []
        for line in result:
            data = {}
            entry = line.split(" ")
            for element in entry:
                attribute, value = element.split("=")
                data[attribute] = value
            r.append(data)
        return r

    def connect(self, config):
        print ("connect")
        os.system("cms iu allocate &")
        time.sleep(2)
        os.system("cms iu port &")

    def allocate(self, config):
        user = config["user"]
        reservation = config["reservation"]
        Console.info("romeo allocate")
        command = f'ssh -tt {user}@juliet.futuresystems.org salloc -p romeo --reservation={reservation}'
        Shell.terminal(command, title="reservation")

    def ps(self, config):
        Console.info("ps")
        user = config["user"]
        host = config["host"]

        command = f'ssh -tt {user}@juliet.futuresystems.org "ssh {host} ps -aux"'
        r = Shell.run(command)
        found = []
        for line in r.split("\n"):
            try:
                if line.startswith(user):
                    found.append(line)
            except:
                pass
        return found


    def kill(self, config, id):
        user = config["user"]
        host = config["host"]
        gpu = config["gpu"]

        command = f'ssh -tt {user}@juliet.futuresystems.org "ssh {host} kill -9 {id}"'
        print (command)
        r = Shell.run(command)
        return r

    def port(self, config):
        user = config["user"]
        host = config["host"]
        gpu = config["gpu"]
        port = config["port"]
        command = f"ssh -L {port}:r-003:{port} -i {port} {user}@juliet.futuresystems.org"
        print (command)
        Shell.terminal(command, title=f"port {port}")



    def config(self, config):
        Console.info("config")
        print (Printer.attribute(config))

        #user = config["user"]
        #host = config["host"]
        #gpu = config["gpu"]

    def lab(self, config):
        os.system("cms iu connect")
        os.system("cms iu jupyter &")
        time.sleep(5)
        self.view(config)

    def jupyter(self, config):
        Console.info("jupyter")
        print (config)

        user = config["user"]
        host = config["host"]
        gpu = config["gpu"]
        port = config["port"]

        command = f'ssh -tt {user}@juliet.futuresystems.org "ssh {host} nohup jupyter-lab --port {port} --ip 0.0.0.0 --no-browser 2>&1 | tee {self.logfile}"'

        print (command)
        os.system(command)
        #Shell.terminal(command)
        r = None
        #r = Shell.run(command)
        #return r

    def info(self, config):
        user = config["user"]
        host = config["host"]
        gpu = config["gpu"]
        port = config["port"]
        command = f"ssh {user}@juliet.futuresystems.org cat {self.logfile}"
        result = Shell.run(command)
        try:
            lines = result.split("\n")
            url = lines[-2]
            print (url)
            url = url.split("or ")[1].strip()
            r = {}
            # r["content"] = result
            r["url"] = url
        except:
            Console.error("jupyter lab info not found")
        return r


    def view(self, config):

        info = self.info(config)
        webbrowser.open(info["url"])
