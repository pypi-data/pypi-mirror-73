import re
from collections import Counter

# PATTERNS
EMAIL_REGEX =  re.compile(r"[\w\.-]+@[\w\.-]+")
NUMBERS_REGEX = re.compile(r"\d+")
PHONE_REGEX = re.compile(r"[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]")
SPECIAL_CHARACTERS_REGEX = re.compile(r"[^A-Za-z0-9 ]+")
EMOJI_REGEX = re.compile("["
                       u"\U0001F600-\U0001F64F"  # for emoticons
                       u"\U0001F300-\U0001F5FF"  # for symbols & pictographs
                       u"\U0001F680-\U0001F6FF"  # for transport & map symbols
                       u"\U0001F1E0-\U0001F1FF"  # for flags (iOS)
                       u"\U00002702-\U000027B0"
                       u"\U000024C2-\U0001F251"
                       "]+", flags=re.UNICODE)

DATE_REGEX = re.compile(r"([0-9]{2}\/[0-9]{2}\/[0-9]{4})|([0-9]{4}\/[0-9]{2}\/[0-9]{2})")

# modified source :https://gist.github.com/dperini/729294
URL_PATTERN = re.compile(
    r"(?:^|(?<![\w\/\.]))"
    # protocol identifier
    # r"(?:(?:https?|ftp)://)"  <-- alt?
    r"(?:(?:https?:\/\/|ftp:\/\/|www\d{0,3}\.))"
    # user:pass authentication
    r"(?:\S+(?::\S*)?@)?" r"(?:"
    # IP address exclusion
    # private & local networks
    r"(?!(?:10|127)(?:\.\d{1,3}){3})"
    r"(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})"
    r"(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})"
    # IP address dotted notation octets
    # excludes loopback network 0.0.0.0
    # excludes reserved space >= 224.0.0.0
    # excludes network & broadcast addresses
    # (first & last IP address of each class)
    r"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
    r"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}"
    r"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"
    r"|"
    # host name
    r"(?:(?:[a-z\\u00a1-\\uffff0-9]-?)*[a-z\\u00a1-\\uffff0-9]+)"
    # domain name
    r"(?:\.(?:[a-z\\u00a1-\\uffff0-9]-?)*[a-z\\u00a1-\\uffff0-9]+)*"
    # TLD identifier
    r"(?:\.(?:[a-z\\u00a1-\\uffff]{2,}))" r")"
    # port number
    r"(?::\d{2,5})?"
    # resource path
    r"(?:\/[^\)\]\}\s]*)?",
    flags=re.UNICODE | re.IGNORECASE,
)

CURRENCY_REGEX = re.compile(
    r"[$¢£¤¥ƒ֏؋৲৳૱௹฿៛ℳ元円圆圓﷼\u20A0-\u20C0]\d+",
    flags=re.UNICODE)

CURRENCY_SYMB_REGEX = re.compile(
    r"[$¢£¤¥ƒ֏؋৲৳૱௹฿៛ℳ元円圆圓﷼\u20A0-\u20C0]",
    flags=re.UNICODE)

# PHONE_REGEX = re.compile(
#     r"(?:^|(?<=[^\w)]))(\+?1[ .-]?)?(\(?\d{3}\)?[ .-]?)?(\d{3}[ .-]?\d{4})"
#     r"(\s?(?:ext\.?|[#x-])\s?\d{2,6})?(?:$|(?=\W))",
#     flags=re.UNICODE | re.IGNORECASE)

STOPWORDS = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

# Metrics
class TextMetrics(object):
	""" TextMetrics : analyses a text for vowels,consonants,etc

	  t1 = TextMetrics(text="Your text Here")
	  t1.word_stats()
	  t1.count_vowels()
	  t1.count_consonants()

	"""
	def __init__(self, text=None):
		super(TextMetrics, self).__init__()
		self.text = text
	

	def __repr__(self):
		return 'TextMetrics(text="{}")'.format(self.text)

	def count_vowels(self):
		words = self.text.lower()
		result = {v:words.count(v) for v in 'aeiou'}
		return result

	def count_consonants(self):
		words = self.text.lower()
		result = {v:words.count(v) for v in 'bcdfghjklmnpqrstvwxyz'}
		return result

	def count_stopwords(self):
		result = [word for word in self.text.lower().split() if word in STOPWORDS]
		final_res = Counter(result)
		return final_res

	def word_stats(self):
		words = self.text.lower()
		result_all_words = Counter(words.split())
		result_stopwords = [word for word in self.text.lower().split() if word in STOPWORDS]
		vowels_num = sum(self.count_vowels().values())
		consonants_num = sum(self.count_consonants().values())
		stats_dict = {"Length of Text":len(words),"Num of Vowels":vowels_num,
		"Num of Consonants":consonants_num,"Num of Stopwords":len(result_stopwords),
		"Stats of Vowels":self.count_vowels(),
		"Stats of Consonants":self.count_consonants(),
		}
		return stats_dict


	@property
	def vowels(self):
		words = self.text.lower()
		result = {v:words.count(v) for v in 'aeiou'}
		return result

	@property 
	def consonants(self):
		words = self.text.lower()
		result = {v:words.count(v) for v in 'bcdfghjklmnpqrstvwxyz'}
		return result

	@property 
	def length(self):
		return len(self.text.lower())
		



# Remove Emails/Phone number/Emoji/Stopwords/etc

class TextCleaner(TextMetrics):
	""" TextCleaner: removes and cleans emails,numbers,etc from text

	usage
	docx = TextCleaner(text="your text here")
	
	"""
	def __init__(self, text=None):
		super(TextCleaner, self).__init__()
		self.text = text

	def __str__(self):
		return '{}'.format(self.text)

	def __repr__(self):
		return 'TextCleaner(text="{}")'.format(self.text)
		

	def remove_emails(self):
		"""Returns A String with the emails removed """
		self.text = re.sub(EMAIL_REGEX,"",self.text)
		return self

	def remove_numbers(self):
		"""Returns A String with the numbers/digits removed """
		self.text = re.sub(NUMBERS_REGEX,"",self.text)
		return self

	def remove_phone_numbers(self):
		"""Returns A String with the phone numbers removed """
		self.text = re.sub(PHONE_REGEX,"",self.text)
		return self


	def remove_special_characters(self):
		"""Returns A String with the specified characters removed """
		self.text = re.sub(SPECIAL_CHARACTERS_REGEX,"",self.text)
		return self

	def remove_emojis(self):
		"""Returns A String with the emojis removed """
		self.text = re.sub(EMOJI_REGEX,"",self.text)
		return self

	def remove_stopwords(self):
		"""Returns A String with the stopwords removed """
		result = [word for word in self.text.split() if word not in STOPWORDS]
		return ' '.join(result)

	def remove_urls(self):
		"""Returns A String with URLS removed """
		self.text = re.sub(URL_PATTERN,"",self.text)
		return self

	def remove_currencies(self):
		"""Returns A String with Currencies removed """
		self.text = re.sub(CURRENCY_REGEX,"",self.text)
		return self

	def remove_currency_symbols(self):
		"""Returns A String with Currency Symbols removed """
		self.text = re.sub(CURRENCY_SYMB_REGEX,"",self.text)
		return self

	def remove_dates(self):
		self.text = re.sub(DATE_REGEX,"",self.text)
		return self

	def replace_emails(self,replace_with="<EMAIL>"):
		"""Replaces the emails in the text with custom label"""
		result = re.sub(EMAIL_REGEX,replace_with,self.text)
		return result
	
	def replace_phone_numbers(self,replace_with="<PHONENUMBER>"):
		"""Replaces the phone numbers in the text with custom label"""
		result = re.sub(PHONE_REGEX,replace_with,self.text)
		return result

	def replace_numbers(self,replace_with="<NUMBER>"):
		"""Replaces numbers/digits in the text with custom label"""
		result = re.sub(NUMBERS_REGEX,replace_with,self.text)
		return result

	def replace_special_characters(self,replace_with="<SPECIAL_CHAR>"):
		"""Replaces special characters in the text with custom label"""
		result = re.sub(SPECIAL_CHARACTERS_REGEX,replace_with,self.text)
		return result

	def replace_emojis(self,replace_with="<EMOJI>"):
		"""Replaces emojis in the text with custom label"""
		result = re.sub(EMOJI_REGEX,replace_with,self.text)
		return result

	def replace_urls(self,replace_with="<URL>"):
		"""Replaces URLS/HTTP(S) in the text with custom label"""
		result = re.sub(URL_PATTERN,replace_with,self.text)
		return result

	def replace_currencies(self,replace_with="<CURRENCY>"):
		"""Replaces Currencies in the text with custom label"""
		result = re.sub(CURRENCY_REGEX,replace_with,self.text)
		return result

	def replace_currency_symbols(self,replace_with="<CURRENCY_SYMB>"):
		"""Replaces currency symbols in the text with custom label"""
		result = re.sub(CURRENCY_SYMB_REGEX,replace_with,self.text)
		return result

	def replace_dates(self,replace_with="<DATE>"):
		"""Replaces Dates in the text with custom label"""
		result = re.sub(DATE_REGEX,replace_with,self.text)
		return result


	def clean_text(self,preserve=False):
		"""
		Clean entire text 
		
		Parameters
		----------
		self

		preserve:Boolean(True/False) default is True
			preserves or keeps the original labels of what was cleaned.

		Returns
		-------
		string
	
		"""
		if preserve == False:
			email_result = re.sub(EMAIL_REGEX,"",self.text)
			phone_result = re.sub(PHONE_REGEX,"",email_result)
			number_result = re.sub(NUMBERS_REGEX,"",phone_result)
			url_result = re.sub(URL_PATTERN,"",number_result)
			emoji_result = re.sub(EMOJI_REGEX,"",url_result)
			special_char_result = re.sub(SPECIAL_CHARACTERS_REGEX,"",emoji_result)
			final_result = special_char_result.lower()
			
		else:
			special_char_result = re.sub(r'[^A-Za-z0-9@ ]+',"",self.text)
			email_result = re.sub(EMAIL_REGEX,"<EMAIL>",special_char_result)
			phone_result = re.sub(PHONE_REGEX,"<PHONENUMBER>",email_result)
			number_result = re.sub(NUMBERS_REGEX,"<NUMBERS>",phone_result)
			url_result = re.sub(URL_PATTERN,"<URL>",number_result)
			emoji_result = re.sub(EMOJI_REGEX,"<EMOJI>",url_result)
			final_result = emoji_result.lower()
			
		return final_result





class TextExtractor(TextCleaner):
	""" TextExtractor: extracts emails,numbers,etc from text
	
	docx = TextExtractor(text="your text here")
	docx.extract_emails()
	
	"""
	def __init__(self, text=None):
		super(TextExtractor, self).__init__()
		self.text = text

	def __repr__(self):
		return 'TextExtractor(text="{}")'.format(self.text)

	def extract_emails(self):
		"""Returns the emails extracted """
		result = re.findall(EMAIL_REGEX,self.text)
		return result

	def extract_numbers(self):
		"""Returns the numbers/digits extracted """
		result = re.findall(NUMBERS_REGEX,self.text)
		return result

	def extract_phone_numbers(self):
		"""Returns the phone number extracted """
		result = re.findall(PHONE_REGEX,self.text)
		return result


	def extract_special_characters(self):
		"""Returns the specified characters extracted """
		result = re.findall(SPECIAL_CHARACTERS_REGEX,self.text)
		return result

	def extract_emojis(self):
		"""Returns the emojis extracted """
		result = re.findall(EMOJI_REGEX,self.text)
		return result

	def extract_stopwords(self):
		"""Returns the stopwords as a list """
		result = [word for word in self.text.split() if word in STOPWORDS]
		return result
	
	def extract_urls(self):
		"""Returns the URLS extracted """
		result = re.findall(URL_PATTERN,self.text)
		return result

	def extract_currencies(self):
		"""Returns the currencies extracted """
		result = re.findall(CURRENCY_REGEX,self.text)
		return result

	def extract_currency_symbols(self):
		"""Returns the currency symbols extracted """
		result = re.findall(CURRENCY_SYMB_REGEX,self.text)
		return result

	def extract_dates(self):
		"""Returns the dates extracted """
		result = re.findall(DATE_REGEX,self.text)
		return result


