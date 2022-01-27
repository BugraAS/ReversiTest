from abc import ABC,abstractmethod
from itertools import chain
from dataclasses import dataclass
from network import Network
import pyray as pr
import numpy as np

addr = ("<Server IP goes here>",5555)

client = Network(addr)


class Reversi:
    def __init__(self,winsize : np.ndarray) -> None:
        self.board = np.zeros((8,8),dtype=np.int8)
        self.exit = False
        self.windim = winsize
        self.winpos = pr.Vector2(0,0)
        self.mousepos = pr.Vector2(0,0)
        self.panoffset = pr.Vector2(0,0)
        self.dragging = False
        self.gridpos = pr.Vector2(-1,-1)
        self.bgrect = pr.Rectangle(3,26,winsize[0]-6,winsize[1]-29)
        self.colors = (
            pr.WHITE,
            pr.DARKGRAY,
            pr.BLACK,
            pr.DARKGREEN,
            pr.DARKBROWN,
            pr.get_color(0x005721FF) # Darker Green
        )
        self.bgcolor : pr.Color = self.colors[3]

    def render(self) -> None:
        pr.begin_drawing()
        self.exit = pr.gui_window_box(pr.Rectangle(0,0,self.windim[0],self.windim[1]),"#198#TestWindow")
        pr.clear_background(self.bgcolor)
        pr.draw_rectangle_rec(self.bgrect,self.bgcolor)
        pr.draw_rectangle_lines_ex(self.bgrect,9.,self.colors[5])
        self.gridpos = pr.gui_grid(pr.Rectangle(250,75,320,320),40.,1)
        pr.draw_text(f"Grid pos is {self.gridpos.x} {self.gridpos.y}",150,40,10,self.colors[2])
        Screen[None].render()
        pr.end_drawing()
    
    def drag(self) ->None:
        self.winpos.x += self.mousepos.x - self.panoffset.x
        self.winpos.y += self.mousepos.y - self.panoffset.y
        if pr.is_mouse_button_released(pr.MOUSE_BUTTON_LEFT): self.dragging = False
        pr.set_window_position(int(self.winpos.x),int(self.winpos.y))

    def logicops(self) -> None:
        texts.var[0] = pr.get_time()
        pass

    def eventops(self) -> None:
        self.mousepos = pr.get_mouse_position()
        if pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT) and pr.check_collision_point_rec(self.mousepos,pr.Rectangle(0,0,self.windim[0],20)):
            self.panoffset = self.mousepos
            self.dragging = True
        if self.dragging:
            self.drag()

    def main(self) -> None:
        pr.set_config_flags(pr.FLAG_WINDOW_UNDECORATED)
        pr.init_window(self.windim[0],self.windim[1],"someone help")
        self.winpos = pr.get_window_position()
        pr.set_target_fps(30)
        pr.set_exit_key(7)
        while not (pr.window_should_close() or self.exit):
            self.eventops()
            self.logicops()
            self.render()
        pr.close_window()

@dataclass
class StrHolder:
    var = ["" , "", "", ""]
    def set(self,index :int, arg):
        self.var[index] = arg
        return arg
texts = StrHolder()

class ScreenMeta(type):
    def __getitem__(cls,key=None):
        return cls.screens[Screen.state]

class Screen(metaclass=ScreenMeta):
    screens = []
    state = 0
    def __init__(self, rendfunc, *args) -> None:
        self.func = rendfunc
        self.objects = [*args]
        Screen.screens.append(self)
    def render(self) -> None:
        for i in chain.from_iterable(self.objects):
            if self.func(i):
                i.handle()
                break
    @staticmethod
    def setState(arg : int):
        Screen.state = arg

class UiItem(ABC):
    def __init__(self,pos) -> None:
        self.pos = pos
    @abstractmethod
    def render(self):
        pass

class BoxItem(UiItem,ABC):
    def __init__(self, pos, dims) -> None:
        super().__init__(pos)
        self.box = pr.Rectangle(pos[0],pos[1],dims[0],dims[1])
    @abstractmethod
    def render(self) -> None:
        pass

class ClickButton(BoxItem):
    def __init__(self, pos, dims, label :str, handler) -> None:
        super().__init__(pos, dims)
        self.str = label
        self.state : bool
        self.handle = handler
    def render(self) -> None:
        return pr.gui_button(self.box,self.str)

class Rectangle(BoxItem):
    def __init__(self, pos, dims, color : pr.Color) -> None:
        super().__init__(pos, dims)
        self.color = color
    def render(self) -> None:
        pr.draw_rectangle_rec(self.box,self.color)

class TextItem(UiItem):
    def __init__(self, pos,text:str, size:int, color: pr.Color) -> None:
        super().__init__(pos)
        self.props = (text,size,color)
    def render(self):
        pr.draw_text(self.props[0],self.pos[0],self.pos[1],self.props[1],self.props[2])
class FormattedText(TextItem):
    def __init__(self, pos, text: str, size: int, color: pr.Color,holder : StrHolder,index :int) -> None:
        super().__init__(pos, text, size, color)
        self.var = holder
        self.index = index
    def render(self):
        pr.draw_text(self.props[0].format(self.var.var[self.index]),self.pos[0],self.pos[1],self.props[1],self.props[2])
class OthelloBoard(BoxItem):
    def __init__(self, pos, dim, colors) -> None:
        super().__init__((pos[0]-10,pos[1]-10), (dim+20,dim+20))
        self.board = pr.Rectangle(pos[0],pos[1],dim,dim)
        self.cellsize = dim / 8
        self.color = colors
        self.state = np.zeros((8,8),dtype=np.int8)
        self.position : pr.Vector2
    def render(self):
        pr.draw_rectangle_rec(self.box,self.color[0])
        pr.draw_rectangle_rec(self.board,self.color[1])
        self.position = pr.gui_grid(self.board,self.cellsize,1)
# Unused class
#class KeyIter:
#    def __init__(self,func) -> None:
#        self.key = func
#    def __iter__(self):
#        self.i :int
#        return self
#    def __next__(self) -> int:
#        self.i = self.key()
#        if self.i == 0:raise StopIteration
#        return self.i

mainmenu : Screen = Screen(
    lambda x: (x.render() if hasattr(x,"render") else None),
    (
        Rectangle((15,100),(150,50),pr.DARKGRAY),
        TextItem((25,125),"OTHELLO",7,pr.BLACK)
    ),
    (
        ClickButton((15,165),(150,50),"This is a Button",lambda:Screen.setState(1)),
    )
)
serverScreen : Screen = Screen(
    lambda x : (x.render() if hasattr(x,"render") else None),
    (
        FormattedText((50,250),"Current time is {}",10,pr.BLACK,texts,1),
    ),
    (
        ClickButton((30,50),(150,50),"Attempt Connection",lambda:Screen.setState(2) if texts.set(1,client.handshake()) else None ),
    )
)
othello : Screen = Screen(
    lambda:None,
    (
        FormattedText((50,50),"Server response: {}",10,pr.BLACK,texts,1),
    ),
    (
        OthelloBoard((250,75),320,(pr.DARKBROWN,pr.DARKGRAY)),
    )
)



if __name__ == "__main__":
    begin : Reversi = Reversi(np.array([600,450]))
    begin.main()