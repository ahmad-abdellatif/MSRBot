from src.main.OZAPIConstants import EntityConstants
from src.main.OZAPIConstants import IntentConstants
from src.main.Utility import Utility
from src.main.DB.DBUtility import DBUtility
from src.main.DB.DBConstants import DBConstants
from src.main.Intents.IntentBase import IntentBase
import time
import datetime
from flask import session

class GetNumberOfCommitByDate(IntentBase):
    def __init__(self, request):
        self.request = request
        self.initParameters()

    def initParameters(self):
        self.date = Utility.getParm(self.request, EntityConstants.DATE)
        print("Date" + self.date)

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

                print(self.date)
                print(fromTime)
                print(toTime)
                fromTime = time.mktime(datetime.datetime.strptime(fromTime, "%Y-%m-%d %H:%M:%S").timetuple())
                toTime = time.mktime(datetime.datetime.strptime(toTime, "%Y-%m-%d %H:%M:%S").timetuple())
                sql = "SELECT COUNT(*) FROM OZBOT.GitInfo WHERE ProjectID=%s and (aDate BETWEEN %s AND %s)"
                cursor.execute(sql, (session["projectID"],fromTime, toTime))

                result = cursor.fetchone()
                result = result['COUNT(*)']
                response = "The number of commits happened during the selected period is " + str(result)
                if str(result) == "0":
                    # sql = "SELECT aDate FROM OZBOT.GitInfo where ProjectID=%s and (aDate BETWEEN %s AND %s) ORDER BY aDate DESC LIMIT 1"
                    # cursor.execute(sql, (session["projectID"], fromTime, toTime))
                    # result = cursor.fetchone()
                    response = "There are no commits happened in the specified date" #+ str(datetime.datetime.fromtimestamp(int(result[DBConstants.aDate])).strftime('%Y-%m-%d'))

                print("----------------RESULT------------------")
                print(response)
        finally:
            connection.close()

        return response
