import cell_machine_levels

l0choices = [
    exit,
]

while True:
    # Choices
    print("0. Exit")
    print()
    
    try:
        # Get and run choice
        choice = int(input("Enter your choice: "))
        l0choices[choice]()
    except (ValueError, IndexError):
        print("Invalid choice")
        continue
