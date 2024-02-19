#!/usr/bin/env sh

script_dir=$(dirname $0)

python -m venv $script_dir/.venv

$script_dir/.venv/bin/pip install -r $script_dir/requirements.txt