from nltk.corpus import wordnet as wn 

# weight = sum_for_all_synsets((count_synset_interm+a)*(count_synset_outterm+b)) / sum_for_all_synsets(count_synset_interm+a)
def calc_similarity(input_term):
	a = 2
	b = 2
	synsets = wn.synsets(input_term) # synsets may be []
	term_weight_dict = dict()
	count_interm = 0

	for synset in synsets:
		count_synset_interm = 0
		for lemma in synset.lemmas():
			if lemma.name()==input_term:
				count_synset_interm += lemma.count()
				break
		count_interm += count_synset_interm

		for lemma in synset.lemmas():
			term = lemma.name()
			if term!=input_term:
				weight = (count_synset_interm+a) * (lemma.count()+b)
				if term in term_weight_dict:
					weight += term_weight_dict[term]
				term_weight_dict[term] = weight 

	for term,weight in term_weight_dict.items():
		term_weight_dict[term] = weight / (count_interm+a*len(synsets))
	return term_weight_dict

def choose_similar_terms(term_weight_dict):
	cut_line = 0.2
	smooth = 0.7
	new_term_weight_dict = dict()
	max_weight = max(term_weight_dict.values())
	for term,weight in term_weight_dict.items():
		if weight>max_weight*cut_line:
			new_term_weight_dict[term] = (weight/max_weight)**smooth
	return new_term_weight_dict

def get_similar_terms(input_term):
	term_weight_dict = calc_similarity(input_term)
	#print(term_weight_dict)
	new_term_weight_dict = choose_similar_terms(term_weight_dict)
	return new_term_weight_dict

###################################################################################

if __name__ == "__main__":
	print(get_similar_terms("USA"))
	print(get_similar_terms("car"))
	print(get_similar_terms("search"))
	print(get_similar_terms("seek"))
	print(get_similar_terms("happy"))
	print(get_similar_terms("felicitous"))
	print(get_similar_terms("sad"))