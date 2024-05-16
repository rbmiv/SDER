from otree.api import *

doc = """
This is the game app for all treatments. Different pages are displayed depending on treatment type, which is assigned 
by the creating_session function in the instructions app.
"""


class C(BaseConstants):
    NAME_IN_URL = 'social_dilemma_game'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 1
    MPCR = .75


class Subsession(BaseSubsession):
    pass


def group_by_arrival_time_method(subsession: Subsession, waiting_players):
    if len(waiting_players) >= 4:
        return waiting_players[:4]
    for player in waiting_players:
        if waiting_too_long(player):
            player.is_surplus = True
            return [player]


class Group(BaseGroup):
    treatment_id = models.StringField()
    p_total = models.IntegerField(initial=0)
    m_total = models.IntegerField(initial=0)
    pm_total = models.IntegerField(initial=0)
    final_group_account = models.IntegerField(initial=0)
    random_draw = models.IntegerField()


class Player(BasePlayer):
    p = models.IntegerField(initial=0, min=0, max=10)
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
        """Determine the appropriate m value based on contribution of others."""
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


def waiting_too_long(player: Player):
    participant = player.participant
    participant = player.participant
    import time
    return time.time() - participant.wait_page_arrival > 5 * 60


# PAGES
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


class DecisionM(Page):
    form_model = 'player'
    form_fields = ['m1','m2', 'm3', 'm4', 'm5', 'm6', 'm7', 'm8', 'm9', 'm10']

    @staticmethod
    def is_displayed(player):
        return player.participant.treatment in ['M', 'PM']

    @staticmethod
    def vars_for_template(player):
        treatment = player.participant.treatment
        return dict(treatment=treatment)


class ResultsWaitPage(WaitPage):
    import random

    @staticmethod
    def after_all_players_arrive(group: Group):
        players = group.get_players()
        import random
        random_draw = random.randint(0, 30)
        group.random_draw = random_draw
        final_group_account = 0

        # Update group account based on contributions if treatment is P
        if players[0].participant.treatment == 'P':
            group.p_total = sum([i.p for i in players])
            final_group_account = group.p_total

        # Update group account based on contributions if treatment is M
        if players[0].participant.treatment in ['M']:
            for i in players:
                i.m_final = i.get_m_value(random_draw)
                print("random draw: ", random_draw)
                print("i.get_m_value(random_draw): ", i.get_m_value(random_draw))
                print("i.get_m_value(30): ", i.get_m_value(30))
                print("i.m_final: ", i.m_final)
            group.m_total = sum([i.m_final for i in players])
            final_group_account = group.m_total

        # Update group account based on strategy method if treatment is PM
        if players[0].participant.treatment in ['PM']:
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
            personal_account = 10 - player.get_m_value(group.random_draw)

        group_account = group.final_group_account
        p_others = round((group.p_total - player.p)/3)
        m_others = round((group.m_total - player.m_final)/3)
        group_payoff = group.final_group_account*C.MPCR
        payoff = personal_account + group_payoff
        return dict(
            treatment=treatment,
            personal_account=personal_account,
            group_account=group_account,
            p_others=p_others,
            m_others=m_others,
            group_payoff=group_payoff,
            payoff=payoff,
            random_draw=group.random_draw,
            m_final=player.m_final
        )


page_sequence = [DecisionP, DecisionM, ResultsWaitPage, Results]
