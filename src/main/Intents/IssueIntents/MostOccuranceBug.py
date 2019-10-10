from src.main.DB.DBUtility import DBUtility
from src.main.DB.DBConstants import DBConstants
from src.main.Intents.IntentBase import IntentBase
import time
import datetime
from flask import session

class MostOccuranceBug(IntentBase):

    def __init__(self, request):
        self.request = request

    def ProcessRespone(self):
        response = ""
        connection = DBUtility.getMYSQLConnection();
        try:
            with connection.cursor() as cursor:

                sql = "SELECT * FROM OZBOT.Issues_Info where ProjectID=%s and IssueStatus = '{}' ORDER BY WatcherCount DESC limit 1"
                response = "The most popular open bug has the following information:\n"
                response = self.printResult(response, cursor ,sql, 'Open', session["projectID"])
                response += "\n **************************************************** \n"
                response += "The most popular Close bug has the following information:\n"
                response = self.printResult(response, cursor, sql, 'Closed', session["projectID"])
                print("----------------RESULT------------------")
                print(response)

        finally:
                connection.close()

        return response


    def printResult(self, response, cursor, sql, status, projectID):
        cursor.execute(sql.format(status), (projectID))
        result = cursor.fetchone()
        while (result):
            response += "Title: " + str(result[DBConstants.Title]) + "\n"
            response += "Issue Key: " + str(result[DBConstants.Issue_Key]) + "\n"
            response += "Type: " + str(result[DBConstants.Issue_Type]) + "\n"
            response += "Created on: " + str(datetime.datetime.fromtimestamp(int(result[DBConstants.Created_Date])).strftime('%d/%m/%Y %H:%M')) + "\n"
            if str(result[DBConstants.Closed_Date]) != '':
                response += "Closed on: " + str(datetime.datetime.fromtimestamp(int(result[DBConstants.Closed_Date])).strftime('%d/%m/%Y %H:%M')) + "\n"
            response += "Assignee: " + str(result[DBConstants.Assignee]) + "\n"
            response += "Reporter: " + str(result[DBConstants.Reporter]) + "\n"
            response += "Number of watchers: " + str(result[DBConstants.WatcherCount]) + "\n"
            response += "Description: " + str(result[DBConstants.Description]) + "\n"
            result = cursor.fetchone()
            print("---------------> \n")
        return response