from src.main.DB.DBUtility import DBUtility
from src.main.DB.DBConstants import DBConstants
from src.main.OZAPIConstants import IntentConstants
from src.main.Intents.IntentBase import IntentBase
from src.main.Utility import Utility
from src.main.DB.DBUtility import DBUtility
from src.main.OZAPIConstants import EntityConstants
from flask import session

class ClassAuthorName(IntentBase):
    def __init__(self, request):
        self.request = request
        self.initParameters()

    def initParameters(self):
        self.className = Utility.getParm(self.request, EntityConstants.CLASS_NAME)

    def ProcessRespone(self):
        response = ""
        connection = DBUtility.getMYSQLConnection();
        try:
            with connection.cursor() as cursor:
                sql = "SELECT CommitClass.CommitID, GitInfo.aName, GitInfo.aDate FROM CommitClass INNER JOIN GitInfo ON CommitClass.CommitID=GitInfo.cHash where CommitClass.ProjectID = %s and CommitClass.ClassId like %s ORDER BY GitInfo.aDate ASC limit 1"
                cursor.execute(sql, (session["projectID"], self.className+"%"))
                result = cursor.fetchone()

                if result == '':
                    response = "I could not find the author, please check the class name."
                else:
                    response = result[DBConstants.aName] + "\n"
                print("----------------RESULT------------------")
                print(response)
        finally:
            connection.close()



        return response