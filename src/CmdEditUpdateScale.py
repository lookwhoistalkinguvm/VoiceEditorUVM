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
import re

class CmdEditUpdateScale(object):

 def __init__(self,scaleBox,editBox,statusBox):

  self.editBox=editBox
  self.statusBox=statusBox
  self.scaleBox=scaleBox
  self.widthScaleBox=VoiceEditorSettings.widthScaleBox
  self.lower_scale=[]
  self.upper_scale=[]
  self.lower_scale_string=""
  self.upper_scale_string=""
  self.reset_scale()


 def __call__(self,command):

  if(self.widthScaleBox<len(self.editBox.Text)):
   self.statusBox.Text="scale function only works for strings that are less %d characters long"%self.widthScaleBox
   return

  if(command == "scale letters"):
   self.scale_letters()
  elif(command =="scale words"):
   self.scale_words()
  else:
   self.statusBox.Text=" Unknown scale command:%s"% command



 def scale_letters(self):

  self.scaleBox.Text=""
  self.reset_scale()

  editCursorPosition=self.editBox.SelectionStart

  for position in range(0,editCursorPosition):
   self.upper_scale[position]="%d"%((editCursorPosition-position)//10)
   self.lower_scale[position]="%s"%((editCursorPosition-position)%10)

  scaleEnd=min(self.widthScaleBox-1,len(self.editBox.Text))
  for position in range(editCursorPosition,scaleEnd):
   scale_value=position-editCursorPosition+1
   self.upper_scale[position]="%d"%((scale_value)//10)
   self.lower_scale[position]="%s"%((scale_value)%10)

  for i in range(0,self.widthScaleBox -1):
   self.upper_scale_string="".join(self.upper_scale)
   self.lower_scale_string="".join(self.lower_scale)

  self.scaleBox.AppendText(self.upper_scale_string+ "\r\n")
  self.scaleBox.AppendText(self.lower_scale_string)



 def scale_words(self):

  self.scaleBox.Text=""
  self.reset_scale()

  editCursorPosition=self.editBox.SelectionStart

  #generate scale to the left of the current cursor position in the edit box

  wordCount=0
  matchCountsAsOneWord=None
  matchCharacterOnWordBoundary=None

  for position in range(editCursorPosition-1,-1,-1):

   #examine current character in edit box to see if it is on the word boundary
   if (position>0):
    editBoxSliceBeingSearched=self.editBox.Text[position-1:position+1]
    matchCharacterOnWordBoundary=re.match(r'[^a-zA-Z][[a-zA-Z]',editBoxSliceBeingSearched)
    matchCountsAsOneWord=re.match(r"[a-zA-Z'][']",editBoxSliceBeingSearched)
   else:
    matchCharacterOnWordBoundary=None

   #examine current character in edit box to see if it is a non-word character
   matchNonWord=re.match(r'[^a-zA-Z\s]',self.editBox.Text[position])

   #assemble scale string
   if(matchCharacterOnWordBoundary or (matchNonWord and not matchCountsAsOneWord) or position==0):

#   if(matchCharacterOnWordBoundary):
    wordCount=wordCount+1
    self.upper_scale[position]="%d"%(wordCount//10)
    self.lower_scale[position]="%s"%(wordCount%10)

   if(wordCount==30):
    break

  #generate scale to the right of the current position in the edit box

  scaleEnd=min(self.widthScaleBox-1,len(self.editBox.Text))
  wordCount=0
  matchCharacterOnWordBoundary = None
  matchNonWord=None

  for position in range(editCursorPosition,scaleEnd):

   #examine current character in edit box to see if it is on the word boundary
   if(position<scaleEnd-2):
    editBoxSliceBeingSearched=self.editBox.Text[position:position+2]
    matchCharacterOnWordBoundary=re.match(r'[a-zA-Z][^a-zA-Z]',editBoxSliceBeingSearched)
    matchCountsAsOneWord=re.match(r"[a-zA-Z'][']",editBoxSliceBeingSearched)
   else:
    matchCharacterOnWordBoundary=None

   #examine current character in edit box to see if it is a non-word character
   matchNonWord=re.match(r'[^a-zA-Z\s]',self.editBox.Text[position])

   #assemble scale string
   if((matchCharacterOnWordBoundary and not matchCountsAsOneWord) or (matchNonWord and not matchCountsAsOneWord) or position==scaleEnd-1):
#   if(matchCharacterOnWordBoundary):
    wordCount=wordCount+1
    self.upper_scale[position]="%d"%(wordCount//10)
    self.lower_scale[position]="%s"%(wordCount%10)

   if(wordCount==30):
    break

  #output scale string to scale box
  for i in range(0,self.widthScaleBox -1):
   self.upper_scale_string="".join(self.upper_scale)
   self.lower_scale_string="".join(self.lower_scale)
  self.scaleBox.AppendText(self.upper_scale_string+ "\r\n")
  self.scaleBox.AppendText(self.lower_scale_string)

 def reset_scale(self):
  del self.lower_scale[:]
  del self.upper_scale[:]
  for i in range(0,self.widthScaleBox):
   self.lower_scale.append(" ")
   self.upper_scale.append(" ")



