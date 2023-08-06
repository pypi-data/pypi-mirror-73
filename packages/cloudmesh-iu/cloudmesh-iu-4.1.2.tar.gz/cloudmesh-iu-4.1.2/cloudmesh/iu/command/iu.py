from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand, map_parameters
from cloudmesh.iu.system.manager import Manager
from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from pprint import pprint
from cloudmesh.common.parameter import Parameter
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.variables import Variables
from cloudmesh.common.util import banner
from cloudmesh.common.Printer import Printer

from cloudmesh.configuration.Config import Config
import random

class IuCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_iu(self, args, arguments):
        """
        ::

          Usage:
                iu lab
                iu connect
                iu config
                iu allocate
                iu ps
                iu info
                iu kill
                iu status
                iu jupyter
                iu port
                iu view
                iu [--user=USERNAME]
                   [--host=HOST]
                   [--node=NUMBER]
                   [--gpu=GPUS]
                   [--res=RESERVATION]
                iu res
                iu setup --user=USERNAME
                iu romeo [--user=USERNAME]

          This command allows you to inteactively log into roeo or volta

          Arguments:
              FILE    a file name
              HOST    the host is either rome or volta [default: romeo]
              NUMBER  is a number that specifies where to login
              GPUS    the number of GPU's to be used

          Options:
              --res=RESERVATION  [default: lijguo_11]

          Example:

              cms iu
                 logs in on the first available node, and uses 1 GPU
                 BUG: some reservation are not detected

              cms iu --node=random
                 logs in on the first available node and uses 1 GPU

              cms iu status
                 lists the status of rome and volta. The output will look like:


                    +-------------+-----------+
                    | romeo       | Used GPUs |
                    +-------------+-----------+
                    | r-001       |           |
                    | r-002       | 7         |
                    | r-003       | 7         |
                    | r-004       | 7         |
                    +-------------+-----------+

                    +-------+-----------+
                    | volta | Used GPUs |
                    +-------+-----------+
                    | r-005 | 5         |
                    | r-006 | 7         |
                    +-------+-----------+

                    Users on romeo

                        user1

                    Users on volta

                        user2
        """
        #VERBOSE(arguments)
        config = Config()["cloudmesh.iu"]


        map_parameters(arguments,
                       "user",
                       "host",
                       "node",
                       "gpu")

        variables = Variables()
        #arguments["user"] = Parameter.find("user", arguments, variables)
        # if arguments.user is None:
        #    config = Config()
        #    arguments.user = config["cloudmesh.iu.user"]

        iu = Manager(user=arguments.user)

        if arguments.setup:

            iu.setup()
            return ""

        elif arguments.config:

            iu.config(config)

            return ""

        if arguments.status:

            iu.status(user=arguments.user)

            return ""

        elif arguments.res:

            iu.reservations(user=arguments.user)

            return ""

        elif arguments.allocate:

            iu.allocate(config)

            return ""

        elif arguments.ps:

            found = iu.ps(config)
            print ("\n".join(found))
            return ""

        elif arguments.info:

            r = iu.info(config)
            print (Printer.attribute(r))
            return ""


        elif arguments.jupyter:

            found = iu.jupyter(config)
            # print ("\n".join(found))
            return ""

        elif arguments.connect:

            found = iu.connect(config)
            return ""

        elif arguments.port:

            found = iu.port(config)
            return ""

        elif arguments.view:

            found = iu.view(config)
            return ""

        elif arguments.lab:

            found = iu.lab(config)
            return ""

        elif arguments.kill:

            found = iu.ps(config)
            for line in found:
                line = line.replace("     ", " ")
                line = line.replace("    ", " ")
                line = line.replace("   ", " ")
                line = line.replace("  ", " ")
                parameter = line.split(" ", 3)
                if "python" in line:
                    id = parameter[1]
                    r = iu.kill(config, id)
                    print(r)
            return ""


        #elif arguments.romeo(user=arguments.user):

        #    iu.reservations(user=arguments.user)

        #    return ""


        else:

            arguments["host"] = Parameter.find("host", arguments, variables,
                                               {"host": "romeo"})
            arguments["node"] = Parameter.find("node", arguments, variables)
            arguments["gpu"] = int(Parameter.find("gpu", arguments, variables,
                                                  {"gpu": "1"}))

            # VERBOSE(arguments)

            banner(f"Login {arguments.host}")

            #iu.login(user=arguments.user,
            #               host=arguments.host,
            #               node=arguments.node,
            #               gpus=arguments.gpu)

            iu.smart_login(user=arguments.user,
                           host=arguments.host,
                           node=arguments.node,
                           gpus=arguments.gpu)

        return ""
