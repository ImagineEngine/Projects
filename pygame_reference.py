import pygame, math

print("pygame")

def pyprint(screen, texti, posi = (0, 0), fonti = "freesans", sizei = 20, colouri = (255, 255, 255), center = False):
    font = pygame.font.SysFont(fonti, sizei)
    text = font.render(str(texti), True, colouri)
    if center:
        textRect = text.get_rect()
        textRect.center = (posi)
        screen.blit(text,textRect)
    else:
        screen.blit(text,posi)

def text(texti, fonti = "freesans", sizei = 20, colouri = (255, 255, 255)):
    font = pygame.font.SysFont(fonti, sizei)
    text = font.render(str(texti), True, colouri)
    return text

def mouse_on(pos, size):
    mpos = pygame.mouse.get_pos()
    if mpos[0]>=pos[0] and mpos[0]<=pos[0]+size[0] and mpos[1]>=pos[1] and mpos[1]<=pos[1]+size[1] :
        return True
    else:
        return False

def sin(x):
    return math.sin(x/180*math.pi)

def cos(x):
    return math.cos(x/180*math.pi)

def crop(surf, pt, size):
    crop = pygame.Surface((size[0], size[1]))
    for x in range(0, size[0]):
        for y in range(0, size[1]):
            crop.set_at((x, y), surf.get_at((pt[0]+x, pt[1]+y)))

def Vtransform(pt, axis, deg):
    x = pt[0]
    y = pt[1]
    z = pt[2]
    if axis == "x":
            return (x, y*cos(deg)-z*sin(deg), y*sin(deg)+z*cos(deg))
    elif axis == "y":
            return (x*cos(deg)+z*sin(deg), y, x*-sin(deg)+z*cos(deg))
    elif axis == "z":
            return (x*cos(deg) + y*-sin(deg), x*sin(deg) + y*cos(deg), z)

def td_plot(pt):
    x = pt[0]
    y = pt[1]
    z = pt[2]
    d = z + 5
    a = 144/360*2*math.pi*d
    if a > 0:
        return (int((x*1000/a)+(screen_width/2)), int((y*1000/-a)+(screen_height/2)))

def in_range(pos, size, mpos):
    if mpos[0] > pos[0] and mpos[0] < pos[0] + size[0] and mpos[1] > pos[1] and mpos[1] < pos[1] + size[1]:
        return True
    else:
        return False

def rblit(surf, posi, deg):
        surf = pygame.transform.rotate(surf, deg)
        pos = [posi[0]-(1/2*surf.get_width()), posi[1]-(1/2*surf.get_height())]
        screen.blit(surf, pos)
        pygame.display.update()
        time.sleep(1/1200)

def KeyName():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            return key.name(event.key)

def slider():
    clicked = False
    pos = [10,10]
    i=0
    cclick = False
    done = False
    while not done:
        if i >0:
            pygame.draw.circle(screen, black, pos,10,0)
        pygame.draw.line(screen, white, (10,10), (210,10),5)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] == True:
                    clicked=True
            if event.type == pygame.MOUSEBUTTONUP:
                if pygame.mouse.get_pressed()[0] == False:
                    clicked = False
                    cclick = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    done = True
        if clicked:
            if pygame.mouse.get_pos()[0] > pos[0] - 10 and pygame.mouse.get_pos()[0] < pos[0] + 10 and pygame.mouse.get_pos()[1] > pos[1] - 10 and pygame.mouse.get_pos()[1] < pos[1] + 10:
                cclick = True
        if cclick:
            pos[0] = pygame.mouse.get_pos()[0]
            pos[1] = pygame.mouse.get_pos()[1]
        if pos[0]<10:
            pos[0]=10
        if pos[0]>210:
            pos[0]=210
        pos[1]=10
        pygame.draw.circle(screen, white, pos,10,0)
        pyprint(str(int((pos[0]-10)/2)), "freesans", 20, (0, 150, 255), (pos[0], 30))
        pygame.display.update()
        clock.tick(60)
        i+=1
        screen.fill(black)
    return (pos[0]-10)/2
