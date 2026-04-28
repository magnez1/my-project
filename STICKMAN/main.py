from tkinter import*
import random
import time
class Game:
    def __init__(self):
        self.tk=Tk()
        self.tk.title('Человечек спешит к выходу')
        self.tk.resizable(False,False)
        self.tk.wm_attributes('-topmost',1)
        self.canvas=Canvas(self.tk,height=500,width=500,highlightthickness=0)
        self.canvas.pack()
        self.tk.update()
        self.canvas_height=500
        self.canvas_width=500
        self.bg=PhotoImage(file='background.gif')
        w=self.bg.width()
        h=self.bg.height()
        for x in range(0,5):
            for y in range(0,5):
                self.canvas.create_image(x*w,y*h,image=self.bg,anchor='nw')
        self.sprites=[]
        self.running=True
    def mainloop(self):
        while True:
            if self.running==True:
                for sprite in self.sprites:
                    sprite.move()
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.01)

class Coords:
    def __init__(self,x1=0,y1=0,x2=0,y2=0):
        self.x1=x1
        self.y1=y1
        self.x2=x2
        self.y2=y2
def within_x(self,co1,co2):
    if (co1.x1>co2.x1 and co1.x1<co2.x2)\
            or (co1.x2>co2.x1 and co1.x2<co2.x2)\
            or (co2.x1>co1.x1 and co2.x1<co1.x2)\
            or (co2.x2>co1.x1 and co2.x2<co1.x2):
        return True
    else:
        return False
def within_y(self,co1,co2):
        if (co1.y1>co2.y1 and co1.y1<co2.y2)\
                or (co1.y2>co2.y1 and co1.y2<co2.y2)\
                or (co2.y1>co1.y1 and co2.y1<co1.y2)\
                or (co2.y2>co1.y1 and co2.y2<co1.y2):
            return True
        else:
            return False
def collided_left(self,co1,co2):
    if within_y(self,co1,co2):
        if co1.x1<=co2.x2 and co1.x1>=co2.x1:
            return True
    return False
def collided_right(self,co1,co2):
    if within_y(self,co1,co2):
        if co1.x2>=co2.x1 and co1.x2<=co2.x2:
            return True
    return False
def collided_top(self,co1,co2):
    if within_x(self,co1,co2):
        if co1.y1<=co2.y2 and co1.y1>=co2.y1:
            return True
    return False
def collided_bottom(self,y,co1,co2):
    if within_x(self,co1,co2 ):
        y_calc=co1.y2+y
        if y_calc>=co2.y1 and y_calc<=co2.y2:
            return True
    return False
class Sprite:
    def __init__(self,game):
        self.game=game
        self.finish_door=False
        self.coordinates=None
    def move(self):
        pass
    def coords(self):
        return self.coordinates
class PlatformSprite(Sprite):
    def __init__(self,game,photo_image,x,y,width,height):
        Sprite.__init__(self,game)
        self.photo_image=photo_image
        self.image=game.canvas.create_image(x,y,image=self.photo_image,anchor='nw')
        self.coordinates=Coords(x,y,x+width,y+height)
class MovingPlatformSprite(Sprite):
    def __init__(self,game,photo_image,x,y,width,height):
        Sprite.__init__(self,game)
        self.height=height
        self.width=width
        self.photo_image=photo_image
        self.image=game.canvas.create_image(x,y,image=self.photo_image,anchor='nw')
        self.coordinates=Coords(x,y,x+self.width,y+self.height)
    def coords(self):
        xy=self.game.canvas.coords(self.image)
        self.coordinates.x1=xy[0]
        self.coordinates.y1=xy[1]
        self.coordinates.x2=xy[0]+self.width
        self.coordinates.y2=xy[1]+self.height
        return self.coordinates
    def move(self):
        self.y_move=0
        if self.coordinates.x1<=0:
            self.x_move=2
        elif self.coordinates.x2>=500:
            self.x_move=-2
        self.coordinates=self.coords()
        self.game.canvas.move(self.image,self.x_move,self.y_move)
#НАСТРОЙКА ДВИЖЕНИЯ В ПРАВО/ЛЕВО
class StickFigureSprite(Sprite):
    def __init__(self,game):
        Sprite.__init__(self,game)
        self.images_left=[PhotoImage(file='figure-L1.gif'),
                          PhotoImage(file='figure-L2.gif'),
                          PhotoImage(file='figure-L3.gif')]
        self.images_right=[PhotoImage(file='figure-R1.gif'),
                           PhotoImage(file='figure-R2.gif'),
                           PhotoImage(file='figure-R3.gif')]
        self.image=game.canvas.create_image(20,400,image=self.images_left[0],anchor='nw')
        self.x=-2
        self.y=0
        self.current_image=0
        self.current_image_add=1
        self.jump_count=0
        self.last_time=time.time()
        self.coordinates=Coords()
        game.canvas.bind_all('<KeyPress-Left>',self.turn_left)
        game.canvas.bind_all('<KeyPress-Right>',self.turn_right)
        game.canvas.bind_all('<space>',self.jump)
    def turn_left(self,evt):
        self.y=0
        self.x=-2
    def turn_right(self,evt):
        self.y=0
        self.x=2
    def jump(self,evt):
        if self.y==0:
            self.y=-4
            self.jump_count=0
#АНИМАЦИЯ ДВИЖЕНИЯ В ПРАВО/ЛЕВО
    def animate(self):
        if self.x!=0 and self.y==0:
            if time.time() - self.last_time>0.1:
                self.last_time=time.time ()
                self.current_image+=self.current_image_add
                if self.current_image>=2:
                    self.current_image_add=-1
                if self.current_image<=0:
                    self.current_image_add=1
        if self.x<0:
            if self.y!=0:
                self.game.canvas.itemconfig(self.image,image=self.images_left[2])
            else:
                self.game.canvas.itemconfig(self.image,image=self.images_left[self.current_image])
        elif self.x>0:
            if self.y!=0:
                self.game.canvas.itemconfig(self.image,image=self.images_right[2])
            else:
                self.game.canvas.itemconfig(self.image,image=self.images_right[self.current_image])
    def coords(self):
        xy=self.game.canvas.coords(self.image)
        self.coordinates.x1=xy[0]
        self.coordinates.y1=xy[1]
        self.coordinates.x2=xy[0]+27
        self.coordinates.y2=xy[1]+30
        return self.coordinates
    def move(self):
        self.animate()
        if self.y<0:
            self.jump_count+=1
            if self.jump_count>20:
                self.y=4
        if self.y>0:
            self.jump_count-=1
        co=self.coords()
        left=True
        right=True
        top=True
        bottom=True
        falling=True
        if self.y>0 and co.y2>=self.game.canvas_height:
            self.y=0
            bottom=False
            self.game.running=False
            self.game.canvas.create_text(250,230,text='Вы Проиграли :(',justify='center',fill='red',font='Arial 40')
            self.game.canvas.itemconfig(self.image,image='')
        elif self.y<0 and co.y1<=0:
            self.y=0
            top=False
        if self.x>0 and co.x2>=self.game.canvas_width:
            self.x=0
            right=False
        elif self.x<0 and co.x1<=0:
            self.x=0
            left=False
        for sprite in self.game.sprites:
            if sprite==self:
                continue
            sprite_co=sprite.coords()
            if top and self.y<0 and collided_top(self,co,sprite_co):
                self.y=-self.y
                top=False
            if bottom and self.y>0 and collided_bottom(self,self.y,co,sprite_co):
                self.y=sprite_co.y1-co.y2
                if self.y<0:
                    self.y=0
                bottom=False
                top=False
            if bottom and falling and self.y==0 and co.y2< self.game.canvas_height and collided_bottom(self,1,co,sprite_co):
                falling=False
            if left and self.x<0 and collided_left(self,co,sprite_co):
                self.x=0
                left=False
                if sprite.finish_door:
                    self.game.running=False
                    self.game.canvas.create_text(250,230,text='Вы Победили!!!',fill='green',justify='center',font='Arial 40')
                    door.animate()
                    self.game.canvas.itemconfig(self.image, image='')
            if right and self.x>0 and collided_right(self,co,sprite_co):
                self.x=0
                right=False
                if sprite.finish_door:
                    self.game.running=False
                    self.game.canvas.create_text(250,230,text='Вы Победили!!!',fill='green',justify='center',font='Arial 40')
                    door.animate()
                    self.game.canvas.itemconfig(self.image, image='')
        if falling and bottom and self.y==0 and co.y2<self.game.canvas_height:
            self.y=4
        self.game.canvas.move(self.image,self.x,self.y)
class DoorSprite(Sprite):
    def __init__(self,game,photo_image1,photo_image2,x,y,width,height):
        Sprite.__init__(self,game)
        self.photo_image1=photo_image1
        self.photo_image2=photo_image2
        self.image=game.canvas.create_image(x,y,image=self.photo_image1,anchor='nw')
        self.coordinates=Coords(x,y,x+(width/2),y+height)
        self.finish_door=True
    def animate(self):
        if self.finish_door:
            self.game.canvas.itemconfig(self.image,image=self.photo_image2)
g=Game()
platform1=PlatformSprite(g,PhotoImage(file='platform1.gif'),0,480,100,10)
platform2=MovingPlatformSprite(g,PhotoImage(file='platform1.gif'),500,440,100,10)
platform3=PlatformSprite(g,PhotoImage(file='platform1.gif'),300,400,100,10)
platform4=PlatformSprite(g,PhotoImage(file='platform1.gif'),300,160,100,10)
platform5=MovingPlatformSprite(g,PhotoImage(file='platform2 (1).gif'),0,350,66,10)
platform6=PlatformSprite(g,PhotoImage(file='platform2 (1).gif'),50,300,66,10)
platform7=MovingPlatformSprite(g,PhotoImage(file='platform2 (1).gif'),500,120,66,10)
platform8=PlatformSprite(g,PhotoImage(file='platform2 (1).gif'),45,60,66,10)
platform9=PlatformSprite(g,PhotoImage(file='platform3 (1).gif'),170,250,32,10)
platform10=PlatformSprite(g,PhotoImage(file='platform3 (1).gif'),230,200,32,10)
g.sprites.append(platform1)
g.sprites.append(platform2)
g.sprites.append(platform3)
g.sprites.append(platform4)
g.sprites.append(platform5)
g.sprites.append(platform6)
g.sprites.append(platform7)
g.sprites.append(platform8)
g.sprites.append(platform9)
g.sprites.append(platform10)
door=DoorSprite(g,PhotoImage(file='door1.gif'),PhotoImage(file='door2.gif'),45,30,40,35)
g.sprites.append(door)
sf=StickFigureSprite(g)
g.sprites.append(sf)
g.mainloop()