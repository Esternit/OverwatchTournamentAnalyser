import asyncio

from data.logger import Logger
from parser_app.utils import main
from data_worker_app.data_converter import normalize_matches_info, convert_player_ids, final_converter

logger = Logger(__name__) 


if __name__ == "__main__":
    final_converter()

    