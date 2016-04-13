
just_run_everything:
	make install_deps
	make analyse
	make serve-front &
	make serve-back &

serve-back:
	python -3 ./manage.py runserver

serve-back-debug:
	DJANGO_SETTINGS_MODULE=serve.settings_debug python -3 ./manage.py runserver

serve-front: build-front
	cd web && grunt serve

build-front:
	cd web && grunt build

install_deps:
	sudo ./install_tools.sh
	sudo ./install_neo4j.sh
	./install_pypy.sh
	./install_js.sh
	touch install_deps

cleardb:
	PYTHONPATH=./pypy ./codesearch.py cleardb

analyse:
	PYTHONPATH=./pypy ./codesearch.py parse data

test:
	PYTHONPATH=./pypy nosetests3 -vs codesearch
