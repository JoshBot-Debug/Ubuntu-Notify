import subprocess
from threading import Timer
from sys import platform

from ubuntu_notify.src.Notification import Notification
from ubuntu_notify.src.gmailAPI import GmailApi


class UbuntuNotify:
    '''
        This package is ment to help impliment custom notifications in Linux.
        The package has been tested in Ubuntu 20.04
    '''

    __NotificationSent = []

    def __init__(self):
        """ Make sure the platform is Linux and start the main thread """

        if platform != "linux":
            raise Exception("This package is ment for Linux!")
        
        self.gmail = GmailApi()
        self.startProcess()


    def startProcess(self):
        """ Start the background process that receives the email data """

        self.thread = Timer(60,self.startProcess)
        self.thread.start()
        
        newEmail = self.gmail.getLatestEmail()
        
        # Make sure the email dict is not empty
        if newEmail != {}:
            # Make sure the email notification was only sent once
            if newEmail['subject'] not in self.__NotificationSent:
                self.__NotificationSent.append(newEmail['subject'])
                Notification(newEmail)

        self.thread.join()