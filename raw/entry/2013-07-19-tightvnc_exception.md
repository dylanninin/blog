---
layout: post
title: A Case of TightVNC Exception
category : Linux
tags : [Linux, Utilities, Exception]
---

configure tightvnc

    [root@db ~]# su - oracle

    [oracle@db ~]$ vncpasswd 
    Password:
    Verify:
	
start vncserver
	
    [oracle@db ~]$ vncserver 

    WARNING: The first attempt to start Xvnc failed, possibly because the font
    catalog is not properly configured.  Attempting to determine an appropriate
    font path for this system and restart Xvnc using that font path ...
    Could not start Xvnc.


    Xvnc TigerVNC 1.1.0 - built Feb 22 2013 22:28:37
    Copyright (C) 1999-2011 TigerVNC Team and many others (see README.txt)
    See http://www.tigervnc.org for information on TigerVNC.
    Underlying X server release 11300000, The X.Org Foundation

    Initializing built-in extension Generic Event Extension
    Initializing built-in extension SHAPE
    Initializing built-in extension MIT-SHM
    Initializing built-in extension XInputExtension
    Initializing built-in extension XTEST
    Initializing built-in extension BIG-REQUESTS
    Initializing built-in extension SYNC
    Initializing built-in extension XKEYBOARD
    Initializing built-in extension XC-MISC
    Initializing built-in extension XFIXES
    Initializing built-in extension RENDER
    Initializing built-in extension RANDR
    Initializing built-in extension DAMAGE
    Initializing built-in extension MIT-SCREEN-SAVER
    Initializing built-in extension DOUBLE-BUFFER
    Initializing built-in extension RECORD
    Initializing built-in extension DPMS
    Initializing built-in extension X-Resource
    Initializing built-in extension XVideo
    Initializing built-in extension XVideo-MotionCompensation
    Initializing built-in extension VNC

    Fri Jul 19 11:32:29 2013
     vncext:      VNC extension running!
     vncext:      Listening for VNC connections on all interface(s), port 5901
     vncext:      created VNC server for screen 0
    [dix] Could not init font path element catalogue:/etc/X11/fontpath.d, removing from list!
    [dix] Could not init font path element built-ins, removing from list!

    Fatal server error:
    could not open default font 'fixed'

    Xvnc TigerVNC 1.1.0 - built Feb 22 2013 22:28:37
    Copyright (C) 1999-2011 TigerVNC Team and many others (see README.txt)
    See http://www.tigervnc.org for information on TigerVNC.
    Underlying X server release 11300000, The X.Org Foundation

    Initializing built-in extension Generic Event Extension
    Initializing built-in extension SHAPE
    Initializing built-in extension MIT-SHM
    Initializing built-in extension XInputExtension
    Initializing built-in extension XTEST
    Initializing built-in extension BIG-REQUESTS
    Initializing built-in extension SYNC
    Initializing built-in extension XKEYBOARD
    Initializing built-in extension XC-MISC
    Initializing built-in extension XFIXES
    Initializing built-in extension RENDER
    Initializing built-in extension RANDR
    Initializing built-in extension DAMAGE
    Initializing built-in extension MIT-SCREEN-SAVER
    Initializing built-in extension DOUBLE-BUFFER
    Initializing built-in extension RECORD
    Initializing built-in extension DPMS
    Initializing built-in extension X-Resource
    Initializing built-in extension XVideo
    Initializing built-in extension XVideo-MotionCompensation
    Initializing built-in extension VNC

    Fri Jul 19 11:32:32 2013
     vncext:      VNC extension running!
     vncext:      Listening for VNC connections on all interface(s), port 5901
     vncext:      created VNC server for screen 0
    [dix] Could not init font path element /usr/share/X11/fonts/misc, removing from list!
    [dix] Could not init font path element /usr/share/X11/fonts/100dpi, removing from list!
    [dix] Could not init font path element /usr/share/X11/fonts/Type1, removing from list!
    [dix] Could not init font path element /usr/share/fonts/default/Type1, removing from list!
    [dix] Could not init font path element built-ins, removing from list!

    Fatal server error:
    could not open default font 'fixed'

reinstall vncserver
    
    [root@db yum.repos.d]# rpm -qa | grep vnc
    tigervnc-server-1.1.0-5.el6.x86_64
    [root@db yum.repos.d]# rpm -e tigervnc-server-1.1.0-5.el6.x86_64

    [root@db sofware]# yum groupinstall -y "X Window System"
    [root@db sofware]# yum -y install tigervnc-server pixman pixman-devel libXfont
   
config and start vncserver
    
    [root@db sofware]# chkconfig vncserver on
    [root@db sofware]# vncpasswd 
    Password:
    Verify:
    [root@db sofware]# vncserver 

    New 'db.egolife.com:1 (root)' desktop is db.egolife.com:1

    Creating default startup script /root/.vnc/xstartup
    Starting applications specified in /root/.vnc/xstartup
    Log file is /root/.vnc/db.egolife.com:1.log