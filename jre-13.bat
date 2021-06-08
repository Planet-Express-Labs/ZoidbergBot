Rem This switches your PATH variable within windows to jdk-13. Of course, this doesn't work with anything outside of Windows. 

@echo off
set JAVA_HOME=C:\Program Files\Java\jdk-13
set Path=%JAVA_HOME%\bin;%Path%
echo Java 13 activated.
PAUSE
