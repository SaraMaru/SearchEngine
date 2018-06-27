import similar_terms
from nltk.corpus import wordnet as wn
import nltk
import re
#import itertools

def similar_query(tokens):
	tagged = nltk.pos_tag(tokens,tagset='universal')
	suggest_terms = dict()
	for (term,tag) in tagged:
		need_to_change = True
		if tag=="NOUN":
			pos = wn.NOUN
		elif tag=="VERB":
			pos = wn.VERB
		elif tag=="ADJ":
			pos = wn.ADJ
		elif tag=="ADV":
			pos = wn.ADV
		else:
			need_to_change = False
		if need_to_change:
			t = similar_terms.get_the_most_similar_term(term,pos)
			if t:
				suggest_terms[term] = t
	print(suggest_terms)

	'''suggest_queries = list()
	for l in itertools.product([0,1],repeat=len(tokens)):
		query = list()
		for i in range(0,len(l)):
			if l[i]==0:
				query.append(tokens[i])
			elif tokens[i] in suggest_terms:
				query.append(suggest_terms[tokens[i]])
			else:
				break
		if(len(query)==len(l)):
			suggest_queries.append(query)'''
	suggest_query = tokens + list(suggest_terms.values())
	return suggest_query


def wildcard_query(term_list,tokens):
	suggest_map = dict()
	for token in tokens:
		if re.search('(\*|\?)',token):
			suggest_map[token] = list()
			pattern = token.replace("*",".*").replace("?",".")
			print(pattern)
			for term in term_list:
				if re.search(pattern,term):
					suggest_map[token].append(term)
	print(suggest_map)
	return suggest_map


def find_wildcard_tokens(tokens,result):
	for token in tokens:
		if re.search('(\*|\?)',token):
			result.add(token)


def check_spelling(token): #only for debug
	print(token,"OK")
	return [1,2]


def bool_search(sentence): #only for debug
	print("bool",sentence)
	return [1,2]


def VSM_search(sentence): #only for debug
	print("VSM",sentence)
	return [1,2]


def phase_search(tokens): #only for debug
	print("phase",sentence)
	return [1,2]


def make_query(sentence):
	if FLAG_PHRASE:
		if FLAG_WILDCARD or FLAG_BOOL:
			print("ERROR: Do not support this mode combination!")
	tokens = nltk.word_tokenize(sentence)

	wildcard_map = dict()
	if FLAG_WILDCARD:
		wildcard_map = wildcard_query(term_list,tokens) # need the list of all terms

	for token in tokens:
		if token not in wildcard_map:
			if re.match('[a-zA-Z]+?$',token): # is a word
				if FLAG_BOOL and not re.match('(AND$)|(OR$)|(NOT$)',token): # not AND/OR/NOT
					check_spelling(token) # need to write a function for it; it only needs to print a suggestion
	
	if FLAG_BOOL:
		query = ""
		for token in tokens:
			if token in wildcard_map:
				query += " ( "
				for index,term in enumerate(wildcard_map[token]):
					if index==0:
						query = query + " " + term
					else:
						query = query + " OR " + term
				query += " ) "
			else:
				query = query + " " + token
		file_list = bool_search(query) # need to write a function for it

	elif FLAG_PHRASE:
		file_list = phase_search(tokens)

	else:
		new_query = tokens
		for terms in wildcard_map.values():
			new_query += terms
		file_list = VSM_search(new_query)
		if(len(file_list)<5):
			suggest_query = similar_query(new_query)
			file_list = VSM_search(suggest_query)

	return file_list







term_list = ["apple","app","application","apolo","bppb","appnd"]
FLAG_WILDCARD = True
FLAG_BOOL = False
FLAG_PHRASE = False

if __name__ == "__main__":
	fl = make_query(" ( love AND computer ) AND app*n OR B2B AND ANDE")
	print(fl)