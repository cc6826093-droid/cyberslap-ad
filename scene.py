import bpy,math,os
from mathutils import Vector
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
s=bpy.context.scene;s.render.engine='BLENDER_EEVEE';s.render.resolution_x=int(os.getenv('WIDTH',360));s.render.resolution_y=int(os.getenv('HEIGHT',640));s.render.resolution_percentage=100;s.render.fps=24;s.frame_start=1;s.frame_end=240;s.render.image_settings.file_format='PNG';s.render.filepath='/tmp/cyberslap_frames/frame_'
def mat(n,c):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=.88;return m
cream=mat('warm ivory',(.82,.78,.69));coral=mat('matte coral',(.83,.29,.32));pink=mat('rose',(.95,.65,.62));sage=mat('sage',(.43,.66,.58));dark=mat('ink',(.16,.21,.23))
def ball(n,pos,scale,m):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=20,location=pos);o=bpy.context.object;o.name=n;o.scale=scale;o.data.materials.append(m);bpy.ops.object.shade_smooth();return o
def key(o,f,p,sc=None):
 o.location=p;o.keyframe_insert(data_path='location',frame=f)
 if sc:o.scale=sc;o.keyframe_insert(data_path='scale',frame=f)
floor=ball('soft floor',(0,0,-1.5),(12,12,.25),cream)
for i in range(7):ball('background pebble',(i-3,2,-.9),(.25,.25,.25),sage if i%2 else pink)
hero=ball('squishy stress ball',(0,0,0),(1,1,1),coral)
for x in (-.23,.23):
 e=ball('eye',(x,-.9,.2),(.075,.04,.09),dark);e.parent=hero;e.matrix_parent_inverse=hero.matrix_world.inverted()
finger=ball('gentle press',(0,-.2,3.5),(.3,.3,.65),pink)
for f,z in [(1,3.5),(70,3.5),(88,.95),(108,3.5),(128,.95),(151,3.5),(240,3.5)]:key(finger,f,(0,-.2,z))
for f,z,sc in [(1,0,(.8,.8,.8)),(70,0,(1,1,1)),(89,-.3,(1.2,1.2,.65)),(104,.24,(.88,.88,1.2)),(116,0,(1,1,1)),(129,-.3,(1.22,1.22,.63)),(146,.27,(.88,.88,1.24)),(168,0,(1,1,1)),(210,.1,(.65,.65,.65)),(240,.1,(.65,.65,.65))]:key(hero,f,(0,0,z),sc)
for i in range(12):
 a=i*math.tau/12;p=ball('relief particle',(0,0,0),(.055,.055,.055),sage if i%2 else pink)
 for f,r,z,sc in [(1,0,0,(0,0,0)),(125,0,0,(0,0,0)),(150,1.5,1.3,(1,1,1)),(195,2,2,(0,0,0))]:key(p,f,(math.cos(a)*r,math.sin(a)*.3*r,math.sin(a)*z),sc)
def text(n,body,z,size):
 c=bpy.data.curves.new(n,'FONT');c.body=body;c.align_x='CENTER';c.size=size;o=bpy.data.objects.new(n,c);s.collection.objects.link(o);o.data.materials.append(dark)
 key(o,1,(0,-.8,6));key(o,195,(0,-.8,6));key(o,220,(0,-.8,z))
text('brand','CyberSlap',1.8,.55);text('tagline','TAP THE STRESS AWAY',1.35,.17)
bpy.ops.object.camera_add(location=(0,-10,2));cam=bpy.context.object;cam.rotation_euler=(Vector((0,0,.1))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';s.camera=cam
for f,scale in [(1,6.8),(70,5.8),(140,5.3),(195,6.6),(240,6.6)]:cam.data.ortho_scale=scale;cam.data.keyframe_insert(data_path='ortho_scale',frame=f)
for pos,power in [((2,-4,6),850),((-4,-2,3),500),((0,3,5),650)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.data.energy=power;o.data.size=5
bpy.ops.render.render(animation=True)
