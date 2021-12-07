from freedictionaryapi.clients.sync_client import DictionaryApiClient
from freedictionaryapi import LanguageCodes
from freedictionaryapi.errors import DictionaryApiError

client = DictionaryApiClient()
parser = None
error = DictionaryApiError
english = LanguageCodes.ENGLISH_UK


