# TwitchBotPy
Minimal python library for creating a twitch bot

## Installing
You can easily install this package via pip

```shell
pip3 install --index-url https://test.pypi.org/simple/ twitchbot
````

## Basics
```python
from bot import Command, TwitchBot
from secrets import username, oauth

# Creating the bot
twitch_bot = TwitchBot(username, oauth)

# Creating a sample command
hello_command = Command("hello", lambda msg, who, channel : bot.send_message_to(channel, "Hello, @"+who) )

# Registering the command
twitch_bot.add_command(hello_command)
 
# Connecting to twitch, to channels "channel" and "channel2" 
twitch_bot.connect(channels=["channel"])
twitch_bot.join("channel2")

# The bot starts listening
twitch_bot.start_listening()

while True:
  pass
```
  
