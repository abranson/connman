# 
# Do NOT Edit the Auto-generated Part!
# Generated by: spectacle version 0.25
# 

Name:       connman

# >> macros
# << macros

Summary:    Connection Manager
Version:    1.4
Release:    1
Group:      Communications/ConnMan
License:    GPLv2
URL:        http://connman.net/
Source0:    http://www.kernel.org/pub/linux/network/connman/%{name}-%{version}.tar.xz
Source1:    connman.tracing
Source2:    main.conf
Source100:  connman.yaml
Patch0:     connman-1.1-tracing.patch
Requires:   dbus >= 1.4
Requires:   wpa_supplicant >= 0.7.1
Requires:   bluez
Requires:   ofono
Requires:   pacrunner
Requires:   connman-configs
Requires:   systemd
Requires(preun): systemd
Requires(post): systemd
Requires(postun): systemd
BuildRequires:  pkgconfig(xtables)
BuildRequires:  pkgconfig(glib-2.0) >= 2.28
BuildRequires:  pkgconfig(gthread-2.0) >= 2.16
BuildRequires:  pkgconfig(dbus-1) >= 1.4
BuildRequires:  pkgconfig(gnutls)
BuildRequires:  openconnect
BuildRequires:  openvpn

%description
Connection Manager provides a daemon for managing Internet connections
within embedded devices running the Linux operating system.


%package devel
Summary:    Development files for Connection Manager
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
connman-devel contains development files for use with connman.

%package test
Summary:    Test Scripts for Connection Manager
Group:      Development/Tools
Requires:   %{name} = %{version}-%{release}
Requires:   dbus-python
Requires:   pygobject2

%description test
Scripts for testing Connman and its functionality

%package tracing
Summary:    Configuration for Connection Manager to enable tracing
Group:      Development/Tools
Requires:   %{name} = %{version}-%{release}

%description tracing
Will enable tracing for ConnMan

%package configs-mer
Summary:    Package to provide default configs for connman
Group:      Development/Tools
Requires:   %{name} = %{version}-%{release}
Provides:   connman-configs

%description configs-mer
This package provides default configs for connman, such as
FallbackTimeservers.



%prep
%setup -q -n %{name}-%{version}

# connman-1.1-tracing.patch
%patch0 -p1
# >> setup
# << setup

%build
# >> build pre
# << build pre

%configure --disable-static \
    --enable-threads \
    --enable-ethernet=builtin \
    --enable-wifi=builtin \
    --enable-bluetooth=builtin \
    --enable-ofono=builtin \
    --enable-openconnect=builtin \
    --enable-openvpn=builtin \
    --enable-loopback=builtin \
    --enable-pacrunner=builtin \
    --enable-client \
    --enable-test \
    --with-systemdunitdir=/%{_lib}/systemd/system

make %{?jobs:-j%jobs}

# >> build post
# << build post

%install
rm -rf %{buildroot}
# >> install pre
# << install pre
%make_install
mkdir -p %{buildroot}%{_sysconfdir}/tracing/connman/
cp -a %{SOURCE1} %{buildroot}%{_sysconfdir}/tracing/connman/
mkdir -p %{buildroot}%{_sysconfdir}/connman/
cp -a %{SOURCE2} %{buildroot}%{_sysconfdir}/connman/


# >> install post
mkdir -p %{buildroot}/%{_lib}/systemd/system/network.target.wants
ln -s ../connman.service %{buildroot}/%{_lib}/systemd/system/network.target.wants/connman.service
# << install post


%preun
# >> preun
if [ "$1" -eq 0 ]; then
systemctl stop connman.service
fi
# << preun

%post
# >> post
systemctl daemon-reload
# Do not restart connman here or network breaks.
# We can't reload it either as connman doesn't
# support that feature.
# << post

%postun
# >> postun
systemctl daemon-reload
# << postun

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING INSTALL ChangeLog NEWS README
%{_sbindir}/*
%{_libdir}/%{name}/scripts/*
%config %{_sysconfdir}/dbus-1/system.d/*.conf
/%{_lib}/systemd/system/connman.service
/%{_lib}/systemd/system/network.target.wants/connman.service
# >> files
# << files

%files devel
%defattr(-,root,root,-)
%doc AUTHORS COPYING INSTALL
%{_includedir}/%{name}/*.h
%{_libdir}/pkgconfig/*.pc
# >> files devel
# << files devel

%files test
%defattr(-,root,root,-)
%{_libdir}/%{name}/test/*
# >> files test
# << files test

%files tracing
%defattr(-,root,root,-)
%config %{_sysconfdir}/tracing/connman
# >> files tracing
# << files tracing

%files configs-mer
%defattr(-,root,root,-)
%config %{_sysconfdir}/connman/main.conf
# >> files configs-mer
# << files configs-mer
