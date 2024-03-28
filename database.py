import psycopg2

# данные от локальной базы данных
dbhost = "localhost"
dbuser = "postgres"
dbpassword = "123"
dbdatabase = "postgres"

#получаем из базы данных данные зарегистрировавшегося пользователя
def getuser(login, password):
    connection = psycopg2.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbdatabase)
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, surname, lastname, role FROM adminka WHERE login = '" + login + "' and password = '" + password + "'")
    result = cursor.fetchall()
    connection.close()
    if len(result) == 0:
        return None
    else:
        return result[0]



#получаем из бд пациентов
def getpatients(id = None):
    connection = psycopg2.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbdatabase)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT surname, name, lastname, medical_policy, birthday FROM patients")
    result = cursor.fetchall()
    connection.close()
    if len(result) == 0:
        return None
    else:
        return result

#добавляем в базу данных карточку пациента
def add_patient(executor, patient):
    connection = psycopg2.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbdatabase)
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO patients (id, surname, name, lastname, medical_policy, birthday) VALUES (DEFAULT, '"+patient[0]+"', '"+patient[1]+"', '"+patient[2]+"', '"+patient[3]+"', '"+patient[4]+"')")
    connection.commit()
    cursor.execute("SELECT id FROM patients WHERE name = '"+patient[1]+"' AND surname = '"+patient[0]+"' AND lastname = '"+patient[2]+"' AND medical_policy = '"+patient[3]+"' AND birthday = '"+patient[4]+"' ")
    result = cursor.fetchall()
    connection.close()
    db_logs(executor, "add", "patients")
    if not result:
        return False
    else:
        return True

#добавляем в базу данных изменения карточек пациента
def edit_patient_data(executor, patient):
    connection = psycopg2.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbdatabase)
    cursor = connection.cursor()
    cursor.execute("UPDATE patients SET name = '"+patient[0]+"', surname = '"+patient[1]+"', lastname = '"+patient[2]+"', birthday = '"+patient[4]+"' WHERE medical_policy = '"+patient[3]+"' ")
    connection.commit(),
    cursor.execute("SELECT id FROM patients WHERE name = '"+patient[0]+"' AND surname = '"+patient[1]+"' AND lastname = '"+patient[2]+"' AND medical_policy = '"+patient[3]+"' AND birthday = '"+patient[4]+"' ")
    result = cursor.fetchall()
    connection.close()
    db_logs(executor, "edit", "patients")
    if not result:
        return False
    else:
        return True

#удаляем из базы данных карточку пациента
def db_delete_patient(executor, patient_med_policy):
    connection = psycopg2.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbdatabase)
    cursor = connection.cursor()
    cursor.execute(
        "DELETE FROM patients WHERE medical_policy = '"+ str(patient_med_policy) +"'")
    connection.commit()
    cursor.execute("SELECT id FROM patients WHERE medical_policy = '"+ str(patient_med_policy) +"' ")
    result = cursor.fetchall()
    connection.close()
    db_logs(executor, "delete", "patients")
    if not result:
        return True
    else:
        return False



#получаем из бд записи
def getnotes(id = None):
    connection = psycopg2.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbdatabase)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT id, fio, policy, fio_doctor, doctor, date_note  FROM notes")
    result = cursor.fetchall()
    connection.close()
    if len(result) == 0:
        return None
    else:
        return result

#получаем из бд фио пациента
def db_get_fio_patient(policy):
    connection = psycopg2.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbdatabase)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT surname, name, lastname FROM patients WHERE medical_policy = '" + policy + "'")
    result = cursor.fetchall()
    connection.close()
    if len(result) == 0:
        return None
    else:
        return result

#получаем список врачей
def db_get_doctors():
    connection = psycopg2.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbdatabase)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT id, name, surname, lastname, specialist FROM doctors ORDER BY specialist")
    result = cursor.fetchall()
    connection.close()
    if len(result) == 0:
        return None
    else:
        return result

#добавляем в базу данных запись к врачу
def db_add_note(executor, note):
    connection = psycopg2.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbdatabase)
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO notes (id, fio, doctor, fio_doctor, date_note, policy) VALUES (DEFAULT, '"+note[0]+"', '"+note[1]+"', '"+note[2]+"', '"+note[3]+"', '"+note[4]+"')")
    connection.commit()
    cursor.execute("SELECT policy, fio_doctor FROM notes ORDER BY ID DESC LIMIT 1")
    result = cursor.fetchall()
    connection.close()
    db_logs(executor, "add", "notes")
    if result[0][0] == note[4] and result[0][1] == note[2]:
        return True
    else:
        return False

#добавляем в базу данных изменения записи к врачу
def edit_note_data(executor, note_id, datetime):
    connection = psycopg2.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbdatabase)
    cursor = connection.cursor()
    cursor.execute("UPDATE notes SET date_note = '"+datetime+"' WHERE id = '"+str(note_id)+"' ")
    connection.commit()
    cursor.execute("SELECT id FROM notes WHERE id = '"+str(note_id)+"' AND date_note = '"+datetime+"'")
    result = cursor.fetchall()
    connection.close()
    db_logs(executor, "edit", "notes")
    if not result:
        return False
    else:
        return True

#удаляем из базы данных запись к врачу
def db_delete_note(executor, note_id):
    connection = psycopg2.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbdatabase)
    cursor = connection.cursor()
    cursor.execute(
        "DELETE FROM notes WHERE id = '" + str(note_id) + "'")
    connection.commit()
    cursor.execute("SELECT id FROM notes WHERE id = '" + str(note_id) + "' ")
    result = cursor.fetchall()
    connection.close()
    db_logs(executor, "delete", "notes")
    if not result:
        return True
    else:
        return False



#получаем из бд работников
def getworker(id = None):
    connection = psycopg2.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbdatabase)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT surname, name, lastname, role, login, password FROM adminka")
    result = cursor.fetchall()
    connection.close()
    if len(result) == 0:
        return None
    else:
        send_info = []
        for item in result:
            info = [item[0], item[1], item[2]]
            if item[3] == "intern": info.append("Стажер")
            elif item[3] == "worker": info.append("Работник")
            elif item[3] == "admin": info.append("Администратор")
            elif item[3] == "root": info.append("гл.Администратор")
            info.append(item[4]); info.append(item[5])
            send_info.append(info)
        return send_info

#добавляем в базу данных работника
def db_add_worker(executor,worker):
    connection = psycopg2.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbdatabase)
    cursor = connection.cursor()
    if worker[3] == "Стажер": role = "intern"
    elif worker[3] == "Работник": role = "worker"
    elif worker[3] == "Администратор": role = "admin"
    elif worker[3] == "гл.Администратор": role = "root"
    cursor.execute(
        "INSERT INTO adminka (id, surname, name, lastname, role, login, password) VALUES (DEFAULT, '"+worker[0]+"', '"+worker[1]+"', '"+worker[2]+"', '"+role+"', '"+worker[4]+"', '"+worker[5]+"')")
    connection.commit()
    cursor.execute("SELECT login FROM adminka WHERE name = '"+worker[1]+"' AND surname = '"+worker[0]+"' AND lastname = '"+worker[2]+"' AND role = '"+role+"' AND login = '"+worker[4]+"' AND password = '"+worker[5]+"' ")
    result = cursor.fetchall()
    connection.close()
    if not result:
        return False
    else:
        return True

#добавляем в базу данных изменения данных работника
def edit_worker_data(executor, worker):
    connection = psycopg2.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbdatabase)
    cursor = connection.cursor()
    cursor.execute("UPDATE adminka SET name = '"+worker[0]+"', surname = '"+worker[1]+"', lastname = '"+worker[2]+"', role = '"+worker[3]+"', password = '"+worker[5]+"' WHERE login = '"+worker[4]+"' ")
    connection.commit(),
    cursor.execute("SELECT login FROM adminka WHERE name = '"+worker[0]+"' AND surname = '"+worker[1]+"' AND lastname = '"+worker[2]+"' AND role = '"+worker[3]+"' AND login = '"+worker[4]+"' AND password = '"+worker[5]+"' ")
    result = cursor.fetchall()
    connection.close()
    if not result:
        return False
    else:
        return True

#удаляем из базы данных работника
def db_delete_worker(executor, worker_login):
    connection = psycopg2.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbdatabase)
    cursor = connection.cursor()
    cursor.execute(
        "DELETE FROM adminka WHERE login = '"+ str(worker_login) +"'")
    connection.commit()
    cursor.execute("SELECT id FROM adminka WHERE login = '"+ str(worker_login) +"' ")
    result = cursor.fetchall()
    connection.close()
    if not result:
        return True
    else:
        return False



#запись любых действий пользователя в таблицу с изменениями
def db_logs(executor, action, table):
    connection = psycopg2.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbdatabase)
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO logs (executor, action, \"table\") VALUES ('"+ str(executor) +"', '"+ action +"', '"+ table +"')")
    connection.commit()
    connection.close()

#получить данные о количестве изменений определенной таблицы
def getlogs(action, table, gap):
    connection = psycopg2.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbdatabase)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT time FROM logs WHERE time > '"+ str(gap) +"' and action = '"+ action +"' and \"table\" = '"+ table +"'")
    connection.commit()
    result = cursor.fetchall()
    connection.close()
    return len(result)

#получить данные о возрасте пациентов
def patients_age(gap, end_gap = None, old = False):
    connection = psycopg2.connect(host=dbhost, user=dbuser, password=dbpassword, database=dbdatabase)
    cursor = connection.cursor()
    if end_gap == None and not old:
        cursor.execute(
            "SELECT id FROM patients WHERE birthday > '"+ str(gap) +"' ")
    elif old:
        cursor.execute(
            "SELECT id FROM patients WHERE birthday < '" + str(gap) + "' ")
    else:
        cursor.execute(
            "SELECT id FROM patients WHERE birthday < '" + str(gap) + "' and birthday > '" + str(end_gap) +"' ")
    connection.commit()
    result = cursor.fetchall()
    connection.close()
    return len(result)



# if __name__ == '__main__':
#     today = datetime.date.today()

