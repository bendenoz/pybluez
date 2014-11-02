# rssi read

import sys
import bluetooth._bluetooth as bluez
import bluetooth

if len(sys.argv) < 2:
    print("usage: rssi.py <addr>")
    sys.exit(2)

bt_addr=sys.argv[1]
port = 0x0

# sock.bind(("",-1)); # -1 means zero for now (see bluez.py)

# establish raw connection
l2_sock = bluetooth.BluetoothSocket(bluetooth.L2CAP, bluetooth.SOCK_RAW)
sys.stderr.write("trying raw connect to %s on PSM 0x%X\n" % (bt_addr, port))
try:
	l2_sock.connect((bt_addr, port)) 
except bluetooth.btcommon.BluetoothError, e:
	sys.stderr.write("Error: %s\n" % e)
else:
	# hci socket for rssi reading
	hci_sock = bluez.hci_open_dev ()
	handle = bluez.hci_acl_conn_handle(hci_sock.fileno(), bt_addr)
	rssi = bluez.hci_read_rssi( hci_sock.fileno(), handle, 0)
	if rssi is not None:
		print "RSSI:", rssi

	hci_sock.close()
	l2_sock.close()