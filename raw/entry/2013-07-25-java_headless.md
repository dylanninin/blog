---
layout: post
title: A Case of Java Headless Exception
category : Java
tags : [Java, Exception]
---

## reproduce exception
    
    [dev@db ~]$ java -version
    java version "1.6.0_33"
    Java(TM) SE Runtime Environment (build 1.6.0_33-b03)
    Java HotSpot(TM) 64-Bit Server VM (build 20.8-b03, mixed mode)
    
    [dev@db ~]$ pwd
    /apps/test/

    [dev@db ~]$ ls -l
    total 40
    drwxrwxr-x. 8 db db 4096 Jul 24 16:21 bin
    drwxrwxr-x. 6 db db 4096 Jul 24 16:21 file
    -rw-rw-r--. 1 db db 1105 Jul 24 16:21 index.htm
    -rw-rw-r--. 1 db db  836 Jul 24 16:21 index.jsp
    drwxrwxr-x. 2 db db 4096 Jul 24 16:21 jsp
    drwxrwxr-x. 2 db db 4096 Jul 24 16:21 logs
    drwxrwxr-x. 2 db db 4096 Jul 24 16:20 META-INF
    -rw-r--r--. 1 db db 4508 Jul 25 15:28 ReportTest.java
    drwxrwxr-x. 7 db db 4096 Jul 25 15:36 WEB-INF
	
exception
	
    [dev@db ~]$ javac ReportTest.java 
    [dev@db ~]$ java ReportTest
    ... ...
    3154 [main] INFO org.hibernate.impl.SessionFactoryObjectFactory - Not binding factory to JNDI, no JNDI name configured
    Exception in thread "main" java.lang.InternalError: Can't connect to X11 window server using 'localhost:10.0' as the value of the DISPLAY variable.
        at sun.awt.X11GraphicsEnvironment.initDisplay(Native Method)
        at sun.awt.X11GraphicsEnvironment.access$100(X11GraphicsEnvironment.java:52)
        at sun.awt.X11GraphicsEnvironment$1.run(X11GraphicsEnvironment.java:155)
        at java.security.AccessController.doPrivileged(Native Method)
        at sun.awt.X11GraphicsEnvironment.<clinit>(X11GraphicsEnvironment.java:131)
        at java.lang.Class.forName0(Native Method)
        at java.lang.Class.forName(Class.java:169)
        at java.awt.GraphicsEnvironment.getLocalGraphicsEnvironment(GraphicsEnvironment.java:68)
        at net.sf.jasperreports.engine.util.JRStyledTextParser.<clinit>(JRStyledTextParser.java:83)
        at net.sf.jasperreports.engine.fill.JRBaseFiller.<init>(JRBaseFiller.java:174)
        at net.sf.jasperreports.engine.fill.JRVerticalFiller.<init>(JRVerticalFiller.java:74)
        at net.sf.jasperreports.engine.fill.JRVerticalFiller.<init>(JRVerticalFiller.java:56)
        at net.sf.jasperreports.engine.fill.JRFiller.createFiller(JRFiller.java:143)
        at net.sf.jasperreports.engine.fill.JRFiller.fillReport(JRFiller.java:53)
        at net.sf.jasperreports.engine.JasperFillManager.fillReport(JasperFillManager.java:417)
        at ReportTest.main(ReportTest.java:77)
        
        
    [dev@db ~]$ java  -Djava.awt.headless=true ReportTest
    ... ...
    3154 [main] INFO org.hibernate.impl.SessionFactoryObjectFactory - Not binding factory to JNDI, no JNDI name configured
    [B@65de41c3

set profile and restart tomcat
    
    [dev@db ~]$ cat ~/.bash_profile 
    # .bash_profile

    # Get the aliases and functions
    if [ -f ~/.bashrc ]; then
        . ~/.bashrc
    fi

    # User specific environment and startup programs
    export CATALINA_HOME=/apps/test/tomcat
    PATH=$PATH:$HOME/bin:$CATALINA_HOME/bin

    export PATH
	
    alias java='java -Djava.awt.headless=true'
    unset DISPLAY

    [dev@db ~]$ ps -ef | grep tomcat
    db     4003     1  1 14:53 ?        00:00:46 /usr/java/jdk1.6.0_33/bin/java -Djava.util.logging.config.file=/apps/test/tomcat/conf/logging.properties -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager -Djava.endorsed.dirs=/apps/test/tomcat/endorsed -classpath /apps/test/tomcat/bin/bootstrap.jar -Dcatalina.base=/apps/db/tomcat -Dcatalina.home=/apps/db/tomcat -Djava.io.tmpdir=/apps/test/tomcat/temp org.apache.catalina.startup.Bootstrap start
    db    13305  6465  0 15:56 pts/3    00:00:00 grep tomcat
    [dev@db ~]$ kill -9 4003
    [dev@db ~]$ catalina.sh start
    Using CATALINA_BASE:   /apps/db/tomcat
    Using CATALINA_HOME:   /apps/db/tomcat
    Using CATALINA_TMPDIR: /apps/test/tomcat/temp
    Using JRE_HOME:        /usr/java/jdk1.6.0_33
    Using CLASSPATH:       /apps/test/tomcat/bin/bootstrap.jar
    
## awt test
   
source code
   
    [root@db sofware]# cat GETest.java 
    import java.awt.GraphicsEnvironment;

    public class GETest{

        public static void main(String[] args){

            GraphicsEnvironment ge = GraphicsEnvironment.getLocalGraphicsEnvironment();
            System.out.println("class: " + ge.getClass());
            System.out.println("isHeadless: " + ge.isHeadless());
        }

    }
	
compile and run test
	
    [root@db sofware]# javac GETest.java 
    [root@db sofware]# java GETest
    Exception in thread "main" java.lang.InternalError: Can't connect to X11 window server using 'localhost:10.0' as the value of the DISPLAY variable.
        at sun.awt.X11GraphicsEnvironment.initDisplay(Native Method)
        at sun.awt.X11GraphicsEnvironment.access$100(X11GraphicsEnvironment.java:52)
        at sun.awt.X11GraphicsEnvironment$1.run(X11GraphicsEnvironment.java:155)
        at java.security.AccessController.doPrivileged(Native Method)
        at sun.awt.X11GraphicsEnvironment.<clinit>(X11GraphicsEnvironment.java:131)
        at java.lang.Class.forName0(Native Method)
        at java.lang.Class.forName(Class.java:169)
        at java.awt.GraphicsEnvironment.getLocalGraphicsEnvironment(GraphicsEnvironment.java:68)
        at GETest.main(GETest.java:7)

    [root@db sofware]# java -Djava.awt.headless=true GETest
    class: class sun.java2d.HeadlessGraphicsEnvironment
    isHeadless: true
    [root@db sofware]# echo $DISPLAY
    localhost:12.0
    [root@db sofware]# java GETest
    Exception in thread "main" java.lang.InternalError: Can't connect to X11 window server using 'localhost:12.0' as the value of the DISPLAY variable.
        at sun.awt.X11GraphicsEnvironment.initDisplay(Native Method)
        at sun.awt.X11GraphicsEnvironment.access$100(X11GraphicsEnvironment.java:52)
        at sun.awt.X11GraphicsEnvironment$1.run(X11GraphicsEnvironment.java:155)
        at java.security.AccessController.doPrivileged(Native Method)
        at sun.awt.X11GraphicsEnvironment.<clinit>(X11GraphicsEnvironment.java:131)
        at java.lang.Class.forName0(Native Method)
        at java.lang.Class.forName(Class.java:169)
        at java.awt.GraphicsEnvironment.getLocalGraphicsEnvironment(GraphicsEnvironment.java:68)
        at GETest.main(GETest.java:7)

unset DISPLAY
		
    [root@db sofware]# unset DISPLAY
    [root@db sofware]# java GETest
    class: class sun.java2d.HeadlessGraphicsEnvironment
    isHeadless: true

## Summary
    
1) Java Technology Community

How to resolve java Exceptions ? :java.awt.HeadlessException

2) java.awt.HeadlessException
 
I have seen this Exception being encountered by many applications, which use UI (AWT/Swing) APIs .

3) When is this exception thrown ? 

java.awt.HeadlessException is thrown on a machine which is headless  when -Djava.awt.headless commandline option is set to true and  Heavyweight AWT components like Applet, Button, Checkbox, Choice, FileDialog, Label, List, Menu, MenuBar, MenuComponent, MenuItem, PopupMenu, Scrollbar,ScrollPane, TextArea, TextComponent, Frame, Window, Dialog, JApplet, JFrame, JWindow, JDialog and TextField are used in the environment.

4) What is the option -Djava.awt.headless all about? 

Many environments, such as mainframe machines and dedicated servers, do not support a display, keyboard, or mouse. On Such machines if we try to to use AWT package,we will get an error like this
"Can't connect to X11 window server using ':0.0' as the value of the DISPLAY variable.
at sun.awt.X11GraphicsEnvironment.initDisplay"
This error is thrown as the AWT package is causing the X11 server to open the DISPLAY.
To correct this problem, We need to tell the Java AWT package that the X11 server is headless (has no display).
To run our environment with a headless implementation, the follow property may be specified at the java command line: 
        
	-Djava.awt.headless=true
		
This will tell the AWT package about the X11 server being headless.
This option is available from Java 1.4 onwards.

5) Why we get a "HeadlessException" after setting this option ?

Headless support is enabled by the GraphicsEnvironment methods "isHeadless" and "isHeadlessInstance".

These methods check whether X11 server has a DISPLAY or its headless(without a DISPLAY).

The heavyweight AWT components like Applet, Button, Checkbox, Choice, FileDialog, Label, List, Menu, MenuBar, MenuComponent, MenuItem, PopupMenu, Scrollbar, ScrollPane, TextArea, TextComponent, Frame, Window, Dialog, JApplet, JFrame, JWindow, JDialog and TextField are affected by the lack of DISPLAY,keyboard  and mouse etc.
Therefore ,if used in a "headless" environment they all will throw a "HeadlessException" like this -
	
	java.awt.HeadlessException 
	at java.awt.GraphicsEnvironment.checkHeadless(GraphicsEnvironment.java:150) 
	at java.awt.Window.<init>(Window.java:311) 
	at java.awt.Frame.<init>(Frame.java:431) 
	at java.awt.Frame.<init>(Frame.java:396)

6) How can we resolve this exception/related erros ?

-Check whether the X11 server is installed 
-Check whether DISPLAY variable is properly set 
-Heavyweight awt/swing components which requires display, mouse keyboard should be run on client side rather than server side.