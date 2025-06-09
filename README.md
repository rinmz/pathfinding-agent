This project demonstrates a simple grid-based pathfinding system with per-goal path memory, visualized using Pygame. The system simulates an entity that learns and reuses the shortest path to randomly placed goals on a 2D grid. For each unique goal, the entity stores the shortest successful path and reuses it if the same goal appears again.

### Usage

Run the simulation with:
```sh
python main.py
```
- The entity will attempt to reach the goal.
- The console will display progress logs.
- The entity will reuse the shortest path if the same goal is encountered again.

### Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements.
