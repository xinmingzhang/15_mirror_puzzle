import json
import random

from math import sin,cos

from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.graphics import Rectangle
from kivy.graphics.texture import Texture
from kivy.core.text import LabelBase
from kivy.properties import OptionProperty
from kivy.app import App
from kivy.lang import Builder
from kivy.graphics.transformation import Matrix
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ListProperty,StringProperty
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.graphics import PushMatrix,PopMatrix,Translate,MatrixInstruction


matrix_0 = Matrix()

matrix_1 = Matrix().scale(-1, 1, 1)

matrix_2 = Matrix().scale(1, -1, 1)

matrix_3 = Matrix().scale(-1, -1, 1)


KV = '''
#:import rr random.random
#:import Window kivy.core.window.Window
#:import matrix_1 __main__.matrix_1
#:import matrix_2 __main__.matrix_2
#:import matrix_3 __main__.matrix_3
#:import FadeTransition kivy.uix.screenmanager.FadeTransition

<Area>:
    size_hint:None,None
    size:Window.width/2,Window.height/2

<Area1@Area>:
    canvas.before:
        PushMatrix
        Translate:
            xy:(Window.width/2, Window.height/2)
    canvas:
        Color:
            rgba:239/255.0,206/255.0,232/255.0,1
        Rectangle:
            size:self.size
            pos:self.pos
    canvas.after:
        PopMatrix
<Area2@Area>:
    canvas.before:
        PushMatrix
        Translate:
            xy:(Window.width/2, Window.height/2)
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
        Translate:
            xy:(Window.width/2, Window.height/2)
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
        Translate:
            xy:(Window.width/2, Window.height/2)
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


<Block>:
    size_hint:None,None
    size:Window.width/8,Window.height/8
    font_size:self.height/2
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
    center:((self.npos % 4 + 0.5) * Window.width / 8, ((3 - self.npos // 4) + 0.5) * Window.height / 8)

<Victory>:
    size_hint: 0.7,0.7
    pos_hint:{'center_x':0.5,'center_y':0.5}
    separator_height:0
    title:'Victory' if app.language=='EN' else '胜利'
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
            size_hint:1,0.3
            text:'{}/{}'.format(app.root.current_screen.time,app.root.current_screen.moves)
            font_size:min(self.height/3,self.width/len(self.text))
        Label:
            pos_hint:{'center_x':0.5,'center_y':0.5}
            size_hint:1,0.5
            text:'Congratulations!'if app.language=='EN' else '恭喜成功'
            font_size:min(self.height/3,self.width/len(self.text))
        Button:
            pos_hint:{'center_x':0.3,'center_y':0.2}
            background_color:239/255.0,206/255.0,232/255.0,1
            size_hint:0.25,0.15
            text:'Replay' if app.language=='EN' else '重玩'
            font_size:min(self.height/3,self.width/len(self.text))
            on_press:root.dismiss();app.root.current_screen.on_enter()
        Button:
            pos_hint:{'center_x':0.7,'center_y':0.2}
            background_color:239/255.0,206/255.0,232/255.0,1
            size_hint:0.25,0.15
            text:'Back'if app.language=='EN' else '返回'
            font_size:min(self.height/3,self.width/len(self.text))
            on_press:root.dismiss();app.root.current='title'

<MLabel>:

<MB>:

<Title>:
    size_hint:None,None
    size:Window.size
    BoxLayout:
        orientation:'vertical'
        spacing:self.height/25
        padding:[self.width/4,self.width/8,self.width/4,self.width/8]
        MLabel:
            text:'15 Mirror Puzzle' if app.language=='EN' else '15 镜像拼图'
            font_size:Window.height/12
            color:0.5,0.5,0.5,1
        Widget:
        Button:
            text:'PLAY' if app.language=='EN' else '开始游戏'
            color:0.5,0.5,0.5,1
            font_size:Window.height/15
            background_normal: ''
            background_color:[239/255.0,206/255.0,232/255.0,0.8]
            on_press:app.root.current = 'game'
        Button:
            text:'SETTINGS' if app.language=='EN' else '游戏设置'
            color:0.5,0.5,0.5,1
            background_normal: ''
            font_size:Window.height/15
            background_color:[243/255.0,215/255.0,181/255.0,0.8]
            on_press:app.root.current  = 'settings'
        Button:
            text:'HELP' if app.language=='EN' else '游戏帮助'
            color:0.5,0.5,0.5,1
            font_size:Window.height/15
            background_normal: ''
            background_color:[253/255.0,255/255.0,223/255.0,0.8]
            on_press:app.root.current  = 'help'
        Button:
            text:'RECORDS'if app.language=='EN' else '游戏记录'
            color:0.5,0.5,0.5,1
            background_normal: ''
            font_size:Window.height/15
            background_color:[218/255.0,249/255.0,202/255.0,0.8]
            on_press:app.root.current = 'records'

<Mode>:
    size_hint:None,None
    size:Window.size
    BoxLayout:
        orientation:'vertical'
        spacing:self.height/20
        padding:[self.width/4,self.width/6,self.width/4,self.width/6]
        Label:
            text:'Settings' if app.language=='EN' else '游戏设置'
            font_size:Window.height/10
            color:0.5,0.5,0.5,1
        Button:
            text:'Language\\nEnglish' if app.language=='EN' else '语言\\n中文'
            color:0.5,0.5,0.5,1
            halign: 'center'
            font_size:Window.height/15
            background_normal: ''
            background_color:[239/255.0,206/255.0,232/255.0,0.8]
            on_press:app.switch_language()
        Button:
            t1:'Mode\\nNormal'if app.language=='EN' else '模式\\n普通'
            t2:'Mode\\nNightmare'if app.language=='EN' else '模式\\n噩梦'
            t3:'Mode\\nHell'if app.language=='EN' else '模式\\n地狱'
            text:self.t1 if app.mode=='normal' else (self.t2 if app.mode == 'nightmare' else self.t3)
            color:0.5,0.5,0.5,1
            halign: 'center'
            background_normal: ''
            font_size:Window.height/15
            background_color:[243/255.0,215/255.0,181/255.0,0.8]
            on_press:app.switch_mode()
    Button:
        size_hint:0.1,0.1
        text:'Back'if app.language=='EN' else '返回'
        pos_hint:{'center_x':0.1,'center_y':0.1}
        color:0.5,0.5,0.5,1
        font_size:self.width/2
        background_normal: ''
        background_color:[253/255.0,255/255.0,223/255.0,0.8]
        on_press:app.root.current = 'title'
    Button:
        size_hint:0.1,0.1
        text:'Start'if app.language=='EN' else '开始'
        pos_hint:{'center_x':0.9,'center_y':0.1}
        color:0.5,0.5,0.5,1
        font_size:self.width/2
        background_normal: ''
        background_color:[218/255.0,249/255.0,202/255.0,1]
        on_press:app.root.current = 'game'

<Records>:
    Label:
        pos_hint:{'center_x':0.5,'center_y':0.9}
        text:'Records' if app.language=='EN' else '游戏记录'
        font_size:Window.height/10
        color:0.5,0.5,0.5,1
    Label:
        pos_hint:{'center_x':0.5,'center_y':0.5}
        font_size:Window.height/20
        color:0.5,0.5,0.5,1
        halign: 'center'
        t1:'Normal \\n' + 'Time  ' + self.parent.nt + '  Moves  ' + self.parent.nm + '\\n\\n' + 'Nightmare \\n' + 'Time  ' + self.parent.tt + '  Moves  ' + self.parent.tm + '\\n\\n'+ 'Hell \\n' + 'Time  ' + self.parent.ht + '  Moves  ' + self.parent.hm
        t2:'普通 \\n' + '时间  ' + self.parent.nt + '  步数  ' + self.parent.nm + '\\n\\n' + '噩梦 \\n' + '时间  ' + self.parent.tt + '  步数  ' + self.parent.tm + '\\n\\n'+ '地狱 \\n' + '时间  ' + self.parent.ht + '  步数  ' + self.parent.hm
        text:self.t1 if app.language=='EN' else self.t2
    Button:
        size_hint:0.1,0.1
        text:'Back'if app.language=='EN' else '返回'
        pos_hint:{'center_x':0.1,'center_y':0.1}
        color:0.5,0.5,0.5,1
        font_size:self.width/2
        background_normal: ''
        background_color:[253/255.0,255/255.0,223/255.0,0.8]
        on_press:app.root.current = 'title'
    Button:
        size_hint:0.1,0.1
        text:'Start'if app.language=='EN' else '开始'
        pos_hint:{'center_x':0.9,'center_y':0.1}
        color:0.5,0.5,0.5,1
        font_size:self.width/2
        background_normal: ''
        background_color:[218/255.0,249/255.0,202/255.0,1]
        on_press:app.root.current = 'game'

<Game>:
    area1:area1
    area2:area2
    area3:area3
    area4:area4
    Area1:
        id:area1
        BoxLayout:
            orientation:'vertical'
            size_hint:None,None
            size:self.parent.size
            Label:
                text:'(*^_^*)'
                color:0.5,0.5,0.5,1
                font_size:self.height/2
            Label:
                text:'time {}'.format(root.time) if app.language=='EN' else '时间 {}'.format(root.time)
                color:0.5,0.5,0.5,1
                font_size:self.height/2
            Label:
                text:'moves {}'.format(root.moves) if app.language=='EN' else '步数 {}'.format(root.moves)
                color:0.5,0.5,0.5,1
                font_size:self.height/2
            BoxLayout:
                MB1:
                    text:'New'if app.language=='EN' else '重玩'
                    color:0.5,0.5,0.5,1
                    font_size:self.height/2
                    background_normal: ''
                    background_color:[253/255.0,255/255.0,223/255.0,0.8]
                MB2:
                    text:'Back'if app.language=='EN' else '返回'
                    color:0.5,0.5,0.5,1
                    font_size:self.height/2
                    background_normal: ''
                    background_color:[218/255.0,249/255.0,202/255.0,1]
    Area2:
        id:area2
    Area3:
        id:area3
    Area4:
        id:area4

<Help>:
    Label:
        pos_hint:{'center_x':0.5,'center_y':0.9}
        text:'Help' if app.language=='EN' else '游戏帮助'
        font_size:Window.height/10
        color:0.5,0.5,0.5,1
    Label:
        size_hint:None,None
        size:Window.width,self.texture_size[1]
        text_size:Window.width*3/4.0, None
        pos_hint:{'center_x':0.5,'center_y':0.5}
        color:0.5,0.5,0.5,1
        font_size:Window.height/25
        text1:'This game is quite similar to The 15-puzzle, which contains 1 empty tile and 15 numbered tiles in random order.Touch the numbered tile next to the empty tile would change the order.When the tile order is from small to large, you win the game.Notice that all tiles are mirror tiles, you should touch these mirror tiles to finish the game.'
        text2:'这个游戏非常类似于“15拼图”，它由1个空块和15个数字块随机组成。触摸挨着空块的数字块改变顺序。当数字块按照从小到大的顺序排列时，你赢得了比赛。注意所有数字块都是镜像，你通过触摸这些镜像来完成游戏。'
        text:self.text1 if app.language=='EN' else self.text2
    Button:
        size_hint:0.1,0.1
        text:'Back'if app.language=='EN' else '返回'
        pos_hint:{'center_x':0.1,'center_y':0.1}
        color:0.5,0.5,0.5,1
        font_size:self.width/2
        background_normal: ''
        background_color:[253/255.0,255/255.0,223/255.0,0.8]
        on_press:app.root.current = 'title'
    Button:
        size_hint:0.1,0.1
        text:'Start'if app.language=='EN' else '开始'
        pos_hint:{'center_x':0.9,'center_y':0.1}
        color:0.5,0.5,0.5,1
        font_size:self.width/2
        background_normal: ''
        background_color:[218/255.0,249/255.0,202/255.0,1]
        on_press:app.root.current = 'game'

<Scenes@ScreenManager>:
    Title:
        name:'title'
    Mode:
        name:'settings'
    Game:
        name:'game'
    Help:
        name:'help'
    Records:
        name:'records'

Scenes:
    current:'title'
    transition:FadeTransition()
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
            for i in self.neighbour_nums:
                if self.parent.parent.situation[i] == 15:
                    self.move(i)

    def move(self, i):
        self.parent.parent.situation[self.npos], self.parent.parent.situation[i] = self.parent.parent.situation[i], self.parent.parent.situation[self.npos]
        self.npos = i
        self.parent.parent.moves += 1

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


class Victory(Popup):
    pass

class MLabel(Label):

    def __init__(self, **args):
        super(MLabel, self).__init__(**args)
        with self.canvas.before:
            PushMatrix()
            self.trans = Translate(xy = (0,0))
            self.mat = MatrixInstruction(matrix = matrix_0)
        with self.canvas.after:
            PopMatrix()
        Clock.schedule_interval(self.update,1/10.0)

    def update(self, *args):
        if 0 < self.opacity < 1:
            if self.direction == '-':
                self.opacity -= 0.1
            elif self.direction == '+':
                self.opacity += 0.1
        elif self.opacity >= 1:
            self.opacity -= 0.1
            self.direction = '-'
        elif self.opacity <= 0:
            self.opacity += 0.1
            self.direction = '+'
            self.mirror_text()

    def mirror_text(self):
        a = Window.width
        if self.trans.xy == (0,0):
            self.mat.matrix = matrix_1
            self.trans.xy = (a, 0)
        else:
            self.trans.xy = (0,0)
            self.mat.matrix = matrix_0


class MB1(Button):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            app = App.get_running_app()
            app.root.current_screen.on_enter()

class MB2(Button):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            app = App.get_running_app()
            app.root.current='title'


class MyScreen(Screen):
    def __init__(self, **args):
        super(MyScreen, self).__init__(**args)
        self.texture = Texture.create(size=(2, 2), colorfmt='rgba')
        p1_color = [239, 206, 232, 255]
        p2_color = [243, 215, 181, 255]
        p3_color = [253, 255, 223, 255]
        p4_color = [218, 249, 202, 255]
        p = p1_color + p2_color + p3_color + p4_color
        buf = bytes(p)
        self.texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        self.texture.wrap = 'mirrored_repeat'
        with self.canvas.before:
            self.rect = Rectangle(pos=self.pos, size=self.size, texture=self.texture)

        self._trig = t = Clock.create_trigger(self._update_rect)
        self.bind(pos=t, size=t)

        Clock.schedule_interval(self._update_texture, 0)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def _update_texture(self, *args):
        a = Clock.get_boottime()*0.1
        self.rect.tex_coords = -sin(a), -cos(a), -(sin(a) + 1), -cos(a), -(sin(a) + 1), -(cos(a) + 1), -sin(a), -(cos(a) + 1)

class Title(MyScreen):
    pass

class Records(MyScreen):
    nt = StringProperty('')
    nm = StringProperty('')
    tt = StringProperty('')
    tm = StringProperty('')
    ht = StringProperty('')
    hm = StringProperty('')

    def on_enter(self, *args):
        with open('record.json', 'r') as f:
            record = json.load(f)
        self.nt = record['normal']['time']
        self.nm = record['normal']['moves']
        self.tt = record['nightmare']['time']
        self.tm = record['nightmare']['moves']
        self.ht = record['hell']['time']
        self.hm = record['hell']['moves']




class Mode(MyScreen):
    pass

class Help(MyScreen):
    pass

class Game(Screen):
    situation = ListProperty([15 for x in range(16)])
    time = NumericProperty(0)
    mode = OptionProperty('normal', options=('normal', 'nightmare','hell'))
    scope = ListProperty([0])
    moves = NumericProperty(0)


    def on_enter(self,*args):
        app = App.get_running_app()
        self.mode = app.mode
        with open('record.json', 'r') as f:
            self.record = json.load(f)
        self.moves = 0
        self.start_new_scope()

        self.start_counting()
        self.start_new_game()

    def start_new_scope(self):
        a = [2,3,4]
        if self.mode == 'normal':
            self.scope = [random.choice(a)]
        elif self.mode == 'nightmare':
            a.remove(random.choice(a))
            self.scope = a
        elif self.mode == 'hell':
            self.scope = a



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
        Victory().open()
        Clock.unschedule(self.update_time)
        if self.record[self.mode]['time'] == '--':
            self.record[self.mode]['time'] = str(self.time)
        elif int(self.record[self.mode]['time']) >self.time:
            self.record[self.mode]['time'] = str(self.time)
        if self.record[self.mode]['moves'] == '--':
            self.record[self.mode]['moves'] = str(self.moves)
        elif int(self.record[self.mode]['moves']) >self.moves:
            self.record[self.mode]['moves'] = str(self.moves)
        with open('record.json', 'w') as f:
            json.dump(self.record, f)

    def start_counting(self):
        Clock.unschedule(self.update_time)
        self.time = 0
        Clock.schedule_interval(self.update_time, 1)

    def start_new_game(self):
        self.area2.clear_widgets()
        self.area3.clear_widgets()
        self.area4.clear_widgets()

        l1 = [i for i in range(15)]
        l2 = self.puzzle_init()
        self.situation = [15 for x in range(16)]
        for i1, i2 in zip(l1, l2):
            self.situation[i2] = i1
            a = random.choice(self.scope)
            if a == 1:
                self.area1.add_widget(NumberBlock(i1, i2))
            elif a == 2:
                self.area2.add_widget(NumberBlock(i1, i2))
            elif a == 3:
                self.area3.add_widget(NumberBlock(i1, i2))
            elif a == 4:
                self.area4.add_widget(NumberBlock(i1, i2))





    def on_situation(self, *args):
        if self.situation == [x for x in range(16)]:
            self.end_game()

    def update_time(self,*args):
        self.time += 1


    def on_touch_down(self, touch):
        if Widget(pos=(0, 0), size=(Window.width / 2, Window.height / 2)).collide_point(*touch.pos):
            touch.pos = (Window.width/2 - touch.pos[0], Window.height/2 - touch.pos[1])
            self.area4.on_touch_down(touch)
        elif Widget(pos=(Window.width / 2, 0), size=(Window.width / 2, Window.height / 2)).collide_point(*touch.pos):
            touch.pos = (touch.pos[0]-Window.width/2,Window.height/2 - touch.pos[1])
            self.area3.on_touch_down(touch)
        elif Widget(pos=(0, Window.height / 2), size=(Window.width / 2, Window.height / 2)).collide_point(*touch.pos):
            touch.pos = (Window.width/2 - touch.pos[0], touch.pos[1]-Window.height/2)
            self.area2.on_touch_down(touch)
        elif Widget(pos=(Window.width / 2, Window.height / 2),
                    size=(Window.width / 2, Window.height / 2)).collide_point(*touch.pos):
            touch.pos = (touch.pos[0] -Window.width/2, touch.pos[1]-Window.height/2)
            self.area1.on_touch_down(touch)





class MyGame(App):
    language = OptionProperty('EN', options=('EN', 'CH'))
    mode = OptionProperty('normal', options=('normal', 'nightmare','hell'))

    def switch_language(self, *args):
        if self.language == 'EN':
            self.language = 'CH'
        elif self.language == 'CH':
            self.language = 'EN'

    def switch_mode(self, *args):
        if self.mode == 'normal':
            self.mode = 'nightmare'
        elif self.mode == 'nightmare':
            self.mode = 'hell'
        elif self.mode == 'hell':
            self.mode = 'normal'

    def build(self):
        return Builder.load_string(KV)


if __name__ == '__main__':
    LabelBase.register('Roboto', 'DroidSansFallback.ttf')
    MyGame().run()
