%define modname dbx
%define dirname %{modname}
%define soname %{modname}.so
%define inifile 16_%{modname}.ini

Summary:	DBX extension module for PHP
Name:		php-%{modname}
Version:	1.1.2
Release:	7
Group:		Development/PHP
URL:		https://www.php.net
License:	PHP License
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
Source1:	%{modname}.ini
BuildRequires:	php-devel >= 3:5.2.0
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The dbx module is a database abstraction layer. The dbx functions
allow you to access all supported databases using a single calling
convention. The dbx-functions themselves do not interface directly
to the databases, but interface to the modules that are used to
support these databases. The currently supported databases are
MySQL, ODBC, Oracle (oci8), MS SQL Server, PostgreSQL, FrontBase,
Sybase-CT and SQLite. The module-dependencies are only for the
databases you wish to use.

%prep

%setup -q -n %{modname}-%{version}
[ "../package.xml" != "/" ] && mv ../package.xml .

cp %{SOURCE1} %{inifile}

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/
install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc CREDITS howto_extend_dbx.html package.xml tests
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


%changelog
* Thu May 03 2012 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.2-5mdv2012.0
+ Revision: 795423
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.2-4
+ Revision: 761214
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.2-3
+ Revision: 696407
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.2-2
+ Revision: 695380
- rebuilt for php-5.3.7

* Thu Aug 11 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.2-1
+ Revision: 694013
- 1.1.2

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.0-35
+ Revision: 646624
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.0-34mdv2011.0
+ Revision: 629779
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.0-33mdv2011.0
+ Revision: 628090
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.0-32mdv2011.0
+ Revision: 600472
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.0-31mdv2011.0
+ Revision: 588755
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.0-30mdv2010.1
+ Revision: 514529
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.0-29mdv2010.1
+ Revision: 485350
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.0-28mdv2010.1
+ Revision: 468156
- rebuilt against php-5.3.1

* Tue Oct 06 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.0-27mdv2010.0
+ Revision: 454522
- P0: php-5.3.x fixes from upstream svn
- rebuilt against php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.0-26mdv2009.1
+ Revision: 346412
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.0-25mdv2009.1
+ Revision: 341501
- rebuilt against php-5.2.9RC2

* Wed Dec 31 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.0-24mdv2009.1
+ Revision: 321726
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.0-23mdv2009.1
+ Revision: 310212
- rebuilt against php-5.2.7

* Tue Jul 15 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.0-22mdv2009.0
+ Revision: 235811
- rebuild

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.0-20mdv2009.0
+ Revision: 200103
- rebuilt against php-5.2.6

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.0-19mdv2008.1
+ Revision: 161959
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.0-18mdv2008.1
+ Revision: 107558
- restart apache if needed

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.0-17mdv2008.0
+ Revision: 77451
- rebuilt against php-5.2.4

* Thu Aug 16 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.0-16mdv2008.0
+ Revision: 64295
- use the new %%serverbuild macro

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.0-15mdv2008.0
+ Revision: 39376
- use distro conditional -fstack-protector

* Fri Jun 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.0-14mdv2008.0
+ Revision: 33771
- rebuilt against new upstream version (5.2.3)

* Thu May 03 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.0-13mdv2008.0
+ Revision: 21020
- rebuilt against new upstream version (5.2.2)


* Thu Feb 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-12mdv2007.0
+ Revision: 117530
- rebuilt against new upstream version (5.2.1)

* Wed Nov 08 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.0-11mdv2007.0
+ Revision: 78141
- fix deps

* Tue Nov 07 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.0-10mdv2007.0
+ Revision: 77337
- rebuilt for php-5.2.0

* Thu Nov 02 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.0-9mdv2007.1
+ Revision: 75194
- Import php-dbx

* Mon Aug 28 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.0-9
- rebuilt for php-5.1.6

* Thu Jul 27 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.0-8mdk
- rebuild

* Sat May 06 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.0-7mdk
- rebuilt for php-5.1.4

* Fri May 05 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.0-6mdk
- rebuilt for php-5.1.3

* Thu Feb 02 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.0-5mdk
- new group (Development/PHP) and iurt rebuild

* Sun Jan 15 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.0-4mdk
- rebuilt against php-5.1.2

* Tue Nov 29 2005 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.0-3mdk
- rebuilt against php-5.1.1

* Sat Nov 26 2005 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.0-2mdk
- rebuilt against php-5.1.0

* Thu Nov 03 2005 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.0-1mdk
- rebuilt against php-5.1.0RC4
- fix versioning

* Sun Oct 30 2005 Oden Eriksson <oeriksson@mandriva.com> 5.1.0-0.RC1.2mdk
- rebuilt to provide a -debug package too

* Sun Oct 02 2005 Oden Eriksson <oeriksson@mandriva.com> 5.1.0_1.1.0-0.RC1.1mdk
- rebuilt against php-5.1.0RC1
- the source lives in pecl now

* Wed Sep 07 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.5-1mdk
- rebuilt against php-5.0.5 (Major security fixes)

* Fri May 27 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4-1mdk
- rename the package

* Sun Apr 17 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4-1mdk
- 5.0.4

* Sun Mar 20 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.3-4mdk
- use the %%mkrel macro

* Sat Feb 12 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.3-3mdk
- rebuilt against a non hardened-php aware php lib

* Sun Jan 16 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.3-2mdk
- rebuild due to hardened-php-0.2.6

* Fri Dec 17 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.3-1mdk
- rebuilt for php-5.0.3

* Sat Sep 25 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.2-1mdk
- rebuilt for php-5.0.2

* Sun Aug 15 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.1-1mdk
- rebuilt for php-5.0.1

* Wed Aug 11 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.0-1mdk
- rebuilt for php-5.0.0
- major cleanups

* Thu Jul 15 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.8-1mdk
- rebuilt for php-4.3.8

* Tue Jul 13 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.7-2mdk
- remove redundant provides

* Tue Jun 15 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.7-1mdk
- rebuilt for php-4.3.7

* Mon May 24 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.6-2mdk
- use the %%configure2_5x macro
- move scandir to /etc/php.d

* Thu May 06 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.6-1mdk
- built for php 4.3.6

