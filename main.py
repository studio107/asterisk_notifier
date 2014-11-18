# coding=utf-8

import objc
import re
import os
from Foundation import *
from AppKit import *
from PyObjCTools import AppHelper
import rumps
import thread
import requests
import time
import os
import Foundation
import objc
import AppKit
import sys

NSUserNotification = objc.lookUpClass('NSUserNotification')
NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')


def notify(title, subtitle, info_text, delay=0, sound=False, userInfo={}):
    notification = NSUserNotification.alloc().init()
    notification.setTitle_(title)
    notification.setSubtitle_(subtitle)
    notification.setInformativeText_(info_text)
    notification.setUserInfo_(userInfo)
    if sound:
        notification.setSoundName_("NSUserNotificationDefaultSoundName")
    notification.setDeliveryDate_(
        Foundation.NSDate.dateWithTimeInterval_sinceDate_(delay, Foundation.NSDate.date()))
    NSUserNotificationCenter.defaultUserNotificationCenter(
    ).scheduleNotification_(notification)


# poach one of the iSync internal images to get things rolling
status_images = {'main': 'images/logo.png'}
start_time = NSDate.date()
last_timestamp = None


class Timer(NSObject):
    images = {}
    statusbar = None
    state = 'main'

    def applicationDidFinishLaunching_(self, notification):
        statusbar = NSStatusBar.systemStatusBar()
        # Create the statusbar item
        self.statusitem = statusbar.statusItemWithLength_(
            NSVariableStatusItemLength)
        # Load all images
        for i in status_images.keys():
            self.images[i] = NSImage.alloc().initByReferencingFile_(
                status_images[i])
        # Set initial image
        self.statusitem.setImage_(self.images['main'])
        # Let it highlight upon clicking
        self.statusitem.setHighlightMode_(1)
        # Set a tooltip
        self.statusitem.setToolTip_('Sync Trigger')

        # Build a very simple menu
        self.menu = NSMenu.alloc().init()
        # Default event
        menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            'Quit', 'terminate:', '')
        self.menu.addItem_(menuitem)
        # Bind it to the status item
        self.statusitem.setMenu_(self.menu)

        # Get the timer going
        self.timer = NSTimer.alloc().initWithFireDate_interval_target_selector_userInfo_repeats_(
            start_time, 1.0, self, 'tick:', None, True)
        NSRunLoop.currentRunLoop().addTimer_forMode_(
            self.timer, NSDefaultRunLoopMode)
        self.timer.fire()

    def tick_(self, notification):
        global last_timestamp
        base_url = 'http://192.168.0.249:8088/asterisk/static/current_incoming'
        r = requests.get(base_url)
        try:
            timestamp, number, _ = r.text.split("\n")
            timestamp = int(timestamp)
        except:
            print("Incorrect response: %s" % r.text)
        else:
            if last_timestamp is None:
                last_timestamp = timestamp

            if timestamp > last_timestamp:
                last_timestamp = timestamp
                notify(u"Входящий еба: %s" %
                       number, u"че бля тупишь", u"алё", sound=True)


if __name__ == "__main__":
    app = NSApplication.sharedApplication()
    delegate = Timer.alloc().init()
    app.setDelegate_(delegate)
    AppHelper.runEventLoop()
