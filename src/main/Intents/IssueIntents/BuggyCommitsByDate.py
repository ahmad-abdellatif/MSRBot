from src.main.OZAPIConstants import EntityConstants, IntentConstants
from src.main.Utility import Utility
from src.main.DB.DBUtility import DBUtility
from src.main.DB.DBConstants import DBConstants
from src.main.Intents.IntentBase import IntentBase
import time
import datetime
from flask import session

class BuggyCommitsByDate(IntentBase):
    def __init__(self, intent, request):
        self.request = request
        self.initParameters()
        self.intent = intent

    def initParameters(self):
        self.date = Utility.getParm(self.request, EntityConstants.DATE)
        print("Date" + self.date)

    def ProcessRespone(self):
        response = ""
        EmptyResults = True
        connection = DBUtility.getMYSQLConnection();
        try:
            with connection.cursor() as cursor:
                datePeriod = self.date.split('/')

                if(len(datePeriod) > 1):
                    fromTime = str(datePeriod[0]) + " 00:00:00"
                    toTime = str(datePeriod[1]) + " 23:59:59"
                else:
                    fromTime = str(self.date) + " 00:00:00"
                    toTime = str(self.date) + " 23:59:59"

                fromTime = time.mktime(datetime.datetime.strptime(fromTime , "%Y-%m-%d %H:%M:%S").timetuple())
                toTime = time.mktime(datetime.datetime.strptime(toTime , "%Y-%m-%d %H:%M:%S").timetuple())


                if self.intent == IntentConstants.BUGGY_COMMITS_BY_DATE:
                    sql = "SELECT aName, aDate, Body FROM OZBOT.GitInfo WHERE ProjectID=%s and (aDate between %s and %s) and contains_bug = TRUE ORDER BY aDate DESC"
                else:
                    sql = "SELECT aName, aDate, Body FROM OZBOT.GitInfo WHERE ProjectID=%s and (aDate between %s and %s) and commits.fix = TRUE ORDER BY aDate DESC"

                cursor.execute(sql, (session["projectID"], fromTime, toTime))

                result = cursor.fetchone()
                while(result):
                    response += "Name: " + str(result[DBConstants.aName]) + "\n"
                    response += "Date: " + str(datetime.datetime.fromtimestamp(int(result[DBConstants.aDate])).strftime('%Y-%m-%d %H:%M:%S')) + "\n"
                    response += "Body: " + str(result[DBConstants.Body]) + "\n"
                    response += "--------------------------------------------------- \n"
                    result = cursor.fetchone()
                    EmptyResults = False

                if(EmptyResults):
                    response= "There is no buggy commits mentioned in the specified period."

                print("----------------RESULT------------------")
                print(response)
        except Exception as ex:
            print (ex)
            response = "Sorry, I am unable to process your query. I have notified the developers about this error. Please try to specify the date in other format :)"
        finally:
                connection.close()


        return response
