from otree.api import *

doc = """

"""


class Subsession(BaseSubsession):
    pass


class C(BaseConstants):
    NAME_IN_URL = 'practice_decisions'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    MPCR = .75


class Player(BasePlayer):
    practice_rounds = models.IntegerField(initial=0)
    repeat = models.StringField(label='You may now choose to repeat the practice round or move on to the real decision'
                                      ' rounds:',
                                choices=['Repeat practice rounds', 'Move on to real decision rounds'],
                                widget=widgets.RadioSelect)
    p = models.IntegerField(initial=0, min=0, max=10, blank=True)  # hypothetical personal P (P, PM)
    p_others = models.IntegerField(initial=0, min=0, max=10, blank=True)  # hyp. avg P of others (P, PM)
    p_ex = models.IntegerField(initial=0, min=0, max=10, blank=True)  # hyp. exogenous contribution (P)
    m = models.IntegerField(initial=0, min=-10, max=10, blank=True)   # hyp. personal M (M, PM)
    m_others = models.IntegerField(initial=0, min=-10, max=10, blank=True)  # hyp. avg M of others (PM)
    final_group_account = models.IntegerField(initial=0, blank=True)  # final group account balance (P, M, PM)


class Group(BaseGroup):
    pass


# PAGES


class PracticeDecisions(Page):

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class PracticeGame(Page):
    form_model = 'player'
    form_fields = ['p', 'p_others', 'm', 'p_ex', 'm_others']

    @staticmethod
    def vars_for_template(player):
        treatment = player.participant.treatment
        return dict(treatment=treatment)

    @staticmethod
    def before_next_page(player, timeout_happened):
        final_group_account = 0
        treatment = player.participant.treatment

        if treatment == 'P':
            final_group_account = player.p + player.p_others * 3
        elif treatment == 'M':
            final_group_account = player.p_ex + player.m + player.m_others * 3
        else:  # treatment == 'PM'
            final_group_account = player.p + player.p_others * 3 + player.m + player.m_others * 3

        player.final_group_account = final_group_account


class PracticeResults(Page):

    @staticmethod
    def vars_for_template(player: Player):
        treatment = player.participant.treatment
        if treatment == 'P':
            personal_account = 10 - player.p
        elif treatment == 'PM':
            personal_account = 20 - player.p - player.m
        else:
            personal_account = 10 - player.m

        group_account = player.final_group_account
        group_payoff = round(player.final_group_account * C.MPCR,2)
        p_total = player.p + player.p_others * 3
        total_payoff = round(personal_account + group_payoff, 2)
        p_ex_payoff = 10 - player.p_ex
        return dict(
            treatment=treatment,
            personal_account=personal_account,
            group_account=group_account,
            p=player.p,
            p_others=player.p_others,
            m=player.m,
            m_others=player.m_others,
            group_payoff=group_payoff,
            total_payoff=total_payoff,
            p_total=p_total,
            p_ex=player.p_ex,
            p_ex_payoff=p_ex_payoff
        )


class RepeatCheck(Page):
    form_model = 'player'
    form_fields = ['repeat']

    @staticmethod
    def vars_for_template(player):
        return dict(practice_rounds=player.practice_rounds)

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.repeat == 'Move on to real decision rounds' or player.round_number == 5:
            return 'social_dilemma_game'


page_sequence = [PracticeDecisions, PracticeGame, PracticeResults, RepeatCheck]
