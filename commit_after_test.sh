#!/bin/sh
commit=1
if [ "$#" -ne 1 ]; then
    commit=0
fi
msg=$1
echo $msg
fail_tests=""
for testfile in `ls test*.py`
do
    python3 $testfile
    if [ "$?" -ne 0 ]; then
        fail_tests=$(printf "$fail_tests\n$testfile")
    fi
done

if [ "$fail_tests" = "" ] && [ "$commit" -eq 1 ] ; then
    git commit -a -m "$msg"
    git push
else
    echo "failed tests: $fail_tests"
fi
