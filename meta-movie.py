import os
import sys
import glob
import operator

import pathlib
import tmdbsimple as tmdb

# To allow special characters
reload(sys).setdefaultencoding("ISO-8859-1")

def check_commandline():
    if len(sys.argv) == 1:
        print "meta-movie: Missing operand."
        print_usage()
    elif is_path(sys.argv[1]) == False:
        print "meta-movie: Invalid folder path: ", sys.argv[1]
        print_usage()
    else:
        return True

def print_usage():
    print "usage: python meta-movie.py [path/to/the/movies/folder/] \n"
    sys.exit()

def is_path(path):
    my_file = pathlib.Path(path)
    if my_file.is_dir():
        return True
    else:
        return False

def prepare_path(path):
    if path[len(path)-1] != "/":
        path = path + "/"
    return path.replace('\ ', ' ')

def get_name(path):
    if path[len(path)-1] == '/':
        total_count = path.count('/')
        count = 0
        for i in range(len(path)):
            if path[i] == '/':
                count += 1
                if count == total_count-1:
                    return path[i+1:]
    else:
        total_count = path.count('/')
        count = 0
        for i in range(len(path)):
            if path[i] == '/':
                count += 1
                if count == total_count:
                    temp = path[i+1:]
        for i in range(len(temp)-1,0,-1):
            if temp[i] == '.':
                return temp[:i]

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




def search_movies(fullpath):
    extensions = ['*/', '*.mp4', '*.avi', '*.mkv']
    for ext in extensions:
        for file in glob.glob(fullpath+ext):
            file = get_name(file)
            print "{:50}".format(file[:45]),

            if file.find('(') != -1:
                year = file[file.find('(')+1:file.find(')')]
                movie_name = file[:file.find('(')]
                search_online(movie_name)

            elif file.find('[') != -1:
                movie_name = file[:file.find('[')]
                search_online(movie_name)

            elif file.count('.') >= 3:
                temp = file.split('.')
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

            elif file.count(' ') >= 3:
                temp = file.split(' ')
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
                search_online(file)



def print_sorted_list():
    try:
        identified.sort(key=operator.itemgetter('vote_average'), reverse=True)
    except KeyError:
        print

    print "\n", "-----"*20, "\n"
    print "Sorted List: [Saved to MovieList.txt]\n"
    print color.CYAN + color.BOLD +  "{:40} {:<10}".format("Movie Title", "Rating") + color.END
    for x in identified:
        print formatted(x)

def write_result_to_file():
    if len(identified):
        output_file = open(fullpath + 'Movie_list.txt', 'w')
        output_file.write("This list was generated with meta-movie. [https://www.github.com/akhilnareshkumar/meta-movie] \n\n\n")
        output_file.write("{:40} {:<10}\n".format("Movie Title", "Rating"))
        output_file.write("-----------------------------------------------\n")
        for x in identified:
            output_file.write(formatted(x))
            output_file.write("\n")
        output_file.close()

def print_stats():
    print "\n", "-----"*20, "\n"
    print color.CYAN + color.BOLD + "Unidentified Movies:" + color.END
    for x in unidentified:
        print x
    print color.CYAN + color.BOLD + "\nMovies found:" + color.END, len(identified)
    print

class color:
   CYAN = '\033[96m'
   BOLD = '\033[1m'
   END = '\033[0m'



check_commandline()

fullpath = prepare_path(sys.argv[1])



# Get an API key from http://themoviedb.org
tmdb.API_KEY = 'f76f07b5a2930828c1add5d5ba10c00e'
movie = tmdb.Movies(603)
search = tmdb.Search()

print color.CYAN + color.BOLD +  "{:50} {:40} {:<10}".format("Folder Name", "Movie Title", "Rating") + color.END

identified = []
unidentified = []

try:
    search_movies(fullpath)
    print_sorted_list()
    write_result_to_file()
    print_stats()
except KeyboardInterrupt:
    pass
