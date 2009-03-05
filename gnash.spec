#TODO: Do a switch for cvs use 

%define with_klash 0
%{?_with_klash: %{expand: %%global with_klash 1}}

%define libname %mklibname %{name} 0
%define libname_dev %mklibname -d %{name} 
%define libname_orig lib%{name}

Name: gnash
Version: 0.8.5
Release: %mkrel 1
Summary: Gnash - a GNU Flash movie player
License: GPLv3
Group: Networking/WWW
Source0: %name-%version.tar.bz2
Patch0: gnash-0.8.5-fix-underlinking.patch
BuildRoot: %{_tmppath}/%{name}-root
URL: http://www.gnu.org/software/gnash/
#BuildRequires:	mesaglut-devel
BuildRequires:  gstreamer0.10-devel
BuildRequires:  SDL_mixer-devel
%if %{with_klash}
BuildRequires:  kdebase3-devel
%endif
#BuildRequires:  gtkglext-devel
BuildRequires:  boost-devel
BuildRequires:  curl-devel
BuildRequires:  docbook2x
BuildRequires:	docbook-dtd412-xml
BuildRequires:  texinfo
BuildRequires:  doxygen
BuildRequires:  rarian
BuildRequires:  slang-devel
BuildRequires:  libxslt-proc
BuildRequires:  agg-devel
BuildRequires:  mysql-devel
BuildRequires:  libltdl-devel
Buildrequires:	gtk2-devel
Buildrequires:	dejagnu
# (nl) : needed for the test-suite
BuildRequires:  ming-devel
BuildRequires:  ming-utils
Requires:	gstreamer0.10-plugins-base
Requires:	gstreamer0.10-plugins-ugly
Requires:	gstreamer0.10-plugins-bad

%description
Gnash is capable of reading up to SWF v9 files and opcodes, but primarily
supports SWF v7, with better SWF v8 and v9 support under heavy development.
With the 0.8.2 release, Gnash includes initial parser support for SWF v8
and v9. Not all ActionScript 2 classes are implemented yet, but all of
the most heavily used ones are. Many ActionScript 2 classes are partially
implemented; there is support for all of the commonly used methods of each
class.

%post -n %{name}
%_install_info %{name}.info

%preun -n %{name}
%_remove_install_info %{name}.info

%files -f %name.lang
%defattr(-,root,root,0755)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README TODO
%{_bindir}/gnash
%{_bindir}/cygnal
%{_bindir}/gprocessor
%{_bindir}/fb-gnash
%{_bindir}/gtk-gnash
%{_bindir}/sdl-gnash
%{_bindir}/soldumper
%{_bindir}/dumpshm
%{_bindir}/flvdumper
%{_mandir}/man?/*
%_sysconfdir/gnashrc
%{_datadir}/gnash
%{_libdir}/gnash/plugins
%_sysconfdir/gnashpluginrc

#--------------------------------------------------------------------

%package -n	%{libname}
Summary:	Gnash library
Group:	        Networking/WWW	
Provides:	%{libname_orig} = %{version}

%description -n %{libname}
Gnash library.

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -n %{libname}
%defattr(-,root,root)
%dir %{_libdir}/gnash
%{_libdir}/gnash/libgnashbase-%{version}.so
%{_libdir}/gnash/libgnashcore-%{version}.so
%{_libdir}/gnash/libgnashamf-%{version}.so
%{_libdir}/gnash/libgnashmedia-%{version}.so
%{_libdir}/gnash/libgnashnet.so.0*
%{_libdir}/gnash/libgnashsound-%{version}.so
%{_libdir}/gnash/libmozsdk.la
%{_libdir}/gnash/libmozsdk.so.0*

#--------------------------------------------------------------------

%package -n	%{libname_dev}
Summary:	Headers of %name for development
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	%{libname_orig}-devel = %{version}-%{release}
Obsoletes: %{libname}-devel

%description -n %{libname_dev}
Headers of %{name} for development.

%files -n %{libname_dev}
%defattr(-,root,root)
%{_libdir}/gnash/libgnash*.la
%{_libdir}/gnash/libgnashamf.so
%{_libdir}/gnash/libgnashbase.so
%{_libdir}/gnash/libgnashcore.so
%{_libdir}/gnash/libgnashmedia.so
%{_libdir}/gnash/libgnashnet.so
%{_libdir}/gnash/libgnashsound.so
%{_libdir}/gnash/libmozsdk.so

#--------------------------------------------------------------------

%package -n %{name}-firefox-plugin
Summary:	Gnash firefox plugin
Group:		Networking/WWW
Requires:	gnash = %{version}
Requires:   firefox > 1.5	

%description -n %{name}-firefox-plugin
Gnash firefox plugin

%files -n %{name}-firefox-plugin
%{_libdir}/mozilla/plugins/*.so

#--------------------------------------------------------------------

%if %{with_klash}
%package -n	%{name}-konqueror-plugin
Summary:	Gnash konqueror plugin
Group:		Graphical desktop/KDE
Requires:	gnash = %{version}
%description -n %{name}-konqueror-plugin
Gnash Konqueror plugin

%files -n %{name}-konqueror-plugin
%{_kde3_bindir}/kde-gnash
#%{_kde3_datadir}/services/klash_part.desktop
%{_kde3_datadir}/apps/klash
#%{_kde3_libdir}/kde3/*
%endif

#--------------------------------------------------------------------

%prep
%setup -q -n %name-%version
%patch0 -p1 -b .link~

%build
QTDIR="%qt3dir" ; export QTDIR ;
PATH="%qt3dir/bin:$PATH" ; export PATH ;

sh autogen.sh
%define __libtoolize /bin/true

%configure --disable-static --with-npapi-plugindir=%{_libdir}/mozilla/plugins \
  --enable-extensions=ALL \
  --enable-docbook \
  --enable-ghelp \
  --disable-rpath \
  --enable-extensions=ALL \
  --enable-jpeg \
%if %{with_klash}
  --with-kparts-install=system \
  --enable-gui=gtk,kde,sdl,fb \
  --with-qtdir=$QTDIR \
  --with-kde-plugindir=%{_kde3_libdir}/kde3 \
  --with-kde-servicesdir=%{_kde3_datadir}/services \
  --with-kde-configdir=%{_kde3_datadir}/config \
  --with-kde-appsdatadir=%{_kde3_datadir}/apps/klash \
  --with-kde-incl=%{_kde3_includedir} \
  --with-kde-lib=%{_kde3_libdir} \
  --with-qt-incl=%qt3dir/include
%else
  --disable-kparts \
  --enable-gui=gtk,sdl,fb \
%endif
  --enable-media=GST \
  --disable-dependency-tracking \
  --disable-rpath \
  --enable-cygnal

%make



%install
strip gui/.libs/*-gnash utilities/.libs/dumpshm  utilities/.libs/g*  utilities/.libs/soldumper
rm -rf $RPM_BUILD_ROOT
make install install-plugins \
 DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p' \
 KDE_PLUGINDIR=%{__kde3_libdir}/kde3 \
 KDE_SERVICESDIR=%{__kde3datadir}/services \
 KDE_CONFIGDIR=%{__kde3_datadir}/config \
 KDE_APPSDATADIR=%{_kde3_datadir}/apps/klash

rm -rf %{buildroot}/%{_localstatedir}/lib/scrollkeeper
rm -rf %{buildroot}/%{_libdir}/mozilla/plugins/*.a
rm -rf %{buildroot}/%{_libdir}/mozilla/plugins/*.la

%if %{with_klash}
#(nl) Fix makefile to have it automacally done
%__mkdir -p %{buildroot}/%{_kde3_bindir}
%__mv %{buildroot}/%{_bindir}/kde-gnash %{buildroot}/%{_kde3_bindir}/kde-gnash
%endif

%find_lang %name

%clean
rm -rf %{buildroot}
