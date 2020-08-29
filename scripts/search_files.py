import os
import re

searchString=r"reset_event"
#searchRoot=os.environ["VOICEEDITORROOT"]
#searchRoot="C:\Users\uvm\Projects\UVM"
searchRoot="C:\Users\uvm\Projects\iic"
#searchRoot="C:\Users\uvm\Projects\uvm_tb_gen\scripts"
#searchRoot="C:\Users\uvm\Projects\iic_b2b"

for path,directories,files in os.walk(searchRoot):
 if(path.endswith("snapshot")):
  continue
 for file in files:
  fullFileName=os.path.join(path,file)
  if ( not fullFileName.endswith((".py",".txt",".template",".bat", ".svh", ".sv"))):
   continue
  fileName=fullFileName
  try:
   fileHandle=open(fileName,"r")
  except:
   print ("Unable to open file: ",fileName)
   sys.exit(1)
  else:
   fileList=fileHandle.readlines()
   fileHandle.close()
  lineNumber=0
  for line in fileList :
   m=re.match(r'.*%s'%searchString,line)
   if(m):
    print ("%s: %0d %s"%(fullFileName,lineNumber,line.rstrip()))
   lineNumber+=1

