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


class FastButtonListVariables(FastButtonRenderButtons):


 historyList=[]


 def __init__(self,voiceEditor,fileToParseName=""):

  FastButtonRenderButtons.__init__(self,voiceEditor)

  self.controlButtonsInitial=["class","local","hierarchical","function","loop","history","backup","load"]

  self.currentContext=fileToParseName
  self.loopVariableList=[]
  self.classVariableList=[]
  #self.functionCallsList=[]
  self.localVariableList=[]
  self.hierarchicalVariableList=[]
  self.functionNameList=[]
  #self.variableList=[]
  self.nextCommand=None
  #self.fastCommand=None
  self.activeCommand=None
  #self.boxList=[]
  #self.buttonList=[]
  self.pageLoop=FastButtonAreaPage("pageLoop")
  self.pageClass=FastButtonAreaPage("pageClass")
  self.pageFunction=FastButtonAreaPage("pageFunction")
  self.pageLocal=FastButtonAreaPage("pageLocal")
  self.pageHierarchical=FastButtonAreaPage("hierarchical")
  self.pageHistory=FastButtonAreaPage("history")
  self.page=self.pageClass
  self.variableList=self.classVariableList
  self.fileToParseName=fileToParseName
  self.fileToParseList=[]
  #self.voiceEditor=voiceEditor

  if(not self.open_file_to_parse()):
   return None

  self.extract_variables()
  self.render_fast_button_area()



 def processCommand(self,fastCommand):

  self.fastCommand=fastCommand

  self.nextCommand=None

  if (self.fastCommand=="loop"):
   self.activeCommand="loop"
   self.page=self.pageLoop
   self.variableList=self.loopVariableList
   self.render_fast_button_area()
   self.nextCommand=self

  if (self.fastCommand=="class"):
   self.activeCommand="class"
   self.page=self.pageClass
   self.variableList=self.classVariableList
   self.render_fast_button_area()
   self.nextCommand=self

  if (self.fastCommand=="local"):
   self.activeCommand="local"
   del self.localVariableList[:]
   if (self.extract_variables()):
    self.page=self.pageLocal
    self.variableList=self.localVariableList
    self.render_fast_button_area()
    self.nextCommand=self
   else:
    self.voiceEditor.statusBox.Text="Unable to extract variables"
    self.nextCommand=None

  if (self.fastCommand=="hierarchical"):
   self.activeCommand="hierarchical"
   self.page=self.pageHierarchical
   self.variableList=self.hierarchicalVariableList
   self.render_fast_button_area()
   self.nextCommand=self

  if (self.fastCommand=="function"):
   self.activeCommand=" function"
   self.page=self.pageFunction
   self.variableList=self.functionNameList
   self.render_fast_button_area()
   self.nextCommand=self

  if (self.fastCommand=="history"):
   self.activeCommand="history"
   self.page=self.pageHistory
   self.variableList=self.historyList
   self.render_fast_button_area()
   self.nextCommand=self

  if (self.fastCommand=="backup"):
   self.activeCommand="backup"
   self.backup_variable_list()
   self.render_fast_button_area()
   self.nextCommand=self

  if (self.fastCommand=="load"):
   self.activeCommand="load"
   self.load_variable_list()
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

  if (self.fastCommand.isdigit()):

   if (int(self.fastCommand)<len(self.variableList)):

    if (self.activeCommand in ["history", "load"]):

     self.voiceEditor.destroy_fast_buttons_and_boxes()
     fileName=self.historyList[int(self.fastCommand)]
     self.nextCommand=FastButtonListVariables(self.voiceEditor,fileName)
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
      self.voiceEditor.statusBox.Text="This fast but in only works when editing a file"

   else:
    self.voiceEditor.statusBox.Text="Coding error, fast button out of range: %d"%int(self.fastCommand)




  if (self.nextCommand==None):
   self.destroy_fast_buttons_and_boxes()


  return self.nextCommand



 def extract_variables(self):

  (localStart,localEnd)=self.get_local_range()

  lineNumber=0

  for line in self.fileToParseList:

   matchLoopDefinition=re.match(r'\s*for\s(?P<loopVariable>.*)in\s(?P<loopObject>.*):',line)
   if(matchLoopDefinition):
    loopVariable=matchLoopDefinition.group("loopVariable")
    loopObject=matchLoopDefinition.group("loopObject")
    if (loopVariable not in self.loopVariableList):
     self.loopVariableList.append(loopVariable.strip())
    if (loopObject not in self.loopVariableList):
     self.loopVariableList.append(loopObject.strip())
    continue

   matchFunctionDefinition=re.match(r'\s*def',line)
   matchEqualSign=re.search(r'=',line)
   matchCommentLine=re.match(r'\s*[#]',line)
   if ( not (matchEqualSign or matchFunctionDefinition) or matchCommentLine):
    lineNumber+=1
    continue

   leftHandSide=line.split(r'=')

   identifierIterator=re.finditer\
   (
   r'''
      (?P<printStatement>^\s*print)
    | (?P<comment>^\s*\#)
    | (^\s*def\s+(?P<functionIdentifier>[_A-Za-z]+))
    | (?P<identifier>[A-Za-z][.A-Za-z\[\]]+)
   ''',
   leftHandSide[0],
   re.VERBOSE
   )

   for matchIdentifier in identifierIterator:

    identifier=matchIdentifier.group("identifier")
    functionIdentifier=matchIdentifier.group("functionIdentifier")

    if (functionIdentifier):
     self.functionNameList.append("self."+functionIdentifier+"([])")

    if(identifier):

     if(keyword.iskeyword(identifier)):
      continue

     matchClass=re.match(r'self[.]',identifier)
     matchHierarchical=re.search(r'[.]',identifier)

     if (matchClass):
      if (identifier not in self.classVariableList):
       self.classVariableList.append(identifier)
     elif (matchHierarchical):
      if (identifier not in self.hierarchicalVariableList):
       self.hierarchicalVariableList.append(identifier)
     elif (lineNumber>=localStart and lineNumber<localEnd):
      if (identifier not in self.localVariableList):
       self.localVariableList.append(identifier)

   lineNumber+=1

  self.loopVariableList.sort()
  self.classVariableList.sort()
  self.localVariableList.sort()
  self.functionNameList.sort()
  self.hierarchicalVariableList.sort()
  self.localVariableList.sort()

  numberOfFastButtonsPerPage=VoiceEditorSettings.numberOfFastButtonsPerPage
  self.pageLoop.max=len(self.loopVariableList)//numberOfFastButtonsPerPage
  self.pageClass.max=len(self.classVariableList)//numberOfFastButtonsPerPage
  self.pageLocal.max=len(self.localVariableList)//numberOfFastButtonsPerPage
  self.pageFunction.max=len(self.functionNameList)//numberOfFastButtonsPerPage
  self.pageHierarchical.max=\
   len(self.hierarchicalVariableList)//numberOfFastButtonsPerPage

  return True



 def get_local_range(self):

  lineNumber=0
  localStart=0
  localEnd=len(self.fileToParseList)-1
  currentEditLine=self.voiceEditor.cmdBoxHandler.cmd.currentEditLine

  for line in self.fileToParseList:
   matchFunctionIdentifier=re.match(r'\s*def\s+(?P<functionIdentifier>([_A-Za-z]+))',line)
   if (matchFunctionIdentifier):
    functionIdentifier=matchFunctionIdentifier.group("functionIdentifier")
    if(functionIdentifier):
     if (lineNumber<=currentEditLine):
      localStart=lineNumber
     if (lineNumber>currentEditLine):
      localEnd=lineNumber
      break
   lineNumber+=1

  return (localStart, localEnd)




 def backup_variable_list(self):

  fileName=VoiceEditorSettings.variableListBackupFileName
  try:
   backupFile=open(fileName,"w")
  except:
   self.voiceEditor.statusBox.Text="Unable to open file for writing: %s"%fileName
   return

  for file in self.historyList:
   backupFile.write(file+"\n")



 def load_variable_list(self):

  fileName=VoiceEditorSettings.variableListBackupFileName
  try:
   backupFile=open(fileName,"r")
  except:
   self.voiceEditor.statusBox.Text="Unable to open file for reading: %s"%fileName
   return

  for fileLine in backupFile.readlines():

   matchCommentLine=re.match(r'\s*#',fileLine)
   if (matchCommentLine):
    continue

   fileToAdd=fileLine.strip()
   if (fileToAdd not in self.historyList):
    self.historyList.append(fileToAdd)

  backupFile.close()



 def open_file_to_parse(self):


  if (self.fileToParseName==""):
   if(isinstance(self.voiceEditor.cmdBoxHandler.cmd,CmdEdit)):
    self.fileToParseName=self.voiceEditor.cmdBoxHandler.cmd.fullFileName


  if (self.fileToParseName==""):
   return False


  if (self.fileToParseName not in self.historyList):
   self.historyList.append(self.fileToParseName)

  if ( not os.path.exists(self.fileToParseName)):
   #this can happen if the file has been deleted since we saved the history list
   self.statusBox.Text="File no longer exists "+self.fileToParseName
   return False

  try:
   fileToParse=open(self.fileToParseName,"r")
  except:
   self.statusBox.Text="unable to open file: "+self.fileToParseName+" read mode: "
   return False

  for fileLine in fileToParse.readlines():
   self.fileToParseList.append(fileLine.rstrip())

  self.currentContext=self.fileToParseName

  return True

