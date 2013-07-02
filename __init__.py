#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Inotify tools for entries
version 1.0
history:
2013-6-19    dylanninin@gmail.com    init
"""

import pyinotify
from config import blogconfig as config
from service import EntryService

entryService = EntryService()


class EntryEventHandler(pyinotify.ProcessEvent):
    """
    EntryEventHandler monitor entries added, modified or deleted
    """
    def process_IN_CREATE(self, event):
        entryService.add_entry(True, event.pathname)

    def process_IN_MODIFY(self, event):
        entryService.add_entry(True, event.pathname)
        
    def process_IN_DELETE(self, event):
        entryService.delete_entry(event.pathname)


wm = pyinotify.WatchManager()
mask = pyinotify.IN_CREATE | pyinotify.IN_MODIFY | pyinotify.IN_DELETE
path =  config.entry_dir
notifier = pyinotify.ThreadedNotifier(wm, EntryEventHandler())
wdd = wm.add_watch(path, mask, rec=True)
notifier.start()
