import falcon
from falcon import Response, Request
import asyncio
import asyncpg
import time
import cProfile


def profile(func):
    """Decorator for run function profile"""

    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        result = profiler.runcall(func, *args, **kwargs)
        res = profiler.create_stats()
        profiler.print_stats('time')
        return result

    return wrapper


async def main(key):
    # await del_table(con, "meteo_data")
    # await create_meteo_data(con)
    conn = await asyncpg.connect(database="test05", user="test05", password="11111111", host="localhost", port="5432")
    meteo = await conn.prepare(
        """INSERT INTO meteo_data (device_id, unix_timestamp, event_id, temp, pressure) VALUES ($1, $2, $3, $4, $5);""")
    tr = conn.transaction()
    await tr.start()

    try:
        for val in key.split():
            await meteo.fetch(*list(map(int, val.split(','))))
    except:
        await tr.rollback()
        print("!!!!!!!!!!!!!!!!!roll trnasaction")

        raise
    finally:
        await tr.commit()
        print("end trnasaction")
    await conn.close()


class ThingsResource:
    def __init__(self):
        pass
        # self.loop1 = asyncio.get_event_loop()
        # self.meteo = self.loop1.run_until_complete(get_pool())
        self.n = 0
        self.count = 0
        self.time = time.time()

    # @profile
    def on_post(self, req: Request, resp: Response):
        print(time.time())
        # self.n += 1
        # if self.n == 100:
        #     self.count += self.n
        #     start = time.time()
        #     delt = start - self.time
        #     self.time = start
        #     print('p/s: {:.3f}  count: {}'.format(self.n / delt, self.count))
        #     self.n = 0

        quer = req.bounded_stream.read().decode()
        fut = asyncio.ensure_future(main(quer))
        loop = asyncio.get_event_loop()

        loop.run_until_complete(fut)
        print(time.time())

        resp.body = "[OK]"
        resp.status = falcon.HTTP_200
        print(time.time())


app = falcon.API()
things = ThingsResource()
app.add_route('/things', things)

if __name__ == '__main__':
    pass
