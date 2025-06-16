import asyncio

from data.logger import Logger
from data_worker_app.data_converter import normalize_matches_info, convert_player_ids, final_converter
from parser_app.utils import main_utils

logger = Logger(__name__) 


if __name__ == "__main__":
    final_converter()
    # asyncio.run(main_utils()) 

    