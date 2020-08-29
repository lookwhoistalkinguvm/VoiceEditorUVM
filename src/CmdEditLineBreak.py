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

class CmdEditLineBreak(object):

 def __init__(self,fileToEditList, cmdBox,editBox,viewBox,statusBox):
  self.cmdBox=cmdBox
  self.editBox=editBox
  self.viewBox=viewBox
  self.statusBox=statusBox
  self.fileToEditList=fileToEditList



 def __call__(self,command,currentEditLine):

  self.currentEditLine=currentEditLine

  if(command == "insert line break"):
   self.insert_line_break()
  elif(command=="remove line break"):
   self.remove_line_break()
  else:
   self.statusBox.Text="Unknown command: %s"%command

  return



 def insert_line_break(self):

  cursorPosition=self.editBox.SelectionStart
  editLine=self.editBox.Text.rstrip()
  matchLeadingSpaces=re.match(r'(\s+)',editLine)
  if(matchLeadingSpaces):
   leadingSpaces=matchLeadingSpaces.group(1)
  else:
   leadingSpaces=""
  linePartOne=editLine[0:cursorPosition]
  linePartTwo=leadingSpaces+editLine[cursorPosition:len(editLine)]
  self.fileToEditList[self.currentEditLine]=linePartOne
  self.fileToEditList.insert(self.currentEditLine+1,linePartTwo)



 def remove_line_break(self):

  if(self.currentEditLine>0):
   self.fileToEditList[self.currentEditLine -1]=\
       self.fileToEditList[self.currentEditLine -1] \
           +self.fileToEditList[self.currentEditLine]

  del self.fileToEditList[self.currentEditLine]



