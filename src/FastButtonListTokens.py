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
from FastButtonRenderButtons import FastButtonRenderButtons
from string import join
from CmdEditSubstitute import CmdEditSubstitute


class FastButtonListTokens(FastButtonRenderButtons):


 historyList=[]
 inverse=0


 def __init__(self,voiceEditor):

  FastButtonRenderButtons.__init__(self,voiceEditor)

  self.controlButtonsInitial=["inverse"]

  self.currentEditLine=self.voiceEditor.cmdBoxHandler.cmd.currentEditLine
  self.fileToEditList=self.voiceEditor.cmdBoxHandler.cmd.fileToEditList
  lineToTokenise=self.fileToEditList[self.currentEditLine]

  self.page=FastButtonAreaPage("page")
  self.currentContext=' inverse: %d '%(FastButtonListTokens.inverse)
  self.tokenList=[]
  self.nextCommand=None

  while(len(lineToTokenise)):

   matchWordCharacter=re.match(r'(\w+)',lineToTokenise)
   matchNotWordCharacter=re.match(r'(\W+)',lineToTokenise)

   if(matchWordCharacter):
    token=lineToTokenise[0:matchWordCharacter.end(0)]
    lineToTokenise=lineToTokenise[matchWordCharacter.end(0):]

   if (matchNotWordCharacter):
    token=lineToTokenise[0:matchNotWordCharacter.end(0)]
    lineToTokenise=lineToTokenise[matchNotWordCharacter.end(0):]

   self.tokenList.append(token)


  self.variableList=self.tokenList


  self.render_fast_button_area()



 def processCommand(self,fastCommand):


  self.fastCommand=fastCommand

  self.nextCommand=None

  if(self.fastCommand=="inverse"):
   self.activeCommand="inverse"
   self.nextCommand=self
   if(FastButtonListTokens.inverse):
    FastButtonListTokens.inverse=0
   else:
    FastButtonListTokens.inverse=1
   self.currentContext=' inverse: %d '%(FastButtonListTokens.inverse)
   self.render_fast_button_area()

  if (self.fastCommand.isdigit()):

   if (int(self.fastCommand)<len(self.variableList)):

    if(FastButtonListTokens.inverse):
     buttonNumber=int(self.fastCommand)
     lowerText=self.variableList[0:buttonNumber]
     upperText=self.variableList[buttonNumber+1:]
     textToInsert=join(lowerText,"")+join(upperText,"")
    else:
     textToInsert=self.variableList[int(self.fastCommand)]

    if (isinstance(self.voiceEditor.cmdBoxHandler.cmd,CmdEdit)):

     if (self.voiceEditor.activeEntryWindow=="edit"):

      if(FastButtonListTokens.inverse):
       self.voiceEditor.editBox.Text=textToInsert
      else:
       self.voiceEditor.cmdBoxHandler.cmd.insert_in_edit_box_at_cursor_position(textToInsert)

     else:

      if(FastButtonListTokens.inverse):
       self.voiceEditor.cmdBox.Text=textToInsert
      else:
       self.voiceEditor.cmdBoxHandler.cmd.insert_in_cmd_box_at_cursor_position(textToInsert)

     self.nextCommand=self

    elif (
     isinstance(self.voiceEditor.cmdBoxHandler.cmd,CmdEditFilter) or
     isinstance(self.voiceEditor.cmdBoxHandler.cmd,CmdEditSubstitute)
    ):

     if (self.voiceEditor.activeEntryWindow=="edit"):

      if(FastButtonListTokens.inverse):
       self.voiceEditor.editBox.Text=textToInsert
      else:
       self.voiceEditor.cmdBoxHandler.cmd.parent.insert_in_edit_box_at_cursor_position(textToInsert)

     else:

      if(FastButtonListTokens.inverse):
       self.voiceEditor.cmdBox.Text=textToInsert
      else:
       self.voiceEditor.cmdBoxHandler.cmd.parent.insert_in_cmd_box_at_cursor_position(textToInsert)

     self.nextCommand=self

    else:

     self.voiceEditor.statusBox.Text="Fast buttons only work when editing or filtering a file"


  if (self.nextCommand==None):
   self.destroy_fast_buttons_and_boxes()


  return self.nextCommand



