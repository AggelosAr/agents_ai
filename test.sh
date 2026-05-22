#!/bin/bash

source .venv/bin/activate

python3 -m test_get_files_info
python3 -m test_get_file_content
python3 -m test_write_file
python3 -m test_run_python_file

