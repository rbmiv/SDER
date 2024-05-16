from otree.api import *

doc = """
This app creates assigns treatment condition and then displays the proper set of instructions.
"""


def creating_session(subsession):
    import itertools
    treatments = itertools.cycle(subsession.session.config['treatments'])
    for player in subsession.get_players():
        player.participant.treatment = next(treatments)


class C(BaseConstants):
    NAME_IN_URL = 'instructions'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES


class Welcome(Page):

    @staticmethod
    def vars_for_template(player: Player):
        treatment = player.participant.treatment
        exchange_rate = player.subsession.session.config['exchange_rate']
        return dict(treatment=treatment, exchange_rate=exchange_rate)


class Decisions(Page):

    @staticmethod
    def vars_for_template(player: Player):
        treatment = player.participant.treatment
        return dict(treatment=treatment)


class Examples(Page):

    @staticmethod
    def vars_for_template(player: Player):
        treatment = player.participant.treatment
        exchange_rate = player.subsession.session.config['exchange_rate']
        return dict(treatment=treatment, exchange_rate=exchange_rate)


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Welcome, Decisions, Examples]
