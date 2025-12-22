from src.config.base import BaseConfig
from src.utils.logging import log

import mysql.connector
import traceback

# Global cache for database connections
connection_cache = {}

class Database:
    @staticmethod
    def get_mysql_connection(db_name: str="main"):
        """Establishes and returns a MySQL connection, reusing existing connections if available."""
        try:
            db_details = BaseConfig.get_db_configuration_details(db_name=db_name, db_type="mysql")

            host, username, secret_name = db_details.get("host"), db_details.get("username"), db_details.get("secret_name")
            password, database = db_details.get("password"), db_details.get("dbname")

            log("get_mysql_connection success", host=host, username=username, database=database)

            connection = mysql.connector.connect(host=host, user=username, password=password, database=database)
            # Store connection in cache
            connection_cache[secret_name] = connection

            return connection_cache[secret_name]

        except Exception as e:
            log("get_mysql_connection failed", level="ERROR", error=str(e))
            log(traceback.format_exc(), level="ERROR")
            return None

    @staticmethod
    def get_mysql_cursor(connection):
        """Creates and returns a MySQL cursor."""
        try:
            cursor = connection.cursor(buffered=True, dictionary=True)
            return cursor
        
        except Exception:
            log("get_mysql_cursor failed", level="ERROR", error=str(e))
            log(traceback.format_exc(), level="ERROR")
            return None

    @staticmethod
    def execute(query: str = "", params={}, cursor=None) -> None:
        """Executes a query without returning results."""
        try:
            cursor.execute(query, params)
            return True

        except Exception as e:
            log("execute failed", level="ERROR", error=str(e))
            return False

    @staticmethod
    def fetch(cursor=None, query: str = "", params={}):
        """Executes a query and fetches all rows."""
        try:
            cursor.execute(query, params)
            results = cursor.fetchall()

            return results

        except Exception:
            print(f"Failed to fetch data:\n{traceback.format_exc()}")
            return []

    @staticmethod
    def fetchone(cursor=None, query: str = "", params={}):
        """Executes a query and fetches a single row."""
        try:
            cursor.execute(query, params)
            result = cursor.fetchone()

            return result

        except Exception as e:
            log("fetchone failed", level="ERROR", error=str(e))
            log(traceback.format_exc(), level="ERROR")
            return None

    @staticmethod
    def close_connection(db_name: str="main"):
        """Closes the MySQL connection and removes it from the cache."""
        db_details = BaseConfig.get_db_configuration_details(db_name=db_name, db_type="mysql")

        secret_name = db_details.get("secret_name")
    
        if secret_name in connection_cache:
            connection_cache[secret_name].close()
            del connection_cache[secret_name]