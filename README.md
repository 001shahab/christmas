# ✨ Merry Christmas & Happy New Year Animation ✨

A stunning, magical Python animation celebrating the festive season with an elegant transition from Christmas to New Year celebrations.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.5+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎄 Features

- **Beautiful Christmas Tree** - Layered, decorated tree with glowing ornaments
- **Falling Snowflakes** - Realistic snow with drift and rotation physics
- **Twinkling Stars** - Dynamic starfield with varying brightness
- **Spectacular Fireworks** - Multiple explosion patterns (burst, ring, willow, star, double)
- **Smooth Transitions** - Elegant fade from "Merry Christmas" to "Happy New Year"
- **Aurora Effect** - Subtle northern lights shimmer in the sky
- **Interactive** - Press SPACE to launch manual fireworks!

## 🎬 Animation Timeline

| Phase | Duration | Description |
|-------|----------|-------------|
| Christmas | 0-15s | Cozy Christmas scene with tree, snow, and occasional fireworks |
| Transition | 15-18s | Smooth crossfade between holiday messages |
| New Year | 18s+ | Celebratory fireworks display with "2026" |

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download this repository**

2. **Create a virtual environment (recommended)**
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the animation**
   ```bash
   python christmas.py
   ```

## 🎮 Controls

| Key | Action |
|-----|--------|
| `SPACE` | Launch a firework |
| `ESC` | Exit the animation |

## 🎨 Visual Elements

### Firework Patterns
- **Burst** - Classic spherical explosion
- **Ring** - Circular pattern with inner burst
- **Double** - Two concentric rings of different colors
- **Willow** - Cascading waterfall effect
- **Star** - Five-pointed star burst

### Color Palette
The animation uses a carefully crafted color palette featuring:
- Deep midnight blues for the night sky
- Warm golds and reds for ornaments
- Crisp whites for snow and stars
- Vibrant colors for fireworks

## 📁 Project Structure

```
christmas/
├── christmas.py      # Main animation script
├── requirements.txt  # Python dependencies
├── README.md         # This file
└── myenv/            # Virtual environment (created by user)
```

## 🔧 Customization

You can easily customize the animation by modifying these variables in `christmas.py`:

```python
# Screen size
WIDTH, HEIGHT = 1200, 800

# Animation timing
christmas_duration = 15000  # Christmas phase duration (ms)
transition_duration = 3000  # Transition duration (ms)

# Particle counts
snowflakes = [Snowflake() for _ in range(150)]  # Number of snowflakes
stars = [Star() for _ in range(100)]            # Number of stars
```

## 💻 Technical Details

- **Framework**: Pygame 2.5+
- **Rendering**: Hardware-accelerated 2D graphics
- **Frame Rate**: 60 FPS with delta time for smooth animation
- **Particle System**: Custom implementation for snow and fireworks
- **Alpha Blending**: SRCALPHA surfaces for glow effects

## 👨‍🎓 Author

**Prof. Shahab Anbarjafari**  
*3S Holding OU*  
*Tartu, Estonia*

---

## 📄 License

This project is open source and available under the MIT License.

---

<p align="center">
  <b>🎄 Wishing you a Merry Christmas and a Happy New Year! 🎆</b>
</p>
