from pathlib import Path
import json

from parser_app.crawler import AnakCrawler
from parser_app.parser import Parser
from data.logger import Logger

logger = Logger(__name__) 

async def main ():
    crawler = AnakCrawler()
    parser = Parser()

    # tournaments = await fetch_tournaments(crawler, parser)
    # matches = await fetch_matches(crawler, parser, tournaments)
    # matches = await checker(crawler, parser, config.TOTAL_MATCHES_COUNT)
    # await fetch_teams_info(crawler, parser)

async def fetch_tournaments(crawler, parser):
    html = await crawler.fetch_main()
    tournaments = parser.parse_tournaments_page(html)
    tournaments = tournaments[::-1]

    save_json("tournaments", tournaments)

    return tournaments

async def fetch_matches(crawler, parser, tournaments):
    tournament_matches = {}

    for i in range(len(tournaments)):
        number = i + 1
        page = 1
        all_matches = []

        while True:
            html = await crawler.fetch_matches_page(number, page)
            matches = parser.parse_matches_page(html)

            if not matches:
                break

            all_matches += matches
            page += 1

        if all_matches != []:
            tournament_matches[tournaments[i]["name"]] = all_matches
            logger.info(f"Saved matches for {tournaments[i]['name']} {len(all_matches)}")


    save_json(f"matches", tournament_matches)

    return tournament_matches

async def fetch_matches_info(crawler, parser):
    all_matches = load_json("matches")

    matches_info = {}
    match_id = 1

    for tournament in all_matches:
        matches_from_json = all_matches[tournament][::-1]
        for i in range(len(matches_from_json)):
            html = await crawler.fetch_match_page(match_id)
            match = parser.parse_match_page(html)

            matches_info[match_id] = match
            match_id += 1

        logger.info(f"Parsed {len(matches_from_json)} matches for {tournament}")

    save_json(f"matches_info", matches_info)

async def fetch_teams_info(crawler, parser):
    all_tournaments = load_json("tournaments")

    teams_info = {}

    for i in range(len(all_tournaments)):
        number = i + 1
        html = await crawler.fetch_teams_page(number)
        teams = parser.parse_tournament_team_info(html)

        teams_info[all_tournaments[i]["name"]] = teams

        logger.info(f"Parsed {len(teams)} teams for {all_tournaments[i]['name']}")

    save_json(f"teams_info", teams_info)

def save_json(name, file):
    output_path = Path(f"data/json/{name}.json")
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(file, f, ensure_ascii=False, indent=4)
    
    logger.info(f"Saved {name} to {output_path}")

async def checker(crawler, parser, max_id):
    matches_info = load_json("matches_info_old")
    match_id = 1

    while match_id <= max_id:
        if str(match_id) not in matches_info:
            html = await crawler.fetch_match_page(match_id)
            match = parser.parse_match_page(html)

            matches_info[match_id] = match

            logger.info(f"Parsed {match_id}")
        
        match_id += 1

    save_json(f"matches_info", matches_info)

def load_json(name):
    input_path = Path(f"data/json/{name}.json")
    
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.info(f"Loaded {name} from {input_path}")
        return data
    except FileNotFoundError:
        logger.warning(f"File {input_path} not found!")
        return None
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in {input_path}!")
        return None


    