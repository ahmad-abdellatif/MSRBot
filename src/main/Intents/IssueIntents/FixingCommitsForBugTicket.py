from src.main.DB.DBUtility import DBUtility
from src.main.DB.DBConstants import DBConstants
from src.main.OZAPIConstants import IntentConstants
from src.main.Intents.IntentBase import IntentBase
from src.main.Utility import Utility
from src.main.DB.DBUtility import DBUtility
from src.main.OZAPIConstants import EntityConstants
import datetime
from flask import session

class FixingCommitsForBugTicket(IntentBase):
    def __init__(self, request):
        self.request = request
        self.initParameters()

    def initParameters(self):
        self.jiraTicket = Utility.getParm(self.request, EntityConstants.JIRA_TICKETS)

    def ProcessRespone(self):

        count = 1
        response = ""
        connection = DBUtility.getMYSQLConnection();
        try:
            with connection.cursor() as cursor:
                print ("---------------->" + str(self.jiraTicket))
                sql = "select * from GitInfo as commits left join COMMITS_ISSUES on commits.cHash = COMMITS_ISSUES.Commit_Hash where commits.ProjectID=%s and COMMITS_ISSUES.JIRA_Id like %s and commits.fix = TRUE"
                cursor.execute(sql, (session["projectID"], "%"+self.jiraTicket+"%"))

                result = cursor.fetchone()
                print(result)
                while (result):
                    response += "Commit Hash:" + str(result[DBConstants.Hash]) + "\n"
                    response += "Name: " + str(result[DBConstants.aName]) + "\n"
                    response += "Date: " + str(datetime.datetime.fromtimestamp(int(result[DBConstants.aDate])).strftime(
                        '%Y-%m-%d %H:%M:%S')) + "\n"
                    response += "Body: " + str(result[DBConstants.Body]) + "\n"
                    response += "--------------------------------------------------- \n"
                    result = cursor.fetchone()
                    print(result)

                if response == '':
                    response = "Sorry, I am unable to find a fixing commit for " + self.jiraTicket

                print("----------------RESULT------------------")
                print(response)
        finally:
            connection.close()



        return response