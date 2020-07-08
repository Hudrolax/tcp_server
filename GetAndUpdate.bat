@ECHO OFF
CLS

SET BASE_NAME=TradeCopy
SET CONNECT_STR="Srvr=""golden1"";Ref=""trade2019"";"
SET USER_NAME=Updater
SET USER_PWD=1234567

SET START_FILE="C:\Program Files\1cv8\8.3.10.2252\bin\1cv8.exe"
SET BACKUP_DIR=C:\PythonScripts
SET CF_DIR=C:\PythonScripts
SET LOG_DIR=C:\PythonScripts

SET UNLOCK_CODE=123

SET CF_FILE=%CF_DIR%\1Cv8.cf
SET LOG_FILE=%LOG_DIR%\update_log_%date:~6,4%-%date:~3,2%-%date:~0,2%.log
SET DUMP_FILE=%BACKUP_DIR%\%BASE_NAME%_%date:~6,4%-%date:~3,2%-%date:~0,2%.dt



ECHO --- Start the update %DATE% %TIME% ---
ECHO --- Start the update %DATE% %TIME% --- >> %LOG_FILE%
ECHO.
ECHO. >> %LOG_FILE%

rem ECHO --- Completion of the inactive terminal sessions ---
rem ECHO --- Completion of the inactive terminal sessions --- >> %LOG_FILE%
rem tskill *1cv8* /a /v
rem @ECHO.
rem @ECHO. >> %LOG_FILE%

ECHO --- Getting conf from storage ---
ECHO --- Getting conf from storage --- >> %LOG_FILE%
START "" /wait %START_FILE% DESIGNER /IBConnectionString%CONNECT_STR% /N%USER_NAME% /P%USER_PWD% /ConfigurationRepositoryF"\\golden1\1cConfigurationStorage\Trade_New_Type" /ConfigurationRepositoryN"update" /ConfigurationRepositoryP"" /ConfigurationRepositoryUpdateCfg /Out%LOG_FILE% -NoTruncate 
ECHO.
ECHO. >> %LOG_FILE%



ECHO --- Information base update ---
ECHO --- Information base update --- >> %LOG_FILE%

START "" /wait %START_FILE% DESIGNER /IBConnectionString%CONNECT_STR% /N%USER_NAME% /P%USER_PWD% /WA- /UC%UNLOCK_CODE% /UpdateDBCfg -WarningsAsErrors /Out%LOG_FILE% -NoTruncate
ECHO.
ECHO. >> %LOG_FILE%


ECHO --- End of update %DATE% %TIME% ---
ECHO --- End of update %DATE% %TIME% --- >> %LOG_FILE%
ECHO.
ECHO. >> %LOG_FILE%

