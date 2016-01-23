movies = [line.rstrip('\n') for line in open('../data/movies.txt')]

#http://stackoverflow.com/questions/5466451/how-can-i-print-a-literal-characters-in-python-string-and-also-use-format
patterns = [
	"Ask for {{{0}|Movie}} {{Property}}",
	"Ask for the {{{0}|Movie}} {{Property}}",
	"Ask for the {{Property}} of {{{0}|Movie}}",
	"Ask for the {{Property}} for {{{0}|Movie}}",
	"Ask to give me {{Property}} of {{{0}|Movie}}",
	"Ask to give me {{Property}} for {{{0}|Movie}}",
	"Ask to tell me {{Property}} of {{{0}|Movie}}",
	"Ask to tell me {{Property}} for {{{0}|Movie}}",
	"Ask to give me the {{Property}} of {{{0}|Movie}}",
	"Ask to give me the {{Property}} for {{{0}|Movie}}",
	"Ask to tell me the {{Property}} of {{{0}|Movie}}",
	"Ask to tell me the {{Property}} for {{{0}|Movie}}"
]

def utterances():
	for pattern in patterns:
		for movie in movies:
			cleaned = movie
			#some movies
			cleaned = cleaned.replace(":", "")
			cleaned = cleaned.replace(",", "")
			#a space odyssey; kubrick is god
			cleaned = cleaned.replace("0", "zero ")
			cleaned = cleaned.replace("1", "one ")
			cleaned = cleaned.replace("2", "two ")
			yield pattern.format(cleaned)

all_utterances = list(utterances())

with open("../data/utterances.txt", "w") as file:
	for utterance in all_utterances:
		file.write("%s\n" % utterance)

print("wrote " + str(len(all_utterances)) + " utterances")