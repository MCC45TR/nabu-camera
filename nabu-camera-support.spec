Name:           nabu-camera-support
Version:        0.1.0
Release:        3.alpha%{?dist}
Summary:        Camera tuning and autofocus support for Xiaomi Pad 5
License:        GPL-2.0-only AND CC0-1.0
URL:            https://github.com/CFM880/nabu-camera
Source0:        %{name}-%{version}.tar.gz
ExclusiveArch:  aarch64

BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(gstreamer-app-1.0)
BuildRequires:  pkgconfig(gstreamer-video-1.0)
BuildRequires:  pkgconfig(gtk4)
Requires:       libcamera-ipa

%description
Fedora userspace support for the Xiaomi Pad 5 camera stack: the original
ChengFangming/CFM880 libcamera simple-IPA colour tuning profiles and the
Nabu rear-camera autofocus helper. Kernel support is provided separately.

Upstream and original work: https://github.com/CFM880/nabu-camera

%prep
%autosetup

%build
%make_build -C camera-app

%install
install -Dm0755 camera-app/nabu-autofocus \
    %{buildroot}%{_bindir}/nabu-autofocus
install -Dm0644 camera-tuning/ov13b10.yaml \
    %{buildroot}%{_datadir}/libcamera/ipa/simple/ov13b10.yaml
install -Dm0644 camera-tuning/ov8856.yaml \
    %{buildroot}%{_datadir}/libcamera/ipa/simple/ov8856.yaml
install -Dm0644 camera-app/README.md \
    %{buildroot}%{_docdir}/%{name}/README-autofocus.md
desktop-file-install --dir=%{buildroot}%{_datadir}/applications \
    camera-app/org.senemos.NabuAutofocus.desktop

%check
test -x %{buildroot}%{_bindir}/nabu-autofocus
%{buildroot}%{_bindir}/nabu-autofocus --help | grep -Fq -- '--position N'
desktop-file-validate \
    %{buildroot}%{_datadir}/applications/org.senemos.NabuAutofocus.desktop
grep -Fqx 'version: 1' \
    %{buildroot}%{_datadir}/libcamera/ipa/simple/ov13b10.yaml
grep -Fqx 'version: 1' \
    %{buildroot}%{_datadir}/libcamera/ipa/simple/ov8856.yaml

%files
%license LICENSES/preferred/GPL-2.0 LICENSES/preferred/CC0-1.0
%doc README.md SOURCE.md
%{_docdir}/%{name}/README-autofocus.md
%{_bindir}/nabu-autofocus
%{_datadir}/applications/org.senemos.NabuAutofocus.desktop
%{_datadir}/libcamera/ipa/simple/ov13b10.yaml
%{_datadir}/libcamera/ipa/simple/ov8856.yaml

%changelog
* Sun Sep 06 2026 mcc45tr <mcc45tr@gmail.com> - 0.1.0-3.alpha
- Add a desktop launcher for the Nabu autofocus helper.
- Add explicit, bounded raw CN3927 positioning for diagnostics and calibration.

* Tue Sep 01 2026 mcc45tr <mcc45tr@gmail.com> - 0.1.0-2.alpha
- Install the autofocus guide under a distinct documentation name.

* Tue Sep 01 2026 mcc45tr <mcc45tr@gmail.com> - 0.1.0-1.alpha
- Package the original CFM880 Nabu camera tuning and autofocus userspace.
