from freedictionaryapi import LanguageCodes
from freedictionaryapi.clients.sync_client import DictionaryApiClient
client = DictionaryApiClient()
for language in LanguageCodes:
    print(language)

pala = input("Digite a palavra\n")
parser = client.fetch_parser(pala, LanguageCodes.ENGLISH_UK)
print(parser.get_transcription())
print(parser.get_all_definitions())
print(parser.get_all_synonyms())

client.close()
