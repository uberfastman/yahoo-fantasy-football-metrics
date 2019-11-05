__author__ = "Wren J. R. (uberfastman)"
__email__ = "wrenjr@yahoo.com"

from collections import defaultdict
from dao.base import BaseTeam, BaseRecord


class Luck(object):

    def __init__(self, teams, matchups_list):
        self.teams = teams
        self.matchups_list = matchups_list

    def calculate(self):
        luck_results = defaultdict(defaultdict)
        matchups = {
            str(team_id): value[
                "result"] for pair in self.matchups_list for team_id, value in list(pair.items())
        }

        for team_1 in self.teams.values():  # type: BaseTeam
            luck_record = BaseRecord()

            for team_2 in self.teams.values():
                if team_1.team_id == team_2.team_id:
                    continue
                score_1 = team_1.points
                score_2 = team_2.points

                if float(score_1) > float(score_2):
                    luck_record.add_win()
                elif float(score_1) < float(score_2):
                    luck_record.add_loss()
                else:
                    luck_record.add_tie()

            luck_results[team_1.team_id]["luck_record"] = luck_record

            # calc luck %
            # TODO: assuming no ties...  how are tiebreakers handled?
            luck = 0.0
            # number of teams excluding current team
            num_teams = float(len(self.teams)) - 1

            if luck_record.get_wins() != 0 and luck_record.get_losses() != 0:
                matchup_result = matchups[str(team_1.team_id)]
                if matchup_result == "W" or matchup_result == "T":
                    luck = (luck_record.get_losses() + luck_record.get_ties()) / num_teams
                else:
                    luck = 0 - (luck_record.get_wins() + luck_record.get_ties()) / num_teams

            # noinspection PyTypeChecker
            luck_results[team_1.team_id]["luck"] = luck * 100

        return luck_results
