---
layout: post
title: Integration SVN with HTTPD and LDAP
category : Linux
tags : [SVN, Apache, LDAP, Linux]
---

## Subversion Architecture

![svn_arch](http://dylanninin.com/assets/images/2013/svn_architecture.png)

## HTTP

To network your repository over HTTP, you basically need four components, available in two packages. You'll need Apache httpd 2.0 or newer, the mod_dav DAV module that comes with it, Subversion, and the `mod_dav_svn` filesystem provider module distributed with Subversion. Once you have all of those components, the process of networking your repository is as simple as:
 
* Getting httpd up and running with the mod_dav module
* Installing the mod_dav_svn backend to mod_dav, which uses Subversion's libraries to access the repository
* Configuring your httpd.conffile to export (or expose) the repository

### `mod_dav_svn`

mod_dav_svn Configuration Directives — Apache configuration directives for serving Subversion repositories through the Apache
HTTP Server.

### `mod_authz_svn`

mod_authz_svn Configuration Directives — Apache configuration directives for configuring path-based authorization for Subversion repositories served through the Apache HTTP Server.

## LDAP 

This module provides authentication front-ends such as mod_auth_basic to authenticate users through an ldap directory.

`mod_authnz_ldap` supports the following features:

* Known to support the OpenLDAP SDK (both 1.x and 2.x), Novell LDAP SDK and the iPlanet (Netscape) SDK.
* Complex authorization policies can be implemented by representing the policy with LDAP filters.
* Uses extensive caching of LDAP operations via mod_ldap.
* Support for LDAP over SSL (requires the Netscape SDK) or TLS (requires the OpenLDAP 2.x SDK or Novell LDAP SDK).

## Sample Configure of SVN, HTTP, LDAP

### Load Module to support SVN

modify /etc/httpd/conf.d/subversion.conf:

	LoadModule dav_module         modules/mod_dav.so
	LoadModule dav_svn_module     modules/mod_dav_svn.so
	LoadModule authz_svn_module   modules/mod_authz_svn.so

### Basic Config

The easiest way to authenticate a client is via the HTTP Basic authentication mechanism, which simply uses a username and password to verify a user's identity. Apache provides the htpasswd utility for managing files containing usernames and passwords.

create a password file:

	$ htpasswd -c -m /apps/svnroot/passwd harry
	New password: *****
	Re-type new password: *****
	Adding password for user harry
	$ htpasswd -m /apps/svnroot/passwd sally
	New password: *******
	Re-type new password: *******
	Adding password for user sally
	
modify /etc/httpd/conf.d/subversion.conf:

	<Location /svn>
		DAV svn
		SVNParentPath /apps/svnroot/
		AuthzSVNAccessFile /apps/svnroot/authz.conf
		AuthType Basic
		AuthName "Subversion welcome to svn"
		AuthUserFile /apps/svnroot/passwd
		Require valid-user
	</Location>

### Load Module to support LDAP

modify /etc/httpd/conf/httpd.conf:

	LoadModule ldap_module modules/mod_ldap.so
	LoadModule authnz_ldap_module modules/mod_authnz_ldap.so

modify /etc/httpd/conf.d/subversion.conf:
	
		<Location /IT>
		DAV svn
		SVNParentPath  /apps/svnroot/
		AuthType Basic
		AuthName "Subversion Repository"
	#   Auth by LDAP
		AuthBasicProvider ldap
		AuthzLDAPAuthoritative off
		AuthLDAPURL  "ldap://192.168.1.111:389/dc=test-it,dc=net?mail?sub"
		AuthLDAPBindDN  "cn=it,ou=admin,dc=test-it,dc=net"
		AuthLDAPBindPassword "itpassword"
	
	#   Auth by passwd file
	#	AuthUserFile /apps/svnroot/passwd
		AuthzSVNAccessFile /apps/svnroot/authz_svn
		Require  valid-user
	</Location>


An [RFC 2255](https://tools.ietf.org/html/rfc2255) URL which specifies the LDAP search parameters to use. The syntax of the URL is

	ldap://host:port/basedn?attribute?scope?filter

## Reference

* Version Control with Subversion
* [`mod_authz_svn`](http://svn.apache.org/repos/asf/subversion/trunk/subversion/mod_authz_svn/INSTALL)
* [`mod_authnz_ldap`](http://httpd.apache.org/docs/2.2/mod/mod_authnz_ldap.html)
* [RFC 2255 - The LDAP URL Format](https://tools.ietf.org/html/rfc2255)
