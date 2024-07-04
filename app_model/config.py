from motorhead import AgnosticDatabase


async def create_indexes(database: AgnosticDatabase) -> None:
    from .device.service import DeviceService

    await DeviceService(database).create_indexes()
