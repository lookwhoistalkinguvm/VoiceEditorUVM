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


import sys
import re

from VoiceEditorSettings import VoiceEditorSettings

class CmdEditExpandCamelBackIdentifiers(object):



 def __init__(self,parent,fileToEditList,currentEditLine,allTheBoxes):

  (self.cmdBox,
       self.editBox,
           self.scaleBox,
               self.viewBox,
                   self.statusBox)=allTheBoxes

  self.fileToEditList=fileToEditList
  self.currentEditLine=currentEditLine
  self.parent=parent
  self.filterList=[]
  self.isFilterEnabled=0
  self.fileToEditListFiltered=[]



 def __call__(self):

  editBoxText=self.editBox.Text+""
  editBoxText=editBoxText.rstrip()

  iterator=re.finditer(
   r'''
   (?P<apostrophe>\'.*?\')
   | (?P<quotes>".*?")
   | (?P<unquoted>[^"\']+)
   ''',
   editBoxText,
   re.VERBOSE
  )

  expandedString=""

  for match in iterator:
   if(match.group("unquoted")):
    unquotedString=match.group("unquoted")
    expandedString=expandedString+self.expand_unquoted(unquotedString)
   if(match.group("quotes")):
    quotedString=match.group("quotes")
    expandedString=expandedString+quotedString
   if(match.group("apostrophe")):
    quotedString=match.group("apostrophe")
    expandedString=expandedString+quotedString

  self.editBox.Text=expandedString

  return self.parent

 def expand_unquoted(self, unquotedText):

  expandedString=""

  ##Expand camel case identifiers

  iterator=re.finditer(
  r'''
   #uppercase letter
   (?P<uppercaseLetter>[A-Z])
   #anything that is not an uppercase letter
   |(?P<notAnUppercaseLetter>[^A-Z]+)
  ''',unquotedText, re.VERBOSE)

  for match in iterator:


   uppercaseLetter=match.group("uppercaseLetter")
   notAnUppercaseLetter=match.group("notAnUppercaseLetter")

   if(match.group("notAnUppercaseLetter")):
    expandedString=expandedString+notAnUppercaseLetter

   if(match.group("uppercaseLetter")):
    if(expandedString=="" or expandedString[-1]==" "):
     expandedString=expandedString+uppercaseLetter
    else:
     expandedString=expandedString+" "+uppercaseLetter



  ##put spaces between words and other characters

  inputString=expandedString
  expandedString=""

  iterator=re.finditer(
  r'''
   #any non-letter
   (?P<anyNotWord>[^A-Za-z_]+)
   #any letter
   |(?P<anyWord>[A-Za-z_]+)
  ''',inputString, re.VERBOSE)

  for match in iterator:

   anyNotWord=match.group("anyNotWord")
   anyWord=match.group("anyWord")


   if(match.group("anyNotWord")):
    if(anyNotWord[0]==" "):
     expandedString=expandedString+anyNotWord
    else:
     expandedString=expandedString+" "+anyNotWord

   if(match.group("anyWord")):
    if((expandedString=="") or expandedString[-1]==" "):
     expandedString=expandedString+anyWord
    else:
     expandedString=expandedString+" "+anyWord


  return expandedString















