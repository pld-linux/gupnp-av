#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
#
Summary:	Library for building UPnP A/V applications
Summary(pl.UTF-8):	Biblioteka do budowania aplikacji UPnP A/V
Name:		gupnp-av
Version:	0.5.6
Release:	2
License:	LGPL v2
Group:		Libraries
Source0:	http://www.gupnp.org/sources/gupnp-av/%{name}-%{version}.tar.gz
# Source0-md5:	31f53256eeb934dae26f86eac84145ff
URL:		http://www.gupnp.org/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gobject-introspection-devel >= 0.6.4
BuildRequires:	gssdp-devel >= 0.7.2
BuildRequires:	gtk-doc >= 1.0
BuildRequires:	gupnp-devel >= 0.13.4
BuildRequires:	libtool
BuildRequires:	pkgconfig
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
Requires:	gupnp-devel >= 0.13.4

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

%prep
%setup -q

%build
%{__gtkdocize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_apidocs:--enable-gtk-doc} \
	--with-html-dir=%{_gtkdocdir} \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

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

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgupnp-av-1.0.so
%{_libdir}/libgupnp-av-1.0.la
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
