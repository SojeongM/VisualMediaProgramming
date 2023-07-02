import pygame
import numpy as np
import os

WINDOW_WIDTH=800
WINDOW_HEIGHT=800

RED=(255, 0, 0)
GRAY=(200, 200, 200)

CannonCenter=[100., 700.]

pygame.init()  # 1! initialize the whole pygame system!
pygame.display.set_caption("문소정 20191585")

screen=pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock=pygame.time.Clock()

current_path = os.path.dirname(__file__)

assets_path = os.path.join(current_path, 'assets')


alien_image = pygame.image.load(os.path.join(assets_path, 'alien.png'))
alien_image = pygame.transform.scale(alien_image, (50, 50))
fire_image = pygame.image.load(os.path.join(assets_path, 'fire.png'))
fire_image = pygame.transform.scale(fire_image, (100, 100))

piano_keysounds=[]
for i in range(1, 14):
    filename= f'piano/FX_piano{i:02}.mp3'
    s=pygame.mixer.Sound(filename)
    piano_keysounds.append(s)

def getRegularPolygonVertices(nv, r):
    v=[]
    for i in range(nv):
        rad=i*2*np.pi/nv
        x=np.cos(rad)*r
        y=np.sin(rad)*r
        v.append([x, y])
    vnp=np.array(v) #conversion
    return vnp


class RegularPolygon():
    def __init__(self, nvertices, radius):
        self.nvertices=nvertices
        self.radius=radius
        self.linewidth=np.random.choice([0, 2, 4])
        self.p=getRegularPolygonVertices(nvertices, radius)
        self.color=GRAY
        
        self.vxy=np.array([0.,0.]) 
        self.txy=np.array([0.,0.]) 
        self.axy=np.array([0.,0.5]) 
        
        self.vdeg=np.random.choice([5, 10, 15, 20]) # degree / frame
        self.deg=0

        self.sound=None
        self.q=None

    def update(self, ):
        self.vxy+=self.axy
        self.txy+=self.vxy

        self.deg+=self.vdeg
        R=Rmat(self.deg)

        qt=R@self.p.T
        q=qt.T

        self.q=q+self.txy

        if self.txy[0] - self.radius < 0:
            self.vxy[0] *= -1
            self.txy[0] = self.radius
        if self.txy[0] + self.radius >= WINDOW_WIDTH:
            self.vxy[0] *= -1
            self.txy[0] = WINDOW_WIDTH - self.radius
        if self.txy[1] + self.radius >= WINDOW_HEIGHT: # object bottom touched the screen height
                self.vxy[1] *= -1  # reverse the moving direction
               # diff=self.txy[1]+self.radius-WINDOW_HEIGHT
                self.txy[1] = WINDOW_HEIGHT - self.radius
             #   if self.sound:
                 #   self.sound.play()
        if self.txy[1]-self.radius<0:
                
                self.vxy[1]*=-1
                
                self.txy[1] = self.radius
    
    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.q, width=self.linewidth)
        pygame.draw.line(screen, (255, 255, 255), self.txy, self.q[0])



        
class Star(RegularPolygon):
    def __init__(self, radius):
        k=np.random.randint(4, 10)
        super().__init__(5, radius)
        self.life_tick=50

    def update(self,):
        self.vxy+=self.axy
        self.txy+=self.vxy
        self.q=self.p+self.txy
        self.life_tick-=1
        if self.life_tick<20:
            self.color=GRAY
    def draw(self, screen):
        for i in range(self.nvertices):
             pygame.draw.line(screen, self.color, self.q[i], self.q[(i+2)%self.nvertices], self.linewidth)



def getRectangle(width, height, x=0, y=0):
    v=np.array([[0      , 0], 
                [width, 0],
                [width, height],
                [0      , height]],
                
                
                dtype="float")
    
    return v

def Rmat(deg):
    theta=np.deg2rad(deg)
    c=np.cos(theta)
    s=np.sin(theta)
    R=np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], dtype="float")
    return R

def Tmat(tx, ty):
    T=np.array([ [1, 0, tx], [0, 1, ty], [0, 0, 1]], dtype="float")
    return T

def draw(M, points, colors, p0=None):
    R=M[0:2, 0:2]
    t=M[0:2, 2]

    point_transformed=( R @ points.T ).T+t
    pygame.draw.polygon(screen, colors, point_transformed, 2)
    if p0 is not None:
        pygame.draw.line(screen, (0, 0, 0), p0, point_transformed[0])


def detect_col(p, x, y):
    s1=p[0][0]-x-20    
    s2=p[0][1]-y-20
    d=np.sqrt(s1**2+s2**2)
    print(s1, s2, x, y)

    if d<50:
        return 1
    else:
        return 0
    
def detect(p, x, y, rad):
    for i in range(1, 9):
        s1=p[i][0]-x-20
        s2=p[i][1]-y-20
        d=np.sqrt(s1**2+s2**2)
        if d<rad[i]+20:
            print(p[i], x, y)
            return 1
        

    return 0

center1=[300, 300.]
width1=200
height1=50
rect1=getRectangle(width1, height1)
angle1=30

gap12=30


width2=280
height2=70
rect2=getRectangle(width2, height2)
def main():
    
    keyboard_x=700.
    keyboard_y=700.

    angle=0
    done=False
    anglese=0
    angleE=0
    angleM=0
    angleEM=0
    angleJ=0
    angleM1=0

    

    col=0
    suncol=0
    col_star=[]


    while not done:
        arm = getRectangle(100, 20)
        
        rad=[]
        planet=[]
        angle+=5.
        anglese+=2.
        angleE+=10.
        angleM+=7.
        angleEM+=10
        angleJ+=15.
        angleM1+=5
        #1. event check
        for event in pygame.event.get(): #1/60 마다 들어온 input buffer에 넣어줌
            if event.type==pygame.QUIT:
                done=True

            elif event.type == pygame.KEYDOWN:
                k=np.random.randint(1, 12)
                piano_keysounds[1].play()
                print(keyboard_x, keyboard_y)
                if event.key==pygame.K_ESCAPE:
                    done=True
                if event.key == pygame.K_LEFT:
                    keyboard_x -= 20
                elif event.key == pygame.K_RIGHT:
                    keyboard_x += 20
                elif event.key == pygame.K_UP:
                    keyboard_y -= 20
                elif event.key == pygame.K_DOWN:
                    keyboard_y += 20
        #2. logic 

        
        


        screen.fill((0, 51, 102))
        distSE=150
        distEM=50

        Sun=getRegularPolygonVertices(20, 40)
        rad.insert(0, 40)
  
        Earth=getRegularPolygonVertices(8, 20)
        rad.insert(1, 20)
        
        Moon=getRegularPolygonVertices(3, 5)
        rad.insert(2, 5)

        Venus=getRegularPolygonVertices(5, 10)
        rad.insert(3, 10)

        Jupter=getRegularPolygonVertices(12, 20)
        rad.insert(4, 20)
        
        newMoon=getRegularPolygonVertices(4, 2)
        rad.insert(5, 5)
        rad.insert(6, 5)
        rad.insert(7, 2)
        rad.insert(8, 2)

        center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
        Msun=Tmat(center[0], center[1]) @Rmat(angle)
        draw(Msun, Sun, (255, 55, 100), center)
        planet.insert(0, center)
        
        Mearth=Tmat(center[0], center[1]) @ Rmat(anglese+30) @ Tmat(distSE, 0) @Rmat(-anglese-30) @Rmat(angleE)
        draw(Mearth, Earth, (0, 255, 100), Mearth[:2, 2])
        planet.insert(1, Mearth[:2, 2])

        Mmoon=Mearth @ Rmat(angleEM) @ Tmat(distEM, 0) @ Rmat(angleM)
        draw(Mmoon, Moon, (255, 204,51), Mmoon[:2, 2])
        planet.insert(2, Mmoon[:2, 2])

        Mvenus=Tmat(center[0], center[1]) @ Rmat(anglese) @ Tmat(100, 0)
        draw(Mvenus, Venus, (255, 255, 102), Mvenus[:2, 2])
        planet.insert(3, Mvenus[:2, 2])

        Mjupeter=Tmat(center[0], center[1]) @ Rmat(anglese) @ Tmat(300, 0) @Rmat(-anglese) @Rmat(angleJ)
        draw(Mjupeter, Jupter, (153, 102, 0), Mjupeter[:2, 2])
        planet.insert(4, Mjupeter[:2, 2])

        Mmoon1=Mjupeter @ Rmat(angleEM) @ Tmat(40, 0) @ Rmat(angleM1)
        draw(Mmoon1, Moon, (204, 255,0), Mmoon1[:2, 2])
        planet.insert(5, Mmoon1[:2, 2])

        Mmoon2=Mjupeter @ Rmat(angleM1) @ Tmat(80, 0) @ Rmat(angleM)
        draw(Mmoon2, Moon, (102, 155,153), Mmoon2[:2, 2])
        planet.insert(6, Mmoon2[:2, 2])

        Mnewmoon1=Mmoon1@ Rmat(angleEM) @ Tmat(15, 0) @ Rmat(angleM1)
        draw(Mnewmoon1, newMoon, (255, 255,200), Mnewmoon1[:2, 2])
        planet.insert(7, Mnewmoon1[:2, 2])

        Mnewmoon2=Mmoon2@ Rmat(angle) @ Tmat(15, 0) @ Rmat(angle)
        draw(Mnewmoon2, newMoon, (255, 255,153), Mnewmoon2[:2, 2])
        planet.insert(7, Mnewmoon2[:2, 2])


        suncol=detect_col(planet, keyboard_x, keyboard_y)
        col=detect(planet, keyboard_x, keyboard_y, rad)
        
        if col==1:
            for i in range(8):
                s=Star(2)
                s.color=np.random.randint(0, 256, size=(3))
                s.linewidth=5
                alien_c=np.array([keyboard_x, keyboard_y])
                s.txy=alien_c+10
                s.vxy=np.zeros(shape=(2))
                s.vxy=np.random.uniform(5, 11)
                       
                angle=i*360./8.
                vxy_rad=np.deg2rad(angle)
                vxy_mag=30
                s.vxy=np.array([np.cos(vxy_rad), np.sin(vxy_rad)])*vxy_mag
                s.q=s.p+s.txy
                        
                col_star.append(s)

        for p in col_star:
            p.update() 
         
        if suncol==0:
            screen.blit(alien_image, [keyboard_x, keyboard_y])   
        elif suncol==1:
            filename= f'snd/폭발1.wav'
            s=pygame.mixer.Sound(filename)
            s.play()
            screen.blit(fire_image, [keyboard_x, keyboard_y]) 
        for p in col_star:
            p.draw(screen) 
        
        
        pygame.display.flip()
        clock.tick(20)
    
    pass



if __name__=="__main__":
    main()