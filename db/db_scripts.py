from db.db_service import Database


class DBHelper:
    create_db_sql = '''CREATE DATABASE business_apps'''
    use_db_sql = '''USE business_apps'''
    create_table_sql = '''CREATE TABLE apps_data (
                        id INT NOT NULL AUTO_INCREMENT, 
                        business_app_name VARCHAR(255), 
                        company_name VARCHAR(255), 
                        release_year VARCHAR(255), 
                        email VARCHAR(255), 
                        PRIMARY KEY (id)
                        )'''
    insert_data_sql = """INSERT INTO apps_data (business_app_name, company_name, release_year, email) 
                        VALUES (%s, %s, %s, %s)"""

    @classmethod
    def create_database(cls):
        db.execute(sql=cls.create_db_sql)

    @classmethod
    def create_table(cls):
        db.execute(sql=cls.use_db_sql)
        db.execute(sql=cls.create_table_sql)

    @classmethod
    def insert_data_into_table(cls, data):
        db = Database("business_apps")
        for item in data:
            db.execute(cls.insert_data_sql, (item['business_app_name'],
                                             item['company_name'],
                                             item['release_year'],
                                             item['email']))

        db.commit()
        db.close()


if __name__ == '__main__':
    db = Database("business_apps")
    DBHelper.create_database()
    DBHelper.create_table()
