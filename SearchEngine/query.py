import similar_terms
from nltk.corpus import wordnet as wn
import nltk
import itertools
import re

def similar_search(sentence):
	tokens = nltk.word_tokenize(sentence)
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
			suggest_terms[term] = similar_terms.get_the_most_similar_term(term,pos)
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
	print(suggest_query)


def wildcard_search(term_list,sentence):
	tokens = nltk.word_tokenize(sentence)
	suggest_query = tokens
	for token in tokens:
		if re.search('(\*|\?|\+)',token):
			suggest_query.remove(token)
			pattern = token
			print(pattern)
			for term in term_list:
				if re.search(pattern,term):
					suggest_query.append(term)
	print(suggest_query)


term_list = ["apple","app","application","apolo","bppb","appnd"]
similar_search("I see dead people")
similar_search("stay foolish")
wildcard_search(term_list,"a app* doc")
wildcard_search(term_list,"a app+ doc")
wildcard_search(term_list,"a app*n doc")