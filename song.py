class Song:
    def __init__(self, name, path, extension):
        self.__name = name
        self.__path = path
        self.__extension = extension

    @property
    def extension(self):
        return self.__extension

    @property
    def path(self):
        return self.__path

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    def __str__(self):
        return f"{self.__name} - {self.__extension} - {self.__path}"
