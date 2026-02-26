prefix		?= /usr
exec_prefix	?= $(prefix)

bindir      ?= $(exec_prefix)/bin
sbindir     ?= $(exec_prefix)/sbin
libexecdir  ?= $(exec_prefix)/libexec
sysconfdir  ?= /etc

.PHONY: clean install

build:
	mkdir -p build/iapm_root build/share build/conf
	cp -r src/* build/iapm_root/
	ln -svf iapm_root/main.py build/iapm
	cp share/iapm.conf build/conf/
	chmod +x build/iapm_root/main.py

	@touch build/.built
	@echo "Build finished."
	@echo "Now you can run \"make install\" or \"make test\""

test: build/.built
	@echo TEST_TODO

clean:
	rm -rvf build/
