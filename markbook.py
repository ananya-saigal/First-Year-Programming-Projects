"""
Markbook Application
Group members: Rishabh, James, Ananya
"""
import json
from typing import Dict, Tuple

try:
    with open("database.json", "r") as database:
        data = json.load(database)

    classes_list = [data["classes_list"]][0]
    all_students = [data["all_students"]][0]

except json.decoder.JSONDecodeError:
    # Checks if the file is empty, if the file is empty, then the classes_list and all_students are initialized to empty list.
    classes_list = []
    all_students = []


def main_choices():
    """Runs the program, Main choices for the user"""
    global classes_list, all_students

    print("What would you like to do?\n")
    print("0) Save and exit")
    print("1) Make a classroom")
    print("2) Create a student")
    print("3) View and edit classes")
    print()

    choice = ensure_integer("> ")

    if choice == 0:
        exit(save())
    elif choice == 1:
        code = input("Enter the course code: ")
        name = input("Enter the course name: ")
        period = ensure_integer("Enter the course period: ")
        teacher = input("Enter the name of teacher: ")
        classes_list.append(create_classroom(code, name, period, teacher))
        print(
            "Classroom Created! \nTo view choices pick the third choice in the main menu.")
        main_choices()
    elif choice == 2:
        first = input("Student's first name: ")
        last = input("Student's last name: ")
        student_num = ensure_integer("Student number: ")
        student_gender = input("Gender: ")
        student_grade = ensure_integer("Grade: ")
        student_email = input("Email: ")
        all_students.append(create_student(
            first, last, student_num, student_gender, student_grade, student_email))
        print("Student Created! \nTo view choices pick the third choice in the main menu.")
        main_choices()
    elif choice == 3 and classes_list != []:
        view = edit_classes(view_classes())
    elif choice == 3 and classes_list == []:
        print("There are no classes to view, please create a classroom.")
        main_choices()
    else:
        print("Not a valid option!")
        main_choices()


def view_classes() -> Dict:
    """Gets the classes that are currently available
    Returns:
        Tuple: Returns a tuple with the class chosen by user (Dict).
    """
    for i, clas in enumerate(classes_list):
        print(f'{i+1}: {clas["course_name"]}, taught by: {clas["teacher"]}')

    while True:
        try:
            class_to_view = int(
                input("Which class do you want to view (Enter 0 to got back): "))
            if class_to_view == 0:
                main_choices()
            if 0 < class_to_view <= len(classes_list):
                break
            print("Please enter a valid option!")
        except ValueError:
            print("Please enter a valid option!")

    return classes_list[class_to_view-1]


def edit_classes(class_to_edit: Dict):
    """Function that will edit a specific class
    Args:
        class_to_edit: The class to edit
        index: The index the class is at in the global variable 'classes_list'
    """
    print("What would you like to do?\n")
    print("0) Save and exit")
    print("1) Main Menu")
    print("2) Add Student")
    print("3) Edit Student")
    print("4) Remove Student")
    print("5) Add Assignment")
    print("6) Edit Assignment")
    print("7) Remove Assignment")
    print("8) Change Student Mark for Assignment")
    print("9) Add report card comments")
    print("10) Print out Reports")
    print("11) Get class information")
    print("12) Save")


    while True:
        try:
            choice = int(input("> "))
            if 0 <= choice <= 12:
                break
            print("Please enter a valid option!")
        except TypeError:
            print("Please enter a valid option!")

    if choice == 0:
        exit(save())

    elif choice == 1:
        pass

    elif choice == 2:
        print("Do you want to create a new student or add existing student?")
        print("0) Back")
        print("1) Create a new student")
        print("2) Add existing student")

        while True:
            try:
                user_option = int(input("> "))
                if 0 <= user_option <= 2:
                    break
                print("Please enter a valid option!")
            except TypeError:
                print("Enter valid choice")

        if choice == 0:
            main_choices()

        elif user_option == 1:
            first = input("Student's first name: ")
            last = input("Student's last name: ")
            student_num = ensure_integer("Student number: ")
            student_gender = input("Gender: ")
            student_grade = ensure_integer("Grade: ")
            student_email = input("Email: ")
            new_student = (create_student(
                first, last, student_num, student_gender, student_grade, student_email))
            all_students.append(new_student)
            add_student_to_classroom(new_student, class_to_edit)
            place_holder_student_mark(class_to_edit, new_student)
            print("Student Created!")

        elif user_option == 2:
            print(get_all_students())

            while True:
                try:
                    student_to_add = int(
                        input("Which student do you want to add: ")) - 1
                    if 0 <= student_to_add < len(all_students):
                        break
                    print("Please enter a valid option!")
                except TypeError:
                    print("Please enter a valid option!")

            for i, student in enumerate(all_students):
                if i == student_to_add and student not in class_to_edit["student_list"]:
                    add_student_to_classroom(student, class_to_edit)
                    place_holder_student_mark(class_to_edit, student)
                    print("Student Created!")
                elif i == student_to_add:
                    print("Student already present!")

    elif choice == 3:
        print(get_all_students_from_classroom(class_to_edit))
        if len(class_to_edit["student_list"]) < 1:
            print("Please create a student in the class first!")
            main_choices()
        student = int(input("Which student's information would you like to be changed: ")) - 1
        number_changes = int(input("Enter the number of values you want to changed: "))
        for key in class_to_edit["student_list"][student].keys():
            print(key)

        for i in range(number_changes):
            key_to_change = input("Enter what you want to change: ")
            values = input("Enter what you want to change it to: ")
            edit_student(class_to_edit["student_list"][student], key_to_change, values)
        print(f"Completed! Here is the student info: {get_reports(class_to_edit, class_to_edit['student_list'][student])}")

    elif choice == 4:
        print(get_all_students_from_classroom(class_to_edit))
        student_to_remove = int(
            input("Which student do you want to remove: ")) - 1
        for i in range(len(class_to_edit['student_list'])):
            if i == student_to_remove:
                remove_student_from_classroom(
                    class_to_edit['student_list'][i], class_to_edit)

    elif choice == 5:
        name_of_assignment = input("Name of assignment: ")
        due_date = input("When will it be due: ")
        points = ensure_integer("What will it be out of: ")
        new_assignment = create_assignment(
            name_of_assignment, due_date, points)
        class_to_edit["assignment_list"].append(new_assignment)
        for student in class_to_edit["student_list"]:
            student["marks"].append("Not Added")
        print("Assignment created!")

    elif choice == 6:
        print(get_all_assignments_from_classroom(class_to_edit))
        assignment_to_edit = ensure_integer("Which assignment do you want to edit: ") - 1
        while True:
            print("\nHere is the assignment info:")
            i = 0
            for key, value in class_to_edit['assignment_list'][assignment_to_edit].items():
                print(f"{i+1}) {key}: {value}")
                i += 1
            value_to_be_edited = ensure_integer("What would you like to edit (Press 0 to go back): ") - 1
            if value_to_be_edited == -1:
                break
            new_value = input("What would you like the new value to be: ")
            try:
                edit_assignment(class_to_edit['assignment_list'][assignment_to_edit], value_to_be_edited, new_value)
            except IndexError:
                print("Please enter a valid option (1-3)")

    elif choice == 7:
        print(get_all_assignments_from_classroom(class_to_edit))
        if len(class_to_edit["assignment_list"])<1:
            print("Please create a assignment in the class first!")
            main_choices()
        assignment_to_remove = int(input("Which assignment(number) do you want to remove: "))
        remove_assignment(class_to_edit, assignment_to_remove)
        print("Assignment Removed!")

    elif choice == 8:
        print(get_all_assignments_from_classroom(class_to_edit))
        if get_all_assignments_from_classroom(class_to_edit) == "":
            print("Make an assignment first!")
            main_choices()
        assignment = ensure_integer("Which assignment do you want to mark: ") - 1
        print(get_all_students_from_classroom(class_to_edit))
        student_to_mark = ensure_integer("Which student do you want to mark: ") - 1
        mark = float(input("What mark do you want to give the student (Out of 100%): "))
        give_student_mark_for_assignment(class_to_edit['student_list'][student_to_mark], mark, assignment)
        print("Student marked!")

    elif choice == 9:
        if get_all_assignments_from_classroom == "":
            print("Make an assignment first!")
            main_choices()
        print(get_all_students_from_classroom(class_to_edit))
        student_to_comment = ensure_integer("Which student's report card do you want to view: ") - 1
        comment_to_give = str(input("What do you want to write: "))
        give_student_comment(class_to_edit["student_list"][student_to_comment], comment_to_give)

    elif choice == 10:
        print(get_all_students_from_classroom(class_to_edit))
        student_to_view = ensure_integer("Which student's report card do you want to view: ") - 1
        get_reports(class_to_edit, class_to_edit["student_list"][student_to_view])

    elif choice == 11:
        get_class_information(class_to_edit)

    elif choice == 12:
        save()

    main_choices()  # ! For a continuos loop


def edit_assignment(assignment_to_edit: dict, what_to_edit: int, new_value: str or int):
    """Edits assignments
    Args:
        assignment_to_edit: The assignment to edit
        what_to_edit: The parameter to edit
        new_value: The new value
    """
    list_of_keys = list(assignment_to_edit.keys())
    assignment_to_edit[list_of_keys[what_to_edit]] = new_value


def get_all_students() -> str:
    """Gets all students
    returns:
        The string of all students
    """
    all_students_string = ""

    for i, student in enumerate(all_students):
        all_students_string += (
            f'{i+1}) Name: {student["first_name"]} {student["last_name"]}\tEmail: {student["email"]}\n')

    return all_students_string


def get_all_students_from_classroom(classroom: Dict) -> str:
    """Gets all students from a particular class
    Args:
        classroom: The classroom to get all students
    Returns:
        A string with the name and email of every student in the classroom
    """
    all_students_in_class = ""

    for i, student in enumerate(classroom['student_list']):
        all_students_in_class += (
            f'{i+1}) Name: {student["first_name"]} {student["last_name"]}\tEmail: {student["email"]}\n')

    return all_students_in_class


def get_all_assignments_from_classroom(classroom: Dict) -> str:
    """Gets all the assignment in a particular class
    Args:
        classroom: The class to get assignments from.
    Returns:
        A string with the name and due date of every assignment.
    """
    all_assignments_in_class = ""

    for i, assignment in enumerate(classroom['assignment_list']):
        all_assignments_in_class += (
            f"Assignment Number {i+1}: Name: {assignment['name']}, Due: {assignment['due']}\n")

    return all_assignments_in_class


def remove_assignment(class_to_edit: Dict, assignment_to_remove: int):
    """Removes an assignment and the corresponding student mark from a class
    Args:
        class_to_edit: Class to remove assignment from.
        assignment_to_remove: The assignment to be removed
    """
    class_to_edit["assignment_list"].pop(assignment_to_remove - 1)
    for student in class_to_edit["student_list"]:
        student["marks"].pop(assignment_to_remove-1)



def create_assignment(name: str, due: str, points: int) -> Dict:
    """Creates an assignment represented as a dictionary
    Args:
        name: the name of the assignment.
        due: the due date for the assignment.
        points: what the assignment is out of.
    Returns:
        Assignment as a dictionary.
    """
    assignment = {
        "name": name,
        "due": due,
        "points": points
    }

    return assignment


def create_classroom(course_code: str, course_name: str, period: int, teacher: str) -> Dict:
    """Creates an classroom as a dictionary
    Args:
        course_code: The course code of the class
        course_name: The name of the class
        period: What period the class is in.
        teacher: The name of the teacher who teaches the class
    Returns:
        A dictionary with the classroom and its information
    """
    classroom = {
        "course_code": course_code,
        "course_name": course_name,
        "period": period,
        "teacher": teacher,
        "student_list": [],
        "assignment_list": []
    }

    return classroom


def calculate_average_mark(student: Dict) -> float:
    """Calculates the average mark of a student
    Args:
        student: Student dict
    Returns:
        The average mark of the student
    """
    sum_of_num = 0
    for mark in student["marks"]:
        try:
            sum_of_num += mark
        except TypeError:
            pass
    return sum_of_num/(len(student["marks"]) - student["marks"].count("Not Added"))


def add_student_to_classroom(student: Dict, classroom: Dict):
    """Adds student to a classroom
    Args:
        student: Student dict
        classroom: The classroom to add the student to
    """
    classroom["student_list"].append(student)


def remove_student_from_classroom(student: Dict, classroom: Dict):
    """Removes student from classroom
    Args:
        student: The student to be removed
        classroom: the class from which the student will be removed.
    """
    classroom["student_list"].remove(student)


def edit_student(student: Dict, info_to_edit: str, new_value: str or int):
    """Edits the student's info
    Args:
        student: The student whose data needs to be updated.
        info_to_edit: The parameter to edit
        new_value: The new value
    """
    try:
        student[info_to_edit] = int(new_value)
    except ValueError:
        student[info_to_edit] = new_value


def create_student(first_name: str, last_name: str, student_number: int,
                   gender: str, grade: int, email: str) -> dict:
    """Create student
    Args:
        first_name: Students' first name
        last_name: Students' last_name
        student_number: students' number
        gender: students' gender
        grade: students' grade
        email: students' email
    Returns:
        Student information as a dictionary
    """
    student = {
        'first_name': first_name,
        'last_name': last_name,
        'student_number': student_number,
        'gender': gender,
        'image': f"{first_name}{last_name}{student_number}.jpg",
        'grade': grade,
        'email': email,
        'marks': [],
        'comments': ""
    }

    return student


def get_reports(classroom: dict, student: dict):
    """Prints the report card of a particular student
    Args:
        classroom: The classroom the student belongs to
        student: The student whose report card is to be retrieved
    """
    print(f"\nName: {student['first_name']} {student['last_name']}")
    print(f"Student number: {student['student_number']}")
    print(f"Gender: {student['gender']}")
    print(f"Image: {student['image']}")
    print(f"Grade: {student['grade']}")
    print(f"Email: {student['email']}")
    print(f"Marks: ")

    for i, mark in enumerate(student["marks"]):
        print(f"\t{classroom['assignment_list'][i]['name']}: {mark} %")

    try:
        average_mark_for_student = calculate_average_mark(student)
        print(f"Average mark: {average_mark_for_student} %")
    except ZeroDivisionError:
        print(f"Average mark: Not Applicable")

    print(f"Teacher's comments: {student['comments']}\n")


def get_class_information(class_name: Dict):
    """Prints information about a particular class
    Args:
        class_name: The class whose information is to be found
    """
    print(f"Course name: {class_name['course_name']}")
    print(f"Course code: {class_name['course_code']}")
    print(f"Period: {class_name['period']}")
    print(f"Name of teacher: {class_name['teacher']}")
    print("Students: ")
    students_marks = []

    for student in class_name['student_list']:
        print(f"\n\tName: {student['first_name']} {student['last_name']}")
        print(f"\t\tGender: {student['gender']}")
        print(f"\t\tGrade: {student['grade']}")
        print(f"\t\tEmail: {student['email']}")
        print(f"\t\tMarks: ")

        for i, mark in enumerate(student["marks"]):
            print(f"\t\t\t{class_name['assignment_list'][i]['name']}: {mark} %")
        try:
            average_mark_for_student = calculate_average_mark(student)
            print(f"\t\tAverage mark: {average_mark_for_student} %")
            students_marks.append(average_mark_for_student)
        except ZeroDivisionError:
            print(f"\t\tAverage mark: Not Applicable")

    try:
        print(f"Class average (Lowest mark dropped): {(sum(students_marks) - min(students_marks))/(len(class_name['student_list'])-1)} %")
    except (ZeroDivisionError, ValueError) as e:
        print(f"Class average: Not applicable")

    print("Assignments: ")

    for assignment in class_name['assignment_list']:
        print(f"\tAssignment: {assignment['name']}")
        print(f"\t\tDue: {assignment['due']}")
        print(f"\t\tPoints: {assignment['points']}")


def give_student_comment(student: Dict, comments: str):
    """Adds comments on a students report card
    Args:
        student: The student to whom the comment is added
        comments: The comment to give to the student
    """
    student["comments"] = comments


def ensure_integer(question: str) -> int:
    """Ensures the number user is entering is an integer
    Args:
        question: The prompt to give to user
    Returns:
        The option that they choose
    """
    while True:
        try:
            integer = int(input(question))
        except ValueError:
            print("Please enter a number!")
        else:
            return integer


def give_student_mark_for_assignment(student: dict, student_mark: float, mark_index: int):
    """Gives student a mark for a particular assignment
    Args:
        student: The student whose mark is to be changed
        student_mark: The mark that the student got
        mark_index: The index of the assignment that is being marked
    """
    student['marks'][mark_index] = student_mark


def place_holder_student_mark(class_to_edit: Dict, student: Dict):
    """Give initial mark to student if student was created after assignment
    Args:
        class_to_edit: The class to edit.
        student: The student who is being added
    """
    i = 0
    if class_to_edit["assignment_list"] != []:
        while i < len(class_to_edit["assignment_list"]):
            student["marks"].append("Not Added")
            i += 1


def save():
    """Saves to the database"""
    master_dict = {"classes_list": classes_list, "all_students": all_students}
    with open("database.json", "w") as database:
        json.dump(master_dict, database, indent=4)


if __name__ == '__main__':
    print(f'\n{"#"*110}\n')
    print(("Welcome to the markbook program").center(110,"-"))
    print(f'\n{"#"*110}\n')
    main_choices()
