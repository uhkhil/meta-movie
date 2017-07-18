import tmdbsimple as tmdb, os, glob, sys, operator

# fullpath = "/media/akhil/New Volume/English Movies/"
# fullpath = "/media/akhil/New Volume/Tv & Movie Series/"
# fullpath = "/home/akhil/Git/meta-movie/example/HDD\ 2/"

def printUsage():
	print "usage: python meta-movie.py [/fullpath/to/the/movies/folder/] \n"
	sys.exit()

def isPath(arg):
	return True

def fullpathWithSpaces(fullpath):
	if fullpath[len(fullpath)-1] != "/":
		fullpath = fullpath + "/"
	return fullpath.replace('\ ',' ')



# Command check

if len(sys.argv) == 1:
	print "meta-movie: Missing operand."
	printUsage()
elif isPath(sys.argv[1]) == False:
	print "meta-movie: Invalid folder path: ",sys.argv[1]
	printUsage()




fullpath = sys.argv[1]

fullpath = fullpathWithSpaces(fullpath)



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

def searchOnline(movie_name):
	response = search.movie(query=movie_name)
	if len(search.results):
		result = search.results[0]
		allMovies.append(result)
		print formattedInfo(result)
	else:
		unidentified.append(movie_name)
		print

def linuxFullPath(fullpath):
	return fullpath.replace(' ','\ ')

def printStatistics():
	print "\n","-----" * 20,"\n"
	print color.CYAN + color.BOLD + "Unidentified Movies:" + color.END
	for x in unidentified:
		print x
	print color.CYAN + color.BOLD + "\nMovies found:" + color.END , len(allMovies)
	print
	# print "Unidentified Movies", len(glob.glob(fullpath+'*/'))
	# return


allMovies = []
unidentified = []

for folder in glob.glob(fullpath+'*/'):

	# Fullpath doesn't work
	folder = getName(folder)

	print "{:50}".format(folder[:45]),

	if folder.find('(') != -1:
		year = folder[folder.find('(')+1:folder.find(')')]
		movie_name = folder[:folder.find('(')]
		searchOnline(movie_name)

	elif folder.find('[') != -1:
		movie_name = folder[:folder.find('[')]
		searchOnline(movie_name)

	elif folder.count('.')>=3:
		temp = folder.split('.')
		movie_name = ""
		isResultPrinted = False
		for i in temp:
			if i.isdigit() and int(i)>1900 and int(i)<2100:
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
			searchOnline(movie_name)

	elif folder.count(' ')>=3:
		temp = folder.split(' ')
		movie_name = ""
		isResultPrinted = False
		for i in temp:
			if i.isdigit() and int(i)>1900 and int(i)<2100:
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
			searchOnline(movie_name)

	else:
		searchOnline(folder)

try:
	allMovies.sort(key=operator.itemgetter('vote_average'),reverse=True)
except KeyError:
	print

print "\n","-----" * 20,"\n"
print "Sorted List: [Saved to MovieList.txt]\n"
print color.CYAN + color.BOLD +  "{:40} {:<10}".format("Movie Title","Rating") + color.END
for x in allMovies:
	print formattedInfo(x)

if len(allMovies):
	output_file = open(fullpath+'Movie_list.txt','w')
	output_file.write("This list was generated with meta-movie. [https://www.github.com/akhilnareshkumar/meta-movie] \n\n\n")
	output_file.write("{:40} {:<10}\n".format("Movie Title","Rating"))
	output_file.write("-----------------------------------------------\n")
	for x in allMovies:
		output_file.write(formattedInfo(x))
		output_file.write("\n")
	output_file.close()

printStatistics()
