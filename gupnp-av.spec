#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	vala		# Vala API

Summary:	Library for building UPnP A/V applications
Summary(pl.UTF-8):	Biblioteka do budowania aplikacji UPnP A/V
Name:		gupnp-av
# note: 0.14.x is stable, 0.15.x unstable
Version:	0.14.4
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	https://download.gnome.org/sources/gupnp-av/0.14/%{name}-%{version}.tar.xz
# Source0-md5:	dd1b780fe9f5c138c722be428bf487b3
URL:		https://wiki.gnome.org/Projects/GUPnP
BuildRequires:	docbook-dtd412-xml
%{?with_apidocs:BuildRequires:	gi-docgen >= 2021.1}
BuildRequires:	glib2-devel >= 1:2.58
BuildRequires:	gobject-introspection-devel >= 1.36.0
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	meson >= 0.58.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	tar >= 1:1.22
%{?with_vala:BuildRequires:	vala >= 2:0.22}
BuildRequires:	xz
Requires:	glib2 >= 1:2.58
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
Requires:	glib2-devel >= 1:2.58
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
BuildArch:	noarch

%description apidocs
API and internal documentation for gupnp-av library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki gupnp-av.

%package -n vala-gupnp-av
Summary:	Vala API for gupnp-av library
Summary(pl.UTF-8):	API języka Vala dla biblioteki gupnp-av
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala >= 2:0.22
BuildArch:	noarch

%description -n vala-gupnp-av
Vala API for gupnp-av library.

%description -n vala-gupnp-av -l pl.UTF-8
API języka Vala dla biblioteki gupnp-av.

%prep
%setup -q

%build
%meson \
	%{?with_apidocs:-Dgtk_doc=true} \
	%{!?with_vala:-Dvapi=false}

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_gidocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/gupnp-av-1.0 $RPM_BUILD_ROOT%{_gidocdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README.md
%attr(755,root,root) %{_libdir}/libgupnp-av-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgupnp-av-1.0.so.3
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
%{_gidocdir}/gupnp-av-1.0
%endif

%if %{with vala}
%files -n vala-gupnp-av
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/gupnp-av-1.0.deps
%{_datadir}/vala/vapi/gupnp-av-1.0.vapi
%endif
