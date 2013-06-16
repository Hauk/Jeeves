import time
import datetime
import re

#Time regex
time_regex = '^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$'

class TimeKeeper():

    def __init__(self, name):
        self.name = name

    def validate_date(self, date):

        """ (str) -> Bool

        This function validates a date in the dd/mm/yyyy format.

        """

        #Try and make a date from the string.
            #If it fails, it is not a valid date.
        try:
            valid_date = time.strptime(date, '%d/%m/%Y')
        except ValueError:
            return False

        return True

    def validate_time(self, time):

        """ (str) -> Bool

        This function validates a time in the hh:mm format.

        """

        if(re.match(time_regex, time, re.M|re.I)):
            return True

        return False

