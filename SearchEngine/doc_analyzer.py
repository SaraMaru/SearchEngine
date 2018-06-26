import nltk
import re
import os
import glob
import json

CLUSTER_SIZE = 200

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def save_as_json(data,json_name):
	with open(json_name, 'w') as f:
		json.dump(data, f)
	print("save_as_json() completed")

def read_data_from_files(file_names):
	postings = dict()
	"""
	postings is likes this:
	{ term_a : { doc_id_x : [ pos1, pos2 ] ,
				 doc_id_y : [ pos3, pos4 ] }
	  term_b : { doc_id_y : [ pos5, pos6 ] ,
			     doc_id_z : [ pos7, pos8 ] } }
	"""

	for doc_id,file_name in enumerate(file_names):
		file = open(file_name,"r")
		content = file.read()
		#print(content)
		tokens = nltk.word_tokenize(content)
		#print(tokens)
		stemmer = nltk.stem.snowball.SnowballStemmer("english")
		stemmed_tokens = [ stemmer.stem(token) for token in tokens ]
		#print(stemmed_tokens)
		result_tokens = []
		for token in stemmed_tokens:
			if re.search('(\D/|/\D)',token):
				for tk in re.split('(/)',token):
					result_tokens.append(tk)
			else:
				result_tokens.append(token)
		#print(result_tokens)
		print(doc_id+1,"/",len(file_names))

		for pos,token in enumerate(result_tokens):
			if token in postings:
				if doc_id in postings[token]:
					postings[token][doc_id].append(pos)
				else:
					postings[token][doc_id] = [pos]
			else:
				postings[token] = dict()
				postings[token][doc_id] = [pos]
	#print(postings)

	tf_info = dict()
	"""
	tf_info is likes this:
	{ term_a : {    -1    : df_a  ,
				 doc_id_x : tf_ax ,
				 doc_id_y : tf_ay }
	  term_b : {    -1    : df_b  ,
	  			 doc_id_y : tf_by ,
			     doc_id_z : tf_bz } }
	"""

	for term,posting in postings.items():
		if term not in tf_info:
			tf_info[term] = dict()
		df = 0
		for doc_id,pos_list in posting.items():
			tf_info[term][doc_id] = len(pos_list)
			df += 1
		tf_info[term][-1] = df #the doc_id of -1 means df
	#print(tf_info)

	data = [postings, tf_info]
	"""
	data is like this:
	[postings, tf_info]
	"""
	return data

def read_data_from_path(src_path, dest_path):
	json_name = dest_path+"filenames.json"
	old_file_names = list()
	if os.path.exists(json_name):
		with open(json_name, 'r') as f:
			old_file_names = json.load(f)
	file_names = glob.glob(src_path+"*.html")
	new_file_names = list(set(file_names).difference(set(old_file_names)))
	print("Found",len(new_file_names),"new files.")
	if(len(new_file_names)==0):
		return
	
	pos_file_names = glob.glob(dest_path+"pos[0-9]*.json")
	indices = list()
	for name in pos_file_names:
		str_id = re.search("pos([0-9]*).json",name).group(1)
		indices.append(int(str_id))
	if len(indices)>0: 
		last_index = max(indices)
	else:
		last_index = -1

	start_index = last_index + 1
	print("The new data file index will start from",start_index,".")
	for index,file_names_part in enumerate(chunks(new_file_names,CLUSTER_SIZE)):
		[postings,tf_info] = read_data_from_files(file_names_part)
		save_as_json(postings, dest_path+"pos"+str(start_index+index)+".json")
		save_as_json(tf_info, dest_path+"tf"+str(start_index+index)+".json")

	save_as_json(file_names, json_name)


###################################################################################

if __name__ == "__main__":
	source_path = "../../one/"
	destination_path = "../TermResource/"
	read_data_from_path(source_path, destination_path)