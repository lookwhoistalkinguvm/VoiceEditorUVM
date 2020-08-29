from AutoMenuBase import AutoMenuBase

class AutoMenuWBSequences(AutoMenuBase):




 def __call__(self,parent,fastButtonAreaHandler):


  nextCommand=parent

  #List wb agent sequence prefabs

  fastButtonAreaHandler.processCommand("fast button list templates")
  fastButtonAreaHandler.processCommand("9")
  fastButtonAreaHandler.processCommand("2")
  fastButtonAreaHandler.processCommand("1")



  return nextCommand




