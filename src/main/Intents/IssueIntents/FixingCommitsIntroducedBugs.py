from src.main.DB.DBUtility import DBUtility
from src.main.Intents.IntentBase import IntentBase
from src.main.Utility import Utility
from src.main.OZAPIConstants import EntityConstants
import time
import datetime
from flask import session

class FixingCommitsIntroducedBugs(IntentBase):
    def __init__(self, request):
        self.request = request
        self.initParameters()

    def initParameters(self):
        self.date = Utility.getParm(self.request, EntityConstants.DATE)

    def ProcessRespone(self):
        connection = DBUtility.getMYSQLConnection();
        try:
            with connection.cursor() as cursor:
                datePeriod = self.date.split('/')

                if (len(datePeriod) > 1):
                    fromTime = str(datePeriod[0]) + " 00:00:00"
                    toTime = str(datePeriod[1]) + " 23:59:59"
                else:
                    fromTime = str(self.date) + " 00:00:00"
                    toTime = str(self.date) + " 23:59:59"

                fromTime = time.mktime(datetime.datetime.strptime(fromTime, "%Y-%m-%d %H:%M:%S").timetuple())
                toTime = time.mktime(datetime.datetime.strptime(toTime, "%Y-%m-%d %H:%M:%S").timetuple())

                sql = "select (100 * (select count(*) from Gitinfo where ProjectID=%s and fix = TRUE and contains_bug = TRUE and (aDate between %s and %s)) / (select count(*)  from Gitinfo where ProjectID=%s and fix = TRUE and (aDate between %s and %s))) as percentage"

                cursor.execute(sql, (session["projectID"], fromTime, toTime, session["projectID"], fromTime, toTime))

                result = cursor.fetchone()
                result = result['percentage']

                if result is None:
                    response = "Sorry, but there are no fixing commits in the specified time period"

                elif str(result) == "0":
                    response = "Woow! All of the fixing commits are perfect, they did not introduce any bug until now :)"

                else:
                    response = "The percentage of fixing commits that are introducing bugs is %" + str(result)


                print("----------------RESULT------------------")
                print(response)
        finally:
            connection.close()

        return response

