import json
import re
import logging
from subprocess import Popen, PIPE

ANSI_ESCAPE = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

class DBTExecuter():
    def __init__(self):
        """"""
        self.dbt_command = None
        self.logger = logging.getLogger(__name__)

    def parse_json(self, command):
        """Parse a dbt command json string to ensure it is constructed properly and
         is using a dbt command that is supported.
         
        Parameters
        ----------
        command : str
            command json string to parse
        """
        json_cmd = json.loads(command)
        print(json_cmd)

        self.dbt_project = json_cmd["Project"]
        self.dbt_command = json_cmd["Command"].split()
        self.check_command()

        if self.dbt_command[1] == "docs":
            ## do prep work for docs
            "foo"

    def check_command(self):
        if self.dbt_command[0] != 'dbt':
            raise ValueError(f"Command does not start with 'dbt':\n{self.cmd}")

        if self.dbt_command[1] not in ["run", "debug", "snapshot", "test", "clean", "docs"]:
            raise ValueError(f"Command includes a dbt command that is not supported':\n{self.cmd}")

    def run_command(self):
        """Run the dbt command.
        """
        if self.dbt_command is None:
            raise ValueError("No command set to run...")

        with Popen(self.dbt_command, stdout=PIPE) as proc:
            for line in proc.stdout:
                line = line.decode('utf-8').replace('\n', '').strip()
                line = ANSI_ESCAPE.sub('', line)
                self.logger.info(line)

#json_cmd = """{
#    "Project": "Landing-To-History",
#    "Command": "dbt run --select OnlineSer"
#}"""
#dbtexe = DBTExecuter()
#dbtexe.parse_json(json_cmd)
#dbtexe.run_command()

