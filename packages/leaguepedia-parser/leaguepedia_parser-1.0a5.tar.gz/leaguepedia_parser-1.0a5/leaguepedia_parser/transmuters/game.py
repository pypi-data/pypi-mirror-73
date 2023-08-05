import urllib.parse
from datetime import datetime, timezone
from typing import TypedDict

import lol_id_tools as lit
from lol_dto.classes.game import LolGame, LolGameTeam, LolGamePlayer, LolGameTeamEndOfGameStats

from leaguepedia_parser.transmuters.game_players import LeaguepediaPlayerIdentifier


game_fields = {
    "Tournament",
    "Team1",
    "Team2",
    "Winner",
    "Gamelength_Number",
    "DateTime_UTC",
    "Team1Score",
    "Team2Score",
    "Team1Bans",
    "Team2Bans",
    "Team1Picks",
    "Team2Picks",
    "Team1Names",
    "Team2Names",
    "Team1Links",
    "Team2Links",
    "Team1Dragons",
    "Team2Dragons",
    "Team1Barons",
    "Team2Barons",
    "Team1Towers",
    "Team2Towers",
    "Team1RiftHeralds",
    "Team2RiftHeralds",
    "Team1Inhibitors",
    "Team2Inhibitors",
    "Patch",
    "MatchHistory",
    "VOD",
    "Gamename",
    "OverviewPage",
    "ScoreboardID_Wiki",
    "UniqueGame",
}


class LeaguepediaGameIdentifier(TypedDict):
    scoreboardIdWiki: str
    uniqueGame: str
    match_history_url: str


def transmute_game(source_dict: dict) -> LolGame:
    """Transforms a ScoreboardGames row into a LolGame

    Some fields like team gold and kills are not present. Get_game_details should be used for that.
    """
    game = LolGame(
        sources={
            "leaguepedia": LeaguepediaGameIdentifier(
                scoreboardIdWiki=source_dict["ScoreboardID Wiki"],
                uniqueGame=source_dict["UniqueGame"],
                match_history_url=source_dict["MatchHistory"],
            )
        },
        tournament=source_dict["Tournament"],
        start=datetime.fromisoformat(source_dict["DateTime UTC"])
        .replace(tzinfo=timezone.utc)
        .isoformat(timespec="seconds"),
        gameInSeries=int(source_dict["Gamename"].replace("Game ", "")),
        patch=source_dict["Patch"],
        duration=int(float(source_dict["Gamelength Number"]) * 60),
        vod=source_dict["VOD"],
        winner="BLUE" if source_dict["Winner"] == "1" else "RED",
        teams={
            side: LolGameTeam(
                name=source_dict[f"Team{i}"],
                players=[
                    LolGamePlayer(
                        uniqueIdentifiers={
                            "leaguepedia": LeaguepediaPlayerIdentifier(
                                name=source_dict[f"Team{i}Names"].split(",")[idx]
                            )
                        },
                        championId=lit.get_id(champion_name, object_type="champion"),
                        championName=champion_name,
                    )
                    for idx, champion_name in enumerate(source_dict[f"Team{i}Picks"].split(","))
                ],
                bansNames=source_dict[f"Team{i}Bans"].split(","),
                bans=[lit.get_id(champion) for champion in source_dict[f"Team{i}Bans"].split(",")],
                endOfGameStats=LolGameTeamEndOfGameStats(
                    towerKills=int(source_dict[f"Team{i}Towers"] or 0),
                    dragonKills=int(source_dict[f"Team{i}Dragons"] or 0),
                    riftHeraldKills=int(source_dict[f"Team{i}RiftHeralds"] or 0),
                    baronKills=int(source_dict[f"Team{i}Barons"] or 0),
                ),
            )
            for side, i in [("BLUE", 1), ("RED", 2)]
        },
    )

    # TODO Handle QQ games in a similar fashion
    if "qq.com" not in source_dict["MatchHistory"]:
        parsed_url = urllib.parse.urlparse(urllib.parse.urlparse(source_dict["MatchHistory"]).fragment)

        query = urllib.parse.parse_qs(parsed_url.query)
        platform_id, game_id = parsed_url.path.split("/")[1:]
        game_hash = query["gameHash"][0]

        game["sources"]["riotLolApi"] = {"gameId": int(game_id), "platformId": platform_id, "gameHash": game_hash}

    return game
