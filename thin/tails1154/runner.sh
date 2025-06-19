#!/bin/bash
echo "[runner.sh] runner.sh started"
counter=0
while [ yes ]; do
	echo "[runner.sh] Running firmware"
	cd /home/tails1154/client
	python3 firmware.py | tee > /home/tails1154/logs/firmware.log
	if [ ls counter.stop ]; then
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
