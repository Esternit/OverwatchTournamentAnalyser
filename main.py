import asyncio

from data.logger import Logger
from parser_app.utils import main

logger = Logger(__name__) 


if __name__ == "__main__":
    asyncio.run(main())

    