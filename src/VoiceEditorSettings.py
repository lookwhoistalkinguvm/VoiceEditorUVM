#
#Copyright 2020 Carsten Thiele
#
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
#associated documentation files (the "Software"), to deal in the Software without restriction, including
#without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject
#to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all copies or substantial
#portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
#LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import os
import sys

class VoiceEditorSettings :

 VOICEEDITORROOT=os.environ["VOICEEDITORROOT"]

 if (VOICEEDITORROOT=="" or not os.path.exists(VOICEEDITORROOT)):
  print("VOICEEDITORROOT not defined or does not exist: ",VOICEEDITORROOT)
  sys.exit(1)


 scriptDirectoryPath=VOICEEDITORROOT+ r"\scripts"

 sourceDirectoryPath=VOICEEDITORROOT+r"\src"

 runDirectoryPath=VOICEEDITORROOT+r"\run"
 numberOfLinesPerPage=51
 scrollSpeed=10
 widthScaleBox= 110

 lineFilterDefinitionFileName=runDirectoryPath+r"\predefinedLineFilters.txt"

 recentFilesListFileName=VOICEEDITORROOT+r"\run\recentFiles.txt"

 recentDirectoriesListFileName=VOICEEDITORROOT+r"\run\recentDirectories.txt"

 favouriteFilesListFileName=\
  VOICEEDITORROOT+r"\run\favouriteFiles.txt"

 favouriteDirectoriesListFileName=\
  VOICEEDITORROOT+r"\run\favouriteDirectories.txt"

 variableListBackupFileName=\
  VOICEEDITORROOT+r"\run\variableBackupList.txt"

 #fast button settings
 fastControlButtonTopLeftVerticalPosition=20
 fastControlButtonTopLeftHorizontalPosition=50
 fastControlButtonHorizontalOffset=100
 fastButtonTopLeftVerticalPosition=60
 fastButtonTopLeftHorizontalPosition=50
 fastBoxWidth=300
 fastBoxHistoryWidth=700
 fastBoxHeight=100
 fastBoxHorizontalOffset=100
 fastBoxFontSize=10
 fastButtonRowHeight=40
 fastButtonRowMax=23
 fastButtonColumnWidth=450
 fastButtonColumnMax=2
 fastBoxHistoryColumnMax=1
 numberOfFastButtonsPerPage=fastButtonRowMax*fastButtonColumnMax
 fastButtonTemplatesDirectory=VOICEEDITORROOT+r"\templates"
 fastContextBoxHorizontalPosition=fastControlButtonTopLeftHorizontalPosition
 fastContextBoxVerticalPosition=fastButtonTopLeftVerticalPosition+\
  fastButtonRowMax*fastButtonRowHeight
 fastContextBoxWidth=850

 helpFile=VOICEEDITORROOT+r'\run\help.txt'

 useUNIXStyleLineEnding=1
