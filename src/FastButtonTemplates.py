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
from CmdEdit import CmdEdit
from CmdEditFilter import CmdEditFilter
from CmdEditSubstitute import CmdEditSubstitute

class FastButtonTemplates(FastButtonRenderButtons):

 def __init__(self,voiceEditor):

  FastButtonRenderButtons.__init__(self,voiceEditor)

  self.page=FastButtonAreaPage("page")
  self.templateDictionary={}
  self.variableList=[]
  self.currentContext=""
  self.controlButtonsInitial=["back"]
  self.isLeafContext=False
  self.nextLevelContextDeltaList=[]
  self.templateHelpDictionary={}

  if(not self.read_templates()):
   return None

  self.get_choices_at_this_level()


  self.variableList=self.variableList
  self.render_fast_button_area()



 def processCommand(self,fastCommand):


  self.nextCommand=None

  currentContextSplitList=self.currentContext.split(".")
  currentContextBackupOne=".".join(currentContextSplitList[0:len(currentContextSplitList)-1])
  currentContextBackupTwo=".".join(currentContextSplitList[0:len(currentContextSplitList)-2])

  if (fastCommand=="up"):
   self.activeCommand="up"
   if (self.page.number>0):
    self.page.number-=1
   self.render_fast_button_area()
   self.nextCommand=self

  elif (fastCommand=="down"):
   self.activeCommand="down"
   if (self.page.number<self.page.max):
    self.page.number+=1
   self.render_fast_button_area()
   self.nextCommand=self

  elif (fastCommand=="back"):

   self.page.number=0

   if (self.currentContext!=""):
    if (len(currentContextSplitList)==1):
     self.currentContext=""
    else:
     if (self.currentContext in self.templateDictionary.keys()):
      self.currentContext=currentContextBackupTwo
     else:
      self.currentContext=currentContextBackupOne

   self.get_choices_at_this_level()
   self.render_fast_button_area()
   self.nextCommand=self

  elif (fastCommand.isdigit()):

   if (self.currentContext in self.templateDictionary.keys()):
    self.currentContext=currentContextBackupOne

   nextLevelContextDelta=self.nextLevelContextDeltaList[int(fastCommand)]
   if (self.currentContext==""):
    self.currentContext=nextLevelContextDelta
   else:
    self.currentContext=self.currentContext+"."+nextLevelContextDelta

   #if(not self.isLeafContext):
   if (self.currentContext not in self.templateDictionary.keys()):
    self.get_choices_at_this_level()
    self.render_fast_button_area()
   else:
    self.insert_template()

   self.nextCommand=self

  else:

   self.nextCommand=None

  if (self.nextCommand==None):
   self.voiceEditor.destroy_fast_buttons_and_boxes()

  self.voiceEditor.recover_active_window()

  return self.nextCommand




 def read_templates(self):

  templatesDirectory=VoiceEditorSettings.fastButtonTemplatesDirectory
  directoryContent=os.listdir(templatesDirectory)
  insideTemplate=False
  insideHelpTemplate=False

  for templateFileName in directoryContent:


   templateFileName=VoiceEditorSettings.fastButtonTemplatesDirectory+"\\"+templateFileName
   templateList=[]
   templateTuple=[]
   templateName=""

   if (templateFileName.endswith(".backup")):
    continue


   try:
    templateFile=open(templateFileName,"r")
   except:
    self.voiceEditor.statusBox.Text="Unable to open file %s"%templateFileName
    return False

   for line in templateFile :

#    matchComment=re.match(r'\s*#',line)
#    if (matchComment):
#     continue
#    matchEmptyLine=re.match(r'\s*$',line)
#    if (matchEmptyLine):
#     continue

    matchTemplateContext=re.match(r'\s*-template_context\s+(?P<templateContext>[\w.]+)',line)
    if (matchTemplateContext):
     templateContext=matchTemplateContext.group("templateContext")

    matchTemplateName=re.match(r'\s*-template_name\s+(?P<templateName>(.*))',line)
    if (matchTemplateName):
     templateName=matchTemplateName.group("templateName")

    if(line.startswith("-template_end")):
     templateTuple=(templateName,templateList)
     self.templateDictionary[templateContext]=templateTuple
     insideTemplate=False

    if (insideTemplate):
     templateList.append(line.rstrip())

    if(line.startswith("-template_start")):
     templateList=[]
     insideTemplate=True

    ## Template Help String


    if(line.startswith("-template_doc_string_end")):
     self.templateHelpDictionary[templateContext]=templateHelpList
     insideHelpTemplate=False

    if (insideHelpTemplate):
     templateHelpList.append(line.rstrip())

    if(line.startswith("-template_doc_string_start")):
     templateHelpList=[]
     insideHelpTemplate=True

  return True




 def get_choices_at_this_level(self):


  self.variableList=[]
  self.nextLevelContextDeltaList=[]


  if (self.currentContext==""):
   contextDepth=0
  else:
   contextDepth=len(self.currentContext.split("."))


  self.isLeafContext=False


  for templateDictionaryKey in sorted (self.templateDictionary.keys()):
   contextHierarchyList=templateDictionaryKey.split(".")
   if (contextDepth<=len(contextHierarchyList)):
    contextPrefix=".".join(contextHierarchyList[0:contextDepth])
    if (self.currentContext==contextPrefix):
     nextLevelContextDelta=contextHierarchyList[contextDepth]
     nextLevelContext=self.currentContext+"."+nextLevelContextDelta
     if(nextLevelContextDelta not in self.nextLevelContextDeltaList):
      self.nextLevelContextDeltaList.append(nextLevelContextDelta)
     if(nextLevelContext in self.templateDictionary.keys()):
      self.isLeafContext=True
      self.variableList.append((self.templateDictionary[nextLevelContext])[0])
     else:
      if (nextLevelContextDelta not in self.variableList):
       self.variableList.append(nextLevelContextDelta)

  self.page.max=len(self.variableList)//VoiceEditorSettings.numberOfFastButtonsPerPage



 def insert_template(self):

  isFilterCommand=False
  isEditCommand=False
  isSubstituteCommand=False

  if(isinstance(self.voiceEditor.cmdBoxHandler.cmd,CmdEditFilter)):
   isFilterCommand=True

  if(isinstance(self.voiceEditor.cmdBoxHandler.cmd,CmdEditSubstitute)):
   isSubstituteCommand=True

  if (isinstance(self.voiceEditor.cmdBoxHandler.cmd,CmdEdit)):
   isEditCommand=True

  if(
   not isEditCommand
   and not isFilterCommand
   and not isSubstituteCommand
  ):
   self.voiceEditor.statusBox.Text = "Must be editing a file to insert template"
   return False

  if (
   not isFilterCommand
   and not isSubstituteCommand
   and self.voiceEditor.cmdBoxHandler.cmd.is_help_file()
  ):
   self.insert_template_help()
   return

  fileToEditList=self.voiceEditor.cmdBoxHandler.cmd.fileToEditList
  if(not isFilterCommand and not isSubstituteCommand):
   currentEditLine=self.voiceEditor.cmdBoxHandler.cmd.currentEditLine
  editBoxText=self.voiceEditor.editBox.Text
  matchLeadingSpaces=re.match(r'(\s*)',editBoxText)
  leadingSpaces=matchLeadingSpaces.group(1)
  template=(self.templateDictionary[self.currentContext])[1]
  if(len(template) >1):
   if(isFilterCommand or isSubstituteCommand):
    self.voiceEditor.statusBox.Text="Can't insert multi-line template when in filter mode"
   else:
    templateLineNumber=0
    for templateLine in template:
     if (templateLineNumber==0):
      if(fileToEditList[currentEditLine+templateLineNumber]==""):
       offset=0
       fileToEditList[currentEditLine+templateLineNumber]=leadingSpaces+templateLine
      else:
       offset=1
       fileToEditList.insert(currentEditLine+templateLineNumber+offset,leadingSpaces+templateLine)
     else:
      fileToEditList.insert(currentEditLine+templateLineNumber+offset,leadingSpaces+templateLine)
     templateLineNumber+=1
    self.voiceEditor.cmdBoxHandler.cmd.displayFile()
  else:
   if(isFilterCommand or isSubstituteCommand):
    self.voiceEditor.cmdBoxHandler.cmd.parent.insert_in_cmd_box_at_cursor_position(template[0])
   else:
    if (self.voiceEditor.activeEntryWindow=="command"):
     self.voiceEditor.cmdBoxHandler.cmd.insert_in_cmd_box_at_cursor_position(template[0])
    else:
     self.voiceEditor.cmdBoxHandler.cmd.insert_in_edit_box_at_cursor_position(template[0])

  return True



 def insert_template_help(self):

  fileToEditList=self.voiceEditor.cmdBoxHandler.cmd.fileToEditList
  self.voiceEditor.cmdBoxHandler.cmd.processThisCommand("clear file")

  if(self.currentContext in self.templateHelpDictionary.keys()):
   templateLineNumber=0
   template=(self.templateDictionary[self.currentContext])[1]
   for templateLine in template:
    fileToEditList.insert(templateLineNumber,templateLine)
    templateLineNumber+=1
   fileToEditList.insert(templateLineNumber,"")
   templateLineNumber+=1
   for templateLine in self.templateHelpDictionary[self.currentContext]:
    fileToEditList.insert(templateLineNumber,templateLine)
    templateLineNumber+=1
   self.voiceEditor.cmdBoxHandler.cmd.displayFile()





