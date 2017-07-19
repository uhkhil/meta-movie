import os, sys, operator, glob
from pathlib import Path

import tmdbsimple as tmdb

# fullpath = "/media/akhil/New Volume/English Movies/"
# fullpath = "/media/akhil/New Volume/Tv & Movie Series/"
# fullpath = "/home/akhil/Git/meta-movie/example/HDD\ 2/"

def print_usage():
	print "usage: python meta-movie.py [/fullpath/to/the/movies/folder/] \n"
	sys.exit()

def is_path(arg):
	my_file = Path(arg)
	if my_file.is_dir():
		return True
	else:
		return False

def prepare_path(fullpath):
	if fullpath[len(fullpath)-1] != "/":
		fullpath = fullpath + "/"
	return fullpath.replace('\ ', ' ')


# Command check
if len(sys.argv) == 1:
	print "meta-movie: Missing operand."
	print_usage()
elif is_path(sys.argv[1]) == False:
	print "meta-movie: Invalid folder path: ", sys.argv[1]
	print_usage()


fullpath = sys.argv[1]
fullpath = prepare_path(fullpath)


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


print color.CYAN + color.BOLD +  "{:50} {:40} {:<10}".format("Folder Name", "Movie Title", "Rating") + color.END


def get_name(fullpath):
	total_count = fullpath.count('/')
	count = 0
	for i in range(len(fullpath)):
		if fullpath[i] == '/':
			count += 1
			if count == total_count-1:
				return fullpath[i+1:]

def formatted(result):
	return "{:40} {:<10}".format((result['title'])[:35], result['vote_average'])

def search_online(movie_name):
	response = search.movie(query=movie_name)
	if len(search.results):
		result = search.results[0]
		identified.append(result)
		print formatted(result)
	else:
		unidentified.append(movie_name)
		print

def print_stats():
	print "\n", "-----"*20, "\n"
	print color.CYAN + color.BOLD + "Unidentified Movies:" + color.END
	for x in unidentified:
		print x
	print color.CYAN + color.BOLD + "\nMovies found:" + color.END , len(identified)
	print


identified = []
unidentified = []

for folder in glob.glob(fullpath+'*/'):

	# Fullpath doesn't work
	folder = get_name(folder)

	print "{:50}".format(folder[:45]),

	if folder.find('(') != -1:
		year = folder[folder.find('(')+1:folder.find(')')]
		movie_name = folder[:folder.find('(')]
		search_online(movie_name)

	elif folder.find('[') != -1:
		movie_name = folder[:folder.find('[')]
		search_online(movie_name)

	elif folder.count('.') >= 3:
		temp = folder.split('.')
		movie_name = ""
		is_result_found = False
		for i in temp:
			if i.isdigit() and int(i) > 1900 and int(i) < 2100:
				year = i
				response = search.movie(query=movie_name)
				if len(search.results):
					result = search.results[0]
					identified.append(result)
					print formatted(result)
					is_result_found = True
					break
			movie_name = movie_name + i + " "

		if is_result_found == False:
			search_online(movie_name)

	elif folder.count(' ') >= 3:
		temp = folder.split(' ')
		movie_name = ""
		is_result_found = False
		for i in temp:
			if i.isdigit() and int(i) > 1900 and int(i) < 2100:
				year = i
				response = search.movie(query=movie_name)
				if len(search.results):
					result = search.results[0]
					identified.append(result)
					print formatted(result)
					is_result_found = True
					break
			movie_name = movie_name + i + " "
		if is_result_found == False:
			search_online(movie_name)

	else:
		search_online(folder)

try:
	identified.sort(key=operator.itemgetter('vote_average'), reverse=True)
except KeyError:
	print

print "\n", "-----"*20, "\n"
print "Sorted List: [Saved to MovieList.txt]\n"
print color.CYAN + color.BOLD +  "{:40} {:<10}".format("Movie Title", "Rating") + color.END
for x in identified:
	print formatted(x)

if len(identified):
	output_file = open(fullpath + 'Movie_list.txt', 'w')
	output_file.write("This list was generated with meta-movie. [https://www.github.com/akhilnareshkumar/meta-movie] \n\n\n")
	output_file.write("{:40} {:<10}\n".format("Movie Title", "Rating"))
	output_file.write("-----------------------------------------------\n")
	for x in identified:
		output_file.write(formatted(x))
		output_file.write("\n")
	output_file.close()

print_stats()
