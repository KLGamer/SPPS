from mysql import connector
connection = connector.connect(
    host = "sql12.freesqldatabase.com",
    user = "sql12822441",
    password = "mD28Lz562k",
    database = "sql12822441",
)
cursor = connection.cursor()
cursor.execute("select * from List;")
for x in cursor:
    print(x)


def shift_tokens_from(cursor, token: int):
    cursor.execute("SELECT COUNT(*) FROM List WHERE token >= %s", (token,))
    count = cursor.fetchone()[0]
    if count:
        cursor.execute(
            "UPDATE List SET token = token + 1 WHERE token >= %s ORDER BY token DESC",
            (token,),
        )
        connection.commit()


def insert_patient(cursor, id: int, pname: str, age: int, blood_group: str, sex: str,
                   temperature: float, mNumber: int, pregnancy: bool, pwd: bool,
                   symptom: str, token_reduction: int):
    # Calculate the new token based on token_reduction
    cursor.execute("SELECT COALESCE(MAX(token), 0) FROM List")
    max_token = cursor.fetchone()[0]
    new_token = max_token + 1 - token_reduction
    if new_token < 1:
        new_token = 1

    # Shift tokens if necessary
    shift_tokens_from(cursor, new_token)

    # Insert the patient
    cursor.execute(
        """INSERT INTO List (id, pname, age, blood_group, sex, temperature, mNumber, pregnancy, pwd, symptom, token)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (id, pname, age, blood_group, sex, temperature, mNumber, pregnancy, pwd, symptom, new_token)
    )
    connection.commit()


def get_all_patients_with_estimated_time():
    cursor.execute(
        "SELECT id, pname, age, blood_group, sex, temperature, mNumber, pregnancy, pwd, symptom, token FROM List ORDER BY token"
    )
    columns = [col[0] for col in cursor.description]
    patients = {}

    for row in cursor.fetchall():
        record = dict(zip(columns, row))
        record["estimated_time_minutes"] = record["token"] * 5
        patients[record["token"]] = record

    return patients


def current_number_of_people(cursor):
    cursor.execute("SELECT COUNT(*) FROM List")
    count = cursor.fetchone()[0]
    return count