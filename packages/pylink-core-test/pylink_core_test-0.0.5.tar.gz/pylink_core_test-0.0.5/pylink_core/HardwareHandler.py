from .ExecThread import *
from .Uf2Manager import *
from .SerialCom import serialList, serialCom
from .uflash import getDisk
from .ImageManager import saveToBmp
from .kerror import KERR
import shutil

class HardwareHandler:
  def __init__(self, websocket, extensions, userPath):
    self.ws = websocket
    self.extensions = extensions
    self.ext = None
    self.comm = None
    self.commType = None
    self.commList = []
    self.uploadTh = None
    self.pid = 0
    self.params = []
    self.userPath = userPath

  def sendResp(self, pid, result, error=None):
      """发送response"""
      res = {
          "jsonrpc":"2.0",
          "id": pid,
          "result": result
      }
      if error:
          res['error'] = error
      self.ws.send(json.dumps(res))

  def sendReq(self,method, params={}):
      """发送request"""
      req = {
          "jsonrpc":"2.0",
          "method":method,
          "params": params
      }
      self.ws.send(json.dumps(req))

  def commRx(self,msg, dt):
      """发送串口读到的数据"""
      if msg == None and dt == -1:
          self.sendReq('connclose')
      else:
          b64 = str(base64.b64encode(msg), 'utf8')
          self.sendReq("data", {"data": b64})

  def handle(self,message):
      """
      供外部使用的方法
      处理收到消息的method/params/id
      根据收到消息的method执行名称对应的方法
      """
      obj = json.loads(message)
    #   print('obj', obj)
      if 'id' in obj:
          self.pid = obj['id']
      if 'params' in obj:
          self.params = obj['params']
      method = obj['method']
      method = method.replace("-", "_")
      func = getattr(self, method, None)
      func()

  def sync(self):
    """与前端连接建立收到第一条消息"""
    extId = self.params['extensionId']
    self.ext = self.extensions[extId]
    self.sendResp(self.pid, self.ext)
  
  def listdevice(self):
    """查看可用串口列表"""
    serPorts = serialList()
    self.commList = serPorts
    self.sendResp(self.pid, self.commList)

  def connect(self):
    """连接串口"""
    peripheralId = self.params['peripheralId']
    port = None
    for p in self.commList:
        if p['peripheralId'] == peripheralId:
            port = p
            break
    try:
      if p['type'] == 'serial':
          self.comm = serialCom(self.commRx)
          self.comm.connect(p['peripheralId'], baud=115200)
          self.commType = 'serial'
      self.sendResp(self.pid, p)
    except Exception as e:
      err = {
          "msg": str(e),
          "code": KERR.SERIAL_COMM_ERROR
      }
      self.sendResp(self.pid, None, error=err)

  def disconnect(self):
    if self.comm :
      self.comm.close()
      print('comm close')
      
  def write(self):
    """通过串口写数据"""
    msg = self.params['data']
    msg = base64.b64decode(msg)
    # print(msg)
    if self.comm:
        self.comm.write(msg)