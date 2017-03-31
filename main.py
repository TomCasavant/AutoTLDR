from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from twython import TwythonStreamer
LANGUAGE = "english"

def getSummary(url, sentences):
	"""Gets summary of article using sumy""" 
	parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
	stemmer = Stemmer(LANGUAGE)

	summarizer = Summarizer(stemmer)
	summarizer.stop_words = get_stop_words(LANGUAGE)
	return summarizer(parser.document, sentences)

class myStreamer(TwythonStreamer):
	def on_success(self, data):
		if 'text' in data:
			print data['text'].encode('utf-8')

	def on_error(self, status_code, data):
		print status_code


if __name__ == '__main__':
	APP_KEY = ConfigParser.get('twitter', 'APP_KEY')
	APP_SECRET = ConfigParser.get('twitter', 'APP_SECRET')
	OAUTH_TOKEN = ConfigParser.get('twitter', 'OAUTH_TOKEN')
	OAUTH_SECRET = ConfigParser.get('twitter', 'OAUTH_SECRET')

	stream = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_SECRET)
	stream.statuses.filter(track='NPR')
getSummary("http://www.npr.org/sections/thetwo-way/2017/03/31/522199535/judge-approves-25-million-settlement-of-trump-university-lawsuit"):

