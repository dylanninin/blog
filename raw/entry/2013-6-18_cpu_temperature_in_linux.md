#Detect CPU Temperatur

os kernel

	[root@tplat1 ~]# uname -a
	Linux tplat1.egolife.net 2.6.32-358.el6.x86_64 #1 SMP Fri Feb 22 13:35:02 PST 2013 x86_64 x86_64 x86_64 GNU/Linux

install lm_sensors

	[root@tplat1 ~]# yum install -y lm_sensors
	Loaded plugins: refresh-packagekit, security
	Setting up Install Process
	Resolving Dependencies
	--> Running transaction check
	---> Package lm_sensors.x86_64 0:3.1.1-17.el6 will be installed
	--> Finished Dependency Resolution
	
	Dependencies Resolved
	
	========================================================================================================================================
	 Package                           Arch                          Version                              Repository                   Size
	========================================================================================================================================
	Installing:
	 lm_sensors                        x86_64                        3.1.1-17.el6                         base                        123 k
	
	Transaction Summary
	========================================================================================================================================
	Install       1 Package(s)
	
	Total download size: 123 k
	Installed size: 350 k
	Downloading Packages:
	lm_sensors-3.1.1-17.el6.x86_64.rpm                                                                               | 123 kB     00:00     
	Running rpm_check_debug
	Running Transaction Test
	Transaction Test Succeeded
	Running Transaction
	  Installing : lm_sensors-3.1.1-17.el6.x86_64                                                                                       1/1 
	  Verifying  : lm_sensors-3.1.1-17.el6.x86_64                                                                                       1/1 
	
	Installed:
	  lm_sensors.x86_64 0:3.1.1-17.el6                                                                                                      
	
	Complete!

detect sensors

	[root@tplat1 ~]# sensors-detect 
	# sensors-detect revision 1.1
	# System: IBM System x3650 M4 -[7915I31]-
	# Board: IBM 00J6520
	
	This program will help you determine which kernel modules you need
	to load to use lm_sensors most effectively. It is generally safe
	and recommended to accept the default answers to all questions,
	unless you know what you're doing.
	
	Some south bridges, CPUs or memory controllers contain embedded sensors.
	Do you want to scan for them? This is totally safe. (YES/no): Y
	Silicon Integrated Systems SIS5595...                       No
	VIA VT82C686 Integrated Sensors...                          No
	VIA VT8231 Integrated Sensors...                            No
	AMD K8 thermal sensors...                                   No
	AMD Family 11h thermal sensors...                           No
	Intel digital thermal sensor...                             Success!
	    (driver `coretemp')
	Intel AMB FB-DIMM thermal sensor...                         No
	VIA C7 thermal and voltage sensors...                       No
	
	Some Super I/O chips contain embedded sensors. We have to write to
	standard I/O ports to probe them. This is usually safe.
	Do you want to scan for Super I/O sensors? (YES/no): Y
	Probing for Super-I/O at 0x2e/0x2f
	Trying family `National Semiconductor'...                   Yes
	Found unknown chip with ID 0x3711
	Probing for Super-I/O at 0x4e/0x4f
	Trying family `National Semiconductor'...                   No
	Trying family `SMSC'...                                     No
	Trying family `VIA/Winbond/Nuvoton/Fintek'...               No
	Trying family `ITE'...                                      No
	
	Some systems (mainly servers) implement IPMI, a set of common interfaces
	through which system health data may be retrieved, amongst other things.
	We first try to get the information from SMBIOS. If we don't find it
	there, we have to read from arbitrary I/O ports to probe for such
	interfaces. This is normally safe. Do you want to scan for IPMI
	interfaces? (YES/no): Y
	Found `IPMI BMC KCS' at 0xcc0...                            Success!
	    (confidence 8, driver `ipmisensors')
	
	Some hardware monitoring chips are accessible through the ISA I/O ports.
	We have to write to arbitrary I/O ports to probe them. This is usually
	safe though. Yes, you do have ISA I/O ports even if you do not have any
	ISA slots! Do you want to scan the ISA I/O ports? (YES/no): Y
	Probing for `National Semiconductor LM78' at 0x290...       No
	Probing for `National Semiconductor LM79' at 0x290...       No
	Probing for `Winbond W83781D' at 0x290...                   No
	Probing for `Winbond W83782D' at 0x290...                   No
	
	Lastly, we can probe the I2C/SMBus adapters for connected hardware
	monitoring devices. This is the most risky part, and while it works
	reasonably well on most systems, it has been reported to cause trouble
	on some systems.
	Do you want to probe the I2C/SMBus adapters now? (YES/no): Y
	Found unknown SMBus adapter 8086:1d22 at 0000:00:1f.3.
	Sorry, no supported PCI bus adapters found.
	Module i2c-dev loaded successfully.
	
	Next adapter: SMBus I801 adapter at 4000 (i2c-0)
	Do you want to scan it? (YES/no/selectively): Y
	Client found at address 0x48
	Probing for `National Semiconductor LM75'...                No
	Probing for `Dallas Semiconductor DS75'...                  No
	Probing for `National Semiconductor LM77'...                No
	Probing for `Dallas Semiconductor DS1621/DS1631'...         No
	Probing for `Maxim MAX6650/MAX6651'...                      No
	Probing for `National Semiconductor LM73'...                No
	Probing for `National Semiconductor LM92'...                No
	Probing for `National Semiconductor LM76'...                No
	Probing for `Maxim MAX6633/MAX6634/MAX6635'...              No
	
	Now follows a summary of the probes I have just done.
	Just press ENTER to continue: 
	
	Driver `coretemp':
	  * Chip `Intel digital thermal sensor' (confidence: 9)
	
	Driver `ipmisensors':
	  * ISA bus, address 0xcc0
	    Chip `IPMI BMC KCS' (confidence: 8)
	
	Warning: the required module ipmisensors is not currently installed
	on your system. If it is built into the kernel then it's OK.
	Otherwise, check http://www.lm-sensors.org/wiki/Devices for
	driver availability.
	
	Do you want to overwrite /etc/sysconfig/lm_sensors? (YES/no): Y
	Starting lm_sensors: loading module ipmi-si coretemp       [  OK  ]
	Unloading i2c-dev... OK

note: yes|sensors-detect

get current cup temperature

	[root@tplat1 ~]# sensors
	coretemp-isa-0000
	Adapter: ISA adapter
	Physical id 0: +39.0°C  (high = +81.0°C, crit = +91.0°C)  
	Core 0:        +35.0°C  (high = +81.0°C, crit = +91.0°C)  
	Core 1:        +36.0°C  (high = +81.0°C, crit = +91.0°C)  
	Core 2:        +36.0°C  (high = +81.0°C, crit = +91.0°C)  
	Core 3:        +39.0°C  (high = +81.0°C, crit = +91.0°C)  
	Core 4:        +33.0°C  (high = +81.0°C, crit = +91.0°C)  
	Core 5:        +38.0°C  (high = +81.0°C, crit = +91.0°C) 

#Reference

* [Linux下查看CPU温度](http://www.linuxsong.org/2010/09/linux-look-cpu-temperature/)
