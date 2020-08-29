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
import keyword
import os
from CmdEdit import CmdEdit
from VoiceEditorSettings import VoiceEditorSettings
from FastButtonAreaPage import FastButtonAreaPage
from CmdEditFilter import CmdEditFilter
from CmdEditSubstitute import CmdEditSubstitute
from FastButtonRenderButtons import FastButtonRenderButtons
from ScanFileForVariables import ScanFileForVariables
from SystemVerilogKeywords import SystemVerilogKeywords


class FastButtonListUVMVariables(FastButtonRenderButtons):


 historyList=[]


 def __init__(self,voiceEditor,fileToParseName=""):

  self.systemVerilogKeywords=SystemVerilogKeywords()

  FastButtonRenderButtons.__init__(self,voiceEditor)

  self.controlButtonsInitial=["class","method","history","tokens","mapping"]

  self.currentContext=fileToParseName
  self.classVariablesList=[]
  self.methodVariablesList=[]
  self.tokenList=[]
  self.mappingVariablesList=[]
  self.nextCommand=None
  self.activeCommand=None
  self.pageClass=FastButtonAreaPage("pageClass")
  self.pageMapping=FastButtonAreaPage("pageMapping")
  self.pageMethod=FastButtonAreaPage("pageMethod")
  self.pageTokens=FastButtonAreaPage("tokenList")
  self.page=self.pageClass
  self.pageHistory=FastButtonAreaPage("history")
  self.variableList=self.methodVariablesList
  self.fileToParseName=fileToParseName

  self.extract_variables()
  self.activeCommand="class"
  self.page=self.pageClass
  self.variableList=self.classVariablesList
  self.render_fast_button_area()




 def processCommand(self,fastCommand):


  self.fastCommand=fastCommand

  self.nextCommand=None

  if (self.fastCommand == "class"):
   self.activeCommand="class"
   self.page=self.pageClass
   self.variableList=self.classVariablesList
   self.render_fast_button_area()
   self.nextCommand=self

  if (self.fastCommand=="method"):
   self.activeCommand="method"
   self.page=self.pageMethod
   self.variableList=self.methodVariablesList
   self.render_fast_button_area()
   self.nextCommand=self

  if (self.fastCommand=="tokens"):
   self.activeCommand="tokens"
   self.page=self.pageTokens
   self.variableList=self.tokenList
   self.render_fast_button_area()
   self.nextCommand=self

  if (self.fastCommand == "mapping"):
   self.activeCommand="mapping"
   self.page=self.pageMapping
   self.variableList=self.mappingVariablesList
   self.render_fast_button_area()
   self.nextCommand=self

  if (self.fastCommand=="up"):
   self.activeCommand="up"
   if (self.page.number>0):
    self.page.number-=1
   self.render_fast_button_area()
   self.nextCommand=self

  if (self.fastCommand=="down"):
   self.activeCommand="down"
   if (self.page.number<self.page.max):
    self.page.number+=1
   self.render_fast_button_area()
   self.nextCommand=self

  if (self.fastCommand=="history"):
   self.activeCommand="history"
   self.page=self.pageHistory
   self.variableList=self.historyList
   self.render_fast_button_area()
   self.nextCommand=self

  if (self.fastCommand.isdigit()):

   if (int(self.fastCommand)<len(self.variableList)):

    if (self.activeCommand in ["history", "load"]):

     self.voiceEditor.destroy_fast_buttons_and_boxes()
     fileName=self.historyList[int(self.fastCommand)]
     self.nextCommand=FastButtonListUVMVariables(self.voiceEditor,fileName)
     self.nextCommand.processCommand("class")

    else:

     if (isinstance(self.voiceEditor.cmdBoxHandler.cmd,CmdEdit)):
      textToInsert=self.variableList[int(self.fastCommand)]
      if (self.voiceEditor.activeEntryWindow=="edit"):
       self.voiceEditor.cmdBoxHandler.cmd.insert_in_edit_box_at_cursor_position(textToInsert)
      else:
       self.voiceEditor.cmdBoxHandler.cmd.insert_in_cmd_box_at_cursor_position(textToInsert)
      self.nextCommand=self
     elif (
      isinstance(self.voiceEditor.cmdBoxHandler.cmd,CmdEditFilter) or
      isinstance(self.voiceEditor.cmdBoxHandler.cmd,CmdEditSubstitute)
     ):
      textToInsert=self.variableList[int(self.fastCommand)]
      if (self.voiceEditor.activeEntryWindow=="edit"):
       self.voiceEditor.cmdBoxHandler.cmd.parent.insert_in_edit_box_at_cursor_position(textToInsert)
      else:
       self.voiceEditor.cmdBoxHandler.cmd.parent.insert_in_cmd_box_at_cursor_position(textToInsert)
      self.nextCommand=self
     else:
      self.voiceEditor.statusBox.Text="Fast buttons only works when editing a file"

   else:
    self.voiceEditor.statusBox.Text="Coding error, fast button out of range: %d"%int(self.fastCommand)




  if (self.nextCommand==None):
   self.destroy_fast_buttons_and_boxes()


  return self.nextCommand



 def extract_variables(self):


  if (self.fileToParseName!=""):

   fullFileName=self.fileToParseName
   currentEditLine=0

  else:

   fullFileName=self.voiceEditor.cmdBoxHandler.cmd.fullFileName
   currentEditLine=self.voiceEditor.cmdBoxHandler.cmd.currentEditLine


  if (fullFileName not in self.historyList):
   self.historyList.append(fullFileName)


  scanFileForVariables=ScanFileForVariables()
  scanFileForVariables(fullFileName,currentEditLine)
  self.classVariablesList=scanFileForVariables.classVariableList


  if (scanFileForVariables.interfaceName):

   self.mappingVariablesList.append(r'\[[]\]')

   for variable in scanFileForVariables.classVariableList:
    self.mappingVariablesList.append('[%s0].%s'%(scanFileForVariables.interfaceName, variable))

  else:

   for variable in scanFileForVariables.classVariableList:
    self.mappingVariablesList.append('.%s([]),'%(variable))


  if(scanFileForVariables.className):
   self.classVariablesList.insert(0,scanFileForVariables.className)


  if(scanFileForVariables.interfaceName):
   self.classVariablesList.insert(0,scanFileForVariables.interfaceName)


  if (scanFileForVariables.moduleName):
   self.classVariablesList.insert(0,scanFileForVariables.moduleName)


  self.methodVariablesList=scanFileForVariables.methodVariableList
  self.tokenList=scanFileForVariables.tokenList
  self.tokenList=list(set(self.tokenList)-set(self.systemVerilogKeywords.keywordsList))
  self.tokenList=sorted(self.tokenList)

  numberOfFastButtonsPerPage=VoiceEditorSettings.numberOfFastButtonsPerPage
  self.pageClass.max=len(self.classVariablesList)//numberOfFastButtonsPerPage
  self.pageMethod.max=len(self.methodVariablesList)//numberOfFastButtonsPerPage
  self.pageTokens.max=len(self.tokenList)//numberOfFastButtonsPerPage



  return True



