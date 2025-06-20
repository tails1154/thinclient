#!/bin/bash

SOCKET="/tmp/indicator_socket"


while [ yes ]; do

echo "warning on" | socat - UNIX-SENDTO:"$SOCKET"

sleep 0.5

echo "warning off" | socat - UNIX-SENDTO:"$SOCKET"


done
