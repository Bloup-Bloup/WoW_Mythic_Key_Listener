# WoW_Mythic_Key_Listener

This program will search for mythic key for each chararcter in your account and send it throught discord webhook.

First Steps : 

Put 'Mythic_Keystone_Tracker' folder into your Interface/AddOns
Add your WoW path into "config.txt".  Be sure to remove the '\' between your C: and your Program Files or whatever. And add a '\' at the end of your path and save.
Now, connect your character in wow and do a /reload or /mkst .

Be sure you have python 3.8 installed ( not tested with an other version )
Modifiy the ListeningAddonFile.py at line 90. Paste your weebhook id.
Install the requierement.txt then launch the .py script with >>> 'python3 ListeningAddonFile.py'


Next time, simply /reload or /mkst and launch the ListeningAddonFile.py
You can compile the ListeningAddonFile.py with pyinstaller included in the env folder.
Run the venv : ./env/Scripts/activate
and >>> 'python3 pyinstaller ListeningAddonFile.py --onefile'
