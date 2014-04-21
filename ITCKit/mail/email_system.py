__author__ = 'Kristo Koert'

import imaplib
import threading
import email
import time
from ITCKit.mail.credential_security import get_password
from ITCKit.settings.settings import get_email_settings
from ITCKit.settings import settings
from ITCKit.db import dbc
from ITCKit.core.datatypes import EMail


class MailHandler(threading.Thread):

    connection = None

    def __init__(self):
        threading.Thread.__init__(self)
        self.mail_settings = get_email_settings()

    def run(self):
        while True:
            if self.mail_settings["activated"]:
                self.get_unread_email()
            else:
                time.sleep(1)

    def connect_to_account(self):
        try:
            mail_service = imaplib.IMAP4_SSL('outlook.office365.com')
            psw = get_password()
            mail_service.login(self.mail_settings["username"], psw)
            return mail_service
        except:
            return None

    def get_unread_email(self):
        mail_service = self.connection
        if mail_service is None:
            self.connection = self.connect_to_account()
            time.sleep(10)
        else:
            inbox = mail_service.select("inbox")
            result, data = mail_service.uid("search", None, "UNSEEN")
            if self.mail_settings["first_time"]:
                settings.update_settings("EMail", "first_time", False)
                dbc.add_mail_uid(data[0].split())
            else:
                new_mail_uids = dbc.get_mail_not_read(data[0].split())
                mail_notifications = []
                if len(new_mail_uids) != 0:
                    for mail_uid in new_mail_uids:
                        result, data = mail_service.uid('fetch', mail_uid, "(RFC822)")
                        raw_email = data[0][1]
                        email_message = email.message_from_bytes(raw_email)
                        mail_notifications.append(EMail(email_message["From"]))
                dbc.add_to_db(mail_notifications)