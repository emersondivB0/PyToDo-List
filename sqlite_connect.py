# CRUD with PyQt5 and SQLite3

import sqlite3

class Communication():
    def __init__(self):
        self.connection = sqlite3.connect('todo_list_py.db')
        # Creación de la tabla
        conn.execute('''CREATE TABLE IF NOT EXISTS tasks
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    NAME TEXT NOT NULL,
                    DESCRIPTION TEXT NOT NULL,
                    END_DATE DATE NOT NULL,
                    FINISHED INTEGER NOT NULL DEFAULT 0);''')


    # Funciones para manejar las tareas
    def add_task(self, name, description, end_date, finished):
        cursor = self.connection.cursor()
        try:
            end_date = datetime.strptime(end_date,
                                              "%d/%m/%Y").date()
        except ValueError:
            messagebox.showerror("Error",
                             "Wrong date format (DD/MM/AAAA)")
            return
        query = "INSERT INTO tasks (NAME, DESCRIPTION, END_DATE, FINISHED) VALUES (?, ?, ?, ?)".format(name, description, end_date,finished)
        cursor.execute(query)
        conn.commit()
        cursor.close()



    def show_tasks(self):
        cursor = self.connection.cursor()
        query = "SELECT * FROM tasks"
        cursor.execute(query)
        tasks = cursor.fetchall()
        return tasks
        #cursor.close()

    def search_task(self, name):
        cursor = self.connection.cursor()
        query = "SELECT * FROM tasks WHERE NAME = ?".format(name_task)
        cursor.execute(query)
        nameX= cursor.fetchall()
        cursor.close()
        return nameX

    def delete_task(self, name):
        cursor = self.connection.cursor()
        query = "DELETE FROM tasks WHERE NAME = ?".format(name)
        cursor.execute(query)
        self.connection.commit()
        cursor.close()


    def edit_task(self, name, description, end_date, finished):
        cursor = self.connection.cursor()
        query = "UPDATE tasks SET NOMBRE = ?, DESCRIPTION = ?, END_DATE = ?, FINISHED = ? WHERE NAME = ?".format(name, description, end_date, finished)
        cursor.execute(query)
        a = cursor.rowcount
        self.connection.commit()
        cursor.close()
        return a
        
