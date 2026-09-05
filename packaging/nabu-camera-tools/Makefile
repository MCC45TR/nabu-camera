.PHONY: srpm

version := 0.1.0

srpm:
	set -euo pipefail; \
	mkdir -p "$(outdir)"; \
	git -C ../.. archive --format=tar \
		--prefix=nabu-camera-tools-$(version)/ HEAD camera-app | \
		gzip -n -9 > nabu-camera-tools-$(version).tar.gz; \
	rpmbuild -bs nabu-camera-tools.spec \
		--define "_sourcedir $$(pwd)" \
		--define "_srcrpmdir $(outdir)"

