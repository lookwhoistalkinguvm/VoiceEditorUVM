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

from VoiceEditorSettings import VoiceEditorSettings

class CmdEditContractLine(object):



 def __init__(self,parent,fileToEditList,currentEditLine,allTheBoxes):

  (self.cmdBox,
       self.editBox,
           self.scaleBox,
               self.viewBox,
                   self.statusBox)=allTheBoxes

  self.fileToEditList=fileToEditList
  self.currentEditLine=currentEditLine
  self.parent=parent



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

  contractedString=""
  preserveLeadingSpaces=True

  for match in iterator:

   if(match.group("unquoted")):
    unquotedString=match.group("unquoted")
    contractedString=\
     contractedString\
     +self.expand_unquoted(unquotedString,preserveLeadingSpaces)

   if(match.group("quotes")):
    quotedString=match.group("quotes")
    contractedString=contractedString+quotedString

   if(match.group("apostrophe")):
    quotedString=match.group("apostrophe")
    contractedString=contractedString+quotedString

   preserveLeadingSpaces=False

  contractedString=self.remove_brackets(contractedString)

  self.editBox.Text=contractedString

  return self.parent

 def expand_unquoted(self,unquotedText,preserveLeadingSpaces):

  iterator=re.finditer(
   r'''
    (?P<leadingSpaces>^\s+)
    | (?P<notWord>[^A-Za-z]+)
    | (?P<aWord>[A-Za-z]+)
   ''',
   unquotedText,
   re.VERBOSE
  )

  contractedString=""
  lastAppendedWord=""

  for match in iterator:

   notWord=match.group("notWord")
   aWord=match.group("aWord")
   leadingSpaces=match.group("leadingSpaces")
   lastAppendedWord=""
   assert notWord==None or aWord==None

   if(leadingSpaces):
    if(preserveLeadingSpaces):
     contractedString=contractedString+leadingSpaces

   if(notWord):
    notWord=re.sub(r' ',"",notWord)
    contractedString=contractedString+notWord

   if(aWord):
    if(keyword.iskeyword(aWord)):
     if (contractedString=="" or contractedString[-1]==" "):
      contractedString=contractedString+aWord+" "
     else:
      contractedString=contractedString+" "+aWord+" "
    else:
     if\
     (
      (self.is_lowercase(lastAppendedWord) and self.is_lowercase(aWord))
      or(self.is_uppercase(lastAppendedWord) and self.is_lowercase(aWord))
     ):
      contractedString=contractedString+" "+aWord
     else:
      contractedString=contractedString+aWord
    lastAppendedWord=aWord


  return contractedString



 def is_lowercase(self,wordToCheck):
  match=re.match(r'^[a-z]+$',wordToCheck)
  if(match):
   return True
  else:
   return False



 def is_uppercase(self,wordToCheck):
  match=re.match(r'^[A-Z][a-z]+$',wordToCheck)
  if(match):
   return True
  else:
   return False



 def remove_brackets(self,contractedString):

  matchStringStartsWithSquareBracket=re.match(r'\s*[[]',contractedString)
  if(matchStringStartsWithSquareBracket):
   contractedString=contractedString.replace("[","",1)
   contractedString=contractedString.replace("]","",1)

  return contractedString

