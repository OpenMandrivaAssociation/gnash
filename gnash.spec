%if %mdkversion >= 200910
%define with_klash 1
%else
%define with_klash 0
%endif

%define with_tests 0

%{?_with_klash: %{expand: %%global with_klash 1}}
%{?_with_gstreamer: %{expand: %%global with_gstreamer 1}}
%{?_with_gstreamer: %{expand: %%global with_tests 1}}

%define libname %mklibname %{name} 0
%define libname_dev %mklibname -d %{name} 
%define libname_orig lib%{name}

%define bzr	0
%define rel	2
%define major	0

%if %bzr
%define release		%mkrel -c %bzr %rel
%define distname	%name-%bzr.tar.xz
%define dir_name	%name
%define buildversion	trunk
%else
%define release		%mkrel %rel
%define distname	%name-%version.tar.bz2
%define dir_name	%name-%version
%define buildversion	%version
%endif

Name: gnash
Version: 0.8.8
Release: %{release}
Summary: %{name} - a GNU Flash movie player
License: GPLv3
Group: Networking/WWW
Source0: %{distname}
Source1: http://www.getgnash.org/gnash-splash.swf
Patch1:	%{name}-0.8.3-manual.patch
BuildRoot: %{_tmppath}/%{name}-root
URL: http://www.gnu.org/software/%{name}/
%if %{with_klash}
BuildRequires:  kdelibs4-devel
%endif
BuildRequires:  SDL_mixer-devel
BuildRequires:  boost-devel
BuildRequires:  curl-devel
#BuildRequires:  docbook2x
#BuildRequires:	docbook-dtd412-xml
#BuildRequires:  texinfo
BuildRequires:  doxygen
BuildRequires:  rarian
BuildRequires:  slang-devel
BuildRequires:  libxslt-proc
BuildRequires:  agg-devel
BuildRequires:  mysql-devel
BuildRequires:  libltdl-devel
BuildRequires:	gtk2-devel
BuildRequires:	libts-devel
BuildRequires:	libgtkglext-devel
BuildRequires:	gsm-devel
BuildRequires:	nspr-devel
BuildRequires:	expat-devel
BuildRequires:  libgstreamer-plugins-base-devel
BuildRequires:	ffmpeg-devel
BuildRequires:  csound-devel
Buildrequires:	dejagnu
BuildRequires:	speex-devel
BuildRequires:	libxi-devel
%if %{with_tests}
BuildRequires:  ming-devel >= 0.4.3
BuildRequires:  ming-utils >= 0.4.3
Buildrequires:  netcat 
Buildrequires:  wget
%endif
Requires:	gstreamer0.10-plugins-base
Requires:	gstreamer0.10-plugins-ugly
Requires:	gstreamer0.10-plugins-bad
Requires:	gstreamer0.10-ffmpeg
Suggests:	lightspark

%description
%{name} is capable of reading up to SWF v9 files and opcodes, but primarily
supports SWF v7, with better SWF v8 and v9 support under heavy development.
With the 0.8.2 release, %{name} includes initial parser support for SWF v8
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
%config(noreplace) %{_sysconfdir}/%{name}pluginrc
%config(noreplace) %{_sysconfdir}/%{name}rc
%{_bindir}/%{name}
%{_bindir}/fb-%{name}
%{_bindir}/gtk-%{name}
%{_bindir}/sdl-%{name}
%{_bindir}/findmicrophones
%{_bindir}/findwebcams
%{_mandir}/man1/findmicrophones.1.*
%{_mandir}/man1/findwebcams.1.*
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/gtk-%{name}.1*
%{_datadir}/%{name}
%{_datadir}/icons/hicolor/32x32/apps/*.png
%{_datadir}/applications/mandriva-%{name}.desktop

#--------------------------------------------------------------------

%package -n	%{libname}
Summary:	%{name} library
Group:	        Networking/WWW	
Provides:	%{libname_orig} = %{version}

%description -n %{libname}
%{name} library.

%files -n %{libname}
%defattr(-,root,root)
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/lib%{name}render.so.%{major}*
%{_libdir}/%{name}/lib%{name}base-%{buildversion}.so
%{_libdir}/%{name}/lib%{name}core-%{buildversion}.so
%{_libdir}/%{name}/lib%{name}amf-%{buildversion}.so
%{_libdir}/%{name}/lib%{name}media-%{buildversion}.so
%{_libdir}/%{name}/lib%{name}net.so.%{major}*
%{_libdir}/%{name}/lib%{name}sound-%{buildversion}.so
%{_libdir}/%{name}/lib%{name}vaapi-%{buildversion}.so
%{_libdir}/%{name}/plugins/*.so

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
%{_includedir}/%{name}/*
%{_libdir}/%{name}/lib%{name}*.la
%{_libdir}/%{name}/lib%{name}render.so
%{_libdir}/%{name}/lib%{name}amf.so
%{_libdir}/%{name}/lib%{name}base.so
%{_libdir}/%{name}/lib%{name}core.so
%{_libdir}/%{name}/lib%{name}media.so
%{_libdir}/%{name}/lib%{name}net.so
%{_libdir}/%{name}/lib%{name}sound.so
%{_libdir}/%{name}/lib%{name}vaapi.so
%{_libdir}/%{name}/plugins/*.la
%{_libdir}/pkgconfig/%{name}.pc
#--------------------------------------------------------------------

%package -n %{name}-firefox-plugin
Summary:	%{name} firefox plugin
Group:		Networking/WWW
Requires:	%{name} = %{version}-%{release}

%description -n %{name}-firefox-plugin
%{name} firefox plugin

%files -n %{name}-firefox-plugin
%{_libdir}/mozilla/plugins/*.so

#--------------------------------------------------------------------

%if %{with_klash}
%package -n	%{name}-konqueror-plugin
Summary:	%{name} konqueror plugin
Group:		Graphical desktop/KDE
Requires:	%{name} = %{version}-%{release}
%description -n %{name}-konqueror-plugin
%{name} Konqueror plugin

%files -n %{name}-konqueror-plugin
%{_kde_bindir}/kde4-%{name}
%{_kde_libdir}/kde4/libklashpart.la
%{_kde_libdir}/kde4/libklashpart.so
%{_kde_datadir}/kde4/services/klash_part.desktop
%{_kde_datadir}/apps/klash/
%{_mandir}/man1/kde4-%{name}.1*
%endif

#--------------------------------------------------------------------

%package cygnal
Summary:   Streaming media server
Requires:  %{name} = %{version}-%{release}
Group:     System/Servers 

%description cygnal
Cygnal is a streaming media server that's Flash aware.

%files cygnal
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/cygnalrc
%{_bindir}/cygnal
%{_mandir}/man1/cygnal.1*
%dir %{_libdir}/cygnal
%{_libdir}/cygnal/plugins/*.so*

#--------------------------------------------------------------------

%package tools
Summary:   gnash tools
Requires:  %{name} = %{version}-%{release}
Group:     Video 

%description tools
Gnash tools.

%files tools
%defattr(-,root,root,-)
%{_bindir}/gprocessor
%{_bindir}/soldumper
%{_bindir}/flvdumper
%{_bindir}/rtmpget
%{_mandir}/man1/gprocessor.1*
%{_mandir}/man1/soldumper.1*
%{_mandir}/man1/flvdumper.1*
%{_mandir}/man1/rtmpget.1*

#--------------------------------------------------------------------

%prep
%setup -q -n %{dir_name}
%patch1 -p1 -b .manual~

%build
./autogen.sh
%define _disable_ld_no_undefined 0

%configure2_5x --disable-static --with-npapi-plugindir=%{_libdir}/mozilla/plugins \
  --enable-extensions=ALL \
  --enable-ghelp \
  --disable-rpath \
%if %{with_klash}
  --enable-gui=gtk,kde4,sdl,fb \
%else
  --disable-kparts \
  --enable-gui=gtk,sdl,fb \
%endif
%if %{with_tests}
  --enable-testsuite \
%else
  --disable-testsuite \
%endif
  --enable-media=ffmpeg,gst \
  --with-gstpbutils-incl=%{_includedir}/gstreamer-0.10 \
  --with-gstpbutils-lib=%{_libdir} \
  --enable-cygnal \
  --disable-dependency-tracking \
  --enable-doublebuf
  #--enable-docbook
   

%make

%if %{with_tests}
%make check
%endif

%install
rm -rf %{buildroot}
make install install-plugins \
 DESTDIR=%{buildroot} INSTALL='install -p' \
 KDE4_PLUGINDIR=%{_kde_libdir}/kde4 \
 KDE4_SERVICESDIR=%{_kde_datadir}/kde4/services \
 KDE4_CONFIGDIR=%{_kde_configdir} \
 KDE4_APPSDATADIR=%{_kde_appsdir}/klash

cp -p %{SOURCE1} %{buildroot}%{_datadir}/%{name}/

#menu entry
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Gnash SWF Viewer
GenericName=SWF Viewer
Comment=%{summary}
Exec=%{name} %{_datadir}/%{name}/%{name}-splash.swf %U
Icon=GnashG
Terminal=false
Type=Application
StartupNotify=false
Categories=AudioVideo;GTK;Video;Player;
MimeType=application/x-shockwave-flash;application/futuresplash;
EOF

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
cp -p ./gui/images/GnashG.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps


rm -rf %{buildroot}/%{_localstatedir}/lib/scrollkeeper
rm -f %{buildroot}/%{_libdir}/mozilla/plugins/*.a
rm -f %{buildroot}/%{_libdir}/mozilla/plugins/*.la

%find_lang %name

%clean
rm -rf %{buildroot}
