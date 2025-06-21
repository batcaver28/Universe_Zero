import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from numpy.fft import fft2, ifft2, fftfreq
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable


# Parámetros del dominio y simulación
L = 10000.0
grid_size = 128
N_particles = 10000
G = 1.0
dt = 1
steps = 300

# Inicialización
dx = L / grid_size

positions = np.random.uniform(0, L, (N_particles, 2)).astype(np.float32)
velocities = np.zeros((N_particles, 2), dtype=np.float32)

trajectory = []
velocities_history = []

# Grilla de densidad
def deposit_mass(positions):
    ix = np.floor(positions[:, 0] / dx).astype(int) % grid_size
    iy = np.floor(positions[:, 1] / dx).astype(int) % grid_size
    rho = np.zeros((grid_size, grid_size), dtype=np.float32)
    np.add.at(rho, (ix, iy), 1.0 / dx**2)
    return rho

# Resolver Poisson por FFT
def solve_poisson(rho):
    rho_k = fft2(rho)
    k = fftfreq(grid_size, d=dx) * 2 * np.pi
    KX, KY = np.meshgrid(k, k, indexing='ij')
    K2 = KX**2 + KY**2
    K2[0, 0] = 1
    phi_k = -4 * np.pi * G * rho_k / K2
    phi_k[0, 0] = 0
    phi = ifft2(phi_k).real
    return phi

# Campo de fuerza
def compute_force(phi):
    fx = (np.roll(phi, -1, axis=0) - np.roll(phi, 1, axis=0)) * (-0.5 / dx)
    fy = (np.roll(phi, -1, axis=1) - np.roll(phi, 1, axis=1)) * (-0.5 / dx)
    return fx.astype(np.float32), fy.astype(np.float32)

# Interpolación de fuerzas vectorizada
def interpolate_force(positions, fx, fy):
    ix = np.floor(positions[:, 0] / dx).astype(int) % grid_size
    iy = np.floor(positions[:, 1] / dx).astype(int) % grid_size
    forces = np.stack([fx[ix, iy], fy[ix, iy]], axis=1)
    return forces

# Simulación
for _ in range(steps):
    rho = deposit_mass(positions)
    phi = solve_poisson(rho)
    fx, fy = compute_force(phi)
    forces = interpolate_force(positions, fx, fy)
    velocities += forces * dt
    positions += velocities * dt
    positions %= L
    trajectory.append(positions.copy())
    velocities_history.append(velocities.copy())

# Normalización automática
all_speed = np.array([np.linalg.norm(v, axis=1) for v in velocities_history])
vmax = np.percentile(all_speed, 99)
norm = Normalize(vmin=0, vmax=vmax)
cmap = plt.colormaps["viridis"]

# Animación
fig, ax = plt.subplots(figsize=(6, 5))
initial_colors = cmap(norm(np.linalg.norm(velocities_history[0], axis=1)))
scat = ax.scatter(trajectory[0][:, 0], trajectory[0][:, 1], s=0.3, alpha=0.6, c=initial_colors)
ax.set_xlim(0, L)
ax.set_ylim(0, L)
ax.set_title("Particle Speed Visualization")
sm = ScalarMappable(norm=norm, cmap=cmap)
sm.set_array([])  # necesario para crear la colorbar sin imagen asociada
cbar = plt.colorbar(sm, ax=ax, orientation='vertical')
cbar.set_label("Speed")

def update(frame):
    pos = trajectory[frame]
    vel = velocities_history[frame]
    speed = np.linalg.norm(vel, axis=1)
    colors = cmap(norm(speed))
    scat.set_offsets(pos)
    scat.set_color(colors)
    return scat,

ani = FuncAnimation(fig, update, frames=steps, interval=30, blit=True)
plt.show()
# ani.save("simulacion1.gif", writer="pillow", fps=30, dpi=100)
