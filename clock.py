import pygame
import numpy as np
import math
import time

WINDOW_WIDTH=800
WINDOW_HEIGHT=800

RED=(255, 0, 0)
GRAY=(200, 200, 200)

CannonCenter=[100., 700.]

pygame.init() 
pygame.display.set_caption("문소정 20191585")

screen=pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock=pygame.time.Clock()

piano_keysounds=[]
for i in range(1, 14):
    filename= f'3_Pygame/piano/FX_piano{i:02}.mp3'
   # print(filename)
    s=pygame.mixer.Sound(filename)
    piano_keysounds.append(s)




def getRectangle(width, height, x=0, y=0):
    v=np.array([[x      , y], 
                [x+width, y],
                [x+width, y+height],
                [x      , y+height]],
                
                dtype="float")
    
    return v

def Rmat(deg):
    theta=np.deg2rad(deg)
    c=np.cos(theta)
    s=np.sin(theta)

    R=np.array([[c, -s], [s, c]])
    return R

def main():
    done=False
    pRect=getRectangle(200, 5, 200, 398.5) #4x2 matrix
    rcenter=np.array([(200/2.+300.), (5/2.+398.5)])
    pRect1=getRectangle(100, 5,300, 398.5)
    pRect2=getRectangle(50, 5, 400, 398.5)
    colors=(0, 0, 0)
    #gmt 시간 가져오기
    gmtime=time.gmtime()
    #초침 각도 계산하기 (시작 각도가 -90도인 점을 고려)
    deg=gmtime.tm_sec*6+90.
    #분침 각도 계산하기 (시작 각도가 -90도인 점을 고려)
    deg1=gmtime.tm_min*6-270.
    
    #kst로 시각 변경하기
    if gmtime.tm_hour+9>23:
        kst=gmtime.tm_hour+9-12  
    else:
        kst=gmtime.tm_hour+9

    #kst에 맞는 시침 각도 계산하기 (시작 각도가 -90도인 점을 고려)
    if (kst)>12:
        deg2=(kst-12)*30.+gmtime.tm_min*0.5-90
    else:
        deg2=(kst)*30.+gmtime.tm_min*0.6/60.-90
    

   

    while not done:
        
        #1. event check
        for event in pygame.event.get(): #1/60 마다 들어온 input buffer에 넣어줌
            if event.type==pygame.QUIT:
                done=True
            elif event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    done=True

        #2. logic 
        #초, 분, 시침 각도 계산
        deg+=6
        deg1+=0.1
        deg2+=0.5/60

        deg1=round(deg1, 2)

        #정각에 초침, 분침, 시침이 올 때마다 0으로 초기화
        if deg==360:
            deg=0
        if deg1>=360:
            deg1=0
        if deg2>360:
            deg2=0

        #초침
        R=Rmat(deg)
        q1=pRect-rcenter 
        q2t = R@q1.T
        q2=q2t.T
        q3=q2+rcenter
        #분침
        R1=Rmat(deg1)
        q11=pRect1-rcenter 
        q22t = R1@q11.T
        q22=q22t.T
        q33=q22+rcenter     
        #시침
        R2=Rmat(deg2)
        q111=pRect2-rcenter 
        q222t = R2@q111.T
        q222=q222t.T
        q333=q222+rcenter

        screen.fill((204, 255, 255))

        pygame.draw.polygon(screen, (51, 204, 255), q3)
        pygame.draw.polygon(screen, (51, 153, 204), q33)
        pygame.draw.polygon(screen, (00, 102, 153), q333)
        pygame.draw.circle(screen, (0, 0, 0), rcenter, 3)
        pygame.draw.circle(screen, colors, rcenter, 300, 2)

        if deg1==90:
            k=np.random.randint(1, 12)
            piano_keysounds[k].play()
            colors=np.random.randint(0, 256, size=(3))
        
        #4
        pygame.display.flip()
        clock.tick(600)
    
    pass



if __name__=="__main__":
    main()