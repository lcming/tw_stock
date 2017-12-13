#!/bin/sh
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <commit message>"
    exit 1
fi
msg=$1
echo $msg
for testfile in `ls test*.py`
do
    ./$testfile
done
if [ "$?" -eq 0 ]; then
    git commit -a -m "$msg"
    git push
fi
