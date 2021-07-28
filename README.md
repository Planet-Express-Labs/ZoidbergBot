<img align="left" width=500 src="https://user-images.githubusercontent.com/45272685/118345209-fb8ecf80-b500-11eb-9f24-d662a27818dc.jpg">

```

8888888888P         d8b      888 888                                    888               888
      d88P          Y8P      888 888                                    888               888
     d88P                    888 888                                    888               888
    d88P    .d88b.  888  .d88888 88888b.   .d88b.  888d888 .d88b.       88888b.   .d88b.  888888
   d88P    d88""88b 888 d88" 888 888 "88b d8P  Y8b 888P"  d88P"88b      888 "88b d88""88b 888
  d88P     888  888 888 888  888 888  888 88888888 888    888  888      888  888 888  888 888
 d88P      Y88..88P 888 Y88b 888 888 d88P Y8b.     888    Y88b 888      888 d88P Y88..88P Y88b.
d8888888888 "Y88P"  888  "Y88888 88888P"   "Y8888  888     "Y88888      88888P"   "Y88P"   "Y888
                                                               888
                                                          Y8b d88P
                                                           "Y88P"
```

Public branch of Zoidberg. Feature request should go in issues. Discord bot that allows you to send confession messages
into a channel without revealing your username to the server.

# Install

Hosted Zoidberg is running on the Azure Ubuntu:latest image. We have a test environment running on Heroku and our deveopers mostly use Windows. There should not be issues with running on different platforms, however we recomend you follow our environment as close as possible. 

Installation is simple.

1. Run `git clone https://github.com/LiemEldert/confessbot-public.git`in a terminal in whatever directory you want the
   server to be stored in.
2. Edit the config_template file and save as `config.ini`. More detailed instructions are inside the file. 

      a: Make a bot account here: discord.com/developers/ 

      b: Make an account on huggingface.co/

      b: To copy the chanel ids, you need to enable developer mode in the settings.

      c: Under the right click menu, there should be an option to copy ids. You need to do this in order to configure the
   bot correctly. To get the server's id, right click the guild name in the upper left. 

      d: Configure logging. 

      e: ***Save the file as `config.ini`!***

3. Run the bot by opening the bot's directory in the termainal and run `python bot.py`. Depending on your installation,
   you might need to use the specific python version instead (ie. python3.7 or python3).
4. Set up is done. This process will likely change soon as we impliment features. View below for more details on what
   will change and how this will effect you.

# Someone really needs to update this readme.
