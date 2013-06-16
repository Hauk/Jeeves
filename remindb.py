import sys
import mysql.connector
from mysql.connector import errorcode

class Database():

    def __init__(self, name, user, password, host, database):
        
        '''(str, str, str, str, str, str, str) -> NoneType

        The __init__ function for the database class instantiates a Database
        object and creates a cursor for the object to talk to the database with.

        '''

        self.name = name
        self.user = user
        self.password = password
        self.host = host
        self.database = database

        try:
            self.db_connector = mysql.connector.connect(user=self.user, password=self.password, database=self.database, host=self.host)
           
            self.db_cursor = self.db_connector.cursor()
        
        except mysql.connector.Error as err:
            
            #Exception Handling.
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Error: Something is wrong with your user name or password.")
            
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exists")
            
            else:
                print(err)
            
        
    def insert_reminder(self, user, date, time, reminder_msg):
	
        print("in insert_reminder")

        if(user != 'mak'):

            print("howiya hey")

            try:
                remind_query = """INSERT INTO reminders (user, date, time, reminder_msg) VALUES (%s, %s, %s, %s)"""

                reminder_data = (user, date, time, reminder_msg)

                print(reminder_data)

                try:
                    self.db_cursor.execute(remind_query, reminder_data)
                except:
                    print("failed to execute query...")
                
                print("committing...")
                self.db_connector.commit()
                print("committed...")
            except mysql.connector.Error as err:
                print(err)
 
    def get_daily_reminders(self, user, todays_date):
        '''(self, str, str) -> list of times and reminder messages.

	    Function returns a list of times and reminders based on the date parameter.
    	'''

        #Setup the query to get all apointments for todays date.
        dailies_query = "SELECT time, reminder_msg FROM reminders WHERE user=%s AND date=%s"

        try:
            self.db_cursor.execute(dailies_query, (user, todays_date))
        except mysql.connector.Error as err:
            print(err)

        #Get the messages into a list.
        return_msgs = []

        #Now query the cursor for the data.
        for entry in self.db_cursor:
            return_msgs.append((entry[0] + ': ' + entry[1]).rstrip())

        return return_msgs

    def get_current_reminders_count(self, curr_date, curr_time):
        '''(self, str, str) -> bool

        Function returns a count of reminders due at the minute(curr_time) given.
        '''

        reminders_count = "SELECT count(*) FROM reminders WHERE date=%s AND time=%s"

        try:
            self.db_cursor.execute(reminders_count, (curr_date, curr_time))
        except mysql.connector.Error as err:
            print(err)

        #Count the number of reminders due. If > 1, reminder is due.
        result_count = self.db_cursor.fetchone()[0]

        print(result_count)

        if(result_count >= 1):
            return True

        return False
