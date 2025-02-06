import pygame
import time
import math
import threading
from threading import Event
from sharded_warehouse_manager import ShardedWarehouseManager
from workload import Workload


def process_transactions_in_thread(workload, done_event):
    """Process transactions sequentially to ensure all are displayed."""
    for _ in range(10):  # Process one transaction at a time
        workload.process_transactions(1)
        time.sleep(2)  # Ensure UI updates before processing the next
    done_event.set()  # Mark the process as done


def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption("Warehouse Simulation")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    # Now ask for input
    num_warehouses = int(input("Enter the number of warehouses: "))
    num_transactions = 10  # Default number of transactions

    # Initialize workload and transaction tracking
    manager = ShardedWarehouseManager()
    workload = Workload(manager)
    workload.generate_warehouses(num_warehouses)  # Create the user-defined number of warehouses
    workload.generate_transactions(num_transactions, num_warehouses)  # Create transactions

    # Create an event to signal when processing is done
    done_event = Event()

    # Start transaction processing in a separate thread
    transaction_thread = threading.Thread(target=process_transactions_in_thread, args=(workload, done_event))
    transaction_thread.start()

    # Adjust the warehouse positions dynamically based on the number of warehouses
    warehouse_positions = {}
    spacing = max(1, 800 // num_warehouses)  # Dynamically adjust the spacing
    for i in range(1, num_warehouses + 1):
        x = 100 + (i - 1) * spacing  # Dynamically calculate x position based on number of warehouses
        warehouse_positions[i] = (x, 200, 100, 50)

    def draw_warehouses():
        """Clears the screen and redraws warehouses."""
        screen.fill((255, 255, 255))  # Clear screen before drawing
        for ID, (x, y, w, h) in warehouse_positions.items():
            pygame.draw.rect(screen, (0, 0, 255), (x, y, w, h))
            text = font.render(f"Warehouse {ID}", True, (255, 255, 255))
            screen.blit(text, (x + 10, y + 15))

    def draw_arrow(start, end):
        # Draws a properly oriented arrow from start to end.
        pygame.draw.line(screen, (255, 0, 0), start, end, 5)  # Main arrow line

        # Calculate angle of arrow
        angle = math.atan2(end[1] - start[1], end[0] - start[0])  

        # Arrowhead size
        arrow_size = 15  

        # Calculate rotated arrowhead points
        left_x = end[0] - arrow_size * math.cos(angle - math.pi / 6)
        left_y = end[1] - arrow_size * math.sin(angle - math.pi / 6)

        right_x = end[0] - arrow_size * math.cos(angle + math.pi / 6)
        right_y = end[1] - arrow_size * math.sin(angle + math.pi / 6)

        # Draw arrowhead triangle
        pygame.draw.polygon(screen, (255, 0, 0), [(end[0], end[1]), (left_x, left_y), (right_x, right_y)])

    last_processed_count = 0  # Track processed transactions to avoid duplicates
    running = True

    while running or last_processed_count < num_transactions:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fetch processed transactions **only once** from the queue
        processed_transactions = manager.get_processed_transactions()[:num_transactions]  # Limit to expected transactions

        if len(processed_transactions) > last_processed_count:
            new_transactions = processed_transactions[last_processed_count:]  # Get only new ones
            last_processed_count = len(processed_transactions)  # Update counter
            
            for transaction in new_transactions:
                draw_warehouses()  # Clear previous arrows/text

                if transaction.warehouse in warehouse_positions:
                    start_pos = (400, 100)  # Transactions originate from a central point
                    end_pos = (warehouse_positions[transaction.warehouse][0] + 50, warehouse_positions[transaction.warehouse][1])

                    draw_arrow(start_pos, end_pos)

                    text = font.render(f"{transaction.item} ({transaction.number})", True, (0, 0, 0))
                    screen.blit(text, (end_pos[0] - 20, end_pos[1] - 20))

                    pygame.display.flip()
                    time.sleep(2)  # Keep visible before moving to the next transaction

        pygame.display.flip()
        clock.tick(60)

        # Check if all transactions have been processed
        if done_event.is_set() and last_processed_count == num_transactions:
            time.sleep(2)  # Ensure the last arrows are displayed before exiting
            break


    # Ensure that the transaction thread has finished processing before exiting
    transaction_thread.join()

    workload.print_inventory()  # Now it's safe to print inventory
    workload.kill_processes()
    pygame.quit()

if __name__ == "__main__":
    main()
