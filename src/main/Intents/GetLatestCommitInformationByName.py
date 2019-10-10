from src.main.DB.DBUtility import DBUtility
from src.main.Utility import Utility
from src.main.OZAPIConstants import EntityConstants
from src.main.DB.DBConstants import DBConstants
from src.main.OZAPIConstants import IntentConstants
from src.main.Intents.IntentBase import IntentBase
from flask import session

class GetLatestCommitInformationByName(IntentBase):
    def __init__(self, request):
        self.request = request
        self.initParameters()

    def initParameters(self):
        self.devName = Utility.getParm(self.request, EntityConstants.DEVELOPERS_NAME_ENTITY)

    def ProcessRespone(self):
        response = ""
        connection = DBUtility.getMYSQLConnection();
        try:
            with connection.cursor() as cursor:
                sql = "SELECT aDate,Body FROM OZBOT.GitInfo where aName = %s and ProjectID = %s ORDER BY aDate DESC limit 10;"
                cursor.execute(sql, (self.devName,session["projectID"]))
                result = cursor.fetchone()
                while (result):
                    response += "Date: " + result[DBConstants.aDate] + "\n"
                    response += "Body: " + result[DBConstants.Body] + "\n"
                    result = cursor.fetchone()
                print("----------------RESULT------------------")
                print(response)
        finally:
            connection.close()


        return response