# 🔭 Particle-Mesh Gravity Simulator

A simulation of 10,000 particles interacting purely through **gravity**, implemented in **Python** using efficient numerical methods and **Matplotlib** for visualization. This project explores emergent dynamics in high-density particle systems within a **toroidal topology** (like a donut), where particles are attracted to each other and seamlessly wrap around the simulation space.

---

## ✨ Features

- 🌌 Simulates **N-body gravity** using the **Particle-Mesh (PM)** method  
- ⚡ High performance: scales as \( O(N + M \log M) \), enabling tens of thousands of particles  
- 🎨 Animated visualization with **logarithmic color mapping** based on particle speed  
- 🌀 **Toroidal space**: particles wrap around the edges of the simulation  
- 🧠 Clean, modular Python code with export options (`.gif` or `.mp4`)  
- 📈 Uses **FFT** to efficiently solve Poisson’s equation  

---

## 🛠 Technologies Used

- **Python 3.10+**
- `numpy`
- `matplotlib`
- `scipy.fft` or `numpy.fft`
- `matplotlib.colors.LogNorm`

---

## 📦 Installation

```bash
git clone https://github.com/your-username/particle-mesh-simulator.git
cd particle-mesh-simulator
pip install -r requirements.txt
```

---

## 🚀 Running the Simulation

```bash
python universe.py
```

To export the animation, uncomment the following lines at the end of the script:

```python
ani.save("simulation.gif", writer="pillow", fps=60, dpi=100)
# or
ani.save("simulation.mp4", writer="ffmpeg", fps=60)
```

---

## 📊 Method Overview

This simulator implements the **Particle-Mesh method**, which works as follows:

1. Particle mass is deposited onto a uniform 2D grid.
2. The gravitational potential is computed by solving Poisson’s equation via FFT.
3. The gravitational field is obtained as the gradient of the potential.
4. Forces are interpolated back to the particles, which are then updated using numerical integration.

This approach avoids expensive \( O(N^2) \) pairwise calculations and is well-suited for **dense gravitational systems**.

---

## 📸 Example Visualization

![preview gif](simulacion1.gif)

---

## ✍️ Author

**Matías Reyes**  
> I simulate a universe of 10,000 particles on a donut-shaped space. I let them attract each other through gravity alone—and from that simplicity, a stunning, complex, and strangely familiar cosmos emerges.

---

## 📄 License

Free to use, modify, and experiment with.
