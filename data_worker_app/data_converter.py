from json_worker import load_json, save_json
from data.config import config
from data.logger import Logger

logger = Logger(__name__)

def normalize_matches_info():
    matches = load_json("matches")
    matches_info = load_json("matches_info")
    teams_info = load_json("teams_info")
    new_matches_info = {}

    match_num = 1

    previous_not_found = 0

    for tournament in matches:
        mathces_from_json = matches[tournament][::-1]
        i = 0

        first  = True

        while i < len(mathces_from_json):
            old_match = matches_info[str(match_num)]

            if not old_match:
                logger.warning(f"Match {match_num} not found in matches_info")
                
                if match_num == 3842 or match_num == 3924 or match_num == 3848:
                    i += 1
            else:
                if not match_checker(old_match, mathces_from_json[i]):
                    logger.warning(f"Match {match_num} is not valid")
                else:
                    new_matches_info[match_num] = {
                        "group": mathces_from_json[i]["group"],
                        "team_1_name": mathces_from_json[i]["team1"],
                        "team_2_name": mathces_from_json[i]["team2"],
                        "team_1_score": mathces_from_json[i]["team1_score"],
                        "team_2_score": mathces_from_json[i]["team2_score"],
                        "team_1_avg_sr": find_avg_sr(teams_info, mathces_from_json[i]["team1"], tournament),
                        "team_2_avg_sr": find_avg_sr(teams_info, mathces_from_json[i]["team2"], tournament),
                        "tournament": tournament,
                        "teams": clear_name(old_match)
                    }
                
                i+=1
            match_num += 1

    save_json("matches_info_full", new_matches_info)


def match_checker(teams_json, matches_info_json):
    if teams_json[0]["name"] == matches_info_json["team1"] and teams_json[1]["name"] == matches_info_json["team2"]:
        return True
    
    elif teams_json[0]["name"] == matches_info_json["team2"] and teams_json[1]["name"] == matches_info_json["team1"]:
        return True
    
    return False

def find_avg_sr(teams_json, team_name, tournament):
    for team in teams_json[tournament]:
        if team["name"] == team_name:
            return team["avg. sr"]

def clear_name(teams):
    for i in range(len(teams)):
        for j in range(len(teams[i]["players"])):
            teams[i]["players"][j]["name"] = teams[i]["players"][j]["name"].split('-')[0]

    return teams

def convert_player_ids():
    matches_full_info = load_json("matches_info_full")

    result = {}

    for match in matches_full_info:
        for team in matches_full_info[match]["teams"]:
            for player in team["players"]:
                if player["name"] not in result:
                    result[player["name"]] = len(result) + 1

    save_json("player_ids", result)

def final_converter():
    matches_full_info = load_json("matches_info_full")
    player_ids = load_json("player_ids")

    result = []

    for match in matches_full_info:
        for team in matches_full_info[match]["teams"]:
            for player in team["players"]:
                result.append({
                    "id":  len(result) + 1,
                    "player_id": player_ids[player["name"]],
                    "role": player["role"],
                    "is_new": player["is_new"],
                    "is_new_role": player["is_new_role"],
                    "division": player["division"],
                    "team_avg_sr": matches_full_info[match]["team_1_avg_sr"] if team["name"] == matches_full_info[match]["team_1_name"] else matches_full_info[match]["team_2_avg_sr"],
                    "opponent_avg_sr": matches_full_info[match]["team_2_avg_sr"] if team["name"] == matches_full_info[match]["team_1_name"] else matches_full_info[match]["team_1_avg_sr"],
                    "taget": matches_full_info[match]["team_1_score"] > matches_full_info[match]["team_2_score"] if team["name"] == matches_full_info[match]["team_1_name"] else matches_full_info[match]["team_2_score"] > matches_full_info[match]["team_1_score"],
                })

    save_json("data", result)