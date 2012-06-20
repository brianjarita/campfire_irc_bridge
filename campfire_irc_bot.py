import pyfire
import types
from settings import *

# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

# system imports
import time, sys, datetime
import requests

global msg_func
msg_func = None

global room

class MessageLogger:
    """
    An independent logger class (because separation of application
    and protocol logic is a good thing).
    """
    def __init__(self):
        a=1

    def log(self, message):
        """Write a message to the file."""
        print message

    def close(self):
        a=1


class LogBot(irc.IRCClient):
    """A logging IRC bot."""

    nickname = "bacit"

    def connectionMade(self):
        global msg_func
        msg_func = self.msg
        irc.IRCClient.connectionMade(self)
        self.logger = MessageLogger()
        self.logger.log("[connected at %s]" %
                        time.asctime(time.localtime(time.time())))

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        self.logger.log("[disconnected at %s]" %
                        time.asctime(time.localtime(time.time())))
        self.logger.close()


    # callbacks for events

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        self.join(self.factory.channel1)
        self.join(self.factory.channel2)

    def joined(self, channel):
        """This will get called when the bot joins the channel."""
        self.logger.log("[I have joined %s]" % channel)

    def privmsg(self, user, channel, msg):
        global room
        if channel == self.nickname:
            room.speak(msg)

    def noticed(self, user, channel, msg):
        a=1

    def action(self, user, channel, msg):
        a=1

    def userJoined(self, user, channel):
        a=1

    def userLeft(self, user, channel):
        a=1

    def userQuit(self, user, channel):
        a=1

    def topicUpdated(self, user, channel, newTopic):
        a=1

    def irc_NICK(self, prefix, params):
        a=1

    def alterCollidedNick(self, nickname):
        return nickname



class LogBotFactory(protocol.ClientFactory):
    """A factory for LogBots.

    A new protocol instance will be created each time we connect to the server.
    """

    def __init__(self, channel1, channel2):
        self.channel1 = channel1
        self.channel2 = channel2

    def buildProtocol(self, addr):
        p = LogBot()
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()


def incoming(message):
    global msg_func
    irc_channel = "#messageschannel"
    header_prefix = "Campfire CHATROOM"
    if not msg_func is None:
        user = ""
        if message.user:
            if type(message.user.name) == types.UnicodeType:
                user = message.user.name.encode('ascii', 'ignore')
            elif type(message.user.name) == types.StringType:
                user = str(message.user.name)

        msg_body = ""
        if message.body:
            if type(message.body) == types.UnicodeType:
                msg_body = message.body.encode('ascii', 'ignore')
            elif type(message.body) == types.StringType:
                msg_body = message.body

        if message.is_joining():
            msg_func(irc_channel, "-- " + header_prefix + " --  [%s] entered the room"
                % user)
        elif message.is_leaving():
            msg_func(irc_channel, "-- " + header_prefix + " --  [%s] left the room"
                % user)
        elif message.is_tweet():
            if msg_body:
                msg_func(irc_channel, "-- " + header_prefix + \
                " --  [%s] tweeted '%s'" % (user, msg_body))
        elif message.is_text():
            msg = "-- " + header_prefix + " --  [%s] %s" % (user, msg_body)
            msg_func(irc_channel, msg)
        elif message.is_upload():
            upload_name = message.upload["name"]
            upload_url = message.upload["url"]

            if type(upload_name) == types.UnicodeType:
                upload_name = upload_name.encode('ascii', 'ignore')
            elif type(upload_name) == types.StringType:
                upload_name = str(upload_name)

            if type(upload_url) == types.UnicodeType:
                upload_url = upload_url.encode('ascii', 'ignore')
            elif type(upload_url) == types.StringType:
                upload_url = str(upload_url)

            msg_func(irc_channel, "-- " + header_prefix + \
            " --  [%s] uploaded file %s: %s" % (user, upload_name, upload_url))
        elif message.is_topic_change():
            msg_func(irc_channel, "-- " + header_prefix + \
            " -- [%s] changed topic to '%s'" % (user, msg_body))

def error(e):
    print("Stream STOPPED due to ERROR: %s" % e)
    print("Press ENTER to continue")

if __name__ == '__main__':
    # initialize logging
    log.startLogging(sys.stdout)

    campfire = pyfire.Campfire( CAMPFIRE_SUBDOMAIN, CAMPFIRE_EMAIL,
        CAMPFIRE_PASSWORD, ssl=True)
    global room
    room = campfire.get_room_by_name("CHATROOM")
    room.join()
    stream = room.get_stream(error_callback=error)
    stream.attach(incoming).start()
    # create factory protocol and application
    f = LogBotFactory('triggerchannel','messageschannel')

    # connect factory to this host and port
    reactor.connectTCP("127.0.0.1", 6667, f)

    reactor.run()


