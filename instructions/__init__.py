from otree.api import *
import time
import pagetime

doc = """
This app assigns treatment condition and then displays the proper set of instructions.
<br><br>
Page sequence:
<ul>
    <li>Informed Consent Form</li>
    <li>Welcome Page</li>
    <li>Decision Instructions</li>
    <li>Example Decisions</li>
    <li>Comprehension Check</li>
</ul>
"""


def creating_session(subsession):
    import itertools
    treatments = itertools.cycle(subsession.session.config['treatments'])
    for player in subsession.get_players():
        player.participant.treatment = next(treatments)
        player.participant.start_time = time.time()


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
        choices=[[1, '$0.50'], [2, '$0.25'], [3, '$2.00'], [4, '$3.00']],
        widget=widgets.RadioSelect,
        initial=0
    )
    value_individual_self = models.IntegerField(
        choices=[[1, '0 ECU'], [2, '0.75 ECUs'], [3, '1 ECU'], [4, '2 ECUs'], ],
        widget=widgets.RadioSelect,
        initial=0
    )
    value_individual_others = models.IntegerField(
        choices=[[1, '0 ECU'], [2, '0.75 ECUs'], [3, '1 ECU'], [4, '2 ECUs'], ],
        widget=widgets.RadioSelect,
        initial=0
    )
    value_group_self = models.IntegerField(
        choices=[[1, '0 ECU'], [2, '0.75 ECUs'], [3, '1 ECU'], [4, '3 ECUs'], ],
        widget=widgets.RadioSelect,
        initial=0
    )
    value_group_others = models.IntegerField(
        choices=[[1, '0 ECU'], [2, '0.75 ECUs'], [3, '1 ECU'], [4, '2 ECUs'], ],
        widget=widgets.RadioSelect,
        initial=0
    )
    random_draw_individual = models.IntegerField(
        choices=[[1, '0'], [2, '10'], [3, '4'], [4, '6'], ],
        widget=widgets.RadioSelect,
        initial=0
    )
    random_draw_group = models.IntegerField(
        choices=[[1, '0'], [2, '10'], [3, '3'], [4, '7'], ],
        widget=widgets.RadioSelect,
        initial=0
    )
    time_consent = models.IntegerField()
    time_comprehension = models.IntegerField()
    time_decisions = models.IntegerField()
    time_examples = models.IntegerField()
    time_welcome = models.IntegerField()
    time_examples_wait = models.IntegerField()


# PAGES

@pagetime.track
class Consent(Page):
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.time_consent = pagetime.last(player.participant)


@pagetime.track
class Welcome(Page):

    @staticmethod
    def vars_for_template(player: Player):
        treatment = player.participant.treatment
        exchange_rate = player.subsession.session.config['exchange_rate']
        return dict(treatment=treatment, exchange_rate=exchange_rate)

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.time_welcome = pagetime.last(player.participant)


@pagetime.track
class Decisions(Page):

    @staticmethod
    def vars_for_template(player: Player):
        treatment = player.participant.treatment
        exchange_rate = player.subsession.session.config['exchange_rate']
        return dict(treatment=treatment, exchange_rate=exchange_rate)

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.time_decisions = pagetime.last(player.participant)


@pagetime.track
class Examples(Page):

    @staticmethod
    def vars_for_template(player: Player):
        treatment = player.participant.treatment
        exchange_rate = player.subsession.session.config['exchange_rate']
        return dict(treatment=treatment, exchange_rate=exchange_rate)

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.time_examples = pagetime.last(player.participant)


@pagetime.track
class ComprehensionCheck(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player):
        treatment = player.participant.treatment
        form_fields = ['value_ecu',
                       'value_individual_self',
                       'value_individual_others',
                       'value_group_self',
                       'value_group_others',
                       ]
        if treatment == 'M':
            form_fields += ['random_draw_group', 'random_draw_individual']
        return form_fields

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
            value_group_others=2,
        )

        if player.participant.treatment == 'M':
            solutions.update(
                random_draw_group=3,
                random_draw_individual=3
            )

        error_messages = {}

        for field_name in solutions:
            if values[field_name] != solutions[field_name]:
                error_messages[field_name] = 'The above answer is incorrect - please try again.'

        return error_messages

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.time_comprehension = pagetime.last(player.participant)


@pagetime.track
class ExamplesWaitPage(Page):

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.time_examples_wait = pagetime.last(player.participant)


@pagetime.track
class Results(Page):

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.time_results = int(time.time())


page_sequence = [Consent, Welcome, Decisions, Examples, ExamplesWaitPage, ComprehensionCheck]
