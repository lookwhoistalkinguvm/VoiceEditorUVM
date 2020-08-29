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
import os
from VoiceEditorSettings import VoiceEditorSettings
from FastButtonRenderButtons import FastButtonRenderButtons
from FastButtonAreaPage import FastButtonAreaPage
from CmdEditFilter import CmdEditFilter

class FastButtonMarkers(FastButtonRenderButtons):

 #line markers for easy reference
 lineMarkersByFile={}



 def __init__(self,voiceEditor):

  FastButtonRenderButtons.__init__(self,voiceEditor)

  self.fileToEditListFilteredLineNumbers=[]

  self.isCmdEditFilter=False
  if(isinstance(self.voiceEditor.cmdBoxHandler.cmd, CmdEditFilter)):
   self.isCmdEditFilter=True

  if (
     not self.voiceEditor.cmdBoxHandler.is_instance_of_cmdedit(self.voiceEditor.cmdBoxHandler.cmd)
     and not self.isCmdEditFilter
     ):

   self.voiceEditor.statusBox.Text="Must be editing a file to use markers"

  else:

   self.page=FastButtonAreaPage("page")
   self.variableList=[]
   self.currentContext=""
   self.controlButtonsInitial=["top","bottom", "mark", "delete", "delete all"]

   if(self.isCmdEditFilter):
    self.fullFileName=self.voiceEditor.cmdBoxHandler.cmd.parent.fullFileName
    self.fileToEditListFilteredLineNumbers=\
     self.voiceEditor.cmdBoxHandler.cmd.fileToEditListFilteredLineNumbers
   else:
    self.fullFileName=self.voiceEditor.cmdBoxHandler.cmd.fullFileName

   self.fileToEditList=self.voiceEditor.cmdBoxHandler.cmd.fileToEditList

   self.assign_variable_list()
   self.render_fast_button_area()



 def processCommand(self,fastCommand):


  self.nextCommand=self
  self.isCmdEditFilter=False

  if(isinstance(self.voiceEditor.cmdBoxHandler.cmd, CmdEditFilter)):
   self.isCmdEditFilter=True
   self.fileToEditListFilteredLineNumbers=\
    self.voiceEditor.cmdBoxHandler.cmd.fileToEditListFilteredLineNumbers

  if (
   not self.voiceEditor.cmdBoxHandler.is_instance_of_cmdedit(self.voiceEditor.cmdBoxHandler.cmd)
   and not self.isCmdEditFilter
   ):


   self.voiceEditor.statusBox.Text="Must be editing a file to use markers"
   self.nextCommand=None

  else:


   currentLineNumber=self.voiceEditor.cmdBoxHandler.cmd.currentEditLine
   currentLine=self.fileToEditList[currentLineNumber]

   if (fastCommand=="top"):
    self.set_current_edit_line_to(0)
    self.voiceEditor.editBox.Text=self.fileToEditList[0]
    self.voiceEditor.cmdBoxHandler.cmd.displayFile()

   elif (fastCommand=="bottom"):
    self.set_current_edit_line_to(len(self.fileToEditList)-1)
    self.voiceEditor.editBox.Text=self.fileToEditList[len(self.fileToEditList)-1]
    self.voiceEditor.cmdBoxHandler.cmd.displayFile()

   elif (fastCommand=="mark"):


    if (not self.fullFileName in FastButtonMarkers.lineMarkersByFile.keys()):
     FastButtonMarkers.lineMarkersByFile[self.fullFileName]=[]
     if(self.isCmdEditFilter):
      for lineNumberToAppend in self.fileToEditListFilteredLineNumbers:
       FastButtonMarkers.lineMarkersByFile[self.fullFileName].append(lineNumberToAppend)
     else:
      FastButtonMarkers.lineMarkersByFile[self.fullFileName]=[currentLineNumber]
    else:
     lineNumberList=FastButtonMarkers.lineMarkersByFile[self.fullFileName]
     if(self.isCmdEditFilter):
      for lineToAppend in self.fileToEditListFilteredLineNumbers:
       if ( not lineToAppend in lineNumberList):
        lineNumberList.append(lineToAppend)
     else:
      if ( not currentLineNumber in lineNumberList):
       lineNumberList.append(currentLineNumber)
    self.assign_variable_list()
    self.render_fast_button_area()

   elif (fastCommand=="delete"):
    if (self.fullFileName in FastButtonMarkers.lineMarkersByFile.keys()):
     if (currentLineNumber in FastButtonMarkers.lineMarkersByFile[self.fullFileName]):
      FastButtonMarkers.lineMarkersByFile[self.fullFileName].remove(currentLineNumber)
    self.assign_variable_list()
    self.render_fast_button_area()


   elif (fastCommand=="delete all"):
    if (self.fullFileName in FastButtonMarkers.lineMarkersByFile.keys()):
     del FastButtonMarkers.lineMarkersByFile[self.fullFileName]
    self.assign_variable_list()
    self.render_fast_button_area()


   elif (fastCommand.isdigit()):
    lineNumber=(FastButtonMarkers.lineMarkersByFile[self.fullFileName])[int(fastCommand)]
    self.set_current_edit_line_to(lineNumber)

   else:

    self.nextCommand=None

  return self.nextCommand



 def set_current_edit_line_to(self,newEditLine):

  if(self.isCmdEditFilter):
   self.voiceEditor.cmdBoxHandler.processCmd("%d"%newEditLine)
  else:
   self.voiceEditor.cmdBoxHandler.cmd.currentEditLine=newEditLine
   self.voiceEditor.cmdBoxHandler.cmd.displayFile()


 def assign_variable_list(self):

  self.variableList=[]
  self.fileToEditList=self.voiceEditor.cmdBoxHandler.cmd.fileToEditList

  if(self.fullFileName in FastButtonMarkers.lineMarkersByFile.keys()):
   lineNumberList=FastButtonMarkers.lineMarkersByFile[self.fullFileName]
   for lineNumber in lineNumberList:
    self.variableList.append("%0d %s"%(lineNumber,self.fileToEditList[lineNumber]))



 @staticmethod
 def adjust_markers(fullFileName,rangeStart,rangeDelta):


  if(fullFileName not in FastButtonMarkers.lineMarkersByFile):
   return

  for index,marker in enumerate(FastButtonMarkers.lineMarkersByFile[fullFileName]):

   if (marker<=rangeStart):
    continue

   if (rangeDelta<0):
    rangeEnd=rangeStart-rangeDelta
   else:
    rangeEnd=rangeStart+rangeDelta

   if (marker<=rangeEnd and rangeDelta<0):
    del FastButtonMarkers.lineMarkersByFile[fullFileName][index]
    continue

   marker+=rangeDelta

   FastButtonMarkers.lineMarkersByFile[fullFileName][index]=marker
