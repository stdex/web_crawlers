from bs4 import BeautifulSoup
import urllib.request
from socket import timeout
import re
import sys
import os
from os.path import basename, splitext
from urllib.parse import urlparse
import codecs
import urllib
import json
import time
import datetime
from colorama import init
from colorama import Fore, Back, Style

import socket
import time
import string
import re
import urllib.request
import csv
import _thread

init()

class Channel:
    def __init__(self, channel):
        self.channel = channel
        self.SpamEnable = True
        self.ChannelConnect(self.channel)

        ##_thread.start_new_thread(self.SpamLoop,()) ## Threading work.

    def ChannelConnect(self, Channel):
        Server.ircsock.send(bytes("JOIN " + Channel + "\n", 'UTF-8'))
        ##self.SendMsg("Connected to "+Channel)

    def SendMsg(self, msg):
        Server.ircsock.send(bytes("PRIVMSG " + self.channel + " :" + msg + "\n", 'UTF-8'))
        print(msg)

    def BotHello(self):
        self.SendMsg("Hello!")

    def Slap(self, USER):
        self.SendMsg("Slapping " + USER)

    def LeaveChannel(self, Channel):
        Channel = Channel
        QuitCommand = bytes("PART " + Channel, 'UTF-8')
        try:
            Server.ircsock.send(QuitCommand)
            print(QuitCommand)
        except:
            print("didnt run")

    def SpamLoop(self):
        self.CTime = 1
        self.OldTime = 1
        self.DefaultWait = 5000  #millis
        while self.SpamEnable == True:
            self.CTime = time.time()
            if self.CTime >= (self.OldTime + self.DefaultWait):
                self.OldTime = time.time()
                self.SendMsg("Testing...")


###################################################
class Server:
    def __init__(self, Server, Port, botnick, botpass):

        self.Server = Server
        self.Port = Port
        self.botnick = botnick
        self.botpass = botpass

        self.Connect(Server, Port, botnick, botpass)

    def Connect(self, Server, Port, botnick, botpass):
        Pass = bytes("PASS " + botpass + '\n', 'UTF-8')
        Nick = bytes("NICK " + botnick + '\n', 'UTF-8')
        Ident = bytes("USER " + botnick + " " + botnick + " " + botnick + " :This bot is created by shiftywarloc\n",
                      'UTF-8')

        self.ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print("Connecting....")
        try:
            self.ircsock.connect_ex((Server, Port))

            self.ircsock.send(Pass)
            self.ircsock.send(Nick)
            self.ircsock.send(Ident)

        except socket.gaierror:
            print("Address invalid, Please check server details and try again")
            quit()

        print("Connected to " + self.Server)

    def ping(self):  #respond to server ping
        self.ircsock.send(bytes("PONG :ping\n", 'UTF-8'))
        print('ponged')


def REGEXCoder(Message, Expression, Convention):
    p = re.compile(Expression)  # Compile Regular Expression
    try:
        DecodedIrcMsg = Message.decode('utf-8')  #decode ircmsg to string
    except UnicodeDecodeError:
        return ""
        #DecodedIrcMsg = str(Message)

    Search = p.search(DecodedIrcMsg)  # search the string for RE

    if Convention == 1:  #search for \r\n
        if Search:
            MsgDecoded = DecodedIrcMsg[:Search.start()]
            Coded = bytes(MsgDecoded, 'utf-8')
            return Coded
    elif Convention == 2:
        if Search:
            MsgDecoded = Search.group()
            return MsgDecoded
    elif Convention == 3:  #Get Last word
        if Search:
            MsgDecoded = DecodedIrcMsg[Search.end():]
            return MsgDecoded
    else:
        print("Convention not found")


def getUptime(startTime):
    """
    Returns the number of seconds since the program started.
    """
    # do return startTime if you just want the process start time
    return time.time() - startTime


def workflow():

    startTime = time.time()

    ChannelsConnected = {}

    info_url = "https://api.twitch.tv/kraken/streams?game=Counter-Strike%3A%20Global%20Offensive&limit=25&offset=0"
    info_response = urllib.request.urlopen(info_url)
    info_result = json.loads(info_response.readall().decode('utf-8'))

    #print(info_result['streams'])
    ChannelList = []

    for key in info_result:
        value_s = info_result[key]
        if (key == 'streams'):
            dict_streams = info_result[key]
            for key_s in dict_streams:
                for key_f in key_s:
                    if (key_f == '_links'):
                        parsed = urlparse(key_s[key_f]['self'])
                        ChannelList.append("#" + parsed[2].split("/")[3])

    print(ChannelList)

    for i in ChannelList:
        Chan = i
        i = Channel(i)
        ChannelsConnected[Chan] = i
        print(Chan, ChannelsConnected[Chan])

    while 1:  #start loop

        ircmsg = Server.ircsock.recv(4096)
        #RE
        NewIrcMsg = REGEXCoder(ircmsg, "[\\r\\n]", 1)
        #CurrentChannelName = REGEXCoder(NewIrcMsg,'[#][a-z]*',2)
        #if type(CurrentChannelName) != str:
        #    CurrentChannelName = "#"
        #print(CurrentChannelName)

        #Server pings
        try:
            if (not (NewIrcMsg is None)):
                if NewIrcMsg.find(bytes("PING :", 'UTF-8')) != -1:
                    Server.ping()
        except:
            continue

        #Reply to hello
        #if NewIrcMsg.find(bytes(":Hello "+ Server.botnick,'UTF-8')) != -1: # If we can find our name call hello()
        #    ChanDirect = ChannelsConnected[CurrentChannelName]
        #    ChanDirect.BotHello()

        #Quit command
        #if NewIrcMsg.find(bytes(":shiftywarloc!shiftywarloc@shiftywarloc.tmi.twitch.tv PRIVMSG "+CurrentChannelName+" :!quit " + Server.botnick,'UTF-8')) != -1:
        #    ChanDirect = ChannelsConnected[CurrentChannelName]
        #    ChanDirect.SendMsg("Bot quitting standby")
        #    Server.ircsock.close()
        #    exit()

        #join another channel
        #if NewIrcMsg.find(bytes(":shiftywarloc!shiftywarloc@shiftywarloc.tmi.twitch.tv PRIVMSG "+CurrentChannelName+" :!join ",'UTF-8')) != -1:
        #    JChannel = REGEXCoder(NewIrcMsg,":!join\s",3)
        #    NewJChannel = Channel(JChannel)
        #    ChannelsConnected[JChannel] = NewJChannel

        '''Leave command not working on twitch.
        if NewIrcMsg.find(bytes(":shiftywarloc!shiftywarloc@shiftywarloc.tmi.twitch.tv PRIVMSG "+CurrentChannelName+" :!leave ",'UTF-8')) != -1:
            LChannel = REGEXCoder(NewIrcMsg,":!leave\s",3)
            ChanDirect = ChannelsConnected[CurrentChannelName]
            ChanDirect.LeaveChannel(LChannel)
            try:
                del ChannelsConnected[LChannel]
            except KeyError:
                ChanDirect = ChannelsConnected[CurrentChannelName]
                ChanDirect.SendMsg("Channel "+LChannel+" not found.")
        '''

        #Slap somone
        #if NewIrcMsg.find(bytes(":shiftywarloc!shiftywarloc@shiftywarloc.tmi.twitch.tv PRIVMSG "+CurrentChannelName+" :!slap ",'UTF-8')) != -1:
        #    USER = REGEXCoder(NewIrcMsg,":!slap\s",3)
        #    ChanDirect = ChannelsConnected[CurrentChannelName]
        #    ChanDirect.Slap(USER)


        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(NewIrcMsg))
        if (urls):
            if (not re.compile(
                    'steamcommunity.com|twitch.tv|twitter.com|streamtip.com|nightbot.tv|spotify.com|strawpoll.me|youtube.com|facebook.com|twitchalerts.com|g2a.com|apple.com|imgur.com|gyazo.com|soundcloud.com|speedtest.net|spoti.fi').search(
                    urls[0])):
                with open(outputTxt, "a") as f:
                    f.write(str(NewIrcMsg) + '\n')
                print(str(NewIrcMsg))
                #print(NewIrcMsg)
                #print("-----------")

        if (getUptime(startTime) > 600):
            break


outputTxt = 'links_new.txt'
#Variables
Serv = "irc.twitch.tv"
Port = 6667
Nick = "road_to_win"
Password = "oauth:8zzshsizp1584gdioe9ua7efbt8nn1"
# Connect to Server
Server = Server(Serv, Port, Nick, Password)
while 1:
    workflow()