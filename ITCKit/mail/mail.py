__author__ = 'Kristo Koert'

#ToDo implement

import imaplib

from ITCKit.settings.settings import get_mail_username, get_mail_password, get_mail_activation_date


def get_unread_email():
    mail_service = imaplib.IMAP4_SSL('outlook.office365.com')
    #Deal with invalid username and password
    mail_service.login(get_mail_username(), get_mail_password())
    inbox = mail_service.select("inbox")
    result, data = mail_service.search(None, '(UNSEEN SENTSINCE {0})'.format(get_mail_activation_date()))
    ids = data[0]
    id_list = ids.split()
    print(len(id_list))
    latest_email_id = id_list[-1]
    print(id_list[-1])
    # message body> RFC822
    result, data = mail_service.fetch(latest_email_id, "(RFC822)")
    raw_email = data[0][1]
    return raw_email

#Date: Sat, 22 Mar 2014 11:36:56 +0000
#From: Kristo Koert <kristo.koert@itcollege.ee>

if __name__ == "__main__":
    print(get_unread_email())