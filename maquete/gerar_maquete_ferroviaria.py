"""Maquete didática 3D: sistema ferroviário de cargas e distribuição logística.
Gera modelo GLB, OBJ, HTML offline e prévia PNG. Sem bibliotecas JS externas.
"""
import os, math, json, base64, random
from collections import defaultdict
import numpy as np
import trimesh

OUT='/mnt/data'
random.seed(19)
# All dimensions are illustrative model units, not an engineering scale.
meshes=defaultdict(lambda:{'vertices':[],'faces':[],'colors':[]})
# Save high-level 3d primitive triangles for browser with triangle shading; include per-triangle color.
triangles=[]

C={
 'base':'#25344B','top':'#839A91','asphalt':'#394756','lane':'#F6CB4F','white':'#EAF1F7',
 'rail':'#BBC9D5','ballast':'#63737E','tie':'#795C45','concrete':'#B2BCC2',
 'blue':'#1E78C5','navy':'#153E66','cyan':'#20ABCE','sky':'#90D8EB',
 'orange':'#E99B3E','rust':'#C6683F','teal':'#159A91','red':'#D95C56',
 'yellow':'#F3C84C','dark':'#263847','window':'#A6DFEF','green':'#4B9571',
 'grass':'#61946E','roof':'#638AA2','steel':'#BBCBD4','silver':'#D3DDE2'
}
def rgb(s):
 s=C.get(s,s).lstrip('#');return [int(s[i:i+2],16) for i in (0,2,4)]

def push(g, v, f, color):
 b=meshes[g]; first=len(b['vertices']);b['vertices'].extend(v); b['faces'].extend([[a+first,c+first,d+first] for a,c,d in f]); b['colors'].extend([rgb(color)+[255]]*len(v))
 color3=rgb(color)
 for a,c,d in f:
  triangles.append((v[a],v[c],v[d],color3, 1 if g=='train' else 0))

def box(g, p, s, c, angle=0):
 x,y,z=p; dx,dy,dz=[q/2 for q in s]
 v=[[-dx,-dy,-dz],[dx,-dy,-dz],[dx,dy,-dz],[-dx,dy,-dz],[-dx,-dy,dz],[dx,-dy,dz],[dx,dy,dz],[-dx,dy,dz]]
 ca,sa=math.cos(angle),math.sin(angle)
 v=[[round(x+a*ca-b*sa,3),round(y+a*sa+b*ca,3),round(z+q,3)] for a,b,q in v]
 f=[[4,5,6],[4,6,7],[2,1,0],[3,2,0],[0,1,5],[0,5,4],[2,3,7],[2,7,6],[1,2,6],[1,6,5],[3,0,4],[3,4,7]]
 push(g,v,f,c)

def cyl(g, p, r, h, c, axis='z', n=12, rtop=None):
 rtop = r if rtop is None else rtop
 x,y,z=p;v=[]
 for q,rad in [(-h/2,r),(h/2,rtop)]:
  for j in range(n):
   t=2*math.pi*j/n;a=rad*math.cos(t);b=rad*math.sin(t)
   if axis=='z':pos=[x+a,y+b,z+q]
   elif axis=='y': pos=[x+a,y+q,z+b]
   else:pos=[x+q,y+a,z+b]
   v.append([round(u,3) for u in pos])
 # orientation may differ for x/y; use outward normals correction via checking normals later
 f=[]
 for j in range(n):
  k=(j+1)%n
  if axis=='y':
   f.extend([[j,n+k,n+j],[j,k,n+k]])
  else:
   f.extend([[j,k,n+k],[j,n+k,n+j]])
 for j in range(1,n-1):
  f.append([0,j+1,j] if axis!='y' else [0,j,j+1])
  f.append([n,n+j,n+j+1] if axis!='y' else [n,n+j+1,n+j])
 push(g,v,f,c)

def beam(g,a,b,w,h,c):
 # rods positioned horizontally with arbitrary XY direction; z can slope
 ax,ay,az=a; bx,by,bz=b
 length=math.hypot(bx-ax,by-ay)
 if length<=0.001: box(g,((ax+bx)/2,(ay+by)/2,(az+bz)/2),(w,w,abs(bz-az)+0.1),c);return
 angle=math.atan2(by-ay,bx-ax)
 if abs(bz-az)<.1:box(g,((ax+bx)/2,(ay+by)/2,(az+bz)/2),(length,w,h),c,angle)
 else:
  # approximate sloped rods as small segments
  n=max(2,int(abs(bz-az)*1.8))
  for i in range(n):
   t=(i+.5)/n; cx=ax+(bx-ax)*t;cy=ay+(by-ay)*t;cz=az+(bz-az)*t
   box(g,(cx,cy,cz),(length/n+0.1,w,h),c,angle)

def building(g,x,y,w,d,h,body,roof='roof'):
 box(g,(x,y,1.45+h/2),(w,d,h),body)
 box(g,(x,y,1.45+h+0.5),(w+1.7,d+1.7,1),roof)

def wheel(g,x,y,z,r=.99):
 cyl(g,(x,y,z),r,.65,'dark',axis='y',n=12)
 cyl(g,(x,y+(-0.37 if y<0 else .37),z),r*.43,.12,'steel',axis='y',n=12)

# Foundation, landscape, curbs
box('base',(0,0,-.75),(154,102,1.5),'base')
box('terrain',(0,0,.2),(151,99,.48),'top')
# planted green regions
for (x,y,w,d) in [(-57,34,33,27),(65,34,17,27),(-49,0,39,15),(64,-38,18,19),(-61,-39,22,15)]:
 box('terrain',(x,y,.52),(w,d,.25),'grass')
# road system: east-west service road and vertical route to local delivery destinations
box('roads',(0,11,.72),(146,12,.24),'asphalt')
box('roads',(51,28,.73),(11.5,34,.25),'asphalt')
box('roads',(42,-3,.72),(11,23,.25),'asphalt')
# dashed service roads center line and crossing markings
for x in range(-69,71,9):
 box('roads',(x,11,.89),(4,0.34,.035),'lane')
for y in range(15,43,6):
 box('roads',(51,y,.9),(.35,2.7,.035),'lane')
for y in [-13.3,-10.1,-6.9]:
 box('roads',(42,y,.91),(8,.4,.035),'white')
# pedestrian/loading zones around warehouse
box('terminal',(-2,20,0.67),(60,6,.30),'concrete')
box('terminal',(-9,-5,.66),(51,13,.26),'concrete')
box('terminal',(32,-5,.66),(20,13,.26),'concrete')
# tracks: main and siding with junctions

def ty(x,track):
 if track=='main':return -22.5
 # industrial siding connects to main at two points
 if x<-56 or x>55:return -22.5
 if x<-37:
  t=(x+56)/19; t=max(0,min(1,t));return -22.5-12*(t*t*(3-2*t))
 if x>31:
  t=(x-31)/24;t=max(0,min(1,t));return -34.5+12*(t*t*(3-2*t))
 return -34.5

def tracks(track):
 pts=[]
 for x in np.linspace(-74,74,102 if track=='main' else 108):pts.append((float(x),ty(float(x),track)))
 # ballast around trajectory segmented, plank supports rails
 for i in range(len(pts)-1):
  a=pts[i];b=pts[i+1]
  beam('rails',(a[0],a[1],.88),(b[0],b[1],.88),8.0,.48,'ballast')
  for offset in [-2.25,2.25]:
   beam('rails',(a[0],a[1]+offset,1.49),(b[0],b[1]+offset,1.49),.37,.38,'rail')
 for x in np.linspace(-73,73,58 if track=='main' else 57):
  y=ty(x,track)
  nexty=ty(min(x+.6,74),track)
  theta=math.atan2(nexty-y,.6)
  box('rails',(float(x),float(y),1.17),(1.0,8.5,.43),'tie',theta)
tracks('main');tracks('siding')
# Freight locomotive and flatcars: modern diesel-electric (didactic proportions)
T_Y=-22.5

def bogie(x,y):
 box('train',(x,y,2.5),(5.0,5.5,.65),'dark')
 for xx in [x-1.65,x+1.65]:
  for yy in [y-2.5,y+2.5]:wheel('train',xx,yy,2.2,1.05)

def coupler(x,y):box('train',(x,y,3.28),(2.35,.75,.46),'dark')

def car(x,col):
 y=T_Y
 box('train',(x,y,3.75),(16.5,6.6,1.18),'navy')
 box('train',(x,y,4.5),(15.7,6,.46),'steel')
 bogie(x-5.7,y); bogie(x+5.7,y)
 box('train',(x,y,7.45),(15.3,5.65,5.6),col)
 # container vertical corrugation and corner castings
 for xx in np.arange(x-6.7,x+7.0,1.7):
  for yy in [y-2.85,y+2.85]:
   box('train',(float(xx),yy,7.35),(.24,.16,4.85),'silver')
 for ex in [-7.05,7.05]:
  for ey in [-2.75,2.75]:box('train',(x+ex,y+ey,7.6),(.3,.4,5.55),'navy')
 coupler(x+9.0,y);coupler(x-9,y)

# 3 cars + locomotive, enough for whole display
for x,col in [(-35,'orange'),(-17.5,'teal'),(0,'cyan')]:car(x,col)
# locomotive at x 22
x=22;y=T_Y
box('train',(x,y,3.8),(18.6,7.1,1.9),'navy')
bogie(x-5.6,y);bogie(x+5.9,y)
box('train',(x-2.5,y,6.5),(12.0,6.0,4.0),'blue')
box('train',(x+6.1,y,8.0),(5.5,6.7,7.2),'yellow')
box('train',(x+6.1,y,11.9),(6.2,6.9,.72),'navy')
for yy in [y-3.39,y+3.39]:
 box('train',(x+6.4,yy,9.6),(3.7,.13,2.6),'window')
 box('train',(x-2.0,yy,6.4),(10.6,.11,1.25),'sky')
 for xx in [x-7,x-5.1,x-3.2,x-1.3]:
  box('train',(xx,yy,8),(.45,.24,2.2),'navy')
box('train',(x+9.32,y,6.5),(.24,5.7,2.9),'navy')
for yy in [y-2,y+2]:cyl('train',(x+9.49,yy,6.4),.65,.12,'white',axis='x')
box('train',(x+9.0,y,3.5),(1.7,7.3,.7),'yellow')
box('train',(x-5.0,y,9.05),(1.6,1.5,1.8),'dark')
box('train',(x-5.0,y,10.1),(2.4,2.0,.35),'silver')
for xx in [x-8,x-5.5,x-3.0]:box('train',(xx,y,8.45),(.8,2.5,.22),'dark')
coupler(x-10,y)

# Gantry crane over siding at x=-8; portal beams spanning terminal apron and siding
cr=-8
for xx in [cr-9.4,cr+9.4]:
 for yy in [-40,-2]:
  box('crane',(xx,yy,9.2),(1.7,1.75,17.0),'yellow')
  box('crane',(xx,yy,1.5),(3.3,3.3,1.0),'navy')
 for zz in [13.2,18.2]:
  beam('crane',(xx,-41,zz),(xx,-1,zz),.98,1.2,'yellow')
 for yy in [-40,-2]:
  for dz in [7.5,11.0,14.5]:
   beam('crane',(xx,yy,dz),(xx,yy+(5.5 if yy<0 else -5.5),dz+3.8),.6,.7,'yellow')
for yy in [-40,-2]:
 beam('crane',(cr-10.8,yy,19.0),(cr+10.8,yy,19.0),1.3,2,'yellow')
box('crane',(cr,-21,19.4),(6.0,5.2,2.0),'navy')
box('crane',(cr,-21,17.7),(3.3,3,.85),'dark')
for xx in [cr-1.9,cr+1.9]:
 for yy in [-22.6,-19.4]:
  box('crane',(xx,yy,14.1),(.23,.27,7.0),'steel')
# lifted container above siding, suspended
box('crane',(cr,-21,9.4),(13.5,5.3,4.7),'rust')
for xx in np.arange(cr-5.6,cr+5.8,1.6):
 for yy in [-23.74,-18.26]:box('crane',(float(xx),yy,9.4),(.17,.16,4),'silver')
# Containers in the terminal apron, stacked at different heights
for x,y,col,n in [(-30,-5,'teal',2),(-30,2,'rust',1),(-9,1,'orange',2),(13,-5,'cyan',2),(13,2,'blue',1),(33,-5,'orange',1)]:
 for k in range(n):
  zz=3.2 + k*5.4
  box('terminal',(x,y,zz),(14,5.4,4.9),col)
  for xx in np.arange(x-5.8,x+6.0,1.55):
   for yy in [y-2.8,y+2.8]: box('terminal',(float(xx),yy,zz),(.17,.14,4.25),'silver')
# big warehouse + receiving docks
building('facilities',-3,32,56,22,11,'white','roof')
box('facilities',(-3,32,12.65),(58,23,.35),'navy')
# front (south y=21) loading dock doors
for xx in [-24,-12,0,12,24]:
 box('facilities',(xx,20.83,6.9),(7.3,.2,8.25),'navy')
 for z in np.linspace(3.4,10.3,6):
  box('facilities',(xx,20.67,float(z)),(7.15,.11,.12),'steel')
 box('facilities',(xx,18.7,1.4),(8.5,4.3,.6),'concrete')
# roof skylight stripes
for xx in [-20,-5,10]:box('facilities',(xx,32,13.06),(3.0,18,.15),'window')
# Control building / dispatch near tracks
building('facilities',40,-4,11,12,13,'white','navy')
for z in [6,10]:
 for yy in [-7.5,-4,-.5]:box('facilities',(45.59,yy,z),(.1,2.25,1.8),'window')
box('facilities',(40,-4,15),(12,13,.32),'yellow')
# industrial grain silos on left, feed warehouse
for sx in [-64,-55,-46]:
 cyl('facilities',(sx,32,10.2),3.2,17.5,'silver',n=18)
 cyl('facilities',(sx,32,20.2),3.45,3.5,'roof',n=18,rtop=.3)
 for zz in [5.3,10.0,14.7]:
  cyl('facilities',(sx,32,zz),3.28,.25,'navy',n=18)
# silo feeder shed
building('facilities',-54,20,27,8,6.0,'concrete','blue')
# delivery hub buildings on upper-right
building('facilities',65,32,15.5,18,8.5,'white','cyan')
for xx in [60,65,70]:
 box('facilities',(xx,22.94,4.9),(3,.13,4.4),'navy')
# parked trucks on y=11, use both orientation variants

def truck(x,y,angle=0,color='rust',length=13):
 # truck long axis x, optionally rotate 90 around z
 def b(px,py,z,sx,sy,sz,c):
  ca,sa=math.cos(angle),math.sin(angle)
  bx=x+px*ca-py*sa; by=y+px*sa+py*ca
  box('vehicles',(bx,by,z),(sx,sy,sz),c,angle)
 b(-2.6,0,2.75,8.7,4.2,3.8,color)
 b(4.2,0,2.7,4.5,4.1,3.9,'blue')
 b(4.3,0,4.0,3.0,4.25,1.3,'window')
 b(-2.1,0,.98,12.0,3.8,.65,'dark')
 for dx in [-5.3,2,5.2]:
  for dy in [-2.05,2.05]:
   tx=x+dx*math.cos(angle)-dy*math.sin(angle)
   ty=y+dx*math.sin(angle)+dy*math.cos(angle)
   if abs(angle)<.1:wheel('vehicles',tx,ty,1.05,.95)
   else:cyl('vehicles',(tx,ty,1.05),.90,.5,'dark',axis='x',n=12)
 # bumper
 b(6.6,0,1.55,.65,4.1,.45,'silver')

truck(30,10.8,0,'orange')
truck(58,16,math.pi/2,'teal')
# small delivery van next to depot
box('vehicles',(65,7.6,2.1),(9.1,4.0,3.1),'white')
box('vehicles',(67.7,7.6,4.2),(3.6,3.9,1.1),'cyan')
for xx in [62,68]:
 for yy in [5.6,9.6]:wheel('vehicles',xx,yy,1,.8)
# forklift near terminal containers
box('vehicles',(30,-2.0,1.35),(4.7,3.1,1.5),'yellow')
box('vehicles',(30,-2.0,2.8),(3.3,2.8,1.7),'dark')
box('vehicles',(28.45,-2.0,3.65),(.25,2.9,3.4),'dark')
box('vehicles',(26.4,-2.0,1.75),(3.0,2.8,.3),'silver')
for xx in [28.3,31.6]:
 for yy in [-3.5,-.5]:wheel('vehicles',xx,yy,1.0,.6)
# overhead signal poles, signs with rail signal lights
for sx,sy in [(-53,-16),(48,-16),(-49,-28),(37,-28)]:
 box('signals',(sx,sy,6),(0.55,.6,10),'steel')
 box('signals',(sx,sy,10.6),(2.15,.7,3.65),'dark')
 for zz,cc in [(11.65,'red'),(10.65,'yellow'),(9.65,'green')]:
  cyl('signals',(sx,sy-.47,zz),.31,.13,cc,axis='y',n=12)
# safety barriers at rail road crossing (x=42)
for sy in [-17.8,-28.2]:
 box('signals',(41.5,sy,3.9),(.43,.45,5.8),'silver')
 beam('signals',(41.5,sy,5.7),(47.9,sy,5.7),.5,.6,'red')
 box('signals',(40.8,sy,7.3),(1.4,.25,1.0),'white')
# pylon lighting
for lx,ly in [(-35,-2),(21,-9),(32,21),(61,40),(-65,-6)]:
 box('signals',(lx,ly,6.9),(.35,.35,12.2),'steel')
 box('signals',(lx,ly,13.1),(3.2,1.8,.42),'silver')
 for xx in [lx-1,lx+1]:box('signals',(xx,ly-0.3,12.65),(.8,1.1,.2),'yellow')
# compact pine/spherical trees around border (stylized)
for tx,ty in [(-69,-42),(-63,-44),(-68,45),(-38,44),(38,43),(72,44),(70,-43),(-15,45),(-34,0),(71,-3)]:
 cyl('nature',(tx,ty,2.8),.65,4.1,'tie',n=8)
 for z,r in [(5,2.6),(7.4,2.0)]:cyl('nature',(tx,ty,z),r,3.2,'green',n=10,rtop=r*.3)
# bollards and painted logistics zones
for x in [-28,-15,-2,11,24]:
 box('terminal',(x,15.1,1.3),(.7,.75,1.7),'yellow')
for x in range(-31,29,5):
 box('terminal',(x,-11.5,.84),(2.2,.26,.1),'white')

# export colored GLB + colored OBJ with vertex colors
print('Geometry triangles',len(triangles),'groups',list(meshes))
scene=trimesh.Scene()
for g,b in meshes.items():
 mesh=trimesh.Trimesh(vertices=np.array(b['vertices'],dtype=float),faces=np.array(b['faces'],dtype=int),process=False)
 mesh.visual.vertex_colors=np.array(b['colors'],dtype=np.uint8)
 scene.add_geometry(mesh, geom_name=g,node_name=g)
print('Exporting GLB ...')
with open(f'{OUT}/maquete_sistema_ferroviario.glb','wb') as f:f.write(scene.export(file_type='glb'))
print('Exporting OBJ ...')
# For a single colored mesh use vertex colors in OBJ non-standard, but Blender supports. Other software may show grey.
combined=trimesh.util.concatenate([v for v in scene.geometry.values()])
with open(f'{OUT}/maquete_sistema_ferroviario.obj','w') as f:f.write(trimesh.exchange.obj.export_obj(combined,include_color=True))
# HTML data: packed triangles -> bytes msgpack? simple json compact coordinate float
# pack each face as 9 coordinates and hex RGB string, group int. round values to 2 dp
compact=[]
for a,b,c,col,g in triangles:
 compact.append([*[round(float(v),2) for vec in (a,b,c) for v in vec], *col, g])
with open(f'{OUT}/maquete_geometry.json','w') as f:json.dump(compact,f,separators=(',',':'))
print('Geometry JSON MB',round(os.path.getsize(f'{OUT}/maquete_geometry.json')/1024**2,2))
