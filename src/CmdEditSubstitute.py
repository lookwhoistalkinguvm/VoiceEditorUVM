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

class CmdEditSubstitute(object):

 oldString="old string"
 newString="new string"
 rangeStartLast="range start"
 rangeEndLast="range end"

 def __init__(self,parent,fileToEditList,cmdBox,editBox,viewBox,statusBox):
  self.parent=parent
  self.cmdBox= cmdBox
  self.editBox=editBox
  self.viewBox=viewBox
  self.statusBox=statusBox
  self.fileToEditList=fileToEditList
  self.operation=""
  self.oldStringHasBeenEntered=False
  self.newStringHasBeenEntered=False
  self.startLineHasBeenEntered=False
  self.endLineHasBeenEntered=False
  self.rangeStart=0
  self.rangeEnd=0

 def __call__(self,command):

  self.statusBox.Text="Please enter old string."

  self.cmdBox.Text=CmdEditSubstitute.oldString
  self.cmdBox.SelectionStart=0
  self.cmdBox.SelectionLength=len(CmdEditSubstitute.oldString)
  return self



 def processThisCommand(self,command):

  self.nextCommand=self

  if (command=="escape command"):
   self.parent.displayFile()
   self.statusBox.Text="OK"
   self.cmdBox.Text=""
   return self.parent

  if(not self.oldStringHasBeenEntered):
   CmdEditSubstitute.oldString=command
   self.oldStringHasBeenEntered=True
   self.statusBox.Text="Please enter new pattern."
   self.cmdBox.Text=CmdEditSubstitute.newString
   self.cmdBox.SelectionStart=0
   self.cmdBox.SelectionLength=len(CmdEditSubstitute.newString)
   return self.nextCommand

  if ( not self.newStringHasBeenEntered):
   CmdEditSubstitute.newString=command
   self.newStringHasBeenEntered=True
   self.statusBox.Text="Please enter start line number."
   self.cmdBox.Text="%s"%CmdEditSubstitute.rangeStartLast
   self.cmdBox.SelectionStart=0
   self.cmdBox.SelectionLength=len("%s"%CmdEditSubstitute.rangeStartLast)
   return self.nextCommand

  if(not self.startLineHasBeenEntered):
   if (command.isdigit()):
    self.rangeStart=int(command)
    CmdEditSubstitute.rangeStartLast=self.rangeStart
   else:
    CmdEditSubstitute.rangeStartLast="range start"
    self.rangeStart=0
   self.startLineHasBeenEntered=True
   self.statusBox.Text="Please enter end line number."
   self.cmdBox.Text="%s"%CmdEditSubstitute.rangeEndLast
   self.cmdBox.SelectionStart=0
   self.cmdBox.SelectionLength=len("%s"%CmdEditSubstitute.rangeEndLast)
   return self.nextCommand

  if ( not self.endLineHasBeenEntered):
   if(command.isdigit()):
    self.rangeEnd=int(command)
    CmdEditSubstitute.rangeEndLast=self.rangeEnd
   else:
    CmdEditSubstitute.rangeEndLast="range end"
    self.rangeEnd=len(self.fileToEditList)-1
   self.endLineHasBeenEntered=True

  if(self.rangeStart<0):
   self.rangeStart=0

  if(self.rangeEnd>=len(self.fileToEditList)-1):
   self.rangeEnd=len(self.fileToEditList)-1

  for lineIndex in range(self.rangeStart,self.rangeEnd+1):
   lineToEdit=self.fileToEditList[lineIndex]
   try:
    lineToEdit=re.sub("%s"%CmdEditSubstitute.oldString,"%s"%CmdEditSubstitute.newString,lineToEdit)
#   lineToEdit=lineToEdit.replace(self.oldString,self.newString)
   except:
    self.statusBox.Text="Invalid substitution patterns"
    return self.parent
   self.fileToEditList[lineIndex]=lineToEdit

  self.parent.displayFile()

  self.statusBox.Text="OK"

  return self.parent






