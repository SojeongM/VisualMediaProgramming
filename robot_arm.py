import pygame
import numpy as np

WINDOW_WIDTH=800
WINDOW_HEIGHT=800

RED=(255, 0, 0)
GRAY=(200, 200, 200)

CannonCenter=[100., 700.]

pygame.init()  # 1! initialize the whole pygame system!
pygame.display.set_caption("문소정 20191585")

screen=pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock=pygame.time.Clock()

piano_keysounds=[]
for i in range(1, 14):
    filename= f'3_Pygame/piano/FX_piano{i:02}.mp3'
    print(filename)
    s=pygame.mixer.Sound(filename)
    piano_keysounds.append(s)

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

def draw(M, points, colors):
    R=M[0:2, 0:2]
    t=M[0:2, 2]

    point_transformed=( R @ points.T ).T+t
    pygame.draw.polygon(screen, colors, point_transformed, 2)


center1=[100, 300.]
width1=200
height1=50
rect1=getRectangle(width1, height1)
angle1=30

gap12=30


width2=280
height2=70
rect2=getRectangle(width2, height2)

width3=80
height3=30

rect3=getRectangle(width3, height3)

width4=30
height4=100
rect4=getRectangle(width4, height4)

width5=60
height5=20
rect5=getRectangle(width5, height5)
def main():
    angle1=30
    angle2=0
    angle3=0
    angle4=0
    angle5=0
    done=False
    while not done:
        
        arm = getRectangle(100, 20)
        
        #1. event check
        for event in pygame.event.get(): #1/60 마다 들어온 input buffer에 넣어줌
            if event.type==pygame.QUIT:
                done=True

            elif event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    done=True
                elif event.key==pygame.K_a:
                    angle1-=5
                    
                elif event.key==pygame.K_b:
                    angle1+=5
                elif event.key==pygame.K_c:
                    angle2+=5
                elif event.key==pygame.K_d:
                    angle2-=5
                elif event.key==pygame.K_e:
                    angle3+=5
                elif event.key==pygame.K_f:
                    angle3-=5
                elif event.key==pygame.K_SPACE:
                    angle4+=5
                    angle5-=5
                elif event.key==pygame.K_q:
                    angle5+=5
                    angle4-=5
        #2. logic 

        
                
    
        screen.fill( (51, 51, 51))

        M = np.eye(3) @ Tmat(center1[0], center1[1]) @ Rmat(angle1) @ Tmat(0, -height1/2.)
        draw(M, rect1, (0, 153, 51))
        pygame.draw.circle(screen,  (255, 255, 204), center1, 3)

        M2 = M @ Tmat(width1, 0) @ Tmat(0, height1/2.) @ Rmat(angle2) @ Tmat(0, -height2/2.) 
        draw(M2, rect2, (51, 153, 0))
        M3 = M2 @ Tmat(width2, 0) @ Tmat(0, height2/2.) @ Rmat(angle3) @ Tmat(0, -height3/2.)
        draw(M3, rect3, (153, 204, 0))
        M4 = M3 @ Tmat(width3, 0) @ Tmat(0, height3/2.) @ Rmat(angle3) @ Tmat(0, -height4/2.)
        draw(M4, rect4, (204, 255, 51))
        M5 = M4 @ Tmat(width4, 0) @ Tmat(0, height5/2) @ Rmat(angle4)@ Tmat(0, -height5/2)
        draw(M5, rect5, (153, 200, 153))
        M6 = M4 @ Tmat(width4, 0) @ Tmat(0, height5/2)@ Tmat(0, height4)@ Tmat(0, -height5) @ Rmat(angle5)@ Tmat(0, -height5/2)
        draw(M6, rect5, (153, 200, 153))
        
        c=M @ Tmat(width1, 0) @ Tmat(0, height1/2.)
        center2=c[0:2, 2]
        pygame.draw.circle(screen, (255, 255, 204), center2, 3)
        c2=M2 @ Tmat(width2, 0) @ Tmat(0, height2/2.)@ Rmat(angle2)
        center3=c2[0:2, 2]
        pygame.draw.circle(screen, (255, 255, 204), center3, 3)
        c3=M3 @ Tmat(width3, 0) @ Tmat(0, height3/2.)@ Rmat(angle3)
        center4=c3[0:2, 2]
        pygame.draw.circle(screen, (255, 255, 204), center4, 3)
        c4=M5  @ Tmat(0, height5/2.)@ Rmat(angle4)
        center4=c4[0:2, 2]
        pygame.draw.circle(screen, (204, 244, 204), center4, 3)
        c4=M6  @ Tmat(0, height5/2.)@ Rmat(angle4)
        center4=c4[0:2, 2]
        pygame.draw.circle(screen, (204, 255, 205), center4, 3)

        pygame.display.flip()
        clock.tick(20)
    
    pass



if __name__=="__main__":
    main()