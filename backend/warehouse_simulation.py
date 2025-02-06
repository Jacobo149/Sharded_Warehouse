from sharded_warehouse_manager import ShardedWarehouseManager
from workload import Workload
import pygame
import time
import math
import threading

from threading import Event

def process_transactions_in_thread(workload, done_event):
    """Process transactions in a separate thread."""
    workload.process_transactions(6)  # Adjust the number of iterations
    done_event.set()  # Mark the process as done

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    # Initialize workload and transaction tracking
    manager = ShardedWarehouseManager()
    workload = Workload(manager)
    workload.generate_warehouses(3)  # Create warehouses
    workload.generate_transactions()  # Create transactions

    # Create an event to signal when processing is done
    done_event = Event()

    # Start transaction processing in a separate thread
    transaction_thread = threading.Thread(target=process_transactions_in_thread, args=(workload, done_event))
    transaction_thread.start()

    warehouse_positions = {
        1: (100, 200, 100, 50),  
        2: (350, 200, 100, 50),  
        3: (600, 200, 100, 50)   
    }

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

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fetch processed transactions **only once** from the queue
        processed_transactions = manager.get_processed_transactions()

        if len(processed_transactions) > last_processed_count:
            new_transactions = processed_transactions[last_processed_count:]  # Get only new ones
            last_processed_count = len(processed_transactions)  # Update counter
            
            for transaction in new_transactions:
                draw_warehouses()  # Clear previous arrows/text

                print(f"Processed Transaction {transaction.ID}: {transaction.item} ({transaction.number} units at ${transaction.price})")

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
        if done_event.is_set() and len(processed_transactions) == 6:  # Adjust if necessary
            break

    # Ensure that the transaction thread has finished processing before exiting
    transaction_thread.join()

    workload.print_inventory()  # Now it's safe to print inventory
    workload.kill_processes()
    pygame.quit()

if __name__ == "__main__":
    main()
