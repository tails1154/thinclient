
ls /home/tails1154/.debug
if [ $? ]; then
	xterm -e ./runner.sh
else
	./runner.sh | tee > logs/runner.log
fi
