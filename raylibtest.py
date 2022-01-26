from pyray import *
init_window(800, 450, "Hello")
while not window_should_close():
    begin_drawing()
    clear_background(WHITE)
    draw_text("Hello world", 190, 200, 20, VIOLET)
    end_drawing()
close_window()

class Iterator:
    def __init__(self,count:int) -> None:
        self.count = count
    def __iter__(self):
        self.i = 0
        return self
    def __next__(self) -> int:
        if self.i == self.count: raise StopIteration
        self.i += 1
        return self.i
for i in Iterator(5):
    print(i)