# Cellular Automata Engine

## Author: Matthew Boughton  
Term Project for **15-112**  

---

## Overview

The **Cellular Automata Engine** is an interactive project designed to showcase three types of cellular automata. It allows users to explore, manipulate, and experience these automata through an engaging interface. The engine incorporates features like board resizing, dynamic ruleset generation, and particle physics simulations.

---

## Installation

### Prerequisites:
To run this program, you must install the `cmu_112_graphics` library. Follow the installation instructions provided on the official website:  
[CMU 112 Graphics Installation Guide](https://www.cs.cmu.edu/~112/notes/notes-graphics.html)  

---

## How to Run

1. Clone or download this repository.
2. Ensure `cmu_112_graphics` is properly installed.
3. Run the `Main.py` file to start the program.
4. In the application, all commands and keybindings will be displayed to guide your interactions.

---

## File Map

- **`Main.py`**: Main entry point for the program.  
- **`Game_Of_Life.py`**: Contains the Game of Life object and logic.  
- **`Wolfram_Grid.py`**: Implements the Wolfram automata simulation.  
- **`Element_Objects.py`**: Defines cell objects for physics-based elements, with each class representing a unique element.  
- **`Physics_CA.py`**: Implements the physics-based cellular automata engine.  
- **`Features.txt`**: Detailed list of program features.  

---

## Features

### General Features:
1. Board automatically resizes based on app dimensions.  
2. Integer-based ruleset creation for automata.  
3. Multiple simulation modes:
   - Game of Life
   - Wolfram Code Simulation
   - Physics-Based Cellular Automata  
4. Interactive brush tools for:
   - Adjustable brush size
   - Drag-to-draw capability  

### Simulation Features:
5. Pause, step forward, and resume simulations.  
6. Track generations over time.  
7. Change automata rulesets in real-time.  
8. Speed up or slow down simulation generations.  
9. Cluster and populate the board interactively.

### Physics Engine:
10. Four-element physics simulation:
    - Unique interactions based on liquid and solid properties.
    - Gravity effects and water velocity calculations.  
11. Elemental behaviors:
    - Salt dissolution.
    - Floatability dynamics.  
12. Particle system algorithm:
    - Individual particle subclasses for six unique elements.  
13. Popularization algorithms for enhanced Game of Life interactions.

### Code Structure:
14. Board logic is modular and stored in static variables/methods within classes.  
15. Dedicated objects for:
    - Game of Life (`Game_Of_Life.py`)  
    - Wolfram automata (`Wolfram_Grid.py`)  
    - Physics elements (`Physics_CA.py`, `Element_Objects.py`)  

---

## Key Highlights

- **Interactive and educational**: Play with simulations to understand cellular automata principles.  
- **Customizable**: Modify rulesets and explore various outcomes.  
- **Physics Integration**: Realistic element interactions, including gravity and fluid dynamics.  

---

## Future Enhancements

- Additional cellular automata types.  
- More complex physics interactions.  
- Advanced visualization options.  

---

Explore the beauty of cellular automata and enjoy experimenting with this versatile engine! 🎮
