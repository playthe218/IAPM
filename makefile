SRCS = main.py iapm.conf

install: $(SRCS)
	cp main.py /usr/bin/iapm
	cp iapm.conf /etc/iapm.conf
	mkdir --parents /var/db/iapm/database/
	mkdir --parents /var/db/iapm/repos/
	mkdir --parents /var/cache/iapm
	cp repos_test/playos.repo /var/db/iapm/repos/
	cp -r locale/*/*/iapm.mo /usr/share/locale/*/*/iapm.mo
	cp iapm.info /var/db/iapm/database/