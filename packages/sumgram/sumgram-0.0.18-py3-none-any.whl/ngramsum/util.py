import json
import os
import requests
import sys

from subprocess import check_output
from multiprocessing import Pool

def genericErrorInfo(errOutfileName='', errPrefix=''):
	exc_type, exc_obj, exc_tb = sys.exc_info()
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	errorMessage = fname + ', ' + str(exc_tb.tb_lineno)  + ', ' + str(sys.exc_info())
	print('\tERROR:', errorMessage)
	
	mode = 'w'
	if( os.path.exists(errOutfileName) ):
		mode = 'a'

	if( len(errPrefix) != 0 ):
		errPrefix = errPrefix + ': '

	errOutfileName = errOutfileName.strip()
	if( len(errOutfileName) != 0 ):
		outfile = open(errOutfileName, mode)
		outfile.write(getNowFilename() + '\n')
		outfile.write('\t' + errPrefix + errorMessage + '\n')
		outfile.close()

	return  sys.exc_info()

def getStopwordsSet(frozenSetFlag=False):
	
	stopwords = getStopwordsDict()
	
	if( frozenSetFlag ):
		return frozenset(stopwords.keys())
	else:
		return set(stopwords.keys())

def getStopwordsDict():

	stopwordsDict = {
		"a": True,
		"about": True,
		"above": True,
		"across": True,
		"after": True,
		"afterwards": True,
		"again": True,
		"against": True,
		"all": True,
		"almost": True,
		"alone": True,
		"along": True,
		"already": True,
		"also": True,
		"although": True,
		"always": True,
		"am": True,
		"among": True,
		"amongst": True,
		"amoungst": True,
		"amount": True,
		"an": True,
		"and": True,
		"another": True,
		"any": True,
		"anyhow": True,
		"anyone": True,
		"anything": True,
		"anyway": True,
		"anywhere": True,
		"are": True,
		"around": True,
		"as": True,
		"at": True,
		"back": True,
		"be": True,
		"became": True,
		"because": True,
		"become": True,
		"becomes": True,
		"becoming": True,
		"been": True,
		"before": True,
		"beforehand": True,
		"behind": True,
		"being": True,
		"below": True,
		"beside": True,
		"besides": True,
		"between": True,
		"beyond": True,
		"both": True,
		"but": True,
		"by": True,
		"can": True,
		"can\'t": True,
		"cannot": True,
		"cant": True,
		"co": True,
		"could not": True,
		"could": True,
		"couldn\'t": True,
		"couldnt": True,
		"de": True,
		"describe": True,
		"detail": True,
		"did": True,
		"do": True,
		"does": True,
		"doing": True,
		"done": True,
		"due": True,
		"during": True,
		"e.g": True,
		"e.g.": True,
		"e.g.,": True,
		"each": True,
		"eg": True,
		"either": True,
		"else": True,
		"elsewhere": True,
		"enough": True,
		"etc": True,
		"etc.": True,
		"even though": True,
		"ever": True,
		"every": True,
		"everyone": True,
		"everything": True,
		"everywhere": True,
		"except": True,
		"for": True,
		"former": True,
		"formerly": True,
		"from": True,
		"further": True,
		"get": True,
		"go": True,
		"had": True,
		"has not": True,
		"has": True,
		"hasn\'t": True,
		"hasnt": True,
		"have": True,
		"having": True,
		"he": True,
		"hence": True,
		"her": True,
		"here": True,
		"hereafter": True,
		"hereby": True,
		"herein": True,
		"hereupon": True,
		"hers": True,
		"herself": True,
		"him": True,
		"himself": True,
		"his": True,
		"how": True,
		"however": True,
		"i": True,
		"ie": True,
		"i.e": True,
		"i.e.": True,
		"if": True,
		"in": True,
		"inc": True,
		"inc.": True,
		"indeed": True,
		"into": True,
		"is": True,
		"it": True,
		"its": True,
		"it's": True,
		"itself": True,
		"just": True,
		"keep": True,
		"latter": True,
		"latterly": True,
		"less": True,
		"made": True,
		"make": True,
		"may": True,
		"me": True,
		"meanwhile": True,
		"might": True,
		"mine": True,
		"more": True,
		"moreover": True,
		"most": True,
		"mostly": True,
		"move": True,
		"must": True,
		"my": True,
		"myself": True,
		"namely": True,
		"neither": True,
		"never": True,
		"nevertheless": True,
		"next": True,
		"no": True,
		"nobody": True,
		"none": True,
		"noone": True,
		"nor": True,
		"not": True,
		"nothing": True,
		"now": True,
		"nowhere": True,
		"of": True,
		"off": True,
		"often": True,
		"on": True,
		"once": True,
		"one": True,
		"only": True,
		"onto": True,
		"or": True,
		"other": True,
		"others": True,
		"otherwise": True,
		"our": True,
		"ours": True,
		"ourselves": True,
		"out": True,
		"over": True,
		"own": True,
		"part": True,
		"per": True,
		"perhaps": True,
		"please": True,
		"put": True,
		"rather": True,
		"re": True,
		"same": True,
		"see": True,
		"seem": True,
		"seemed": True,
		"seeming": True,
		"seems": True,
		"several": True,
		"she": True,
		"should": True,
		"show": True,
		"side": True,
		"since": True,
		"sincere": True,
		"so": True,
		"some": True,
		"somehow": True,
		"someone": True,
		"something": True,
		"sometime": True,
		"sometimes": True,
		"somewhere": True,
		"still": True,
		"such": True,
		"take": True,
		"than": True,
		"that": True,
		"the": True,
		"their": True,
		"theirs": True,
		"them": True,
		"themselves": True,
		"then": True,
		"thence": True,
		"there": True,
		"thereafter": True,
		"thereby": True,
		"therefore": True,
		"therein": True,
		"thereupon": True,
		"these": True,
		"they": True,
		"this": True,
		"those": True,
		"though": True,
		"through": True,
		"throughout": True,
		"thru": True,
		"thus": True,
		"to": True,
		"together": True,
		"too": True,
		"toward": True,
		"towards": True,
		"un": True,
		"until": True,
		"upon": True,
		"us": True,
		"very": True,
		"via": True,
		"was": True,
		"we": True,
		"well": True,
		"were": True,
		"what": True,
		"whatever": True,
		"when": True,
		"whence": True,
		"whenever": True,
		"where": True,
		"whereafter": True,
		"whereas": True,
		"whereby": True,
		"wherein": True,
		"whereupon": True,
		"wherever": True,
		"whether": True,
		"which": True,
		"while": True,
		"whither": True,
		"who": True,
		"whoever": True,
		"whole": True,
		"whom": True,
		"whose": True,
		"why": True,
		"will": True,
		"with": True,
		"within": True,
		"without": True,
		"would": True,
		"yet": True,
		"you": True,
		"your": True,
		"yours": True,
		"yourself": True,
		"yourselves": True
	}
	
	return stopwordsDict

def sortDctByKey(dct, key, reverse=True):

	key = key.strip()
	if( len(dct) == 0 or len(key) == 0 ):
		return []

	return sorted(dct.items(), key=lambda x: x[1][key], reverse=reverse)

def dumpJsonToFile(outfilename, dictToWrite, indentFlag=True, extraParams=None):

	if( extraParams is None ):
		extraParams = {}

	extraParams.setdefault('verbose', True)

	try:
		outfile = open(outfilename, 'w')
		
		if( indentFlag ):
			json.dump(dictToWrite, outfile, ensure_ascii=False, indent=4)#by default, ensure_ascii=True, and this will cause  all non-ASCII characters in the output are escaped with \uXXXX sequences, and the result is a str instance consisting of ASCII characters only. Since in python 3 all strings are unicode by default, forcing ascii is unecessary
		else:
			json.dump(dictToWrite, outfile, ensure_ascii=False)

		outfile.close()

		if( extraParams['verbose'] ):
			print('\twriteTextToFile(), wrote:', outfilename)
	except:
		if( extraParams['verbose'] ):
			print('\terror: outfilename:', outfilename)
		genericErrorInfo()

def readTextFromFile(infilename):

	text = ''

	try:
		with open(infilename, 'r') as infile:
			text = infile.read()
	except:
		print('\treadTextFromFile()error filename:', infilename)
		genericErrorInfo()
	

	return text

#nlp server - start

def nlpIsServerOn(addr='http://localhost:9000'):

	try:
		response = requests.head(addr)
		
		if( response.status_code == 200 ):
			return True
		else:
			return False

	except:
		genericErrorInfo()

	return False

def nlpSentenceAnnotate(text, parsed={}, host='localhost', port='9000'):

	payload = { 'sentences': [] }
	if( text == '' ):
		return payload

	#see annotators: https://stanfordnlp.github.io/CoreNLP/annotators.html
	#lemma annotator also does: tokenize, ssplit, pos
	request = host + ':' + port + '/?properties={"annotators":"lemma","outputFormat":"json"}'
	
	try:
		if( len(parsed) == 0 ):
			parsed = check_output(['wget', '-q', '-O', '-', '--post-data', text, request])

		parsed = parsed.decode('utf-8')
		parsed = json.loads( parsed )
		#dumpJsonToFile( 'ner_output.json', parsed )#for debugging 

		if( 'sentences' not in parsed ):
			return []

		for sentence in parsed['sentences']:

			if( 'tokens' not in sentence ):
				continue
			
			payload['sentences'].append({
				'tokens': [],
				'sentence': ''
			})

			singleSentence = ''
			lemmatizedSentence = ''
			sentenceSize = len(sentence['tokens'])

			for i in range( sentenceSize ):

				tok = sentence['tokens'][i]
				payload['sentences'][-1]['tokens'].append({
					'pos': tok['pos'],
					'tok': tok['originalText'],
					'lemma': tok['lemma']
				})

				lemmatizedSentence = lemmatizedSentence + tok['lemma'] + tok['after']
				singleSentence = singleSentence + tok['originalText'] + tok['after']
			
			if( sentenceSize != 0 ):
				
				st = sentence['tokens'][0]['characterOffsetBegin']
				en = sentence['tokens'][sentenceSize - 1]['characterOffsetBegin'] + 1
				payload['sentences'][-1]['sentence'] = text[ st:en ]
				
				#payload['sentences'][-1]['sentence'] = singleSentence.strip()
				payload['sentences'][-1]['lemmatized_sentence'] = lemmatizedSentence.strip()

	except:
		genericErrorInfo()

	return payload

def nlpServerStartStop(msg='start'):

	if( msg == 'start' ):
		try:
			if( nlpIsServerOn() ):
				print('\tCoreNLP Server already on - no-op')
			else:
				print('\tStarting CoreNLP Server')
				#docker run --rm -d -p 9000:9000 --name stanfordcorenlp anwala/stanfordcorenlp
				check_output([
					'docker', 
					'run', 
					'--rm', 
					'-d', 
					'-p', 
					'9000:9000', 
					'--name',
					'stanfordcorenlp',
					'anwala/stanfordcorenlp'
				])

				#warm up server (preload libraries, so subsequent responses are quicker)
				nlpGetEntitiesFromText('A quick brown fox jumped over the lazy dog')
		except:
			genericErrorInfo()
	elif( msg == 'stop' ):
		try:
			check_output(['docker', 'rm', '-f', 'stanfordcorenlp'])
		except:
			genericErrorInfo()

#nlp server - end

def overlapFor2Sets(firstSet, secondSet):

	intersection = float(len(firstSet & secondSet))
	minimum = min(len(firstSet), len(secondSet))

	if( minimum != 0 ):
		return  round(intersection/minimum, 4)
	else:
		return 0

def parallelProxy(job):
	
	output = job['func'](**job['args'])

	if( 'print' in job ):
		if( len(job['print']) != 0 ):
			print(job['print'])

	return {'input': job, 'output': output, 'misc': job['misc']}

def parallelTask(jobsLst, threadCount=5):

	if( len(jobsLst) == 0 ):
		return []

	if( threadCount < 2 ):
		threadCount = 2

	try:
		workers = Pool(threadCount)
		resLst = workers.map(parallelProxy, jobsLst)

		workers.close()
		workers.join()
	except:
		genericErrorInfo()
		return []

	return resLst