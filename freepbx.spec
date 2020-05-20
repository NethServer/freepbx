%global debug_package %{nil}

Summary:	Asterisk FreePBX Web Interface
Name:		freepbx
Version:	14.0
Release:	8%{dist}
License:    	GPL
Group:		System/Servers
Source0:	freepbx-14.0.13.12.tgz
Source1:	freepbx.service
Source2:	music.tar.gz
Source3:	dahdi-blacklist.conf
BuildRoot:	%{_tmppath}/%{name}-%{version}
BuildArch: 	noarch
AutoReq:	no
Packager: 	Nethesis
URL:		http://www.freepbx.org/

Requires:	asterisk13-core, asterisk13-addons-mysql, asterisk13-speex, asterisk13-voicemail-odbcstorage, asterisk13-resample, asterisk13-odbc
Requires:	asterisk-sounds-extra-en-ulaw
Requires:	kmod-dahdi-linux, dahdi-linux, dahdi-tools, dahdi-firmware
Requires:	httpd, mariadb, mariadb-server

Requires:   dahdi-tools-libs >= 2.11.1-16
Obsoletes:  libtonezone

Requires:   rh-php56, rh-php56-php-fpm
Requires:   rh-php56-php-mysql, rh-php56-php-pear, rh-php56-php-pdo
Requires:   rh-php56-php-process, rh-php56-php-xml, rh-php56-php-mbstring
Requires:   rh-php56-php-intl, rh-php56-php-ldap, rh-php56-php-odbc, rh-php56-php-gd

# Various packages required for FreePBX
Requires:	sudo, nodejs, icu,  net-tools, postfix, rsync, ghostscript, libtiff, unixODBC, mysql-connector-odbc
Requires:	libpri, libresample, libss7, libopenr2, icu, libicu-devel, tftp-server, whois, dos2unix
Requires:	sox, radiusclient-ng, mpg123

# This is to make sure postfix can talk to TLS endpoints
Requires:	cyrus-sasl-plain

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
mkdir -p %{buildroot}/usr/src/%{name}/amp_conf/moh
tar xzpf %{SOURCE2} -C %{buildroot}/usr/src/%{name}/amp_conf/moh
mkdir -p %{buildroot}/etc/modprobe.d
cp %{SOURCE3} %{buildroot}/etc/modprobe.d/dahdi-blacklist.conf

%pre

%post

%clean
rm -rf %{buildroot}

%files
/etc/modprobe.d/dahdi-blacklist.conf
/usr/src/%{name}/*
/lib/systemd/system/freepbx.service
