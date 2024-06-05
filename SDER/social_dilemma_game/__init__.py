from otree.api import *
import csv

doc = """
This is the game app for all treatments. Different pages are displayed depending on treatment type, which is assigned 
by the creating_session function in the instructions app.

Some important notes for setup: 
    - for treatment M, you must load in a .csv called 'exogenous_decisions'. This file has to contain all of the 
    exogenous P choices from other treatment PM's that you want to assign to individuals. In that file, there should be 
    the following rows: group, player, p_ex, p_ex_id. id should just be a unique number to make referencing easier later
    in the data. Group number should start at 2. This is because "group 1" will be the initial grouping of all players 
    for previous apps in oTree, and when it creates a new group of 4 in the social_dilemma_game app, it makes group 2
    as the next group. Groups will be formed based on arrival time after completing practice questions.
"""


class C(BaseConstants):
    NAME_IN_URL = 'social_dilemma_game'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 1
    MPCR = .75


def creating_session(subsession):
    subsession.session.vars['exogenous_decisions'] = (
        load_exogenous_decisions('social_dilemma_game/exogenous_decisions.csv'))


class Subsession(BaseSubsession):
    pass


def group_by_arrival_time_method(subsession, waiting_players):
    print(f'Current waiting_players count: {len(waiting_players)}')
    for wp in waiting_players:
        print(f'Waiting Player ID: {wp.id_in_subsession}')
    if len(waiting_players) >= 4:
        group = waiting_players[:4]
        print(f'Forming group with players: {[p.id_in_subsession for p in group]}')
        return group


def load_exogenous_decisions(file_path):
    data = {}
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            key = (int(row['group']), int(row['player']))
            data[key] = {
                'p_ex': int(row['p_ex']),
                'p_ex_id': int(row['p_ex_id'])
            }
    return data


class Group(BaseGroup):
    treatment_id = models.StringField()
    p_total = models.IntegerField(initial=0)
    m_total = models.IntegerField(initial=0)
    pm_total = models.IntegerField(initial=0)
    final_group_account = models.IntegerField(initial=0)


class Player(BasePlayer):
    p = models.IntegerField(initial=0, min=0, max=10)
    p_ex = models.IntegerField(initial=0, min=0, max=10)
    p_ex_id = models.IntegerField(initial=999)
    m0 = models.IntegerField(initial=0, min=0, max=10)
    m1 = models.IntegerField(initial=0, min=-1, max=10)
    m2 = models.IntegerField(initial=0, min=-2, max=10)
    m3 = models.IntegerField(initial=0, min=-3, max=10)
    m4 = models.IntegerField(initial=0, min=-4, max=10)
    m5 = models.IntegerField(initial=0, min=-5, max=10)
    m6 = models.IntegerField(initial=0, min=-6, max=10)
    m7 = models.IntegerField(initial=0, min=-7, max=10)
    m8 = models.IntegerField(initial=0, min=-8, max=10)
    m9 = models.IntegerField(initial=0, min=-9, max=10)
    m10 = models.IntegerField(initial=0, min=-10, max=10)
    m_final = models.IntegerField(initial=0)

    def get_m_value(self, group_value):
        if group_value - self.p == 0:
            return self.m0
        elif group_value - self.p <= 3:
            return self.m1
        elif group_value - self.p <= 6:
            return self.m2
        elif group_value - self.p <= 9:
            return self.m3
        elif group_value - self.p <= 12:
            return self.m4
        elif group_value - self.p <= 15:
            return self.m5
        elif group_value - self.p <= 18:
            return self.m6
        elif group_value - self.p <= 21:
            return self.m7
        elif group_value - self.p <= 24:
            return self.m8
        elif group_value - self.p <= 27:
            return self.m9
        else:
            return self.m10


# PAGES

class GroupingWaitPage(WaitPage):
    title_text = "Please wait"
    body_text = "Waiting to form your group."
    group_by_arrival_time = True
    after_all_players_arrive = 'after_all_players_arrive'

    @staticmethod
    def after_all_players_arrive(group: Group):
        print(f'Formed Group: {group.id_in_subsession} with players {[p.id_in_subsession for p in group.get_players()]}')


class RealDecisions(Page):

    @staticmethod
    def vars_for_template(player):
        treatment = player.participant.treatment
        return dict(treatment=treatment)

    @staticmethod
    def before_next_page(player, timeout_happened):
        print("Group: ", player.group.id_in_subsession, "Player: ", player.id_in_group)
        treatment = player.participant.treatment
        if treatment == 'M':
            group_number = player.group.id_in_subsession
            player_id_in_group = player.id_in_group

            # Load the exogenous decisions data from session variables
            exogenous_decisions = player.session.vars['exogenous_decisions']

            # Debugging: Print the current group and player IDs
            print(f"Assigning p_ex for Group {group_number}, Player {player_id_in_group}")

            # Find the corresponding row in the exogenous decisions data
            key = (group_number, player_id_in_group)
            if key in exogenous_decisions:
                player.p_ex = exogenous_decisions[key]['p_ex']
                player.p_ex_id = exogenous_decisions[key]['p_ex_id']
                player.participant.vars['p_ex_id'] = exogenous_decisions[key]['p_ex_id']
                print(f"Assigned p_ex: {player.p_ex} and p_ex_id: {player.participant.vars['p_ex_id']} to Player {player.id_in_group} in Group {group_number}")
            else:
                print(f"Error: No matching data found for Group {group_number}, Player {player_id_in_group}")
                raise ValueError(f"No matching data found for Group {group_number}, Player {player_id_in_group}")

class DecisionP(Page):
    form_model = 'player'
    form_fields = ['p']

    @staticmethod
    def is_displayed(player):
        return player.participant.treatment in ['P', 'PM']

    @staticmethod
    def vars_for_template(player):
        treatment = player.participant.treatment
        return dict(treatment=treatment)


class RandomDraw(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.treatment == 'M'

    @staticmethod
    def vars_for_template(player):
        p_ex = player.p_ex
        p_ex_payoff = 10 - player.p_ex
        return dict(p_ex=p_ex,p_ex_payoff=p_ex_payoff)


class DecisionM(Page):
    form_model = 'player'
    form_fields = ['m1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7', 'm8', 'm9', 'm10']

    @staticmethod
    def is_displayed(player):
        return player.participant.treatment in ['M', 'PM']

    @staticmethod
    def vars_for_template(player):
        treatment = player.participant.treatment
        p_ex = player.p_ex
        p = player.p
        return dict(treatment=treatment, p=p, p_ex=p_ex)


class ResultsWaitPage(WaitPage):
    title_text = "Please wait"
    body_text = "Waiting for other group members to make their decisions."

    @staticmethod
    def after_all_players_arrive(group: Group):
        players = group.get_players()
        final_group_account = 0
        treatment = players[0].participant.treatment

        if treatment == 'P':
            group.p_total = sum([i.p for i in players])
            final_group_account = group.p_total

        if treatment in ['M', 'PM']:
            if treatment == 'M':
                group.p_total = sum([i.p_ex for i in players])
            else:  # treatment == 'PM'
                group.p_total = sum([i.p for i in players])

            for i in players:
                i.m_final = i.get_m_value(group.p_total)

            group.m_total = sum([i.m_final for i in players])
            group.pm_total = group.p_total + group.m_total
            final_group_account = group.pm_total

        group.final_group_account = final_group_account  # Save the updated total back to group account


class Results(Page):

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        treatment = player.participant.treatment
        if treatment == 'P':
            personal_account = 10 - player.p
        elif treatment == 'PM':
            personal_account = 20 - player.p - player.get_m_value(group.p_total)
        else:  # treatment == 'M'
            personal_account = 10 - player.get_m_value(group.p_total)

        group_account = group.final_group_account
        p_others = round((group.p_total - player.p) / 3, 1)
        m_others = round((group.m_total - player.m_final) / 3, 1)
        group_payoff = group.final_group_account * C.MPCR
        p_ex_payoff = 10-player.p_ex
        total_payoff = personal_account + group_payoff + p_ex_payoff
        return dict(
            treatment=treatment,
            personal_account=personal_account,
            group_account=group_account,
            p_others=p_others,
            m_others=m_others,
            group_payoff=group_payoff,
            total_payoff=total_payoff,
            p_total=group.p_total,
            m_final=player.m_final,
            p_ex=player.p_ex,
            p_ex_payoff=p_ex_payoff

        )


page_sequence = [GroupingWaitPage, RealDecisions, DecisionP, RandomDraw, DecisionM, ResultsWaitPage, Results]
