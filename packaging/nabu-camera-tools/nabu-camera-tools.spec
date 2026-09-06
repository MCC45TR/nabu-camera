Name:           nabu-camera-tools
Version:        0.1.0
Release:        2%{?dist}
Summary:        Compatibility package for Xiaomi Pad 5 camera tools
License:        GPL-2.0-only
URL:            https://github.com/MCC45TR/nabu-camera
Source0:        %{name}-%{version}.tar.gz
ExclusiveArch:  aarch64

Requires:       nabu-camera-support >= 0.1.0-3.alpha

%description
This compatibility package installs nabu-camera-support, which provides the
continuous and tap-to-focus helper, camera tuning, and bounded raw CN3927
positioning. It intentionally owns no camera executable itself.

%prep
%autosetup

%check
test -f camera-app/README.md

%files
%doc camera-app/README.md

%changelog
* Sun Sep 06 2026 mcc45tr <mcc45tr@gmail.com> - 0.1.0-2
- Convert to a compatibility package requiring nabu-camera-support.
- Avoid owning files already shipped by nabu-camera-support.

* Sun Sep 06 2026 mcc45tr <mcc45tr@gmail.com> - 0.1.0-1
- Package continuous and tap-to-focus support for the Nabu rear camera.
- Add explicit raw CN3927 position control for calibration and diagnostics.
