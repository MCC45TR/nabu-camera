# nabu-camera

Experimental Linux support for the front and rear cameras and the CN3927 focus
motor on Xiaomi Pad 5 (`nabu`, SM8150), together with a userspace autofocus
prototype.

This is a fork of [CFM880/nabu-camera](https://github.com/CFM880/nabu-camera).
The camera implementation is original work by ChengFangming/CFM880; the
SENEMOS branches only package it and adapt it to newer kernels. Please preserve
that attribution when redistributing or reusing this work.

> This code is experimental. Replacing a kernel, DTB, or kernel modules can make
> the device unbootable. Keep a tested recovery path and a known-good kernel.

## Current features

- Qualcomm SM8150 CAMSS, CCI, CSIPHY, CSID, and VFE support
- OV13B10 rear camera, up to 4208 x 3120
- OV8856 front camera
- CN3927 VCM focus motor with 10-bit `V4L2_CID_FOCUS_ABSOLUTE`
- libcamera simple-IPA tuning files
- GTK4/GStreamer autofocus prototype with continuous and tap-to-focus modes
- GNOME Snapshot 50.0 patches for high-resolution capture and orientation

## Repository layout

```text
kernel-overlay/   Camera kernel sources arranged by Linux source path
config/           Camera Kconfig fragment for an existing .config
camera-app/       nabu-autofocus and GNOME Snapshot patches
camera-tuning/    libcamera simple-IPA tuning files
scripts/          Overlay, build, and installation helpers
LICENSES/         License texts referenced by source SPDX identifiers
```

## Device-tree overlay model

The repository does not replace `sm8150.dtsi` or modify the original
`sm8150-xiaomi-nabu.dts`. Camera nodes are composed through:

```text
sm8150-xiaomi-nabu-camera.dts
  |-- include sm8150-xiaomi-nabu.dts
  `-- include sm8150-xiaomi-nabu-camera.dtsi
```

Build and boot with `qcom/sm8150-xiaomi-nabu-camera.dtb`. When `nabu-iris` is
also installed, use the combined
`qcom/sm8150-xiaomi-nabu-iris-camera.dtb` instead.

## Applying to a kernel tree

Prepare a kernel tree at the baseline documented in [SOURCE.md](SOURCE.md), then
apply the overlay:

```sh
git clone https://gitlab.postmarketos.org/soc/qualcomm-sm8150/linux.git linux
git -C linux checkout 5181e1358ddd6ea8028e841d928942373e6aebc8
./scripts/apply-overlay.sh ./linux
```

The helper permits non-overlapping changes, including a previously applied
`nabu-iris` overlay. It stops instead of silently overwriting a camera target
that has already been changed.

## Building

The output directory must already contain a working Nabu `.config`. The build
helper merges `config/nabu-camera.config` with the kernel's `merge_config.sh`:

```sh
./scripts/build.sh ./linux ./linux/out
```

To merge only the configuration fragment:

```sh
./scripts/merge-config.sh ./linux ./linux/out
```

The resulting modules and DTB must exactly match the running kernel version,
configuration, and symbols.

## Installing modules and tuning files

After verifying that `BUILD_DIR` points to the correct kernel output:

```sh
sudo BUILD_DIR=$PWD/linux/out ./scripts/install-camera-modules.sh
```

The helper installs CCI, CAMSS, and CN3927 modules plus both libcamera tuning
files, while retaining rollback copies. A reboot is required. To roll back:

```sh
sudo ./scripts/install-camera-modules.sh --rollback
```

## Autofocus application

```sh
make -C camera-app
camera-app/nabu-autofocus
```

Click or touch the preview to focus on that region. `--once` performs one
windowless autofocus operation. See
[`camera-app/README.md`](camera-app/README.md) for all options.

## Fedora and Linux 7.2.2

The `senemos-fedora-copr` branch contains `nabu-camera-support.spec` and an SCM
SRPM target for automatic COPR builds. The Linux 7.2.2 kernel integration lives
in [MCC45TR/nabu-linux-kernel](https://github.com/MCC45TR/nabu-linux-kernel/tree/senemos-linux-7.2.2-camera-iris).

## Sources and licenses

The exact kernel baseline, source revisions, and split history are documented
in [SOURCE.md](SOURCE.md). Each source file remains under its own SPDX license;
see `COPYING` and `LICENSES/`. Authorship and license notices from the original
project must remain intact.
