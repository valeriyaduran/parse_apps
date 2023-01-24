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