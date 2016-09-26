%global debug_package %{nil}

Summary:	Asterisk FreePBX Web Interface
Name:		freepbx
Version:	14.0
Release:    	2%{dist}
License:    	GPL
Group:		System/Servers
Source0:	http://mirror.freepbx.org/modules/packages/freepbx/%{name}-%{version}-latest.tgz
Source1:	freepbx.service
BuildRoot:	%{_tmppath}/%{name}-%{version}
BuildArch: 	noarch
AutoReq:	no
Packager: 	Nethesis
URL:		http://www.freepbx.org/

Requires:	asterisk-core, kmod-dahdi-linux, dahdi-linux, dahdi-tools, dahdi-firmware, wanpipe, asterisk-addons-mysql, asterisk-speex asterisk-voicemail-odbcstorage asterisk-resample
Requires:	httpd, mariadb, mariadb-server

Requires:   rh-php56, rh-php56-php-fpm
Requires:   rh-php56-php-mysql, rh-php56-php-pear, rh-php56-php-pdo
Requires:   rh-php56-php-process, rh-php56-php-xml, rh-php56-php-mbstring
Requires:   rh-php56-php-intl, rh-php56-php-ldap, rh-php56-php-odbc, rh-php56-php-gd

# Various packages required for FreePBX
Requires:	sudo, nodejs, icu,  net-tools, postfix, rsync, ghostscript, libtiff, unixODBC, mysql-connector-odbc
Requires:	libwat, libpri, libtonezone, libresample, libss7, libopenr2, icu, libicu-devel, tftp-server, whois, dos2unix
Requires:	sox, radiusclient-ng

# This is to make sure postfix can talk to TLS endpoints
Requires:	cyrus-sasl-plain

Requires:	nethserver-mysql

#Requires:	libicu-devel

Provides:	perl(retrieve_parse_amportal_conf.pl)
Provides:	freepbx14,freepbx

%description
FreePBX is a GUI that gives you the ability to manage your Asterisk system.

%prep
rm -rf %{buildroot}

%setup -q -n %{name}

%build

%install
%{__install} -d %{buildroot}/usr/src/%{name}
cp -r * %{buildroot}/usr/src/%{name}
mkdir -p %{buildroot}/etc/httpd/conf.d
mkdir -p %{buildroot}/lib/systemd/system
cp %{SOURCE1} %{buildroot}/lib/systemd/system

%pre

%post

%clean
rm -rf %{buildroot}

%files
/usr/src/%{name}/*
/lib/systemd/system/freepbx.service
