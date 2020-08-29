from AutoMenuBase import AutoMenuBase

class AutoMenuObjectMacroTemplates(AutoMenuBase):




 def __call__(self,parent,fastButtonAreaHandler):


  nextCommand=parent

  #List objects macro templates

  fastButtonAreaHandler.processCommand("fast button list templates")
  fastButtonAreaHandler.processCommand("5")
  fastButtonAreaHandler.processCommand("0")



  return nextCommand




