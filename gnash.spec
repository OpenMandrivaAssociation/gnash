# TODO
# Add a cvs switch
# Fix --enable-renderer=agg
# fix --enable-gui=fltk
####################################################

%define __libtoolize /bin/true
%define name	gnash
%define version 0.7.3
%define release %mkrel 0.%cvs.3

%define cvs     070501

%define libname %mklibname %{name} 0
%define libname_orig lib%{name}

Name:		%name
Summary:	Gnash - a GNU Flash movie player
Version:	%version
Release:	%release
License:	GPL
Group:		Networking/WWW
Source0:	%name-%cvs.tar.bz2
Patch0:         gnash-gcc-warning-fixes.diff
BuildRoot:	%{_tmppath}/%{name}-root
URL:		http://www.gnu.org/software/gnash/
BuildRequires:	mesaglut-devel
BuildRequires:  mozilla-firefox-devel > 1.5
BuildRequires:  mad-devel
BuildRequires:  SDL_mixer-devel
BuildRequires:  kdebase-devel
BuildRequires:  gtkglext-devel
BuildRequires:  boost-devel
BuildRequires:  curl-devel
BuildRequires:  docbook2x
BuildRequires:  texinfo
BuildRequires:  doxygen
BuildRequires:	scrollkeeper
BuildRequires:	libxslt-proc
BuildRequires:  agg-devel
BuildRequires:  mysql-devel
BuildRequires:  libltdl-devel
Buildrequires:	gtk2-devel
Buildrequires:	dejagnu
# (nl) : needed for the test-suite
BuildRequires:  ming-devel

%description
Gnash is a GNU Flash movie player. Till now it has been possible 
to play flash movies with proprietary software. While there are a 
few free flash players, none supports anything higher than SWF v4 
at best. Gnash is based on GameSWF, and supports many SWF v7 features.

%post -n %{name}
%_install_info %{name}.info

%preun -n %{name}
%_remove_install_info %{name}.info

%files
%defattr(-,root,root,0755)
%doc AUTHORS COPYING ChangeLog ChangeLog.gameswf INSTALL NEWS README TODO
%{_bindir}/gnash
%{_bindir}/gparser
%{_bindir}/gprocessor
%{_bindir}/cygnal
%{_mandir}/man?/*

%{_infodir}/%{name}.info.bz2
%{_infodir}/asspec.info.bz2
%{_datadir}/omf/gnash
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
%{_libdir}/libgnashamf-cvs20070502.so
%{_libdir}/libgnashasobjs-cvs20070502.so
%{_libdir}/libgnashbackend-cvs20070502.so
%{_libdir}/libgnashbase-cvs20070502.so
%{_libdir}/libgnashgeo-cvs20070502.so
%{_libdir}/libgnashgui-cvs20070502.so
%{_libdir}/libgnashparser-cvs20070502.so
%{_libdir}/libgnashparser.so
%{_libdir}/libgnashplayer-cvs20070502.so
%{_libdir}/libgnashserver-cvs20070502.so
%{_libdir}/libgnashvm-cvs20070502.so
%{_libdir}/libgnashamf.so
%{_libdir}/libgnashbackend.so
%{_libdir}/libgnashbase.so
%{_libdir}/libgnashgeo.so
%{_libdir}/libgnashgui.so
%{_libdir}/libgnashplayer.so
%{_libdir}/libgnashserver.so
%{_libdir}/libgnashvm.so

#--------------------------------------------------------------------

%package -n	%{libname}-devel
Summary:	Headers of %name for development
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	%{libname_orig}-devel = %{version}-%{release}

%description -n %{libname}-devel
Headers of %{name} for development.

%files -n %{libname}-devel
%defattr(-,root,root)
%{_libdir}/libgnashasobjs.la
%{_libdir}/libgnashamf.la
%{_libdir}/libgnashvm.la
%{_libdir}/libgnashbackend.la
%{_libdir}/libgnashplayer.la
%{_libdir}/libgnashbase.la
%{_libdir}/libgnashgeo.la
%{_libdir}/libgnashgui.la
%{_libdir}/libgnashserver.la
%{_libdir}/kde3/libklashpart.la
%{_libdir}/libgnashparser.la

#--------------------------------------------------------------------

%package -n     %{name}-firefox-plugin
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
%{_libdir}/kde3/*.so
%{_datadir}/apps/klash
%{_datadir}/services/klash_part.desktop

#--------------------------------------------------------------------

%prep
%setup -q -n %name
#%patch0

%build
sh autogen.sh
%configure2_5x	--enable-mp3 \
		--enable-ghelp  \
		--enable-docbook \
		--enable-plugin \
		--with-plugindir=%{_libdir}/mozilla/plugins  \
		--disable-rpath \
		--enable-extensions \
		--enable-sdk-install \
		--enable-jpeg \
		--enable-ghelp \
		--enable-klash \
		--enable-gui=gtk \
		--enable-sound=sdl \
		--with-qt-incl="`pkg-config --variable=includedir qt-mt`" \
		--with-qt-lib="`pkg-config --variable=libdir qt-mt`"

%make "OPENGL_LIBS = -lGL"


%install
rm -rf %{buildroot}


# Big fat but working hack
perl -pi -e "s,install-info,/../sbin/install-info," doc/C/Makefile

%makeinstall_std
rm -rf %{buildroot}/%{_localstatedir}/scrollkeeper
perl -pi -e "s,-L%{_builddir}/%{name}-%{version}/libbase,,g" %{buildroot}/%{_libdir}/libgnashgeo.la

#drop devel files
#rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
#rm -f $RPM_BUILD_ROOT%{_libdir}/gnash/plugins/*.la
#rm -f $RPM_BUILD_ROOT%{_libdir}/kde3/*.la

%clean
rm -rf %{buildroot}




