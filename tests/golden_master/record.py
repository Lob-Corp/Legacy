import subprocess
import os
import shutil


import json
from typing import List
from pydantic import BaseModel, ValidationError

import web_action_runner
from web_action_runner import WebActionRunner, WEB_ACTION_TYPE

class LegacyRunner:
    def __init__(self):
        self.legacy_gwd_process = None

    def start(self):
        legacy_distribution_directory = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../legacy/distribution"))
        if (not os.path.isdir(legacy_distribution_directory)):
            raise Exception(f"Legacy distribution directory not found. Please build Legacy first")

        # If tests databse is found, delete it and recreate it.
        legacy_bases_directory = os.path.join(legacy_distribution_directory, "bases")
        tests_database_path = os.path.join(legacy_bases_directory, "tests.gwd")
        if (os.path.isdir(tests_database_path)):
            shutil.rmtree(tests_database_path)
        subprocess.run(["../gw/gwc", "-f", "-o", "tests"], cwd=legacy_bases_directory)

        # Start gwd server
        self.legacy_gwd_process = subprocess.Popen(["./gwd.sh"], cwd=legacy_distribution_directory)

    def stop(self):
        if self.legacy_gwd_process:
            self.legacy_gwd_process.terminate()
            self.legacy_gwd_process.wait()

def action_from_dict(d):
    action_type = d.pop("type", None)
    if action_type is None or action_type not in WEB_ACTION_TYPE:
        raise ValueError(f"Unknown or missing action type: {action_type}")
    return WEB_ACTION_TYPE[action_type](**d)

class Scenario(BaseModel):
    name: str
    actions: List[web_action_runner.WebAction]

def load_scenarios() -> List[Scenario]:
    scenarios_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scenarios")
    scenarios: List[Scenario] = []

    for root, _, files in os.walk(scenarios_directory):
        for filename in files:
            if not filename.endswith(".json"):
                continue
            filepath = os.path.join(root, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                actions = [action_from_dict(a) for a in data["actions"]]
                scenario = Scenario(name=data["name"], actions=actions)
                scenarios.append(scenario)
    return scenarios

def main():
    scenarios: List[Scenario] = load_scenarios()
    web_action_runner: WebActionRunner = WebActionRunner()
    runner = LegacyRunner()
    runner.start()

    for scenario in scenarios:
        print(f"Running scenario: {scenario.name}")
        web_action_runner.run_action_sequence(scenario.actions)

    web_action_runner.dispose()
    runner.stop()

if __name__ == "__main__":
    main()

