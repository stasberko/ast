async def create_obd_data(cursor, ):
    await cursor.execute("CREATE TABLE obd_data\
                (cat_id SERIAL PRIMARY KEY,\
                device_id SMALLINT,\
                unix_timestamp INTEGER,\
                event_id SMALLINT,\
                pid INTEGER,\
                value INTEGER);")
    return True


async def create_imu_data(cursor):
    await cursor.execute("CREATE TABLE imu_data\
                (cat_id SERIAL PRIMARY KEY,\
                device_id SMALLINT,\
                unix_timestamp INTEGER,\
                event_id SMALLINT,\
    \
                acc_x INTEGER,\
                acc_y INTEGER,\
                acc_z INTEGER,\
                mag_x INTEGER,\
                mag_y INTEGER,\
                mag_z INTEGER,\
                gyro_xangle INTEGER,\
                gyro_yangle INTEGER,\
                gyro_zangle INTEGER);")
    return True


async def create_meteo_data(cursor):
    await cursor.execute("CREATE TABLE meteo_data\
                (cat_id SERIAL PRIMARY KEY,\
                device_id SMALLINT,\
                unix_timestamp INTEGER,\
                event_id SMALLINT,\
    \
                temp INTEGER,\
                pressure INTEGER);")
    return True


async def create_gps_data(cursor):
    await cursor.execute("CREATE TABLE gps_data\
                (cat_id SERIAL PRIMARY KEY,\
                device_id SMALLINT,\
                unix_timestamp INTEGER,\
                event_id SMALLINT,\
    \
                latitude VARCHAR,\
                longitude VARCHAR,\
                attitude VARCHAR,\
                track INTEGER);")
    return True


async def del_table(cursor, name):
    sql = "DROP TABLE %s;" % (name)
    await cursor.execute(sql)
    return True


async def create_plan(cur, name=None):
    pass


async def insert(cursor, table="meteo_data", *args):
    await cursor.execute(
        """INSERT INTO meteo_data (device_id, unix_timestamp, event_id, temp, pressure) VALUES ($1, $2, $3, $4, $5);""",
        1111, 2222, 3333, 4444, 5555)
    return True


# import psycopg2
#
# tables = 'obd_data', 'imu_data', 'meteo_data', 'gps_data'
# plan_name = ("obd_plan", "imu_plan", "meteo_plan", "gps_plan")
# conn = psycopg2.connect(dbname="test_db", user="suser", password="password", host="localhost", port="5432")
# cur = conn.cursor()
#
# res = cur.execute(
#     "PREPARE %s AS "
#     "INSERT INTO meteo_data (device_id, unix_timestamp, event_id, temp, pressure) VALUES ($1, $2, $3, $4, $5);",
#     ("weqw",))
# print(res)
#
# # create_meteo_data(cur)
# # insert(cur)
# conn.commit()
# cur.close()
# conn.close()



import asyncio
import asyncpg
import time


async def main():
    conn = await asyncpg.connect(database="test05", user="test05", password="11111111", host="localhost", port="5432")
    # await del_table(conn, "meteo_data")
    await create_meteo_data(conn)
    # await insert(conn)
    meteo = await conn.prepare(
        """INSERT INTO meteo_data (device_id, unix_timestamp, event_id, temp, pressure) VALUES ($1, $2, $3, $4, $5);""")
    # await del_table(conn, 'meteo_data')
    await conn.close()


# fut = asyncio.ensure_future(main())  # type : asyncio.Future
# asyncio.get_event_loop().run_until_complete(fut)

# asyncio.get_event_loop().run_until_complete(main())
# print(time.time())
