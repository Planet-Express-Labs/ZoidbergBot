# How we use and store your data.
We are very serious about keeping your data private. We want to be as transparent as possible with your data. 

# What do we store? 
Currently, our databases don't store very much information. Here's an overview of what's stored.  

## Main bot: 
![fun and fancy code](https://user-images.githubusercontent.com/45272685/120039158-73193000-bfd2-11eb-94a2-dd13008b9bd6.png)
- The guild column stores the guild id for your server. This is a unique identifer for your server that allows us to track what server is what. From this we can find the guild's members, name, etc. 
- The prefix is what you put before a command to trigger the bot, and hopefully not some other bot. (!help as opposed to /help)
- Enabled_modules stores which cogs the bot should use on a specific server. This is used so you can mass-disable commands in a group - such as disabling everything in confession. 
- Admin and mod roles stores which roles are allowed to use certain commands. More information on this is in the wiki. 
- Cooldown stores the amount of time allowed between each command. This is currently unused. 
- Auto_delete store the amount of time the bot will wait before deleting it's messages. This is also currently unused. 
- Premium is just a boolean that stores if your server has an active premium subscription. This is unused until we actually make this a thing. Don't expect it any time soon.


## Confession cog:
![like actually the best code ever](https://user-images.githubusercontent.com/45272685/120039192-7e6c5b80-bfd2-11eb-84d8-e72d03f07c29.png)
> Nice comments.
- The guild column is the unique ID for your server, just let's us track where to send confessions.
- The confess_channel is the ID for the specific channel where we send the confessions.
- The log_channel is where the bot sends confessions with additional metadata, like their username.
- Last_message_number is the suboptimal way we keep track of the number of the last confession.  
