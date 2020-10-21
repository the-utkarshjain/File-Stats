def search_keywords(keywords_filename,sentences):

	with open(keywords_filename, 'r') as in_file:
		text = in_file.read()
		search_keywords = text.split(",")

	# print(sentences)
	# print(search_keywords)

	sentences_with_keywords=[]

	for sentence in sentences:
		if (any(map(lambda word: word in sentence, search_keywords))):
			sentences_with_keywords.append(sentence)
			if(len(sentences_with_keywords)==1):
				msg = sentence + "\n"
			else:
				msg +=sentence + "\n"

	return sentences_with_keywords, msg