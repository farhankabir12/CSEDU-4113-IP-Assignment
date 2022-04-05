from MySQLDB import MySQLDB
from PostgresDB import  PostgresDB
from flask import Flask
from flask_restful import Resource, Api, reqparse
import xml.etree.ElementTree as ET
import mysql.connector



app = Flask(__name__)
api = Api(app)


class StudentInfo(Resource):
    def get(self):
        return database.selectData('query.xml')

    def post(self):
        database.insertData("query.xml")


    # def put(self):                                does not work (updateData)
    #     database.updateData("query.xml")


    def delete(self):
        database.deleteData("query.xml")



api.add_resource(StudentInfo, '/', '/<int:id>')

if __name__ == '__main__':
    try:
        root_node = ET.parse('config.xml').getroot()
    except mysql.connector.Error as err:
        print("Error".format(err))

    dbType = (root_node.find('dbtype')).text

    if dbType == 'MySQL':
        database = MySQLDB()
    elif dbType == 'PostgreSQL':
        database = PostgresDB()

    configFile = 'config.xml'
    database.connectUser(configFile)

    app.run(debug=True)
    print('Server is live!')
