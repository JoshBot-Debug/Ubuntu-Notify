import os
from re import search
from ubuntu_notify.interface.NotificationInterface import NotificationInterface

class Notification(NotificationInterface):
    '''
        This class is used to send notifications to Ubuntu using subprocess.Popen(["notify-send",Message])
    '''

    def __init__(self, Message: dict, AutoFire = True):
        if AutoFire:
            self.send(Message)


    def send(self, Message: dict) -> bool:
        icon = os.path.realpath(__file__).replace("Notification.py","")+"gicon.png"
        eFrom = search("(.*) <",Message['from']).group(1)

        try:
            os.system(f"notify-send --urgency=critical --icon='{icon}' '{eFrom}' '{Message['subject']}'")
        except:
            return False

        return True