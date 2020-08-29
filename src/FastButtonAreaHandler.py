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



from FastButtonListVariables import FastButtonListVariables
from FastButtonCommandFactory import FastButtonCommandFactory
from VoiceEditorSettings import VoiceEditorSettings
from FastButtonMarkers import FastButtonMarkers
from FastButtonTemplates import FastButtonTemplates


class FastButtonAreaHandler(object):

 def __init__(self,voiceEditor):

  self.voiceEditor=voiceEditor
  self.fastButtonCommandFactory=FastButtonCommandFactory(voiceEditor)
  self.command=None



 def processCommand(self,fastCommandString):

  if (self.command==None):
   #No currently active fast button command
   self.command= self.fastButtonCommandFactory.get_command_object(fastCommandString)
   if (self.command==None):
    self.voiceEditor.statusBox.Text="Unknown fast button command: %s "%fastCommandString
  else :
   #Feed supplied command to currently active fast button command
   self.command=self.command.processCommand(fastCommandString)
   if (self.command==None):
    #Supplied command cannot be handled by currently active command
    #therefore it is presumably a new top level fast button command
    self.command=self.fastButtonCommandFactory.get_command_object(fastCommandString)
    if (self.command==None):
     self.voiceEditor.statusBox.Text="Unknown fast button command: %s "%fastCommandString



 def refresh(self):

  if (self.command==None):
   return

  if (isinstance(self.command,FastButtonMarkers)):
   self.command.assign_variable_list()

  self.command.render_fast_button_area()



 def reset(self):


  if (self.command==None):
   return

  if (isinstance(self.command,FastButtonMarkers)):
   self.command=None
   self.voiceEditor.destroy_fast_buttons_and_boxes()



 def is_instance_of_fastbuttontemplates(self,objectToCheck):
  return isinstance(objectToCheck,FastButtonTemplates)




