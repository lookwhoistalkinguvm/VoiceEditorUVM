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


import sys
import re

from VoiceEditorSettings import VoiceEditorSettings

class CmdDosRecentFiles(object):



 def __init__(self,listDirectory,recentFilesList,allTheBoxes):

  (self.cmdBox,
       self.editBox,
           self.scaleBox,
               self.viewBox,
                   self.statusBox)=allTheBoxes

  self.listDirectory=listDirectory
  self.recentFilesList=recentFilesList


 def __call__(self):
  if (self.list_recent_files()):
   #Successfully wrote recent file list file
   fullName=VoiceEditorSettings.recentFilesListFileName
   cmdEdit= self.listDirectory.create_cmd_edit_object()
   cmdEdit.processThisCommand(fullName)
   return cmdEdit
  else:
   #Failed to write recent file list file
   self.listDirectory.processThisCommand("list directory")
   return self.listDirectory



 def list_recent_files(self):

  try:
   recentFileListFile=open(VoiceEditorSettings.recentFilesListFileName,"w")
  except:
   self.statusBox.Text="unable to open file: %s"\
       %VoiceEditorSettings.recentFilesListFileName
   return 0

  for file in self.recentFilesList:
   if(file.endswith("duplicate_move_delete.py")):
    continue
   recentFileListFile.write("%s\n"%file)

  recentFileListFile.close()

  return 1

