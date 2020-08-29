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

class CmdEditFilter(object):

 lastFilterUsed= "TBD"
 filterList=[]
 filterDefinitionFileHasBeenRead=0


 def __init__(self,parent,fileToEditList,currentEditLine,allTheBoxes):

  (self.cmdBox,
       self.editBox,
           self.scaleBox,
               self.viewBox,
                   self.statusBox)=allTheBoxes

  self.fileToEditList=fileToEditList
  self.currentEditLine=currentEditLine
  self.parent=parent
  self.isFilterEnabled=0
  self.fileToEditListFiltered=[]
  self.fileToEditListFilteredLineNumbers=[]

  if ( not CmdEditFilter.filterDefinitionFileHasBeenRead):
   self.read_predefined_filters()
   CmdEditFilter.filterDefinitionFileHasBeenRead=1


 def __call__(self):

  filterOptionsReturnValue=self.list_filter_options()

  if(filterOptionsReturnValue<0):
   return self.parent


  return self



 def processThisCommand(self,command):

  self.nextCommand=self

  if(command=="list directory"):
   #User has chosen to abort filter operation
   self.parent.processThisCommand(command)
   self.isFilterEnabled=0
   self.nextCommand=self.parent.listDirectory
  elif(command == "remove lines"):
   numberOfLinesAlreadyDeleted=0
   for lineNumber in self.fileToEditListFilteredLineNumbers:
    del self.fileToEditList[lineNumber-numberOfLinesAlreadyDeleted]
    numberOfLinesAlreadyDeleted=numberOfLinesAlreadyDeleted+1
   self.toggle_filter()
  elif(command == "duplicate lines"):
   self.parent.clear_line_operation_buffer()
   for lineNumber in self.fileToEditListFilteredLineNumbers:
    self.parent.append_line_to_line_operation_buffer(self.fileToEditList[lineNumber],lineNumber)
    # CmdEdit.currentEditLineByFile.append(self.fileToEditList[lineNumber])
   self.toggle_filter()
  elif(command == "comment out lines"):
   for lineNumber in self.fileToEditListFilteredLineNumbers:
    lineToCommentOut=self.fileToEditList[lineNumber]
    lineToCommentOut="#"+lineToCommentOut
    self.fileToEditList[lineNumber]=lineToCommentOut
   self.toggle_filter()
  elif(command == "comment in lines"):
   for lineNumber in self.fileToEditListFilteredLineNumbers:
    lineToCommentIn=self.fileToEditList[lineNumber]
    lineToCommentIn=lineToCommentIn.replace(r'#', "",1)
    self.fileToEditList[lineNumber]=lineToCommentIn
   self.toggle_filter()
  elif(command=="toggle filter"):
   #If filter is already enabled then pressing filter button results in toggling filter to off
   self.toggle_filter()
  elif(command.isdigit() and self.isFilterEnabled):
   #command contains line number to jumped to
   self.parent.processThisCommand(command)
   self.isFilterEnabled=0
   self.nextCommand=self.parent
  elif(command.isdigit() and not self.isFilterEnabled):
   #command contains list index of filter to apply
   selectedFilter=int(command)
   if(selectedFilter<0 or selectedFilter>len(CmdEditFilter.filterList)-1):
    self.statusBox.Text=\
        "Selected predefined filter option is out of range: %d"%selectedFilter
   else:
    if(selectedFilter==0):
     self.filterToApply=CmdEditFilter.lastFilterUsed
    else:
     self.filterToApply=CmdEditFilter.filterList[selectedFilter]
    self.apply_filter()
    self.isFilterEnabled=1
    self.nextCommand=self
  else:
   #User has entered ad hoc filter in command window
   if(command==""):
    self.filterToApply=CmdEditFilter.lastFilterUsed
   else:
    self.filterToApply=command
   self.apply_filter()
   self.isFilterEnabled=1
   self.nextCommand=self

  return self.nextCommand



 def list_filter_options(self):

  self.viewBox.Text=""


  message= """
  \r\n
  Please enter custom filter in command window or select from list below.
  \r\n
  \r\n"""

  self.viewBox.AppendText(message)

  index=0

  #Add last filter to the list of filters if it is not already on the list
  if (CmdEditFilter.lastFilterUsed!="TBD"):
   CmdEditFilter.filterList[0]=CmdEditFilter.lastFilterUsed
   if ( not CmdEditFilter.lastFilterUsed in CmdEditFilter.filterList[1:len(CmdEditFilter.filterList)]):
    CmdEditFilter.filterList.append(CmdEditFilter.lastFilterUsed)

  for index,filterDefinition in enumerate(CmdEditFilter.filterList):
   self.viewBox.AppendText("    %4d %s \r\n"%(index,CmdEditFilter.filterList[index]))

  return 0



 def apply_filter(self):

  lineNumber=0
  self.viewBox.Text=""
  self.fileToEditLineFiltered=[]

  CmdEditFilter.lastFilterUsed=self.filterToApply

  for fileToEditLine in self.fileToEditList:

   try:
    matchFilter=re.search(self.filterToApply,fileToEditLine,re.IGNORECASE)
   except:
    self.viewBox.Text="Invalid regular expression: %s"%self.filterToApply
    matchFilter=None

   if(matchFilter):
    self.viewBox.AppendText("%d %s \r\n"%(lineNumber,fileToEditLine))
    self.fileToEditLineFiltered.append(fileToEditLine)
    self.fileToEditListFilteredLineNumbers.append(lineNumber)
   lineNumber=lineNumber+1



 def toggle_filter(self):

  self.isFilterEnabled=0
  self.parent.displayFile()
  self.nextCommand=self.parent


 def read_predefined_filters(self):

  try:
   filterDefinitionFile=open\
       (VoiceEditorSettings.lineFilterDefinitionFileName,"r")
  except:
   self.statusBox.Text="Unable to open file: %s"\
       %VoiceEditorSettings.lineFilterDefinitionFileName
   return

  for filterDefinitionFileLine in filterDefinitionFile:

   #Ignore empty lines
   copyOfFilterDefinitionFileLine=filterDefinitionFileLine
   if(not copyOfFilterDefinitionFileLine.strip()):
    continue

   #Everything before the ultimate hash sign is the filter definition.
   matchLastPositionOfHashSign=\
       re.search(r'#', filterDefinitionFileLine[::-1])
   if(matchLastPositionOfHashSign):
    positionOfLastHashSign=\
        len(filterDefinitionFileLine)-1-matchLastPositionOfHashSign.start()
   else:
    positionOfLastHashSign=len(filterDefinitionFileLine)-1

   #Store all filter definitions retrieved from file.
   nonCommentPartOfFilterDefinitionLine=\
       filterDefinitionFileLine[0:positionOfLastHashSign]
   CmdEditFilter.filterList.append(nonCommentPartOfFilterDefinitionLine)


  #Reserve the top slot for the last filter
  CmdEditFilter.filterList.insert(0,"TBD #Last filter used")
