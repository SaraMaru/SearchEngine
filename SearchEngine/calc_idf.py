import glob
import json
import math

def calc_idf(file_path,json_path):
	all_df = dict()
	json_names = glob.glob(json_path+"tf*.json")
	for json_name in json_names:
		with open(json_name, 'r') as f:
			tf_info = json.load(f)
		for term,dic in tf_info.items():
			if term in all_df:
				all_df[term] += dic["-1"] # dic[-1] saves df
			else:
				all_df[term] = dic["-1"]
		print("Finished dealing with",json_name)

	file_names = glob.glob(file_path+"*.html")
	file_num = len(file_names)
	all_idf = dict()
	for term,df in all_df.items():
		all_idf[term] = math.log(file_num/df)
	print(all_idf)

	with open(json_path+"idf.json", 'w') as f:
		json.dump(all_idf, f)
	print("calc_idf() completed")


###################################################################################

if __name__ == "__main__":
	file_path = "../../one/"
	json_path = "../TermResource/"
	calc_idf(file_path, json_path)