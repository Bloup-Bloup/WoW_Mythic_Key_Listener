# WoW_Mythic_Key_Listener

This program will search for mythic key for each chararcter in your account and send it throught discord webhook.
It will create rows into the database and update or add another next time you using it.
A config.txt will be created the first time, to store your current wow path and increase speed of the programm for the next time.

First Steps : 

Connect your character in wow and do a /reload or /mkst .

Be sure you have python 3.8 installed ( not tested with an other version )
Modifiy the ListeningAddonFile.py at line 129. Paste your weebhook id.
Install the requierement.txt then launch the .py script with >>> 'python3 ListeningAddonFile.py'


Next time, simply /reload or /mkst and launch the ListeningAddonFile.py


You can compile the ListeningAddonFile.py with pyinstaller included in the env folder.
Run the venv : ./env/Scripts/activate
and >>> 'python3 pyinstaller ListeningAddonFile.py --onefile'
