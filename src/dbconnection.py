class DatabaseConnection:
    def __init__(self, username, password, host='localhost', database='your_database'):
        self.username = username
        self.password = password
        self.host = host
        self.database = database
        self.connection = None

    def connect(self):
        import mysql.connector  # or use psycopg2 for PostgreSQL
        try:
            self.connection = mysql.connector.connect(
                user=self.username,
                password=self.password,
                host=self.host,
                database=self.database
            )
            print("Connection established.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.connection = None

    def close(self):
        if self.connection:
            self.connection.close()
            print("Connection closed.")