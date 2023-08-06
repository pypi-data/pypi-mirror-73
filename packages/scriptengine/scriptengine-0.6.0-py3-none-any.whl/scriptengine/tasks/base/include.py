"""Include task for ScriptEngine

   The Include task reads a YAML file, parses the content to create a
   ScriptEngine script and lets the active ScriptEngine instance execute it.
"""

import os

import scriptengine.yaml

from scriptengine.tasks.base import Task
from scriptengine.tasks.base.timing import timed_runner


class Include(Task):

    def __init__(self, parameters):
        super().__init__(__name__, parameters, required_parameters=["src"])

    def __str__(self):
        return f"Include: {self.src}"

    @timed_runner
    def run(self, context):
        inc_file = self.getarg('src', context)
        self.log_info(f"Include script from {inc_file}")

        search_path = [".", context.get("_se_cmd_cwd", "")] + context.get("_se_filepath", [])
        self.log_debug(f"Searching in path: {search_path}")
        for directory in search_path:
            inc_file_path = os.path.join(directory, inc_file)
            self.log_debug(f"Seraching for include file at '{inc_file_path}'")
            if os.path.isfile(inc_file_path):
                self.log_debug(f"Found include file at '{inc_file_path}'")
                break
        else:
            if self.getarg('ignore_not_found', False):
                self.log_warning(f"Include file {inc_file} not found.")
                return
            raise RuntimeError(f"Include file '{inc_file}' not found")

        script = scriptengine.yaml.parse_file(inc_file_path)

        inc_file_dir = os.path.dirname(os.path.abspath(inc_file_path))
        if inc_file_dir not in context.get("_se_filepath", []):
            context.setdefault("_se_filepath", []).append(inc_file_dir)

        try:
            se_instance = context['_se_instance']
        except KeyError:
            raise RuntimeError("ScriptEngine instance not found")
        else:
            self.log_debug(f"Execute script from '{inc_file}'")
            se_instance.run(script, context)
            self.log_debug(f"Finished executing script from '{inc_file}'")
