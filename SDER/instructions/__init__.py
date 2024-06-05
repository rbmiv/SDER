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
    value_ecu = models.IntegerField(
        choices=[[1, '$0.50'], [2, '$1.00'], [3, '$2.00'], [4, '$3.00']],
        widget=widgets.RadioSelect,
        initial=0
    )
    value_individual_self = models.IntegerField(
        choices=[[1, '0 ECU'], [2, '0.75 ECUs'], [3, '1 ECUs'], [4, '2 ECUs'], ],
        widget=widgets.RadioSelect,
        initial=0
    )
    value_individual_others = models.IntegerField(
        choices=[[1, '0 ECU'], [2, '0.75 ECUs'], [3, '1 ECUs'], [4, '2 ECUs'], ],
        widget=widgets.RadioSelect,
        initial=0
    )
    value_group_self = models.IntegerField(
        choices=[[1, '0 ECU'], [2, '0.75 ECUs'], [3, '1 ECUs'], [4, '2 ECUs'], ],
        widget=widgets.RadioSelect,
        initial=0
    )
    value_group_others = models.IntegerField(
        choices=[[1, '0 ECU'], [2, '0.75 ECUs'], [3, '1 ECUs'], [4, '2 ECUs'], ],
        widget=widgets.RadioSelect,
        initial=0
    )


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
        exchange_rate = player.subsession.session.config['exchange_rate']
        return dict(treatment=treatment, exchange_rate=exchange_rate)


class Examples(Page):

    @staticmethod
    def vars_for_template(player: Player):
        treatment = player.participant.treatment
        exchange_rate = player.subsession.session.config['exchange_rate']
        return dict(treatment=treatment, exchange_rate=exchange_rate)


class ComprehensionCheck(Page):
    form_model = 'player'
    form_fields = ['value_ecu',
                   'value_individual_self',
                   'value_individual_others',
                   'value_group_self',
                   'value_group_others'
                   ]

    @staticmethod
    def vars_for_template(player: Player):
        treatment = player.participant.treatment
        exchange_rate = player.subsession.session.config['exchange_rate']
        return dict(treatment=treatment, exchange_rate=exchange_rate)

    @staticmethod
    def error_message(player: Player, values):
        solutions = dict(
            value_ecu=2,
            value_individual_self=3,
            value_individual_others=1,
            value_group_self=2,
            value_group_others=2
        )

        error_messages = {}

        for field_name in solutions:
            if values[field_name] != solutions[field_name]:
                error_messages[field_name] = 'The above answer is incorrect - please try again.'

        return error_messages


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Welcome, Decisions, Examples, ComprehensionCheck]
