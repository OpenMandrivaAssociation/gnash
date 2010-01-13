%if %mdkversion >= 200910
%define with_klash 1
%else
%define with_klash 0
%endif

%define with_gstreamer 0
%define with_tests 0

%{?_with_klash: %{expand: %%global with_klash 1}}
%{?_with_gstreamer: %{expand: %%global with_gstreamer 1}}
%{?_with_gstreamer: %{expand: %%global with_tests 1}}

%define libname %mklibname %{name} 0
%define libname_dev %mklibname -d %{name} 
%define libname_orig lib%{name}

%define bzr	20100113
%define rel	1
%define major	0

%if %bzr
%define release		%mkrel -c %bzr %rel
%define distname	%name-%bzr.tar.xz
%define dirname		%name
%else
%define release		%mkrel %rel
%define distname	%name-%version.tar.bz2
%define dirname		%name-%version
%endif

Name: gnash
Version: 0.8.7
Release: %{release}
Summary: %{name} - a GNU Flash movie player
License: GPLv3
Group: Networking/WWW
Source0: %{distname}
Patch0: %{name}-0.8.5-ignore-moc-output-version.patch
Patch1:	%{name}-0.8.3-manual.patch
BuildRoot: %{_tmppath}/%{name}-root
URL: http://www.gnu.org/software/%{name}/
%if %{with_klash}
BuildRequires:  kdelibs4-devel
%endif
BuildRequires:  SDL_mixer-devel
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
%if %{with_gstreamer}
BuildRequires:  libgstreamer-plugins-base-devel
%else
BuildRequires:	ffmpeg-devel
%endif
BuildRequires:  csound-devel
Buildrequires:	dejagnu
BuildRequires:	speex-devel
%if %{with_tests}
BuildRequires:  ming-devel
BuildRequires:  ming-utils
Buildrequires:  netcat 
Buildrequires:  wget
%endif
%if %{with_gstreamer}
Requires:	gstreamer0.10-plugins-base
Requires:	gstreamer0.10-plugins-ugly
Requires:	gstreamer0.10-plugins-bad
Requires:	gstreamer0.10-ffmpeg
%endif

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
%{_bindir}/%{name}
%{_bindir}/gprocessor
%{_bindir}/fb-%{name}
%{_bindir}/gtk-%{name}
%{_bindir}/sdl-%{name}
%{_bindir}/soldumper
%{_bindir}/dumpshm
%{_bindir}/flvdumper
%if %{with_gstreamer}
%{_bindir}/findmicrophones
%{_bindir}/findwebcams
%endif
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/dumpshm.1*
%{_mandir}/man1/gprocessor.1*
%{_mandir}/man1/soldumper.1*
%{_mandir}/man1/flvdumper.1*
%{_sysconfdir}/%{name}rc
%{_sysconfdir}/%{name}pluginrc
%{_datadir}/%{name}

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
%{_libdir}/%{name}/lib%{name}agg.so.%{major}*
%{_libdir}/%{name}/lib%{name}base.so.%{major}*
%{_libdir}/%{name}/lib%{name}core-trunk.so
%{_libdir}/%{name}/lib%{name}amf-trunk.so
%{_libdir}/%{name}/lib%{name}media-trunk.so
%{_libdir}/%{name}/lib%{name}net.so.%{major}*
%{_libdir}/%{name}/lib%{name}sound-trunk.so
%{_libdir}/%{name}/libmozsdk.so.%{major}*
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
%{_libdir}/%{name}/lib%{name}agg.so
%{_libdir}/%{name}/lib%{name}amf.so
%{_libdir}/%{name}/lib%{name}base.so
%{_libdir}/%{name}/lib%{name}core.so
%{_libdir}/%{name}/lib%{name}media.so
%{_libdir}/%{name}/lib%{name}net.so
%{_libdir}/%{name}/lib%{name}sound.so
%{_libdir}/%{name}/libmozsdk.la
%{_libdir}/%{name}/libmozsdk.so
%{_libdir}/%{name}/plugins/*.la
%{_libdir}/pkgconfig/%{name}.pc
#--------------------------------------------------------------------

%package -n %{name}-firefox-plugin
Summary:	%{name} firefox plugin
Group:		Networking/WWW
Requires:	%{name} = %{version}-%{release}
Requires:   firefox > 1.5	

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
%{_mandir}/man1/rtmpget.1*
%dir %{_libdir}/cygnal
%{_libdir}/cygnal/plugins/*.so*

#--------------------------------------------------------------------

%prep
%setup -q -n %{dirname}
%patch0 -p1 -b .ignore~
%patch1 -p1 -b .manual~

%build
sh autogen.sh
%define _disable_ld_no_undefined 1

%configure2_5x --disable-static --with-npapi-plugindir=%{_libdir}/mozilla/plugins \
  --enable-extensions=ALL \
  --enable-docbook \
  --enable-ghelp \
  --disable-rpath \
%if %{with_klash}
  --enable-gui=gtk,kde4,sdl,fb \
%else
  --disable-kparts \
  --enable-gui=gtk,sdl,fb \
%endif
%if %{with_gstreamer}
  --enable-media=gst \
  --with-gstpbutils-incl=%{_includedir}/gstreamer-0.10 \
  --with-gstpbutils-lib=%{_libdir} \
%else
  --enable-media=ffmpeg \
%endif
  --enable-cygnal \
  --disable-dependency-tracking \
  --enable-avm2
  

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

rm -rf %{buildroot}/%{_localstatedir}/lib/scrollkeeper
rm -f %{buildroot}/%{_libdir}/mozilla/plugins/*.a
rm -f %{buildroot}/%{_libdir}/mozilla/plugins/*.la

%find_lang %name

%clean
rm -rf %{buildroot}
