# How we use and store your data.
We are very serious about keeping your data private. We want to be as transparent as possible with your data. 

# What do we store? 
Currently, our databases don't store very much information. Here's an overview of what's stored.  

## Main bot: 
<img src="https://i.imgur.com/QlF7F5H.png">
The guild column stores the guild id for your server. This is a unique identifer for your server that allows us to track what server is what. From this we can find the guild's members, name, etc. 
The prefix is what you put before a command to trigger the bot, and hopefully not some other bot. (!help as opposed to /help)
Enabled_modules stores which cogs the bot should use on a specific server. This is used so you can mass-disable commands in a group - such as disabling everything in confession. 
Admin and mod roles stores which roles are allowed to use certain commands. More information on this is in the wiki. 
Cooldown stores the amount of time allowed between each command. This is currently unused. 
Auto_delete store the amount of time the bot will wait before deleting it's messages. This is also currently unused. 
Premium is just a boolean that stores if your server has an active premium subscription. This is unused until we actually make this a thing. Don't expect it any time soon.
