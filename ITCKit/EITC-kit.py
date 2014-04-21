__author__ = 'Kristo Koert'

from gui import toolbarindicator
from mail import email_system
from core import notification_system
from gi.repository import Gtk, Gdk

if __name__ == "__main__":
    #ToDo possible race condition?
    import time

    Gdk.threads_init()
    indicator = toolbarindicator.activate_toolbar()

    time.sleep(0.25)

    Gdk.threads_leave()
    email_thread = email_system.MailHandler()
    email_thread.start()
    Gdk.threads_enter()

    time.sleep(0.25)

    Gdk.threads_leave()
    notification_thread = notification_system.NotificationHandler(indicator, indicator.main_menu)
    notification_thread.start()
    Gdk.threads_enter()

    time.sleep(0.25)

    Gtk.main()