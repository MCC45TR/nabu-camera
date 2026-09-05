Name:           nabu-camera-tools
Version:        0.1.0
Release:        1%{?dist}
Summary:        Camera diagnostics and focus tools for Xiaomi Pad 5
License:        GPL-2.0-only
URL:            https://github.com/MCC45TR/nabu-camera
Source0:        %{name}-%{version}.tar.gz
ExclusiveArch:  aarch64

BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(gstreamer-app-1.0)
BuildRequires:  pkgconfig(gstreamer-video-1.0)
BuildRequires:  pkgconfig(gtk4)

%description
Nabu camera tools provide continuous and tap-to-focus operation for the rear
OV13B10 camera and CN3927 lens actuator.  Raw actuator positioning is exposed
for diagnostics without pretending that uncalibrated values are dioptres.

%prep
%autosetup

%build
%make_build -C camera-app

%install
install -D -m 0755 camera-app/nabu-autofocus \
    %{buildroot}%{_bindir}/nabu-autofocus
desktop-file-install --dir=%{buildroot}%{_datadir}/applications \
    camera-app/org.senemos.NabuAutofocus.desktop

%check
./camera-app/nabu-autofocus --help | grep -Fq -- '--position N'
desktop-file-validate camera-app/org.senemos.NabuAutofocus.desktop

%files
%license camera-app/nabu-autofocus.cpp
%doc camera-app/README.md
%{_bindir}/nabu-autofocus
%{_datadir}/applications/org.senemos.NabuAutofocus.desktop

%changelog
* Sun Sep 06 2026 mcc45tr <mcc45tr@gmail.com> - 0.1.0-1
- Package continuous and tap-to-focus support for the Nabu rear camera.
- Add explicit raw CN3927 position control for calibration and diagnostics.
