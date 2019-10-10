from src.main.DB.DBUtility import DBUtility
from src.main.DB.DBConstants import DBConstants
from src.main.Intents.IntentBase import IntentBase
import time
import datetime
from flask import session

class BugsCountsPerStatus(IntentBase):

    totalNumberOfBugOnStatus = 0

    def __init__(self, request):
        self.request = request

    def ProcessRespone(self):
        response = ""
        connection = DBUtility.getMYSQLConnection();
        try:
            with connection.cursor() as cursor:
                bugStatus = ['Open', 'Closed', 'Resolved', 'Awaiting Response', 'Awaiting Test Case', 'Reopened', 'In Progress']
                bugPriority = ['Minor', 'Major', 'Critical', 'Blocker', 'Trivial', 'None']
                sql = "SELECT Count(*) FROM OZBOT.Issues_Info where ProjectID=%s and IssueStatus = '{}' and priority ='{}'"
                response = "Here is the bug report:\n"
                for status in bugStatus:
                    for priority in bugPriority:
                        response = self.printResult(response, cursor ,sql, status, priority, session["projectID"])
                    response += "The total number of " + status + ": " + str(self.totalNumberOfBugOnStatus) + "\n"
                    self.totalNumberOfBugOnStatus = 0

                print("----------------RESULT------------------")
                print(response)

        finally:
                connection.close()

        return response


    def printResult(self, response, cursor, sql, status, priority, ProjectID):
        cursor.execute(sql.format(status,priority), (ProjectID))
        result = cursor.fetchone()
        self.totalNumberOfBugOnStatus += result["Count(*)"]
        response += priority + ": " + str(result["Count(*)"]) + "\n"
        return response

