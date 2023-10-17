
import psycopg2
from psycopg2 import sql

from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


dbname = os.getenv("POSTGRES_DB")
password = os.getenv("POSTGRES_PASSWORD")
user = os.getenv("POSTGRES_USER")

trigger = f'''
CREATE OR REPLACE FUNCTION notify_trigger() RETURNS TRIGGER AS $$
BEGIN
  PERFORM pg_notify('new_token', NEW.id::text);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER new_token_trigger
AFTER INSERT OR UPDATE OR DELETE ON bot
FOR EACH ROW
EXECUTE FUNCTION notify_trigger();
'''

try:
    # Подключение к существующей базе данных
    connection = psycopg2.connect(f"dbname={dbname} user={user} password={password} host=db port=5432")
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()

    cursor.execute(trigger)
except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")
