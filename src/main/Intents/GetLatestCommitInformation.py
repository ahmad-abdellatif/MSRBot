from src.main.DB.DBUtility import DBUtility
from src.main.DB.DBConstants import DBConstants
from src.main.OZAPIConstants import IntentConstants
from src.main.Intents.IntentBase import IntentBase
from flask import session

class GetLatestCommitInformation(IntentBase):
    def __init__(self, request):
        self.request = request

    def ProcessRespone(self):
#SELECT cName,cDate,Body FROM OZBOT.GitInfo ORDER BY cDate DESC limit 10;
        response = ""
        connection = DBUtility.getMYSQLConnection();
        try:
            with connection.cursor() as cursor:
                sql = "SELECT aName,aDate,Body FROM OZBOT.GitInfo where ProjectID=%s ORDER BY aDate DESC limit 10"
                cursor.execute(sql, (session["projectID"]))
                result = cursor.fetchone()
                while (result):
                    response += "Name: " + result[DBConstants.aName] + "\n"
                    response += "Date: " + result[DBConstants.aDate] + "\n"
                    response += "Body: " + result[DBConstants.Body] + "\n"
                    result = cursor.fetchone()
                print("----------------RESULT------------------")
                print(response)
        finally:
            connection.close()



        return response