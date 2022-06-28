from datetime import datetime
import faker
from random import randint, choice
import sqlite3

NUMBER_TEACHERS = 3
NUMBER_GROUPS = 3
NUMBER_STUDENTS = 30
NUMBER_MARKS_FOR_STUDENT = 20
SUBJECTS = ['Physics', 'Chemistry', 'English','Economy','Law basics']


def generate_fake_data(number_teachers,number_groups,number_students,subjects, number_marks_for_student) -> tuple():
    fake_teachers = []  
    fake_groups = []  
    fake_students = []
    fake_subjects = [] 
    fake_marks_for_student = []

    fake_data = faker.Faker('en-US')
    
    for _ in range(number_teachers):
        fake_teachers.append(fake_data.name())
    
    for _ in range(number_groups):
        fake_groups.append(fake_data.license_plate())

    for _ in range(number_students):
        fake_students.append(fake_data.name())

    for subject in subjects:
        
        fake_subjects.append(subject)

    for _ in range(number_marks_for_student):
        fake_marks_for_student.append(randint(1,100)) 

    return fake_teachers,fake_groups,fake_students,fake_subjects, fake_marks_for_student


def prepare_data(teachers, groups, students, subjects, marks_for_student) -> tuple():
    for_teachers = []
    
    for teacher in teachers:
        for_teachers.append((teacher, ))

    for_groups = [] 

    for group in groups:
        for_groups.append((group, randint(2020, 2022)))

    for_students = []

    for student in students:
        for_students.append((student, randint(1, NUMBER_GROUPS)))
    
    for_subjects = []

    for subject in subjects:
        for_subjects.append((subject,))

    for_students_mark = []
    for num_student in range(NUMBER_STUDENTS):
        
        for mark in marks_for_student:
            date_mark = datetime(randint(2020,2022),randint(1,12), randint(1,28)).date()
            
            for_students_mark.append((mark, num_student, randint(1,len(SUBJECTS)), randint(1,NUMBER_TEACHERS), date_mark))    
        
        
    
    return for_teachers,for_groups,for_students,for_subjects, for_students_mark


def insert_data_to_db(teachers, groups, students, subjects ,marks_for_student) -> None:

    with sqlite3.connect('hw-8.db') as con:

        cur = con.cursor()


        sql_to_teachers = """INSERT OR REPLACE INTO teachers(full_name)
                               VALUES (?)"""

        cur.executemany(sql_to_teachers, teachers)

        sql_to_groups = """INSERT OR REPLACE INTO groups (group_name, group_year)
                               VALUES (?, ?)"""

        cur.executemany(sql_to_groups, groups)
        print(groups)
        sql_to_students = """INSERT OR REPLACE into students (full_name, id_group)
                              VALUES (?, ?)"""

        cur.executemany(sql_to_students, students)

        sql_to_subjects = """INSERT OR REPLACE INTO subjects (subject_name)
                              VALUES (?)"""

        cur.executemany(sql_to_subjects, subjects)
       
        sql_to_marks = """INSERT OR REPLACE into marks (marks, id_student, id_subject, id_teacher, mark_date)
                               VALUES (?, ?, ?, ?, ?)"""
        
        cur.executemany(sql_to_marks, marks_for_student)

        con.commit()


if __name__ == "__main__":
    teachers, groups, students, subjects, marks_for_student = generate_fake_data(NUMBER_TEACHERS, NUMBER_GROUPS, NUMBER_STUDENTS, SUBJECTS, NUMBER_MARKS_FOR_STUDENT)
    teachers, groups, students, subjects, marks_for_student = prepare_data(teachers, groups, students, subjects, marks_for_student)
    insert_data_to_db(teachers, groups, students, subjects, marks_for_student)