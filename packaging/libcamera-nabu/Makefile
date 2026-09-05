.PHONY: srpm

srpm:
	set -euo pipefail; \
	mkdir -p "$(outdir)"; \
	archive=libcamera-v0.7.2.tar.bz2; \
	curl -fsSL --retry 3 \
		"https://gitlab.freedesktop.org/camera/libcamera/-/archive/v0.7.2/$$archive" \
		-o "$$archive"; \
	sha256sum -c UPSTREAM.sha256; \
	sha256sum -c PATCHES.sha256; \
	rpmbuild -bs libcamera.spec \
		--define "_sourcedir $$(pwd)" \
		--define "_srcrpmdir $(outdir)"
