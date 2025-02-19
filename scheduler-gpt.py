#!/usr/bin/env python3
"""
scheduler-gpt.py

Team Members:
- Tho Pham
- Yauheni Khvashcheuski
- Aaron Nogues

Description:
    This script simulates process scheduling using three algorithms:
    1. FIFO (First In, First Out)
    2. Pre-emptive Shortest Job First (SJF)
    3. Round Robin (RR) with a configurable quantum.

    The code is organized into sections for each team member according to our iterative plan.
    Each section contains empty code blocks marked for iterative development.
    
Usage:
    scheduler-gpt.py <input file.in>
"""

import sys
import os

# =============================================================================
# SECTION: Tho Pham
# Tasks:
# - Develop and test the input parser.
# - Read and validate command-line arguments.
# - Parse the input file (processcount, runfor, use, quantum, process, end).
# - Implement error handling for missing parameters.
# - Create a Process data structure/class.
# Iterative Steps:
#   Iteration 1: Generate pseudocode and initial implementation.
#   Iteration 2: Integrate feedback and refine error handling.
#   Iteration 3: Finalize the parser and populate the process list.
# =============================================================================

class Process:
    def __init__(self, name, arrival, burst):
        """
        Initialize a process with the given parameters.
        Iterative development notes:
            - Iteration 1: Define basic attributes.
            - Iteration 2: Add attributes for simulation (e.g., remaining time, start_time, finish_time).
            - Iteration 3: Finalize initialization and any helper methods.
        """
        self.name = name
        self.arrival = int(arrival)
        self.burst = int(burst)
        self.remaining = int(burst)
        self.start_time = None
        self.finish_time = None
        self.wait_time = 0

    def __repr__(self):
        return f"Process({self.name}, arrival={self.arrival}, burst={self.burst})"

def parse_input_file(filename):
    """
    Parse the input file and extract:
    - process_list: List of Process instances.
    - runfor: Total time ticks.
    - algorithm: Scheduling algorithm to use ('fcfs', 'sjf', or 'rr').
    - quantum: Quantum value for Round Robin scheduling (if applicable).

    Iterative development notes:
        - Iteration 1: Write pseudocode and initial parser structure.
        - Iteration 2: Refine parsing logic and error handling.
        - Iteration 3: Finalize parser to correctly populate process_list.
    """
    process_list = []
    process_count = None
    runfor = None
    algorithm = None
    quantum = None

    valid_algorithms = {"fcfs", "sjf", "rr"}

    # (Tho Pham - Iteration 1): Implement file reading and token parsing.
    # Implemented error handling for missing/invalid parameters
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            
            for line in lines:
                parts = line.strip().split()
                if not parts:
                    continue  # Skip empty lines
                
                key = parts[0]
                
                if key == "processcount":
                    if len(parts) < 2:
                        raise ValueError("Missing value for 'processcount'.")
                    process_count = int(parts[1])
                
                elif key == "runfor":
                    if len(parts) < 2:
                        raise ValueError("Missing value for 'runfor'.")
                    runfor = int(parts[1])
                
                elif key == "use":
                    if len(parts) < 2:
                        raise ValueError("Missing scheduling algorithm.")
                    algorithm = parts[1]
                    if algorithm not in valid_algorithms:
                        raise ValueError(f"Invalid scheduling algorithm '{algorithm}'. Choose from {valid_algorithms}.")
                
                elif key == "quantum":
                    if len(parts) < 2:
                        raise ValueError("Missing value for 'quantum'.")
                    quantum = int(parts[1])
                    if quantum <= 0:
                        raise ValueError("Quantum must be a positive integer.")
                
                elif key == "process":
                    if len(parts) < 7:
                        raise ValueError("Malformed process entry. Expected format: process name arrival <value> burst <value>")
                    
                    name = parts[2]
                    try:
                        arrival = int(parts[4])
                        burst = int(parts[6])
                    except ValueError:
                        raise ValueError(f"Invalid arrival/burst value for process '{name}'. Expected integers.")
                    
                    process_list.append(Process(name, arrival, burst))

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Final validation for missing critical parameters
    if process_count is None:
        print("Error: 'processcount' is missing in the input file.")
        sys.exit(1)
    
    if runfor is None:
        print("Error: 'runfor' is missing in the input file.")
        sys.exit(1)
    
    if algorithm is None:
        print("Error: 'use' (scheduling algorithm) is missing in the input file.")
        sys.exit(1)
    
    if algorithm == "rr" and quantum is None:
        print("Error: 'quantum' value is required for Round Robin (RR) scheduling.")
        sys.exit(1)
    
    return process_count, process_list, runfor, algorithm, quantum

# =============================================================================
# SECTION: Yauheni Khvashcheuski
# Tasks:
# - Implement scheduling algorithms:
#   - FIFO scheduler
#   - Pre-emptive SJF scheduler
#   - Round Robin scheduler with configurable quantum
# Iterative Steps:
#   Iteration 1: Basic pseudocode and initial FIFO scheduler.
#   Iteration 2: Extend with pre-emptive SJF logic.
#   Iteration 3: Develop Round Robin scheduler.
#   Iteration 4: Test and refine all schedulers.
# =============================================================================

def fcfs_scheduler(process_list, runfor):
    """
    FIFO (First In, First Out) Scheduling Algorithm.
    
    Iterative development notes:
        - Iteration 1: Draft basic FIFO logic.
        # TODO: Implement scheduling based on process arrival order.
        - Iteration 2: Refine process selection and timing.
        - Iteration 3: Finalize scheduler logic.
    """
    # TODO (Yauheni - Iteration 1): Implement FIFO scheduling.
    pass

def sjf_scheduler(process_list, runfor):
    """
    Pre-emptive Shortest Job First (SJF) Scheduling Algorithm.
    
    Iterative development notes:
        - Iteration 1: Draft pseudocode for SJF scheduler.
        - Iteration 2: Incorporate remaining burst time and arrival conditions.
        - Iteration 3: Finalize pre-emptive logic.
    """
    # TODO (Yauheni - Iteration 1): Implement initial SJF logic.
    pass

def rr_scheduler(process_list, runfor, quantum):
    """
    Round Robin Scheduling Algorithm.
    
    Iterative development notes:
        - Iteration 1: Draft pseudocode for Round Robin scheduler.
        - Iteration 2: Integrate time-slice (quantum) parameter.
        - Iteration 3: Finalize Round Robin logic.
    """
    # TODO (Yauheni - Iteration 1): Implement initial Round Robin logic.
    pass

# =============================================================================
# SECTION: Aaron Nogues
# Tasks:
# - Implement simulation loop and metrics calculations:
#   - Time-tick loop handling arrivals, selections, completions, and idle periods.
#   - Log events at each time tick.
#   - Calculate turnaround, waiting, and response times.
# - Output formatting and file creation:
#   - Format the simulation output.
#   - Write the output to a .out file matching the input's base name.
# Iterative Steps:
#   Iteration 1: Develop pseudocode for the simulation loop and logging.
#   Iteration 2: Implement metric calculations and integrate with the simulation loop.
#   Iteration 3: Finalize output formatting and file writing.
#   Iteration 4: Test the complete simulation and adjust as needed.
# =============================================================================

def simulate_and_calculate(process_list, runfor, algorithm, quantum):
    """
    Run the simulation for the specified time ticks and calculate process metrics.
    
    Iterative development notes:
        - Iteration 1: Draft pseudocode for the simulation loop and event logging.
        - Iteration 2: Implement metric calculations and integrate scheduler functions.
        - Iteration 3: Finalize output formatting.
        - Iteration 4: Test simulation and adjust event logging/details.
    """
    # TODO (Aaron - Iteration 1): Set up the time-tick loop and initial logging.
    
    # Choose scheduler based on the algorithm specified.
    if algorithm == 'fcfs':
        fcfs_scheduler(process_list, runfor)
    elif algorithm == 'sjf':
        sjf_scheduler(process_list, runfor)
    elif algorithm == 'rr':
        if quantum is None:
            print("Error: Missing quantum parameter when use is 'rr'")
            sys.exit(1)
        rr_scheduler(process_list, runfor, quantum)
    else:
        print(f"Error: Unknown scheduling algorithm '{algorithm}'")
        sys.exit(1)
    
    # TODO (Aaron - Iteration 2): Calculate and log turnaround, waiting, and response times.
    
    # TODO (Aaron - Iteration 3): Format and write the output to the .out file.

# =============================================================================
# Main Function
# =============================================================================

def main():
    # Validate command-line arguments.
    if len(sys.argv) != 2:
        print("Usage: scheduler-gpt.py <input file>")
        sys.exit(1)
    
    input_filename = sys.argv[1]
    if not input_filename.endswith(".in"):
        print("Error: Input file must have a '.in' extension.")
        sys.exit(1)
    
    # Parse input file.
    process_list, runfor, algorithm, quantum = parse_input_file(input_filename)
    
    # Optionally print configuration details (e.g., number of processes, algorithm used).
    # TODO (Aaron or Tho): Add optional configuration logging if desired.
    
    # Run simulation and calculate metrics.
    simulate_and_calculate(process_list, runfor, algorithm, quantum)

if __name__ == "__main__":
    main()
