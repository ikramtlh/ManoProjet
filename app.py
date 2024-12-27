# Import required libraries
from typing import Dict, List
import time

# Data structures to store information about robots, workers, and products
robots: Dict = {}
workers: Dict = {}
tasks: Dict = {}
products: Dict = {}

class RoboticCell:
    def __init__(self):
        self.robots = {}
        self.workers = {}
        self.tasks = {}
        self.products = {}

    def add_robot(self) -> None:
        """Add a new robot to the robotic cell"""
        robot_id = len(self.robots) + 1
        self.robots[robot_id] = {
            'status': 'idle',
            'current_task': None
        }
        print(f"Robot {robot_id} has been added successfully.")

    def remove_robot(self, robot_id: int) -> None:
        """Remove a robot from the robotic cell"""
        if robot_id not in self.robots:
            print(f"Error: Robot {robot_id} does not exist.")
            return
        
        if self.robots[robot_id]['status'] != 'idle':
            print(f"Error: Cannot remove Robot {robot_id} while it is working.")
            return
        
        del self.robots[robot_id]
        print(f"Robot {robot_id} has been removed successfully.")

    def add_worker(self) -> None:
        """Add a new worker to the robotic cell"""
        worker_id = len(self.workers) + 1
        self.workers[worker_id] = {
            'status': 'idle',
            'current_task': None
        }
        print(f"Worker {worker_id} has been added successfully.")

    def remove_worker(self, worker_id: int) -> None:
        """Remove a worker from the robotic cell"""
        if worker_id not in self.workers:
            print(f"Error: Worker {worker_id} does not exist.")
            return
        
        if self.workers[worker_id]['status'] != 'idle':
            print(f"Error: Cannot remove Worker {worker_id} while they are working.")
            return
        
        del self.workers[worker_id]
        print(f"Worker {worker_id} has been removed successfully.")

    def create_product(self, product_name: str) -> None:
        """Create a new product with assembly steps"""
        self.products[product_name] = {
            'steps': [],
            'status': 'not started',
            'current_step': 0
        }
        print(f"Product '{product_name}' has been created.")

    def add_assembly_step(self, product_name: str, step_name: str, 
                         robots_needed: int, workers_needed: int, duration: int) -> None:
        """Add an assembly step to a product"""
        if product_name not in self.products:
            print(f"Error: Product '{product_name}' does not exist.")
            return

        step = {
            'name': step_name,
            'robots_needed': robots_needed,
            'workers_needed': workers_needed,
            'duration': duration,
            'status': 'not started'
        }
        self.products[product_name]['steps'].append(step)
        print(f"Assembly step '{step_name}' added to product '{product_name}'.")

    def start_assembly(self, product_name: str) -> None:
        """Start the assembly process for a product"""
        if product_name not in self.products:
            print(f"Error: Product '{product_name}' does not exist.")
            return

        product = self.products[product_name]
        if not product['steps']:
            print(f"Error: No assembly steps defined for product '{product_name}'.")
            return

        current_step = product['steps'][product['current_step']]
        
        # Check if we have enough available resources
        available_robots = [r for r in self.robots if self.robots[r]['status'] == 'idle']
        available_workers = [w for w in self.workers if self.workers[w]['status'] == 'idle']

        if len(available_robots) < current_step['robots_needed']:
            print(f"Error: Not enough idle robots available. Need {current_step['robots_needed']}")
            return

        if len(available_workers) < current_step['workers_needed']:
            print(f"Error: Not enough idle workers available. Need {current_step['workers_needed']}")
            return

        # Assign resources to the current step
        for i in range(current_step['robots_needed']):
            robot_id = available_robots[i]
            self.robots[robot_id]['status'] = 'working'
            self.robots[robot_id]['current_task'] = current_step['name']

        for i in range(current_step['workers_needed']):
            worker_id = available_workers[i]
            self.workers[worker_id]['status'] = 'working'
            self.workers[worker_id]['current_task'] = current_step['name']

        current_step['status'] = 'in progress'
        print(f"Started assembly step '{current_step['name']}' for product '{product_name}'")

    def complete_current_step(self, product_name: str) -> None:
        """Complete the current assembly step"""
        if product_name not in self.products:
            print(f"Error: Product '{product_name}' does not exist.")
            return

        product = self.products[product_name]
        current_step = product['steps'][product['current_step']]
        
        # Free up resources
        for robot_id in self.robots:
            if self.robots[robot_id]['current_task'] == current_step['name']:
                self.robots[robot_id]['status'] = 'idle'
                self.robots[robot_id]['current_task'] = None

        for worker_id in self.workers:
            if self.workers[worker_id]['current_task'] == current_step['name']:
                self.workers[worker_id]['status'] = 'idle'
                self.workers[worker_id]['current_task'] = None

        current_step['status'] = 'completed'
        product['current_step'] += 1

        if product['current_step'] >= len(product['steps']):
            product['status'] = 'completed'
            print(f"Product '{product_name}' assembly has been completed!")
        else:
            print(f"Assembly step '{current_step['name']}' completed. Moving to next step.")

    def display_status(self) -> None:
        """Display the current status of the robotic cell"""
        print("\n=== ROBOTIC CELL STATUS ===")
        
        print("\nROBOTS:")
        for robot_id, robot in self.robots.items():
            print(f"Robot {robot_id}: Status: {robot['status']}, Task: {robot['current_task']}")

        print("\nWORKERS:")
        for worker_id, worker in self.workers.items():
            print(f"Worker {worker_id}: Status: {worker['status']}, Task: {worker['current_task']}")

        print("\nPRODUCTS:")
        for product_name, product in self.products.items():
            print(f"\nProduct: {product_name}")
            print(f"Status: {product['status']}")
            print("Assembly Steps:")
            for step in product['steps']:
                print(f"- {step['name']}: {step['status']}")

def main():
    cell = RoboticCell()
    
    while True:
        print("\n=== ROBOTIC CELL MANAGEMENT SYSTEM ===")
        print("1. Add Robot")
        print("2. Remove Robot")
        print("3. Add Worker")
        print("4. Remove Worker")
        print("5. Create New Product")
        print("6. Add Assembly Step")
        print("7. Start Assembly")
        print("8. Complete Current Step")
        print("9. Display Status")
        print("10. Exit")

        choice = input("\nEnter your choice (1-10): ")

        if choice == '1':
            cell.add_robot()
        elif choice == '2':
            robot_id = int(input("Enter Robot ID to remove: "))
            cell.remove_robot(robot_id)
        elif choice == '3':
            cell.add_worker()
        elif choice == '4':
            worker_id = int(input("Enter Worker ID to remove: "))
            cell.remove_worker(worker_id)
        elif choice == '5':
            product_name = input("Enter product name: ")
            cell.create_product(product_name)
        elif choice == '6':
            product_name = input("Enter product name: ")
            step_name = input("Enter step name: ")
            robots_needed = int(input("Enter number of robots needed: "))
            workers_needed = int(input("Enter number of workers needed: "))
            duration = int(input("Enter step duration (minutes): "))
            cell.add_assembly_step(product_name, step_name, robots_needed, workers_needed, duration)
        elif choice == '7':
            product_name = input("Enter product name to start assembly: ")
            cell.start_assembly(product_name)
        elif choice == '8':
            product_name = input("Enter product name to complete current step: ")
            cell.complete_current_step(product_name)
        elif choice == '9':
            cell.display_status()
        elif choice == '10':
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()