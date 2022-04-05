from abc import ABC, abstractmethod


class DatabaseAbsClass(ABC):

    @abstractmethod
    def insertData(self, fileLocation):
        pass

    @abstractmethod
    def updateData(self, fileLocation):
        pass

    @abstractmethod
    def deleteData(self, fileLocation):
        pass

    @abstractmethod
    def selectData(self, fileLocation):
        pass

    @abstractmethod
    def connectUser(self, fileLocation):
        pass

    @abstractmethod
    def disconnectUser(self):
        pass

    @abstractmethod
    def commitDB(self):
        pass

