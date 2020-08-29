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


from VoiceEditorSettings import VoiceEditorSettings


class FastButtonRenderButtons(object):

 def __init__(self,voiceEditor):

  self.voiceEditor=voiceEditor
  self.boxList=[]
  self.buttonList=[]
  self.fastCommand=None
  self.page=None
  self.controlButtonsInitial=[]
  self.controlButtons=[]
  self.variableList=[]
  self.currentContext=""


 def render_fast_button_area(self):


  self.destroy_fast_buttons_and_boxes()
  self.create_control_buttons()
  self.create_variable_buttons_and_boxes()
  self.render_context_box()



 def create_control_buttons(self):

  del self.controlButtons[:]
  self.controlButtons.extend(self.controlButtonsInitial)

  if (self.page.number>0):
   self.controlButtons.append("up")

  if (self.page.number<self.page.max):
   self.controlButtons.append("down")

  horizontalOffset=VoiceEditorSettings.fastControlButtonHorizontalOffset
  horizontalPosition=VoiceEditorSettings.fastControlButtonTopLeftHorizontalPosition
  verticalPosition=VoiceEditorSettings.fastControlButtonTopLeftVerticalPosition
  for control in self.controlButtons:
   self.voiceEditor.create_fast_button(control,horizontalPosition,verticalPosition)
   horizontalPosition+=horizontalOffset



 def create_variable_buttons_and_boxes(self):

  if (self.fastCommand=="history"):
   columnMax=VoiceEditorSettings.fastBoxHistoryColumnMax
   boxWidth=VoiceEditorSettings.fastBoxHistoryWidth
  else:
   columnMax=VoiceEditorSettings.fastButtonColumnMax
   boxWidth=VoiceEditorSettings.fastBoxWidth

  row=0
  column=0
  rowMax=VoiceEditorSettings.fastButtonRowMax
  rowHeight=VoiceEditorSettings.fastButtonRowHeight
  columnWidth=VoiceEditorSettings.fastButtonColumnWidth
  initialHorizontalPosition=\
   VoiceEditorSettings.fastButtonTopLeftHorizontalPosition+columnWidth*(columnMax-1)
  initialVerticalPosition=VoiceEditorSettings.fastButtonTopLeftVerticalPosition

  lower = self.page.number*VoiceEditorSettings.numberOfFastButtonsPerPage
  upper = lower+VoiceEditorSettings.numberOfFastButtonsPerPage


  for variable in self.variableList[lower:upper]:

   horizontalPosition=initialHorizontalPosition-column*columnWidth
   verticalPosition=initialVerticalPosition+row*rowHeight
   buttonNumber=(row+rowMax*column)+self.page.number*VoiceEditorSettings.numberOfFastButtonsPerPage

   buttonName="%d"%buttonNumber
   self.voiceEditor.create_fast_button\
   (
    buttonName,
    horizontalPosition,
    verticalPosition
   )

   boxName="box%d"%buttonNumber
   boxHorizontalPosition=horizontalPosition+VoiceEditorSettings.fastBoxHorizontalOffset
   self.voiceEditor.create_fast_text_box\
   (
    boxName,
    variable,
    boxHorizontalPosition,
    verticalPosition,
    boxWidth
   )

   self.buttonList.append(buttonName)
   self.boxList.append(boxName)

   row=(row+1)%rowMax
   if (row==0):
    column+=1
   if (column==columnMax):
    self.voiceEditor.statusBox.Text="Unable to list all variables in available fast button space"
    break



 def destroy_fast_buttons_and_boxes(self):

  self.voiceEditor.destroy_fast_buttons_and_boxes()



 def render_context_box(self):

  boxName="contextBox"
  self.voiceEditor.create_fast_text_box\
  (
   boxName,
   self.currentContext,
   VoiceEditorSettings.fastButtonTopLeftHorizontalPosition,
   VoiceEditorSettings.fastContextBoxVerticalPosition,
   VoiceEditorSettings.fastContextBoxWidth
  )


