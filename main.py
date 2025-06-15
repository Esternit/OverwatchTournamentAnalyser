import asyncio
from pathlib import Path
import json

from parser_app.crawler import AnakCrawler
from parser_app.parser import Parser
from data.logger import Logger

logger = Logger(__name__) 

async def main ():
    crawler = AnakCrawler()
    parser = Parser()

    html = await crawler.fetch_main()
    tournaments = parser.parse_tournaments_page(html)
    tournaments = tournaments[::-1]

    save_json("tournaments", tournaments)

    tournament_matches = {}

    for i in range(len(tournaments)):
        number = i + 1
        page = 1
        all_matches = []

        while True:
            html = await crawler.fetch_matches_page(number, page)
            matches = parser.parse_match_page(html)

            if not matches:
                break

            all_matches += matches
            page += 1

        if all_matches != []:
            tournament_matches[tournaments[i]["name"]] = all_matches
            logger.info(f"Saved matches for {tournaments[i]['name']} {len(all_matches)}")


    save_json(f"matches", tournament_matches)
def save_json(name, file):
    output_path = Path(f"data/json/{name}.json")
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(file, f, ensure_ascii=False, indent=4)
    
    logger.info(f"Saved {name} to {output_path}")

if __name__ == "__main__":
    asyncio.run(main())

    