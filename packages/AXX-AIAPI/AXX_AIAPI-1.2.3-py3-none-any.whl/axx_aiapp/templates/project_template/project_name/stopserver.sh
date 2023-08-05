#!/usr/bin/env bash
PIDFILE="$PWD/gunicorn.pid"

if [ -f $PIDFILE ]; then
    PID=$(cat $PIDFILE)
    kill -9 $PID
    rm $PIDFILE
    echo 'over'
fi