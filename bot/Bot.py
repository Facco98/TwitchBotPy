import websocket
from threading import Thread
from bot.Command import Command
import time

class Bot:

    def __init__(self, username, password, host):
        self.__commands = dict()
        self._username = username
        self._password = password
        self.__host = host
        self.__threadStarted = False
        self.__thread = None


    def connect(self):
        self.__websocket = websocket.create_connection(self.__host)


    def join(self, channel):
        self.__websocket.send("JOIN #" + channel)

    def send(self, msg):
        self.__websocket.send(msg)

    def send_message_to(self, channel, message=""):
        self.__websocket.send("PRIVMSG #" + channel + " :" + message)

    def start_listening(self, callback):
        try:
            if not self.__threadStarted:
                self.__thread = Thread(target=self.__listen_function__, args=(callback,))
                self._thread.deamon = True
                self.__threadStarted = True
                self.__thread.start()
        except Exception:
            pass


    def __listen_function__(self, callback):
        try:
            while self.__threadStarted:
                received = self.__websocket.recv()
                callback(received)
        except Exception:
            pass

    def stop_listening(self):
        self.__threadStarted = False
        self.__thread = None

    def disconnect(self):
        if self.__threadStarted:
            self.stop_listening()
        self.__websocket.close()

    def add_command(self, command):
        if isinstance(command, Command):
            self.__commands[command.name()] = command
        else:
            raise ValueError("\"command\" must be an instance of class Command")

    def responds_to(self, cmd):
        return cmd in self.__commands

    def execute_command(self, cmd, params):
        if self.responds_to(cmd):
            self.__commands[cmd].execute(params)


class TwitchBot(Bot):

    def __init__(self, username, password):
        super().__init__(username, password, "ws://irc-ws.chat.twitch.tv:80")
        self.on_message = self.__default_on_message
        self.on_command = self.__default_on_command
        self.unknown_command =  self.__defualt_unknown_command

    def connect(self, channels=[]):
        super().connect()
        super().send("PASS " + self._password)
        super().send("NICK " + self._username)
        for channel in channels:
            self.join(channel)

    def start_listening(self, callback=None ):
        if callback is None:
            super().start_listening(self.dispatch)
        else:
            super().start_listening(callback)

    def dispatch(self, msg):
        if msg == "PING :tmi.twitch.tv":
            super().send("PONG :tmi.twitch.tv")
            print("PING")
        else:
            try:
                finenome = msg.index("!")
                who = msg[1:finenome]

                inizioCanale = msg.index("#")
                fineCanale = msg.index(" :")

                canale = msg[inizioCanale+1:fineCanale]
                content = msg[fineCanale+2: ]
                if content.startswith("!"):
                    cmd, other = self.__parse_command(content+" ")
                    self.on_command(cmd.strip(), other.strip(), who, canale)
                else:
                    self.on_message(content.strip(), who, canale)
            except Exception:
                pass

    def __parse_command(self, str):

        try:
            finecomando = str.find(" ")
            cmd = str[1:finecomando]
            content = str[finecomando+1:]
            return cmd, content
        except Exception as ex:
            print(str, ex)



    def __default_on_message(self, msg, who, channel):
        pass

    def __default_on_command(self, cmd, other, who, channel):
        if super().responds_to(cmd):
            super().execute_command(cmd, [other, who, channel])
        else:
            self.unknown_command(cmd, who, channel)

    def __defualt_unknown_command(self, cmd, who, channel):
        super().send_message_to("#"+channel, "@" + who + ", unknown command")



