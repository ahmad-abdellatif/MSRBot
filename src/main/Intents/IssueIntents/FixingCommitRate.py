from src.main.OZAPIConstants import IntentConstants
from src.main.DB.DBUtility import DBUtility
from src.main.Intents.IntentBase import IntentBase
from flask import session

class FixingCommitRate(IntentBase):
    def __init__(self, intnet, request):
        self.request = request
        self.intent = intnet

    def ProcessRespone(self):
        connection = DBUtility.getMYSQLConnection();
        try:
            with connection.cursor() as cursor:

                # Fixing Rate Query
                if(self.intent == IntentConstants.Fixing_COMMITS_RATE):
                    sql = "select (100 * (select count(*) from Gitinfo where ProjectID=%s and fix = TRUE) / (select count(*)  from Gitinfo where ProjectID=%s)) as percentage"
                    response = "The  percentage of fixing commits is %"
                else:
                # Buggy Rate Query
                    sql = "select (100 * (select count(*) from Gitinfo where ProjectID=%s and contains_bug = TRUE) / (select count(*)  from Gitinfo where ProjectID=%s)) as percentage"
                    response = "The  percentage of buggy commits is %"

                cursor.execute(sql, (session["projectID"], session["projectID"]))
                result = cursor.fetchone()
                result = result['percentage']
                response += str(result)
                if str(result) == "0":
                    response = "Woow! All of the fixing commits are perfect, they did not introduce any bug till this moment :)"
                print("----------------RESULT------------------")
                print(response)
        finally:
            connection.close()

        return response