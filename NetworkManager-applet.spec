%define		orgname	network-manager-applet

Summary:	NetworkManager applet for GNOME
Name:		NetworkManager-applet
Version:	0.9.8.10
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/network-manager-applet/0.9/%{orgname}-%{version}.tar.xz
# Source0-md5:	5148348c139229c6a753f815f3f11e1c
BuildRequires:	NetworkManager-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	gnome-bluetooth-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk+3-devel
BuildRequires:	libgnome-keyring-devel
BuildRequires:	libnotify-devel
BuildRequires:	pkg-config
BuildRequires:	polkit-devel
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	glib-gio-gsettings
Requires:       %{name}-libs = %{version}-%{release}
Requires:	NetworkManager
Requires:	xdg-desktop-notification-daemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/NetworkManager

%description
Network Manager applet for GNOME.

%package libs
Summary:        GTK+ dialogs library for NetworkManager
Group:          Development/Libraries

%description libs
GTK+ dialogs library for NetworkManager.

%package devel
Summary:        Development files for nm-gtk library
Group:          X11/Development/Libraries
Requires:       %{name}-libs = %{version}-%{release}

%description devel
Development files for nm-gtk library.

%package -n gnome-bluetooth-plugin-network-manager
Summary:	GNOME Bluetooth plugin
Group:		Applications
Requires:	%{name} = %{version}-%{release}
Requires:	gnome-bluetooth

%description -n gnome-bluetooth-plugin-network-manager
GNOME Bluetooth plugin.

%prep
%setup -qn %{orgname}-%{version}

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--disable-migration		\
	--disable-schemas-compile	\
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_datadir}/GConf/gsettings/*.convert
%if 0
%{__rm} $RPM_BUILD_ROOT%{_libdir}/{*,gnome-bluetooth/plugins/*}.la
%endif

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%update_gsettings_cache

%postun
%update_icon_cache hicolor
%update_gsettings_cache

%post   libs -p /usr/sbin/ldconfig
%postun libs -p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/nm-applet
%attr(755,root,root) %{_bindir}/nm-connection-editor
%{_datadir}/nm-applet
%{_desktopdir}/nm-applet.desktop
%{_desktopdir}/nm-connection-editor.desktop
%{_iconsdir}/hicolor/*/apps/*.png
%{_iconsdir}/hicolor/*/apps/*.svg
%{_sysconfdir}/xdg/autostart/*.desktop
%{_datadir}/glib-2.0/schemas/org.gnome.nm-applet.gschema.xml
%{_mandir}/man1/nm-applet.1*
%{_mandir}/man1/nm-connection-editor.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libnm-gtk.so.?
%attr(755,root,root) %{_libdir}/libnm-gtk.so.*.*.*
%{_libdir}/girepository-1.0/NMGtk-1.0.typelib
%{_datadir}/libnm-gtk

%files devel
%defattr(644,root,root,755)
%{_includedir}/libnm-gtk
%{_libdir}/libnm-gtk.so
%{_datadir}/gir-1.0/NMGtk-1.0.gir
%{_pkgconfigdir}/libnm-gtk.pc

%if 0
%files -n gnome-bluetooth-plugin-network-manager
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gnome-bluetooth/plugins/libnma.so
%endif

