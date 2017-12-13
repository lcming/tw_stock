#!/bin/sh
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <commit message>"
    exit 1
fi
msg=$1
echo $msg
fail_tests=""
for testfile in `ls test*.py`
do
    ./$testfile
    if [ "$?" -ne 0 ]; then
        fail_tests=$(printf "$fail_tests\n$testfile")
    fi
done

if [ "$fail_tests" = "" ]; then
    git commit -a -m "$msg"
    git push
else
    echo "failed tests: $fail_tests"
fi
