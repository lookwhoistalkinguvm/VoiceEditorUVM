
import re
import os

class ScanFileForVariables(object):



 def __call__(self,fullFileName,editLineNumber=0):

  doClassMatch=0
  doModuleMatch=0
  doInterfaceMatch=0
  doMethodMatch=0
  self.classVariableList=[];
  self.isRandClassVariable={}
  variable=""
  self.methodVariableList=[]
  self.tokenList=[]
  localVariablesLatched=0
  self.className=""
  self.interfaceName=""
  self.moduleName=""
  self.isModulePortDefinitionLine=0


  fileName=fullFileName
  try:
   fileHandle=open(fileName,"r")
  except:
   sys.exit(1)
  else:
   fileList=fileHandle.readlines()
   fileHandle.close()


  if(fullFileName.endswith(".svh") or fullFileName.endswith(".sv") or fullFileName.endswith(".v")):
   commentCharacter=r'//'
  else:
   commentCharacter=r'#'


  lineNumber=0

  for line in fileList:

   line= line.rstrip()

    # Skip Comment Lines

   commentLineMatch=re.match(r'\s*%s'%(commentCharacter),line)
   if (commentLineMatch):
    continue

   self.tokenList.extend(re.findall(r"[\w']+",line))

   ## Class Match

   startClassMatch=re.match(
    r'''
    \s*class\s+(?P<className>\w+)(\s*\#\(\w+\))?\s+extends
    ''',
    line,
    re.VERBOSE
   )
   if(startClassMatch):
    self.className=startClassMatch.group("className")

   endClassMatch=re.match(
    r'''
    \s*endclass\s*
    ''',
    line,
    re.VERBOSE
   )

   if(startClassMatch):
    doClassMatch=1

   if(endClassMatch):
    doClassMatch=0


   ## Interface Match

   startInterfaceMatch=re.match(
    r'''
    \s*interface\s+(?P<interfaceName>\w+)(\s*\#\(\w+\))?(\s*\(.*\))?\s*;
    ''',
    line,
    re.VERBOSE
   )
   if(startInterfaceMatch):
    self.interfaceName=startInterfaceMatch.group("interfaceName")

   endInterfaceMatch=re.match(
    r'''
    \s*endinterface\s*
    ''',
    line,
    re.VERBOSE
   )

   if(startInterfaceMatch):
    doInterfaceMatch=1

   if(endInterfaceMatch):
    doInterfaceMatch=0


   ## Module Match

   startModuleMatch=re.match(
    r'''
    \s*module\s+(?P<moduleName>\w+)
    ''',
    line,
    re.VERBOSE
   )
   if(startModuleMatch):
    self.moduleName=startModuleMatch.group("moduleName")

   endModuleMatch=re.match(
    r'''
    \s*endmodule\s*
    ''',
    line,
    re.VERBOSE
   )

   if(startModuleMatch):
    doModuleMatch=1

   if(endModuleMatch):
    doModuleMatch=0



   ## Method Match

   startMethodMatch=re.match(
    r'''
    \s*(task|function)\s
    ''',
    line,
    re.VERBOSE
   )

   endMethodMatch=re.match(
    r'''
    \s*(endfunction|endtask)\s*
    ''',
    line,
    re.VERBOSE
   )

   if (startMethodMatch):
    doMethodMatch=1

   if(endMethodMatch):
    doMethodMatch=0
    if (lineNumber>=editLineNumber):
     localVariablesLatched=1


   # Module Port Definition
   modulePortMatch=re.match(
    r'''
    \s*(input|output)\s+
    ''',
    line,
    re.VERBOSE
   )


   # Gather Variables

   if (doClassMatch or doInterfaceMatch or doModuleMatch ):

    standardVariableMatch=re.match(
     r'''
     \s*(?P<rand>rand\s+)?(\w+)(\s*[#]\(.*\))?(\s*\[.*\])?\s+(?P<variable>\w+)\s*;
     ''',
     line,
     re.VERBOSE
    )

    if(standardVariableMatch):

     variable=standardVariableMatch.group("variable")
     rand=standardVariableMatch.group("rand")

     if(doModuleMatch):

      if (modulePortMatch):
       self.classVariableList.append(variable)
      else:
       self.methodVariableList.append(variable)

     else:

      self.classVariableList.append(variable)
      if(rand):
       self.isRandClassVariable[variable]=1
      else:
       self.isRandClassVariable[variable]=0


    virtualInterfaceMatch=re.match(
     r'''
     \s*virtual\s+(\w+)\s+(?P<variable>\w+)\s*;
     ''',
     line,
     re.VERBOSE
    )

    if (virtualInterfaceMatch):
     variable=virtualInterfaceMatch.group("variable")
     self.isRandClassVariable[variable]=0
     self.classVariableList.append(variable)


   if (doMethodMatch and not localVariablesLatched):

    m=re.match(
     r'''
     \s*(\w+)\s*(\[.*\])?\s+(?P<variable>\w+)\s*(\[.*\])?\s*;
     ''',
     line,
     re.VERBOSE
    )

    if(m):
     variable=m.group("variable")
     self.methodVariableList.append(variable)


   lineNumber+=1




