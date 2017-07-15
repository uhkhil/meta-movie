import tmdbsimple as tmdb, os, glob, sys, operator

# To allow special characters
reload(sys).setdefaultencoding("ISO-8859-1")

# Get an API key from http://themoviedb.org
tmdb.API_KEY = 'f76f07b5a2930828c1add5d5ba10c00e'

movie = tmdb.Movies(603)
search = tmdb.Search()

class color:
   CYAN = '\033[96m'
   BOLD = '\033[1m'
   END = '\033[0m'


print color.CYAN + color.BOLD +  "{:50} {:40} {:<10}".format("Folder Name","Movie Title","Rating") + color.END


def getName(fullpath):
	total_count = fullpath.count('/')
	count = 0
	for i in range(len(fullpath)):
		if fullpath[i] == '/':
			count += 1
			if count == total_count-1:
				return fullpath[i+1:]


def formattedInfo(result):
	return "{:40} {:<10}".format((result['title'])[:35], result['vote_average'])


allMovies = []

for folder in glob.glob("example/HDD/*/"):

	# Fullpath doesn't work
	folder = getName(folder)

	print "{:50}".format(folder[:45]),

	if folder.find('(') != -1:
		year = folder[folder.find('(')+1:folder.find(')')]
		movie_name = folder[:folder.find('(')]
		response = search.movie(query=movie_name)
		if len(search.results):
			result = search.results[0]
			allMovies.append(result)
			print formattedInfo(result)
		else:
			print

	elif folder.find('[') != -1:
		movie_name = folder[:folder.find('[')]
		response = search.movie(query=movie_name)
		if len(search.results):
			result = search.results[0]
			allMovies.append(result)
			print formattedInfo(result)
		else:
			print

	elif folder.count('.')>=4:
		temp = folder.split('.')
		movie_name = ""
		isResultPrinted = False
		for i in temp:
			if i.isdigit():
				year = i
				response = search.movie(query=movie_name)
				if len(search.results):
					result = search.results[0]
					allMovies.append(result)
					print formattedInfo(result)
					isResultPrinted = True
					break
			movie_name = movie_name + i + " "
		if isResultPrinted == False:
			print

	else:
		response = search.movie(query=folder)
		if len(search.results):
			result = search.results[0]
			allMovies.append(result)
			print formattedInfo(result)
		else:
			print

try:
	allMovies.sort(key=operator.itemgetter('vote_average'),reverse=True)
except KeyError:
	print


print "\n\nSorted List: [Saved to MovieList.txt]\n"
print color.CYAN + color.BOLD +  "{:40} {:<10}".format("Movie Title","Rating") + color.END
for x in allMovies:
	print formattedInfo(x)

output_file = open('MovieList.txt','w')
for x in allMovies:
	output_file.write(formattedInfo(x))
	output_file.write("\n")
output_file.close()