# VoiceEditorUVM

VoiceEditor for UVM

0) Demo video at : 
https://youtu.be/yHlBrfDe0wI 

1) Install IronPython
https://ironpython.net/download/

2) Download latest VoiceEditorUVM release and unpack.

Define user env variable that points to installation directory eg :

VOICEEDITORROOT = C:\%HOMEPATH%\Projects\VoiceEditorUVM

3) Set/add the following environment variables :
IRONPYTHONPATH += %VOICEEDITORROOT%\src
IRONPYTHONPATH += %VOICEEDITORROOT%\src_uvm

4) cd %VOICEEDITORROOT%\run
   Run create_snapshot BAT script : run_create_snapshot.bat

5) In the same directory as 4), invoke the editor : run.bat


   
