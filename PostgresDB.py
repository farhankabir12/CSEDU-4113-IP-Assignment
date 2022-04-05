import psycopg2
from DatabaseAbsClass import DatabaseAbsClass
import xml.etree.ElementTree as ET


class PostgresDB(DatabaseAbsClass):

    def __init__(self):
        self.mydb

    def connectUser(self, fileLocation):
        try:
            configFile = ET.parse(fileLocation).getroot()

            host = (configFile.find('host')).text
            user = (configFile.find('user')).text
            passwd = (configFile.find('passwd')).text
            database = (configFile.find('database')).text

            self.mydb = psycopg2.connector.connect(host=host, user=user, passwd=passwd, database=database)
            print("Connected")
        except psycopg2.connector.Error as err:
            print("Connection or file Error".format(err))

    def insertData(self, fileLocation):
        root_node = ET.parse(fileLocation).getroot()
        if self.mydb.is_connected():
            insert = root_node.findall('insert')
            for i in insert:
                table = ""
                value = "("
                if i[0].tag == "table":
                    table = i[0].text
                if i[1].tag == "value":
                    for k in range(4):
                        if k < 3:
                            value += "'" + i[1][k].text + "',"
                        else:
                            value += "'" + i[1][k].text + "')"
                myCursor = self.mydb.cursor()
                insertQuery = "insert into " + table + " values " + value
                try:
                    myCursor.execute(insertQuery)
                except mysql.connector.Error as err:
                    print("Could not insert".format(err))
        else:
            print("Database not connected")

    def updateData(self, fileLocation):
        try:
            root_node = ET.parse(fileLocation).getroot()
        except mysql.connector.Error as err:
            print("File error".format(err))

        if self.mydb.is_connected():
            update = root_node.findall('updateall/update')
            for i in update:
                table = ""
                setValues = ""
                condition = ""
                if i[0].tag == "table":
                    table = i[0].text
                if i[1].tag == "value":
                    for k in range(len(i[1])):
                        if k < len(i[1]) - 1:
                            setValues += i[1][k].tag + " = '" + i[1][k].text + "',"
                        else:
                            setValues += i[1][k].tag + " = '" + i[1][k].text + "'"
                if i[2].tag == "condition":
                    for k in range(len(i[2])):
                        if k < len(i[2]) - 1:
                            condition += i[2][k].tag + " = '" + i[2][k].text + "',"
                        else:
                            condition += i[2][k].tag + " = '" + i[2][k].text + "'"

                myCursor = self.mydb.cursor()
                updateQuery = "update " + table + " set " + setValues + " where " + condition
                myCursor.execute(updateQuery)
            print("Data updated")
        else:
            print("Database not connected")

    def deleteData(self, fileLocation):
        try:
            root_node = ET.parse(fileLocation).getroot()
        except mysql.connector.Error as err:
            print("File error".format(err))

        if self.mydb.is_connected():
            delete = root_node.findall('delete')
            for i in delete:
                table = ""
                condition = ""
                if i[0].tag == "table":
                    table = i[0].text

                if i[1].tag == "condition":
                    for k in range(len(i[1])):
                        if k < len(i[1]) - 1:
                            condition += i[1][k].tag + " = '" + i[1][k].text + "' and "
                        else:
                            condition += i[1][k].tag + " = '" + i[1][k].text + "'"
                myCursor = self.mydb.cursor(buffered=True)
                deleteQuery = "delete from " + table + " where " + condition
                myCursor.execute(deleteQuery)
                myCursor.execute("select * from studentinfo")
                results = []
            return print("Data deleted")
        else:
            print("Database not connected")

    def selectData(self, fileLocation):
        try:
            root_node = ET.parse(fileLocation).getroot()
        except mysql.connector.Error as err:
            print("File error".format(err))

        if self.mydb.is_connected():
            myCursor = self.mydb.cursor()

            select = root_node.findall('select')
            for i in select:
                table = ""
                attributes = ""
                if i[0].tag == "table":
                    table = i[0].text

                if i[1].tag == "columns":
                    for k in range(len(i[1])):
                        if k == 0:
                            attributes += i[1][k].text
                        else:
                            attributes += "," + i[1][k].text

            selectCommand = "select " + attributes + " from " + table

            myCursor.execute(selectCommand)
            results = []
            # print("Selected Data:")
            for i in myCursor:
                print(i)
                results.append(i)
            return results
        else:
            print("Database not connected")

    def disconnectUser(self):
        self.mydb.close()
        self.myCursor.close()

    def commitDB(self):
        self.mydb.commit()