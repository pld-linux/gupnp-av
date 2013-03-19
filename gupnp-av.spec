#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	vala		# Vala API
#
Summary:	Library for building UPnP A/V applications
Summary(pl.UTF-8):	Biblioteka do budowania aplikacji UPnP A/V
Name:		gupnp-av
# note: 0.12.x is stable, 0.13.x unstable
Version:	0.12.1
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gupnp-av/0.12/%{name}-%{version}.tar.xz
# Source0-md5:	2d15a94d743720febb400b2cacde1cdc
URL:		http://gupnp.org/
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	docbook-dtd412-xml
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	gtk-doc >= 1.10
BuildRequires:	gupnp-devel >= 0.19.0
BuildRequires:	libtool >= 2:2.2
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
%{?with_vala:BuildRequires:	vala >= 2:0.14}
%{?with_vala:BuildRequires:	vala-gupnp >= 0.19.0}
BuildRequires:	xz
Requires:	gupnp >= 0.19.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
gupnp-av is a small library that aims to easy the handling and
implementation of UPnP A/V profiles.

%description -l pl.UTF-8
gupnp-av jest małą biblioteką, której celem jest uproszczenie obsługi
i implementacji profili UPnP A/V.

%package devel
Summary:	Header files for gupnp-av library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki gupnp-av
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 2.0
Requires:	gupnp-devel >= 0.19.0
Requires:	libxml2-devel >= 2.0

%description devel
Header files for gupnp-av library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki gupnp-av.

%package static
Summary:	Static gupnp-av library
Summary(pl.UTF-8):	Statyczna biblioteka gupnp-av
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static gupnp-av library.

%description static -l pl.UTF-8
Statyczna biblioteka gupnp-av.

%package apidocs
Summary:	gupnp-av library API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki gupnp-av
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
API and internal documentation for gupnp-av library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki gupnp-av.

%package -n vala-gupnp-av
Summary:	Vala API for gupnp-av library
Summary(pl.UTF-8):	API języka Vala dla biblioteki gupnp-av
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala >= 2:0.14
Requires:	vala-gupnp >= 0.19.0

%description -n vala-gupnp-av
Vala API for gupnp-av library.

%description -n vala-gupnp-av -l pl.UTF-8
API języka Vala dla biblioteki gupnp-av.

%prep
%setup -q

%build
%{__gtkdocize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{?with_apidocs:--enable-gtk-doc} \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libgupnp-av-1.0.la

%{!?with_apidocs:rm -rf $RPM_BUILD_ROOT%{_gtkdocdir}}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libgupnp-av-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgupnp-av-1.0.so.2
%{_libdir}/girepository-1.0/GUPnPAV-1.0.typelib
%{_datadir}/gupnp-av

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgupnp-av-1.0.so
%{_datadir}/gir-1.0/GUPnPAV-1.0.gir
%{_includedir}/gupnp-av-1.0
%{_pkgconfigdir}/gupnp-av-1.0.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libgupnp-av-1.0.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gupnp-av
%endif

%if %{with vala}
%files -n vala-gupnp-av
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/gupnp-av-1.0.deps
%{_datadir}/vala/vapi/gupnp-av-1.0.vapi
%endif
