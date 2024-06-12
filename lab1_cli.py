from subprocess import Popen, PIPE
import shlex


def dir_from_file(file_path, delimiter: str):
    return delimiter.join(file_path.split(delimiter)[:-1])


def erase_meta_inf(row_file: str) -> (str, str):
    splited_row_file: list[str] = row_file.split("#")
    test_data, erased_meta_inf = splited_row_file[0], splited_row_file[-1]
    return test_data, erased_meta_inf


def create_run_file(file_name: str, run_command: str, input_data: str) -> None:
    echo_command: list[str] = ["echo", f"\'{input_data}\'", "|"]
    run_command_and_param: list[str] = shlex.split(run_command, comments=False, posix=True)

    with open(file_name, mode="w") as file:
        file.write(" ".join(echo_command))
        file.write(" ".join(run_command_and_param))


class Lab1API:
    CWD_PIPELINE = dir_from_file(__file__, "/")

    @staticmethod
    def run_with_input_file(run_command: str, file_path: str) -> (str, str):
        """
        :param run_command: Строка с командами запуска
        :param file_path: Путь до файла с входными данными
        :return: Статус запуска и метаинформация

        Функция объединяет входные данные и команду для запуска в конвейер,
        запаковывая результат в отдельный файл t.sh. После чего запускает его:

        >> sh RUN_FILE_NAME
        """
        RUN_FILE_NAME = "t.sh"

        file_with_input = open(file_path, "r")

        treated_input, meta_inf = erase_meta_inf(file_with_input.read().replace("\r", ""))
        create_run_file(RUN_FILE_NAME, run_command, treated_input)

        with Popen(["sh", RUN_FILE_NAME], stdout=PIPE, stderr=PIPE, cwd=Lab1API.CWD_PIPELINE) as proc:
            return proc.wait(), meta_inf
