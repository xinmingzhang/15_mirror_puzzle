import random
from kivy.app import App
from kivy.lang import Builder
from kivy.graphics.transformation import Matrix
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty, ListProperty
from kivy.uix.popup import Popup
from kivy.clock import Clock

matrix_1 = Matrix().scale(-1, 1, 1).translate(Window.width, 0, 0)

matrix_2 = Matrix().scale(1, -1, 1).translate(0, Window.height, 0)

matrix_3 = Matrix().scale(-1, -1, 1).translate(Window.width, Window.height, 0)

KV = '''
#:import rr random.random
#:import Window kivy.core.window.Window
#:import matrix_1 __main__.matrix_1
#:import matrix_2 __main__.matrix_2
#:import matrix_3 __main__.matrix_3

<Area>:
    size_hint:None,None
    size:Window.width/2,Window.height/2


<Block>:
    size_hint:None,None
    size:Window.width/8,Window.height/8
    font_size:self.size[1]-10
    color:1,1,1,1
    canvas.before:
        Color:
            rgba:0,0,0,0.5
        Rectangle:
            size:self.size
            pos:self.pos
        Color:
            rgba:1,1,1,1
        Line:
            points:[self.x,self.y,self.right,self.y,self.right,self.top,self.x,self.top]
            width:1
            joint:'bevel'
            close:True


<NumberBlock>:

<Area1@Area>:
    canvas:
        Color:
            rgba:239/255.0,206/255.0,232/255.0,1
        Rectangle:
            size:self.size
            pos:self.pos
<Area2@Area>:
    canvas.before:
        PushMatrix
        MatrixInstruction:
            matrix:matrix_1
    canvas:
        Color:
            rgba:243/255.0,215/255.0,181/255.0,1
        Rectangle:
            size:self.size
            pos:self.pos
    canvas.after:
        PopMatrix

<Area3@Area>:
    canvas.before:
        PushMatrix
        MatrixInstruction:
            matrix:matrix_2
    canvas:
        Color:
            rgba:253/255.0,255/255.0,223/255.0,1
        Rectangle:
            size:self.size
            pos:self.pos
    canvas.after:
        PopMatrix

<Area4@Area>:
    canvas.before:
        PushMatrix
        MatrixInstruction:
            matrix:matrix_3
    canvas:
        Color:
            rgba:218/255.0,249/255.0,202/255.0,1
        Rectangle:
            size:self.size
            pos:self.pos
    canvas.after:
        PopMatrix

<Victory>:
    size_hint: 0.7,0.7
    pos_hint:{'center_x':0.5,'center_y':0.5}
    separator_height:0
    title:'Victory'
    title_align:'center'
    auto_dismiss:False
    FloatLayout:
        canvas:
            Color:
                rgba:199/255.0,179/255.0,229/255.0,1
            Rectangle:
                size:self.size
                pos:self.pos
        Label:
            pos_hint:{'center_x':0.5,'center_y':0.8}
            size_hint:0.8,0.3
            text:'You have spend {}s'.format(app.root.time)
            font_size:self.size[1]/3
        Label:
            pos_hint:{'center_x':0.5,'center_y':0.5}
            size_hint:0.8,0.5
            text:'Congratulations!'
            font_size:self.size[1]/3
        Button:
            pos_hint:{'center_x':0.5,'center_y':0.2}
            background_color:239/255.0,206/255.0,232/255.0,1
            size_hint:0.25,0.15
            text:'Replay'
            font_size:self.size[1]/2
            on_press:root.dismiss();app.start_new_game()


<Title@BoxLayout>:
    size_hint:None,None
    size:Window.width/2,Window.height/2
    orientation:'vertical'
    on_touch_down:app.start_new_game()
    Label:
    Label:
        text:'15'
        font_size:self.size[1]
        color:0.5,0.5,0.5,1
    Label:
        text:'MIRROR'
        font_size:self.size[1]
        color:0.5,0.5,0.5,1
    Label:
        text:'SLIDE'
        font_size:self.size[1]
        color:0.5,0.5,0.5,1
    Label:
        text:'PUZZLE'
        font_size:self.size[1]
        color:0.5,0.5,0.5,1
    Label:
    Label:
        text:'tap to start the game'
        font_size:self.size[1]/2
        color:0.5,0.5,0.5,1
    Label:

GameBoard:
    area1:area1
    area2:area2
    area3:area3
    area4:area4
    Area1:
        id:area1
        Title:
    Area2:
        id:area2
        Title:
    Area3:
        id:area3
        Title:
    Area4:
        id:area4
        Title:

'''


class Block(Label):
    pass


class NumberBlock(Block):
    npos = NumericProperty(100)

    def __init__(self, n1, n2, *args):
        super(NumberBlock, self).__init__(*args)
        self.num = n1
        self.text = str(self.num + 1)
        self.npos = n2

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            app = App.get_running_app()
            for i in self.neighbour_nums:
                if app.root.situation[i] == 15:
                    self.move(i)

    def move(self, i):
        app = App.get_running_app()
        app.root.situation[self.npos], app.root.situation[i] = app.root.situation[i], app.root.situation[self.npos]
        self.npos = i

    def on_npos(self, *args):
        n = self.npos
        a = n % 4
        b = 3 - n // 4
        self.center = ((a + 0.5) * Window.width / 8, (b + 0.5) * Window.height / 8)

    @property
    def neighbour_nums(self):
        n = self.npos
        a = n % 4
        b = 3 - n // 4
        neighbours_co = [(a - 1, b), (a + 1, b), (a, b - 1), (a, b + 1)]
        neighbours = [n for n in neighbours_co if n[0] not in (-1, 4) and n[1] not in (-1, 4)]
        nums = [n[0] + (3 - n[1]) * 4 for n in neighbours]
        return nums


class Area(Widget):
    pass

class GameBoard(FloatLayout):
    situation = ListProperty([15 for x in range(16)])
    time = NumericProperty(0)

    def on_situation(self, *args):
        if self.situation == [x for x in range(16)]:
            App.get_running_app().end_game()

    def update_time(self,*args):
        self.time += 1


    def on_touch_down(self, touch):
        if Widget(pos=(0, 0), size=(Window.width / 2, Window.height / 2)).collide_point(*touch.pos):
            self.area1.on_touch_down(touch)
        elif Widget(pos=(Window.width / 2, 0), size=(Window.width / 2, Window.height / 2)).collide_point(*touch.pos):
            touch.pos = (Window.width - touch.pos[0], touch.pos[1])
            self.area2.on_touch_down(touch)
        elif Widget(pos=(0, Window.height / 2), size=(Window.width / 2, Window.height / 2)).collide_point(*touch.pos):
            touch.pos = (touch.pos[0], Window.height - touch.pos[1])
            self.area3.on_touch_down(touch)
        elif Widget(pos=(Window.width / 2, Window.height / 2),
                    size=(Window.width / 2, Window.height / 2)).collide_point(*touch.pos):
            touch.pos = (Window.width - touch.pos[0], Window.height - touch.pos[1])
            self.area4.on_touch_down(touch)


class Victory(Popup):
    pass


class MyGame(App):

    def puzzle_init(self):
        while True:
            init_p = [i for i in range(15)]
            random.shuffle(init_p)
            n = 0
            for i in range(15):
                smaller_num = [x for x in init_p[i + 1:] if x < init_p[i]]
                n += len(smaller_num)
            if n % 2 == 0:
                return init_p

    def end_game(self):
        root = App.get_running_app().root
        Victory().open()
        Clock.unschedule(root.update_time)

    def start_new_game(self):
        root = App.get_running_app().root
        root.area1.clear_widgets()
        root.area2.clear_widgets()
        root.area3.clear_widgets()
        root.area4.clear_widgets()

        l1 = [i for i in range(15)]
        l2 = self.puzzle_init()

        for i1, i2 in zip(l1, l2):
            root.situation[i2] = i1
            a = random.randint(1, 4)
            if a == 1:
                root.area1.add_widget(NumberBlock(i1, i2))
            elif a == 2:
                root.area2.add_widget(NumberBlock(i1, i2))
            elif a == 3:
                root.area3.add_widget(NumberBlock(i1, i2))
            elif a == 4:
                root.area4.add_widget(NumberBlock(i1, i2))
        root.time = 0
        Clock.schedule_interval(root.update_time, 1)

    def build(self):
        root = Builder.load_string(KV)
        return root


if __name__ == '__main__':
    MyGame().run()
