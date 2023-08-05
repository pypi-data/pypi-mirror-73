from .MeowbitHandler import MeowbitHandler

class HardwareHandlerFactory:
  def handle(self, hwVersion, websocket, extensions, userPath):
    if hwVersion == 'meowbit':
      print("handlerfactory 0.0.6")
      return MeowbitHandler(websocket, extensions, userPath)