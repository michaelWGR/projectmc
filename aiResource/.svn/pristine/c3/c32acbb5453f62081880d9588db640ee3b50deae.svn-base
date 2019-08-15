#!/bin/bash

scriptPath=$(cd `dirname $0`; pwd)
projectPath=$(cd `dirname $scriptPath`; pwd)
managePath="$projectPath/manage.py"

python "$managePath" run_samples_by_csv ocr aliyun,baiducloud,tuputech,txcloud "$projectPath/ocr_debug.csv"