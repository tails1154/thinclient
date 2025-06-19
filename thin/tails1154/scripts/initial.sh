echo "Factory Reset (Delete all data)"
echo "Deleting Client"
rm -rf /home/tails1154/client
mkdir /home/tails1154/client
echo "Deleting Logs"
rm -rf /home/tails1154/logs
mkdir /home/tails1154/logs
echo "Deleting SSID"
rm -rf /home/tails1154/ssid.txt
echo "Reading IP"
export baseurl="$(cat /home/tails1154/ip.txt)"
echo "Downloading Dummy Client"
wget "$baseurl/tailsnet/dummy.py"
echo "Moving dummy client"
mv dummy.py /home/tails1154/client/firmware.py
echo "Script Completed!"
exit 0
