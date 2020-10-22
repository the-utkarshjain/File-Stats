# Function to search for sentences with keywords
def search_keywords(keywords_filename, sentences, originalsentences):

	line = 1
	msg = ""

	text = open(keywords_filename, "r").read()
	search_keywords = text.split(",")

	for i in range(len(sentences)):
		if (any(map(lambda word: word.lower() in sentences[i], search_keywords))):
			msg += str(line) + ". " + originalsentences[i].strip() + ".\n"
			line += 1

	return msg