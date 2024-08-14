@echo off

SET ERROR=""
SET modulename=mimetypeplus
SET pyver=3.12

REM NOTE THIS MUST BE BUILT USING A VERSION OF PYTHON >= 3.10, 3.9.1 and 3.8.7 #THX https://github.com/pypa/build/issues/255#issuecomment-794560752
REM below are the commands used on windows, feel free to use the most up to date version of python when possible

ECHO The following expects that the current directory is the root of this repository, and that the git repo is already initialised
PAUSE

IF NOT EXIST "./%modulename%" GOTO :error

IF NOT EXIST "./reports" MKDIR "./reports"

py -%pyver% -m pip install pip-tools validate-pyproject[all] build twine setuptools coverage pdoc3 pyright pylint || GOTO :error

py -%pyver% -m validate_pyproject -vv pyproject.toml -E setuptools distutils || GOTO :error

py -%pyver% -m unittest -v 2> "./reports/UNITTEST.txt" || GOTO :error

py -%pyver% -m pyright --warnings > "./reports/PYRIGHT.txt" || GOTO :error
py -%pyver% -m pylint -d all -e F,E,W --output-format=text "%modulename%" > "./reports/PYLINT.txt" | GOTO :error

py -%pyver% -m coverage run -m unittest discover || GOTO :error
py -%pyver% -m coverage report --format=markdown > "./reports/COVERAGE.md" || GOTO :error

py -%pyver% -m piptools compile -v --resolver=backtracking --no-header -U --annotate --no-strip-extras -r pyproject.toml || GOTO :error

py -%pyver% -m pdoc --html -f -c show_inherited_members=True -c list_class_variables_in_index=False -c show_type_annotations=True -c show_source_code=True -o tempdocs %modulename% || GOTO :error
IF EXIST "./docs" RMDIR "./docs" /q /s || GOTO :error
REN "./tempdocs/%modulename%" docs || GOTO :error
MOVE "./tempdocs/docs" . || GOTO :error
RMDIR "./tempdocs" /q /s || GOTO :error

py -%pyver% -m build -v -o "./build" || GOTO :error
py -%pyver% -m twine check "./build/*" || GOTO :error
RMDIR "%modulename%.egg-info" /q /s || GOTO :error

git add -v -A || GOTO :error
git gc  --auto || GOTO :error

ECHO Also upload to pypi?
PAUSE
py -%pyver% -m twine upload "./build/*" --username __token__ || GOTO :error

ECHO Complete!
GOTO :EOF

:error
ECHO Failed with error '%ERROR%' #%errorlevel%.
exit /b %errorlevel%
