import random
import math
import numpy as np
from swarmy.actuation import Actuation

ROBOT_TRACK_WIDTH_L = 50.0
SIMULATION_DT = 1.0


class GridCellTracker:
    """Tracks unique visited grid cells for fitness evaluation."""

    def __init__(self, world_width, world_height, cell_size=5.0):
        self.cell_size = cell_size
        self.grid = set()
        self.max_x_cell = math.ceil(world_width / cell_size)
        self.max_y_cell = math.ceil(world_height / cell_size)
        self.world_width = world_width
        self.world_height = world_height

    def update(self, x, y):
        """Adds the current cell coordinate (ix, iy) to the set of visited cells."""
        ix = int(x / self.cell_size)
        iy = int(y / self.cell_size)
        # Check if outside of frame
        if x < self.world_width and y < self.world_height:
            ix = np.clip(ix, 0, self.max_x_cell - 1)
            iy = np.clip(iy, 0, self.max_y_cell - 1)
            self.grid.add((ix, iy))

    def get_fitness(self):
        """Returns the number of unique visited cells."""
        return len(self.grid)


class MyController(Actuation):
    EVALUATION_STEPS = 1000
    MUTATION_RATE = 0.2

    # Frequency of visualization
    VISUAL_SKIP_CYCLES = 100

    # Range for initial random parameters
    PARAM_RANGE = (0, 1.0)

    # Maximum allowed wheel velocity
    MAX_V = 1.0

    def __init__(self, agent, config):
        super().__init__(agent)
        self.config = config
        self.init_pos = True

        self.current_genome = self._initialize_genome()
        self.best_genome = np.copy(self.current_genome)
        self.best_fitness = -1

        self.steps_counter = 0

        # Fitness tracker setup
        world_w = self.config['world_width']
        world_h = self.config['world_height']
        self.grid_tracker = GridCellTracker(world_w, world_h, cell_size=5.0)

        self.generation_count = 1

    def _initialize_genome(self):
        """Initializes a random genome within the specified range."""
        low, high = self.PARAM_RANGE
        return np.random.uniform(low, high, 6)

    def _mutate_genome(self, genome):
        """Applies Gaussian mutation to the genome and clips the result."""
        mutation = np.random.normal(0, self.MUTATION_RATE, size=6)
        mutated_genome = genome + mutation

        for i in range(len(mutated_genome)):
            if i%2: mutated_genome[i] = np.clip(mutated_genome[i], -self.MAX_V/4, self.MAX_V/4)
            else: mutated_genome[i] = np.clip(mutated_genome[i], -self.MAX_V, self.MAX_V)

        return mutated_genome

    def _reset_evaluation_state(self):
        """Resets robot position and fitness tracker for a new run."""
        start_x = self.config['world_width'] / 5
        start_y = self.config['world_height'] / 5
        start_heading = 90.0
        self.agent.set_position(start_x, start_y, int(start_heading))

        self.steps_counter = 0
        world_w = self.config['world_width']
        world_h = self.config['world_height']
        self.grid_tracker = GridCellTracker(world_w, world_h, cell_size=5.0)
        self.init_pos = False

    def _evaluate_and_evolve(self):
        """Handles the end-of-generation comparison and mutation."""
        current_fitness = self.grid_tracker.get_fitness()

        print(f"\n--- Generation {self.generation_count} Complete ---")
        print(f"Fitness Score: {current_fitness}")

        if current_fitness >= self.best_fitness:
            # Success: New peak found (or equal)
            print(f"New BEST fitness ({current_fitness} >= {self.best_fitness})! Accepting new genome.")
            self.best_fitness = current_fitness
            self.best_genome = np.copy(self.current_genome)
        else:
            # Failure: Fitness decreased
            print(f"Fitness did not improve ({current_fitness} < {self.best_fitness}). Backtracking to best.")
            self.current_genome = np.copy(self.best_genome)

        self.generation_count += 1

        self.current_genome = self._mutate_genome(self.best_genome)

        # Start the next evaluation
        self._reset_evaluation_state()
        print(f"--- Starting Generation {self.generation_count} ---")
        print(f"Next Candidate Genome: {self.current_genome}")

    def _perform_single_step(self):
        """Performs one step of perception, actuation, and kinematics."""

        try:
            sensor_values = self.agent.get_perception()[1]
        except:
            sensor_values = self.agent.get_perception()

        sl, sm, sr = sensor_values[0], sensor_values[1], sensor_values[2]

        m0, c0, m1, c1, m2, c2 = self.current_genome

        vl = m0 * sl + c0
        vr = m1 * sr + c1 + m2 * sm + c2

        vl = np.clip(vl, -self.MAX_V, self.MAX_V)
        vr = np.clip(vr, -self.MAX_V, self.MAX_V)

        current_x, current_y, current_heading = self.agent.get_position()

        linear_v = (vr + vl) / 2.0
        angular_v = (vr - vl) / ROBOT_TRACK_WIDTH_L

        new_heading = current_heading + angular_v * SIMULATION_DT
        new_heading = new_heading % 360.0

        heading_rad = math.radians(current_heading)

        new_x = current_x + linear_v * math.sin(heading_rad) * SIMULATION_DT
        new_y = current_y + linear_v * math.cos(heading_rad) * SIMULATION_DT

        self.agent.set_position(new_x, new_y, int(new_heading))

        self.grid_tracker.update(new_x, new_y)

        self.steps_counter += 1

    def controller(self):

        # Initial setup on first call
        if self.init_pos:
            print(f"--- Starting Hill Climber (Generation 1) ---")
            print(f"Initial Genome: {self.current_genome}")
            self._reset_evaluation_state()
            self.init_pos = False

        if self.steps_counter == self.EVALUATION_STEPS:
            # evaluate result
            self._evaluate_and_evolve()

        # Show each 100th generation
        is_visual = (self.generation_count % self.VISUAL_SKIP_CYCLES)

        steps_to_execute = 1
        if not is_visual:
            if self.steps_counter == 0:
                steps_to_execute = self.EVALUATION_STEPS

        for i in range(steps_to_execute):
            self._perform_single_step()

            if self.steps_counter == self.EVALUATION_STEPS and steps_to_execute > 1:
                self._evaluate_and_evolve()
                return

    def torus(self):
        return