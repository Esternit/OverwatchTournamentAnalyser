from bs4 import BeautifulSoup
from data.config import config

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

        return result
    
    def parse_match_page(self, html):
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

        return result