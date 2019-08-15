#!/bin/bash

scriptPath=$(cd `dirname $0`; pwd)
projectPath=$(cd `dirname $scriptPath`; pwd)

current_dir=$(pwd)
cd "$projectPath"
python -m unittest management.test.third_party
cd "$current_dir"