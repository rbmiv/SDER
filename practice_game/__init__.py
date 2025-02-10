from otree.api import *
import pagetime

doc = """
This app allows subjects to complete three practice rounds where they can choose:

<ul>
    <li>Hypothetical decisions for themselves</li>
    <li>Average hypothetical decisions for their group members</li>
    <li>Random draws for themselves and their group members (Treatment M only)</li>
</ul>

Page sequence:
<ul>
    <li>Practice Instructions Page</li>
    <li>Practice Game (3x)</li>
    <li>Practice Results (3x)</li>
</ul>
"""


class Subsession(BaseSubsession):
    pass


class C(BaseConstants):
    NAME_IN_URL = 'practice_decisions'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 3
    MPCR = .75


class Player(BasePlayer):
    practice_rounds = models.IntegerField(initial=0)
    # repeat = models.StringField(label='You may now choose to repeat the practice round or move on to the real decision'
    #                                   ' rounds:',
    #                             choices=['Repeat practice rounds', 'Move on to real decision rounds'],
    #                             widget=widgets.RadioSelect)
    p = models.IntegerField(initial=0, min=0, max=10, blank=True)  # hypothetical personal P (P, PM)
    p_others = models.IntegerField(initial=0, min=0, max=10, blank=True)  # hyp. avg P of others (P, PM)
    p_ex = models.IntegerField(initial=0, min=0, max=10, blank=True)  # hyp. exogenous contribution (P)
    m = models.IntegerField(initial=0, min=-10, max=10, blank=True)  # hyp. personal M (M, PM)
    m_others = models.IntegerField(initial=0, min=-10, max=10, blank=True)  # hyp. avg M of others (PM)
    final_group_account = models.IntegerField(initial=0, blank=True)  # final group account balance (P, M, PM)
    time_practice_instructions = models.IntegerField()
    time_practice_game = models.IntegerField()
    time_practice_results = models.IntegerField()
    time_practice_wait = models.IntegerField()


class Group(BaseGroup):
    pass


# PAGES

@pagetime.track
class PracticeInstructions(Page):

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.time_practice_instructions = pagetime.last(player.participant)


@pagetime.track
class PracticeGame(Page):
    form_model = 'player'
    form_fields = ['p', 'p_others', 'm', 'p_ex', 'm_others']

    timeout_seconds = 120
    timer_text = 'Time left:'


    @staticmethod
    def vars_for_template(player):
        treatment = player.participant.treatment
        return dict(treatment=treatment)

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.time_practice_game = pagetime.last(player.participant)

        final_group_account = 0
        treatment = player.participant.treatment

        if treatment == 'P':
            final_group_account = player.p + player.p_others * 3
        elif treatment == 'M':
            final_group_account = player.p_ex + player.p_others * 3 + player.m + player.m_others * 3
        else:  # treatment == 'PM'
            final_group_account = player.p + player.p_others * 3 + player.m + player.m_others * 3

        player.final_group_account = final_group_account


@pagetime.track
class PracticeResults(Page):

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.time_practice_results = pagetime.last(player.participant)

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
        group_payoff = round(player.final_group_account * C.MPCR, 2)
        p_total = player.p + player.p_others * 3
        if treatment == 'M':
            p_ex_payoff = 10 - player.p_ex
        else:
            p_ex_payoff = 0
        total_payoff = round(personal_account + group_payoff + p_ex_payoff, 2)
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


class PracticeWaitPage(WaitPage):
    wait_for_all_groups = True
    title_text = "Please wait"
    body_text = "Waiting for other subjects to finish practice rounds."

    @staticmethod
    def is_displayed(player):
        display = (player.round_number == C.NUM_ROUNDS)
        return display

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.time_practice_wait = pagetime.last(player.participant)


page_sequence = [PracticeInstructions, PracticeGame, PracticeResults, PracticeWaitPage]
