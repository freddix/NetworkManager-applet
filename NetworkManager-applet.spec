%define		orgname	network-manager-applet

Summary:	NetworkManager applet for GNOME
Name:		NetworkManager-applet
Version:	0.9.8.0
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/network-manager-applet/0.9/%{orgname}-%{version}.tar.xz
# Source0-md5:	531ce56c51ec86c5d2dc4cbe58649583
BuildRequires:	NetworkManager-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	gnome-bluetooth-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk+-devel
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
	--disable-static	\
	--enable-more-warnings=yes
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

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
%attr(755,root,root) %{_libexecdir}/nm-applet-migration-tool
%{_datadir}/GConf/gsettings/nm-applet.convert
%{_datadir}/glib-2.0/schemas/org.gnome.nm-applet.gschema.xml
/usr/share/man/man1/nm-applet.1.gz
/usr/share/man/man1/nm-connection-editor.1.gz

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

%files -n gnome-bluetooth-plugin-network-manager
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gnome-bluetooth/plugins/libnma.so

