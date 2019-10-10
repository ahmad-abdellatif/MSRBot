from src.main.DB.DBUtility import DBUtility
from src.main.DB.DBConstants import DBConstants
from src.main.OZAPIConstants import IntentConstants
from src.main.Intents.IntentBase import IntentBase
from src.main.Utility import Utility
from src.main.DB.DBUtility import DBUtility
from src.main.OZAPIConstants import EntityConstants
import time
import datetime
from flask import session

class GetInfoAboutClass(IntentBase):
    def __init__(self, request, isLatest):
        self.request = request
        self.initParameters()
        self.isLatest = isLatest

    def initParameters(self):
        self.className = Utility.getParm(self.request, EntityConstants.CLASS_NAME)

    def ProcessRespone(self):

        response = ""
        connection = DBUtility.getMYSQLConnection();
        try:
            with connection.cursor() as cursor:

                if(self.isLatest):
                    sql = "SELECT Distinct GitInfo.aName, GitInfo.aDate, GitInfo.Body FROM CommitClass INNER JOIN GitInfo ON CommitClass.CommitID=GitInfo.cHash where CommitClass.ProjectID=%s and CommitClass.ClassId like %s ORDER BY GitInfo.aDate DESC Limit 3"
                else:
                    sql = "SELECT Distinct GitInfo.aName, GitInfo.aDate, GitInfo.Body FROM CommitClass INNER JOIN GitInfo ON CommitClass.CommitID=GitInfo.cHash where CommitClass.ProjectID=%s and CommitClass.ClassId like %s ORDER BY GitInfo.aDate DESC"

                cursor.execute(sql, (session["projectID"], self.className+"%"))

                result = cursor.fetchone()
                while (result):
                    response += "Name: " + str(result[DBConstants.aName]) + "\n"
                    response += "Date: " + str(datetime.datetime.fromtimestamp(int(result[DBConstants.aDate])).strftime('%Y-%m-%d %H:%M:%S')) + "\n"
                    response += "Body: " + str(result[DBConstants.Body]) + "\n"
                    response += "--------------------------------------------------- \n"
                    result = cursor.fetchone()

                if result == '':
                    response = "I could not find the developers who made the change, please check the class name."

                print("----------------RESULT------------------")
                print(response)
        finally:
            connection.close()



        return response