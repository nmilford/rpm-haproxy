# To Build:
#
# sudo yum -y install rpmdevtools && rpmdev-setuptree
# sudo yum -y install pcre-devel gcc make
# wget https://raw.github.com/nmilford/rpm-haproxy/master/haproxy.spec -O ~/rpmbuild/SPECS/haproxy.spec
# wget http://haproxy.1wt.eu/download/1.5/src/devel/haproxy-1.5-dev26.tar.gz -O ~/rpmbuild/SOURCES/haproxy-1.5-dev26.tar.gz
# rpmbuild -bb  ~/rpmbuild/SPECS/haproxy.spec

%define version 1.5.10
%define release 1

Summary: HA-Proxy is a TCP/HTTP reverse proxy for high availability environments
Name: haproxy
Version: %{version}
Release: %{release}%{?dist}
License: GPL
Group: System Environment/Daemons
URL: http://haproxy.1wt.eu/
Source0: http://haproxy.1wt.eu/download/1.5/src/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: pcre-devel make gcc openssl-devel
Requires: /sbin/chkconfig, /sbin/service

%description
HA-Proxy is a TCP/HTTP reverse proxy which is particularly suited for high
availability environments. Indeed, it can:
- route HTTP requests depending on statically assigned cookies
- spread the load among several servers while assuring server persistence
  through the use of HTTP cookies
- switch to backup servers in the event a main one fails
- accept connections to special ports dedicated to service monitoring
- stop accepting connections without breaking existing ones
- add/modify/delete HTTP headers both ways
- block requests matching a particular pattern

It needs very little resource. Its event-driven architecture allows it to easily
handle thousands of simultaneous connections on hundreds of instances without
risking the system's stability.

%prep
%setup -n %{name}-%{version}

# We don't want any perl dependecies in this RPM:
%define __perl_requires /bin/true

%build
%{__make} USE_PCRE=1 DEBUG="" ARCH=%{_target_cpu} TARGET=linux26 USE_OPENSSL=1

%install
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%{__install} -d %{buildroot}%{_sbindir}
%{__install} -d %{buildroot}%{_sysconfdir}/rc.d/init.d
%{__install} -d %{buildroot}%{_sysconfdir}/%{name}
%{__install} -d %{buildroot}%{_mandir}/man1/
%{__install} -d %{buildroot}%{_sharedstatedir}/haproxy

mkdir -p %{buildroot}/etc/haproxy/errors
mkdir -p %{buildroot}/usr/share/haproxy
cp examples/errorfiles/503.http %{buildroot}/etc/haproxy/errors/503.http

%{__install} -s %{name} %{buildroot}%{_sbindir}/
%{__install} -c -m 644 examples/%{name}.cfg %{buildroot}%{_sysconfdir}/%{name}/
%{__install} -c -m 755 examples/%{name}.init %{buildroot}%{_sysconfdir}/rc.d/init.d/%{name}
%{__install} -c -m 755 doc/%{name}.1 %{buildroot}%{_mandir}/man1/

%clean
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%pre
/usr/sbin/groupadd -g 188 -r haproxy 2>/dev/null || :
/usr/sbin/useradd -u 188 -g haproxy -d /var/lib/haproxy -s /sbin/nologin -r haproxy 2>/dev/null || :

%post
/sbin/chkconfig --add %{name}

%preun
if [ $1 = 0 ]; then
  /sbin/service %{name} stop >/dev/null 2>&1 || :
  /sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" -ge "1" ]; then
  /sbin/service %{name} condrestart >/dev/null 2>&1 || :
fi

%files
/usr/share/haproxy
/etc/haproxy/errors/503.http

%defattr(-,root,root)
%doc CHANGELOG examples/*.cfg doc/haproxy-en.txt doc/haproxy-fr.txt doc/architecture.txt doc/configuration.txt
%doc %{_mandir}/man1/%{name}.1*

%attr(0755,root,root) %{_sbindir}/%{name}
%dir %{_sysconfdir}/%{name}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/%{name}.cfg
%attr(0755,root,root) %config %{_sysconfdir}/rc.d/init.d/%{name}

%attr(0755,haproxy,haproxy) %{_sharedstatedir}/haproxy

%changelog
* Thu Aug 21 2014 Don Ky <don.d.ky@gmail.com>
- updated to 1.5.0-dev26

* Mon May 19 2014 Tim Shelton <timothy.shelton@gmail.com>
- updated to 1.5.0-dev25

* Fri Mar 05 2014 Ilya Sukhanov <ilya@sukhanov.net>
- updated to 1.5.0-dev22

* Fri Feb 21 2014 Chao Lin <clin@amplify.com>
- Build with ssl support

* Mon Oct 15 2013 Ilya Sukhanov <ilya@sukhanov.net>
- add user creation
- set up chroot dir

* Mon Jul 01 2013 Nathan Milford <nathan@milford.io>
- updated to 1.5.0-dev19

* Mon Nov 29 2010 Willy Tarreau <w@1wt.eu>
- updated to 1.4.10

* Fri Oct 29 2010 Willy Tarreau <w@1wt.eu>
- updated to 1.4.9

* Wed Jun 16 2010 Willy Tarreau <w@1wt.eu>
- updated to 1.4.8

* Mon Jun  7 2010 Willy Tarreau <w@1wt.eu>
- updated to 1.4.7

* Sun May 16 2010 Willy Tarreau <w@1wt.eu>
- updated to 1.4.6

* Thu May 13 2010 Willy Tarreau <w@1wt.eu>
- updated to 1.4.5

* Wed Apr  7 2010 Willy Tarreau <w@1wt.eu>
- updated to 1.4.4

* Tue Mar 30 2010 Willy Tarreau <w@1wt.eu>
- updated to 1.4.3

* Wed Mar 17 2010 Willy Tarreau <w@1wt.eu>
- updated to 1.4.2

* Thu Mar  4 2010 Willy Tarreau <w@1wt.eu>
- updated to 1.4.1

* Fri Feb 26 2010 Willy Tarreau <w@1wt.eu>
- updated to 1.4.0

* Tue Feb  2 2010 Willy Tarreau <w@1wt.eu>
- updated to 1.4-rc1

* Mon Jan 25 2010 Willy Tarreau <w@1wt.eu>
- updated to 1.4-dev8

* Mon Jan 25 2010 Willy Tarreau <w@1wt.eu>
- updated to 1.4-dev7

* Fri Jan  8 2010 Willy Tarreau <w@1wt.eu>
- updated to 1.4-dev6

* Sun Jan  3 2010 Willy Tarreau <w@1wt.eu>
- updated to 1.4-dev5

* Mon Oct 12 2009 Willy Tarreau <w@1wt.eu>
- updated to 1.4-dev4

* Thu Sep 24 2009 Willy Tarreau <w@1wt.eu>
- updated to 1.4-dev3

* Sun Aug  9 2009 Willy Tarreau <w@1wt.eu>
- updated to 1.4-dev2

* Wed Jul 29 2009 Willy Tarreau <w@1wt.eu>
- updated to 1.4-dev1

* Tue Jun 09 2009 Willy Tarreau <w@1wt.eu>
- updated to 1.4-dev0

* Sun May 10 2009 Willy Tarreau <w@1wt.eu>
- updated to 1.3.18

* Sun Mar 29 2009 Willy Tarreau <w@1wt.eu>
- updated to 1.3.17

* Sun Mar 22 2009 Willy Tarreau <w@1wt.eu>
- updated to 1.3.16

* Sat Apr 19 2008 Willy Tarreau <w@1wt.eu>
- updated to 1.3.15

* Wed Dec  5 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.14

* Thu Oct 18 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.13

* Sun Jun 17 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.12

* Sun Jun  3 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.11.4

* Mon May 14 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.11.3

* Mon May 14 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.11.2

* Mon May 14 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.11.1

* Mon May 14 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.11

* Thu May 10 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.10.2

* Tue May 09 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.10.1

* Tue May 08 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.10

* Sun Apr 15 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.9

* Tue Apr 03 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.8.2

* Sun Apr 01 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.8.1

* Sun Mar 25 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.8

* Wed Jan 26 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.7

* Wed Jan 22 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.6

* Wed Jan 07 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.5

* Wed Jan 02 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.4

* Wed Oct 15 2006 Willy Tarreau <w@1wt.eu>
- updated to 1.3.3

* Wed Sep 03 2006 Willy Tarreau <w@1wt.eu>
- updated to 1.3.2

* Wed Jul 09 2006 Willy Tarreau <w@1wt.eu>
- updated to 1.3.1

* Wed May 21 2006 Willy Tarreau <willy@w.ods.org>
- updated to 1.2.14

* Wed May 01 2006 Willy Tarreau <willy@w.ods.org>
- updated to 1.2.13

* Wed Apr 15 2006 Willy Tarreau <willy@w.ods.org>
- updated to 1.2.12

* Wed Mar 30 2006 Willy Tarreau <willy@w.ods.org>
- updated to 1.2.11.1

* Wed Mar 19 2006 Willy Tarreau <willy@w.ods.org>
- updated to 1.2.10

* Wed Mar 15 2006 Willy Tarreau <willy@w.ods.org>
- updated to 1.2.9

* Sat Jan 22 2005 Willy Tarreau <willy@w.ods.org>
- updated to 1.2.3 (1.1.30)

* Sun Nov 14 2004 Willy Tarreau <w@w.ods.org>
- updated to 1.1.29
- fixed path to config and init files
- statically linked PCRE to increase portability to non-pcre systems

* Sun Jun  6 2004 Willy Tarreau <willy@w.ods.org>
- updated to 1.1.28
- added config check support to the init script

* Tue Oct 28 2003 Simon Matter <simon.matter@invoca.ch>
- updated to 1.1.27
- added pid support to the init script

* Wed Oct 22 2003 Simon Matter <simon.matter@invoca.ch>
- updated to 1.1.26

* Thu Oct 16 2003 Simon Matter <simon.matter@invoca.ch>
- initial build
