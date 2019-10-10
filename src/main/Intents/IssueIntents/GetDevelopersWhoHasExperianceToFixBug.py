from src.main.Intents.IntentBase import IntentBase
from src.main.Utility import Utility
from src.main.DB.DBUtility import DBUtility
from src.main.OZAPIConstants import EntityConstants
from src.main.DB.DBConstants import DBConstants
from flask import session


class GetDevelopersWhoHasExperianceToFixBug(IntentBase):

    def __init__(self, request):
        self.request = request
        self.initParameters()

    def initParameters(self):
        self.className = Utility.getParm(self.request, EntityConstants.CLASS_NAME)

    def ProcessRespone(self):
        print(self.className)
        response = ""
        count = 1;
        connection = DBUtility.getMYSQLConnection();
        try:
            with connection.cursor() as cursor:

                sql = "select GitInfo.aName ,count(GitInfo.aName) as countCommit from GitInfo inner join CommitClass on GitInfo.cHash = CommitClass.CommitID and GitInfo.fix=true and GitInfo.ProjectID=%s and CommitClass.ClassID like %s group by GitInfo.aName order by countCommit DESC limit 5"
                cursor.execute(sql, (session["projectID"], self.className + "%"))
                result = cursor.fetchone()
                response = "The developers that fixed most of the bugs in the specified class are:" + "\n"
                while (result):
                    response += str(count) +"- " + str(result[DBConstants.aName]) + "\n"
                    result = cursor.fetchone()
                    count+=1

            if count == 1:
                response = "I could not find the developers who made fixes on the mentioned class."

        finally:
            connection.close()


        return response