from bs4 import BeautifulSoup

from data.config import config
from data.logger import Logger

logger = Logger(__name__) 

class Parser:
    def __init__(self):
        pass
    
    def parse_tournaments_page(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        result = []

        try:
            tournaments = soup.find_all('div', class_ = config.TOURNAMENT_CLASS)
            if tournaments:
                for tournament in tournaments:
                    name = tournament.find('h3', class_ = config.TOURNAMENT_NAME_CLASS).text.strip()
                    participants = tournament.find('div', class_ = config.TOURNAMENT_PARTICIPANT_CLASS).text.strip()
                    result.append({"name": name, "participants": participants})

        except Exception as e:
            tournaments = []
            logger.error(e)

        return result
    
    def parse_matches_page(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        result = []

        try:
            matches = soup.find_all('tr', class_ = config.MATCH_CLASS)
            if matches:
                for match in matches:
                    tds = match.find_all('td', class_ = config.MATCH_TD_CLASS)
                    if tds:
                        team_text = tds[0].find("div")
                        group_text = tds[1].find("div")
                        score_text = tds[3].find("div")

                        result.append({
                            "team1": team_text.text.strip().split(" vs ")[0] if team_text else "", 
                            "team2": team_text.text.strip().split(" vs ")[1] if team_text else "",
                            "group": group_text.text.strip() if group_text else "",
                            "team1_score": score_text.text.strip().split("-")[0] if score_text else "",
                            "team2_score": score_text.text.strip().split("-")[1] if score_text else ""
                        })

        except Exception as e:
            matches = []
            logger.error(e)

        return result
    
    def parse_match_page(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        result = []

        try:
            teams = soup.find_all('div', class_ = config.TEAM_CLASS)
            if teams:
                for team in teams:
                    name_container = team.find('div', class_ = config.TEAM_NAME_CLASS)
                    if name_container:
                        name = name_container.find('h3').text.strip()

                        if name:
                            players = team.find_all('tr', class_ = config.TEAM_TR_CLASS)
                                
                            player_result = []
                            for player in players:
                                tds = player.find_all('td')

                                role = self.role_selector(tds[0].find("path")["d"])
                                player_name = tds[0].find("a")["href"].split("/")[-1]
                                division = self.get_division(tds[1].find("img")["src"])
                                is_new = tds[2].find("svg")["class"] == config.CIRCLE_CLASS_PLUS_SVG
                                is_new_role = tds[3].find("svg")["class"] == config.CIRCLE_CLASS_PLUS_SVG

                                player_result.append({
                                    "role": role,
                                    "name": player_name,
                                    "division": division,
                                    "is_new": is_new,
                                    "is_new_role": is_new_role
                                })

                            result.append({
                                "name": name,
                                "players": player_result
                            })

        except Exception as e:
            teams = []
            logger.error(e)

        return result
    
    def role_selector(self, role_svg):
        if role_svg == config.TANK_CLASS_SVG:
            return "tank"
        if role_svg == config.DPS_CLASS_SVG:
            return "dps"
        if role_svg == config.SUPPORT_CLASS_SVG:
            return "support"
    
    def get_division(self, img_src):
        splitted = img_src.split("%")

        for part in splitted:
            if "png" in part:
                return part.split(".")[0].split("F")[1]
        
        return ""