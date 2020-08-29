from AutoMenuBase import AutoMenuBase

class AutoMenuStartSequence(AutoMenuBase):




 def __call__(self,parent,fastButtonAreaHandler):


  nextCommand=parent

  #List sequencer handles from virtual sequence

  fastButtonAreaHandler.processCommand("fast button list templates")
  fastButtonAreaHandler.processCommand("9")
  fastButtonAreaHandler.processCommand("1")
  fastButtonAreaHandler.processCommand("1")


  return nextCommand




