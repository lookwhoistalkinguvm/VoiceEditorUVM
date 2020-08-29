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

class CmdEditCommentLines(object):

 def __init__(self,fileToEditList,fullFileName,cmdBox,editBox,viewBox,statusBox):
  self.cmdBox=cmdBox
  self.editBox=editBox
  self.viewBox=viewBox
  self.statusBox=statusBox
  self.fileToEditList=fileToEditList
  self.operation=""
  self.rangeStart=0
  self.rangeEnd=0

  self.commentCharacter="#"

  if (fullFileName.endswith(".svh") or fullFileName.endswith(".sv")):
   self.commentCharacter="//"


 def __call__(self,command):

  matchOperation=re.match(r'(comment out|comment in)\s+lines\s*(\d+)\s*', command)
  if(matchOperation):
   self.operation=matchOperation.group(1)
   self.rangeStart=int(matchOperation.group(2))
   self.rangeEnd=self.rangeStart

  matchOperation=re.match(r'(comment out|comment in)\s+lines\s*(\d+)\s*:\s*(\d+)', command)
  if(matchOperation):
   self.operation=matchOperation.group(1)
   self.rangeStart=int(matchOperation.group(2))
   self.rangeEnd=int(matchOperation.group(3))

  if(self.rangeStart < 0):
   self.rangeStart=0

  if(self.rangeEnd >=len(self.fileToEditList)-1):
   self.rangeEnd=len(self.fileToEditList)-1

  if(self.operation not in ("comment out", "comment in")):
   self.statusBox.Text="Invalid operation: %s" % self.operation
   return

  if(self.operation=="comment out"):
   self.comment_out()

  if(self.operation=="comment in"):
   self.comment_in()

 def comment_out(self):
  for lineIndex in range(self.rangeStart,self.rangeEnd+1):
   lineToEdit=self.fileToEditList[lineIndex]
   lineToEdit=self.commentCharacter+lineToEdit
   self.fileToEditList[lineIndex]=lineToEdit

 def comment_in(self):
  for lineIndex in range(self.rangeStart,self.rangeEnd+1):
   lineToEdit=self.fileToEditList[lineIndex]
   matchCommentLine=re.match(r'(\s*%s)'%self.commentCharacter,lineToEdit)
   if(matchCommentLine):
    lineToEdit=lineToEdit.replace(r'%s'%self.commentCharacter, "",1)
   self.fileToEditList[lineIndex]=lineToEdit




