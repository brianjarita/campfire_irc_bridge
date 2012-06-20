campfire_irc_bridge
===================

Campfire IRC bridge

Getting Started
---------------
1. Download and setup pyfire <https://github.com/mariano/pyfire>
2. Setup an IRC server (or use one that exists)
2. Update the settings/__init__.py file with your user settings.
3. Update the nickname on line 38
4. Update the IRC channel on line 189. The first param should be an active irc channel
(i am using it as a trigger) and the second param should be where you want the
messages to go.
5. Update line 123 to match the messages channel


Optional
---------------
Update the header prefix on line 124

Usage
---------------
python camfire_irc_bot.py

To send a message to the campfire room send a private message to the bot.
To view the messages in the campfire room be in the messages irc channel.


