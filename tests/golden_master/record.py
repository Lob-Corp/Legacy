import subprocess
import os
import time
import shutil

import web_action_runner
from web_action_runner import WebActionRunner

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


# Add empty family
scenario_add_empty_family = [
    web_action_runner.WebGetAction("http://localhost:2317/tests"),
    web_action_runner.WebClickAction("css", "div.d-inline-flex:nth-child(3) > a:nth-child(1)"),
    web_action_runner.WebClickAction("css", "button.btn-primary:nth-child(3)"),
    web_action_runner.WebSaveHTMLAction("records/scenario_add_empty_family.html")
]

scenario_add_valid_family_parent_still_alive = [
    web_action_runner.WebGetAction("http://localhost:2317/tests"),
    web_action_runner.WebClickAction("css", "div.d-inline-flex:nth-child(3) > a:nth-child(1)"),

    # --- Fill parents form ---
    # Parent 1 (John)
    web_action_runner.WebTypeAction("css", "#pa1_fn", "John"),
    web_action_runner.WebTypeAction("css", "#pa1_sn", "Smith"),
    web_action_runner.WebTypeAction("css", "#pa1b_mm", "04"),
    web_action_runner.WebTypeAction("css", "#pa1b_dd", "12"),
    web_action_runner.WebTypeAction("css", "#pa1b_yyyy", "1975"),
    web_action_runner.WebTypeAction("css", "#pa1b_pl", "London, UK"),
    web_action_runner.WebTypeAction("css", "#pa1_occu", "Software Engineer"),

    # Parent 2 (Emily)
    web_action_runner.WebTypeAction("css", "#pa2_fn", "Emily"),
    web_action_runner.WebTypeAction("css", "#pa2_sn", "Johnson"),
    web_action_runner.WebTypeAction("css", "#pa2b_mm", "09"),
    web_action_runner.WebTypeAction("css", "#pa2b_dd", "23"),
    web_action_runner.WebTypeAction("css", "#pa2b_yyyy", "1978"),
    web_action_runner.WebTypeAction("css", "#pa2b_pl", "Manchester, UK"),
    web_action_runner.WebTypeAction("css", "#pa2_occu", "Teacher"),

    web_action_runner.WebClickAction("css", "button.btn-primary:nth-child(3)"),
    web_action_runner.WebSaveHTMLAction("records/scenario_add_valid_family_parent_still_alive.html")
]

scenario_add_valid_family_parent_dead = [
    web_action_runner.WebGetAction("http://localhost:2317/tests"),
    web_action_runner.WebClickAction("css", "div.d-inline-flex:nth-child(3) > a:nth-child(1)"),

    # --- Fill parents form ---
    # Parent 1 (William)
    web_action_runner.WebTypeAction("css", "#pa1_fn", "William"),
    web_action_runner.WebTypeAction("css", "#pa1_sn", "Brown"),
    web_action_runner.WebTypeAction("css", "#pa1b_mm", "11"),
    web_action_runner.WebTypeAction("css", "#pa1b_dd", "02"),
    web_action_runner.WebTypeAction("css", "#pa1b_yyyy", "1901"),
    web_action_runner.WebTypeAction("css", "#pa1b_pl", "Boston, USA"),

    web_action_runner.WebTypeAction("css", "#pa1d_mm", "07"),
    web_action_runner.WebTypeAction("css", "#pa1d_dd", "18"),
    web_action_runner.WebTypeAction("css", "#pa1d_yyyy", "1980"),
    web_action_runner.WebTypeAction("css", "#pa1d_pl", "New York, USA"),

    web_action_runner.WebTypeAction("css", "#pa1_occu", "Carpenter"),

    # Parent 2 (Emily)
    web_action_runner.WebTypeAction("css", "#pa2_fn", "Margaret"),
    web_action_runner.WebTypeAction("css", "#pa2_sn", "Brown"),
    web_action_runner.WebTypeAction("css", "#pa2b_mm", "05"),
    web_action_runner.WebTypeAction("css", "#pa2b_dd", "15"),
    web_action_runner.WebTypeAction("css", "#pa2b_yyyy", "1905"),
    web_action_runner.WebTypeAction("css", "#pa2b_pl", "Philadelphia, USA"),

    web_action_runner.WebTypeAction("css", "#pa2d_mm", "02"),
    web_action_runner.WebTypeAction("css", "#pa2d_dd", "22"),
    web_action_runner.WebTypeAction("css", "#pa2d_yyyy", "1990"),
    web_action_runner.WebTypeAction("css", "#pa2d_pl", "New York, USA"),

    web_action_runner.WebTypeAction("css", "#pa2_occu", "Nurse"),

    web_action_runner.WebClickAction("css", "button.btn-primary:nth-child(3)"),
    web_action_runner.WebSaveHTMLAction("records/scenario_add_valid_family_parent_dead.html")
]

scenario_add_valid_family_parent_still_alive_same_sex = [
    web_action_runner.WebGetAction("http://localhost:2317/tests"),
    web_action_runner.WebClickAction("css", "div.d-inline-flex:nth-child(3) > a:nth-child(1)"),

    # --- Fill parents form ---
    # Parent 1 (Carlos)
    web_action_runner.WebTypeAction("css", "#pa1_fn", "Carlos"),
    web_action_runner.WebTypeAction("css", "#pa1_sn", "Martínez"),
    web_action_runner.WebTypeAction("css", "#pa1b_mm", "06"),
    web_action_runner.WebTypeAction("css", "#pa1b_dd", "10"),
    web_action_runner.WebTypeAction("css", "#pa1b_yyyy", "1985"),
    web_action_runner.WebTypeAction("css", "#pa1b_pl", "Madrid, Spain"),
    web_action_runner.WebTypeAction("css", "#pa1_occu", "Architect"),

    # Parent 2 (Daniel)
    web_action_runner.WebTypeAction("css", "#pa2_fn", "Daniel"),
    web_action_runner.WebTypeAction("css", "#pa2_sn", "López"),
    web_action_runner.WebTypeAction("css", "#pa2b_mm", "03"),
    web_action_runner.WebTypeAction("css", "#pa2b_dd", "14"),
    web_action_runner.WebTypeAction("css", "#pa2b_yyyy", "1987"),
    web_action_runner.WebTypeAction("css", "#pa2b_pl", "Barcelona, Spain"),
    web_action_runner.WebTypeAction("css", "#pa2_occu", "Graphic Designer"),

    web_action_runner.WebClickAction("css", "button.btn-primary:nth-child(3)"),
    web_action_runner.WebSaveHTMLAction("records/scenario_add_valid_family_parent_still_alive_same_sex.html")
]

if __name__ == "__main__":

    web_action_runner: WebActionRunner = WebActionRunner()
    time.sleep(2)
    runner = LegacyRunner()
    runner.start()

    scenarios = [
        scenario_add_empty_family,
        scenario_add_valid_family_parent_still_alive,
        scenario_add_valid_family_parent_dead,
        scenario_add_valid_family_parent_still_alive_same_sex
    ]
    for scenario in scenarios:
        web_action_runner.run_action_sequence(scenario)

    web_action_runner.dispose()
    runner.stop()
