# What is this?
 - This is the session delete of CISCO ISE script.
 - you can see the active session in CISCO ISE

## Required package
	pip intall requests
  pip intall xmltodict
  pip intall PyQt5
  (you can see this : https://pypi.org/project/PyQt5/)

## Used to
 this support is tow mode.
 - cli mode : only delete(session, mac, ip)
 - gui mode : any function(show session, delete session/mac/ip)

#### Connection example
	from cims_db import db_manager
	conn_state = dbmanager.Connect('<HOST_IP>', '<HOST_PORT>', '<DB_NAME>', '<ID>', '<PW>')
	if conn_state == True:
		print ("Connection is OK")
	else:
		print ("Connection is Failed")
