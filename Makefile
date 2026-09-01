.PHONY: srpm

srpm:
	mkdir -p "$(outdir)"
	work=$$(mktemp -d); \
	trap 'rm -rf -- "$$work"' EXIT; \
	mkdir -p "$$work/SOURCES" "$$work/SPECS"; \
	git archive --format=tar.gz --prefix=nabu-camera-support-0.1.0/ \
		-o "$$work/SOURCES/nabu-camera-support-0.1.0.tar.gz" HEAD; \
	cp nabu-camera-support.spec "$$work/SPECS/"; \
	rpmbuild -bs --define "_topdir $$work" \
		"$$work/SPECS/nabu-camera-support.spec"; \
	cp "$$work"/SRPMS/*.src.rpm "$(outdir)/"
