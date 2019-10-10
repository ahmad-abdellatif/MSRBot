from src.main.DB.DBUtility import DBUtility
from src.main.DB.DBConstants import DBConstants
from src.main.Intents.IntentBase import IntentBase
from flask import session


class MostDeveloperHasOpenedClosedBugs(IntentBase):

    def __init__(self, request, status):
        self.request = request
        self.status = "Open, In progress" #status
        self.statusArray = []
        self.statusArray.append("Open")
        self.statusArray.append("In progress")
        self.statusArray.append("Reopened")
        self.statusArray.append("Awaiting Response")
        self.statusArray.append("Awaiting Test Response")

    def ProcessRespone(self):
        response = ""
        counter = 1;
        connection = DBUtility.getMYSQLConnection();
        try:
            with connection.cursor() as cursor:

                #sql = "SELECT Assignee, count(Assignee)  FROM Issues_Info where IssueStatus = '{}' GROUP BY Assignee ORDER BY COUNT(*) DESC LIMIT 10;"
                sql = "SELECT Assignee, count(Assignee) FROM Issues_Info where ProjectID=%s and IssueStatus IN ('Open','In progress','Reopened','Awaiting Response','Awaiting Test Response') GROUP BY Assignee ORDER BY COUNT(*) DESC LIMIT 11;"
                response = ("The most developers who had {} bugs are:\n").format(self.status)
                # format_strings = ','.join(['%s'] * (len(session["projectID"])+1))
                # cursor.execute(sql % format_strings , (session["projectID"], tuple(self.statusArray)))

                cursor.execute(sql, (session["projectID"]))


                #cursor.execute(sql.format(self.status), ())
                result = cursor.fetchone()
                while(result):
                    response += str(counter) + "- " + str(result[DBConstants.Assignee]) + " " + str(result["count(Assignee)"]) + "\n"
                    result = cursor.fetchone()
                    counter += 1
                print("----------------RESULT------------------")
                print(response)

        finally:
                connection.close()

        return response