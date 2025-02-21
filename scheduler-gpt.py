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
                        raise ValueError(
                            f"Invalid scheduling algorithm '{algorithm}'. Choose from {valid_algorithms}.")

                elif key == "quantum":
                    if len(parts) < 2:
                        raise ValueError("Missing value for 'quantum'.")
                    quantum = int(parts[1])
                    if quantum <= 0:
                        raise ValueError("Quantum must be a positive integer.")

                elif key == "process":
                    if len(parts) < 7:
                        raise ValueError(
                            "Malformed process entry. Expected format: process name arrival <value> burst <value>")

                    name = parts[2]
                    try:
                        arrival = int(parts[4])
                        burst = int(parts[6])
                    except ValueError:
                        raise ValueError(
                            f"Invalid arrival/burst value for process '{name}'. Expected integers.")

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
    FIFO (First-Come First-Served) Scheduler - Finalized with Timeline Simulation

    Expected input example:
        processcount 2	# Read 2 processes
        runfor 20	# Run for 20 time units
        use fcfs
        process name P1 arrival 0 burst 5
        process name P2 arrival 7 burst 9
        end

    Expected output:
          2 processes
    Using First-Come First-Served
    Time   0 : P1 arrived
    Time   0 : P1 selected (burst   5)
    Time   5 : P1 finished
    Time   5 : Idle
    Time   6 : Idle
    Time   7 : P2 arrived
    Time   7 : P2 selected (burst   9)
    Time  16 : P2 finished
    Time  16 : Idle
    Time  17 : Idle
    Time  18 : Idle
    Time  19 : Idle
    Finished at time  20

    P1 wait   0 turnaround   5 response   0
    P2 wait   0 turnaround   9 response   0
    """
    # Sort processes in arrival order.
    sorted_processes = sorted(process_list, key=lambda p: p.arrival)

    # Print header.
    print(f"  {len(process_list)} processes")
    print("Using First-Come First-Served")

    # List of processes that have arrived and are waiting.
    ready_queue = []
    current_time = 0       # Simulation clock.
    arrival_index = 0      # Index for processes sorted by arrival.
    running_process = None  # Currently executing process.

    # Simulation loop: iterate through each time tick.
    while current_time < runfor:
        events = []  # Collect events to print for this tick.
        selected = False

        # Check for process arrivals at the current time.
        while (arrival_index < len(sorted_processes) and
               sorted_processes[arrival_index].arrival == current_time):
            proc = sorted_processes[arrival_index]
            events.append(f"Time {current_time:3} : {proc.name} arrived")
            ready_queue.append(proc)
            arrival_index += 1

        # If a process is running, check if it finishes at the current time.
        if running_process is not None and current_time == running_process.start_time + running_process.burst:
            running_process.finish_time = current_time
            events.append(
                f"Time {current_time:3} : {running_process.name} finished")
            # Calculate waiting time (for FIFO, response equals wait time).
            running_process.wait_time = running_process.start_time - running_process.arrival
            running_process = None

        # If the CPU is idle and there are processes waiting, select the next one.
        if running_process is None and ready_queue:
            next_proc = ready_queue.pop(0)
            next_proc.start_time = current_time
            events.append(
                f"Time {current_time:3} : {next_proc.name} selected (burst {next_proc.burst:3})")
            running_process = next_proc
            selected = True

        # If no process is running and no selection occurred, print an idle event.
        if running_process is None and not selected:
            events.append(f"Time {current_time:3} : Idle")

        # Print all events scheduled for the current tick.
        for event in events:
            print(event)

        current_time += 1

    # After the simulation, print the finishing time.
    print(f"Finished at time {runfor:3}")

    # Print metrics for each process.
    for proc in sorted_processes:
        turnaround = proc.finish_time - proc.arrival if proc.finish_time is not None else 0
        response = proc.start_time - proc.arrival if proc.start_time is not None else 0
        print(
            f"{proc.name} wait {proc.wait_time:3} turnaround {turnaround:3} response {response:3}")


def sjf_scheduler(process_list, runfor):
    """
    Pre-emptive Shortest Job First (SJF) Scheduler - Finalized Version:

    This scheduler simulates each time tick from 0 to runfor-1. At each tick:
      - Processes arriving at that time are added to the ready queue.
      - If a process is running, the scheduler checks if any waiting process has a
        shorter remaining burst time. If so, the running process is pre-empted.
      - If no process is running and the ready queue is non-empty, the process with
        the shortest remaining burst is selected.
      - The selected process runs for one time unit.
      - When a process's remaining burst reaches zero, it is marked as finished.

    Timeline events (arrival, selection, finish, idle) are printed at each tick.
    After the simulation, process metrics are printed.

    Expected timeline for a sample input:
        2 processes
    Using preemptive Shortest Job First
    Time   0 : P1 arrived
    Time   0 : P1 selected (burst   5)
    Time   5 : P1 finished
    Time   5 : Idle
    Time   6 : Idle
    Time   7 : P2 arrived
    Time   7 : P2 selected (burst   9)
    Time  16 : P2 finished
    Time  16 : Idle
    Time  17 : Idle
    Time  18 : Idle
    Time  19 : Idle
    Finished at time  20

    P1 wait   0 turnaround   5 response   0
    P2 wait   0 turnaround   9 response   0
    """
    # Sort processes by arrival time for a consistent simulation order.
    sorted_processes = sorted(process_list, key=lambda p: p.arrival)

    # Print header information.
    print(f"  {len(process_list)} processes")
    print("Using preemptive Shortest Job First")

    current_time = 0
    arrival_index = 0
    ready_queue = []       # Processes that have arrived and are waiting.
    running_process = None  # Currently running process.

    # Simulation loop: one tick at a time.
    while current_time < runfor:
        events = []  # Collect events to print for this tick.

        # a. Process Arrivals.
        while (arrival_index < len(sorted_processes) and
               sorted_processes[arrival_index].arrival == current_time):
            proc = sorted_processes[arrival_index]
            events.append(f"Time {current_time:3} : {proc.name} arrived")
            ready_queue.append(proc)
            arrival_index += 1

        # b. Pre-emption check:
        if running_process is not None and ready_queue:
            # Find the process in ready_queue with the smallest remaining burst.
            candidate = min(ready_queue, key=lambda p: p.remaining)
            if candidate.remaining < running_process.remaining:
                # Preempt the running process.
                ready_queue.append(running_process)
                running_process = candidate
                ready_queue.remove(candidate)
                # If this is the process's first run, record its start time.
                if running_process.start_time is None:
                    running_process.start_time = current_time
                events.append(
                    f"Time {current_time:3} : {running_process.name} selected (burst {running_process.remaining:3})")

        # c. Process selection:
        if running_process is None and ready_queue:
            running_process = min(ready_queue, key=lambda p: p.remaining)
            ready_queue.remove(running_process)
            if running_process.start_time is None:
                running_process.start_time = current_time
            events.append(
                f"Time {current_time:3} : {running_process.name} selected (burst {running_process.remaining:3})")

        # d. Execution:
        if running_process is not None:
            # Run the current process for one time unit.
            running_process.remaining -= 1
            # Check if the process finishes at this tick.
            if running_process.remaining == 0:
                running_process.finish_time = current_time + 1
                events.append(
                    f"Time {current_time+1:3} : {running_process.name} finished")
                # Calculate waiting time (first selection minus arrival time).
                running_process.wait_time = running_process.start_time - running_process.arrival
                running_process = None
        else:
            # If no process is running, record an idle tick.
            events.append(f"Time {current_time:3} : Idle")

        # Print all events for the current time tick.
        for event in events:
            print(event)

        current_time += 1

    # End-of-simulation summary.
    print(f"Finished at time {runfor:3}")

    # Print metrics for each process.
    for proc in sorted_processes:
        turnaround = proc.finish_time - proc.arrival if proc.finish_time is not None else 0
        response = proc.start_time - proc.arrival if proc.start_time is not None else 0
        print(
            f"{proc.name} wait {proc.wait_time:3} turnaround {turnaround:3} response {response:3}")


def rr_scheduler(process_list, runfor, quantum):
    """
    Round Robin Scheduler - Finalized Version:

    This scheduler simulates each time tick from 0 to runfor-1. At each tick:
      - New arrivals are added to a ready queue.
      - If the CPU is idle, the next process is selected from the ready queue.
      - The selected process runs for one time unit.
      - If the process exhausts its time slice (quantum) before finishing, it is requeued.
      - When a process finishes, its finish time is recorded and a finish event is logged.

    Expected example output:
      2 processes
      Using Round-Robin
      Quantum   2

      Time   0 : P2 arrived
      Time   0 : P2 selected (burst   9)
      Time   2 : P2 selected (burst   7)
      Time   3 : P1 arrived
      Time   4 : P1 selected (burst   5)
      Time   6 : P2 selected (burst   5)
      Time   8 : P1 selected (burst   3)
      Time  10 : P2 selected (burst   3)
      Time  12 : P1 selected (burst   1)
      Time  13 : P1 finished
      Time  13 : P2 selected (burst   1)
      Time  14 : P2 finished
      Time  14 : Idle
      Finished at time  15

      P1 wait   5 turnaround  10 response   1
      P2 wait   5 turnaround  14 response   0
    """
    # Sort processes by arrival time.
    sorted_processes = sorted(process_list, key=lambda p: p.arrival)

    # Print header information.
    print(f"  {len(process_list)} processes")
    print("Using Round-Robin")
    print(f"Quantum {quantum:4}\n")

    current_time = 0
    arrival_index = 0
    ready_queue = []
    running_process = None
    # Counts how many time units the current process has run.
    time_slice_counter = 0

    # Simulation loop: tick-by-tick.
    while current_time < runfor:
        events = []

        # Process Arrivals: add processes arriving at the current time.
        while (arrival_index < len(sorted_processes) and
               sorted_processes[arrival_index].arrival == current_time):
            proc = sorted_processes[arrival_index]
            events.append(f"Time {current_time:3} : {proc.name} arrived")
            ready_queue.append(proc)
            arrival_index += 1

        # Process Selection: if no process is running, select the next one.
        if running_process is None and ready_queue:
            running_process = ready_queue.pop(0)
            # Record start time only the first time the process is selected.
            if running_process.start_time is None:
                running_process.start_time = current_time
            time_slice_counter = 0  # Reset the time slice counter.
            events.append(
                f"Time {current_time:3} : {running_process.name} selected (burst {running_process.remaining:3})")

        # Execution: if a process is running, run it for one time unit.
        if running_process is not None:
            running_process.remaining -= 1
            time_slice_counter += 1

            # If the process finishes execution.
            if running_process.remaining == 0:
                running_process.finish_time = current_time + 1
                events.append(
                    f"Time {current_time+1:3} : {running_process.name} finished")
                # Reset the running process and time slice.
                running_process = None
                time_slice_counter = 0
            # If the process's time slice (quantum) expires but it is not finished.
            elif time_slice_counter == quantum:
                # Requeue the process for later execution.
                ready_queue.append(running_process)
                running_process = None
                time_slice_counter = 0

        # Idle: if no process is running and no process is in the ready queue.
        if running_process is None and not ready_queue:
            events.append(f"Time {current_time:3} : Idle")

        # Print all events for this tick.
        for event in events:
            print(event)

        current_time += 1

    # End-of-simulation summary.
    print(f"Finished at time {runfor:3}\n")

    # Calculate and print metrics for each process.
    for proc in sorted_processes:
        turnaround = proc.finish_time - proc.arrival if proc.finish_time is not None else 0
        # For Round Robin, waiting time is turnaround minus the original burst.
        wait = turnaround - proc.burst
        response = proc.start_time - proc.arrival if proc.start_time is not None else 0
        print(
            f"{proc.name} wait {wait:3} turnaround {turnaround:3} response {response:3}")


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
