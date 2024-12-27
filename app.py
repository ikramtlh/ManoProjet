from datetime import datetime, timedelta

# Initialize the robotic cell with dictionaries for robots, workers, and tasks
robots = {}  # Store robots with their IDs and statuses
workers = {}  # Store workers with their IDs and statuses
products = {} # Store products with their assembly steps

def add_robot():
    """Add a new robot to the robotic cell with a unique ID"""
    robot_id = len(robots) + 1
    robots[robot_id] = {'status': 'idle'}  # Status: idle, working
    print(f"Robot {robot_id} added successfully.")

def remove_robot(robot_id):
    """Remove a robot from the robotic cell if it's not engaged in a task"""
    if robot_id not in robots:
        print(f"Error: Robot {robot_id} does not exist.")
        return
    if robots[robot_id]['status'] != 'idle':
        print(f"Error: Cannot remove Robot {robot_id} while engaged in a task.")
        return
    del robots[robot_id]
    print(f"Robot {robot_id} removed successfully.")

def add_worker():
    """Add a new worker to the robotic cell with a unique ID"""
    worker_id = len(workers) + 1
    workers[worker_id] = {'status': 'idle'}  # Status: idle, working
    print(f"Worker {worker_id} added successfully.")

def remove_worker(worker_id):
    """Remove a worker from the robotic cell if they're not engaged in a task"""
    if worker_id not in workers:
        print(f"Error: Worker {worker_id} does not exist.")
        return
    if workers[worker_id]['status'] != 'idle':
        print(f"Error: Cannot remove Worker {worker_id} while engaged in a task.")
        return
    del workers[worker_id]
    print(f"Worker {worker_id} removed successfully.")

def assign_product():
    """Set up a new product to be assembled with its required steps"""
    product_name = input("Enter product name: ")
    if product_name in products:
        print(f"Error: Product {product_name} already exists.")
        return
    
    num_steps = int(input("Enter number of assembly steps: "))
    steps = []
    
    for i in range(num_steps):
        print(f"\nStep {i+1} details:")
        step = {
            'name': input("Enter step name (e.g., welding, assembling, testing): "),
            'robots_required': int(input("Number of robots required: ")),
            'workers_required': int(input("Number of workers required: ")),
            'duration': int(input("Enter step duration (seconds): ")),
            'start_time': None,
            'status': 'not started',
            'assigned_robots': [],
            'assigned_workers': []
        }
        steps.append(step)
    
    products[product_name] = {
        'steps': steps,
        'current_step': 0,
        'status': 'not started'
    }
    print(f"Product {product_name} added with {num_steps} assembly steps.")

def assign_task():
    """Dynamically assign tasks to available robots and workers"""
    # First, check and complete any in-progress steps
    for product_name, product in products.items():
        if product['status'] == 'in progress':
            current_step = product['steps'][product['current_step']]
            if current_step['status'] == 'in progress':
                time_passed = datetime.now() - current_step['start_time']
                if time_passed.total_seconds() >= current_step['duration']:
                    # Complete current step
                    print(f"\nStep '{current_step['name']}' for product {product_name} has finished!")
                    
                    # Free up resources
                    for robot_id in current_step['assigned_robots']:
                        robots[robot_id]['status'] = 'idle'
                    for worker_id in current_step['assigned_workers']:
                        workers[worker_id]['status'] = 'idle'
                    
                    current_step['assigned_robots'] = []
                    current_step['assigned_workers'] = []
                    current_step['status'] = 'completed'
                    product['current_step'] += 1

                    if product['current_step'] >= len(product['steps']):
                        product['status'] = 'completed'
                        print(f"Product {product_name} has been fully assembled!")
                    else:
                        print(f"Moving to next step for product {product_name}...")
                        current_step = product['steps'][product['current_step']]
                        current_step['status'] = 'not started'

    # Get available resources
    available_robots = []
    available_workers = []
    
    for robot_id in robots:
        if robots[robot_id]["status"] == "idle":
            available_robots.append(robot_id)
    
    for worker_id in workers:
        if workers[worker_id]["status"] == "idle":
            available_workers.append(worker_id)

    # Try to start steps for all products that aren't completed
    for product_name, product in products.items():
        if product['status'] != 'completed' and product['current_step'] < len(product['steps']):
            current_step = product['steps'][product['current_step']]
            
            if current_step['status'] == 'not started':
                # Check if we have enough resources for this step
                if len(available_robots) >= current_step['robots_required'] and \
                   len(available_workers) >= current_step['workers_required']:
                    
                    # Assign robots
                    for i in range(current_step['robots_required']):
                        robot_id = available_robots[0]
                        robots[robot_id]['status'] = 'working'
                        current_step['assigned_robots'].append(robot_id)
                        available_robots.remove(robot_id)

                    # Assign workers
                    for i in range(current_step['workers_required']):
                        worker_id = available_workers[0]
                        workers[worker_id]['status'] = 'working'
                        current_step['assigned_workers'].append(worker_id)
                        available_workers.remove(worker_id)

                    current_step['status'] = 'in progress'
                    current_step['start_time'] = datetime.now()
                    product['status'] = 'in progress'
                    print(f"\nStarted step: {current_step['name']} for product {product_name}")
                    print(f"Duration: {current_step['duration']} seconds")
                else:
                    print(f"Waiting: Not enough resources available for {product_name} - {current_step['name']}")
                    print(f"Required: {current_step['robots_required']} robots and {current_step['workers_required']} workers")
                    print(f"Available: {len(available_robots)} robots and {len(available_workers)} workers")
                    
def check_status():
    """Monitor the progress of tasks, robots, and workers"""
    print("\n=== ROBOTIC CELL STATUS ===")
    
    print("\nROBOTS:")
    for robot_id, robot in robots.items():
        print(f"Robot {robot_id}: {robot['status']}")
    
    print("\nWORKERS:")
    for worker_id, worker in workers.items():
        print(f"Worker {worker_id}: {worker['status']}")
    
    print("\nPRODUCTS AND ASSEMBLY STEPS:")
    for product_name, product in products.items():
        print(f"\nProduct: {product_name} - Status: {product['status']}")
        for i, step in enumerate(product['steps']):
            current = "-> " if i == product['current_step'] else "   "
            status_info = step['status']
            if step['status'] == 'in progress':
                time_passed = datetime.now() - step['start_time']
                seconds_remaining = step['duration'] - time_passed.total_seconds()
                status_info += f" ({int(seconds_remaining)} seconds remaining)"
            print(f"{current}Step {i+1}: {step['name']} - {status_info}")

def main():
    while True:
        assign_task()  # This will handle both checking completion and starting new steps
        
        print("\n=== ROBOTIC CELL MANAGEMENT SYSTEM ===")
        print("1. Add Robot")
        print("2. Remove Robot")
        print("3. Add Worker")
        print("4. Remove Worker")
        print("5. Create New Product")
        print("6. Check Status")
        print("7. Exit")

        choice = input("\nEnter your choice (1-7): ")

        if choice == '1':
            add_robot()
        elif choice == '2':
            robot_id = int(input("Enter Robot ID to remove: "))
            remove_robot(robot_id)
        elif choice == '3':
            add_worker()
        elif choice == '4':
            worker_id = int(input("Enter Worker ID to remove: "))
            remove_worker(worker_id)
        elif choice == '5':
            assign_product()
            assign_task()  # Start the first step if possible
        elif choice == '6':
            check_status()
        elif choice == '7':
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()