Summary:	BBClone - A PHP based Web Counter on Steroids
Summary(pl):	BBClone - oparty na PHP licznik stron WWW
Name:		bbclone
Version:	0.4.7
Release:	0.1
License:	GPL 2
Group:		Applications/WWW
Source0:	http://www.bbclone.de/download.php?get=%{name}-%{version}.tar.gz
# Source0-md5:	cc4141767818e75950f1dd5a56ec1201
Source1:	%{name}.conf
Source2:	%{name}.txt
Patch0:		%{name}-security.patch
URL:		http://www.bbclone.de/
Requires:	apache >= 1.3.33-2
Requires:	apache(mod_access)
Requires:	apache(mod_alias)
Requires:	php >= 4.1.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir		/usr/share/bbclone
%define		_sysconfdir	/etc/bbclone
%define		_vardir		/var/lib
%define		_apache1dir	/etc/apache
%define		_apache2dir	/etc/httpd

%description
BBclone is a web counter written in PHP and gives a detailed view
of the visitors of your web site by displaying the nth last users
(and the data they provided, like their IP, browser and so on) that
visited the web site, not just showing a number of visitors.
This is very handy for webmasters that want to see who is visiting
their sites, what browser people use, where they came from etc.

For each visitor, BBClone can display:
* IP address,
* hostname,
* operating system,
* robots,
* browser,
* referring URL (where do they come from),
* visit date,
* number of time the visitor has loaded the page,
* number of visitor,
* the visited pages in the order someone viewed them,
* the last visited page,
* the search engine query that lead to your site (if applicable),
* ranking of the most frequent countries, referrers, OS, browsers,
robots, page views and hostnames.

%description -l pl
BBclone to licznik WWW napisany w PHP. Udostêpnia szczegó³owy widok
odwiedzaj±cych stronê WWW wy¶wietlaj±c n-tych ostatnich u¿ytkowników
(oraz dostarczone przez nich dane, takie jak adres IP, przegl±darkê
itd.), którzy odwiedzili stronê, a nie tylko pokazuj±c liczbê go¶ci.
Jest to bardzo przydatne dla webmasterów, którzy chc± widzieæ, kto
odwiedza ich strony, jakich przegl±darek u¿ywaj±, sk±d pochodz± itp.

Dla ka¿dego odwiedzaj±cego BBClone mo¿e wy¶wietlaæ:
- adres IP,
- nazwê hosta,
- system operacyjny,
- roboty,
- przegl±darkê,
- URL odniesienia (sk±d wyst±pi³o odwo³anie),
- datê odwiedzin,
- czas potrzebny na za³adowanie strony,
- numer go¶cia,
- odwiedzone strony w kolejno¶ci ich ogl±dania,
- ostatni± odwiedzon± stronê,
- zapytanie silnika wyszukuj±cego, które zaprowadzi³o na stronê (je¶li
  dotyczy ¿±dania),
- ranking najczê¶ciej wystêpuj±cych krajów, odniesieñ, systemów
  operacyjnych, przegl±darek, robotów, stron i nazw hostów.

%prep
%setup -q -n %{name}
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir} \
	$RPM_BUILD_ROOT%{_vardir}/%{name} \
	$RPM_BUILD_ROOT%{_appdir}/{doc,images,ip2ext,language,lib}

cp -pR	*.php                      $RPM_BUILD_ROOT%{_appdir}

cp -pR  images/*                   $RPM_BUILD_ROOT%{_appdir}/images
cp -pR  ip2ext/*                   $RPM_BUILD_ROOT%{_appdir}/ip2ext
cp -pR  language/*                 $RPM_BUILD_ROOT%{_appdir}/language
cp -pR  lib/*                      $RPM_BUILD_ROOT%{_appdir}/lib

cp -pR	conf/*                     $RPM_BUILD_ROOT%{_sysconfdir}
cp -pR	var/*                      $RPM_BUILD_ROOT%{_vardir}/%{name}
cp -pR	var/.htalock               $RPM_BUILD_ROOT%{_vardir}/%{name}

ln -s %{_sysconfdir}               $RPM_BUILD_ROOT%{_appdir}/conf
ln -s %{_vardir}/%{name}           $RPM_BUILD_ROOT%{_appdir}/var

install %{SOURCE1}                 $RPM_BUILD_ROOT%{_sysconfdir}/apache-%{name}.conf
install %{SOURCE2}                 $RPM_BUILD_ROOT%{_appdir}/example.txt

%clean
rm -rf $RPM_BUILD_ROOT

%post
# apache1
if [ -d %{_apache1dir}/conf.d ]; then
	ln -sf %{_sysconfdir}/apache-%{name}.conf %{_apache1dir}/conf.d/99_%{name}.conf
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi
# apache2
if [ -d %{_apache2dir}/httpd.conf ]; then
	ln -sf %{_sysconfdir}/apache-%{name}.conf %{_apache2dir}/httpd.conf/99_%{name}.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%postun
if [ "$1" = "0" ]; then
	# apache1
	if [ -d %{_apache1dir}/conf.d ]; then
		rm -f %{_apache1dir}/conf.d/99_%{name}.conf
		if [ -f /var/lock/subsys/apache ]; then
			/etc/rc.d/init.d/apache restart 1>&2
		fi
	fi
	# apache2
	if [ -d %{_apache2dir}/httpd.conf ]; then
		rm -f %{_apache2dir}/httpd.conf/99_%{name}.conf
		if [ -f /var/lock/subsys/httpd ]; then
			/etc/rc.d/init.d/httpd restart 1>&2
		fi
	fi
fi

%files
%defattr(644,root,root,755)
%doc doc/*
%attr(750,root,http) %dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache-%{name}.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config.php
%dir %{_vardir}/%{name}
%attr(660,root,http) %{_vardir}/%{name}/*.php
%attr(660,root,http) %{_vardir}/%{name}/*.inc
%attr(660,root,http) %{_vardir}/%{name}/.htalock

%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/example.txt
%{_appdir}/conf
%{_appdir}/images
%{_appdir}/ip2ext
%{_appdir}/language
%{_appdir}/lib
%{_appdir}/var
