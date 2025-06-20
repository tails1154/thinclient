#!/bin/bash

SOCKET="/tmp/indicator_socket"


while [ yes ]; do

echo "power on" | socat - UNIX-SENDTO:"$SOCKET"

sleep 0.5

echo "power off" | socat - UNIX-SENDTO:"$SOCKET"


done
