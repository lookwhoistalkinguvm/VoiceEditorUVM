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
from CmdDosListDirectory import CmdDosListDirectory
from CmdEdit import CmdEdit

class CmdBoxHandler :



 def __init__(self,voiceEditor,cmdBox,editBox,scaleBox,viewBox,statusBox):
  self.voiceEditor=voiceEditor
  self.cmdBox=cmdBox
  self.scaleBox=scaleBox
  self.editBox=editBox
  self.statusBox=statusBox
  self.viewBox=viewBox
  self.cmd=CmdDosListDirectory\
   (voiceEditor,self.cmdBox,self.editBox,self.scaleBox,self.viewBox,self.statusBox)



 def processCmd(self,command):
  self.cmd=self.cmd.processThisCommand(command)



 def is_instance_of_cmdedit(self,objectToCheck):
  return isinstance(objectToCheck,CmdEdit)



