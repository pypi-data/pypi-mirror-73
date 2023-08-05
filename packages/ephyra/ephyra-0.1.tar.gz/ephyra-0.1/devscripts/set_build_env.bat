@ECHO OFF

ECHO Using currently active SDK
SET DISTUTILS_USE_SDK=1

ECHO Forcing dynamic linking with vcruntime library
SET PY_VCRUNTIME_REDIST=No thanks