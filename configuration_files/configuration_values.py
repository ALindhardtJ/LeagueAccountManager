import json
from pathlib import Path

configuratons_file = Path("configuration_files/configurations.json")
with configuratons_file.open("r") as conf_json_file:
    configuration_values = json.load(conf_json_file)

automatic_queue_accept: bool = configuration_values.get("automatic_queue_accept")
collect_data_on_startup: bool = configuration_values.get("collect_data_on_startup")


def toggle_automatic_queue_accept():
    configuration_values["automatic_queue_accept"] = not configuration_values.get("automatic_queue_accept", False)
    with configuratons_file.open("w") as conf_json_file:
        json.dump(configuration_values, conf_json_file)

def toggle_collect_data_on_startup():
    configuration_values["collect_data_on_startup"] = not configuration_values.get("collect_data_on_startup", False)
    with configuratons_file.open("w") as conf_json_file:
        json.dump(configuration_values, conf_json_file)