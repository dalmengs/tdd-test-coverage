from prisma import Prisma

class DatabaseRepository:
    client = Prisma()

    @staticmethod
    async def connect():
        await DatabaseRepository.client.connect() # pragma: no cover

    @staticmethod
    def get_client():
        return DatabaseRepository.client
