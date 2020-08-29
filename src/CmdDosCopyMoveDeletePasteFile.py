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
import os.path
import sys
from VoiceEditorSettings import VoiceEditorSettings
from string import Template

class CmdDosCopyMoveDeletePasteFile(object) :


 def __init__(self,parent,files,cmdBox,editBox,viewBox,statusBox) :
  self.operation = "idle"
  self.path=os.getcwd()
  self.files=files
  self.cmdBox=cmdBox
  self.editBox=editBox
  self.viewBox=viewBox
  self.statusBox=statusBox
  self.parent=parent
  self.moveList=[]
  self.duplicateList=[]
  self.deleteList=[]

 def __call__(self,command):

  if(re.match(r'duplicate ',command)):
   self.statusBox.Text="Please enter list of files to copy in command box"
   self.operation="duplicate"
   duplicateList=[]
   moveList=[]
   self.sourceDirectory=os.getcwd()

  if(re.match(r'move ',command)):
   self.statusBox.Text = "Please enter list of files to move in command box"
   self.operation= "move"
   self.duplicateList=[]
   self.moveList=[]
   self.sourceDirectory=os.getcwd()

  if(re.match(r'delete ',command)):
   self.sourceDirectory=os.getcwd()
   self.statusBox.Text = "Please enter list of files to delete in command box"
   self.operation= "delete"
   self.deleteList=[]
   self.moveList=[]
   self.duplicateList=[]

  if(re.match(r'insert ',command)):
   self.destinationDirectory=os.getcwd()
   if (self.operation=="idle"):
    self.statusBox.Text="No file operation (copy,move,delete) has been selected. Aborting insert."
    self.parent.commandState="wait for selection"
    self.parent.list_directory()
    return self.parent
   else:
    self.insert_files()
    scriptFileName=os.path.join(VoiceEditorSettings.scriptDirectoryPath,"duplicate_move_delete.py")
    return self.parent.edit_file(scriptFileName)

  self.viewBox.Text = ""
  index=0
  self.viewBox.AppendText("%s files from directory %s" % (self.operation, self.path)+"\r\n")
  self.viewBox.AppendText ("please choose files from list below: "+"\r\n")
  self.viewBox.AppendText ("\r\n")
  for type,directory,file in self.files:
   self.viewBox.AppendText("%2d %s"%(index,file)+"\r\n")
   index=index+1

  self.statusBox.Text="OK"

  return self


 def get_file_list(self):

  indexList=[]
  fileList=[]

  #compile list of indexes of files to operate on
  rangesList=self.cmdBox.Text.split(",")
  for singleRange in rangesList:

   matchRange=re.match(r'\s*(\d+)\s*:\s*(\d+)\s*',singleRange)
   matchSingle=re.match(r'\s*(\d+)\s*',singleRange)

   if(matchRange):
    lower=int(matchRange.group(1))
    upper=int(matchRange.group(2))
   elif(matchSingle):
    lower=upper= int(matchSingle.group(1))

   #If there were no matches then an invalid format was supplied.
   #In that case no further processing is required.
   if(not matchSingle and not matchRange):
    del fileList[:]
    return fileList

   #if either bound is less than 0 or greater than the array size return an empty list
   if(lower< 0 or upper < 0 or lower > len(self.files)or upper > len(self.files)):
    self.statusBox.Text=" Selected file range out of bounds: %d %d" % (lower, upper)
    del fileList[:]
    return fileList

   #files to operate on have been identified so let's compile a list of indexes
   for fileIndex in range(lower,upper+ 1):
    indexList.append(fileIndex)

  #convert indexes into filenames and directory information
  self.viewBox.Text=""
  if(self.operation == "duplicate"):
   self.viewBox.AppendText("Files to be copied from directory: %s"%(self.path)+"\r\n")
  elif(self.operation == "move"):
   self.viewBox.AppendText("Files to be moved from directory: %s"%(self.path)+"\r\n")
  elif(self.operation=="delete"):
   self.viewBox.AppendText("Files to be deleted from directory: %s"%(self.path)+"\r\n")
  else:
   self.statusBox.Text="Invalid operation: %s" % self.operation
   del fileList[:]
   return self.fileList

  self.viewBox.AppendText ("\r\n")
  for index in indexList:
   type, directory, file=self.files[index]
   self.viewBox.AppendText("%s"%(file)+"\r\n")
   fileList.append(file)

  return fileList

 def processThisCommand(self,command):

  self.path=os.getcwd()

  if(command=="list directory"):
   self.parent.processThisCommand("list directory")
   return self.parent

  if(self.operation == "duplicate"):
   self.duplicateList=self.get_file_list()
  elif(self.operation=="move"):
   self.moveList=self.get_file_list()
  elif(self.operation=="delete"):
   self.destinationDirectory=os.getcwd()
   self.deleteList=self.get_file_list()
   self.insert_files()
   scriptFileName=os.path.join(VoiceEditorSettings.scriptDirectoryPath,"duplicate_move_delete.py")
   return self.parent.edit_file(scriptFileName)

  if(self.duplicateList==[]and self.moveList==[]and self.deleteList==[]):
   self.statusBox.Text="Unable to parse file selection command: %s"%command
   return self

  return self.parent


 def insert_files(self):

  fileList=[]

  scriptFileName=os.path.join(VoiceEditorSettings.scriptDirectoryPath,"duplicate_move_delete.py")
  try:
   self.statusBox.Text="Successfully opened file for writing: %s"%scriptFileName
   scriptFile=open(scriptFileName,"w")
  except:
   self.statusBox.Text="Unable to open file for writing: %s"%scriptFileName
   return

  if(self.operation == "duplicate"):
   fileList=self.duplicateList
  elif(self.operation == "move"):
   fileList=self.moveList
  elif(self.operation=="delete"):
   fileList = self.deleteList

  scriptFile.write("import shutil\n")
  scriptFile.write("import sys\n")
  scriptFile.write("import subprocess\n")

  scriptFile.write("commandList = [\n")

  for file in fileList:
   sourceFileName=os.path.join(self.sourceDirectory,file)
   destinationFileName=os.path.join(self.destinationDirectory,file)
   if(self.operation == "duplicate"):
    scriptFile.write("r'copy %s %s',\n" % (sourceFileName, destinationFileName))
   elif(self.operation=="move"):
    scriptFile.write("r'move %s %s',\n" % (sourceFileName, destinationFileName))
   elif(self.operation=="delete"):
    scriptFile.write("r'del %s',\n" % (sourceFileName))

  scriptFile.write("]\n")

  scriptFile.write("""
for shellCommand in commandList:
 try:
  shellCommandOutput=subprocess.check_call(shellCommand,shell=True)
 except subprocess.CalledProcessError as e:
  self.statusBox.Text="Unable to duplicate file %s"%e
 except:
  print ("Unexpected error:",sys.exc_info())
  """)

  scriptFile.close()
