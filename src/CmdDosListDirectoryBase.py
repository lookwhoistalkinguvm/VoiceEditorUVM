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
import re

import VoiceEditorSettings

class CmdDosListDirectoryBase(object) :

 def __init__(self,voiceEditor,cmdBox,editBox,scaleBox,viewBox,statusBox):
  self.voiceEditor=voiceEditor
  self.commandState = "idle"
  self.cmdBox=cmdBox
  self.scaleBox=scaleBox
  self.viewBox=viewBox
  self.statusBox=statusBox
  self.editBox=editBox
  self.nextCommand=None
  self.files=[]
  self.path=""

 def processThisCommand(self,command):
  pass

 def list_directory(self):
  dirs=[]
  operations=[]
  self.fileList=[]
  del self.files[:]
  self.viewBox.Text = ""
  self.editBox.Text = ""
  self.path = os.getcwd()
  self.slice_path(dirs)
  try:
   directory_contents = os.listdir(self.path)
  except:
   self.statusBox.Text="Unable to enter directory: %s"%self.path
   return
  operations.append((3,self.path,".."))
  operations.append((3,self.path,"create new file"))
  operations.append((3,self.path,"create new directory"))
  operations.append((3,self.path,"duplicate file(s)"))
  operations.append((3,self.path,"move file(s)"))
  operations.append((3,self.path,"delete file(s)"))
  operations.append((3,self.path,"insert file(s)"))
  for file in directory_contents :
   full_name= os.path.join(self.path, file )
   if os.path.isdir(full_name):
    dirs.append((1,self.path,file))
   if os.path.isfile(full_name):
    if(not re.search(r'.backup$', full_name)):
     self.files.append((0,self.path,file))
  self.fileList=operations+dirs+self.files
  self.viewBox.AppendText("Path : " + self.path + "\n\n")
  self.viewBox.AppendText("\n")
  self.viewBox.AppendText("Operations :" + "\n")
  fileCount=0
  for file in operations:
   self.viewBox.AppendText("%4d %s" % (fileCount,file[2]) + "\n" )
   fileCount=fileCount+1
  self.viewBox.AppendText("\n")
  self.viewBox.AppendText("Directories :" + "\n")
  for file in dirs:
   self.viewBox.AppendText("%4d %s" % (fileCount,file[2]) + "\n" )
   fileCount=fileCount+1
  self.viewBox.AppendText("\n")
  self.viewBox.AppendText("files :" + "\n")
  for file in self.files:
   self.viewBox.AppendText("%4d %s" % (fileCount,file[2]) + "\n" )
   fileCount=fileCount+1
  self.viewBox.AppendText("\n")

 def slice_path(self, directories):
  choppedPath=""
  path=self.path
  while(1):
   choppedPath=os.path.dirname(path)
   if choppedPath==path:
    break
   directories.append((1, "", choppedPath))
   path = choppedPath









