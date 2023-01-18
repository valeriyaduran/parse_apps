from db.db_helper_service import DatabaseHelperService


class DBScriptsService:
    create_db_sql = """CREATE DATABASE business_apps"""
    use_db_sql = """USE business_apps"""
    create_table_sql = """CREATE TABLE apps_data (
                        id INT NOT NULL AUTO_INCREMENT, 
                        business_app_name VARCHAR(255), 
                        company_name VARCHAR(255), 
                        release_year VARCHAR(255), 
                        email VARCHAR(255), 
                        PRIMARY KEY (id)
                        )"""
    insert_data_sql = """INSERT INTO apps_data (business_app_name, company_name, release_year, email) 
                        VALUES (%s, %s, %s, %s)"""

    @classmethod
    def create_database(cls):
        db_helper.execute(sql=cls.create_db_sql)

    @classmethod
    def create_table(cls):
        db_helper.execute(sql=cls.use_db_sql)
        db_helper.execute(sql=cls.create_table_sql)

    @classmethod
    def insert_data_into_table(cls, data):
        db_helper = DatabaseHelperService("business_apps")
        for item in data:
            db_helper.execute(cls.insert_data_sql, (item["business_app_name"],
                                                    item["company_name"],
                                                    item["release_year"],
                                                    item["email"]))

        db_helper.commit()
        db_helper.close()


if __name__ == "__main__":
    db_helper = DatabaseHelperService("business_apps")
    DBScriptsService.create_database()
    DBScriptsService.create_table()
