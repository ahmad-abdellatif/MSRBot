from src.main.DB.DBConstants import DBConstants
from src.main.Intents.IntentBase import IntentBase
from src.main.DB.DBUtility import DBUtility
from flask import session

class MostFileContainsBugs(IntentBase):
    def __init__(self, request):
        self.request = request

    def ProcessRespone(self):

        count = 1
        response = ""
        connection = DBUtility.getMYSQLConnection();
        try:
            with connection.cursor() as cursor:

                sql = 'SELECT DISTINCT(ClassID), count(ClassID) AS count FROM CommitClass left join GitInfo on CommitClass.CommitID=GitInfo.cHash where CommitClass.ProjectID=%s and GitInfo.contains_bug=TRUE GROUP BY ClassID HAVING count > 1 order by count DESC limit 10;'
                cursor.execute(sql, (session["projectID"]))
                result = cursor.fetchone()
                while (result):
                    response += str(count) + "- " + str(result[DBConstants.ClassID]) + " has " + str(result["count"]) + " buggy commits" +  "\n\n"
                    result = cursor.fetchone()
                    count += 1

                if response == "":
                    response = "Wow! There are no buggy files in the repo"

                print("----------------RESULT------------------")
                print(response)
        finally:
            connection.close()



        return response