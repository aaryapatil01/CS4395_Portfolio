# Name: Aarya Patil
# Project: Portfolio Assignment 1 (Text Processing with Python)
# Date: 01/31/23

import sys
import os
import pickle
import re


# Class to store information about people from the file
class Person:
    # Constructor
    def __init__(self, last_name, first_name, middle_initial, ID, phone_num):
        # Define all class attributes
        self.last_name = last_name
        self.first_name = first_name
        self.middle_initial = middle_initial
        self.ID = ID
        self.phone_num = phone_num

    # Display function to print out all information from file in an organized format
    def display(self):
        # Print out employee information
        print('\nEmployee id:', self.ID)  # Print out the employee's ID
        print('\t', self.first_name, self.middle_initial, self.last_name)  # Print out the employee's name
        print('\t', self.phone_num)  # Print out the employee's phone number


# Function to check if a filepath was provided
def check_file_path():
    if len(sys.argv) < 2:  # in case no filename is given
        quit('ERROR: Filename not provided.')
    else:  # stores filepath and calls read_file function
        file_path = sys.argv[1]
        return read_file(file_path)  # return contents from file back to main()


# Function to read the contents of a file given a filepath
def read_file(file_path):
    current_dir: str = os.getcwd()  # gets current directory

    with open(os.path.join(current_dir, file_path), 'r') as f:  # joins current directory to filepath specified
        text_in = f.read()  # reads in content
    return text_in  # returns information from inside file


# Function to process the contents of a file
def process_file(file_info):
    temp_list = file_info.split('\n')  # create a temporary list to store each line of info in the file
    temp_list.pop(0)  # deletes the first line of content from the temporary list
    # print(temp_list)  # debug for checking list contents)

    emp_list = []  # create list to hold all employees (will be of class Person)

    # For loop to create a new instance for each person in the list and store each attribute of that person
    for temp in temp_list:
        attrib_list = temp.split(',')  # splits the individual attributes
        person = Person(attrib_list[0], attrib_list[1], attrib_list[2], attrib_list[3],
                        attrib_list[4])  # create new instance of class Person for each employee
        emp_list.append(person)  # add instance to employee list as a new element

    return emp_list  # return employee list


# Function to clean up the attributes to make sure they are correct and formatted properly
def clean_info(employees):
    # Edit employee information
    for employee in employees:
        employee.last_name = employee.last_name.capitalize()  # capitalize the last name
        employee.first_name = employee.first_name.capitalize()  # capitalize the first name

        if not employee.middle_initial:  # if the employee does not have a middle name, replace with X
            employee.middle_initial = 'X'
        employee.middle_initial = employee.middle_initial.capitalize()  # capitalize the middle initial

        # Regex for id: [A-Z]{2}\d{4} - [A-Z] searches for capital letters (2 letters) and the \d looks for numbers (4)
        while not re.fullmatch('[A-Z]{2}\d{4}',
                               employee.ID):  # checks to see if the ID matches the format specified
            print("\nID invalid:", employee.ID)
            print("ID is two letters followed by 4 digits")
            employee.ID = input("Please enter a valid id: ")

        # Regex for number: \d{3}-\d{3}-\d{4} - looks for 3 numbers, hyphen, 3 numbers again, hyphen, and 4 nums
        while not re.fullmatch('\d{3}-\d{3}-\d{4}',
                               employee.phone_num):  # checks to see if the number matches the format specified
            print("\nPhone", employee.phone_num, "is invalid")
            print("Enter phone number in form 123-456-7890")
            employee.phone_num = input("Enter phone number: ")

    return employees  # Return the fixed employee list


# Function to create a dict of persons where the id is the  key
def create_dict(processed_emp_list):
    # Create a dict
    emp_dict = {}

    for emp in processed_emp_list:
        if emp.ID in emp_dict:  # check for duplicate IDs
            print("ERROR: ID already exists within the dictionary")
        else:  # add the employee to the dictionary with the ID as the key
            emp_dict[emp.ID] = emp

    return emp_dict  # Return the new dictionary of employees


# Main function
def main():
    file_info = check_file_path()  # calls function to check if user provided a filepath

    # Create a list to hold all the employees (will be of Person class)
    employee_list = process_file(file_info)  # call process_file info to decipher info retrieved from file

    # Call clean_info function to fix the attributes for each instance of the Person class in employee_list
    processed_emp_list = clean_info(employee_list)

    # Call create_dict function to create a dict of the persons
    employee_dict = create_dict(processed_emp_list)

    # Pickle the dict created above
    with open('emp_dict_pickle', 'wb') as handle:
        pickle.dump(employee_dict, handle)
    # Unpack the pickled dict
    with open('emp_dict_pickle', 'rb') as handle:
        new_employee_dict = pickle.load(handle)

    # Call display function to print out information
    print('\nEmployee List:')
    for i, p in sorted(new_employee_dict.items()):  # iterates over dict (i is id, and p is the Person object)
        p.display()


if __name__ == '__main__':  # uses double underscores
    main()
