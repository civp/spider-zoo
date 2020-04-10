"""Tracks updates of web pages using etag.
TODO: multi-page, snapshot
"""
import os
import time
import datetime
import tkinter
from tkinter import messagebox

import requests

# hide main tkinter window
root = tkinter.Tk()
root.withdraw()


class Tracker():
    """Tracks the content of a page.

    Attributes:
        url (str): URL of a page.
        interval (int): Tracking interval in seconds.
        cache (str): Cached etag.
    """
    def __init__(self, url, interval=600):
        self.url = url
        self.interval = interval
        self.cache = None

    def check_etag(self):
        """Checks is etag up to date."""
        etag = requests.get(self.url).headers.get('etag', None)
        if not etag:
            raise ValueError('Error: etag not available in {}'.format(self.url))
        if self.cache and self.cache != etag:
            self.cache = etag
            return True
        return False

    def alert(self):
        messagebox.showinfo('Page Updated', 'Check {}'.format(self.url))

    def run(self):
        try:
            while True:
                if not self.check_etag():
                    self.alert()
                time.sleep(self.interval)
        except KeyboardInterrupt:
            print('Ciao')


if __name__ == "__main__":
    Tracker('URL').run()