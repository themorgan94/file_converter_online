from flask_babel import gettext as _
import collections

supported_languages = {
    "en" : _("English"),
    #"fr" : _("French")
}

supported_languages = collections.OrderedDict(supported_languages)
