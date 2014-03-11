__author__ = 'Kristo Koert'

from src.database.datatypes.notification import Notification


class Reminder(Notification):

    def __init__(self, message, time):
        """
            :param message: The message displayed on reminder activation.
            :type message: str
            :param time: Time when reminder should activate.
            :type time: Timestamp
        """
        Notification.__init__(self, message, time, "Reminder")

    def get_database_info(self):
        return self.get_notification_info()