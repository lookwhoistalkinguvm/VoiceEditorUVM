
import re
import string
import shutil
import glob
import os
import subprocess


def main():

 classDictionary={}
 originalFilesList=[]

 VOICEEDITORROOT=os.environ["VOICEEDITORROOT"]

 #copy all the files the reference directory
 for directory in [r'\src',r'\src_uvm']:
  directory=VOICEEDITORROOT+ directory
  os.chdir(directory)
  for file in glob.glob(r'*.py'):
   print(file)
   originalFilesList.append(file)
   try:
    shutil.copy(file,VOICEEDITORROOT+r'\snapshot')
   except:
    print("unable to copy file "+ file)

 #Change to snapshot directory
 os.chdir(VOICEEDITORROOT+r'\snapshot')

 #Delete all the old snapshots first
 for snapshotFile in glob.glob(r'*Snapshot.py'):
  shellCommand=r'del %s'%snapshotFile
  shellOutput=subprocess.check_output(shellCommand,shell=True)

 #extract all the class names
 for file in glob.glob(r'*.py'):
  #print(file)
  try:
   fileHandle=open(file,"r")
  except:
   print("unable to open file for reading: "+ file)
  for currentLine in fileHandle:
   m=re.match(r'\s*class\s+(\w+)', currentLine)
   if(m):
    className=m.group(1)
    newClassName=className+"Snapshot"
    classDictionary[className]=newClassName
    currentLine=re.sub(className,newClassName, currentLine)
    #print(currentLine)

 #now go through all the files again and substitute the class names with their snapshot equivalents
 for file in glob.glob(r'*.py'):
  try:
   fileHandle=open(file,"r")
   fileArray=fileHandle.readlines()
  except:
   print("unable to open file: "+ file)
   return
  #fileHandle.seek(0)
  fileHandle.close()
  (fileBase, fileExtension)=os.path.splitext(file)
  print(fileBase)
  file= file.replace(fileBase, fileBase+"Snapshot")
  print("file: ", file)
  try:
   fileHandle=open(file,"w")
  except:
   print("unable to open file for writing: "+ file)
   return
  lineNumber=0
  for fileLine in fileArray :
   for(className, newClassName ) in classDictionary.items():
#    if(className!="VoiceEditorSettings" or re.match(r'\s*class\s', fileLine)):
    if(fileBase=="VoiceEditorSettings" and not re.match(r'\s*class ', fileLine)):
     pass
    else:
     fileLine=re.sub(r"\b%s\b"%(className),newClassName, fileLine)
   fileHandle.write(fileLine)
   if (fileLine.rstrip()!=""):
    debugString = "print (\" %s %0d \")"% (file, lineNumber)
    #fileHandle.write(debugString+"\n")
   lineNumber+=1
  fileHandle.close()

 #Now delete the original non-snapshot files
 for file in originalFilesList :
  shellCommand=r'del %s'% file
  shellOutput=subprocess.check_output(shellCommand,shell=True)


if __name__ == "__main__":
 main()



