from os import environ

SESSION_CONFIGS = [
    dict(
        name='SDER_M',
        display_name='SDER - Treatment M',
        app_sequence=['instructions', 'practice_game', 'social_dilemma_game', 'survey'],
        treatments='M'

    ),
    dict(
        name='SDER_P',
        display_name='SDER - Treatment P',
        app_sequence=['instructions', 'practice_game', 'social_dilemma_game', 'survey'],
        treatments='P',
    ),
    dict(
        name='SDER_PM',
        display_name='SDER - Treatment PM',
        app_sequence=['instructions', 'practice_game', 'social_dilemma_game', 'survey'],
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
    real_world_currency_per_point=0.25,
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
    'finished'
]
SESSION_FIELDS = ['exogenous_decisions']


ROOMS = [
    dict(
        name='SDER',
        display_name='SDER',
        participant_label_file='_rooms/SDER.txt',
    ),
]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '5607494413396'
