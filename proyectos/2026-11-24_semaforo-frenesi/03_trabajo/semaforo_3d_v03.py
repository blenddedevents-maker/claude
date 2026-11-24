"""v03 — Semáforo realista estilo foto con flash nocturno.
Genera dos imágenes: <salida>.png (render) y <salida>_mask.png (alfa del semáforo + poste),
para poder colocar el título POR DETRÁS del semáforo en la composición.
Uso: python3 semaforo_3d_v03.py <salida_sin_ext> <ancho> <alto> <samples>
"""
import sys, math, random, bpy, bmesh
from mathutils import Vector

base_out = sys.argv[1] if len(sys.argv) > 1 else "render"
W = int(sys.argv[2]) if len(sys.argv) > 2 else 540
H = int(sys.argv[3]) if len(sys.argv) > 3 else 675
SAMPLES = int(sys.argv[4]) if len(sys.argv) > 4 else 32
random.seed(21)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

# ============================================================ utilidades de nodos
def new_mat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    return m, nt.nodes, nt.links, nt.nodes.new("ShaderNodeOutputMaterial")

def math_node(N, L, op, a=None, b=None, va=None, vb=None):
    n = N.new("ShaderNodeMath"); n.operation = op
    if a is not None: L.new(a, n.inputs[0])
    elif va is not None: n.inputs[0].default_value = va
    if b is not None: L.new(b, n.inputs[1])
    elif vb is not None: n.inputs[1].default_value = vb
    return n.outputs[0]

def ramp(N, L, src, p0, p1, c0=(0, 0, 0, 1), c1=(1, 1, 1, 1)):
    r = N.new("ShaderNodeValToRGB")
    r.color_ramp.elements[0].position = p0; r.color_ramp.elements[0].color = c0
    r.color_ramp.elements[1].position = p1; r.color_ramp.elements[1].color = c1
    L.new(src, r.inputs["Fac"]); return r.outputs["Color"]

def noise(N, L, vec, scale, detail=8, rough=.6):
    n = N.new("ShaderNodeTexNoise"); n.inputs["Scale"].default_value = scale
    n.inputs["Detail"].default_value = detail; n.inputs["Roughness"].default_value = rough
    if vec is not None: L.new(vec, n.inputs["Vector"])
    return n.outputs["Fac"]

def mapping(N, L, vec, scale=(1, 1, 1), rot=(0, 0, 0)):
    m = N.new("ShaderNodeMapping"); m.inputs["Scale"].default_value = scale
    m.inputs["Rotation"].default_value = rot; L.new(vec, m.inputs["Vector"]); return m.outputs["Vector"]

def mix_rgb(N, L, fac, a, b):
    m = N.new("ShaderNodeMix"); m.data_type = "RGBA"
    if isinstance(fac, float): m.inputs[0].default_value = fac
    else: L.new(fac, m.inputs[0])
    for i, v in ((6, a), (7, b)):
        if isinstance(v, tuple): m.inputs[i].default_value = v
        else: L.new(v, m.inputs[i])
    return m.outputs[2]

# ============================================================ materiales
def painted_metal(name, paint, dust=(0.32, 0.30, 0.27), dust_amt=1.0, scratch=1.0):
    """Pintura vieja: polvo en superficies hacia arriba, chorretones, rayones y bordes gastados."""
    m, N, L, o = new_mat(name)
    b = N.new("ShaderNodeBsdfPrincipled")
    tc = N.new("ShaderNodeTexCoord").outputs["Object"]
    geo = N.new("ShaderNodeNewGeometry")
    # polvo: normales hacia arriba + ruido
    sep = N.new("ShaderNodeSeparateXYZ"); L.new(geo.outputs["Normal"], sep.inputs[0])
    up = ramp(N, L, sep.outputs["Z"], .35, .95)
    dn = noise(N, L, tc, 14, 10, .7)
    dmask = math_node(N, L, "MULTIPLY", up, ramp(N, L, dn, .35, .7))
    dmask = math_node(N, L, "MULTIPLY", dmask, vb=.85 * dust_amt)
    # chorretones verticales de lluvia
    streak = noise(N, L, mapping(N, L, tc, (60, 60, 1.2)), 3, 6, .5)
    sm = ramp(N, L, streak, .55, .75)
    # manchas generales
    blot = ramp(N, L, noise(N, L, tc, 5, 12, .65), .3, .8)
    # rayones finos (bordes de voronoi estirados) con máscara
    def scr(rot, s):
        v = N.new("ShaderNodeTexVoronoi"); v.feature = "DISTANCE_TO_EDGE"; v.inputs["Scale"].default_value = s
        L.new(mapping(N, L, tc, (1, 1, .25), rot), v.inputs["Vector"])
        return ramp(N, L, v.outputs["Distance"], 0, .006, (1, 1, 1, 1), (0, 0, 0, 1))
    sc_ = math_node(N, L, "MAXIMUM", scr((.4, .9, .3), 9), scr((1.1, -.5, 2.2), 15))
    sc_ = math_node(N, L, "MULTIPLY", sc_, ramp(N, L, noise(N, L, tc, 3), .52, .62))
    sc_ = math_node(N, L, "MULTIPLY", sc_, vb=scratch)
    # color
    col = mix_rgb(N, L, math_node(N, L, "MULTIPLY", blot, vb=.35), (*paint, 1), tuple(min(c * 1.8 + .01, 1) for c in paint) + (1,))
    col = mix_rgb(N, L, math_node(N, L, "MULTIPLY", sm, vb=.3), col, (0.05, 0.045, 0.04, 1))
    col = mix_rgb(N, L, sc_, col, (0.42, 0.42, 0.43, 1))      # metal visto bajo la pintura
    col = mix_rgb(N, L, dmask, col, (*dust, 1))
    L.new(col, b.inputs["Base Color"])
    # rugosidad
    rr = N.new("ShaderNodeMath"); rr.operation = "MULTIPLY_ADD"
    L.new(blot, rr.inputs[0]); rr.inputs[1].default_value = .2; rr.inputs[2].default_value = .42
    r2 = math_node(N, L, "MAXIMUM", rr.outputs[0], math_node(N, L, "MULTIPLY", dmask, vb=.95))
    r3 = math_node(N, L, "SUBTRACT", r2, math_node(N, L, "MULTIPLY", sc_, vb=.15))
    L.new(r3, b.inputs["Roughness"])
    L.new(math_node(N, L, "MULTIPLY", sc_, vb=.6), b.inputs["Metallic"])
    # relieve
    bump = N.new("ShaderNodeBump"); bump.inputs["Distance"].default_value = .0015; bump.inputs["Strength"].default_value = .25
    h = math_node(N, L, "ADD", math_node(N, L, "MULTIPLY", noise(N, L, tc, 90, 4), vb=.25), math_node(N, L, "MULTIPLY", sc_, vb=-.5))
    L.new(h, bump.inputs["Height"]); L.new(bump.outputs["Normal"], b.inputs["Normal"])
    L.new(b.outputs[0], o.inputs[0])
    return m

def galvanized(name):
    m, N, L, o = new_mat(name)
    b = N.new("ShaderNodeBsdfPrincipled"); b.inputs["Metallic"].default_value = 1
    tc = N.new("ShaderNodeTexCoord").outputs["Object"]
    vo = N.new("ShaderNodeTexVoronoi"); vo.inputs["Scale"].default_value = 30; L.new(tc, vo.inputs["Vector"])
    spang = ramp(N, L, vo.outputs["Distance"], .0, 1., (.25, .25, .26, 1), (.45, .45, .47, 1))
    dirt = ramp(N, L, noise(N, L, mapping(N, L, tc, (20, 20, 1)), 4), .4, .8)
    col = mix_rgb(N, L, math_node(N, L, "MULTIPLY", dirt, vb=.7), spang, (.06, .055, .05, 1))
    L.new(col, b.inputs["Base Color"])
    rr = N.new("ShaderNodeMath"); rr.operation = "MULTIPLY_ADD"
    L.new(dirt, rr.inputs[0]); rr.inputs[1].default_value = .35; rr.inputs[2].default_value = .3
    L.new(rr.outputs[0], b.inputs["Roughness"])
    L.new(b.outputs[0], o.inputs[0]); return m

def rubber(name):
    m, N, L, o = new_mat(name)
    b = N.new("ShaderNodeBsdfPrincipled")
    b.inputs["Base Color"].default_value = (.012, .012, .012, 1); b.inputs["Roughness"].default_value = .7
    L.new(b.outputs[0], o.inputs[0]); return m

def led_lens(name, col, hot, power, R):
    """Lente LED: matriz de LEDs emisivos + difusor + lente con anillos fresnel y capa brillante."""
    m, N, L, o = new_mat(name)
    tc = N.new("ShaderNodeTexCoord").outputs["Object"]
    sep = N.new("ShaderNodeSeparateXYZ"); L.new(tc, sep.inputs[0])
    xz = N.new("ShaderNodeCombineXYZ"); L.new(sep.outputs["X"], xz.inputs["X"]); L.new(sep.outputs["Z"], xz.inputs["Y"])
    rad = N.new("ShaderNodeVectorMath"); rad.operation = "LENGTH"; L.new(xz.outputs[0], rad.inputs[0])
    rad = rad.outputs["Value"]
    # LEDs en anillos concéntricos (como los semáforos reales): ángulo y radio cuantizados
    pitch = 0.0145
    ring_i = math_node(N, L, "DIVIDE", rad, vb=pitch)
    ring_f = math_node(N, L, "SUBTRACT", math_node(N, L, "FRACT", ring_i), vb=.5)
    ring_n = math_node(N, L, "FLOOR", math_node(N, L, "ADD", ring_i, vb=.5))
    ang = math_node(N, L, "ARCTAN2", sep.outputs["Z"], sep.outputs["X"])
    count = math_node(N, L, "MAXIMUM", math_node(N, L, "FLOOR", math_node(N, L, "MULTIPLY", ring_n, vb=6.2832)), vb=1)
    a_i = math_node(N, L, "MULTIPLY", math_node(N, L, "DIVIDE", ang, vb=6.2832), count)
    a_f = math_node(N, L, "SUBTRACT", math_node(N, L, "FRACT", a_i), vb=.5)
    # distancia aproximada al centro del LED (en unidades de pitch)
    arc = math_node(N, L, "MULTIPLY", a_f, math_node(N, L, "DIVIDE", math_node(N, L, "MULTIPLY", ring_n, vb=6.2832), count))
    d2 = math_node(N, L, "ADD", math_node(N, L, "POWER", ring_f, vb=2), math_node(N, L, "POWER", arc, vb=2))
    d = math_node(N, L, "SQRT", d2)
    dot = ramp(N, L, d, .16, .36, (1, 1, 1, 1), (0, 0, 0, 1))
    inside = ramp(N, L, rad, R * .86, R * .9, (1, 1, 1, 1), (0, 0, 0, 1))
    dot = math_node(N, L, "MULTIPLY", dot, inside)
    # brillo: difusor tenue + LEDs muy calientes, caída suave hacia el borde
    fall = ramp(N, L, rad, 0, R, (1, 1, 1, 1), (.55, .55, .55, 1))
    strength = math_node(N, L, "MULTIPLY",
                         math_node(N, L, "ADD", math_node(N, L, "MULTIPLY", dot, vb=power), vb=power * .05), fall)
    ecol = mix_rgb(N, L, math_node(N, L, "MULTIPLY", dot, vb=.8), (*col, 1), (*hot, 1))
    em = N.new("ShaderNodeEmission"); L.new(ecol, em.inputs["Color"]); L.new(strength, em.inputs["Strength"])
    # capa de policarbonato: reflejos del flash, anillos fresnel y algo de suciedad
    gl = N.new("ShaderNodeBsdfPrincipled")
    gl.inputs["Base Color"].default_value = (col[0] * .02, col[1] * .02, col[2] * .02, 1)
    gl.inputs["Specular IOR Level"].default_value = .8
    dirt = ramp(N, L, noise(N, L, tc, 18, 12, .7), .45, .85)
    rr = N.new("ShaderNodeMath"); rr.operation = "MULTIPLY_ADD"
    L.new(dirt, rr.inputs[0]); rr.inputs[1].default_value = .45; rr.inputs[2].default_value = .05
    L.new(rr.outputs[0], gl.inputs["Roughness"])
    rings = math_node(N, L, "SINE", math_node(N, L, "MULTIPLY", rad, vb=520))
    bump = N.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = .25; bump.inputs["Distance"].default_value = .0004
    L.new(rings, bump.inputs["Height"]); L.new(bump.outputs["Normal"], gl.inputs["Normal"])
    add = N.new("ShaderNodeAddShader"); L.new(em.outputs[0], add.inputs[0]); L.new(gl.outputs[0], add.inputs[1])
    L.new(add.outputs[0], o.inputs[0])
    return m

def emissive(name, col, s):
    m, N, L, o = new_mat(name)
    e = N.new("ShaderNodeEmission"); e.inputs["Color"].default_value = (*col, 1); e.inputs["Strength"].default_value = s
    L.new(e.outputs[0], o.inputs[0]); return m

M_PAINT = painted_metal("pintura", (0.016, 0.017, 0.016), scratch=.35)
M_VISOR = painted_metal("visera", (0.014, 0.015, 0.014), dust_amt=1.3, scratch=.35)
M_POLE = galvanized("poste")
M_RUB = rubber("goma")

# ============================================================ geometría
def bevel(ob, w, seg=5):
    md = ob.modifiers.new("bev", "BEVEL"); md.width = w; md.segments = seg; md.limit_method = "ANGLE"

def box(loc, size, mat, bw=.01, seg=4):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object; o.scale = size; bpy.ops.object.transform_apply(scale=True)
    bevel(o, bw, seg); o.data.materials.append(mat); bpy.ops.object.shade_smooth(); return o

def cyl(loc, r, d, mat, rot=(0, 0, 0), v=48):
    bpy.ops.mesh.primitive_cylinder_add(vertices=v, radius=r, depth=d, location=loc, rotation=rot)
    o = bpy.context.object; o.data.materials.append(mat); bpy.ops.object.shade_smooth(); return o

MW, MD, MH = 0.34, 0.24, 0.355     # módulo
GAP = 0.008
R = 0.104                          # lente Ø 200 mm aprox
LIGHTS = [
    (MH + GAP, (1.0, 0.015, 0.01), (1.0, 0.22, 0.12), 6),
    (0.0,      (1.0, 0.28, 0.0),   (1.0, 0.70, 0.25), 6),
    (-(MH + GAP), (0.0, 1.0, 0.18), (0.45, 1.0, 0.55), 5),
]
FRONT = -MD / 2

for z, col, hot, pw in LIGHTS:
    box((0, 0, z), (MW, MD, MH), M_PAINT, .028, 6)
    # marco frontal (puerta) ligeramente sobresaliente
    box((0, FRONT - .006, z), (MW - .03, .014, MH - .03), M_PAINT, .006, 3)
    # junta de goma + aro
    bpy.ops.mesh.primitive_torus_add(major_radius=R + .006, minor_radius=.008, location=(0, FRONT - .016, z),
                                     rotation=(math.pi / 2, 0, 0), major_segments=96, minor_segments=16)
    t = bpy.context.object; t.data.materials.append(M_RUB); bpy.ops.object.shade_smooth()
    # lente abombada
    bpy.ops.mesh.primitive_uv_sphere_add(radius=R, segments=128, ring_count=64, location=(0, FRONT - .012, z))
    ln = bpy.context.object; ln.scale = (1, .16, 1); bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    ln.data.materials.append(led_lens(f"led{z:.2f}", col, hot, pw, R)); bpy.ops.object.shade_smooth()
    # visera larga (tubo abierto por abajo), con leve inclinación
    L_V = .27
    bpy.ops.mesh.primitive_cylinder_add(vertices=128, radius=R + .028, depth=L_V, end_fill_type="NOTHING",
                                        location=(0, 0, 0), rotation=(math.pi / 2, 0, 0))
    v = bpy.context.object; bpy.ops.object.transform_apply(rotation=True)
    bm = bmesh.new(); bm.from_mesh(v.data)
    bmesh.ops.delete(bm, geom=[q for q in bm.verts if q.co.z < -(R + .028) * .42], context="VERTS")
    bm.to_mesh(v.data); bm.free()
    v.location = (0, FRONT - .02 - L_V / 2, z + .004); v.rotation_euler.x = math.radians(-5)
    s = v.modifiers.new("s", "SOLIDIFY"); s.thickness = .006; s.offset = 1
    bevel(v, .002, 2); v.data.materials.append(M_VISOR); bpy.ops.object.shade_smooth()
    # tornillos del marco
    for sx in (-1, 1):
        for sz in (-1, 1):
            cyl((sx * (MW / 2 - .035), FRONT - .014, z + sz * (MH / 2 - .035)), .0075, .008, M_POLE, rot=(math.pi / 2, 0, 0), v=16)
    # bisagra lateral
    cyl((-MW / 2 - .004, FRONT + .02, z), .009, MH * .55, M_PAINT, v=16)
    # luz de derrame
    bpy.ops.object.light_add(type="POINT", location=(0, FRONT - .2, z + .02))
    p = bpy.context.object; p.data.energy = 2.2; p.data.color = col; p.data.shadow_soft_size = .08

# tapa superior y base
box((0, 0, 1.5 * MH + GAP + .012), (MW - .01, MD - .01, .025), M_PAINT, .01)
box((0, 0, -1.5 * MH - GAP - .012), (MW - .01, MD - .01, .025), M_PAINT, .01)
# poste y abrazaderas
POLE_Y = MD / 2 + .12
cyl((0, POLE_Y, -1.2), .055, 5, M_POLE, v=64)
for zz in (MH * .9, -MH * .9):
    box((0, MD / 2 + .06, zz), (.09, .13, .05), M_POLE, .006, 2)
    bpy.ops.mesh.primitive_torus_add(major_radius=.061, minor_radius=.01, location=(0, POLE_Y, zz))
    t = bpy.context.object; t.data.materials.append(M_POLE); bpy.ops.object.shade_smooth()
# cable
bpy.ops.curve.primitive_bezier_curve_add(location=(0, 0, 0))
cv = bpy.context.object; cv.data.bevel_depth = .007
pts = cv.data.splines[0].bezier_points
pts[0].co = (.0, MD / 2, -1.5 * MH); pts[0].handle_left = (0, MD / 2, -1.4 * MH); pts[0].handle_right = (.03, MD / 2 + .05, -1.9 * MH)
pts[1].co = (.035, POLE_Y - .05, -2.3 * MH); pts[1].handle_left = (.04, POLE_Y - .05, -2.0 * MH); pts[1].handle_right = (.03, POLE_Y - .05, -2.6 * MH)
cv.data.materials.append(M_RUB)

# bokeh de ciudad muy al fondo
BOKEH = []
pal = [(0.55, 0.25, 1.0), (0.25, 0.35, 1.0), (1.0, 0.55, 0.2), (0.9, 0.2, 0.9), (1, .85, .6)]
for i in range(0):
    x = random.uniform(-7, 7); z = random.uniform(-4.5, 5.0); y = random.uniform(10, 22)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=random.uniform(.03, .08), location=(x, y, z), segments=12, ring_count=6)
    o = bpy.context.object; o.data.materials.append(emissive(f"bk{i}", random.choice(pal), random.uniform(6, 22)))
    BOKEH.append(o)

# ============================================================ cámara (como una foto con flash)
cam_loc = Vector((0.40, -2.86, 0.03))
bpy.ops.object.camera_add(location=cam_loc)
cam = bpy.context.object; sc.camera = cam
cam.data.lens = 50
tgt = Vector((0.085, 0, -0.15))
cam.rotation_euler = (tgt - cam_loc).to_track_quat("-Z", "Y").to_euler()
cam.rotation_euler.rotate_axis("Z", math.radians(-6))
cam.data.dof.use_dof = True
cam.data.dof.focus_distance = (Vector((0, FRONT - .05, 0)) - cam_loc).length
cam.data.dof.aperture_fstop = 3.2

# flash: fuente pequeña y potente junto a la cámara → sombras duras y caída rápida
fl_loc = cam_loc + Vector((-0.10, 0.02, 0.16))
bpy.ops.object.light_add(type="AREA", location=fl_loc)
fl = bpy.context.object; fl.data.shape = "RECTANGLE"; fl.data.size = .05; fl.data.size_y = .03
fl.data.energy = 120; fl.data.color = (1.0, 0.975, 0.95)
fl.rotation_euler = (tgt - fl_loc).to_track_quat("-Z", "Y").to_euler()
# contraluz violeta para separar la silueta del fondo
bpy.ops.object.light_add(type="AREA", location=(-1.2, 1.6, 1.4))
rim = bpy.context.object; rim.data.size = .8; rim.data.energy = 120; rim.data.color = (.55, .3, 1.0)
rim.rotation_euler = (Vector((0, 0, 0)) - rim.location).to_track_quat("-Z", "Y").to_euler()

world = bpy.data.worlds.new("w"); sc.world = world; world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.0005, 0.0004, 0.001, 1)

# ============================================================ render
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"
sc.cycles.use_denoising = True
sc.cycles.max_bounces = 6
sc.render.resolution_x = W; sc.render.resolution_y = H
sc.view_settings.view_transform = "Standard"; sc.view_settings.look = "Medium High Contrast"
sc.render.image_settings.file_format = "PNG"

sc.cycles.samples = SAMPLES
sc.render.film_transparent = False
sc.render.image_settings.color_mode = "RGB"
sc.render.filepath = base_out + ".png"
bpy.ops.render.render(write_still=True)

# máscara: sin bokeh y fondo transparente → alfa = semáforo + poste
for o in BOKEH: o.hide_render = True
sc.render.film_transparent = True
sc.render.image_settings.color_mode = "RGBA"
sc.cycles.samples = 16
sc.cycles.use_denoising = False
sc.render.filepath = base_out + "_mask.png"
bpy.ops.render.render(write_still=True)
print("OK", base_out)
