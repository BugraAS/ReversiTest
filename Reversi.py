from abc import ABC,abstractmethod
import pyray as pr
import numpy as np

class Reversi:
    def __init__(self,winsize : np.ndarray) -> None:
        self.state = 0
        self.exit = False
        self.windim = winsize
        self.winpos = pr.Vector2(0,0)
        self.mousepos = pr.Vector2(0,0)
        self.panoffset = pr.Vector2(0,0)
        self.dragging = False
        self.guipos : pr.Vector2
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
        pr.clear_background(self.bgcolor)
        self.exit = pr.gui_window_box(pr.Rectangle(0,0,self.windim[0],self.windim[1]),"#198#TestWindow")
        pr.draw_text(f"the states are {pr.gui_get_state()}",200,200,10,self.colors[2])
        pr.draw_rectangle_rec(self.bgrect,self.bgcolor)
        pr.draw_rectangle_lines_ex(self.bgrect,9.,self.colors[5])
        self.gridpos = pr.gui_grid(pr.Rectangle(100,100,320,320),40.,1)
        pr.draw_text(f"Grid pos is {self.gridpos.x} {self.gridpos.y}",250,30,10,self.colors[2])
        Screen[self.state].render(self)
        pr.end_drawing()
    
    def drag(self) ->None:
        self.winpos.x += self.mousepos.x - self.panoffset.x
        self.winpos.y += self.mousepos.y - self.panoffset.y
        if pr.is_mouse_button_released(pr.MOUSE_BUTTON_LEFT): self.dragging = False
        pr.set_window_position(int(self.winpos.x),int(self.winpos.y))

    def logicops(self) -> None:
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

class ScreenMeta(type):
    def __getitem__(cls,val):
        return cls.screens[val]

class Screen(ABC,metaclass=ScreenMeta):
    screens = []
    def __init__(self, rendfunc, boxes, text, clickables) -> None:
        self.func = rendfunc
        self.box = boxes
        self.text = text
        self.button = clickables
        Screen.screens.append(self)
    def render(self, arg:Reversi) -> None:
        self.func(self)
        self.boxes.render()
        self.text.render()
        self.button.render(arg)

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
    def __init__(self, pos, dims, label :str, handler :function) -> None:
        super().__init__(pos, dims)
        self.str = label
        self.state : bool
        self._handler = handler
    def render(self, arg: Reversi) -> None:
        self.state = pr.gui_button(self.box,self.str)
        if self.state: self.handler(arg)
        return self.state

class Rectangle(BoxItem):
    def __init__(self, pos, dims, color : pr.Color) -> None:
        super().__init__(pos, dims)
        self.color = color
    def render(self) -> None:
        pr.draw_rectangle_rec(self.box,self.color)

class TextItem(UiItem):
    def __init__(self, pos, size:int, color: pr.Color) -> None:
        super().__init__(pos)


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

noop = lambda *args,**kargs:None
mainmenu : Screen = Screen(
    noop ,
    [
        ClickButton([50,250],[150,75],"Start")
    ],
    [
        lambda *args:None
    ]
)

if __name__ == "__main__":
    begin : Reversi = Reversi(np.array([600,450]))
    begin.main()