import psycopg2
from faker import Faker
import random
import time

fake = Faker()

def wait_for_psql():
    while True:
        try:
            conn=psycopg2.connect(
                host='postgresql',
                port=5432,
                user='admin',
                password='admin',
                dbname='myapp_data'
            )
            conn.close()
            print('psql is ready!')
            break
        except PermissionError as e:
            print('psql is not ready yet....')
            time.sleep(5)

def insert_fake_data(n,cur):
    if not cur:
        return None
    for _ in range(n):
        name=fake.name()
        address=fake.address().replace('\n',', ')
        comment=fake.text().replace('\n',', ')
        price = round(random.uniform(0.00, 99.99), 2)
        cur.execute(
            """
            INSERT INTO mock_data (name, address, comment, price)
            VALUES (%s, %s, %s, %s)
            """,
            (name, address, comment, price)
        )
    print(f'{n} number of data has been inserted into database!')

def main(n=100):
    wait_for_psql()

    try:
        conn=psycopg2.connect(
            host='postgresql',
            port=5432,
            user='admin',
            password='admin',
            dbname='myapp_data'
        )
        cur=conn.cursor()
        insert_fake_data(n,cur)
        conn.commit()
        conn.close()
    except Exception as e:
        print('database connection has been failed!')

if __name__=="__main__":
    main(200)