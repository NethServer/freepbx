%global debug_package %{nil}

Summary:	Asterisk FreePBX Web Interface
Name:		freepbx
Version:	14.0
Release:    	1%{dist}
License:    	GPL
Group:		System/Servers
Source0:	http://mirror.freepbx.org/modules/packages/freepbx/%{name}-%{version}-latest.tgz
Source1:	freepbx.service
Patch0:  	allow-php-5.6.5.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}
BuildArch: 	noarch
AutoReq:	no
Packager: 	Nethesis
URL:		http://www.freepbx.org/

Requires:	asterisk-core, kmod-dahdi-linux, dahdi-linux, dahdi-tools, dahdi-firmware, wanpipe
Requires:	httpd, mariadb, mariadb-server

Requires:       rh-php56, rh-php56-php-fpm
Requires:       rh-php56-php-mysql, rh-php56-php-pear, rh-php56-php-pdo
Requires:       rh-php56-php-process, rh-php56-php-xml, rh-php56-php-mbstring
Requires:       rh-php56-php-intl, rh-php56-php-ldap, rh-php56-php-odbc, rh-php56-php-gd

# Various packages required for FreePBX
Requires:	sudo, nodejs, icu,  net-tools, postfix, rsync, ghostscript, libtiff, unixODBC, mysql-connector-odbc
Requires:	libwat, libpri, libtonezone, libresample, libss7, libopenr2, icu, libicu-devel, tftp-server, whois, dos2unix
Requires:	sox, radiusclient-ng

# This is to make sure postfix can talk to TLS endpoints
Requires:	 cyrus-sasl-plain

#Requires:	libicu-devel

Provides:	perl(retrieve_parse_amportal_conf.pl)
Provides:	freepbx14,freepbx

%description
FreePBX is a GUI that gives you the ability to manage your Asterisk system.

%prep
rm -rf %{buildroot}

%setup -q -n %{name}
%patch0 -p1

%build

%install
%{__install} -d %{buildroot}/usr/src/%{name}-%{version}
cp -r * %{buildroot}/usr/src/%{name}-%{version}
mkdir -p %{buildroot}/etc/httpd/conf.d
mkdir -p %{buildroot}/lib/systemd/system
cp %{SOURCE1} %{buildroot}/lib/systemd/system

%pre
#only do on a new install
if [ $1 == 1 ]; then
	# Note that the Sangoma httpd rpm explicitly starts as the correct user.
	# This is OK in the chroot
	systemctl start asterisk

fi

%post

# Before we do anything, make sure we can write to the logfile
mkdir -p /var/log/asterisk
chown -R asterisk.asterisk /var/log/asterisk

#only do on a new install
if [ $1 == 1 ]; then

	mv -f /usr/src/%{name} /usr/src/%{name}.RPMSAVE
	ln -s /usr/src/%{name}-%{version} /usr/src/%{name}

	mkdir -p /etc/asterisk

	#new install call install
	echo " *** Installing FreePBX"
	echo " *** Installing FreePBX" >> /var/log/freepbx_rpm_install.log
	date >> /var/log/freepbx_rpm_install.log
	cd /usr/src/%{name}-%{version}
	./start_asterisk start &>> /var/log/freepbx_rpm_install.log

	# We also need to ensure that the database is up
	# This errors if it's run in the chroot
	CHROOT=`systemctl start mariadb 2>&1 | grep chroot`
	if [ "$CHROOT" != "" ]; then
		echo "Chroot detected, trying to start manually... " >> /var/log/freepbx_rpm_install.log
		# We errored, maria isn't started. Start it manually.
		chown -R mysql /var/lib/mysql
		/usr/bin/mysql_install_db --user=mysql &>> /var/log/freepbx_rpm_install.log
		nohup /usr/bin/mysqld_safe --basedir=/usr &>> /var/log/freepbx_rpm_install.log &
	fi

	# Make sure that the default mysql socket exists, and if it doesn't,
	# wait for it.
	while [ ! -e /var/lib/mysql/mysql.sock ]; do
		echo `date` "Socket file doesn't exists, waiting for it" &>> /var/lib/freepbx_rpm_install.log
		sleep 1
	done

	chmod 777 /var/log/asterisk/freepbx.log

	mkdir -p /var/lib/asterisk/sounds/custom/

	./install -n &>> /var/log/freepbx_rpm_install.log

	touch /var/log/asterisk/fail2ban
	touch /var/log/asterisk/freepbx_security.log
	touch /var/log/asterisk/cdr-csv/Master.csv
	chmod 777  /var/log/asterisk/cdr-csv/Master.csv
	chmod 755 /var/spool/asterisk/monitor
	/usr/sbin/fwconsole chown &>> /var/log/freepbx_rpm_install.log
	/usr/sbin/fwconsole r &>> /var/log/freepbx_rpm_install.log

	# Update php's max file size
	sed -i 's/\(^upload_max_filesize = \).*/\1256M/' /etc/php.ini

	echo " *** FreePBX installed!" &>> /var/log/freepbx_rpm_install.log

	mysql -N --batch asterisk -e 'select `data` from `module_xml` where `id`="randomid"' > /etc/asterisk/freepbx-id

	# We shutdown mysql here, in case we're still in the chroot.
	# If we're not in the chroot, we start it immediately after.
	/bin/mysqladmin shutdown

else
	echo "FreePBX has not been upgraded. Please upgrade FreePBX through Module Admin."
fi

# Always make sure that our required services are started and set to start automatically
for S in mariadb httpd dnsmasq freepbx; do
	systemctl enable $S &>> /var/log/freepbx_rpm_install.log || :
	systemctl start $S &>> /var/log/freepbx_rpm_install.log  || :
done

# Final file permissions cleanup
mkdir -p /var/log/pbx/install
mkdir -p /var/log/pbx/upgrade

echo "Final Chown start..." >> /var/log/freepbx_rpm_install.log
chown -R asterisk.asterisk /var/run/asterisk /var/log/pbx /var/lib/asterisk/sounds /etc/asterisk
chmod -R 755 /etc/asterisk
chmod 750 /etc/asterisk/keys
echo "Complete! RPM Successfully installed." >> /var/log/freepbx_rpm_install.log
date &>> /var/log/freepbx_rpm_install.log

%clean
rm -rf %{buildroot}

%files
/usr/src/%{name}-%{version}/*
/lib/systemd/system/freepbx.service
