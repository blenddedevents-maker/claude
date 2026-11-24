"""Escena Blender: semáforo en primer plano con flash duro (estilo foto nocturna).
Uso: python3 semaforo_3d.py <salida.png> <ancho> <alto> <samples>
"""
import sys, math, bpy, bmesh
from mathutils import Vector

out = sys.argv[1] if len(sys.argv) > 1 else "render.png"
W = int(sys.argv[2]) if len(sys.argv) > 2 else 1080
H = int(sys.argv[3]) if len(sys.argv) > 3 else 1350
SAMPLES = int(sys.argv[4]) if len(sys.argv) > 4 else 64

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

# ---------------------------------------------------------------- materiales
def node_mat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    o = nt.nodes.new("ShaderNodeOutputMaterial")
    return m, nt, o

def scratched(name, base, rough_lo, rough_hi, metallic, scale=6.0, brushed=(60, 1, 1.5), scr_scale=7):
    """Metal/pintura con cepillado, rayones finos y manchas procedurales."""
    m, nt, o = node_mat(name)
    N, L = nt.nodes, nt.links
    bsdf = N.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Metallic"].default_value = metallic
    tc = N.new("ShaderNodeTexCoord")
    # cepillado: ruido muy estirado
    mb = N.new("ShaderNodeMapping"); mb.inputs["Scale"].default_value = brushed
    L.new(tc.outputs["Object"], mb.inputs["Vector"])
    nb = N.new("ShaderNodeTexNoise"); nb.inputs["Scale"].default_value = 4; nb.inputs["Detail"].default_value = 8
    L.new(mb.outputs["Vector"], nb.inputs["Vector"])
    # rayones finos: bordes de voronoi estirados en dos direcciones
    def scr(rot, sc):
        mp = N.new("ShaderNodeMapping"); mp.inputs["Rotation"].default_value = rot
        mp.inputs["Scale"].default_value = (1, 1, .3)
        L.new(tc.outputs["Object"], mp.inputs["Vector"])
        vo = N.new("ShaderNodeTexVoronoi"); vo.feature = "DISTANCE_TO_EDGE"; vo.inputs["Scale"].default_value = sc
        L.new(mp.outputs["Vector"], vo.inputs["Vector"])
        cr = N.new("ShaderNodeValToRGB")
        cr.color_ramp.elements[0].position = 0.0; cr.color_ramp.elements[0].color = (1, 1, 1, 1)
        cr.color_ramp.elements[1].position = 0.007; cr.color_ramp.elements[1].color = (0, 0, 0, 1)
        L.new(vo.outputs["Distance"], cr.inputs["Fac"])
        return cr
    s1 = scr((0.4, 0.9, 0.3), scr_scale); s2 = scr((1.1, -0.5, 2.2), scr_scale * 1.7)
    # máscara para que los rayones no estén en todas partes
    nm = N.new("ShaderNodeTexNoise"); nm.inputs["Scale"].default_value = 2.5
    L.new(tc.outputs["Object"], nm.inputs["Vector"])
    nmr = N.new("ShaderNodeValToRGB")
    nmr.color_ramp.elements[0].position = 0.5; nmr.color_ramp.elements[1].position = 0.62
    L.new(nm.outputs["Fac"], nmr.inputs["Fac"])
    sadd = N.new("ShaderNodeMath"); sadd.operation = "MAXIMUM"
    L.new(s1.outputs["Color"], sadd.inputs[0]); L.new(s2.outputs["Color"], sadd.inputs[1])
    smul = N.new("ShaderNodeMath"); smul.operation = "MULTIPLY"
    L.new(sadd.outputs[0], smul.inputs[0]); L.new(nmr.outputs["Color"], smul.inputs[1])
    # manchas / huellas
    nz = N.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = scale
    nz.inputs["Detail"].default_value = 10; nz.inputs["Roughness"].default_value = .65
    L.new(tc.outputs["Object"], nz.inputs["Vector"])
    nr = N.new("ShaderNodeValToRGB")
    nr.color_ramp.elements[0].position = 0.35; nr.color_ramp.elements[1].position = 0.75
    L.new(nz.outputs["Fac"], nr.inputs["Fac"])
    mx = N.new("ShaderNodeMix"); mx.data_type = "FLOAT"
    mx.inputs[2].default_value = rough_lo; mx.inputs[3].default_value = rough_hi
    L.new(nr.outputs["Color"], mx.inputs[0])
    br = N.new("ShaderNodeMath"); br.operation = "MULTIPLY_ADD"
    br.inputs[1].default_value = .12; br.inputs[2].default_value = -.06
    L.new(nb.outputs["Fac"], br.inputs[0])
    r1 = N.new("ShaderNodeMath"); r1.operation = "ADD"
    L.new(mx.outputs[0], r1.inputs[0]); L.new(br.outputs[0], r1.inputs[1])
    r2 = N.new("ShaderNodeMath"); r2.operation = "MULTIPLY_ADD"; r2.inputs[1].default_value = .25
    L.new(smul.outputs[0], r2.inputs[0]); L.new(r1.outputs[0], r2.inputs[2])
    clamp = N.new("ShaderNodeClamp"); clamp.inputs["Min"].default_value = .04
    L.new(r2.outputs[0], clamp.inputs["Value"])
    L.new(clamp.outputs[0], bsdf.inputs["Roughness"])
    cmix = N.new("ShaderNodeMix"); cmix.data_type = "RGBA"
    cmix.inputs[6].default_value = (*base, 1)
    cmix.inputs[7].default_value = (min(base[0]*2.5+.12,1), min(base[1]*2.5+.12,1), min(base[2]*2.5+.12,1), 1)
    sdim = N.new("ShaderNodeMath"); sdim.operation = "MULTIPLY"; sdim.inputs[1].default_value = .1
    L.new(smul.outputs[0], sdim.inputs[0]); L.new(sdim.outputs[0], cmix.inputs[0])
    L.new(cmix.outputs[2], bsdf.inputs["Base Color"])
    bump = N.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = .15
    bump.inputs["Distance"].default_value = .001
    hadd = N.new("ShaderNodeMath"); hadd.operation = "MULTIPLY_ADD"; hadd.inputs[1].default_value = .3
    L.new(nb.outputs["Fac"], hadd.inputs[0]); L.new(smul.outputs[0], hadd.inputs[2])
    L.new(hadd.outputs[0], bump.inputs["Height"])
    L.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    L.new(bsdf.outputs["BSDF"], o.inputs["Surface"])
    return m

def lens_mat(name, col, power):
    """Lente de policarbonato con anillos fresnel y emisión."""
    m, nt, o = node_mat(name)
    N, L = nt.nodes, nt.links
    tc = N.new("ShaderNodeTexCoord")
    # anillos concéntricos (fresnel) usando distancia radial en coords de objeto
    sep = N.new("ShaderNodeSeparateXYZ"); L.new(tc.outputs["Object"], sep.inputs["Vector"])
    comb = N.new("ShaderNodeCombineXYZ")
    L.new(sep.outputs["X"], comb.inputs["X"]); L.new(sep.outputs["Z"], comb.inputs["Y"])
    ln = N.new("ShaderNodeVectorMath"); ln.operation = "LENGTH"
    L.new(comb.outputs["Vector"], ln.inputs[0])
    mul = N.new("ShaderNodeMath"); mul.operation = "MULTIPLY"; mul.inputs[1].default_value = 150
    L.new(ln.outputs["Value"], mul.inputs[0])
    sn = N.new("ShaderNodeMath"); sn.operation = "SINE"; L.new(mul.outputs[0], sn.inputs[0])
    # caída radial: centro más caliente
    fall = N.new("ShaderNodeMapRange")
    fall.inputs["From Min"].default_value = 0.0; fall.inputs["From Max"].default_value = 0.11
    fall.inputs["To Min"].default_value = 1.0; fall.inputs["To Max"].default_value = 0.25
    L.new(ln.outputs["Value"], fall.inputs["Value"])
    # rejilla de micro-prismas
    vor = N.new("ShaderNodeTexVoronoi"); vor.inputs["Scale"].default_value = 260
    L.new(tc.outputs["Object"], vor.inputs["Vector"])
    hot = N.new("ShaderNodeMix"); hot.data_type = "RGBA"
    hot.inputs[6].default_value = (*col, 1)
    hot.inputs[7].default_value = (1, min(col[1]*1.4+.45, 1), min(col[2]*1.4+.35, 1), 1)
    pw = N.new("ShaderNodeMath"); pw.operation = "POWER"; pw.inputs[1].default_value = 3
    L.new(fall.outputs["Result"], pw.inputs[0]); L.new(pw.outputs[0], hot.inputs[0])
    em = N.new("ShaderNodeEmission")
    L.new(hot.outputs[2], em.inputs["Color"])
    st = N.new("ShaderNodeMath"); st.operation = "MULTIPLY"; st.inputs[1].default_value = power
    L.new(fall.outputs["Result"], st.inputs[0])
    st2 = N.new("ShaderNodeMath"); st2.operation = "MULTIPLY_ADD"
    st2.inputs[1].default_value = .18; st2.inputs[2].default_value = .9
    L.new(sn.outputs[0], st2.inputs[0])
    st3 = N.new("ShaderNodeMath"); st3.operation = "MULTIPLY"
    L.new(st.outputs[0], st3.inputs[0]); L.new(st2.outputs[0], st3.inputs[1])
    L.new(st3.outputs[0], em.inputs["Strength"])
    # capa brillante encima (reflejos del flash)
    gl = N.new("ShaderNodeBsdfPrincipled")
    gl.inputs["Base Color"].default_value = (*col, 1)
    gl.inputs["Roughness"].default_value = .12
    gl.inputs["Coat Weight"].default_value = 1.0
    bump = N.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = .35
    L.new(sn.outputs[0], bump.inputs["Height"])
    L.new(bump.outputs["Normal"], gl.inputs["Normal"])
    b2 = N.new("ShaderNodeBump"); b2.inputs["Strength"].default_value = .15
    L.new(vor.outputs["Distance"], b2.inputs["Height"]); L.new(bump.outputs["Normal"], b2.inputs["Normal"])
    L.new(b2.outputs["Normal"], gl.inputs["Normal"])
    ad = N.new("ShaderNodeAddShader")
    L.new(em.outputs[0], ad.inputs[0]); L.new(gl.outputs[0], ad.inputs[1])
    L.new(ad.outputs[0], o.inputs["Surface"])
    return m

M_HOUSE = scratched("carcasa", (0.010, 0.011, 0.012), .25, .5, .2, scale=4, brushed=(2, 2, 2), scr_scale=5)
M_VISOR = scratched("visera", (0.03, 0.03, 0.033), .12, .3, .3, scale=5, brushed=(2, 2, 2), scr_scale=6)
M_WALL = scratched("pared", (0.16, 0.17, 0.19), .3, .6, 1.0, scale=1.2, brushed=(90, 1, 1.2), scr_scale=5)
M_POLE = scratched("poste", (0.25, 0.26, 0.28), .2, .5, 1.0, scale=8, brushed=(1, 1, 60))

# ---------------------------------------------------------------- geometría
def add_bevel(ob, w, seg=6):
    md = ob.modifiers.new("bev", "BEVEL"); md.width = w; md.segments = seg
    md.limit_method = "ANGLE"

# carcasa (eje Y = hacia cámara negativa)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
house = bpy.context.object; house.scale = (0.40, 0.26, 1.18)
bpy.ops.object.transform_apply(scale=True)
add_bevel(house, .045, 8)
house.data.materials.append(M_HOUSE)
bpy.ops.object.shade_smooth()

LIGHTS = [(+0.385, (1.0, 0.02, 0.03), 6), (0.0, (1.0, 0.30, 0.0), 4.5), (-0.385, (0.0, 1.0, 0.12), 4.5)]
R = 0.135
for i, (z, col, pw) in enumerate(LIGHTS):
    # aro portalente
    bpy.ops.mesh.primitive_torus_add(major_radius=R + .012, minor_radius=.014, location=(0, -.131, z), rotation=(math.pi/2, 0, 0))
    ring = bpy.context.object; ring.data.materials.append(M_VISOR); bpy.ops.object.shade_smooth()
    # lente (esfera aplanada → domo)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=R, segments=96, ring_count=48, location=(0, -.118, z))
    lens = bpy.context.object; lens.scale = (1, .22, 1)
    bpy.ops.object.transform_apply(scale=True)
    lens.data.materials.append(lens_mat(f"lente{i}", col, pw)); bpy.ops.object.shade_smooth()
    # visera: tubo abierto, se elimina la mitad inferior
    bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=R + .03, depth=.24, end_fill_type="NOTHING",
                                        location=(0, -.24, z), rotation=(math.pi/2, 0, 0))
    vis = bpy.context.object
    bpy.ops.object.transform_apply(rotation=True, location=False, scale=False)
    bm = bmesh.new(); bm.from_mesh(vis.data)
    kill = [v for v in bm.verts if v.co.z < -.055]
    bmesh.ops.delete(bm, geom=kill, context="VERTS"); bm.to_mesh(vis.data); bm.free()
    # inclinación ligera hacia abajo como las viseras reales
    vis.rotation_euler.x = math.radians(4)
    sol = vis.modifiers.new("s", "SOLIDIFY"); sol.thickness = .008
    add_bevel(vis, .003, 2)
    vis.data.materials.append(M_VISOR); bpy.ops.object.shade_smooth()
    # luz real que derrama color hacia delante
    bpy.ops.object.light_add(type="POINT", location=(0, -.32, z))
    pl = bpy.context.object; pl.data.energy = 6; pl.data.color = col; pl.data.shadow_soft_size = .1

# soporte / abrazadera y poste detrás
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=.07, depth=4, location=(0, .34, 0))
pole = bpy.context.object; pole.data.materials.append(M_POLE); bpy.ops.object.shade_smooth()
for zz in (.5, -.5):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, .22, zz))
    b = bpy.context.object; b.scale = (.12, .2, .06); bpy.ops.object.transform_apply(scale=True)
    add_bevel(b, .01, 3); b.data.materials.append(M_POLE)

# pared de chapa al fondo
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, .75, 0), rotation=(math.pi/2, 0, 0))
wall = bpy.context.object; wall.scale = (8, 8, 1)
bpy.ops.object.transform_apply(scale=True); wall.data.materials.append(M_WALL)

# ---------------------------------------------------------------- cámara y luz flash
bpy.ops.object.camera_add(location=(0.55, -2.55, -0.1))
cam = bpy.context.object; sc.camera = cam
cam.data.lens = 40
tgt = Vector((0.12, 0, -0.16))
d = tgt - cam.location
cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
cam.rotation_euler.rotate_axis("Z", math.radians(-9))  # encuadre inclinado, más dinámico

bpy.ops.object.light_add(type="AREA", location=(0.6, -2.2, 0.15))
flash = bpy.context.object; flash.data.size = .09; flash.data.energy = 90
flash.data.color = (1.0, 0.97, 0.93)
flash.rotation_euler = (tgt - flash.location).to_track_quat("-Z", "Y").to_euler()

# relleno azulado frío muy tenue (como en la referencia)
bpy.ops.object.light_add(type="AREA", location=(-2.0, -0.8, 1.6))
rim = bpy.context.object; rim.data.size = 2; rim.data.energy = 40; rim.data.color = (0.45, 0.35, 1.0)
rim.rotation_euler = (tgt - rim.location).to_track_quat("-Z", "Y").to_euler()

world = bpy.data.worlds.new("w"); sc.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0, 0, 0, 1)

# ---------------------------------------------------------------- render
sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = SAMPLES
sc.cycles.use_denoising = True
sc.render.resolution_x = W; sc.render.resolution_y = H
sc.render.film_transparent = False
sc.view_settings.view_transform = "Standard"
sc.view_settings.look = "Medium High Contrast"
sc.view_settings.exposure = 0.0
sc.render.image_settings.file_format = "PNG"
sc.render.filepath = out
bpy.ops.render.render(write_still=True)
print("OK", out)
