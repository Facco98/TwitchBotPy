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
## Advanced
You can easily costumize what the bot does when a message is received, when a command is executed or when a user tries to run an unknown command.

```python
.
.
twitch_bot = TwitchBot(username, oauth)
twitch_bot.on_message = lambda msg, who, channel : {
  # Your code goes here
}

twitch_bot.on_command = lambda cmd, other, who, channel : {
  # Your commands handling logig
}

twitch_bot.unknown_command = lambda cmd, who, channel : {
  # Handle and unsupported command logic
}
.
.

````

You can even define your own callback and handle directly the string twitch sends you
```python
.
.
twitch_bot = TwitchBot(username, oauth)
twitch_bot.connect()
twitch_bot.join("Channel")
twitch_bot.start_listening(callback=lambda msg : {
  # Handle the raw string from twitch
})

.
.
```

