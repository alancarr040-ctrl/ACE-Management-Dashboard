__TOC__
==READ ME FIRST!==
Before you embark further on the wonderful journey of being an admin, here are some tips: 
<br>
#DO be fair and unbiased. Admins that favor their friends, give away XP or do anything other than simply resolving game bugs will lose players.
#DO be respectful. Admins should be cool, calm and collected even when dealing with highly emotional players. Behave like a police officer or you will lose players.
#DO have time to admin effectively by being present as much as possible. Admin(s) that are never around, and have no published email address to contact them, will lose players.
#This page is NOT an exhaustive list of all possible admin commands, event and content creation... it is an INTRODUCTION to help you get started. Being a long-term, successful server admin and/or content creator requires significant time and effort.
#If you do not have significant time, or do not plan to run the occasional event... consider joining one of the existing ACE servers listed on the Discord #server-links channel. Keep an eye on things like the degree of XP acceleration, frequency of live or custom events, amount of custom content and how fair and polite the admin(s) are, as this goes a long way to how you will enjoy the experience.
<br>
That all said, let's jump right into some of the core knowledge required to be a successful admin! Credits to ''gmriggs'' and ''Arcane Hand'' for their time that helped put this page together.
<br>
<br>
==Managing the server==
===Seeing which players are online===
Use the <code>@pop</code> command to see the number of players online (including yourself).
* <code>@pop</code>

Use the <code>@listplayers</code> command to list all players currently on the server, and the total number of connected players.
* <code>@listplayers</code>

You will see:

''+ExampleAdmin : 12
<BR>
Total connected Players: 1''
<br>
<br>
<br>
===Send an admin broadcast to all players on the server===
Use the <code>@gamecastlocal</code> command to broadcast a message to all players.
*<code>@gamecastlocal This is an example of a broadcast message.</code>

Players will see the following in green text:
<BR>
''Broadcast from +ExampleAdmin> This is an example of a broadcast.''
<br>
<br>
<br>
===Opening or closing the server to players===
*Use <code>@world open</code> to allow players to log into the server (default).
*Use <code>@world close</code> to prevent any new logins to the server only.
*Use <code>@world close boot</code> to force all players to logoff immediately (it is better to warn players of this with an admin broadcast first).
<br>
<br>
<br>
===Restarting and Stopping the server===
1. Enter the <code>@pop</code> server command to see if there are any players online (including yourself).
<blockquote>
If there are NO PLAYERS ONLINE, you can shutdown the server IMMEDIATELY without warning using the <code>@stop-now</code> server command.
*<code>@stop-now</code>
</blockquote>

2. Use the <code>@set-shutdown-interval</code> server command to set how many seconds until the server should shutdown.
<blockquote>
<code>@set-shutdown-interval 600</code> will set the shutdown to occur in 600 seconds, or 10 minutes.
<br>
''INFO : Shutdown Interval (seconds to shutdown server) has been set to 600 seconds.
</blockquote>

2. Use the <code>@gamecastlocal</code> server command to broadcast a message to all players about a pending server shutdown.
<blockquote>
<code>@gamecastlocal The server will be going down for maintenance in an hour. A 10 minute warning will proceed the server shutdown itself.
</code>
<BR>
Players will see the following in green text:
*''Broadcast from +ExampleAdmin> The server will be going down for maintenance in an hour. A 10 minute warning will proceed the server shutdown itself.''
</blockquote>

3. Use the <code>@shutdown</code> server command followed by a message to inform players of a shutdown with the amount of time set above using set-shutdown-interval.
<blockquote>
<code>@shutdown The server will be coming down in 10 minutes. Please find a safe place to log out.</code>
</blockquote>

If you simply issue the <code>@shutdown</code> server command without a custom messsage, players will see default text:
<br>
''Server initiated a complete server shutdown @ 5/8/2021 4:23:09 AM UTC
The server will go down in 10 minutes.'

4. To CANCEL a shutdown, issue the <code>@cancel-shutdown</code> command.
<br>
<br>
-----
==Managing Accounts==
<br>
===Renaming a character===
Enter <code>@rename OldName , NewName</code>. Be sure to include a SPACE before and after the comma.
<br>
<br>
<br>
===Move a character to a different account===
1 Ask the player for a) the SOURCE account name, b) the DESTINATION account name and c) the CHARACTER NAME to be moved.

2 Run the SQL client (try clicking Windows Start and type 'maria' to find the MariaSQL command prompt).

3 Enter these SQL commands (NOTE: the backticks (`) is used around the word `character` and apostrophies (') are used around the name of the character to move).

  use ace_auth;
  SELECT accountID,accountName FROM account WHERE accountName='{SOURCE_ACCOUNT}';
  SELECT accountID,accountName FROM account WHERE accountName='{DESTINATION_ACCOUNT}';

NOTE: If you get empty results for either of these commands then you have been given an invalid account name and DO NOT proceed further:

4 Assuming you have a different accountID you can now proceed to move the character:

  use ace_shard;
  UPDATE `character` SET account_Id=13 WHERE name='{CHARACTER_NAME}';

NOTE: If you get changed result of 0 then you've done something wrong.

<br>
Here's an example of moving a character called 'My Battlemage' from account 'mysourceacc' to account 'mydestacc':
<br>
<pre>
MariaDB [ace_auth]> use ace_auth;
Database changed
MariaDB [ace_auth]> SELECT accountID,accountName FROM account WHERE accountName='mysourceacc';
+-----------+--------------------+
| accountID | accountName        |
+-----------+--------------------+
|        11 | mysourceacc        |
+-----------+--------------------+
1 row in set (0.000 sec)

MariaDB [ace_auth]> SELECT accountID,accountName FROM account WHERE accountName='mydestacc';
+-----------+-------------+
| accountID | accountName |
+-----------+-------------+
|        13 | mydestacc   |
+-----------+-------------+
1 row in set (0.000 sec)

MariaDB [ace_auth]> use ace_shard;
Database changed
MariaDB [ace_shard]> UPDATE `character` SET account_Id=13 WHERE name='My Battlemage';
Query OK, 1 row affected (0.001 sec)
Rows matched: 1  Changed: 1  Warnings: 0

MariaDB [ace_shard]>
</pre>
<br>
<br>
==Managing Players==
===Admin Powers===
<br>
====Becoming immortal====
Use <code>@neversaydie</code> to make yourself un-killable.
<br>
<br>
====Becoming unattackable====
Use <code>@attackable on</code> to make yourself no longer attackable by monsters. Use <code>@attackable off</code> to reverse it.
<br>
<br>
====Running fast====
Use <code>@run</code> to make yourself run very fast.
<br>
<br>
====Becoming invisible or appearing as a player====
Use <code>@cloak on</code> to become invisible, and <code>@cloak off</code> to become visible again.<br>
Use <code>@cloak player</code> to appear without a + in front of your name.
<br>
<br>
====Teleporting====
=====To a player=====
Use <code>@teleto {character_name}</code>.
<br>
<br>
=====A player to you=====
Use <code>@teletome {character_name}</code>.
<br>
<br>
=====To a location given to you=====
Use the <code>@teleloc {loc_data}</code> where {loc_data} is generated by any character using the <code>/loc</code> command.<br>
<br>
Example:
#A player enters <code>/loc</code> and gives you something like:<br>
#*''Your location is: 0x2B120021 [105.994911 7.602986 48.006001] 0.887545 0.000000 0.000000 -0.460721''
#As an admin you enter that location as <code>@teleloc 0x2B120021 [105.994911 7.602986 48.006001] 0.887545 0.000000 0.000000 -0.460721</code>
<br>
<br>
<br>
====Insta-killing monster(s)====
If you need to kill a monster or all monsters on radar range to help a character, use the following commands:
*<code>@smite</code> kills the targeted monster.
*<code>@smite all</code> kills ALL monsters in radar range.
<br>
<br>
====Opening locked items====
If you need to unlock something that is locked, click on the object and enter:
*<code>@crack</code>
<br>
<br>
===Resolving Player Issues===
====Invisible Monsters====
*The player can issue the /objsend command every 5 minutes.
*Failing that, a relog can clear this issue.
<br>
<br>
====Resetting Quest Timers====
*To reset a players quest timer manually, select the player
*Use <code>@qst erase {quest_name}</code> to delete the quest from the player, thus resetting the timer.
<br>
<br>
===Disruptive Players===
====Squelching====
*Use <code>@gag {character_name}</code> to prevent a character from being able to speak.
*Use <code>@ungag {character_name}</code> to allow a player to speak again.
<br>
<br>
====Booting a player off the server====
To boot a character from the game enter <code>@boot char character_name</code>.
*The player can log back in again unless you ban them first, however booting can be a good form of warning.
<br>
The player will be immediately logged off and the client will show a blue window with a message box.
The message box says '''"You have been booted from Asheron's Call for Code of Conduct Violations."'''
<br>
<br>
====Bans====
To see all banned accounts enter <code>@banlist</code>.

To ban an account do the following:
<blockquote>
#Use <code>@finger {character_name}</code> to get the account name.
#Use <code>@ban {ACCOUNT_name} {days} {hours} {minutes} {reason}</code>
##e.g. <code>@ban their_account 1 0 0 You have been banned for 24 hours because of X reason</code>

The player will be immediately logged off and the client will show a blue window with a message box.
The message box says "You have been booted from Asheron's Call. - You have been banned for 24 hours because of X reason".
</blockquote>

To unban an account do the following:
<blockquote>
#Use <code>@finger {character_name}</code> to get their '''account name''' if you don't have it.
#Use <code>@unban {ACCOUNT_name}</code>
</blockquote>
<br>
<br>
<br>
<hr>
==Spawning items==
===Introduction to Spawning===
All objects, whether they are clothing, weapons, jewelry or even portals are known as "weenies".
#To edit an object you firstly need it's '''wcid'''.
#To locate an items wcid, search for it at http://ac.yotesfan.com/weenies/

===Spawn an Item===
To spawn an item using the wcid or classname you have obtained in the previous section, enter:
<code>@create <wcid or classname> (amount) (palette) (shade)</code>

Example:<br>
How to spawn 1 unit of Aerfalle's Pallium (robe)... it will spawn on the ground in front of the admin.
*<code>@create 8133 1</code>
<br>
<br>
<br>
<hr>
==Editing items==
===Introduction to Editing===
All objects, whether they are clothing, weapons, jewelry or even portals are known as "weenies".
To edit an object you firstly need it's '''classId'''.

To obtain the classId you can:
#Search for it on http://ac.yotesfan.com/weenies/
#Select it ingame and enter the <code>@getinfo</code> command.
<br>
<br>
<br>
===Adding Bonus to Mana Conversion to a quest item===
With the classId you obtained from the Introduction section:

#From the server console enter <code>@export-sql {classId}</code>
#Edit the extracted file and look for the line starting with <code>INSERT INTO `weenie_properties_float`</code> (around line 30 to 34 often)
##At the end of the section add <code>     , (10731, 144,     0.x) /* ManaConversionMod */;</code> where x can range from 0.01 (1%) to 0.2 (20%)
#From the server console enter <code>/import-sql {classId}</code>
<br>
Example editing a Quiddity Orb to add Bonus to Mana Conversion:
<br>
Before:
<blockquote>
INSERT INTO `weenie_properties_float` (`object_Id`, `type`, `value`)<br>
VALUES (10731,   5,   -0.05) /* ManaRate */<br>
     , (10731,  12,     0.5) /* Shade */<br>
     , (10731,  29,       1) /* WeaponDefense */<br>
     , (10731,  76,     0.5) /* Translucency */;
</blockquote>
<br>
After (new line with attribute 144 added):
<blockquote>
INSERT INTO `weenie_properties_float` (`object_Id`, `type`, `value`)<br>
VALUES (10731,   5,   -0.05) /* ManaRate */<br>
     , (10731,  12,     0.5) /* Shade */<br>
     , (10731,  29,       1) /* WeaponDefense */<br>
     , (10731,  76,     0.5) /* Translucency */<br>
     , (10731, 144,     0.1) /* ManaConversionMod */;
</blockquote>
<br>
NOTE: this will not update existing Quiddity Orbs in the game, only new ones given as a quest reward. (JasonFJ note: need to figure out how to spawn an NPC that will accept pre-patch items (e.g. the Quiddity Orb in my example above) with customized content).
<br>
<br>
<br>
===Portals (changing level, tie, summonable attributes)===
With the classId you obtained from the Introduction section:

#From the server console enter <code>@export-sql {classId}</code>
#Edit the extracted file and go to line 10 (or whatever line has "PortalBitmask" mentioned on it).
##change the value from 49 (not tieable, not summonable) to 1 (unrestricted). For a list of all bits see [https://github.com/ACEmulator/ACE/blob/master/Source/ACE.Entity/Enum/PortalBitmask.cs PortalBitMask reference]
#*Optionally: you can also change level restrictions by changing the MinLevel (attr. 86) usually on line 9.
#From the server console enter <code>/import-sql {classId}</code>
#To make the change immediate instead of rebooting the server, a character near the portal can enter in the ingame AC client command<code>@reload-landblock</code>
<br>
<br>
<br>
<hr>
==Managing Events==
===Send an event text to all players on the server===
Event messages do not include any information about the admin sending it... it literally sends the text as it is typed.
Use the <code>@we</code> command to broadcast a message to all players.
*<code>@we There is a disturbance in the lands of Dereth.</code>

Players will see the following in green text:
<BR>
''There is a disturbance in the lands of Dereth.''
<br>
<br>
<br>

===Generating a monster spawn===
#Go to http://ac.yotesfan.com/weenies/ and search for ''generator'' to list different monster generators and their unique ''wcid'' identifier.
#Go to where you would like to spawn the monster class and enter <code>@addenc {wcid}</code>

IMPORTANT:
*You can generate one encounter per cell, where a cell is about 20 feet by 20 feet in size.
*Once the encounter is created, defeated monsters will keep respawning.
<br>
<br>
<br>
<hr>
==Introduction to Custom Content==
You can do this like this:
#create a NPC shop vendor anywhere
#create an NPC that will exchange item X for item Y

===Creating a vendor NPC===
'''A. Lifestoned.org Steps'''
<br>
#Create an account on https://lifestoned.org/  (Use https://lifestoned.net/ if the site is down, as the domain expired per their Discord.)
##Choose menu '''Weenies'''
##Enter ''jeweler'' in the Name box and click '''Search'''
##On the second for ''Urmolt the Jeweler'' click on the Downloads and choose ''Original''. Save this file to your ACE server installation at the following relative path: ''\ACE\Server\Content\json\weenies''
##Go to the file location and rename the file from ''665 - Urnolt the Jeweler.json'' to ''300000 - My New Jeweler.json''. The value of 300000 is a unique custom value, but you can use any value from 200000 upward. Try to avoid using 600000-699999 as this is used by a community of content creators.
###Edit the file using Notepad and where it says ''{"wcid":665'' change the value from ''665'' to ''300000''. 
##Choose menu '''Weenies menu -> Upload JSON Data''' and select the file you just renamed.
##Choose menu ''Sandbox'', then for ''Umolt the Jeweler' entry choose '''Edit'''
###If not already selected, choose the '''String''' tab, and go to the ''01 - Name'' property and change ''Umolt the Jeweler'' to ''My New Jeweler'.
###On the far left side vertical menu, choose the '''Change Log/History''' icon (buttom icon) and if it's blank enter any text.
###On the far left side vertical menu, choose the '''Emotes''' menu (triangle icon, second from bottom)
####For the first emote (Open), click the '''+ Actions''' button to expand the section
####Change the text from ''Welcome to my shop.  What can I do for you?'' to ''This is how to change text for an NPC!'
###On the far left side vertical menu, choose the '''Save''' menu (flag icon, at the top)
<br>
'''B. ACE Server Steps'''
<br>
#Enter the command <code>import-json 300000</code>
<br>
'''B. Admin Steps'''
<br>
#Go to the location where you want the NPC and enter <code>@createinst 300000</code>. NOTE: if you're just testing and want the vendor to despawn in 5 minutes, use <code>@create</code> instead of <code>@createinst</code>.
#You can move the NPC to where you are standing by selecting it, appraising it, then entering <code>@movetome</code>.
<br>
''Congratulations! You should now have your new, customized Jeweler NPC created!''

