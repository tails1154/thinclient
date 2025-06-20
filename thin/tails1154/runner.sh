#!/bin/bash
echo "[runner.sh] runner.sh started"
echo "[runner.sh] Starting pulseaudio"
pulseaudio --start
sleep 3
echo "[runner.sh] Starting indicator"
python3 /home/tails1154/light.py &
echo "[runner.sh] Sleeping 5 seconds for it to start"
sleep 5
SOCKET="/tmp/indicator_socket"
echo "[runner.sh] Starting blink"
/home/tails1154/blink.sh &
echo "[runner.sh] Starting window manager"
icewm &
echo "[runner.sh] Starting unclutter"
unclutter -idle 0 &
counter=0
while [ yes ]; do
	killall -9 blink.sh
	/home/tails1154/blink.sh &
	echo "[runner.sh] Running firmware"
	cd /home/tails1154/client
#	killall blink.sh
	echo "power on" | socat - UNIX-SENDTO:"$SOCKET"
	python3 firmware.py
	killall -9 blink.sh
	/home/tails1154/blink.sh &
	if [ $(ls counter.stop) ]; then
	echo "[runner.sh] Counter bypassed because counter.stop exists."
	rm -rf counter.stop
	else
	counter=$((counter + 1))
	echo "[runner.sh] firmware.py closed. Counter is now $counter"
	if [ "$counter" -ge 20 ]; then
		echo "[runner.sh] Counter has reached 20. Assuming firmware is broken. Downloading a dummy (downloader?) copy."
		export yip="$(cat /home/tails1154/ip.txt)"
		wget "$yip/tailsnet/dummy.py"
		mv dummy.py /home/tails1154/client/firmware.py
		echo "[runner.sh] Resetting counter."
		let counter=0
	fi
	fi
done
