_python = python3
_manage_py = $(_python) manage.py
_execc = docker-compose exec
_pytest = python3 -B -m pytest

###############################################################################
#
# OS related
#
###############################################################################
app_bash:
	$(_execc) app bash

###############################################################################
#
# Docker related
#
###############################################################################
build:
	docker-compose build

up:
	docker-compose up

###############################################################################
#
# Django related
#
###############################################################################

migrate:
	$(_execc) app $(_manage_py) migrate

makemigrations:
	$(_execc) app $(_manage_py) makemigrations


load_infra:
	$(_execc) app $(_manage_py) load_cloud_infrastructure -f /$(FILE)

overwrite_infra:
	$(_execc) app $(_manage_py) load_cloud_infrastructure -d -f /$(FILE)

###############################################################################
#
# Unit Testing related
#
###############################################################################

clean_before_test:
	@find ./ -name '*.pyc' -delete

test: clean_before_test
	$(_execc) app $(_pytest)

linter: clean_before_test
	$(_execc) app bash -c 'find . -name "*.py" | xargs pylint'

