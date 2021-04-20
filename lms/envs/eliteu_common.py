# -*- coding: utf-8 -*-
import sys
import logging
import json
import os
from path import Path as path

from django.utils.translation import ugettext_lazy as _

from .common import *
from .common import _make_mako_template_dirs
from .eliteu import *

PLATFORM_NAME = _('Elite A.I. Academy')

FEATURES.update({
    # enable unicode username
    'ENABLE_UNICODE_USERNAME': True,

    'ENABLE_MKTG_SITE': True,
    # eliteu apps
    # Whether to enable membership
    'ENABLE_MEMBERSHIP_INTEGRATION': False,

    # Whether to enable payments
    'ENABLE_PAYMENTS_INTEGRATION': False,

    # Whether to enable course unenroll
    'ENABLE_COURSE_UNENROLL': False,

    # Whether to enable elite courses sort
    'ENABLE_COURSE_SORTING_BY_START_DATE_DESC': False

})

MEMBERSHIP_ROOT = REPO_ROOT / "../edx-membership"

sys.path.append(MEMBERSHIP_ROOT)

OAUTH2_PROVIDER.update({
    'ACCESS_TOKEN_EXPIRE_SECONDS': 60 * 60 * 24 * 365,
})

# Mako templating
import tempfile

MAKO_MODULE_DIR = os.path.join(tempfile.gettempdir(), 'mako_lms')
MAKO_TEMPLATE_DIRS_BASE.append(
    MEMBERSHIP_ROOT / 'membership' / 'templates',
)

###############################################################################################
# Django templating
TEMPLATES = [
    {
        'NAME': 'django',
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Don't look for template source files inside installed applications.
        'APP_DIRS': False,
        # Instead, look for template source files in these dirs.
        'DIRS': [
            PROJECT_ROOT / "templates",
            COMMON_ROOT / 'templates',
            COMMON_ROOT / 'lib' / 'capa' / 'capa' / 'templates',
            COMMON_ROOT / 'djangoapps' / 'pipeline_mako' / 'templates',
            COMMON_ROOT / 'static',  # required to statically include common Underscore templates
            MEMBERSHIP_ROOT / 'membership' / 'templates',
        ],
        # Options specific to this backend.
        'OPTIONS': {
            'loaders': [
                # We have to use mako-aware template loaders to be able to include
                # mako templates inside django templates (such as main_django.html).
                'openedx.core.djangoapps.theming.template_loaders.ThemeTemplateLoader',
                'edxmako.makoloader.MakoFilesystemLoader',
                'edxmako.makoloader.MakoAppDirectoriesLoader',
            ],
            'context_processors': CONTEXT_PROCESSORS,
            # Change 'debug' in your environment settings files - not here.
            'debug': False
        }
    },
    {
        'NAME': 'mako',
        'BACKEND': 'edxmako.backend.Mako',
        # Don't look for template source files inside installed applications.
        'APP_DIRS': False,
        # Instead, look for template source files in these dirs.
        'DIRS': _make_mako_template_dirs,
        # Options specific to this backend.
        'OPTIONS': {
            'context_processors': CONTEXT_PROCESSORS,
            # Change 'debug' in your environment settings files - not here.
            'debug': False,
        }
    },
]
derived_collection_entry('TEMPLATES', 1, 'DIRS')
DEFAULT_TEMPLATE_ENGINE = TEMPLATES[0]
DEFAULT_TEMPLATE_ENGINE_DIRS = DEFAULT_TEMPLATE_ENGINE['DIRS'][:]


def _add_microsite_dirs_to_default_template_engine(settings):
    """
    Derives the final DEFAULT_TEMPLATE_ENGINE['DIRS'] setting from other settings.
    """
    if settings.FEATURES.get('USE_MICROSITES', False) and getattr(settings, "MICROSITE_CONFIGURATION", False):
        DEFAULT_TEMPLATE_ENGINE_DIRS.append(settings.MICROSITE_ROOT_DIR)
    return DEFAULT_TEMPLATE_ENGINE_DIRS


DEFAULT_TEMPLATE_ENGINE['DIRS'] = _add_microsite_dirs_to_default_template_engine
derived_collection_entry('DEFAULT_TEMPLATE_ENGINE', 'DIRS')

###############################################################################################

USERNAME_REGEX_PARTIAL = r'[\u4e00-\u9fa5\w .@_+-]+'

STATICFILES_DIRS.append(
    MEMBERSHIP_ROOT / "membership" / "static",
)

LANGUAGES = [
    ('en', u'English'),
    ('rtl', u'Right-to-Left Test Language'),
    ('eo', u'Dummy Language (Esperanto)'),  # Dummy languaged used for testing
    ('fake2', u'Fake translations'),  # Another dummy language for testing (not pushed to prod)

    # ('am', u'አማርኛ'),  # Amharic
    # ('ar', u'العربية'),  # Arabic
    # ('az', u'azərbaycanca'),  # Azerbaijani
    # ('bg-bg', u'български (България)'),  # Bulgarian (Bulgaria)
    # ('bn-bd', u'বাংলা (বাংলাদেশ)'),  # Bengali (Bangladesh)
    # ('bn-in', u'বাংলা (ভারত)'),  # Bengali (India)
    # ('bs', u'bosanski'),  # Bosnian
    # ('ca', u'Català'),  # Catalan
    # ('ca@valencia', u'Català (València)'),  # Catalan (Valencia)
    # ('cs', u'Čeština'),  # Czech
    # ('cy', u'Cymraeg'),  # Welsh
    # ('da', u'dansk'),  # Danish
    # ('de-de', u'Deutsch (Deutschland)'),  # German (Germany)
    # ('el', u'Ελληνικά'),  # Greek
    # ('en-uk', u'English (United Kingdom)'),  # English (United Kingdom)
    # ('en@lolcat', u'LOLCAT English'),  # LOLCAT English
    # ('en@pirate', u'Pirate English'),  # Pirate English
    # ('es-419', u'Español (Latinoamérica)'),  # Spanish (Latin America)
    # ('es-ar', u'Español (Argentina)'),  # Spanish (Argentina)
    # ('es-ec', u'Español (Ecuador)'),  # Spanish (Ecuador)
    # ('es-es', u'Español (España)'),  # Spanish (Spain)
    # ('es-mx', u'Español (México)'),  # Spanish (Mexico)
    # ('es-pe', u'Español (Perú)'),  # Spanish (Peru)
    # ('et-ee', u'Eesti (Eesti)'),  # Estonian (Estonia)
    # ('eu-es', u'euskara (Espainia)'),  # Basque (Spain)
    # ('fa', u'فارسی'),  # Persian
    # ('fa-ir', u'فارسی (ایران)'),  # Persian (Iran)
    # ('fi-fi', u'Suomi (Suomi)'),  # Finnish (Finland)
    # ('fil', u'Filipino'),  # Filipino
    # ('fr', u'Français'),  # French
    # ('gl', u'Galego'),  # Galician
    # ('gu', u'ગુજરાતી'),  # Gujarati
    # ('he', u'עברית'),  # Hebrew
    # ('hi', u'हिन्दी'),  # Hindi
    # ('hr', u'hrvatski'),  # Croatian
    # ('hu', u'magyar'),  # Hungarian
    # ('hy-am', u'Հայերեն (Հայաստան)'),  # Armenian (Armenia)
    # ('id', u'Bahasa Indonesia'),  # Indonesian
    # ('it-it', u'Italiano (Italia)'),  # Italian (Italy)
    # ('ja-jp', u'日本語 (日本)'),  # Japanese (Japan)
    # ('kk-kz', u'қазақ тілі (Қазақстан)'),  # Kazakh (Kazakhstan)
    # ('km-kh', u'ភាសាខ្មែរ (កម្ពុជា)'),  # Khmer (Cambodia)
    # ('kn', u'ಕನ್ನಡ'),  # Kannada
    # ('ko-kr', u'한국어 (대한민국)'),  # Korean (Korea)
    # ('lt-lt', u'Lietuvių (Lietuva)'),  # Lithuanian (Lithuania)
    # ('ml', u'മലയാളം'),  # Malayalam
    # ('mn', u'Монгол хэл'),  # Mongolian
    # ('mr', u'मराठी'),  # Marathi
    # ('ms', u'Bahasa Melayu'),  # Malay
    # ('nb', u'Norsk bokmål'),  # Norwegian Bokmål
    # ('ne', u'नेपाली'),  # Nepali
    # ('nl-nl', u'Nederlands (Nederland)'),  # Dutch (Netherlands)
    # ('or', u'ଓଡ଼ିଆ'),  # Oriya
    # ('pl', u'Polski'),  # Polish
    # ('pt-br', u'Português (Brasil)'),  # Portuguese (Brazil)
    # ('pt-pt', u'Português (Portugal)'),  # Portuguese (Portugal)
    # ('ro', u'română'),  # Romanian
    # ('ru', u'Русский'),  # Russian
    # ('si', u'සිංහල'),  # Sinhala
    # ('sk', u'Slovenčina'),  # Slovak
    # ('sl', u'Slovenščina'),  # Slovenian
    # ('sq', u'shqip'),  # Albanian
    # ('sr', u'Српски'),  # Serbian
    # ('sv', u'svenska'),  # Swedish
    # ('sw', u'Kiswahili'),  # Swahili
    # ('ta', u'தமிழ்'),  # Tamil
    # ('te', u'తెలుగు'),  # Telugu
    # ('th', u'ไทย'),  # Thai
    # ('tr-tr', u'Türkçe (Türkiye)'),  # Turkish (Turkey)
    # ('uk', u'Українська'),  # Ukranian
    # ('ur', u'اردو'),  # Urdu
    # ('vi', u'Tiếng Việt'),  # Vietnamese
    # ('uz', u'Ўзбек'),  # Uzbek
    ('zh-cn', u'中文 (简体)'),  # Chinese (China)
    # ('zh-hk', u'中文 (香港)'),  # Chinese (Hong Kong)
    # ('zh-tw', u'中文 (台灣)'),  # Chinese (Taiwan)
]

########################## CERTIFICATE NAME ########################
CERT_NAME_SHORT = _("Certificate")
CERT_NAME_LONG = _("Certificate of Achievement")

#### PASSWORD POLICY SETTINGS #####
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "util.password_policy_validators.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "util.password_policy_validators.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 6
        }
    },
    {
        "NAME": "util.password_policy_validators.MaximumLengthValidator",
        "OPTIONS": {
            "max_length": 75
        }
    },
]

# Country code overrides
# Used by django-countries
COUNTRIES_OVERRIDE = {
    # Taiwan is specifically not translated to avoid it being translated as "Taiwan (Province of China)"
    # "TW": "Taiwan",
    'XK': _('Kosovo'),
}

ACCOUNT_VISIBILITY_CONFIGURATION = {
    # Default visibility level for accounts without a specified value
    # The value is one of: 'all_users', 'private'
    "default_visibility": "all_users",

    # The list of all fields that can be shared with other users
    "shareable_fields": [
        'username',
        'profile_image',
        'country',
        'time_zone',
        'date_joined',
        'language_proficiencies',
        'bio',
        'social_links',
        'account_privacy',
        # Not an actual field, but used to signal whether badges should be public.
        'accomplishments_shared',
    ],

    # The list of account fields that are always public
    "public_fields": [
        'username',
        'profile_image',
        'account_privacy',
    ],

    # The list of account fields that are visible only to staff and users viewing their own profiles
    "admin_fields": [
        "username",
        "email",
        "is_active",
        "bio",
        "country",
        "date_joined",
        "profile_image",
        "language_proficiencies",
        "social_links",
        "name",
        "gender",
        "goals",
        "year_of_birth",
        "level_of_education",
        "mailing_address",
        "requires_parental_consent",
        "account_privacy",
        "accomplishments_shared",
        "extended_profile",
        "phone",
    ]
}
############################ eliteu envs #########################

log = logging.getLogger(__name__)

# SERVICE_VARIANT specifies name of the variant used, which decides what JSON
# configuration files are read during startup.
SERVICE_VARIANT = os.environ.get('SERVICE_VARIANT', None)

# CONFIG_ROOT specifies the directory where the JSON configuration
# files are expected to be found. If not specified, use the project
# directory.
CONFIG_ROOT = path(os.environ.get('CONFIG_ROOT', ENV_ROOT))

# CONFIG_PREFIX specifies the prefix of the JSON configuration files,
# based on the service variant. If no variant is use, don't use a
# prefix.
CONFIG_PREFIX = SERVICE_VARIANT + "." if SERVICE_VARIANT else ""

with open(CONFIG_ROOT / CONFIG_PREFIX + "env.json") as env_file:
    ENV_TOKENS = json.load(env_file)

with open(CONFIG_ROOT / CONFIG_PREFIX + "auth.json") as auth_file:
    AUTH_TOKENS = json.load(auth_file)

ENV_FEATURES = ENV_TOKENS.get('FEATURES', {})
for feature, value in ENV_FEATURES.items():
    FEATURES[feature] = value

# Apple In-app purchase
APPLE_VERIFY_RECEIPT_IS_SANDBOX = ENV_TOKENS.get('APPLE_VERIFY_RECEIPT_IS_SANDBOX', '')
APPLE_VERIFY_RECEIPT_URL = ENV_TOKENS.get('APPLE_VERIFY_RECEIPT_URL', '')
APPLE_VERIFY_RECEIPT_SANDBOX_URL = ENV_TOKENS.get('APPLE_VERIFY_RECEIPT_SANDBOX_URL', '')
APPLE_IN_APP_PRODUCT_ID = AUTH_TOKENS.get('APPLE_IN_APP_PRODUCT_ID', {})

# verify student
SHOW_VERIFY_STUDENT_SUPPORT = FEATURES.get('SHOW_VERIFY_STUDENT_SUPPORT', True)

# Sentry
try:
    SENTRY_DSN_FRONTEND = ENV_FEATURES.get('SENTRY_DSN_FRONTEND', '')
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_dsn_backend = ENV_FEATURES.get('SENTRY_DSN_BACKEND', '')
    if sentry_dsn_backend:
        sentry_sdk.init(
            dsn=sentry_dsn_backend,
            integrations=[DjangoIntegration()]
        )
        log.info("Sentry Start Up Success")
except ImportError:
    log.info("Sentry Module Import Error")

# CourseSearch
SEARCH_SORT = ENV_TOKENS.get('SEARCH_SORT', None)

# App Version
MOBILE_APP_USER_AGENT_REGEXES = ENV_TOKENS.get('MOBILE_APP_USER_AGENT_REGEXES', None)

# Baidu Bridge
BAIDU_BRIDGE_URL = ENV_TOKENS.get('BAIDU_BRIDGE_URL', '')

############### Settings for AES Encryption/Decryption  ##################
AES_KEY = AUTH_TOKENS.get('AES_KEY', '')
