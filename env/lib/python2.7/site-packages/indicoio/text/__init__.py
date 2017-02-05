from importlib import import_module

from .language import language
from .personality import personality
from .political import political
from .summarization import summarization
from .twitter_engagement import twitter_engagement
from .emotion import emotion
from .organizations import organizations
from .personas import personas
from .relevance import relevance
from .text_features import text_features
from .keywords import keywords
from .people import people
from .places import places
from .sentiment import sentiment
from .sentiment_hq import sentiment_hq
from .text_tags import text_tags

TEXT_APIS = {
    "language": language,
    "personality": personality,
    "political": political,
    "summarization": summarization,
    "twitter_engagement": twitter_engagement,
    "emotion": emotion,
    "organizations": organizations,
    "personas": personas,
    "relevance": relevance,
    "text_features": text_features,
    "keywords": keywords,
    "people": people,
    "places": places,
    "sentiment": sentiment,
    "sentiment_hq": sentiment_hq,
    "text_tags": text_tags
}
