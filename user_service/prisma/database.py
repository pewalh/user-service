from prisma import Prisma


# create a database connection for dependency injection into endpoints
# placed here to prepare for possible future extensions

async def get_db():
    async with Prisma() as db:
        yield db
    

