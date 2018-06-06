import psycopg2
import random

from coursework.enums import *


def connect(host):
    return psycopg2.connect(
        dbname="coursework",
        user="postgres",
        host=host,
        port="5432",
        password='password'
    )


def generate_student():
    return {
        "name": names[random.randint(0, len(names) - 1)],
        "rating": random.uniform(60, 100),
        "year": 2018 - random.randint(0, 5),
        "group": groups[random.randint(0, len(groups) - 1)],
        "course": random.randint(1, 6),
        "age": random.randint(18, 24)
    }


def generate_students():
    return [generate_student() for _ in range(200)]


def validate(student):
    return (
        student["name"] and len(student["name"]) < 50 and
        60 <= student["rating"] <= 100 and
        student["year"] and student["year"] > 1900 and
        student["group"] and len(student["group"]) <= 5 and
        1 <= student["course"] <= 6 and
        18 <= student["age"] <= 24
    )


def validate_students(students):
    return list(filter(lambda s: validate(s), students))


def generate():
    try:
        conn = connect("10.0.3.230")
        cursor = conn.cursor()

        students = validate_students(generate_students())

        for s in students:
            try:
                cursor.execute(
                    """
                        INSERT INTO students (name, rating, year, "group", course, age)
                        VALUES(%s, %s, %s, %s, %s, %s);
                    """,
                    (s["name"], s["rating"], s["year"], s["group"], s["course"], s["age"])
                )
                conn.commit()
            except ValueError:
                print("Value error")
    except:
        print("I am unable to connect to the database")
