.PHONY: build dist docs
VERSION=`python setup.py -V`

build:
	python setup.py build

install: dist
	pip -V
	pip install --no-cache-dir --no-deps --upgrade --force-reinstall --find-links ./dist/django-cas-server-${VERSION}.tar.gz django-cas-server

uninstall:
	pip uninstall django-cas-server || true

clean_pyc:
	find ./ -name '*.pyc' -delete
	find ./ -name __pycache__ -delete
clean_build:
	rm -rf build django_cas_server.egg-info dist
clean_tox:
	rm -rf .tox tox_logs
clean_test_venv:
	rm -rf test_venv
clean_coverage:
	rm -rf coverage.xml .coverage htmlcov
clean_tild_backup:
	find ./ -name '*~' -delete
clean_docs:
	rm -rf docs/_build/ docs/django.inv
clean_eggs:
	rm -rf .eggs/

clean: clean_pyc clean_build clean_coverage clean_tild_backup

clean_all: clean clean_tox clean_test_venv clean_docs clean_eggs

dist:
	python setup.py sdist

test_venv/bin/python:
	python3 -m venv test_venv
	test_venv/bin/pip install -U --requirement requirements-dev.txt 'Django>=2.0,<2.1'

test_venv/cas/manage.py: test_venv
	mkdir -p test_venv/cas
	test_venv/bin/django-admin startproject cas test_venv/cas
	ln -s ../../cas_server test_venv/cas/cas_server
	sed -i "s/'django.contrib.staticfiles',/'django.contrib.staticfiles',\n    'cas_server',/" test_venv/cas/cas/settings.py
	sed -i "s/'django.middleware.clickjacking.XFrameOptionsMiddleware',/'django.middleware.clickjacking.XFrameOptionsMiddleware',\n    'django.middleware.locale.LocaleMiddleware',/" test_venv/cas/cas/settings.py
	sed -i 's/from django.conf.urls import url/from django.conf.urls import url, include/' test_venv/cas/cas/urls.py
	sed -i "s@url(r'^admin/', admin.site.urls),@url(r'^admin/', admin.site.urls),\n    url(r'^', include('cas_server.urls', namespace='cas_server')),@" test_venv/cas/cas/urls.py
	test_venv/bin/python test_venv/cas/manage.py migrate
	test_venv/bin/python test_venv/cas/manage.py createsuperuser

test_venv: test_venv/bin/python

test_project: test_venv/cas/manage.py
	@echo "##############################################################"
	@echo "A test django project was created in $(realpath test_venv/cas)"

run_server: test_project
	test_venv/bin/python test_venv/cas/manage.py runserver

run_tests: test_venv
	python setup.py check --restructuredtext --stric
	test_venv/bin/py.test -rw -x --cov=cas_server --cov-report html --cov-report term
	rm htmlcov/coverage_html.js  # I am really pissed off by those keybord shortcuts

test_venv/bin/sphinx-build: test_venv
	test_venv/bin/pip install Sphinx sphinx_rtd_theme

docs: test_venv/bin/sphinx-build
	bash -c "source test_venv/bin/activate; cd docs; make html"

publish_pypi_release:
	python setup.py sdist bdist_wheel upload --sign
