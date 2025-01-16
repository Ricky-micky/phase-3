import sqlite3

# Connect to the SQLite database (creates the file if it doesn't exist)
CONN = sqlite3.connect('school.db')

# Cursor for executing SQL statements
CURSOR = CONN.cursor()

class Student:
    def __init__(self, name, age, course, fees, id=None):
        # Instance attributes representing the columns in the database table
        self.id = id
        self.name = name
        self.age = age
        self.course = course
        self.fees = fees

    @classmethod
    def create_table(cls):
        sql = '''
        CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            course TEXT,
            fees REAL
        )
        '''
        CURSOR.execute(sql)
        CONN.commit()


    #add a class methods  for deleting  the table 
    @classmethod 
    def drop_table(cls):
                sql = '''
                    DROP TABLE IF EXISTING student ;
                    ''' 
                CURSOR.execute(sql)
                CONN.commit()

        

    @classmethod
    def create (cls, name,age, course, fees) :
                #creating a new student instance 
            student = cls(name, age, course ,fees)
            sql = "INSERT INTO students (name, age, course ,fees) VALUES (?,?,?,?)"
            CURSOR.execute(sql, (student.name, student.age, student.course, student.fees))
            CONN.commit()

            student.id = CURSOR.lastrowid
            return Student


#execute by running 
student1 = Student.create('Michael', 20, "Computer Science", 1500.50) 
# Run the method to create the table
Student.create_table()