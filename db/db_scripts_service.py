from db.db_helper_service import DatabaseHelperService
from db.db_queries import create_db_sql, use_db_sql, create_table_sql, insert_data_sql


class DBScriptsService:
    def __init__(self):
        self._db_helper = DatabaseHelperService("business_apps")

    def create_database(self):
        self._db_helper.execute(sql=create_db_sql)

    def create_table(self):
        self._db_helper.execute(sql=use_db_sql)
        self._db_helper.execute(sql=create_table_sql)

    def insert_data_into_table(self, data):
        for item in data:
            self._db_helper.execute(insert_data_sql, (item["business_app_name"],
                                                      item["company_name"],
                                                      item["release_year"],
                                                      item["email"]))

        self._db_helper.commit()
        self._db_helper.close()


if __name__ == "__main__":
    db_scripts_service = DBScriptsService()
    DBScriptsService.create_database(db_scripts_service)
    DBScriptsService.create_table(db_scripts_service)
