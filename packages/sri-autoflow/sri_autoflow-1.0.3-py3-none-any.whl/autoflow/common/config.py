from d3m.metadata import base as meta_base

PACKAGE_NAME = 'sri-autoflow'
VERSION = '1.0.3'
TAG_NAME = ''
D3M_API_VERSION = '2020.5.18'


REPOSITORY = 'https://gitlab.com/daraghhartnett/tpot-ta2'
ISSUES_URL = 'https://gitlab.com/daraghhartnett/tpot-ta2/-/issues'

D3M_PERFORMER_TEAM = 'SRI'
MAINTAINER = 'Daragh Hartnett & Dayne Freitag'
EMAIL = 'daragh.hartnett@sri.com, dayne.freitag@sri.com'

PACKAGE_URI = ''
if TAG_NAME:
    PACKAGE_URI = "git+%s@%s" % (REPOSITORY, TAG_NAME)
else:
    PACKAGE_URI = "git+%s" % (REPOSITORY)

PACKAGE_URI = "%s#egg=%s" % (PACKAGE_URI, PACKAGE_NAME)


INSTALLATION = {
    'type' : meta_base.PrimitiveInstallationType.PIP,
    'package': PACKAGE_NAME,
    'version': VERSION
}

SOURCE = {
    'name': D3M_PERFORMER_TEAM,
    'uris': [ REPOSITORY, ISSUES_URL ],
    'contact': "mailto:%s" % (EMAIL),
}
