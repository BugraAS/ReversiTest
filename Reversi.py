from abc import ABC,abstractmethod
import pyray as pr
import numpy as np

gamestate = 0
class Reversi:
    def __init__(self,winsize : np.ndarray) -> None:
        self.exit = False
        self.windim = winsize
        self.winpos = pr.Vector2(0,0)
        self.mousepos = pr.Vector2(0,0)
        self.panoffset = pr.Vector2(0,0)
        self.dragging = False
        self.screen = 0
        self.colors = [
            pr.WHITE,
            pr.DARKGRAY,
            pr.BLACK,
            pr.DARKGREEN,
            pr.DARKBROWN
        ]
        self.bgcolor : pr.Color = self.colors[3]

    def render(self) -> None:
        pr.begin_drawing()
        pr.clear_background(self.bgcolor)
        self.exit = pr.gui_window_box(pr.Rectangle(0,0,self.windim[0],self.windim[1]),"#198#TestWindow")
        pr.gui_set_style(1,1,1)
        Screen[gamestate]
        pr.end_drawing()
    
    def drag(self) ->None:
        pass

    def logicops(self) -> None:
        pass

    def eventops(self) -> None:
        self.mousepos = pr.get_mouse_position()
        if pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT) and pr.check_collision_point_rec(self.mousepos,pr.Rectangle(0,0,self.windim[0],20)):
            self.panoffset = self.mousepos
            self.dragging = True
        if self.dragging:
            self.winpos.x += self.mousepos.x - self.panoffset.x
            self.winpos.y += self.mousepos.y - self.panoffset.y
            if pr.is_mouse_button_released(pr.MOUSE_BUTTON_LEFT): self.dragging = False
            pr.set_window_position(int(self.winpos.x),int(self.winpos.y))

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
        x = cls.screens[val]
        x.render()
        for i in range(len(x.gui)):
            if x.gui[i].render() : x.handle[i]()

class Screen(metaclass=ScreenMeta):
    screens = []
    def __init__(self, rendfunc, guilist, handlers) -> None:
        self.render = rendfunc
        self.gui = guilist
        self.handle = handlers
        Screen.screens.append(self)

class GuiItem(ABC):
    def __init__(self,pos,dims) -> None:
        self.dims = dims
        self.pos = pos
        self.box = pr.Rectangle(pos[0],pos[1],dims[0],dims[1])
    @abstractmethod
    def render(self):
        pass
class ClickButton(GuiItem):
    def __init__(self, pos, dims, label :str) -> None:
        super().__init__(pos, dims)
        self.str = label
        self.state : bool
    def render(self):
        return pr.gui_button(self.box,self.str)

class KeyIter:
    def __init__(self,func) -> None:
        self.key = func
    def __iter__(self):
        self.i :int
        return self
    def __next__(self) -> int:
        self.i = self.key()
        if self.i == 0:raise StopIteration
        return self.i

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