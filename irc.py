import socket
import string

class IRC:

    def __init__(self, name, net, port, nick, channel, owner, ident, readbuffer):
        self.name = name
        self.net = net
        self.port = port
        self.nick = nick
        self.channel = channel
        self.owner = owner
        self.ident = owner
        self.readbuffer = readbuffer

        #Create a socket to send messages to IRC.
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        

    def connect_to_channel(self):

        #Connect to IRC!
        self.s.connect((self.net, self.port))

        self.s.send(('USER '+self.ident+' '+self.net+' bla :'+self.owner+'\r\n').encode())
        self.s.send(('NICK '+self.nick+'\r\n').encode())
        self.s.send(('JOIN '+self.channel+'\r\n').encode())
        self.s.send(('PRIVMSG ' + self.owner + ' :Good evening sir.\r\n').encode())

        print((self.s.recv(4096)).decode())

    def get_irc_message(self):

        '''() -> list of str

        This function reads from the sockets buffer and creates a list of the
        words in the sentence from IRC.
        '''

        #Read everything from the buffer.
        sentence = ' '
        self.readbuffer = self.readbuffer+self.s.recv(2048).decode("UTF-8")
        temp = str.split(self.readbuffer, "\n")
        self.readbuffer = temp.pop()

        #Strip all the words form the line
        for line in temp:
            line=str.rstrip(line)
            line=str.split(line)

        #Handle the pings.
        if(line[0] == 'PING'):
            self.s.send(('PONG ' + line[1]+'\r\n').encode())

        #Handle forming a PM.
        if(line[1] == 'PRIVMSG'):
            #Required for full sentence.
            for n in range(4, len(line)):
                sentence += line[n]+' '

        return line

    def send_message_to_channel(self, message):

        '''(self, str) -> NoneType
        
        This function sends a message to the channel based on data returned from
        the database.
        '''

        priv = 'PRIVMSG ' + self.channel + ' :' + message + ' \r\n'

        self.s.send(priv.encode())

    def private_message_user(self, user, reminder_details):
        '''(self, str, str) -> NoneType
	
	Function sends a private message to the user.

	'''

        priv_msg = ' PRIVMSG ' + user + ' :' + reminder_details + '\r\n'

        self.s.send(priv_msg.encode())

    def get_irc_user_name(self, unsplit_nick):
        
        '''(self, str) -> str

        Function splits the IRC users nick from: "username!redbrick.dcu.ie"
        '''

        split_nick = unsplit_nick.split('!')
        nick_element = split_nick[0]
        irc_user_name = nick_element[1:]
        return irc_user_name


if __name__ == "__main__":
    
    irc_handler = IRC("IRC_Handler", 'irc.redbrick.dcu.ie', 6667, 'Jeeves', '#bots1', 'hauk', 'hauK', '')

    irc_handler.connect_to_channel()

    while(True):

        line = irc_handler.get_irc_message()
        #print line

        if(line[3] == ":!lol"):
            irc_handler.send_message_to_channel("hullo good sire. *bows*")

        #If any of of the triggers are in a list of jobs.
        #If job in list of jobs:
            #Set JOBS_AVAILABLE TO TRUE.

        #Wake up "database inserter" thread.
        #It should check jobs are avaiable for processing.
        #If so, process them, else sleep.
        
        #Check it has been one minute since last call(time is: 06:23:00 etc)
        #Wake up Jeeves(the IRC message sender).
        #Check all the times in the database against current time.
        #Form notification messages for user reminders or user requesting their schedule.
        #Broadcast to IRC.
        #Sleep for another minute.  
