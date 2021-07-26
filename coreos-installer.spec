%global rustflags -Clink-arg=-Wl,-z,relro,-z,now -C debuginfo=2

Name:           coreos-installer
#               This will be set by osc services, that will run after this.
Version:        0.0.0
Release:        0
Summary:        Installer for Fedora CoreOS, openSUSE Kubic, and RHEL CoreOS
# Upstream license specification: Apache-2.0
License:        ASL 2.0
Group:          System/Boot
Url:            https://github.com/coreos/coreos-installer
Source0:        %{name}-%{version}.tar.xz
Source1:        vendor.tar.xz
Source2:        cargo_config

BuildRequires:  cargo
BuildRequires:  systemd-rpm-macros

ExcludeArch:    s390 s390x ppc ppc64 ppc64le %ix86


%global _description %{expand:
coreos-installer installs Fedora CoreOS, openSUSE Kubic or RHEL CoreOS to bare-metal 
machines (or, occasionally, to virtual machines).
}

%description %{_description}

%prep
%setup -q
%setup -qa1
mkdir .cargo
cp %{SOURCE2} .cargo/config
# Remove exec bits to prevent an issue in fedora shebang checking
find vendor -type f -name \*.rs -exec chmod -x '{}' \;

%build
export RUSTFLAGS="%{rustflags}"
cargo build --offline --release

%install
install -D -d -m 0755 %{buildroot}%{_bindir}
# Install binaries, dracut modules, units, targets, generators for running via systemd
install -D -m 0755 -t %{buildroot}%{dracutlibdir}/modules.d/50rdcore dracut/50rdcore/module-setup.sh
install -D -m 0755 -t %{buildroot}%{_libexecdir} scripts/coreos-installer-service
install -D -m 0755 -t %{buildroot}%{_libexecdir} scripts/coreos-installer-disable-device-auto-activation
install -D -m 0644 -t %{buildroot}%{_unitdir} systemd/coreos-installer-disable-device-auto-activation.service
install -D -m 0644 -t %{buildroot}%{_unitdir} systemd/coreos-installer.service
install -D -m 0644 -t %{buildroot}%{_unitdir} systemd/coreos-installer-reboot.service
install -D -m 0644 -t %{buildroot}%{_unitdir} systemd/coreos-installer-noreboot.service
install -D -m 0644 -t %{buildroot}%{_unitdir} systemd/coreos-installer-pre.target
install -D -m 0644 -t %{buildroot}%{_unitdir} systemd/coreos-installer.target
install -D -m 0644 -t %{buildroot}%{_unitdir} systemd/coreos-installer-post.target
install -D -m 0755 -t %{buildroot}%{_systemdgeneratordir} systemd/coreos-installer-generator
mv %{buildroot}%{_bindir}/rdcore %{buildroot}%{dracutlibdir}/modules.d/50rdcore/

%files
%license LICENSE
%doc README.md
%{_bindir}/coreos-installer

%changelog