import re
import string
import shutil
import glob
import os
import subprocess
import sys


def main():

 classDictionary={}

 #Delete all the old release files first
 os.chdir(r'C:\Users\thiel\Projects\Python\VoiceEditor_release')
 for releaseFile in glob.glob(r'*.py'):
  try:
   shellCommand=r'del %s'%releaseFile
   shellOutput=subprocess.check_output(shellCommand,shell=True)
  except:
   print("command %s failed with: "%shellCommand,shellOutput)

 #copy all the files the reference directory
 os.chdir(r'C:\Users\thiel\Projects\Python\VoiceEditor\src')
 for file in glob.glob(r'*.py'):
  #print(file)
  try:
   shutil.copy(file,r'C:\Program Files\VoiceEditor\release')
  except:
   print("unable to copy file "+ file)

 #read in licence
 try:
  fileHandle=open(r'C:\Users\thiel\Projects\scratch\MIT_License.txt',"r")
  licenceFileTextList=fileHandle.readlines()
  fileHandle.close()
 except:
  print("Unable to open licence file text for reading")
  sys.exit(1)

 #Change to release directory
 os.chdir(r'C:\Program Files\VoiceEditor\release')
 for file in glob.glob(r'*.py'):
  print("processing file: ", file)
  try:
   print("reading file: ", file)
   fileHandle=open(file,"r")
   fileList=fileHandle.readlines()
   fileHandle.close()
  except:
   print("Unable to open file for reading:", file)
   sys.exit(1)
  try:
   print("writing file: ", file)
   fileHandle=open(file,"w")
   print("hello")
   fileHandle.write("".join(licenceFileTextList))
   print("hello 2")
   fileHandle.write("".join(fileList))
   fileHandle.close()
  except:
   print("Unable to open file for writing:", file)
   sys.exit(1)








if __name__ == "__main__":
 main()



