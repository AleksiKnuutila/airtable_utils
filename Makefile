# This needs to be migrated away from pipenv

all:
	@echo "\t\`make test\` to run tests"
	@echo "\t\`make dev\` to install development version"
	@echo "\t\`make lint\` to run static typing tests"

dev :
	@pipenv install --dev
	@pipenv run pip install -e .
	@echo "installed development version; run \`pipenv shell\` to enter activated environment."

test:
	@pipenv run pytest --cov-report term-missing --cov=airtable_forms tests/


lint :
	@echo "======== PYLINT ======="
	@pipenv run pylint --rcfile=.pylintrc airtable_forms -f parseable -r n
	@echo "======== MYPY ======="
	@pipenv run mypy --ignore-missing-imports --follow-imports=skip airtable_forms
	@echo "======== PYCODESTYLE ======="
	@pipenv run pycodestyle airtable_forms --max-line-length=120
	@echo "======== PYDOCSTYLE  ======="
	@pipenv run pydocstyle airtable_forms

remove:
	@echo "removing virtual environment..."
	@pipenv --rm

