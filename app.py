# Store all our data in simple dictionaries and lists
robots = {}  # Dictionary to store robots
workers = {}  # Dictionary to store workers
tasks = []   # List to store tasks
products = [] # List to store products

def add_robot(robot_id):
    """Add a new robot with given ID"""
    if robot_id in robots:
        print(f"Robot {robot_id} already exists!")
        return False
    
    robots[robot_id] = {
        "status": "idle",
        "current_task": None
    }
    print(f"Added robot {robot_id} successfully!")
    return True

def add_worker(worker_id):
    """Add a new worker with given ID"""
    if worker_id in workers:
        print(f"Worker {worker_id} already exists!")
        return False
    
    workers[worker_id] = {
        "status": "idle",
        "current_task": None
    }
    print(f"Added worker {worker_id} successfully!")
    return True
#    Remove a robot if it s not workin
def remove_robot(robot_id):

    if robot_id not in robots:
        print(f"Robot {robot_id} not found!")
        return False
    
    if robots[robot_id]["status"] == "working":
        print(f"Cannot remove robot {robot_id} while it's working!")
        return False
    
    del robots[robot_id]
    print(f"Removed robot {robot_id} successfully!")
    return True
#    Remove a worker if they r not workin
def remove_worker(worker_id):

    if worker_id not in workers:
        print(f"Worker {worker_id} not found!")
        return False
    
    if workers[worker_id]["status"] == "working":
        print(f"Cannot remove worker {worker_id} while they're working!")
        return False
    
    del workers[worker_id]
    print(f"Removed worker {worker_id} successfully!")
    return True

#Assign a new task
def assign_task(task_name, robots_needed, workers_needed):
    
    available_robots = []
    available_workers = []
    
    for robot_id in robots:
        if robots[robot_id]["status"] == "idle":
            available_robots.append(robot_id)
    
    for worker_id in workers:
        if workers[worker_id]["status"] == "idle":
            available_workers.append(worker_id)
    
    if len(available_robots) < robots_needed:
        print(f"Not enough available robots! Need {robots_needed}, but only have {len(available_robots)}")
        return False
    
    if len(available_workers) < workers_needed:
        print(f"Not enough available workers! Need {workers_needed}, but only have {len(available_workers)}")
        return False
    
    new_task = {
        "name": task_name,
        "status": "in_progress",
        "robots": available_robots[:robots_needed],
        "workers": available_workers[:workers_needed]
    }
    
    for robot_id in new_task["robots"]:
        robots[robot_id]["status"] = "working"
        robots[robot_id]["current_task"] = task_name
    
    for worker_id in new_task["workers"]:
        workers[worker_id]["status"] = "working"
        workers[worker_id]["current_task"] = task_name
    
    tasks.append(new_task)
    print(f"Started task '{task_name}' successfully!")
    return True
# fun to show current status for robots and workers nd active tasks
def show_status():
    print("\n=== CURRENT STATUS ===")
    
    print("\nROBOTS:")
    for robot_id in robots:
        status = robots[robot_id]["status"]
        task = robots[robot_id]["current_task"] or "no task"
        print(f"Robot {robot_id}: {status} ({task})")
    
    print("\nWORKERS:")
    for worker_id in workers:
        status = workers[worker_id]["status"]
        task = workers[worker_id]["current_task"] or "no task"
        print(f"Worker {worker_id}: {status} ({task})")
    
    print("\nACTIVE TASKS:")
    if not tasks:
        print("No active tasks")
    for task in tasks:
        print(f"Task: {task['name']}")
        print(f"- Status: {task['status']}")
        print(f"- Robots assigned: {task['robots']}")
        print(f"- Workers assigned: {task['workers']}")
    
    print("\n===================")

def display_menu():
    # Display the main menu options
    print("\n=== ROBOTIC CELL MANAGEMENT SYSTEM ===")
    print("1. Add Robot")
    print("2. Add Worker")
    print("3. Remove Robot")
    print("4. Remove Worker")
    print("5. Assign New Task")
    print("6. Show Status")
    print("7. Exit")
    print("=====================================")

def main():
    while True:
        display_menu()
        choice = input("Enter your choice (1-7): ")
        
        if choice == "1":
            robot_id = input("Enter robot ID (e.g., R1): ")
            add_robot(robot_id)
        
        elif choice == "2":
            worker_id = input("Enter worker ID (e.g., W1): ")
            add_worker(worker_id)
        
        elif choice == "3":
            robot_id = input("Enter robot ID to remove: ")
            remove_robot(robot_id)
        
        elif choice == "4":
            worker_id = input("Enter worker ID to remove: ")
            remove_worker(worker_id)
        
        elif choice == "5":
            task_name = input("Enter task name (e.g., welding): ")
            robots_needed = int(input("Enter number of robots needed: "))
            workers_needed = int(input("Enter number of workers needed: "))
            assign_task(task_name, robots_needed, workers_needed)
        
        elif choice == "6":
            show_status()
        
        elif choice == "7":
            print("Thank you for using the Robotic Cell Management System!")
            break
        
        else:
            print("Invalid choice! Please select 1-7")

if __name__ == "__main__":
    main()