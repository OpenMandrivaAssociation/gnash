# TODO
# Add a cvs switch
# Fix --enable-renderer=agg
# fix --enable-gui=fltk
####################################################

%define __libtoolize /bin/true
%define name	gnash
%define version 0.8.1
%define release %mkrel 1
#%define cvs     070802

%define libname %mklibname %{name} 0
%define libname_orig lib%{name}

Name:		%name
Summary:	Gnash - a GNU Flash movie player
Version:	%version
Release:	%release
License:	GPLv3
Group:		Networking/WWW
Source0:	%name-%version.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-root
URL:		http://www.gnu.org/software/gnash/
BuildRequires:	mesaglut-devel
BuildRequires:  mozilla-firefox-devel > 1.5
BuildRequires:  libgstreamer0.10-devel
BuildRequires:  SDL_mixer-devel
BuildRequires:  kdebase-devel
BuildRequires:  gtkglext-devel
BuildRequires:  boost-devel
BuildRequires:  curl-devel
BuildRequires:  docbook2x
BuildRequires:  texinfo
BuildRequires:  doxygen
BuildRequires:  scrollkeeper
BuildRequires:  slang-devel
BuildRequires:  libxslt-proc
BuildRequires:  agg-devel
BuildRequires:  MySQL-devel
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

%files -f %name.lang
%defattr(-,root,root,0755)
%doc AUTHORS COPYING ChangeLog ChangeLog.gameswf INSTALL NEWS README TODO
%{_bindir}/gnash
%{_bindir}/gparser
%{_bindir}/gprocessor
%{_bindir}/gtk-gnash
%{_mandir}/man?/*

%{_infodir}/%{name}.info.*
%{_infodir}/asspec.info.*
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
%{_libdir}/libgnashbackend-cvs.so
%{_libdir}/libgnashbase-cvs.so
%{_libdir}/libgnashgeo-cvs.so
%{_libdir}/libgnashserver-cvs.so
%{_libdir}/libgnashamf-cvs.so

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
%{_libdir}/libgnash*.la
%{_libdir}/libgnashamf.so
%{_libdir}/libgnashamf.a
%{_libdir}/libgnashbackend.so
%{_libdir}/libgnashbackend.a
%{_libdir}/libgnashbase.so
%{_libdir}/libgnashbase.a
%{_libdir}/libgnashgeo.so
%{_libdir}/libgnashgeo.a
%{_libdir}/libgnashserver.so
%{_libdir}/libgnashserver.a

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
%{_bindir}/kde-gnash
%{_libdir}/kde3/*.so
%{_libdir}/kde3/*.a
%{_libdir}/kde3/*.la
%{_datadir}/apps/klash
%{_datadir}/services/klash_part.desktop

#--------------------------------------------------------------------

%prep
%setup -q -n %name-%version
%build
sh autogen.sh
%configure	--enable-mp3 \
		--enable-ghelp  \
		--enable-docbook \
		--enable-plugin \
		--with-plugindir=%{_libdir}/mozilla/plugins  \
		--enable-media=gst \
		--disable-rpath \
		--enable-extensions \
		--enable-sdk-install \
		--enable-jpeg \
		--enable-ghelp \
		--enable-gui=gtk \
		--enable-sound=sdl \
		--with-qt-incl="`pkg-config --variable=includedir qt-mt`" \
		--with-qt-lib="`pkg-config --variable=libdir qt-mt`" \
                --enable-klash 

%make "OPENGL_LIBS = -lGL"


%install
rm -rf %{buildroot}


# Big fat but working hack
# perl -pi -e "s,install-info,/../sbin/install-info," doc/C/Makefile

%makeinstall_std
rm -rf %{buildroot}/%{_localstatedir}/scrollkeeper
perl -pi -e "s,-L%{_builddir}/%{name}-%{version}/libbase,,g" %{buildroot}/%{_libdir}/libgnashgeo.la

%find_lang %name

%clean
rm -rf %{buildroot}
