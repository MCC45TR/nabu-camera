Name:           libcamera
Version:        0.7.2
Release:        10.nabu1%{?dist}
Summary:        A library to support complex camera ISPs
License:        LGPL-2.1-or-later
URL:            https://libcamera.org/
Source0:        https://gitlab.freedesktop.org/camera/libcamera/-/archive/v%{version}/%{name}-v%{version}.tar.bz2
Source1:        qcam.desktop
Source2:        qcam.metainfo.xml
Source3:        70-libcamera.rules
Patch01:        0001-disable-rpi-pisp.patch
Patch02:        0002-fix-ov01a10-flickering.patch
Patch03:        0001-ipa-add-OV13B10-and-OV8856-gain-helpers.patch
Patch04:        0002-pipeline-simple-cancel-metadata-only-requests-on-sto.patch
Patch05:        0003-sensor-add-OV13B10-and-OV8856-properties.patch
Patch06:        0001-libcamera-control_ids_core-Add-flash-controls.patch
Patch07:        0002-libcamera-Add-support-for-camera-flash-devices.patch
Patch08:        0003-Documentation-Add-flash-driver-requirements.patch
Patch09:        0004-libcamera-Add-flash-helpers-for-pipeline-handlers.patch
Patch10:        0005-pipeline-simple-expose-and-safely-reset-camera-flash.patch
Patch11:        0006-software-isp-discard-stale-debayer-work-on-stop.patch
Patch12:        0007-ipa-soft-honor-frame-duration-limits.patch
ExcludeArch:    s390x ppc64le

BuildRequires:  gcc-c++
BuildRequires:  gtest-devel
BuildRequires:  desktop-file-utils
BuildRequires:  meson
BuildRequires:  openssl
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  gnutls-devel
BuildRequires:  pkgconfig(gstreamer-video-1.0)
BuildRequires:  pkgconfig(gstreamer-allocators-1.0)
BuildRequires:  libatomic
BuildRequires:  pkgconfig(libdw)
BuildRequires:  libevent-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libtiff-devel
BuildRequires:  libyaml-devel
BuildRequires:  libyuv-devel
BuildRequires:  lttng-ust-devel
BuildRequires:  pkgconfig(Qt6Core)
BuildRequires:  pkgconfig(Qt6Gui)
BuildRequires:  pkgconfig(Qt6OpenGL)
BuildRequires:  pkgconfig(Qt6OpenGLWidgets)
BuildRequires:  pkgconfig(Qt6Widgets)
BuildRequires:  pybind11-devel
BuildRequires:  python3-devel
BuildRequires:  python3-jinja2
BuildRequires:  python3-ply
BuildRequires:  python3-pyyaml
BuildRequires:  SDL2-devel
BuildRequires:  systemd-devel
Recommends:     %{name}-ipa%{?_isa}
Obsoletes:      libcamera-doc < 0.6.0

%description
libcamera provides a userspace camera stack. This Fedora-compatible build adds
generic OV13B10 and OV8856 gain conversion and fixes request cancellation in
the simple software-ISP pipeline used by Qualcomm CAMSS.  It also exposes the
standard libcamera flash controls for media-controller-linked flash devices.
The simple software ISP also applies standard frame-duration limits so regular
30 fps camera clients retain usable exposure while explicit high-rate modes
remain available.

%package devel
Summary: Development package for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
Files for developing against libcamera.

%package ipa
Summary: ISP Image Processing Algorithm Plugins for %{name}
License: LGPL-2.1-or-later AND BSD-2-Clause
Requires: %{name}%{?_isa} = %{version}-%{release}
%description ipa
Image processing algorithm plugins for libcamera.

%package tools
Summary: Tools for %{name}
License: LGPL-2.1-or-later AND BSD-3-Clause
Requires: %{name}%{?_isa} = %{version}-%{release}
%description tools
Command-line tools for libcamera.

%package qcam
Summary: Graphical QCam application for %{name}
License: GPL-2.0-or-later AND MIT
Requires: %{name}%{?_isa} = %{version}-%{release}
%description qcam
Graphical camera demonstration application.

%package gstreamer
Summary: GStreamer plugin for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description gstreamer
GStreamer plugin for libcamera.

%package v4l2
Summary: V4L2 compatibility layer for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description v4l2
V4L2 compatibility layer for libcamera.

%package -n python3-%{name}
Summary: Python bindings for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description -n python3-%{name}
Python bindings for libcamera.

%prep
%autosetup -p1 -n %{name}-v%{version}

%build
export CFLAGS="%{optflags} -Wno-deprecated-declarations"
export CXXFLAGS="%{optflags} -Wno-deprecated-declarations --param=max-devirt-targets=1"
%meson -Dv4l2=enabled -Dlc-compliance=disabled -Dlibunwind=disabled \
       -Dtest=true -Ddocumentation=disabled -Drpi-awb-nn=disabled
%meson_build

%define __spec_install_post \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %{__os_install_post} \
    %{_builddir}/%{name}-v%{version}/src/ipa/ipa-sign-install.sh %{_builddir}/%{name}-v%{version}/%{_vpath_builddir}/src/ipa-priv-key.pem %{buildroot}/%{_libdir}/libcamera/ipa_*.so \
%{nil}

%install
%meson_install
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %SOURCE1
mkdir -p %{buildroot}/%{_metainfodir}/
cp -a %SOURCE2 %{buildroot}/%{_metainfodir}/
install -D -m 644 %SOURCE3 %{buildroot}/%{_udevrulesdir}/70-libcamera.rules

%check
# Mock/COPR build roots do not expose a dma-buf heap.  The GStreamer tests
# require one even with the virtual pipeline, while the remaining test suite
# is hardware-independent and remains mandatory.
%meson_test --no-suite gstreamer
grep -Fq 'REGISTER_CAMERA_SENSOR_HELPER("ov13b10"' src/ipa/libipa/camera_sensor_helper.cpp
grep -Fq 'REGISTER_CAMERA_SENSOR_HELPER("ov8856"' src/ipa/libipa/camera_sensor_helper.cpp
grep -Fq 'while (!queuedRequests_.empty())' src/libcamera/pipeline/simple/simple.cpp
grep -Fq '{ "ov13b10", {' src/libcamera/sensor/camera_sensor_properties.cpp
grep -Fq '{ "ov8856", {' src/libcamera/sensor/camera_sensor_properties.cpp
grep -Fq '.unitCellSize = { 1120, 1120 }' src/libcamera/sensor/camera_sensor_properties.cpp
grep -Fq 'FlashControl::updateFlashControls(sensor_->flash(), controls)' src/libcamera/pipeline/simple/simple.cpp
grep -Fq 'FlashControl::handleFlashControls(data->sensor_->flash()' src/libcamera/pipeline/simple/simple.cpp
grep -Fq 'setMode(CameraFlash::Mode::None)' src/libcamera/pipeline/simple/simple.cpp
grep -Fq 'removeMessages(debayer_.get())' src/libcamera/software_isp/software_isp.cpp
grep -Fq 'V4L2_CID_VBLANK, { delays.vblankDelay, true }' src/libcamera/pipeline/simple/simple.cpp
grep -Fq 'controls::FrameDurationLimits' src/ipa/simple/soft_simple.cpp
grep -Fq 'controls::FrameDuration' src/ipa/simple/soft_simple.cpp

%files
%license COPYING.rst LICENSES/LGPL-2.1-or-later.txt
%{_libdir}/libcamera*.so.0.7
%{_libdir}/libcamera*.so.%{version}
%{_udevrulesdir}/70-libcamera.rules

%files devel
%{_includedir}/%{name}/
%{_libdir}/libcamera*.so
%{_libdir}/pkgconfig/libcamera-base.pc
%{_libdir}/pkgconfig/libcamera.pc

%files ipa
%{_datadir}/libcamera/
%{_libdir}/libcamera/
%{_libexecdir}/libcamera/
%exclude %{_libexecdir}/libcamera/v4l2-compat.so

%files gstreamer
%{_libdir}/gstreamer-1.0/libgstlibcamera.so

%files qcam
%{_bindir}/qcam
%{_datadir}/applications/qcam.desktop
%{_metainfodir}/qcam.metainfo.xml

%files tools
%license LICENSES/GPL-2.0-only.txt
%{_bindir}/cam
%{_bindir}/libcamera-bug-report

%files v4l2
%{_bindir}/libcamerify
%{_libexecdir}/libcamera/v4l2-compat.so

%files -n python3-%{name}
%{python3_sitearch}/*

%changelog
* Sun Sep 06 2026 mcc45tr <mcc45tr@gmail.com> - 0.7.2-10.nabu1
- Materialize calculated sensor timing as utils::Duration before conversion.

* Sun Sep 06 2026 mcc45tr <mcc45tr@gmail.com> - 0.7.2-9.nabu1
- Keep sensor frame-line arithmetic in the signed type expected by Duration.
- Preserve the FrameDurationLimits and 30/120 fps behavior from 0.7.2-8.

* Sun Sep 06 2026 mcc45tr <mcc45tr@gmail.com> - 0.7.2-8.nabu1
- Apply FrameDurationLimits in the simple software ISP through VBLANK.
- Let normal 30 fps clients use longer exposure without removing 120 fps modes.
- Refresh mode-specific controls after sensor configuration.

* Sun Sep 06 2026 mcc45tr <mcc45tr@gmail.com> - 0.7.2-7.nabu1
- Drop stale asynchronous debayer work when a camera session stops.
- Prevent old software-ISP buffers from being processed after camera switch.

* Sun Sep 06 2026 mcc45tr <mcc45tr@gmail.com> - 0.7.2-6.nabu1
- Add the upstream-proposed generic libcamera flash API and driver contract.
- Expose linked flash controls through the simple Qualcomm CAMSS pipeline.
- Force flash and torch off whenever a camera stream stops.
- Correct flash-current units and failed-control read handling.

* Sun Sep 06 2026 mcc45tr <mcc45tr@gmail.com> - 0.7.2-5.nabu1
- Publish OV13B10 and OV8856 unit-cell and standard test-pattern properties.

* Sun Sep 06 2026 mcc45tr <mcc45tr@gmail.com> - 0.7.2-4.nabu1
- Add gain helpers for OV13B10 and OV8856.
- Cancel metadata-only simple-pipeline requests cleanly during camera stop.
