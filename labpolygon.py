#Gabriel Quiroz
#19255
#20/08/2021
#Graficas
import struct


def char(c):
    #1 byte (char)
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    #2 bytes (short)
    return struct.pack('=h', w)

def dword(d):
    #4 bytes (long)
    return struct.pack('=l', d)

def color(r, g, b):
    # Acepta valores de 0 a 1
    return bytes([ int(b * 255), int(g* 255), int(r* 255)])


color1 = color(0,0,0)
color2 = color(1,1,1)

#Funciones implementadas
class Renderer(object):
    #Glinit
    def __init__(self, width, height):
        self.punto_color = color2
        self.bitmap_color = color1
        self.glCreateWindow(width, height)
    #GlCreateWindow
    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.glClear()
        self.glViewport(0,0, width, height)
    #GlViewPort
    def glViewport(self, x, y, width, height):
        self.vpX = int(x)
        self.vpY = int(y)
        self.vpWidth = int(width)
        self.vpHeight = int(height)

    #glClearColor
    def glClearColor(self, r, g, b):
        self.bitmap_color = color(r, g, b)
    #glClear
    def glClear(self):
        self.pixels = [[ self.bitmap_color for y in range(self.height)]
                       for x in range(self.width)]
    
    def glPoint(self, x, y, color = None):
        if x < self.vpX or x >= self.vpX + self.vpWidth or y < self.vpY or y >= self.vpY + self.vpHeight:
            return

        if (0 <= x < self.width) and (0 <= y < self.height):
            self.pixels[int(x)][int(y)] = color or self.punto_color

    def glColor(self, r, g, b):
        self.punto_color = color(r,g,b)
    
    def line(self, x0, y0, x1, y1):
      dy = abs(y1 - y0)
      dx = abs(x1 - x0)

      steep = dy > dx

      if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

      offset = 0 * 2 * dx
      threshold = 0.5 * 2 * dx
      y = y0

      # y = mx + b
      points = []
      for x in range(x0, x1):
        if steep:
          points.append((y, x, self.punto_color))
        else:
          points.append((x, y, self.punto_color))

        offset += (dy/dx) * 2 * dx
        if offset >= threshold:
          y += 1 if y0 < y1 else -1
          threshold += 1 * 2 * dx

      for point in points:
          r.glPoint(*point)
          
    #glVertex
    def glVertex(self, x, y, color = None):
        x = int( (x + 1) * (self.vpWidth / 2) + self.vpX )
        y = int( (y + 1) * (self.vpHeight / 2) + self.vpY)


        if x < self.vpX or x >= self.vpX + self.vpWidth or y < self.vpY or y >= self.vpY + self.vpHeight:
            return

        if (0 <= x < self.width) and (0 <= y < self.height):
            self.pixels[int(x)][int(y)] = color or self.punto_color
            
    #glFinish
    def glFinish(self, filename):
        with open(filename, "wb") as file:
            # Header
            file.write(bytes('B'.encode('ascii')))
            file.write(bytes('M'.encode('ascii')))
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(14 + 40))

            # InfoHeader
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            # Bitmap
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])
                    
    def glLine(self, v0x, v0y, v1x, v1y, color = None):

        x0 = int( (v0x + 1) * (self.vpWidth / 2) + self.vpX)
        x1 = int( (v1x + 1) * (self.vpWidth / 2) + self.vpX)
        y0 = int( (v0y + 1) * (self.vpHeight / 2) + self.vpY)
        y1 = int( (v1y + 1) * (self.vpHeight / 2) + self.vpY)

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0
        limit = 0.5
        m = dy/dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                self.glPoint(y, x, self.punto_color)
            else:
                self.glPoint(x, y, self.punto_color)

            offset += m
            if offset >= limit:
                y += 1 if y0 < y1 else -1
                limit += 1
                
                
            
    def poligono(self, vertices):
        puntosx=[]
        puntosy=[]

        for i in vertices:
          puntosx.append(i[0])
          puntosy.append(i[1])

        Xmax = max(puntosx)
        Xmin = min(puntosx)
        Ymax = max(puntosy)
        Ymin = min(puntosy) 
        length=len(puntosx)


        for y in range(Ymin, Ymax):
          for x in range(Xmin, Xmax):
            num = len(vertices)
            j = num - 1
            pixel = 0
            for i in range(num):
              x0=vertices[j][0]
              y0=vertices[j][1]
              x1=vertices[i][0]
              y1=vertices[i][1]

              between = ((x1 > x) != (x0 > x))
              if  between:
                coordY = (y0 - y1) * (x - x1) / (x0 - x1) + y1
                if y < coordY:
                  pixel +=1
              j = i
            if (pixel%2) == 1:
              self.glPoint(x,y)
                 
                          
r = Renderer(1024, 768)
r.glClearColor(0,0,0)
r.glClear()
r.glColor(0,0,1)
r.poligono([(165,380),(185,360),(180,330),(207,345),(233,330),(230,360),(250,380),(220,385),(205,410),(193,383)]) 
r.poligono([(321, 335), (288, 286), (339, 251), (374, 302)])
r.poligono([(377, 249), (411, 197), (436, 249)])
r.poligono([(413, 177), (448, 159), (502, 88), (553, 53), (535, 36), (676, 37), (660, 52),(750, 145), (761, 179), (672, 192), (659, 214), (615, 214), (632, 230),
            (580, 230),(597, 215), (552, 214), (517, 144), (466, 180)])
r.poligono([(682, 175), (708, 120), (735, 148), (739, 170),])
r.glFinish('gabriel.bmp')
print("Se ha creado el archivo 'gabriel.bmp'")