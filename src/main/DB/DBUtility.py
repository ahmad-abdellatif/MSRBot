import pymysql.cursors
import pymysql

class DBUtility:
    HOST_NAME = ""  # Your host.
    USER_NAME = ""  # Your DB user name.
    PASSWORD = ""   # Your DB user password.
    DB = ""         # Your DB name.
    CHARSET = "latin1"

    
   
    @staticmethod
    def getMYSQLConnection():
        
        #Init the connection
        
        connection = pymysql.connect(host= DBUtility.HOST_NAME,
                             user= DBUtility.USER_NAME,
                             password= DBUtility.PASSWORD,
                             db= DBUtility.DB,
                             charset= DBUtility.CHARSET,
                             cursorclass=pymysql.cursors.DictCursor)
        
        
        #connection = pymysql.connect(constants.HOST_NAME, constants.USER_NAME, constants.PASSWORD, constants.DB, constants.CHARSET, cursorclass=pymysql.cursors.DictCursor)
        
        return connection