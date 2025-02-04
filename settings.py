from os import environ

SESSION_CONFIGS = [
    dict(
        name='SDER_M',
        display_name='SDER - Treatment M',
        app_sequence=['instructions', 'practice_game', 'social_dilemma_game'],
        treatments='M'

    ),
    dict(
        name='SDER_P',
        display_name='SDER - Treatment P',
        app_sequence=['instructions', 'practice_game', 'social_dilemma_game'],
        treatments='P',
    ),
    dict(
        name='SDER_PM',
        display_name='SDER - Treatment PM',
        app_sequence=['instructions', 'practice_game', 'social_dilemma_game'],
        treatments=['PM'],
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    num_demo_participants=12,
    exchange_rate=.25,
    survey=3,
    real_world_currency_per_point=1.00,
    participation_fee=5.00,
    doc=""
)

PARTICIPANT_FIELDS = [
    'treatment',
    'p_ex',
    'p_ex_id',
    'wait_page_arrival',
    'start_time',
    'end_time',
    'total_time',
    'total_payoff',
    'time_comprehension',
    'time_consent',
    'time_decisions',
    'time_examples',
    'time_welcome',
    'time_practice',
    'time_decision_m',
    'time_decision_p',
    'time_random_draw',
    'time_real_decisions',
    'time_results',
    'time_instructions',
    'time_survey'

]
SESSION_FIELDS = ['exogenous_decisions']

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '5607494413396'
