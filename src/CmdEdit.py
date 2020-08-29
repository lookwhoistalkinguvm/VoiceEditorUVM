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


import io
import string
import re
import shutil
import os
from VoiceEditorSettings import VoiceEditorSettings
from CmdEditDuplicateYankInsertLines import CmdEditDuplicateYankInsertLines
from CmdEditCommentLines import CmdEditCommentLines
from CmdEditIndentLines import CmdEditIndentLines
from CmdEditSubstitute import CmdEditSubstitute
from CmdEditUpdateScale import CmdEditUpdateScale
from CmdEditLineBreak import CmdEditLineBreak
from CmdEditFilter import CmdEditFilter
from CmdDosRecentFiles import CmdDosRecentFiles
from CmdDosRecentDirectories import CmdDosRecentDirectories
from CmdDosFavouriteDirectories import CmdDosFavouriteDirectories
from CmdEditExpandCamelBackIdentifiers import CmdEditExpandCamelBackIdentifiers
from CmdEditContractLine import CmdEditContractLine
from FastButtonMarkers import FastButtonMarkers
#UVM only
from AutoMenuStartSequence import AutoMenuStartSequence
from AutoMenuWBSequences import AutoMenuWBSequences
from AutoMenuObjectMacroTemplates import AutoMenuObjectMacroTemplates
#UVM only


class CmdEdit(object) :

 #remember for each file what line we were editing
 currentEditLineByFile={}

 #buffer of lines to be duplicated or yanked
 lineOperationBuffer=[]

 def __init__(self,voiceEditor,listDirectory,cmdBox,editBox,scaleBox,viewBox,statusBox):
  self.voiceEditor=voiceEditor
  self.listDirectory=listDirectory
  self.commandState = "idle"
  self.cmdBox=cmdBox
  self.scaleBox=scaleBox
  self.viewBox=viewBox
  self.statusBox=statusBox
  self.editBox=editBox
  self.allTheBoxes=(
      self.cmdBox,
          self.editBox,
              self.scaleBox,
                  self.viewBox,
                      self.statusBox)
  self.nextCommand=None
  self.fileToEditList=[]
  self.numberOfLinesPerPage=VoiceEditorSettings.numberOfLinesPerPage
  self.halfWayDownThePage=self.numberOfLinesPerPage/2
  self.currentEditLine=1
  self.fileLength= 0
  self.fullFileName=""
  self.lineStart= 0
  self.lineEnd= 0
  self.fileToEdit=None
  self.removeSpaces= False
  self.cmdEditDuplicateYankInsertLines=\
      CmdEditDuplicateYankInsertLines\
          (self,cmdBox,editBox,viewBox,statusBox)
  self.cmdEditIndentLines=CmdEditIndentLines(self.fileToEditList,cmdBox,editBox,viewBox,statusBox)
  #self.cmdEditSubstitute=CmdEditSubstitute(self.fileToEditList,cmdBox,editBox,viewBox,statusBox)
  self.cmdEditUpdateScale=CmdEditUpdateScale(self.scaleBox,self.editBox,self.statusBox)
  self.cmdEditLineBreak=CmdEditLineBreak\
      (self.fileToEditList,self.cmdBox,self.editBox,self.viewBox,self.statusBox)
  self.cmdEditFilter=None
  self.voiceEditor.fastButtonAreaHandler.reset()



 def processThisCommand(self,command):
  self.statusBox.Text="%s (Edited)"%self.fullFileName
  self.nextCommand=self
  editBoxText=re.sub(r'^\s*\d+\s+','',self.editBox.Text)
  CmdEdit.currentEditLineByFile[self.fullFileName]=self.currentEditLine
  if(command=="list directory"):
   self.listDirectory.processThisCommand(command)
   self.nextCommand=self.listDirectory
   self.save_file()
   #self.close_file()
   self.fileToEdit=None
   self.set_previous_file()
   CmdEdit.currentEditLineByFile[self.fullFileName]=self.currentEditLine
  elif(command == "switch to previous file"):
   self.nextCommand=self.switch_to_previous_file()
  elif(command == "expand camelback identifiers"):
   cmdEditExpandCamelBackIdentifiers=CmdEditExpandCamelBackIdentifiers\
       (self,self.fileToEditList,self.currentEditLine,self.allTheBoxes)
   self.nextCommand=cmdEditExpandCamelBackIdentifiers()
  elif(command == "list favourite directories"):
   self.save_file()
   cmdDosFavouriteDirectories=self.listDirectory.create_favourite_directories_object()
   self.nextCommand=cmdDosFavouriteDirectories()
  elif(command == "list recent directories"):
   self.set_previous_file()
   self.save_file()
   cmdDosRecentDirectories=self.listDirectory.create_recent_directories_object()
   self.nextCommand=cmdDosRecentDirectories()
  elif(command == "list recent files"):
   self.set_previous_file()
   self.save_file()
   cmdDosRecentFiles=self.listDirectory.create_recent_files_object()
   self.nextCommand=cmdDosRecentFiles()
  elif(command == "list favourite files"):
   self.set_previous_file()
   self.save_file()
   cmdDosFavouriteFiles=self.listDirectory.create_favourite_files_object()
   self.nextCommand=cmdDosFavouriteFiles()
  elif(command == "toggle filter"):
   self.cmdEditFilter=CmdEditFilter\
       (self,self.fileToEditList,self.currentEditLine,self.allTheBoxes)
   self.nextCommand=self.cmdEditFilter()
  elif(
      command =="insert line break"
          or command=="remove line break"):
   self.save_file()
   self.cmdEditLineBreak(command,self.currentEditLine)
   self.displayFile()
  elif(command=="scale words" or command=="scale letters"):
   self.cmdEditUpdateScale(command)
  elif(re.match(r'\s*substitute',command)):
   self.cmdEditSubstitute=\
    CmdEditSubstitute(self,self.fileToEditList,self.cmdBox,self.editBox,self.viewBox,self.statusBox)
   self.save_file()
   self.nextCommand=self.cmdEditSubstitute(command)
  elif(re.match(r'\s*(indent lines left |indent lines right)',command)):
   self.save_file()
   self.cmdEditIndentLines(command)
   self.displayFile()
  elif(re.match(r'\s*(comment out|comment in)\s+line',command)):
   cmdEditCommentLines=\
    CmdEditCommentLines(\
     self.fileToEditList,self.fullFileName, self.cmdBox, self.editBox, self.viewBox, self.statusBox)
   self.save_file()
   cmdEditCommentLines(command)
   self.displayFile()
  elif(re.match(r'\s*(duplicate|yank|insert)\s+line',command)):
   self.save_file()
   self.cmdEditDuplicateYankInsertLines(command,self.currentEditLine,CmdEdit.lineOperationBuffer)
   self.displayFile()
  elif(command=="save file"):
   self.save_file()
  elif(command=="contract edit line"):
   cmdEditContractLine=\
       CmdEditContractLine(self,self.fileToEditList,self.currentEditLine,self.allTheBoxes)
   self.nextCommand=cmdEditContractLine()
   editBoxText=re.sub(r'^\s*\d+\s+','',self.editBox.Text)
   self.fileToEditList[self.currentEditLine]=editBoxText.rstrip()
   self.currentEditLine=self.currentEditLine
   self.displayFile()
   self.save_file()
  elif(command=="scroll_up"):
   if(self.currentEditLine-VoiceEditorSettings.scrollSpeed >=0):
    self.currentEditLine=self.currentEditLine-VoiceEditorSettings.scrollSpeed
   self.displayFile()
  elif(command=="scroll_down"):
   if(self.currentEditLine+VoiceEditorSettings.scrollSpeed<=len(self.fileToEditList)):
    self.currentEditLine=self.currentEditLine+VoiceEditorSettings.scrollSpeed
   self.displayFile()
  elif(command=="down"):
   self.fileToEditList[self.currentEditLine]=editBoxText.rstrip()
   self.currentEditLine=self.currentEditLine+1
   if(self.currentEditLine>len(self.fileToEditList)-1):
    self.currentEditLine=len(self.fileToEditList)-1
   self.displayFile()
  elif(command=="insert"):
   self.fileToEditList[self.currentEditLine]=editBoxText.rstrip()
   self.currentEditLine=self.currentEditLine
   self.displayFile()
   self.save_file()
  elif(command=="up"):
   self.fileToEditList[self.currentEditLine]=editBoxText.rstrip()
   self.currentEditLine=self.currentEditLine-1
   if(self.currentEditLine<0):
    self.currentEditLine=0
    self.fileToEditList.insert(0,"")
    FastButtonMarkers.adjust_markers(self.fullFileName,0,1)
   self.displayFile()
  elif(command=="return"):
   self.fileToEditList[self.currentEditLine]=editBoxText.rstrip()
   self.fileToEditList.insert(self.currentEditLine+1,"")
   self.currentEditLine=self.currentEditLine+1
   FastButtonMarkers.adjust_markers(self.fullFileName,self.currentEditLine,1)
   self.displayFile()
  elif(command=="insert class definition"):
   functionTemplate="class []([object]) :"
   self.insert_in_edit_box_at_cursor_position(functionTemplate)
  elif(command=="insert main function check"):
   functionTemplate='if __name__ == "__main__":'
   self.fileToEditList.insert(self.currentEditLine,functionTemplate)
   functionTemplate=" main()"
   self.fileToEditList.insert(self.currentEditLine+1,functionTemplate)
   self.displayFile()
  elif(command=="insert function call"):
   functionTemplate="[]=[]([])"
   self.insert_in_edit_box_at_cursor_position(functionTemplate)
  elif(command=="insert constructor function definition"):
   functionTemplate="def __init__(self [,][]):"
   self.insert_in_edit_box_at_cursor_position(functionTemplate)
  elif(command=="insert function definition"):
   cursorPosition=self.editBox.SelectionStart
   functionTemplate="def [] ([self]):"
   self.insert_in_edit_box_at_cursor_position(functionTemplate)
  elif(command=="clear file"):
   self.save_file()
   del self.fileToEditList[:]
   self.fileToEditList.append("")
   self.currentEditLine=0
   self.displayFile()
  elif(command=="remove line"):
   self.save_file()
   del self.fileToEditList[self.currentEditLine]
   self.displayFile()
  elif(re.match(r'^remove lines\s*(\d+)\s*:\s*(\d+)',command)):
   m=re.match(r'^remove lines\s*(\d+)\s*:\s*(\d+)',command)
   self.save_file()
   start=int(m.group(1))
   end=int(m.group(2))
   for lineToDelete in range(start,end+1):
    del self.fileToEditList[start]
   self.displayFile()
  elif(command=="revert file"):
   self.fileToEdit.close()
   self.load_file()
   self.displayFile()
   #UVM only
  elif(command=="auto menu start sequence"):
   autoMenuStartSequence=AutoMenuStartSequence()
   self.nextCommand=autoMenuStartSequence(self,self.voiceEditor.fastButtonAreaHandler )
  elif(command=="auto menu wish bone sequences"):
   autoMenuWBSequences=AutoMenuWBSequences()
   self.nextCommand=autoMenuWBSequences(self,self.voiceEditor.fastButtonAreaHandler)
  elif(command=="auto menu object macro templates"):
   autoMenuObjectMacroTemplates=AutoMenuObjectMacroTemplates()
   self.nextCommand=autoMenuObjectMacroTemplates(self,self.voiceEditor.fastButtonAreaHandler)
   #UVM only
  elif(command.isdigit()):
   self.currentEditLine=int(command)
   if(self.currentEditLine>len(self.fileToEditList)-1):
    self.currentEditLine=len(self.fileToEditList)-1
   if(self.fullFileName==VoiceEditorSettings.recentFilesListFileName):
    self.nextCommand=self.switch_to_another_file()
   elif(self.fullFileName==VoiceEditorSettings.favouriteFilesListFileName):
    self.nextCommand=self.switch_to_another_file()
   elif(self.fullFileName==VoiceEditorSettings.recentDirectoriesListFileName):
    self.nextCommand=self.change_directory()
   elif(self.fullFileName==VoiceEditorSettings.favouriteDirectoriesListFileName):
    self.nextCommand=self.change_directory()
   else:
    #This selected line number is the line number to edit
    self.displayFile()
  elif(self.fileToEdit==None):
   #if there is no file open already then we were called from CmdDosListDirectory
   #with the name of the file to open given as the argument to processThisCommand()
   self.viewBox.Text=""
   self.fullFileName=command
   self.load_file()
   if (self.fileToEdit==None):
    #for some reason we were unable to open the file supplied, return to list_directory
    self.nextCommand=self.listDirectory
    self.listDirectory.processThisCommand("list directory")
   else:
    self.displayFile()
  else:
    self.statusBox.Text="unknown command "+command
    self.viewBox.Text=" Error, see status window."

  return self.nextCommand

 def displayFile(self):
  self.viewBox.Text=""
  if (self.currentEditLine>len(self.fileToEditList)-1):
   self.currentEditLine=len(self.fileToEditList)-1
  self.lineStart=self.currentEditLine-self.halfWayDownThePage
  self.editBox.Text=""
  leadingSpacePattern=re.compile(r'\s+')
  #self.editBox.AppendText("%4d %s" % (self.currentEditLine,self.fileToEditList[self.currentEditLine]))
  for verticalPos in range(self.numberOfLinesPerPage):
   fileLineNumber=verticalPos+self.lineStart
   if(fileLineNumber>=0 and fileLineNumber<len(self.fileToEditList)):
    lineToPrint=self.fileToEditList[fileLineNumber]
    leadingSpacePM=leadingSpacePattern.match(lineToPrint)
    if (fileLineNumber==self.currentEditLine):
     self.editBox.AppendText(lineToPrint)
     editLineIndicator=">>"
    else:
     editLineIndicator="  "
    if(leadingSpacePM):
     leadingDots = "." * leadingSpacePM.end()
     appendStringView =\
          "%4d %s %2d %s%s" %\
               (fileLineNumber,editLineIndicator,leadingSpacePM.end(),\
                   leadingDots,lineToPrint[leadingSpacePM.end():])
    else:
     appendStringView = "%4d %s %2d %s" % (fileLineNumber,editLineIndicator,0, lineToPrint)
    self.viewBox.AppendText(appendStringView+"\r\n")
   else:
    self.viewBox.AppendText("\r\n")
  self.lineEnd=fileLineNumber
  self.viewBox.Select(0 ,len(self.viewBox.Text))
  return self.nextCommand

 def save_file(self):
  if (self.fileToEdit==None):
   self.statusBox.Text = "No file open"
  else:
   self.open_file("w")
   if(self.fileToEdit==None):
    return
   self.fileToEdit.seek(0)
   self.fileToEdit.truncate()
   for line in self.fileToEditList:
    self.fileToEdit.write(line+"\n")
   self.close_file()
   self.statusBox.Text="%s (Saved)"%self.fullFileName

 def load_file(self):
  del self.fileToEditList[:]
  #make a backup copy case things go wrong
  try:
   shutil.copyfile(self.fullFileName,self.fullFileName+".backup")
  except:
   self.statusBox.Text=" Unable to copy file "+self.fullFileName+" to "+self.fullFileName+".backup"
  self.open_file("r")
  if(self.fileToEdit==None):
   return
  for fileLine in self.fileToEdit.readlines():
   self.fileToEditList.append(fileLine.rstrip())
  if (len(self.fileToEditList)== 0):
   self.fileToEditList.insert(0,"")
#  self.fileToEditList=map(str.rstrip,self.fileToEditList)
#  for index in range(len(self.fileToEditList)):
#   self.fileToEditList[index]=self.fileToEditList[index].rstrip
  if(self.fullFileName in CmdEdit.currentEditLineByFile.keys()):
   self.currentEditLine=CmdEdit.currentEditLineByFile[self.fullFileName]
  else:
   if (self.halfWayDownThePage<len(self.fileToEditList)):
    self.currentEditLine=self.halfWayDownThePage
   else:
    self.currentEditLine=len(self.fileToEditList)-1
  self.statusBox.Text="%s (Saved)"%self.fullFileName
  self.fileToEdit.close()



 def insert_in_edit_box_at_cursor_position(self,insertString):
   selectionStart=self.editBox.SelectionStart
   selectionEnd=self.editBox.SelectionStart+self.editBox.SelectionLength
   self.editBox.Text=self.editBox.Text[:selectionStart]+insertString+self.editBox.Text[selectionEnd:]
   self.editBox.SelectionStart=selectionStart+len(insertString)
   self.editBox.SelectionLength=0



 def insert_in_cmd_box_at_cursor_position(self,insertString):
   selectionStart=self.cmdBox.SelectionStart
   selectionEnd=self.cmdBox.SelectionStart+self.cmdBox.SelectionLength
   self.cmdBox.Text=self.cmdBox.Text[:selectionStart]+insertString+self.cmdBox.Text[selectionEnd:]
   self.cmdBox.SelectionStart=selectionStart+len(insertString)
   self.cmdBox.SelectionLength=0



 def open_file(self,mode):

  if(not os.path.exists(self.fullFileName)):
   #this can happen if the file has been deleted since we did a list directory
   self.statusBox.Text="File no longer exists "+self.fullFileName
   self.fileToEdit=None
   return

  try:
   if(VoiceEditorSettings.useUNIXStyleLineEnding):
    self.fileToEdit=io.open(self.fullFileName, mode,newline='\n')
   else:
    self.fileToEdit=io.open(self.fullFileName, mode)
  except:
   self.statusBox.Text="unable to open file: "+self.fullFileName+" mode: "+ mode
   self.fileToEdit=None



 def change_directory(self):

  #The selected line number contains the file to open
  fullDirectoryName=self.fileToEditList[self.currentEditLine]
  fullDirectoryName=fullDirectoryName.rstrip()
  if(not os.path.isabs(fullDirectoryName)):
   fullDirectoryName=VoiceEditorSettings.VOICEEDITORROOT+r"\\"+fullDirectoryName
  try:
   os.chdir(fullDirectoryName)
   self.listDirectory.processThisCommand("list directory")
   return self.listDirectory
  except:
   self.statusBox.Text="Unable to change to directory: %s"%fullDirectoryName
   return self



 def switch_to_another_file(self):

  #The selected line number contains the file to open
  fullFileName=self.fileToEditList[self.currentEditLine]
  fullFileName=fullFileName.rstrip()
  if(not os.path.isabs(fullFileName)):
   fullFileName=VoiceEditorSettings.VOICEEDITORROOT+r"\\"+fullFileName
  if ( not os.path.exists(fullFileName)):
   self.statusBox.Text="File does not exist: %s"%fullFileName
   return self
  if(fullFileName not in self.listDirectory.recentFilesList):
   self.listDirectory.recentFilesList.append(fullFileName)
  cmdEdit=self.listDirectory.create_cmd_edit_object()
  cmdEdit.processThisCommand(fullFileName)
  return cmdEdit



 def switch_to_previous_file(self):

  self.save_file()

  previousFile=self.listDirectory.get_previous_file()
  if(previousFile==""):
   self.statusBox.Text="No previous file"
   return self

  self.set_previous_file()

  cmdEdit=self.listDirectory.create_cmd_edit_object()
  cmdEdit.processThisCommand(previousFile)
  return cmdEdit



 def close_file(self):

  self.fileToEdit.close()



 def set_previous_file(self):

  previousFile=self.listDirectory.get_previous_file()

  excludedFilesList=[
   VoiceEditorSettings.runDirectoryPath+r"\recentFiles.txt",
   VoiceEditorSettings.runDirectoryPath+r"\recentDirectories.txt",
   VoiceEditorSettings.runDirectoryPath+r"\favouriteDirectories.txt",
   VoiceEditorSettings.runDirectoryPath+r"\favouriteFiles.txt"]



  if ((self.fullFileName not in excludedFilesList) and (self.fullFileName!=previousFile)):
   self.listDirectory.set_previous_file(self.fullFileName)



 def display_help_template(self,templateNumber):

  if (
    self.voiceEditor.fastButtonAreaHandler.is_instance_of_fastbuttontemplates(
     self.voiceEditor.fastButtonAreaHandler.command
    )
  ):

   helpStringList=\
    self.voiceEditor.fastButtonAreaHandler.command.get_template_help_string_list(templateNumber)



 def is_help_file(self):

  helpFile=os.path.normpath(VoiceEditorSettings.helpFile)
  currentFile=os.path.normpath(self.fullFileName)

  if (currentFile==helpFile):
   return True
  else:
   return False



 def append_line_to_line_operation_buffer(self,line,lineNumber):
  CmdEdit.lineOperationBuffer.append(self.fileToEditList[lineNumber])



 def clear_line_operation_buffer(self):
  CmdEdit.lineOperationBuffer=[]
