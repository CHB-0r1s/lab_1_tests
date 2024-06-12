import json
import os


def dir_from_file(file_path, delimiter: str):
    return delimiter.join(file_path.split(delimiter)[:-1])


class ActionsManager:
    JSON_WTH_METHOD_INFO = "stud-info.json"
    FILE_WITH_RUN_CONFIG = "run.sh"
    DELIMITER = "/"

    required_method: int = None  # TODO: Переделать на enum
    run_configuration: str = None
    current_dir: str = dir_from_file(__file__, DELIMITER)

    @staticmethod
    def catch_required_method() -> bool:
        json_path = ActionsManager.current_dir + ActionsManager.DELIMITER + ActionsManager.JSON_WTH_METHOD_INFO
        if not os.path.exists(json_path):
            return False
        row_json_data = open(json_path).read()
        stud_info: dict = json.loads(row_json_data)
        stud_method = stud_info.get("required_method", None)
        if stud_method:
            if isinstance(stud_method, str):
                stud_method = int(stud_method)
            ActionsManager.required_method = stud_method
        return bool(stud_method)

    @staticmethod
    def catch_run_config() -> bool:
        sh_path = ActionsManager.current_dir + ActionsManager.DELIMITER + ActionsManager.FILE_WITH_RUN_CONFIG
        if not os.path.exists(sh_path):
            return False
        run_data = open(sh_path).read().strip()
        if run_data:
            ActionsManager.run_configuration = run_data
        return bool(run_data)