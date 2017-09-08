import falcon
from falcon import Response, Request
import asyncio
import asyncpg
import time
import cProfile


from sql import del_table, create_meteo_data

def profile(func):
    """Decorator for run function profile"""
    def wrapper(*args, **kwargs):
        profile_filename = func.__name__ + '.prof'
        profiler = cProfile.Profile()
        result = profiler.runcall(func, *args, **kwargs)
        res = profiler.create_stats()
        profiler.print_stats('time')
        return result
    return wrapper


def wh(num, text="-"):
    if not wh.i:
        while num < 1:
            num *= 10
            wh.i += 1
    else:
        num *= (10 ** wh.i)
    print("{:6.3f}".format(num), text)
wh.i = 0

async def main(key, pool, meteo):
        async with pool.acquire() as con:
            # await del_table(con, "meteo_data")
            # await create_meteo_data(con)

            for val in key.split():
                await meteo.fetch(*list(map(int, val.split(','))))

async def get_pool():
    pool = await asyncpg.create_pool(database="test05", user="test05", password="11111111", host="localhost", port="5432")
    async with pool.acquire() as con:
        meteo = await con.prepare(
            """INSERT INTO meteo_data (device_id, unix_timestamp, event_id, temp, pressure) VALUES ($1, $2, $3, $4, $5);""")
    return pool, meteo


class ThingsResource:

    def __init__(self):
        loop1 = asyncio.get_event_loop()
        self.pool, self.meteo = loop1.run_until_complete(get_pool())
        self.n = 0
        self.count = 0
        self.time = time.time()

    # @profile
    def on_post(self, req: Request, resp: Response):
        self.n += 1
        if self.n == 100:
            self.count += self.n
            start = time.time()
            delt = start - self.time
            self.time = start
            print('p/s: {:.3f}  count: {}'.format(self.n/delt, self.count))
            self.n = 0
        quer = req.bounded_stream.read().decode()
        fut = asyncio.ensure_future(main(quer, self.pool, self.meteo))

        loop = asyncio.get_event_loop()
        loop.run_until_complete(fut)

        resp.body = "[OK]"
        resp.status = falcon.HTTP_200


app = falcon.API()
things = ThingsResource()
app.add_route('/things', things)

if __name__ == '__main__':
    pass