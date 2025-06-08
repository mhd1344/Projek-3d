import numpy as np
import plotly.graph_objects as go
 
# ─────────────────────────────────────────────
# Fungsi Pembangun Objek 3D
# ─────────────────────────────────────────────
 
def create_cube(center, size, color):
    cx, cy, cz = center
    lx, ly, lz = size
    x = [-lx/2, lx/2]
    y = [-ly/2, ly/2]
    z = [-lz/2, lz/2]
    vertices = np.array([[cx+i, cy+j, cz+k] for i in x for j in y for k in z])
    faces = [
        [0, 1, 3, 2], [4, 5, 7, 6], [0, 1, 5, 4],
        [2, 3, 7, 6], [1, 3, 7, 5], [0, 2, 6, 4]
    ]
    i, j, k = [], [], []
    for face in faces:
        i += [face[0], face[1], face[2]]
        j += [face[1], face[2], face[3]]
        k += [face[2], face[3], face[0]]
    return go.Mesh3d(
        x=vertices[:,0], y=vertices[:,1], z=vertices[:,2],
        i=i, j=j, k=k, color=color, flatshading=True
    )
 
def create_cylinder(center, radius, height, color, resolution=20):
    cx, cy, cz = center
    theta = np.linspace(0, 2*np.pi, resolution)
    x = np.concatenate([radius * np.cos(theta) + cx, radius * np.cos(theta) + cx])
    y = np.concatenate([radius * np.sin(theta) + cy, radius * np.sin(theta) + cy])
    z = np.concatenate([np.full(resolution, cz), np.full(resolution, cz + height)])
 
    triangles = []
    for i in range(resolution):
        next_i = (i + 1) % resolution
        triangles.extend([
            [i, next_i, resolution + next_i],
            [i, resolution + next_i, resolution + i]
        ])
    i, j, k = zip(*triangles)
    return go.Mesh3d(x=x, y=y, z=z, i=i, j=j, k=k, color=color)
 
def create_sphere(center, radius, color, resolution=20):
    u = np.linspace(0, 2 * np.pi, resolution)
    v = np.linspace(0, np.pi, resolution)
    x = center[0] + radius * np.outer(np.cos(u), np.sin(v)).flatten()
    y = center[1] + radius * np.outer(np.sin(u), np.sin(v)).flatten()
    z = center[2] + radius * np.outer(np.ones_like(u), np.cos(v)).flatten()
    return go.Mesh3d(x=x, y=y, z=z, alphahull=0, color=color)
 
def create_cone(center, radius, height, color, resolution=20):
    cx, cy, cz = center
    theta = np.linspace(0, 2*np.pi, resolution)
    x = np.append(radius * np.cos(theta) + cx, cx)
    y = np.append(radius * np.sin(theta) + cy, cy)
    z = np.append(np.full(resolution, cz), cz + height)
 
    triangles = [[i, (i+1)%resolution, resolution] for i in range(resolution)]
    i, j, k = zip(*triangles)
    return go.Mesh3d(x=x, y=y, z=z, i=i, j=j, k=k, color=color)
 
# ─────────────────────────────────────────────
# Membangun Scene
# ─────────────────────────────────────────────
 
# 1. MEJA
meja_atas = create_cube(center=[0, 0, 1], size=[6, 3, 0.3], color='#8B4513')  # Meja 6x3 unit
kaki_meja = [
    create_cylinder(center=[x, y, 0], radius=0.2, height=1, color='#654321')
    for x, y in [(-2.5,-1), (-2.5,1), (2.5,-1), (2.5,1)]
]
 
# 2. LAMPU BELAJAR - POSISI Disesuaikan ke KIRI, LEBIH TINGGI, dan Lengan ke DALAM
# Ubah koordinat X untuk memindahkan dasar lampu ke kiri
# Ubah koordinat Z untuk memindahkan keseluruhan lampu lebih tinggi
posisi_dasar_lampu_x = -2.7 # Dari 2.7 (kanan) ke -2.7 (kiri)
posisi_dasar_lampu_y = -0.8 # Biarkan sama
posisi_dasar_lampu_z = 1.25 # Dari 1.15 ke 1.25 (sedikit lebih tinggi)
 
tinggi_tiang = 0.8 # Sedikit lebih tinggi dari 0.7
 
dasar_lampu = create_cube(center=[posisi_dasar_lampu_x, posisi_dasar_lampu_y, posisi_dasar_lampu_z], size=[0.3, 0.3, 0.1], color='#A9A9A9')  # Dasar lampu di sudut meja
tiang_lampu = create_cylinder(center=[posisi_dasar_lampu_x, posisi_dasar_lampu_y, posisi_dasar_lampu_z + 0.05], radius=0.03, height=tinggi_tiang, color='#696969')  # Tiang vertikal
sendi_lampu = create_sphere(center=[posisi_dasar_lampu_x, posisi_dasar_lampu_y, posisi_dasar_lampu_z + tinggi_tiang + 0.05], radius=0.05, color='#333333')  # Sendi penyangga
 
# Lengan lampu memanjang ke KANAN (ke dalam meja) dari sendi.
# Pusatnya akan berada di (posisi_sendi_x + panjang_lengan/2)
panjang_lengan = 1.0
posisi_sendi_x = posisi_dasar_lampu_x
posisi_sendi_y = posisi_dasar_lampu_y
posisi_sendi_z = posisi_dasar_lampu_z + tinggi_tiang + 0.05 # Z sendi
 
lengan_lampu = create_cube(center=[posisi_sendi_x + panjang_lengan/2, posisi_sendi_y, posisi_sendi_z], size=[panjang_lengan, 0.04, 0.04], color='#696969') # Lengan horizontal
 
# Tudung lampu dan bohlam diposisikan di ujung lengan horizontal
# Ujung lengan horizontal sekarang berada di x = posisi_sendi_x + panjang_lengan
posisi_ujung_lengan_x = posisi_sendi_x + panjang_lengan
posisi_ujung_lengan_y = posisi_sendi_y
posisi_ujung_lengan_z = posisi_sendi_z # Z sama dengan lengan
 
tudung_lampu = create_cone(center=[posisi_ujung_lengan_x, posisi_ujung_lengan_y, posisi_ujung_lengan_z], radius=0.25, height=0.4, color='#FFD700')  # Tudung lampu
bohlam_lampu = create_sphere(center=[posisi_ujung_lengan_x, posisi_ujung_lengan_y, posisi_ujung_lengan_z - 0.15], radius=0.07, color='#FFFFE0')  # Bohlam
 
# 3. AKSESORIS MEJA
buku = create_cube(center=[-1.5, 0.5, 1.2], size=[0.8, 1.2, 0.15], color='#4169E1')
pensil = create_cylinder(center=[-0.5, 1.0, 1.2], radius=0.03, height=0.6, color='#FF0000')
 
# Gabungkan semua objek
semua_objek = [
    meja_atas,
    *kaki_meja,
    dasar_lampu,
    tiang_lampu,
    sendi_lampu,
    lengan_lampu,
    tudung_lampu,
    bohlam_lampu,
    buku,
    pensil
]
 
# Konfigurasi tampilan
fig = go.Figure(data=semua_objek)
fig.update_layout(
    scene=dict(
        camera=dict(
            eye=dict(x=1.5, y=-1.5, z=1.2),  # Sudut pandang diagonal
            up=dict(x=0, y=0, z=1)
        ),
        aspectmode='data',
        xaxis=dict(visible=False, range=[-3.5,4]),
        yaxis=dict(visible=False, range=[-2,2]),
        zaxis=dict(visible=False, range=[0,2.5])
    ),
    margin=dict(l=0, r=0, b=0, t=0),
    scene_camera=dict(
        projection=dict(type='perspective')
    )
)
 
 
# === Export as JSON for embedding (e.g., in Pyodide) ===
fig_json = fig.to_json()
def get_plot_json():
    return fig_json