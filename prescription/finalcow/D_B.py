import mysql.connector as connector






class DB:
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(DB)
            return cls.instance
        return cls.instance

    def __init__(self):
        self.config = {
                'user': 'root',
                'password': '',
                'host': '127.0.0.1',
                'database': 'django2_db'
                }
        self.conn = self.connect()
        self.cursor = self.conn.cursor()
        
    # def __del__(self):
    #     self.cursor.close()
    #     self.conn.close()

    def connect(self):
        try:
            return connector.connect(**self.config)
        except connector.Error as e:
            print(e)

    def close(self):
        self.cursor.close()
        self.conn.close()
    
    
    
    
    
    def select(self, fields, table):
        SQL= (f'SELECT {fields} FROM {table} ')
        self.cursor.execute(SQL)
        res= [name[0] for name in self.cursor]
        
        # self.close()
            
        return res
    
    def insert(self, table_name, column_names, values):
        query = "INSERT INTO {} ({}) VALUES ({});".format(table_name, column_names, ",".join(["%s"]*len(values)))
        try:
            self.cursor.execute(query, values)
        except connector.Error as e:
                print(e)
        self.conn.commit()
        return self.cursor.lastrowid
    
    
    
    def raw(self,row,data):
        # if not where:
        SQL= (row)%data
        
        print('HOW'*50)
        print(SQL)
        try:
            self.cursor.execute(SQL)
        except connector.Error as e:
            print(e)
        
        

        self.conn.commit()
        
    





