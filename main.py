"""
Grid-based pathfinding agent with per-goal path memory and Pygame visualization.

This module implements a simple agent that learns and reuses the shortest path to a randomly
placed goal on a 2D grid. For each unique goal, the agent stores the shortest successful path
and reuses it if the same goal appears again. Visualization is provided via Pygame.

Author: Reis Inanmaz
"""

import pygame
import random
import logging
from typing import List, Tuple, Dict

# Configure logging: Only message, no date or level
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)

# Screen and grid configuration
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
GRID_SIZE = 10
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE

# Colors (R, G, B)
COLOR_BG = (240, 240, 240)
COLOR_GRID = (100, 100, 100)
COLOR_AGENT = (54, 12, 124)
COLOR_GOAL = (90, 200, 100)

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# State variables
position: List[int] = [0, 0]  # Current position of the entity
goal: List[int] = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]

# Stores the shortest successful path for each goal position
goal_paths: Dict[Tuple[int, int], List[str]] = {}

def draw_grid() -> None:
    """Draws the grid lines on the screen."""
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, COLOR_GRID, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, COLOR_GRID, (0, y), (SCREEN_WIDTH, y))

def draw_entities() -> None:
    """Draws the entity and goal on the grid."""
    pygame.draw.rect(
        screen,
        COLOR_AGENT,
        (position[0] * CELL_SIZE, position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    )
    pygame.draw.rect(
        screen,
        COLOR_GOAL,
        (goal[0] * CELL_SIZE, goal[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    )

def manhattan_distance(pos1: List[int], pos2: List[int]) -> int:
    """
    Calculates the Manhattan distance between two positions.

    Args:
        pos1: [x, y] position 1.
        pos2: [x, y] position 2.

    Returns:
        int: Manhattan distance.
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def random_direction() -> str:
    """Returns a random direction as a string."""
    return random.choice(['up', 'down', 'left', 'right'])

def move_position(pos: List[int], direction: str) -> None:
    """
    Moves the position in the specified direction if within grid bounds.

    Args:
        pos: [x, y] position to move.
        direction: Direction to move ('up', 'down', 'left', 'right').
    """
    if direction == 'up' and pos[1] > 0:
        pos[1] -= 1
    elif direction == 'down' and pos[1] < GRID_SIZE - 1:
        pos[1] += 1
    elif direction == 'left' and pos[0] > 0:
        pos[0] -= 1
    elif direction == 'right' and pos[0] < GRID_SIZE - 1:
        pos[0] += 1

def find_successful_path(goal_pos: List[int], max_steps: int = 100) -> None:
    """
    Attempts to find a successful path from [0, 0] to the goal using random moves.

    Args:
        goal_pos: [x, y] goal position.
        max_steps: Maximum number of steps per episode.
    """
    trial_pos = [0, 0]
    path: List[str] = []
    for _ in range(max_steps):
        direction = random_direction()
        path.append(direction)
        move_position(trial_pos, direction)
        if trial_pos == goal_pos:
            key = tuple(goal_pos)
            if key not in goal_paths or len(path) < len(goal_paths[key]):
                goal_paths[key] = path.copy()
            # logging.info("Found path to goal %s in %d steps.", key, len(path))
            break

def move_with_memory() -> None:
    """
    Moves the entity using the stored successful path for the current goal if available.
    Otherwise, moves randomly.
    """
    key = tuple(goal)
    if key in goal_paths:
        best_path = goal_paths[key]
        if move_with_memory.step < len(best_path):
            direction = best_path[move_with_memory.step]
            move_with_memory.step += 1
        else:
            direction = random_direction()
    else:
        direction = random_direction()
    move_position(position, direction)

move_with_memory.step = 0

def reset_position_and_goal() -> None:
    """Resets the entity to the start and places the goal at a new random position."""
    position[0], position[1] = 0, 0
    goal[0], goal[1] = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
    move_with_memory.step = 0

def ensure_path_for_goal(goal_pos: List[int]) -> None:
    """
    Ensures there is a successful path for the given goal by running random episodes.

    Args:
        goal_pos: [x, y] goal position.
    """
    for _ in range(1000):
        find_successful_path(goal_pos)
        if tuple(goal_pos) in goal_paths:
            break

def main() -> None:
    """Main loop for the pathfinding simulation."""
    step_count = 0
    episode_count = 0

    ensure_path_for_goal(goal)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        prev_distance = manhattan_distance(position, goal)
        move_with_memory()
        new_distance = manhattan_distance(position, goal)
        step_count += 1

        # Reward logic for debugging
        if new_distance < prev_distance:
            reward = 1
        elif new_distance > prev_distance:
            reward = -1
        else:
            reward = 0
        logging.debug("Step reward: %d", reward)

        # Goal reached check
        if position == goal:
            episode_count += 1
            logging.info(
                "Goal reached at %s in %d steps. Total episodes: %d",
                tuple(goal), step_count, episode_count
            )
            reset_position_and_goal()
            step_count = 0
            ensure_path_for_goal(goal)

        # Drawing
        screen.fill(COLOR_BG)
        draw_grid()
        draw_entities()
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()