#!/bin/bash

# check argv
if [ $# -ne 2 ]; then
  echo "./sindan-time-checker.sh linux NUM" 1>&2
  exit 1
fi

if [ "$1" != "linux" ]; then
  echo "Only linux support"
  exit 1
fi

if expr "$2" : "[0-9]*$" >&/dev/null; then
  _now_date=$(date +"%Y-%m-%d-%H-%M")

  mkdir -p sindan-sh-time-log
  mkdir -p sindan-sh-time-log/log-$_now_date

  for i in `seq $2`
  do
    echo "${i}:" | tee sindan-sh-time-log/time-log-$_now_date.output
    _run_time=$(date +"%Y-%m-%d-%H-%M")
    echo "Do : time sudo $HOME/sindan-client/linux/sindan.sh" | tee -a sindan-sh-time-log-$_now_date/time-log-$_now_date.output
    ( time ( sudo $HOME/sindan-client/linux/sindan.sh >> sindan-sh-time-log/log-$_now_date/log-${1}-$_run_time.log)) 2>> sindan-sh-time-log/time-log-$_now_date.output
    echo "" >> sindan-sh-time-log/time-log-$_now_date.output
    echo "" >> sindan-sh-time-log/time-log-$_now_date.output
  done
else
  echo "$2 is not a number"
fi
