import time

# Global variables to store system data
robots = {}  # Dictionary to store robot IDs and their statuses
workers = {}  # Dictionary to store worker IDs and their statuses
tasks = []  # List to store tasks with details like type, duration, and assigned resources
products = []  # List to manage products and their assembly steps

# Functions

def add_robot(robot_id):
    # Add a robot to the system if it does not already exist
    if robot_id in robots:
        print(f"Robot {robot_id} already exists.")
        return
    robots[robot_id] = "idle"  # Set the robot's status to idle
    print(f"Robot {robot_id} added successfully.")

def remove_robot(robot_id):
    # Remove a robot from the system if it exists and is idle
    if robot_id not in robots:
        print(f"Robot {robot_id} does not exist.")
        return
    if robots[robot_id] != "idle":
        print(f"Cannot remove Robot {robot_id} as it is not idle.")
        return
    del robots[robot_id]  # Remove the robot from the dictionary
    print(f"Robot {robot_id} removed successfully.")

def add_worker(worker_id):
    # Add a worker to the system if they do not already exist
    if worker_id in workers:
        print(f"Worker {worker_id} already exists.")
        return
    workers[worker_id] = "idle"  # Set the worker's status to idle
    print(f"Worker {worker_id} added successfully.")

def remove_worker(worker_id):
    # Remove a worker from the system if they exist and are idle
    if worker_id not in workers:
        print(f"Worker {worker_id} does not exist.")
        return
    if workers[worker_id] != "idle":
        print(f"Cannot remove Worker {worker_id} as they are not idle.")
        return
    del workers[worker_id]  # Remove the worker from the dictionary
    print(f"Worker {worker_id} removed successfully.")

def assign_task(task_type, duration, required_robots=1, required_workers=1):
    # Assign a task to available robots and workers if resources are sufficient
    idle_robots = [r for r, status in robots.items() if status == "idle"]
    idle_workers = [w for w, status in workers.items() if status == "idle"]

    if len(idle_robots) < required_robots or len(idle_workers) < required_workers:
        print("Not enough idle robots or workers available to assign the task.")
        return

    assigned_robots = idle_robots[:required_robots]  # Allocate required robots
    assigned_workers = idle_workers[:required_workers]  # Allocate required workers

    for r in assigned_robots:
        robots[r] = "working"  # Update robot status to working
    for w in assigned_workers:
        workers[w] = "working"  # Update worker status to working

    # Create and append task details to the tasks list
    task = {
        "type": task_type,
        "duration": duration,
        "robots": assigned_robots,
        "workers": assigned_workers,
        "status": "in progress"
    }
    tasks.append(task)
    print(f"Task '{task_type}' assigned successfully.")

def monitor_tasks():
    # Monitor and update the status of ongoing tasks
    for task in tasks:
        if task["status"] == "in progress":
            time.sleep(task["duration"])  # Simulate task duration
            for r in task["robots"]:
                robots[r] = "idle"  # Set robot status to idle
            for w in task["workers"]:
                workers[w] = "idle"  # Set worker status to idle
            task["status"] = "completed"  # Mark task as completed
            print(f"Task '{task['type']}' completed.")

def assign_product(product_name, assembly_steps):
    # Assign a product for assembly and manage its steps
    product = {
        "name": product_name,
        "steps": assembly_steps,
        "status": "in progress"
    }
    products.append(product)  # Add the product to the list
    print(f"Product '{product_name}' assigned to the robotic cell.")

    # Execute each step in the product's assembly process
    for step in assembly_steps:
        print(f"Starting step: {step['name']}")
        assign_task(step['name'], step['duration'], step['robots'], step['workers'])
        monitor_tasks()

    product["status"] = "completed"  # Mark product assembly as completed
    print(f"Product '{product_name}' fully assembled.")

def display_status():
    # Display the current status of robots, workers, and tasks
    print("\nRobots:")
    for r, status in robots.items():
        print(f"  Robot {r}: {status}")

    print("\nWorkers:")
    for w, status in workers.items():
        print(f"  Worker {w}: {status}")

    print("\nTasks:")
    for t in tasks:
        print(f"  Task {t['type']}: {t['status']}")

# Example Usage
if __name__ == "__main__":
    # Add robots and workers to the system
    add_robot("R1")
    add_robot("R2")
    add_worker("W1")
    add_worker("W2")

    # Assign a product and its assembly steps
    assign_product("Widget", [
        {"name": "Welding", "duration": 2, "robots": 1, "workers": 1},
        {"name": "Assembling", "duration": 3, "robots": 1, "workers": 1},
        {"name": "Inspecting", "duration": 1, "robots": 1, "workers": 1}
    ])

    # Display the final status of the system
    display_status()
