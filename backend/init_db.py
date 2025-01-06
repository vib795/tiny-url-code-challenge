import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import time
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_config():
    return {
        'host': 'postgres',
        'admin_user': os.getenv('POSTGRES_USER'),
        'admin_password': os.getenv('POSTGRES_PASSWORD'),
        'admin_db': os.getenv('POSTGRES_DB'),
        'app_db': os.getenv('POSTGRES_DB_NAME'),
        'app_user': os.getenv('POSTGRES_APP_USER'),
        'app_password': os.getenv('POSTGRES_APP_PASSWORD')
    }

def wait_for_db():
    config = get_db_config()
    while True:
        try:
            conn = psycopg2.connect(
                dbname=config['admin_db'],
                user=config['admin_user'],
                password=config['admin_password'],
                host=config['host']
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
            
            cursor.execute(f"SELECT 1 FROM pg_database WHERE datname='{config['app_db']}'")
            if cursor.fetchone() is None:
                print(f"Creating database {config['app_db']}...")
                cursor.execute(f"CREATE DATABASE {config['app_db']}")
                print("Database created!")
            
            cursor.execute(f"SELECT 1 FROM pg_roles WHERE rolname='{config['app_user']}'")
            if cursor.fetchone() is None:
                print(f"Creating user {config['app_user']}...")
                cursor.execute(f"CREATE USER {config['app_user']} WITH PASSWORD '{config['app_password']}'")
                print("User created!")
            
            # Grant privileges
            cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {config['app_db']} TO {config['app_user']}")
            
            # Connect to database to set up schema privileges
            conn.close()
            conn = psycopg2.connect(
                dbname=config['app_db'],
                user=config['admin_user'],
                password=config['admin_password'],
                host=config['host']
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
            
            # Grant schema privileges
            cursor.execute(f"GRANT ALL ON SCHEMA public TO {config['app_user']}")
            cursor.execute(f"GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO {config['app_user']}")
            cursor.execute(f"ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO {config['app_user']}")
            
            print("Database initialization completed successfully!")
            break
            
        except psycopg2.OperationalError as e:
            print(f"Waiting for database... {e}")
            time.sleep(2)
        except Exception as e:
            print(f"Error initializing database: {e}")
            raise e
        finally:
            try:
                if conn:
                    conn.close()
            except:
                pass

if __name__ == "__main__":
    wait_for_db()