#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Inotify tools for entries
version 1.0
history:
2013-6-19    dylanninin@gmail.com    init
"""

from config import blogconfig as config
from service import EntryService

entryService = EntryService()


# pyinotify is optional when just have a try
try:
    import pyinotify
except ImportError:
    print 'Could not import pyinotify'
else:
    class EntryEventHandler(pyinotify.ProcessEvent):
        """
        EntryEventHandler monitor entries added, modified or deleted
        """
        def process_default(self, event):
            """
            处理监听的业务逻辑
            :param event:
            :return:
            """
            mask_add = pyinotify.IN_CLOSE_WRITE | pyinotify.IN_MOVED_TO | pyinotify.IN_MOVE_SELF
            mask_del = pyinotify.IN_DELETE | pyinotify.IN_DELETE_SELF | pyinotify.IN_MOVED_FROM | pyinotify.IN_MOVE_SELF
            if event.mask & mask_add:
                entryService.add_entry(True, event.pathname)
            if event.mask & mask_del:
                entryService.delete_entry(event.pathname)


    wm = pyinotify.WatchManager()
    mask = pyinotify.ALL_EVENTS
    path = config.entry_dir
    notifier = pyinotify.ThreadedNotifier(wm, EntryEventHandler())
    wdd = wm.add_watch(path, mask, rec=True)
    notifier.start()
