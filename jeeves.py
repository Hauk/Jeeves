from threading import *
import threading
import alfred
import datetime
from timekeeper import TimeKeeper 
from remindb import Database
import dbconfig
from irc import IRC

s1 = Semaphore(value=1)

#Global variable for both threads to signal to one another that a reminder is
#due to be sent to the user in the channel.
REMINDERS_DUE = False

class Jeeves (threading.Thread):

    def __init__(self, threadID, name):
        threading.Thread.__init__(self)

        self.threadID = threadID
        self.name = name

    def run(self):

        print("lol")
        print("omg i'm running")

    #Initial four functions

    #1. A function to send appointments for that day on demand.
    def send_dailies(self, line, irc_handler, db_handler):
        """ 
        
        This function sends a list of all the current days appointments to the user.

        """

        #Get the irc user.
        user = irc_handler.get_irc_user_name(line[0])

        today = datetime.datetime.now()

        #Get the format into dd/MM/YYYY
        todays_date = today.strftime("%d/%m/%Y")

        #Set empty list to receive reminder messages
        message_list = []

        try:
            
            #Get all messages from database.
            message_list = db_handler.get_daily_reminders(user, todays_date)
        
        except Exception as e:
            print("Error getting data from table.")
            print(e)

        if(len(message_list) == 0):
            irc_handler.private_message_user(user, "You have no appointments for today Sir.")
        else:
            irc_handler.private_message_user(user, "Your appointments for today Sir:")

            for message in message_list:
                irc_handler.private_message_user(user, message)

    def send_weeklies():
        """

        Function sends a list of all the current weeks appointments to the user.

        """

        user = irc_handler.get_irc_user_name(line[0])

        today = datetime.datetime.now()

    #2. A function to add a reminder from a user to the database.
    def get_reminder_from_irc(self, line, irc_handler, db_handler, time_keeper):
        """(list of str, IRC, TimeKeeper) -> NoneType
        
        Function listens for a trigger from IRC to add a reminder to Jeeves
        appointments. Jeeves takes the message and puts it in a queue to be
        written to the database.

        """

        try:
            
            #Set a boolean to track message is well formed.
            message_ok = True

            #Check there's a date, time, and at least a one word reminder.
            if(len(line) > 5):

                #Get the date and time into their own variables.
                reminder_date = line[4]
                reminder_time = line[5]

                #Validate the date.
                if(time_keeper.validate_date(reminder_date) == False):
                    irc_handler.send_message_to_channel("Invalid date. Format is: DD/MM/YYYY.")
                    message_ok = False

                #Validate the time.
                if(time_keeper.validate_time(reminder_time) == False):
                    irc_handler.send_message_to_channel("Invalid time. Format is: HH:MM")
                    message_ok = False

                if(message_ok == True):

                    reminder_msg = ''

                    #Construct the reminder message from the rest of the list.
                    for i in range(6, len(line)):
                        reminder_msg += line[i] + ' '

                    try:

                        #If all messages are well formed, we can insert the reminder into the database.
                        user = irc_handler.get_irc_user_name(line[0])

                        #Insert reminder into the reminders table.
                        db_handler.insert_reminder(irc_handler.get_irc_user_name(line[0]), reminder_date, reminder_time, reminder_msg)
                        
                        #Notify user in channel of successful insert.
                        irc_handler.send_message_to_channel(user + ": Certainly sir. I have added it to your schedule and will remind you then.")
                    except Error as e:
                        print("Something happened on insert.")
                        print(e)


        except Error as e:
            irc_handler.send_message_to_channel("Something went wrong adding the reminder.")
            print(e)

    def check_notifications(self, db_handler, curr_date, curr_time):
        '''(self, Database, str, str) -> bool

        Function takes in the database handler, current date and current time and uses the db_handlers get_current_reminders_count to check for any notifications.
        '''

        return db_handler.get_current_reminders_count(curr_date, curr_time)

    #3. A function to notify a user of a reminder they have.
    def notify_users_of_reminders():
        """

        Function is queried on the minute by a thread.
        Appointment times are taken from the database and added to the queue of
        that times reminders and a message sent to the user on IRC.

        """

        #Get current date into dd/mm/YYYY format.
        now = datetime.datetime.now()
        todays_date = now.strftime("%d/%m/%Y")

        #Get current time and convert it to hh:mm.
        todays_time = now.strftime("%H:%M")
        print(todays_time)

        #Select all notifications from the database based on that date and time.
        notifications_query = """SELECT user, reminder_msg FROM reminders WHERE (date=%s AND time=%s);"""

        #Setup our parameters
        notifications_params = (todays_date, todays_time)

        #TODO: Add in cursor.
        #TODO: Run query and get reminder data.
        #TODO: Loop over returned rows, and notify users with send_message_to_irc()

    #4. A function to text someone using o2sms.
    def send_text_to_user(user):
        """

        Function takes an IRC username, hashes it and compares it against a
        hashed username in the database. It means numbers are in text, but
        private(I think).

        """

def main():

    #Create an instance of Jeeves and the TimeKeeper classes.
    jeeves = Jeeves(1, "Jeeves")

    time_keeper = TimeKeeper("TimeKeeper1")

    jeeves.start()

    print(jeeves.name)
    print(time_keeper.name)

   # jeeves.join()

    irc_handler = IRC("IRC_Handler", 'localhost', 6667, 'Jeeves', '#bots1', 'hauk', 'hauK', '')

    irc_handler.connect_to_channel()

    db_handler = Database("DB_Handler", dbconfig.user, dbconfig.dbpass, "localhost", "reminders")

    while(True):
        line = irc_handler.get_irc_message()

        print(line)

        if(line[3] == ":!lol"):
            irc_handler.send_message_to_channel("hullo good sire. *bows*")
        
        if(line[3] == ":!reminder"):
            jeeves.get_reminder_from_irc(line, irc_handler, db_handler, time_keeper)

        if(line[3] == ":!dailies"):
            jeeves.send_dailies(line, irc_handler, db_handler)
            print(jeeves.check_notifications(db_handler, "23/05/2013", "16:00"))
            print(jeeves.check_notifications(db_handler, "23/05/2013", "13:00"))

if __name__ == "__main__":
    main()

    #Need a thread to monitor IRC for users login and get and send all that days appointments.

    #Need a thread to watch irc channel and add appointments to the queue.
    #Need a thread to update the DB from the queue (don't forget a queue).

    #Need a thread to update apointments list with current(due) appointments from the DB.
    #Need a thread to notify all users based on appointments in list..
        #Wake up.
        #If jobs in appointments list.
            #Notify users.
        #If not, do go back asleep.
    # Thread to delete all processed jobs.

    # Thread to check for text job.

