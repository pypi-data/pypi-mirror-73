from .MeowbitHandler import MeowbitHandler

class HardwareHandlerFactory:
  def handle(self, hwVersion, websocket, extensions, userPath):
    if hwVersion == 'meowbit':
      print("handler factory 0.0.5")
      return MeowbitHandler(websocket, extensions, userPath)
