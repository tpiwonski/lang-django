@ECHO OFF

IF "%1"=="" GOTO END
IF NOT EXIST .%1.env GOTO END

set PIPENV_DOTENV_LOCATION=.%1.env
pipenv shell

:END
