from os import listdir, path

import pytest

from lab1_cli import Lab1API
from actions_manager import ActionsManager


def validate_output_gauss(correct_output_file, checked_output_file, meta_inf):
    correct_x = correct_output_file.readline().strip().split()
    checked_x = checked_output_file.readline().strip().split()
    if len(correct_x) == 1:
        if correct_x == checked_x:
            return True
    else:
        correct_x = list(map(float, correct_x))
        checked_x = list(map(float, checked_x))
        for x, y in zip(checked_x, correct_x):
            if x - y <= 0.001:
                continue
            else:
                return False
        return True


def validate_output_gauss_an(correct_output_file, checked_output_file, meta_inf):
    return True


def validate_output_simple_iteration(correct_output_file, checked_output_file, meta_inf):
    correct_x = correct_output_file.readline().strip().split()
    checked_x = checked_output_file.readline().strip().split()
    if len(correct_x) == 1:
        if correct_x == checked_x:
            return True
    else:
        eps = float(meta_inf.replace(",", "."))
        correct_x = list(map(float, correct_x))
        checked_x = list(map(float, checked_x))
        for x, y in zip(checked_x, correct_x):
            if x - y <= eps:
                continue
            else:
                return False
        return True


def validate_output_gauss_zeidel(correct_output_file, checked_output_file, meta_inf):
    return validate_output_simple_iteration(correct_output_file, checked_output_file, meta_inf)


def validate_output(meta_inf, test_file_path):
    # TODO: прописать/устранить неявную логику метча тестов и ответов (если по имени, то как BORIS FIX проходит?)
    print(test_file_path)
    test_dir_path, method, input_file_name = test_file_path.rsplit("/", 2)
    test_dir_path = test_dir_path.rsplit("/", 1)[0]
    output_file_name = f"{method}/{input_file_name.split('.')[0]}_ans.txt"
    output_file_path = f"{test_dir_path}/output_fixtures/{output_file_name}"
    print(output_file_path)
    correct_output_file = open(output_file_path, "r")
    checked_output_file = open(f"{test_dir_path}/lab1_test_result.txt", "r")
    if method == "Simple_Iter":
        return validate_output_simple_iteration(correct_output_file, checked_output_file, meta_inf)
    elif method == "Gauss_Regular":
        return validate_output_gauss(correct_output_file, checked_output_file, meta_inf)
    elif method == "Gauss_Zeidel":
        return validate_output_gauss_an(correct_output_file, checked_output_file, meta_inf)
    elif method == "":
        return validate_output_gauss_zeidel(correct_output_file, checked_output_file, meta_inf)


def dir_from_file(file_path, delimiter: str):
    return delimiter.join(file_path.split(delimiter)[:-1])


d = "/"
FIXTURE_DIR_PATH = f'{dir_from_file(__file__, d)}{d}input_fixtures'


def collect_tests():
    assert ActionsManager.catch_required_method() and ActionsManager.catch_run_config(), "Ошибка инициализации"
    method = ActionsManager.required_method
    # https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
    if method == 1:
        test_dir_path = FIXTURE_DIR_PATH + d + "Gauss_Regular"
    elif method == 2:
        test_dir_path = FIXTURE_DIR_PATH + d + "Simple_Iter"
    elif method == 3:
        test_dir_path = FIXTURE_DIR_PATH + d + "Gauss_Zeidel"
    else:
        raise Exception(method)

    return [
        path.join(test_dir_path, f)
        for f in listdir(test_dir_path)
        if path.isfile(path.join(test_dir_path, f))
    ]


@pytest.mark.dependency()
def test_workflow_init():
    assert ActionsManager.required_method, "Не удалось прочитать метод и stud-info.json"
    assert ActionsManager.run_configuration, "Не удалось прочитать конфиг из run.sh"


@pytest.mark.dependency(depends=["test_workflow_init"])
@pytest.mark.parametrize("test_file_path", collect_tests())
def test_empty_input(test_file_path):
    run_command = ActionsManager.run_configuration
    return_code, meta_inf = Lab1API.run_with_input_file(run_command, test_file_path)
    assert validate_output(meta_inf, test_file_path)
    assert return_code == 0
