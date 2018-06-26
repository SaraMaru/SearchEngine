import similar_terms
from nltk.corpus import wordnet as wn
import nltk

sentence = """At eight o'clock on Thursday morning Arthur didn't feel very good."""
tokens = nltk.word_tokenize(sentence)
print(tokens)
tagged = nltk.pos_tag(tokens,tagset='universal')
print(tagged)
for (term,tag) in tagged:
	print(term,tag)
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
		print(similar_terms.get_similar_terms(term,pos))