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

def getRegularPolygonVertices(nv, r):
    v=[]
    for i in range(nv):
        rad=i*2*np.pi/nv
        x=np.cos(rad)*r
        y=np.sin(rad)*r
        v.append([x, y])
    vnp=np.array(v) #conversion
    return vnp


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

  #  R=np.array([[c, -s], [s, c]])
    R=np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], dtype="float")
    return R

def Tmat(tx, ty):
    T=np.array([ [1, 0, tx], [0, 1, ty], [0, 0, 1]], dtype="float")
    return T

def draw(M, points, colors):
    R=M[0:2, 0:2]
    t=M[0:2, 2]

    point_transformed=( R @ points.T ).T+t
    pygame.draw.polygon(screen, colors, point_transformed, 3)


center1=[400, 150.]
width1=20
height1=20
rect1=getRectangle(width1, height1)
angle1=30

gap12=30


width2=200
height2=100
rect2=getRectangle(width2, height2)

width3=80
height3=30

rect3=getRectangle(width3, height3)

width4=30
height4=120
rect4=getRectangle(width4, height4)

width5=160
height5=30
rect5=getRectangle(width5, height5)

width6=140
height6=20
rect6=getRectangle(width6, height6)

width7=100
height7=15
rect7=getRectangle(width7, height7)
def main():
    angle_neck=90
    angle_body=0
    angle_arm1=0
    angle_arm2=0
    angle_arm3=0
    angle_arm4=0
    angle_leg1=0
    angle_leg2=0
    angle_leg3=0
    angle_leg4=0
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
                elif event.key==pygame.K_LEFT: #neck
                    angle_neck-=5
                    
                elif event.key==pygame.K_RIGHT:
                    angle_neck+=5
                elif event.key==pygame.K_a:
                    angle_body+=10
                elif event.key==pygame.K_s:
                    angle_body-=10
                elif event.key==pygame.K_d:
                    angle_arm1+=5
                    angle_arm2-=5
                elif event.key==pygame.K_f:
                    angle_arm1-=5
                    angle_arm2+=5
                elif event.key==pygame.K_1:
                    angle_arm3-=5
                elif event.key==pygame.K_2:
                    angle_arm3+=5
                elif event.key==pygame.K_3:
                    angle_arm4-=5
                elif event.key==pygame.K_4:
                    angle_arm4+=5
                elif event.key==pygame.K_q:
                    angle_leg1+=5
                    
                elif event.key==pygame.K_w:
                    angle_leg1-=5
                  
                elif event.key==pygame.K_e:
                    angle_leg2+=5
                elif event.key==pygame.K_r:
                    angle_leg2-=5
                elif event.key==pygame.K_5:
                    angle_leg3-=5
                elif event.key==pygame.K_6:
                    angle_leg3+=5
                elif event.key==pygame.K_7:
                    angle_leg4-=5
                elif event.key==pygame.K_8:
                    angle_leg4+=5
            
        #2. logic 

        
                
    
        screen.fill( (51, 51, 51))
        pygame.draw.circle(screen,  (255, 229, 204), (center1[0], center1[1]-50), 50, 3)
        #neck
        M = np.eye(3) @ Tmat(center1[0], center1[1]) @ Rmat(angle_neck) @ Tmat(0, -height1/2.)
        draw(M, rect1, (255, 229, 204))
        pygame.draw.circle(screen,  (255, 255, 204), center1, 3)
        #body
        M2 = M @ Tmat(width1, 0) @ Tmat(0, height1/2.) @ Rmat(angle_body) @ Tmat(0, -height2/2.)
        draw(M2, rect2, (153, 153, 255))
        #pelvis
        M4 = M2 @ Tmat(width2, 0) @ Tmat(0, height2/2.) @ Rmat(angle_body) @ Tmat(0, -height4/2.)
        draw(M4, rect4, (204, 255, 51))
        #leg1
        M5 = M4 @ Tmat(width4, 0) @ Tmat(0, height4/2.)  @ Tmat(0, -height4/2.) @ Tmat(0, height5/2) @ Rmat(angle_body)@ Tmat(0, -height5/2)  @ Rmat(angle_leg1)
        draw(M5, rect5, (102, 178, 255))
        #leg2
        M6 = M4 @ Tmat(width4, 0) @ Tmat(0, height4/2.)  @ Tmat(0, -height4/2.) @ Tmat(0, height5/2)@ Tmat(0, height4)@ Tmat(0, -height5) @ Rmat(angle_leg2)@ Tmat(0, -height5/2)
        draw(M6, rect5, (102, 178, 255))
        #leg3
        M7 = M5 @ Tmat(width5, 0) @ Tmat(0, height5/2.) @ Rmat(angle_leg1) @ Tmat(0, -height6/2.)@ Rmat(angle_leg3)
        draw(M7, rect6, (255, 229, 204))
        #leg4
        M8 = M6 @ Tmat(width5, 0) @ Tmat(0, height5/2.) @ Rmat(angle_leg2) @ Tmat(0, -height6/2.)@ Rmat(angle_leg4)
        draw(M8, rect6, (255, 229, 204))

        #arm1
        M9=M2@ Tmat(0, height2/2.)  @ Tmat(0, -height2/2.) @ Rmat(angle_body)@ Tmat(0, -height6)@ Rmat(angle_arm1)
        draw(M9, rect6, (153, 153, 255))
        #arm2
        M10 = M2 @ Tmat(0, height2/2.)  @ Tmat(0, -height2/2.) @ Tmat(0, height6)@ Tmat(0, height2)@ Tmat(0, -height6) @ Rmat(angle_arm2)
        draw(M10, rect6, (153, 153, 255))
        #arm3
        M11 = M9 @ Tmat(width6, 0) @ Tmat(0, height6/2.) @ Rmat(angle_arm1) @ Tmat(0, -height7/2.) @ Rmat(angle_arm3)
        draw(M11, rect7, (255, 229, 204))
        #arm4
        M12 = M10 @ Tmat(width6, 0) @ Tmat(0, height6/2.) @ Rmat(angle_arm2) @ Tmat(0, -height7/2.) @ Rmat(angle_arm4)
        draw(M12, rect7, (255, 229, 204))
        
        pygame.display.flip()
        clock.tick(20)
    
    pass



if __name__=="__main__":
    main()