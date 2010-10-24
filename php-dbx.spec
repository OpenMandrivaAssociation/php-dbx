%define modname dbx
%define dirname %{modname}
%define soname %{modname}.so
%define inifile 16_%{modname}.ini

Summary:	DBX extension module for PHP
Name:		php-%{modname}
Version:	1.1.0
Release:	%mkrel 31
Group:		Development/PHP
URL:		http://www.php.net
License:	PHP License
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tar.bz2
Source1:	%{modname}.ini
Patch0:		dbx-1.1.0-php530.diff
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

%patch0 -p1

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
