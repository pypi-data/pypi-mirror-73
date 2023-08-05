name = "csinscapp"
version = "0.0.2"

# tested on remi version = "2020.3.10"
import remi.gui as gui
from remi import start, App
from threading import *
import base64

class Event:
  def __init__(self, type, source, *args):
    self.type = type
    self.control = source
    self.args = args

class Command:
  def __init__(self, command, arg):
    self.command = command
    self.arg = arg

class ControlCommand (Command):
  def __init__(self, command, control, arg):
    self.control = control
    super(ControlCommand, self).__init__(command, arg)

class StyleCommand(ControlCommand):
  def __init__(self, command, control, arg):
    super(StyleCommand, self).__init__(command, control, arg)
  def execute(self):
    self.control.widget.style[self.command] = self.arg

class FunctionCallCommand(ControlCommand):
  def __init__(self, command, control, arg):
    super(FunctionCallCommand, self).__init__(command, control, arg)
  def execute(self):
    self.command(self.arg)



class Control:
  def __init__(self, x, y):
    self.widget.style["position"] = "absolute;"
    self.widget.style["top"] = f"{y}px;"
    self.widget.style["left"] = f"{x}px;"    
    self.widget.style["white-space"] = "pre-wrap;"
    self._visible = True
    self._bgcolor = [0, 0, 0, 1]
    self._color = [255, 255, 255, 1]
    self._padding = [0, 0, 0, 0]
    self._margin = [0, 0, 0, 0]

  @property
  def visible(self): 
    return self._visible
  @visible.setter
  def visible(self, value): 
    self._visible = value

    if CSinSCApp.buffered_mode:
      CSinSCApp.styles[self] = ["display", "inline;" if self._visible == True else "none;"]
    else:
      self.widget.style["display"] = "inline;" if self._visible == True else "none;"

  @property
  def bgcolor(self): 
    return self._bgcolor
  @bgcolor.setter
  def bgcolor(self, value): 
    self._bgcolor = list(value)

    if CSinSCApp.buffered_mode:
      CSinSCApp.commands.append(StyleCommand("background-color", self, f"rgba({self._bgcolor[0]}, {self._bgcolor[1]}, {self._bgcolor[2]}, {self._bgcolor[3]});"))
    else:
      self.widget.style["background-color"] = f"rgba({self._bgcolor[0]}, {self._bgcolor[1]}, {self._bgcolor[2]}, {self._bgcolor[3]});"

  @property
  def padding(self): 
    return self._padding
  @padding.setter
  def padding(self, value): 
    self._padding = list(value)

    if CSinSCApp.buffered_mode:
      CSinSCApp.commands.append(StyleCommand("padding", self, f"{self._padding[0]}px {self._padding[1]}px {self._padding[2]}px {self._padding[3]}px;"))
    else:
      self.widget.style["padding"] = f"{self._padding[0]}px {self._padding[1]}px {self._padding[2]}px {self._padding[3]}px;"

  @property
  def margin(self): 
    return self._margin
  @margin.setter
  def margin(self, value): 
    self._margin = list(value)

    if CSinSCApp.buffered_mode:
      CSinSCApp.commands.append(StyleCommand("margin", self, f"{self._margin[0]}px {self._margin[1]}px {self._margin[2]}px {self._margin[3]}px;"))
    else:
      self.widget.style["margin"] = f"{self._margin[0]}px {self._margin[1]}px {self._margin[2]}px {self._margin[3]}px;"      


  @property
  def color(self): 
    return self._color
  @color.setter
  def color(self, value): 
    self._color = list(value)

    if CSinSCApp.buffered_mode:
      CSinSCApp.commands.append(StyleCommand("color", self, f"rgba({self._color[0]}, {self._color[1]}, {self._color[2]}, {self._color[3]});"))
    else:
      self.widget.style["color"] = f"rgba({self._color[0]}, {self._color[1]}, {self._color[2]}, {self._color[3]});"    

  def setData(self, data):
    pass

class Label (Control):
  def __init__(self, text, x, y, width, height):
    self.widget = gui.Label(text, width = width, height = height)  
    super(Label, self).__init__(x, y)   

    self._fontSize = "12px"
    self._fontFamily = "arial"

    # centred by default
    self.widget.style["display"] = "flex;"
    self.widget.style["justify-content"] = "center;"
    self.widget.style["align-items"] = "center;"
    self.widget.style["text-align"] = "center;"

  @property
  def fontSize(self): 
    return self._fontSize  
  @fontSize.setter
  def fontSize(self, value): 
    # overriding the visible property to "flex" instead of "inline"
    self._fontSize = value

    if CSinSCApp.buffered_mode:
      CSinSCApp.commands.append(StyleCommand("font-size", self, f"{self._fontSize}px"))
    else:    
      self.widget.style["font-size"] = f"{self._fontSize}px"

  @property
  def fontFamily(self): 
    return self._fontFamily  
  @fontFamily.setter
  def fontFamily(self, value): 
    # overriding the visible property to "flex" instead of "inline"
    self._fontFamily = value

    if CSinSCApp.buffered_mode:
      CSinSCApp.commands.append(StyleCommand("font-family", self, f"{self._fontFamily}"))
    else:    
      self.widget.style["font-family"] = f"{self._fontFamily}"      

  @property
  def visible(self): 
    return self._visible  
  @visible.setter
  def visible(self, value): 
    # overriding the visible property to "flex" instead of "inline"
    self._visible = value

    if CSinSCApp.buffered_mode:
      CSinSCApp.commands.append(StyleCommand("display", self, "flex;" if self._visible == True else "none;"))
    else:    
      self.widget.style["display"] = "flex;" if self._visible == True else "none;"  
  
  def setData(self, data):
    if CSinSCApp.buffered_mode:
      CSinSCApp.commands.append(FunctionCallCommand(self.widget.set_text, self, data))
    else:
      self.widget.set_text(data)    

class Button (Control):
  def __init__(self, text, x, y, width, height):
    self.widget = gui.Button(text, width = width, height = height)  
    super(Button, self).__init__(x, y)   

  def setData(self, data):
    if CSinSCApp.buffered_mode:
      CSinSCApp.commands.append(FunctionCallCommand(self.widget.set_text, self, data))
    else:
      self.widget.set_text(data)    

class Image (Control):
  def __init__(self, filename, x, y, width, height):
    self.widget = gui.Image('', width = width, height = height)  

    self.widget.attributes['ondragstart'] = "event.preventDefault();"

    super(Image, self).__init__(x, y)   

    self.cached_filename = None

    if filename is not None and len(filename) > 0:
      self.setData(filename)

  def setData(self, data):
    if data == self.cached_filename:
      return
      
    if CSinSCApp.buffered_mode:
      CSinSCApp.commands.append(FunctionCallCommand(self._setData, self, data))
    else:      
      imageData = CSinSCApp.readResource(data)
      self.widget.set_image("data:image/" + imageData[0] + ";base64," + imageData[1].decode("utf-8"))

      self.cached_filename = data

  def _setData(self, data):
    imageData = CSinSCApp.readResource(data)
    self.widget.set_image("data:image/" + imageData[0] + ";base64," + imageData[1].decode("utf-8"))

    self.cached_filename = data


class CSinSCApp:

  CLICK = 0
  MOUSE_DOWN = 1  
  MOUSE_MOVE = 2

  buffered_mode = False

  resources_cache = {}

  commands = []
  styles = {}

  def __init__(self, width = 640, height = 480):
    self.events = []  
    self.initialised = False

    self.container = gui.Container(width = width, height = height)   
    self.container.style["display"] = "flex;"
    self.container.style["justify-content"] = "center;"
    self.container.style["align-items"] = "top;"         

  def addControl(self, control):
    self.container.append(control.widget)
    control.widget.onclick.do(self.on_click, control)

  def remi_thread(self):
    start(CSinSCApp.MyApp, debug=False, address='0.0.0.0', port=0, multiple_instance = False, userdata = (self,))    

  def main(self):
    self.initialised = True
    return self.container

  def run(self):
    thread_id = Thread(target=self.remi_thread, daemon=True)
    thread_id.daemon = True
    thread_id.start()

    while not self.initialised:
      pass

  def refresh(self, buffer = True):

    CSinSCApp.buffered_mode = buffer
    
    for command in CSinSCApp.commands:
      command.execute()

    # apply all styles
    for control in CSinSCApp.styles.keys():
      control.widget.style[CSinSCApp.styles[control][0]] = CSinSCApp.styles[control][1]

    CSinSCApp.commands = []
    CSinSCApp.styles = {}

  def readResource(filename):

    if filename in CSinSCApp.resources_cache:
      #print(f"found {filename} in resources cache")
      return CSinSCApp.resources_cache[filename]

    resource_ext = filename.split(".")[-1]

    with open(filename, "rb") as resource:
      encoded_string = base64.b64encode(resource.read())

      CSinSCApp.resources_cache[filename] = (resource_ext, encoded_string)

    return (resource_ext, encoded_string)

  class MyApp(App):
    def __init__(self, *args):
      
      self.window = args[-1].userdata[0]
      
      super(CSinSCApp.MyApp, self).__init__(*args)   

    def main(self, userdata):
      return userdata.main()

  def on_click(self, widget, control):
    self.events.append(Event(CSinSCApp.CLICK, control))

  def on_mouse_down(self, widget, x, y, control):
    self.events.append(Event(CSinSCApp.MOUSE_DOWN, widget, x, y))

  def on_mouse_move(self, widget, x, y, control):
    self.events.append(Event(CSinSCApp.MOUSE_MOVE, widget, x, y))    
  
  def get_next_event(self):
    event = Event(None, None)
    if len(self.events) > 0:
      event = self.events[0]
      del self.events[0]
    return event     
