"""
===========================================================
EXAM SEATING ARRANGEMENT SYSTEM
===========================================================

"""

from time import time


# ---------------------------------------------------------
# DATA STORAGE
# ---------------------------------------------------------

halls = {}
groups = {}

trace_log = []


# ---------------------------------------------------------
# HALL CLASS
# ---------------------------------------------------------

class Hall:

    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity


# ---------------------------------------------------------
# 1. ADD HALL
# ---------------------------------------------------------

def add_hall():

    hall_name = input("Enter Hall Name: ")

    if hall_name in halls:
        print("Hall already exists.")
        return

    capacity = int(input("Enter Hall Capacity: "))

    halls[hall_name] = Hall(hall_name, capacity)

    print("\nHall Added Successfully!")
    print(f"Total Halls Added: {len(halls)}")

# ---------------------------------------------------------
# 2. ADD GROUP
# ---------------------------------------------------------

def add_group():

    group_name = input("Enter Group Name: ")

    if group_name in groups:
        print("Group already exists.")
        return

    groups[group_name] = []

    print("Group Added Successfully!")


# ---------------------------------------------------------
# 3. ADD STUDENTS
# ---------------------------------------------------------

def add_students():

    if not groups:
        print("No groups available.")
        return

    print("\nAvailable Groups:")

    for group in groups:
        print(group)

    group_name = input("\nEnter Group Name: ")

    if group_name not in groups:
        print("Group not found.")
        return

    count = int(input("Enter Number of Students: "))

    start = len(groups[group_name]) + 1

    for i in range(start, start + count):
        groups[group_name].append(f"{group_name}-{i}")

    print("Students Added Successfully!")


# ---------------------------------------------------------
# 4. VIEW HALL DETAILS
# ---------------------------------------------------------

def view_hall_details():

    if not halls:
        print("\nNo halls available.")
        return

    print("\n========== HALL DETAILS ==========")

    for hall in halls.values():
        print(
            f"Hall Name: {hall.name} | Capacity: {hall.capacity}"
        )
# ---------------------------------------------------------
# 5. DELETE HALL
# ---------------------------------------------------------

def delete_hall():

    hall_name = input("Enter Hall Name to Delete: ")

    if hall_name in halls:
        del halls[hall_name]
        print("Hall Deleted Successfully.")
    else:
        print("Hall Not Found.")


# ---------------------------------------------------------
# 6. DELETE STUDENTS
# ---------------------------------------------------------

def delete_students():

    group_name = input("Enter Group Name: ")

    if group_name not in groups:
        print("Group Not Found.")
        return

    count = int(
        input("How Many Students to Remove? ")
    )

    current = len(groups[group_name])

    if count > current:
        print("Cannot remove more students than available.")
        return

    for _ in range(count):
        groups[group_name].pop()

    print("Students Removed Successfully.")


# ---------------------------------------------------------
# 7. DELETE GROUP
# ---------------------------------------------------------

def delete_group():

    group_name = input(
        "Enter Group Name to Delete: "
    )

    if group_name in groups:
        del groups[group_name]
        print("Group Deleted Successfully.")
    else:
        print("Group Not Found.")


# ---------------------------------------------------------
# CSP FUNCTIONS
# ---------------------------------------------------------

def get_group(student):

    return student.split("-")[0]


def is_valid(seating, student):

    """
    Constraint:
    Same group students should not sit adjacent.
    """

    if not seating:
        return True

    previous_student = seating[-1]

    if get_group(previous_student) == get_group(student):

        trace_log.append(
            f"Constraint Failed: {student} "
            f"cannot sit beside {previous_student}"
        )

        return False

    return True


# ---------------------------------------------------------
# MRV HEURISTIC
# ---------------------------------------------------------

def select_group(remaining):

    """
    MRV-inspired heuristic:
    Choose group with maximum students left.
    """

    available = []

    for group in remaining:

        if len(remaining[group]) > 0:
            available.append(
                (group, len(remaining[group]))
            )

    if not available:
        return None

    available.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return available[0][0]


# ---------------------------------------------------------
# BACKTRACKING SEARCH
# ---------------------------------------------------------

def backtrack(seating,
              remaining,
              total_students):

    if len(seating) == total_students:
        return True

    groups_sorted = sorted(
        remaining.keys(),
        key=lambda g: len(remaining[g]),
        reverse=True
    )

    for group in groups_sorted:

        if not remaining[group]:
            continue

        student = remaining[group][0]

        if is_valid(seating, student):

            seating.append(student)
            remaining[group].pop(0)

            trace_log.append(
                f"Placed {student}"
            )

            if backtrack(
                    seating,
                    remaining,
                    total_students):
                return True

            remaining[group].insert(
                0,
                student
            )

            seating.pop()

            trace_log.append(
                f"Backtracked {student}"
            )

    return False


# ---------------------------------------------------------
# 8. GENERATE SEATING ARRANGEMENT
# ---------------------------------------------------------

def generate_seating():

    if not halls:
        print("No halls available.")
        return

    if not groups:
        print("No groups available.")
        return

    total_capacity = sum(
        hall.capacity
        for hall in halls.values()
    )

    all_students = []

    for group_students in groups.values():
        all_students.extend(group_students)

    total_students = len(all_students)

    if total_students == 0:
        print("No students available.")
        return

    if total_students > total_capacity:

        print("\nInsufficient Capacity")
        print(
            f"Students : {total_students}"
        )
        print(
            f"Seats    : {total_capacity}"
        )

        return

    remaining = {}

    for group in groups:
        remaining[group] = groups[group][:]

    seating = []

    start_time = time()

    success = backtrack(
        seating,
        remaining,
        total_students
    )

    end_time = time()

    print("\n" + "=" * 60)
    print("SEATING ARRANGEMENT REPORT")
    print("=" * 60)

    if not success:
        print(
            "No valid seating arrangement found."
        )
        return

    index = 0

    for hall in halls.values():

        print(
            f"\nHALL : {hall.name}"
        )

        print("-" * 40)

        for seat in range(
                1,
                hall.capacity + 1):

            if index >= len(seating):
                break

            print(
                f"Seat {seat:03d} "
                f"-> {seating[index]}"
            )

            index += 1

    print("\n" + "=" * 60)
    print("SEARCH STATISTICS")
    print("=" * 60)

    print(
        f"Total Students : {total_students}"
    )

    print(
        f"Total Halls    : {len(halls)}"
    )

    print(
        f"Execution Time : "
        f"{end_time-start_time:.5f} sec"
    )

    print(
        f"Trace Entries  : "
        f"{len(trace_log)}"
    )

    print("\nConstraint Explanations:")

    count = 0

    for item in trace_log:

        if "Constraint Failed" in item:
            print(item)

            count += 1

        if count == 5:
            break


# ---------------------------------------------------------
# MAIN MENU
# ---------------------------------------------------------

while True:

    print("\n")
    print("=" * 60)
    print(
        " EXAM SEATING ARRANGEMENT SYSTEM"
    )
    print("=" * 60)

    print("1. Add Halls")
    print("2. Add Groups")
    print("3. Add Students")
    print("4. View Hall Details")
    print("5. Delete Hall")
    print("6. Delete Students")
    print("7. Delete Group")
    print("8. Generate Seating Arrangement")
    print("9. Exit")

    choice = input(
        "\nEnter Your Choice: "
    )

    if choice == "1":
        add_hall()

    elif choice == "2":
        add_group()

    elif choice == "3":
        add_students()

    elif choice == "4":
        view_hall_details()

    elif choice == "5":
        delete_hall()

    elif choice == "6":
        delete_students()

    elif choice == "7":
        delete_group()

    elif choice == "8":
        generate_seating()

    elif choice == "9":

        print(
            "\nThank You For Using The System!"
        )

        break

    else:
        print("Invalid Choice.")
