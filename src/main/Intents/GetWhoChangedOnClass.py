from src.main.DB.DBUtility import DBUtility
from src.main.DB.DBConstants import DBConstants
from src.main.OZAPIConstants import IntentConstants
from src.main.Intents.IntentBase import IntentBase
from src.main.Utility import Utility
from src.main.DB.DBUtility import DBUtility
from src.main.OZAPIConstants import EntityConstants
from flask import session

class GetWhoChangedOnClass(IntentBase):
    def __init__(self, request):
        self.request = request
        self.initParameters()

    def initParameters(self):
        self.className = Utility.getParm(self.request, EntityConstants.CLASS_NAME)

    def ProcessRespone(self):

        count = 1
        response = ""
        connection = DBUtility.getMYSQLConnection();
        try:
            with connection.cursor() as cursor:
                print ("---------------->" + str(self.className))
                sql = "SELECT distinct(GitInfo.aName) FROM CommitClass INNER JOIN GitInfo ON CommitClass.CommitID=GitInfo.cHash where CommitClass.ProjectID=%s and CommitClass.ClassId like %s"
                cursor.execute(sql, (session["projectID"],"%"+self.className+"%"))
                result = cursor.fetchone()
                print(result)
                while (result):
                    response += str(count) + "- " + result[DBConstants.aName] + "\n"
                    result = cursor.fetchone()
                    count+=1
                    print(result)

                if result == '':
                    response = "I could not find the developers who made the change, please check the class name."

                print("----------------RESULT------------------")
                print(response)
        finally:
            connection.close()



        return response