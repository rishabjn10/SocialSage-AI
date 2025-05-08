import datetime
from crewai import Task
import os

LOG_DIR = None

def log_step_details(task: Task):
    """
    Callback function to log verbose details of each step within a task.
    This function is registered with the Crew's step_callbacks.
    It captures the agent's thought process and other step details.
    Includes debugging prints to diagnose logging issues.
    """
    print("\n--- log_step_details function called ---") # Debug print
    # print(f"Received step data: {step}") # Debug print
    print(f"Received task data (description): {task.description}") # Debug print


    global LOG_DIR
    # Ensure log directory is created only once per crew run
    if LOG_DIR is None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        LOG_DIR = f"crew_logs/{timestamp}"
        try:
            os.makedirs(LOG_DIR, exist_ok=True)
            print(f"--- Created log directory for this run: {LOG_DIR} ---") # Debug print
        except OSError as e:
            print(f"Error creating log directory {LOG_DIR}: {e}") # Debug print
            # If directory creation fails, we can't write logs, so return.
            return


    # Use task description as a base for the log file name.
    # Sanitize the description to be safe for a filename.
    task_identifier = task.name
    # Simple sanitization: replace non-alphanumeric/underscore/hyphen with underscore
    safe_task_identifier = "".join([c if c.isalnum() or c in ('-', '_') else '_' for c in task_identifier]).rstrip()
    safe_task_identifier = safe_task_identifier[:50].strip('_') # Truncate and remove trailing underscores

    # Handle empty or invalid task identifiers after sanitization
    if not safe_task_identifier:
        safe_task_identifier = f"unknown_task_{datetime.datetime.now().strftime('%f')}" # Use a unique fallback

    log_file_path = os.path.join(LOG_DIR, f"{safe_task_identifier}.log")
    print(f"Log file path: {log_file_path}") # Debug print

    # Extract verbose details from the step dictionary.
    # The 'thought' key typically contains the agent's reasoning process.
    tool_output = task.raw
    task_expected_output = task.expected_output
    step_description = task.description # This might be the description of the current step (e.g., 'Thinking', 'Tool Use')
    agent_name = task.agent # Get agent name if available

    try:
        # Append the step details to the task's log file
        with open(log_file_path, "a") as f: # Use "a" for append mode to add each step's details
            f.write(f"--- Step Details for Task: {task_identifier} ---\n")
            f.write(f"Agent: {agent_name}\n")
            f.write(f"Step Description: {step_description}\n")
            f.write(f"Expected output: {task_expected_output}\n")
            if tool_output:
                 f.write(f"Tool Output:\n{tool_output}\n") # Added newline for readability
            f.write("-" * 40 + "\n\n") # Separator for steps, made longer

        print(f"--- Successfully logged step for task '{task_identifier}' to {log_file_path} ---") # Debug print

    except IOError as e:
        print(f"Error writing to log file {log_file_path}: {e}") # Debug print
    except Exception as e:
        print(f"An unexpected error occurred during logging: {e}") # Debug print