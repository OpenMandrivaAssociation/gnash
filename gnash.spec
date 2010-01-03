%if %mdkversion >= 200910
%define with_klash 1
%else
%define with_klash 0
%endif

%define with_gstreamer 0

%{?_with_klash: %{expand: %%global with_klash 1}}
%{?_with_gstreamer: %{expand: %%global with_gstreamer 1}}

%define libname %mklibname %{name} 0
%define libname_dev %mklibname -d %{name} 
%define libname_orig lib%{name}

%define bzr	20091231
%define rel	4
%define major	0

%if %bzr
%define release		%mkrel 0.%bzr.%rel
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
Summary: Gnash - a GNU Flash movie player
License: GPLv3
Group: Networking/WWW
Source0: %{distname}
Patch0: gnash-0.8.5-ignore-moc-output-version.patch
Patch1:	gnash-0.8.3-manual.patch
BuildRoot: %{_tmppath}/%{name}-root
URL: http://www.gnu.org/software/gnash/
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
Buildrequires:  netcat 
Buildrequires:  wget 
# (nl) : needed for the test-suite
BuildRequires:  ming-devel
BuildRequires:  ming-utils
BuildRequires:	speex-devel

%if %{with_gstreamer}
Requires:	gstreamer0.10-plugins-base
Requires:	gstreamer0.10-plugins-ugly
Requires:	gstreamer0.10-plugins-bad
Requires:	gstreamer0.10-ffmpeg
%endif

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
%{_bindir}/gprocessor
%{_bindir}/fb-gnash
%{_bindir}/gtk-gnash
%{_bindir}/sdl-gnash
%{_bindir}/soldumper
%{_bindir}/dumpshm
%{_bindir}/flvdumper
%if %{with_gstreamer}
%{_bindir}/findmicrophones
%{_bindir}/findwebcams
%endif
%{_mandir}/man1/gnash.1*
%{_mandir}/man1/dumpshm.1*
%{_mandir}/man1/gprocessor.1*
%{_mandir}/man1/soldumper.1*
%{_mandir}/man1/flvdumper.1*
%{_sysconfdir}/gnashrc
%{_sysconfdir}/gnashpluginrc
%{_datadir}/gnash

#--------------------------------------------------------------------

%package -n	%{libname}
Summary:	Gnash library
Group:	        Networking/WWW	
Provides:	%{libname_orig} = %{version}

%description -n %{libname}
Gnash library.

%files -n %{libname}
%defattr(-,root,root)
%dir %{_libdir}/gnash
%{_libdir}/gnash/libgnashbase.so.%{major}*
%{_libdir}/gnash/libgnashcore-trunk.so
%{_libdir}/gnash/libgnashamf-trunk.so
%{_libdir}/gnash/libgnashmedia-trunk.so
%{_libdir}/gnash/libgnashnet.so.%{major}*
%{_libdir}/gnash/libgnashsound-trunk.so
%{_libdir}/gnash/libmozsdk.so.%{major}*
%{_libdir}/gnash/plugins/*.so

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
%{_includedir}/gnash/*
%{_libdir}/gnash/libgnash*.la
%{_libdir}/gnash/libgnashamf.so
%{_libdir}/gnash/libgnashbase.so
%{_libdir}/gnash/libgnashcore.so
%{_libdir}/gnash/libgnashmedia.so
%{_libdir}/gnash/libgnashnet.so
%{_libdir}/gnash/libgnashsound.so
%{_libdir}/gnash/libmozsdk.la
%{_libdir}/gnash/libmozsdk.so
%{_libdir}/gnash/plugins/*.la
%{_libdir}/pkgconfig/gnash.pc
#--------------------------------------------------------------------

%package -n %{name}-firefox-plugin
Summary:	Gnash firefox plugin
Group:		Networking/WWW
Requires:	%{name} = %{version}-%{release}
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
Requires:	%{name} = %{version}-%{release}
%description -n %{name}-konqueror-plugin
Gnash Konqueror plugin

%files -n %{name}-konqueror-plugin
%{_kde_bindir}/kde4-gnash
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
