from src.main.OZAPIConstants import EntityConstants
from src.main.OZAPIConstants import IntentConstants
from src.main.Utility import Utility
from src.main.DB.DBUtility import DBUtility
from src.main.DB.DBConstants import DBConstants
from src.main.Intents.IntentBase import IntentBase
from flask import session
import time
import datetime

class GetCommentBodyByDateAndName(IntentBase):
    def __init__(self, request):
        self.request = request
        self.initParameters()

    def initParameters(self):
        self.date = Utility.getParm(self.request, EntityConstants.DATE)
        self.givenName = Utility.getParm(self.request, EntityConstants.DEVELOPERS_NAME_ENTITY)

    def ProcessRespone(self):
        response = ""
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


                sql = "SELECT Body FROM OZBOT.GitInfo WHERE ProjectID = %s and aName = %s and (aDate between %s and %s)"

                cursor.execute(sql, (session["projectID"], self.givenName, fromTime, toTime))
                result = cursor.fetchone()
                while(result):
                    response += result[DBConstants.Body] + "\n"
                    result = cursor.fetchone()
                print("----------------RESULT------------------")
                print(response)
        finally:
                connection.close()

        return response