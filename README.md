# What is this?
 - This is the session delete of CISCO ISE script.
 - you can see the active session in CISCO ISE

## Installation and Run
#### 1. Clone the repo
	git clone https://github.com/JungnamKim-dev/ise_session.git

#### 2. change into directory
	cd ise_session

#### 3. Create the virtual environment in a sub dir in the same directory
	python3 -m venv venv
	
#### 4. Start the virtual environment and install requirements.txt from the <ise_session>
	source venv/bin/activate
	pip install -r requirements.txt 
	
#### 5. Runtime compiler C++2015
install the [Runtime Compiler C++2015](https://www.microsoft.com/en-us/download/details.aspx?id=48145)
	
## Run
this support is tow mode.
 - cli mode : only delete(session, mac, ip)
 - gui mode : any function(show session, delete session/mac/ip)
 
#### cli example
	python3 ise_session.py
<img src="./doc/ise_session_cli.png">
	
#### gui example
	python3 ise_session_gui.py
<img src="./doc/ise_session_gui.png">
	

## License
This project is licensed under the Apache License 2.0 - see the  [LICENSE.md](./LICENSE.md) file for details.

