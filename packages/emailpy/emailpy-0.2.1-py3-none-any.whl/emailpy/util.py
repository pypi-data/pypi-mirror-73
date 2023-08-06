from base64 import *
from .send import sendmail, sendzoominvite, forward, sendmailobj, \
     genzoominvite
from .read import readmail, getfoldernames, createfolder, deletefolder

class EmailSender:
    def __init__(self, email, pwd):
        self.email = email
        self.pwd = b85encode(pwd.encode())

    def send(self, toemails, subject = '', body = '', html = None,
             attachments = None, nofileattach = None):
        return sendmail(self.email, b85decode(self.pwd).decode(),
                        toemails, subject, body, html,
                        attachments, nofileattach)

    def forward(self, mailobj, toemails, **kwargs):
        return forward(self.email, b85decode(self.pwd).decode(),
                       mailobj, toemails, **kwargs)

    def sendmailobj(self, mailobj, toemails, **kwargs):
        return sendmailobj(self.email, b85decode(self.pwd).decode(),
                           mailobj, toemails, **kwargs)

class EmailReader:
    def __init__(self, email, pwd):
        self.email = email
        self.pwd = b85encode(pwd.encode())

    def read(self, foldername = 'INBOX'):
        return readmail(self.email, b85decode(self.pwd).decode(),
                        foldername)

    def getfoldernames(self):
        return getfoldernames(self.email, b85decode(self.pwd).decode())

    def createfolder(self, foldername):
        return createfolder(self.email, b85decode(self.pwd).decode(),
                            foldername)

    def deletefolder(self, foldername):
        return deletefolder(self.email, b85decode(self.pwd).decode(),
                            foldername)

class EmailManager:
    def __init__(self, email, pwd):
        self.sender = EmailSender(email, pwd)
        self.reader = EmailReader(email, pwd)
        self.email = email

    def send(self, toemails, subject = '', body = '', html = None,
             attachments = None, nofileattach = None):
        return self.sender.send(toemails, subject, body, html,
                        attachments, nofileattach)

    def read(self, foldername = 'INBOX'):
        return self.reader.read(foldername)

    def sendzoominvite(self, invitees, meetingurl, meetingid = None,
                       meetingpwd = None):
        return sendzoominvite(self.sender.email, b85decode(self.sender.pwd),
                              invitees, meetingurl, meetingid, meetingpwd)

    def getfoldernames(self):
        return self.reader.getfoldernames()

    def forward(self, mailobj, toemails, **kwargs):
        return self.sender.forward(mailobj, toemails, **kwargs)

    def sendmailobj(self, mailobj, toemails, **kwargs):
        return self.sender.sendmailobj(mailobj, toemails, **kwargs)

    def createfolder(self, foldername):
        return self.reader.createfolder(foldername)

    def deletefolder(self, foldername):
        return self.reader.deletefolder(foldername)
