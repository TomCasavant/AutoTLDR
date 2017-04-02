from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import time
from ConfigParser import SafeConfigParser
from twython import TwythonStreamer
from twython import Twython


LANGUAGE = "english"

def getSummary(url, sentences):
	"""Gets summary of article using sumy""" 
	parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
	stemmer = Stemmer(LANGUAGE)

	summarizer = Summarizer(stemmer)
	summarizer.stop_words = get_stop_words(LANGUAGE)
	fullText = ""
	for sentence in summarizer(parser.document, sentences):
		fullText += str(sentence) + " "

	return fullText

class myStreamer(TwythonStreamer):
	def on_success(self, data):
		"""If data received, check if this is an original tweet from one of chosen news sources, then reply"""
		if 'text' in data:
			try:
				if not data['retweeted'] and not data['in_reply_to_status_id'] and '@' not in data['text'] and not data['quoted_status_id']:
					reply(data['entities']['urls'][0]['expanded_url'], data['id_str'], data['user']['screen_name'])
				#	print "Responded"
			except:
				pass
	def on_timeout(self, data):
		print "Timeout"
	def on_error(self, status_code, data):
		print status_code

def splitText(text, n):
	"""Splits text every n characters"""
	newText = []
	while text:
		newText.append(text[:n])
		text = text[n:]
	return newText #TODO Split text at end of words, don't split in the middle

def reply(url, id, screen_name):
	"""Replies to a tweet with summary given id"""
	#print id
	summary = getSummary(url, 3)
	split = splitText(summary, 140) #Splits text every 140 characters
	id = twitter.update_status(status= ("@"+ screen_name + " Here is a short summary of the posted link: "), in_reply_to_status_id=id)['id'] #Posts initial tweet and saves ID
	for segment in split:
		#Send tweet for every 140 characters in reply format
		id = twitter.update_status(status=segment, in_reply_to_status_id=id)['id']

if __name__ == '__main__':
	parser = SafeConfigParser()
	parser.read("config.ini")
	API_KEY = parser.get('twitter', 'API_KEY')
	API_SECRET = parser.get('twitter', 'API_SECRET')
	ACCESS_TOKEN = parser.get('twitter', 'ACCESS_TOKEN')
	ACCESS_SECRET = parser.get('twitter', 'ACCESS_SECRET')

	twitter = Twython(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
	stream = myStreamer(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
	stream.statuses.filter(follow=['5392522', '612473', '5402612','742143','5741722'], filter_level='low') #Reads from certain Twitter Accounts (@NPR, @BBC, @BBCNews...)
