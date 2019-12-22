import pygame, time, math
import pygame_reference as disp

pygame.init()
clock = pygame.time.Clock()

start_time = time.time()

Imagine = pygame.image.load('C:/Users/Anay Datta/Documents/python files/Imagine_t.png')
Imagine_logo = pygame.image.load('C:/Users/Anay Datta/Documents/python files/Imagine_logo.png')
Imagine = pygame.transform.scale(Imagine, (400, 166))

screen_width = 1000
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Imagine Engine")
pygame.display.set_icon(Imagine_logo)

def reverse(a):
    list = []
    for i in range(0, len(a)):
        list.append(len(a)-i)
    return list

def sin(x):
    return math.sin(x/180*math.pi)

def cos(x):
    return math.cos(x/180*math.pi)

def v_add(v1, v2):
    vo = []
    for i in range(0, len(v1)):
        vo.append(v1[i] + v2[i])
    return vo

def v_scale(v, c):
    vo = []
    for i in range(0, len(v)):
        vo.append(c*v[i])
    return vo

def bias(n1, n2, weight):
    return int(n2+(n1-n2)*weight)

def glow(screen, colour, pos, radius, ratio=2, opacity=128, solid_rad=8):
    if solid_rad < 8:
        solid_rad = 8
    colour_ratio = opacity/255
    try:
        colour2 = screen.get_at(pos)
    except:
        colour2 = screen.get_at((0, 0))
    pygame.draw.ellipse(screen, (colour[0], colour[1], colour[2]), (pos[0]-solid_rad*.5*ratio, pos[1]-.5*solid_rad, ratio*solid_rad, solid_rad), 0)
    for i in range(solid_rad, radius):
        pygame.draw.ellipse(screen, (bias(colour[0], colour2[0], (radius-i)*colour_ratio/radius), bias(colour[1], colour2[1], (radius-i)*colour_ratio/radius), bias(colour[2], colour2[2], (radius-i)*colour_ratio/radius), (radius-i)*colour_ratio/radius), (pos[0]-i*.5*ratio, pos[1]-.5*i, ratio*i, i), 4)

def convert(pt):
    x = pt[0]
    y = pt[1]
    z = pt[2]
    d = z + 10
    a = 90/360*2*math.pi*d
    if a > 0:
        return (int((x*1000/a)+screen_width/2), int((y*1000/-a)+screen_height/2))

def average(list):
    num = 0
    for i in range(0, len(list)):
        num += list[i]
    return num/len(list)

#everything made in this 3D grapher is made by planes
class Plane():
    obj_list = []
    def __init__(self, pos, colour = (255, 255, 255)):
        self.type = type
        self.pos = pos
        self.angle = [0, 0, 0]
        self.merged = [False]
        self.colour = colour
        Plane.obj_list.append(self)
        self.avg_vector = [0, 0, 0]
        self.average = 0
    def rotate(self, axis, degrees, point=None):
        if point == None:
            point = self.avg_vector
            for i in range(1, len(self.merged)):
                point = v_add(point, self.merged[i].avg_vector)
            point = v_scale(point, 1/len(self.merged))
        if axis == "x":
            self.angle[0] += degrees
        if axis == "y":
            self.angle[1] += degrees
        if axis == "z":
            self.angle[2] += degrees
        for i in range(0, len(self.pos)):
            x = self.pos[i][0]-point[0]
            y = self.pos[i][1]-point[1]
            z = self.pos[i][2]-point[2]
            if axis == "x":
                self.pos[i] = [x+point[0], y*cos(degrees)-z*sin(degrees)+point[1], y*sin(degrees)+z*cos(degrees)+point[2]]
            elif axis == "y":
                self.pos[i] = [x*cos(degrees)+z*sin(degrees)+point[0], y+point[1], x*-sin(degrees)+z*cos(degrees)+point[2]]
            elif axis == "z":
                self.pos[i] = [x*cos(degrees) + y*-sin(degrees)+point[0], x*sin(degrees)+y*cos(degrees)+point[1], z+point[2]]
        if self.merged[0]:
            for n in range(1, len(self.merged)):
                 self.merged[n].rotate(axis, degrees, point)
    def translate(self, direction):
        for i in range(0, len(self.pos)):
            self.pos[i][0] += direction[0]
            self.pos[i][1] += direction[1]
            self.pos[i][2] += direction[2]
        if self.merged[0]:
            for n in range(1, len(self.merged)):
                 self.merged[n].translate(direction)
    def delete(self):
        Plane.obj_list.remove(self)
        del self
    def merge(self, list):
        if not self.merged[0]:
            self.merged = [True]
            for i in range(0, len(list)):
                self.merged.append(list[i])
        else:
            for i in range(0, len(list)):
                self.merged.append(list[i])
    @classmethod
    def order(cls):
        for self in Plane.obj_list:
            vector = [0, 0, 0]
            for i in range(0, len(self.pos)):
                vector = v_add(vector, self.pos[i])
            self.avg_vector = v_scale(vector, 1/len(self.pos))
            self.avg = (((self.avg_vector[0])**2)+((self.avg_vector[1])**2)+((self.avg_vector[2]+10)**2)**1/2)
        list = []
        alist = []
        for i in Plane.obj_list:
            list.append(i)
            alist.append(i.avg)
        obj_list = []
        for i in range(0, len(list)):
            obj_list.append(list[alist.index(max(alist))])
            del list[alist.index(max(alist))]
            del alist[alist.index(max(alist))]
        Plane.obj_list = obj_list
    @classmethod
    def blit(cls, screen):
        Plane.order()
        for i in Plane.obj_list:
            list = []
            for j in i.pos:
                list.append(convert(j))
            pygame.draw.polygon(screen, i.colour, list, 0)

screen.blit(Imagine, ((screen_width/2)-33, (screen_height/2)-66))
pygame.draw.rect(screen, (0, 0, 0), [33+(screen_width/2), 0, screen_width, screen_height])
pygame.display.update()
time.sleep(1)

for i in range(0, 200-33, 3):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    screen.blit(Imagine, ((screen_width/2)-33-i, (screen_height/2)-66))
    pygame.draw.rect(screen, (0, 0, 0), [33+(screen_width/2)+i, 0, screen_width, screen_height])
    pygame.display.update()
    time.sleep(1/100)
    screen.fill((0, 0, 0))

for i in range(1, 100, 5):
    glow(screen, (62, 72, 204), (int(screen_width/2), int(screen_height/2)+25), 200, 2, i)
    screen.blit(Imagine, ((screen_width/2)-200, (screen_height/2)-66))
    pygame.display.update()
    time.sleep(1/50)
    screen.fill((0, 0, 0))


for i in range(0, 900, 5):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    glow(screen, (62, 72, 204), (int(screen_width/2), int(screen_height/2)+25), int(30*sin(i))+200, 2, 100)
    screen.blit(Imagine, ((screen_width/2)-200, (screen_height/2)-66))
    pygame.display.update()
    time.sleep(1/100)
    screen.fill((0, 0, 0))

for i in range(1, 100, 5):
    glow(screen, (62, 72, 204), (int(screen_width/2), int(screen_height/2)+25), 200, 2, 100-i)
    screen.blit(Imagine, ((screen_width/2)-200, (screen_height/2)-66))
    pygame.display.update()
    time.sleep(1/50)
    screen.fill((0, 0, 0))

for i in range(0, 200-33, 3):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    screen.blit(Imagine, ((screen_width/2)-200+i, (screen_height/2)-66))
    pygame.draw.rect(screen, (0, 0, 0), [(screen_width/2)+200-i, 0, screen_width, screen_height])
    pygame.display.update()
    time.sleep(1/100)
    screen.fill((0, 0, 0))

time.sleep(1)

points = [[0, 1, 0], [.5, 1, 0], [.5, -1, 0], [0, -1, 0]]
for i in range(-90, 250, 5):
    points.append([9/32*cos(i), 9/32*sin(i)+9/32, 0])
for i in range(90, 260, 5):
    points.append([1/2*cos(350-i), 1/2*sin(350-i)+1/2, 0])

plane1 = Plane(points, (63, 72, 204))

done = False

x, y = 0, 0
clicked = False
n = 1
colour = (0, 162, 232)

for i in range(0, 50):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    Plane.blit(screen)
    time.sleep(1/60)
    pygame.display.update()
    screen.fill((bias(colour[0], 0, i/100), bias(colour[1], 0, i/100), bias(colour[2], 0, i/100)))

plane1.rotate("y", 360)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
            pygame.mouse.get_rel()
        if event.type == pygame.MOUSEBUTTONUP:
            clicked = False
        if clicked:
            x, y = pygame.mouse.get_rel()
    if not 0 < plane1.angle[0] < 1:
        y += plane1.angle[0]/10
    if not 0 < plane1.angle[1] < 1:
        x += plane1.angle[1]/10
    x/=1.05
    y/=1.05
    plane1.rotate("y", -x/5)
    Plane.blit(screen)
    time.sleep(1/100)
    pygame.display.update()
    n+=1
    screen.fill(((sin(1/2*n)+1)*1/2*colour[0], (sin(1/2*n)+1)*1/2*colour[1], (sin(1/2*n)+1)*1/2*colour[2]))
    glow(screen, (255, 255, 0), (0.8*screen_height*sin(90+n/2)+screen_width/2, 0.8*screen_height*cos(90+n/2)+screen_height), 600, 1, 255/2, 50)
    glow(screen, (255, 255, 255), (-600*sin(90+n/2)+screen_width/2, -0.8*screen_height*cos(90+n/2)+screen_height), 300, 1, 255/2, 50)
