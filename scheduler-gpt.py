#!/usr/bin/env python3
"""
scheduler-gpt.py

Team Members:
- Tho Pham
- Yauheni Khvashcheuski
- Aaron Nogues

Description:
    This script simulates process scheduling using three algorithms:
    1. FIFO (First-Come First-Served)
    2. Pre-emptive Shortest Job First (SJF)
    3. Round Robin (RR) with a configurable quantum.

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
# =============================================================================

class Process:
    def __init__(self, name, arrival, burst):
        """
        Initialize a process with the given parameters.
        """
        self.name = name
        self.arrival = int(arrival)
        self.burst = int(burst)
        self.remaining = int(burst)
        self.start_time = None
        self.finish_time = None
        # used only in SJF to track how many ticks have been executed
        self.executed_time = 0

    def __repr__(self):
        return f"Process({self.name}, arrival={self.arrival}, burst={self.burst})"


def parse_input_file(filename):
    """
    Parse the input file and extract:
    - process_list: List of Process instances.
    - runfor: Total time ticks.
    - algorithm: Scheduling algorithm to use ('fcfs', 'sjf', or 'rr').
    - quantum: Quantum value for Round Robin scheduling (if applicable).
    """
    process_list = []
    process_count = None
    runfor = None
    algorithm = None
    quantum = None

    valid_algorithms = {"fcfs", "sjf", "rr"}

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
                            "Malformed process entry. Expected format: process name <name> arrival <value> burst <value>")
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
# =============================================================================

def fcfs_scheduler(process_list, runfor, process_log):
    """
    FIFO (First-Come First-Served) Scheduler.
    Uses a copy of the original process order for final metric output.
    """
    original_order = list(process_list)
    sorted_processes = sorted(original_order, key=lambda p: p.arrival)
    log_event(process_log, f"{len(process_list):3} processes\nUsing First-Come First-Served")
    
    current_time = 0
    arrival_index = 0
    ready_queue = []
    running_process = None

    while current_time < runfor:
        events = []
        selected = False

        # Process arrivals.
        while arrival_index < len(sorted_processes) and sorted_processes[arrival_index].arrival == current_time:
            proc = sorted_processes[arrival_index]
            events.append(f"Time {current_time:3} : {proc.name} arrived")
            ready_queue.append(proc)
            arrival_index += 1

        # Check if the running process finishes at this tick.
        if running_process is not None and current_time == running_process.start_time + running_process.burst:
            running_process.finish_time = current_time
            events.append(f"Time {current_time:3} : {running_process.name} finished")
            running_process = None

        # If no process is running, select next process if available.
        if running_process is None and ready_queue:
            next_proc = ready_queue.pop(0)
            next_proc.start_time = current_time
            events.append(f"Time {current_time:3} : {next_proc.name} selected (burst {next_proc.burst:3})")
            running_process = next_proc
            selected = True

        if running_process is None and not selected:
            events.append(f"Time {current_time:3} : Idle")

        for event in events:
            log_event(process_log, event)
        current_time += 1

    log_event(process_log, f"Finished at time {runfor:3}\n")

    # Compute metrics using: wait = turnaround - burst
    for proc in original_order:
        turnaround = proc.finish_time - proc.arrival if proc.finish_time is not None else 0
        wait = turnaround - proc.burst
        response = proc.start_time - proc.arrival if proc.start_time is not None else 0
        log_event(process_log, f"{proc.name} wait {wait:3} turnaround {turnaround:3} response {response:3}")

    return original_order


def sjf_scheduler(process_list, runfor, process_log):
    """
    Pre-emptive Shortest Job First (SJF) Scheduler.
    Incorporates:
      - Finish event logging at the current tick using executed_time.
      - Preemption when a waiting process has a strictly shorter remaining time.
      - Preservation of original order for final metrics.
    """
    original_order = list(process_list)
    sorted_processes = sorted(original_order, key=lambda p: p.arrival)
    log_event(process_log, f"{len(process_list):3} processes\nUsing preemptive Shortest Job First")
    
    current_time = 0
    arrival_index = 0
    ready_queue = []
    running_process = None

    while current_time < runfor:
        events = []

        # Process arrivals.
        while arrival_index < len(sorted_processes) and sorted_processes[arrival_index].arrival == current_time:
            proc = sorted_processes[arrival_index]
            events.append(f"Time {current_time:3} : {proc.name} arrived")
            ready_queue.append(proc)
            arrival_index += 1

        # Check if the running process finishes at this tick.
        if running_process is not None and running_process.executed_time == running_process.burst:
            running_process.finish_time = current_time
            events.append(f"Time {current_time:3} : {running_process.name} finished")
            running_process = None

        # Preemption check: if a waiting process has a shorter remaining burst.
        if running_process is not None and ready_queue:
            candidate = min(ready_queue, key=lambda p: p.remaining)
            if candidate.remaining < running_process.remaining:
                ready_queue.append(running_process)
                running_process = candidate
                ready_queue.remove(candidate)
                if running_process.start_time is None:
                    running_process.start_time = current_time
                events.append(f"Time {current_time:3} : {running_process.name} selected (burst {running_process.remaining:3})")

        # If no process is running, select next process.
        if running_process is None and ready_queue:
            running_process = min(ready_queue, key=lambda p: p.remaining)
            ready_queue.remove(running_process)
            if running_process.start_time is None:
                running_process.start_time = current_time
            events.append(f"Time {current_time:3} : {running_process.name} selected (burst {running_process.remaining:3})")

        # Execute one tick.
        if running_process is not None:
            running_process.remaining -= 1
            running_process.executed_time += 1
        else:
            events.append(f"Time {current_time:3} : Idle")

        for event in events:
            log_event(process_log, event)
        current_time += 1

    log_event(process_log, f"Finished at time {runfor:3}\n")

    # Compute metrics using: wait = turnaround - burst
    for proc in original_order:
        turnaround = proc.finish_time - proc.arrival if proc.finish_time is not None else 0
        wait = turnaround - proc.burst
        response = proc.start_time - proc.arrival if proc.start_time is not None else 0
        log_event(process_log, f"{proc.name} wait {wait:3} turnaround {turnaround:3} response {response:3}")

    return original_order


def rr_scheduler(process_list, runfor, quantum, process_log):
    """
    Round Robin Scheduler.
    (Assumed to be working correctly.)
    """
    original_process_list = list(process_list)
    sorted_processes = sorted(process_list, key=lambda p: p.arrival)
    
    log_event(process_log, f"{len(original_process_list):3} processes")
    log_event(process_log, "Using Round-Robin")
    log_event(process_log, f"Quantum {quantum:3}\n")
    
    current_time = 0
    arrival_index = 0
    ready_queue = []
    running_process = None
    time_slice_counter = 0
    
    while current_time < runfor:
        while arrival_index < len(sorted_processes) and sorted_processes[arrival_index].arrival == current_time:
            proc = sorted_processes[arrival_index]
            log_event(process_log, f"Time {current_time:3} : {proc.name} arrived")
            ready_queue.append(proc)
            arrival_index += 1
        
        if running_process is not None:
            running_process.remaining -= 1
            time_slice_counter += 1
            
            if running_process.remaining == 0:
                log_event(process_log, f"Time {current_time:3} : {running_process.name} finished")
                running_process.finish_time = current_time
                running_process = None
                time_slice_counter = 0
            elif time_slice_counter == quantum:
                ready_queue.append(running_process)
                running_process = None
                time_slice_counter = 0
        
        if running_process is None:
            if ready_queue:
                running_process = ready_queue.pop(0)
                if running_process.start_time is None:
                    running_process.start_time = current_time
                log_event(process_log, f"Time {current_time:3} : {running_process.name} selected (burst {running_process.remaining:3})")
            else:
                log_event(process_log, f"Time {current_time:3} : Idle")
        
        current_time += 1
    
    log_event(process_log, f"Finished at time {runfor:3}\n")
    
    for proc in original_process_list:
        turnaround = proc.finish_time - proc.arrival if proc.finish_time is not None else 0
        wait = turnaround - proc.burst
        response = proc.start_time - proc.arrival if proc.start_time is not None else 0
        log_event(process_log, f"{proc.name} wait {wait:3} turnaround {turnaround:3} response {response:3}")
    
    return original_process_list

# =============================================================================
# SECTION: Aaron Nogues
# Tasks:
# - Implement simulation loop and metrics calculations.
# - Output formatting and file creation.
# =============================================================================

def simulate_and_calculate(process_list, runfor, algorithm, quantum, process_log):
    if algorithm == 'fcfs':
        fcfs_scheduler(process_list, runfor, process_log)
    elif algorithm == 'sjf':
        sjf_scheduler(process_list, runfor, process_log)
    elif algorithm == 'rr':
        if quantum is None:
            print("Error: Missing quantum parameter when use is 'rr'")
            sys.exit(1)
        rr_scheduler(process_list, runfor, quantum, process_log)
    else:
        print(f"Error: Unknown scheduling algorithm '{algorithm}'")
        sys.exit(1)


def log_event(process_log, event):
    process_log.append(f"{event}")


def write_output_file(process_log, input_filename):
    output_filename = input_filename.replace(".in", ".generated.out")
    with open(output_filename, "w") as f:
        for log in process_log:
            f.write(log + "\n")


def main():
    input_filename = ""
    process_log = []

    if len(sys.argv) != 2:
        print("Usage: scheduler-gpt.py <input file>")
        sys.exit(1)

    input_filename = sys.argv[1]
    if not input_filename.endswith(".in"):
        print("Error: Input file must have a '.in' extension.")
        sys.exit(1)

    _, process_list, runfor, algorithm, quantum = parse_input_file(input_filename)
    simulate_and_calculate(process_list, runfor, algorithm, quantum, process_log)
    write_output_file(process_log, input_filename)


if __name__ == "__main__":
    main()
