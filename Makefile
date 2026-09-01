.PHONY: srpm

srpm:
	mkdir -p "$(outdir)"
	work=$$(mktemp -d); \
	trap 'rm -rf -- "$$work"' EXIT; \
	mkdir -p "$$work/SOURCES" "$$work/SPECS"; \
	tar --exclude=.git --exclude=camera-app/nabu-autofocus \
		--transform='s,^,nabu-camera-support-0.1.0/,' \
		-czf "$$work/SOURCES/nabu-camera-support-0.1.0.tar.gz" .; \
	cp nabu-camera-support.spec "$$work/SPECS/"; \
	rpmbuild -bs --define "_topdir $$work" \
		"$$work/SPECS/nabu-camera-support.spec"; \
	cp "$$work"/SRPMS/*.src.rpm "$(outdir)/"
