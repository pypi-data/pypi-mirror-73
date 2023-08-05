import json
import datetime
import logging

import lol_id_tools as lit
from lol_dto.classes.game import (
    LolGamePlayerSummonerSpell,
    LolGamePlayerEndOfGameStats,
    LolGamePlayerItem,
    LolGamePlayerRune,
    Position,
    LolGamePlayerSnapshot,
    LolGameTeamMonsterKill,
    LolGameKill,
    LolGamePlayerSkillLevelUpEvent,
    LolGamePlayerItemEvent,
)
from riot_transmute.match_timeline_to_game import (
    monster_type_dict,
    monster_subtype_dict,
    building_dict,
    get_player as get_player_riot_transmute,
)

from lol_esports_parser.dto.wp_dto import (
    LolWpGamePlayer,
    LolWpGame,
    LolWpGamePlayerWardEvent,
    LolWpGamePlayerMonsterKillEvent,
    LolWpGameTeam,
    LolWpGamePlayerPosition,
)


def get_player(game, participant_id) -> LolWpGamePlayer:
    return get_player_riot_transmute(game, participant_id)


def parse_wp_game(raw_data: dict, patch: str = None, add_names=True, discrete_mode=True) -> LolWpGame:
    """Parses a JSON from wp into a LolGame.

    Args:
        raw_data: the JSON you got from the match details endpoint
        patch: MM.mm patch, to query the proper runes and add it to the object
        add_names: whether or not to add names to items, runes, and so on and so forth
        discrete_mode: whether or not to add fields that are specific to this data source
    """
    data = raw_data["data"]

    # Those are dicts with keys teamid (str), teamalias, and faction ("red", "blue")
    blue_team = data["blue"]
    blue_team["side"] = "BLUE"

    red_team = data["red"]
    red_team["side"] = "RED"

    winner = next(t for t in (blue_team, red_team) if t["teamid"] == data["info"]["winner"])["side"]

    # TODO Check games over 1h
    minutes, seconds = data["info"]["duration"].split(":")
    duration = int(minutes) * 60 + int(seconds)

    game = LolWpGame(
        # The game version field is FALSE but a decent approximation
        patch=patch or data["info"]["gameversion"],
        winner=winner,
        # TODO Check this is properly gameInSeries
        gameInSeries=int(data["info"]["gametype"]),
        duration=duration,
        teams={
            "BLUE": LolWpGameTeam(
                name=blue_team["teamalias"],
                uniqueIdentifiers={"wp": {"id": int(blue_team["teamid"])}} if not discrete_mode else None,
                players=[],
                buildingsKills=[],
            ),
            "RED": LolWpGameTeam(
                name=red_team["teamalias"],
                uniqueIdentifiers={"wp": {"id": int(red_team["teamid"])}} if not discrete_mode else None,
                players=[],
                buildingsKills=[],
            ),
        },
        kills=[],
    )

    game_start = None
    game_id = None

    for players_list in data["plList"]:
        for player_dict in players_list.values():
            player_team_dict = next(team for team in (blue_team, red_team) if team["teamid"] == player_dict["teamid"])
            team = game["teams"][player_team_dict["side"]]

            game_start = datetime.datetime.utcfromtimestamp(int(player_dict["matchcreation"]))
            game_id = int(player_dict["matchid"])

            summoner_spells = [
                LolGamePlayerSummonerSpell(
                    slot=i - 1,
                    id=int(player_dict[f"skill{i}id"]),
                    name=lit.get_name(int(player_dict[f"skill{i}id"]), object_type="summoner_spell")
                    if add_names
                    else None,
                )
                for i in (1, 2)
            ]

            # TODO Make that backwards-compatible with pre-runes reforged games
            runes = [
                LolGamePlayerRune(
                    id=player_dict["stats"].get(f"perk{i}"),
                    slot=i,
                    stats=[player_dict["stats"].get(f"perk{i}Var{j}") for j in range(1, 4)],
                )
                for i in range(0, 6)
            ]

            # Adding stats perks
            runes.extend([LolGamePlayerRune(id=player_dict["stats"].get(f"perk{i}"), slot=i + 6,) for i in range(0, 3)])

            items = [LolGamePlayerItem(id=player_dict["stats"].get(f"item{i}"), slot=i) for i in range(0, 7)]

            end_of_game_stats = LolGamePlayerEndOfGameStats(
                items=items,
                firstBlood=player_dict["stats"].get("firstBloodKill"),
                firstBloodAssist=player_dict["stats"].get("firstBloodAssist"),  # This field is wrong by default
                kills=player_dict["stats"].get("kills"),
                deaths=player_dict["stats"].get("deaths"),
                assists=player_dict["stats"].get("assists"),
                gold=player_dict["stats"].get("goldEarned"),
                cs=player_dict["stats"].get("minionsKilled") + player_dict["stats"].get("neutralMinionsKilled"),
                level=player_dict["stats"].get("champLevel"),
                wardsPlaced=player_dict["stats"].get("wardsPlaced"),
                wardsKilled=player_dict["stats"].get("wardsKilled"),
                visionWardsBought=player_dict["stats"].get("visionWardsBoughtInGame"),
                visionScore=player_dict["stats"].get("visionScore"),
                killingSprees=player_dict["stats"].get("killingSprees"),
                largestKillingSpree=player_dict["stats"].get("largestKillingSpree"),
                doubleKills=player_dict["stats"].get("doubleKills"),
                tripleKills=player_dict["stats"].get("tripleKills"),
                quadraKills=player_dict["stats"].get("quadraKills"),
                pentaKills=player_dict["stats"].get("pentaKills"),
                monsterKills=player_dict["stats"].get("neutralMinionsKilled"),
                monsterKillsInAlliedJungle=player_dict["stats"].get("neutralMinionsKilledTeamJungle"),
                monsterKillsInEnemyJungle=player_dict["stats"].get("neutralMinionsKilledEnemyJungle"),
                totalDamageDealt=player_dict["stats"].get("totalDamageDealt"),
                physicalDamageDealt=player_dict["stats"].get("physicalDamageDealt"),
                magicDamageDealt=player_dict["stats"].get("magicDamageDealt"),
                totalDamageDealtToChampions=player_dict["stats"].get("totalDamageDealtToChampions"),
                physicalDamageDealtToChampions=player_dict["stats"].get("physicalDamageDealtToChampions"),
                magicDamageDealtToChampions=player_dict["stats"].get("magicDamageDealtToChampions"),
                damageDealtToObjectives=player_dict["stats"].get("damageDealtToObjectives"),
                damageDealtToTurrets=player_dict["stats"].get("damageDealtToTurrets"),
                totalDamageTaken=player_dict["stats"].get("totalDamageTaken"),
                physicalDamageTaken=player_dict["stats"].get("physicalDamageTaken"),
                magicDamageTaken=player_dict["stats"].get("magicDamageTaken"),
                longestTimeSpentLiving=player_dict["stats"].get("longestTimeSpentLiving"),
                largestCriticalStrike=player_dict["stats"].get("largestCriticalStrike"),
                goldSpent=player_dict["stats"].get("goldSpent"),
                totalHeal=player_dict["stats"].get("totalHeal"),
                totalUnitsHealed=player_dict["stats"].get("totalUnitsHealed"),
                damageSelfMitigated=player_dict["stats"].get("damageSelfMitigated"),
                totalTimeCCDealt=player_dict["stats"].get("totalTimeCrowdControlDealt"),
                timeCCingOthers=player_dict["stats"].get("timeCCingOthers"),
            )

            player = LolWpGamePlayer(
                id=int(player_dict["participantid"]),  # This is string everywhere unfortunately
                uniqueIdentifiers={"wp": {"id": int(player_dict["playerid"])}} if not discrete_mode else None,
                inGameName=player_dict["playername"],
                championId=int(player_dict["cpheroid"]),
                championName=lit.get_name(int(player_dict["cpheroid"]), object_type="champion") if add_names else None,
                summonerSpells=summoner_spells,
                primaryRuneTreeId=player_dict["stats"].get("perkPrimaryStyle"),
                secondaryRuneTreeId=player_dict["stats"].get("perkSubStyle"),
                runes=runes,
                endOfGameStats=end_of_game_stats,
                snapshots=[],
                wardsEvents=[],
                itemsEvents=[],
                skillsLevelUpEvents=[],
                monstersKills=[],
            )

            # Then, we add convenience name fields for human readability if asked
            if add_names:
                player["championName"] = lit.get_name(player["championId"], object_type="champion")
                player["primaryRuneTreeName"] = lit.get_name(player["primaryRuneTreeId"])
                player["secondaryRuneTreeName"] = lit.get_name(player["secondaryRuneTreeId"])

                for item in player["endOfGameStats"]["items"]:
                    item["name"] = lit.get_name(item["id"], object_type="item")
                for rune in player["runes"]:
                    rune["name"] = lit.get_name(rune["id"], object_type="rune")
                for summoner_spell in player["summonerSpells"]:
                    summoner_spell["name"] = lit.get_name(summoner_spell["id"], object_type="summoner_spell")

            team["players"].append(player)

    # We only have game start after parsing players, quality API
    game_start = game_start.replace(tzinfo=datetime.timezone.utc)
    game["start"] = game_start.isoformat(timespec="seconds")

    if not discrete_mode:
        game["sources"] = {"wp": {"id": game_id}}
        game = add_timeline(game, data, add_names)

    return game


def add_timeline(game: LolWpGame, data: dict, add_names) -> LolWpGame:

    frames_dict = json.loads(data["info"]["framecache"])
    game["teamfights"] = frames_dict.get("battleInfo")  # TODO Look at it in depth

    for frame in frames_dict["frames"]:
        # We start by adding player information at the given snapshot timestamps
        for participant_frame in frame["participantFrames"].values():
            team_side = "BLUE" if participant_frame["participantId"] < 6 else "RED"

            # Finding the player with the same id in our game object
            player = next(
                p for p in game["teams"][team_side]["players"] if p["id"] == participant_frame["participantId"]
            )

            try:
                position = Position(x=participant_frame["position"]["x"], y=participant_frame["position"]["y"])
            except KeyError:
                position = None

            snapshot = LolGamePlayerSnapshot(
                timestamp=frame["timestamp"] / 1000,
                currentGold=participant_frame["currentGold"],
                totalGold=participant_frame["totalGold"],
                xp=participant_frame["xp"],
                level=participant_frame["level"],
                cs=participant_frame["minionsKilled"] + participant_frame["jungleMinionsKilled"],
                monstersKilled=participant_frame["jungleMinionsKilled"],
                position=position,
            )

            player["snapshots"].append(snapshot)

        for event in frame["events"]:
            timestamp = event["timestamp"] / 1000

            if "position" in event:
                position = Position(x=event["position"]["x"], y=event["position"]["y"])
            else:
                position = None

            # Monsters kills (epic and non epic)
            if event["type"] == "ELITE_MONSTER_KILL":
                if event["killerId"] < 1:
                    # This is Rift Herald killing itself, we just pass
                    logging.info(f"Epic monster kill with killer id 0 found, likely Rift Herald killing itself.")
                    continue

                try:
                    monster_type = monster_type_dict[event["monsterType"]]

                    team = game["teams"]["BLUE" if event["killerId"] < 6 else "RED"]

                    event_dto = LolGameTeamMonsterKill(
                        timestamp=timestamp, type=monster_type, killerId=event["killerId"]
                    )

                    if monster_type == "DRAGON":
                        try:
                            event_dto["subType"] = monster_subtype_dict[event["monsterSubType"]]
                        # If we don’t know how to translate the monster subtype, we simply leave it as-is
                        except KeyError:
                            event_dto["subType"] = event["monsterSubType"]

                    team["monstersKills"].append(event_dto)

                except KeyError:
                    # This is a non-epic monster and belongs to a PLAYER
                    player = get_player(game, event["killerId"])
                    player: LolWpGamePlayer

                    if event["monsterType"] == "BLUE_GOLEM":
                        monster_type = "BLUE_BUFF"
                    elif event["monsterType"] == "RED_LIZARD":
                        monster_type = "RED_BUFF"
                    else:
                        monster_type = None

                    player["monstersKills"].append(
                        LolWpGamePlayerMonsterKillEvent(
                            timestamp=timestamp, position=position, monsterType=monster_type,
                        )
                    )

            # Buildings kills
            elif event["type"] == "BUILDING_KILL":
                # The teamId here refers to the SIDE of the tower that was killed, so the opponents killed it
                team = game["teams"]["RED" if event["teamId"] == 100 else "BLUE"]

                # Get the prebuilt "building" event DTO
                event_dto = building_dict[event["position"]["x"], event["position"]["y"]]

                # Fill its timestamp
                event_dto["timestamp"] = timestamp

                if event.get("killerId"):
                    event_dto["killerId"] = event.get("killerId")

                team["buildingsKills"].append(event_dto)

            # Champions kills
            elif event["type"] == "CHAMPION_KILL":

                game["kills"].append(
                    LolGameKill(
                        timestamp=timestamp,
                        position=position,
                        killerId=event["killerId"],
                        victimId=event["victimId"],
                        assistsIds=event["assistingParticipantIds"],
                    )
                )

            # Skill points use
            elif event["type"] == "SKILL_LEVEL_UP":
                player = get_player(game, event["participantId"])

                player["skillsLevelUpEvents"].append(
                    LolGamePlayerSkillLevelUpEvent(
                        timestamp=timestamp, slot=event["skillSlot"], type=event["levelUpType"]
                    )
                )

            # Item buying, selling, and undoing
            elif "ITEM" in event["type"]:
                player = get_player(game, event["participantId"])
                event_type = event["type"].lstrip("ITEM_")

                if event_type == "UNDO":
                    item_event = LolGamePlayerItemEvent(
                        timestamp=timestamp, type=event_type, id=event["afterId"], undoId=event["beforeId"]
                    )
                else:
                    item_event = LolGamePlayerItemEvent(timestamp=timestamp, type=event_type, id=event["itemId"])

                if add_names:
                    item_event["name"] = lit.get_name(item_event["id"], object_type="item")

                player["itemsEvents"].append(item_event)

            # Wards placing and killing
            # This is different than traditional Riot timelines
            elif "WARD" in event["type"]:
                if event["type"] == "WARD_KILL":
                    player = get_player(game, event["killerId"])
                    event_type = "KILLED"
                else:
                    try:
                        player = get_player(game, event["creatorId"])
                    except StopIteration:
                        # Ghost Poro wards
                        continue
                    event_type = "PLACED"

                try:
                    death_timestamp = event.get("deadTime") / 1000
                except TypeError:
                    death_timestamp = None

                ward_event = LolWpGamePlayerWardEvent(
                    timestamp=timestamp,
                    position=position,
                    deathTimestamp=death_timestamp,
                    type=event_type,
                    wardType=event["wardType"],
                    killType=event.get("deadType"),  # TODO Properly understand that field
                )

                player["wardsEvents"].append(ward_event)

    for player_key in frames_dict["positionInfo"]:
        player = get_player(game, int(player_key))
        position_dict = frames_dict["positionInfo"][player_key]

        player["position"] = []

        assert player["championId"] == position_dict["hero_id_"]

        interval = position_dict["interval_"]

        for idx, position in enumerate(position_dict["hot_point_"]):
            player["position"].append(
                LolWpGamePlayerPosition(
                    timestamp=interval * idx, position=Position(x=position["axis_x_"], y=position["axis_y_"],)
                )
            )

    return game
