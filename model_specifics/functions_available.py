import os
from functools import partial
from pathlib import Path
from typing import Callable, Mapping

from functions.get_file_contents import _get_file_contents
from functions.get_files_info import _get_files_info
from functions.run_python_file import __run_python_file
from functions.write_file import _write_file
from model_specifics.consts import AI_CWD

FUNCTIONS: Mapping[str, Callable] = {
    'get_file_content': partial(_get_file_contents, Path(os.path.join(os.getcwd(), AI_CWD))),
    'write_file': partial(_write_file, Path(os.path.join(os.getcwd(), AI_CWD))),
    'run_python_file': partial(__run_python_file, Path(os.path.join(os.getcwd(), AI_CWD))),
    'get_files_info': partial(_get_files_info, Path(os.path.join(os.getcwd(), AI_CWD)))
}
