class Command:

    def __init__(self, cmd, callback):
        self.__cmd__ = cmd
        self.__callback__ = callback


    def execute(self, params):
        self.__callback__(*params)

    def name(self):
        return self.__cmd__
