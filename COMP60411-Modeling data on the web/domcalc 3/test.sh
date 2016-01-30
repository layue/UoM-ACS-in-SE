#!/bin/sh
CWD="$(cd -P -- "$(dirname -- "$0")" && pwd -P)"
for entry in "$CWD/resource"/*.xml
do
  name=${entry##*/}
  test_case=${name%.*}
  printf "\n------------  $test_case  ------------\n"
  $CWD/run.sh $test_case
  read -p " Press enter to continue or ^C to terminate .."
done
echo "Finished."