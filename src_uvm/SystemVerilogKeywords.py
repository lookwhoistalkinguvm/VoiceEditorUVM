import os
import sys

class SystemVerilogKeywords(object):



 def __init__(self ):

  voiceEditorRoot=os.environ["VOICEEDITORROOT"]
  fileName=voiceEditorRoot+ r'\src_uvm\systemVerilogKeywords.txt'
  try:
   fileHandle=open(fileName,"r")
  except:
   print ("Unable to open file: ",fileName)
   sys.exit(1)
  else:
   fileList=fileHandle.readlines()
   fileHandle.close()

  self.keywordsList=map(str.strip,fileList)


