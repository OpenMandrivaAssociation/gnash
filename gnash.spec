%define libname %mklibname %{name} 0
%define libname_dev %mklibname -d %{name} 
%define libname_orig lib%{name}

Name: gnash
Version: 0.8.2
Release: %mkrel 2
Summary: Gnash - a GNU Flash movie player
License: GPLv3
Group: Networking/WWW
Source0: %name-%version.tar.bz2
BuildRoot: %{_tmppath}/%{name}-root
URL: http://www.gnu.org/software/gnash/
BuildRequires:	mesaglut-devel
BuildRequires:  mozilla-firefox-devel > 1.5
BuildRequires:  libgstreamer0.10-devel
BuildRequires:  SDL_mixer-devel
BuildRequires:  kdebase-devel
BuildRequires:  gtkglext-devel
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
BuildRequires:  MySQL-devel
BuildRequires:  libltdl-devel
Buildrequires:	gtk2-devel
Buildrequires:	dejagnu
# (nl) : needed for the test-suite
BuildRequires:  ming-devel

Requires:	gstreamer0.10-plugins-base
Requires:	gstreamer0.10-plugins-ugly
Requires:	gstreamer0.10-plugins-bad

%description
Gnash is a GNU Flash movie player. Till now it has been possible 
to play flash movies with proprietary software. While there are a 
few free flash players, none supports anything higher than SWF v4 
at best. Gnash is based on GameSWF, and supports many SWF v7 features.

%post -n %{name}
%_install_info %{name}.info

%preun -n %{name}
%_remove_install_info %{name}.info

%files -f %name.lang
%defattr(-,root,root,0755)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README TODO
%{_bindir}/gnash
%{_bindir}/gprocessor
%{_bindir}/gtk-gnash
%{_bindir}/soldumper
%{_bindir}/dumpshm
%{_mandir}/man?/*
#%{_infodir}/%{name}.info.*
#%{_datadir}/omf/gnash
%{_datadir}/gnash

#--------------------------------------------------------------------

%package -n	%{libname}
Summary:	Gnash library
Group:	        Networking/WWW	
Provides:	%{libname_orig} = %{version}

%description -n %{libname}
Gnash library.

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/gnash/libgnashbase-%{version}.so
%{_libdir}/gnash/libgnashserver-%{version}.so
%{_libdir}/gnash/libgnashamf-%{version}.so
%{_libdir}/gnash/libgnashmedia-%{version}.so

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
%{_libdir}/gnash/libgnashamf.a
%{_libdir}/gnash/libgnashbase.so
%{_libdir}/gnash/libgnashbase.a
%{_libdir}/gnash/libgnashserver.so
%{_libdir}/gnash/libgnashserver.a
%{_libdir}/gnash/libgnashmedia.so
%{_libdir}/gnash/libgnashmedia.a

#--------------------------------------------------------------------

%package -n %{name}-firefox-plugin
Summary:	Gnash firefox plugin
Group:		Networking/WWW
Requires:	gnash = %{version}
Requires:	libmozilla-firefox > 1.5

%description -n %{name}-firefox-plugin
Gnash firefox plugin

%files -n %{name}-firefox-plugin
%{_libdir}/mozilla/plugins/*.so


#--------------------------------------------------------------------

%package -n	%{name}-konqueror-plugin
Summary:	Gnash konqueror plugin
Group:		Graphical desktop/KDE
Requires:	gnash = %{version}
%description -n %{name}-konqueror-plugin
Gnash Konqueror plugin

%files -n %{name}-konqueror-plugin
%{_bindir}/kde-gnash
%{_datadir}/apps/klash/pluginsinfo
%{_datadir}/services/klash_part.desktop
%{_datadir}/apps/klash
%{_libdir}/kde3/*
%exclude %{_libdir}/kde3/*.a

#--------------------------------------------------------------------

%prep
%setup -q -n %name-%version

%build
QTDIR="/usr/lib/qt3" ; export QTDIR ;
PATH="/usr/lib/qt3/bin:$PATH" ; export PATH ;

sh autogen.sh
%configure	\
		--enable-mp3 \
		--enable-ghelp  \
		--enable-docbook \
		--enable-plugin \
		--with-npapi-plugindir=%{_libdir}/mozilla/plugins  \
		--enable-media=gst \
		--disable-rpath \
		--enable-extensions \
		--enable-sdk-install \
		--enable-jpeg \
		--enable-ghelp \
		--enable-sound=sdl \
		--enable-klash \
		--enable-render=agg

%make "OPENGL_LIBS = -lGL"

%install
#%makeinstall_std install-plugin
strip gui/.libs/*-gnash utilities/.libs/dumpshm  utilities/.libs/g*  utilities/.libs/soldumper
rm -rf $RPM_BUILD_ROOT
make install install-plugins DESTDIR=$RPM_BUILD_ROOT

rm -rf %{buildroot}/%{_localstatedir}/scrollkeeper
rm -rf %{buildroot}/%{_libdir}/mozilla/plugins/*.a
rm -rf %{buildroot}/%{_libdir}/mozilla/plugins/*.la

%find_lang %name

%clean
rm -rf %{buildroot}
