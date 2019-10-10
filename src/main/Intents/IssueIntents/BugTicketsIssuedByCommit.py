from src.main.DB.DBUtility import DBUtility
from src.main.DB.DBConstants import DBConstants
from src.main.OZAPIConstants import IntentConstants
from src.main.Intents.IntentBase import IntentBase
from src.main.Utility import Utility
from src.main.DB.DBUtility import DBUtility
from src.main.OZAPIConstants import EntityConstants
import datetime
from flask import session

class BugTicketsIssuedByCommit(IntentBase):
    def __init__(self, request):
        self.request = request
        self.initParameters()

    def initParameters(self):
        self.commitHash = Utility.getParm(self.request, EntityConstants.COMMIT_HASH)
#How many new bugs are introduced for every bug that is fixed?
    def ProcessRespone(self):

        count = 1
        response = ""
        fixes = []
        noResults = True
        connection = DBUtility.getMYSQLConnection();
        try:
            with connection.cursor() as cursor:
                print ("---------------->" + str(self.commitHash))

                #Get the fixes commits
                sql = "select fixes from GitInfo where ProjectID=%s and cHash = %s"
                cursor.execute(sql, (session["projectID"], self.commitHash))
                result = cursor.fetchone()
                if result:

                        fixes_commits = (str(result[DBConstants.Fixes])[2:-2]).split('", "')

                        print(fixes_commits)
                        for fix in fixes_commits:
                            fixes.append(fix)

                        # print(fix)
                        format_strings = ','.join(['%s'] * len(fixes))

                        sql = "select DISTINCT (JIRA_Id) from COMMITS_ISSUES where Commit_Hash in (%s);"
                        cursor.execute(sql % format_strings, (tuple(fixes)))
                        result = cursor.fetchone()

                        response = "The commit hash you mentioned introduced:\n"
                        while (result):
                            response += str(count) + "- " + str(result[DBConstants.JiraID]) + "\n"
                            result = cursor.fetchone()
                            count += 1
                            noResults = False
                        # print(response)

                if noResults:
                    response = "I am unable to find the bug (if any) produced by " + self.commitHash

                print("----------------RESULT------------------")
                print(response)
        finally:
            connection.close()



        return response