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


import re
import os.path

class CmdDosCreateNewFile(object) :


 def __init__(self,cmdBox,editBox, viewBox,statusBox) :
  self.commandState = "idle"
  self.cmdBox=cmdBox
  self.viewBox=viewBox
  self.statusBox=statusBox
  self.editBox=editBox
  self.nextCommand=None
  self.statusBox.Text="create new file in "+os.getcwd()

 def processThisCommand(self,command):
  self.nextCommand=self
  if (command=="list directory"or command=="escape command"):
   self.listDirectory.processThisCommand(command)
   self.nextCommand=self.listDirectory
   return self.nextCommand
  else:
   fileToCreate=command
   validFileNamePattern=re.compile(r'[.\w+]')
   if (os.path.exists(fileToCreate)):
    print("File already exists : ",fileToCreate)
    self.statusBox.Text="File already exists : "+fileToCreate
   if(validFileNamePattern.match(fileToCreate)):
    try:
     f=open(fileToCreate,"w+")
     f.close()
     self.listDirectory.processThisCommand("list directory")
     self.nextCommand=self.listDirectory
    except:
     print("unable to open file :",fileToCreate)
   else:
    self.statusBox="Not a valid file name :"+fileToCreate
  return self.nextCommand
