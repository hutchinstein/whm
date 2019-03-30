import bs4 as bs
import urllib.request
import csv
import xml.etree.ElementTree as ET
import os
files = []
blank_file_names = []
episode_num_list = []
sqlString = ''

## Have this start to run off of saved XML
def xml_generator(ep_num_start, ep_num_stop):
    f = open('movie_year.csv')
    csv_f = csv.reader(f)
    key = '49f91ae0'

    for row in csv_f:
        try:
            title = row[0]
            year = row[1]
            episode_num = row[2]
            ep = int(episode_num[-3:])
            title = title.replace(" ", "+")

            if ep_num_start <= ep <= ep_num_stop:
                if year == '':
                    sauce = urllib.request.urlopen('http://www.omdbapi.com/?t=' +
                                                   title + '&plot=full&r=xml&apikey=' + key).read()
                else:
                    sauce = urllib.request.urlopen('http://www.omdbapi.com/?t=' +
                                                   title + '&y=' + year + '&plot=full&r=xml&apikey=' + key).read()
                print(title)
                soup = bs.BeautifulSoup(sauce, 'xml')

                output = str(soup)

                if output == '':
                    print(title, 'has an empty file')
                    blank_file_names.append(title)

                title = title.replace(":", " ")
                title = title.replace(',', '-')
                file_name = title.replace("+", "_")
                f = open('xml/' + file_name + '.xml', 'w+', encoding='utf-8')
                f.write(output)
                f.close()
                files.append(file_name + '.xml')
                episode_num_list.append(episode_num)
            else:
                continue

        except:
            print('Error ', row, ep)
    print(blank_file_names)
    print(files)


def parse(sql):
    # files = ['Number_One_with_a_Bullet.xml', 'The_Pack.xml', 'Congo.xml', 'Psychomania.xml', 'The_Hand.xml', 'K-9.xml']
    # sql = ''
    ep_counter = 0
    for i in files:

        ep_num = episode_num_list[ep_counter]
        ep_counter = ep_counter + 1

        parser = ET.XMLParser(encoding='utf-8')
        tree = ET.parse('xml/' + i, parser=parser)

        root = tree.getroot()

        for movie in root.findall('movie'):

            current_film = []
            final_list = ''
            actors = str(movie.get('actors'))

            title = movie.get('title')
            title = title.replace(',', ' ')
            director = movie.get('director')
            genre = movie.get('genre')
            imdbRating = movie.get('imdbRating')
            rated = movie.get('rated')
            runtime = movie.get('runtime')
            runtime = runtime[:3]
            released = movie.get('released')
            writers = movie.get('writer')
            plot = movie.get('plot')
            plot = plot.replace(',', '')
            poster = movie.get('poster')
            imdbID = movie.get('imdbID')
            awards = movie.get('awards')
            metascore = movie.get('metascore')
            actor_list = actors.split(',')
            genre_list = genre.split(',')
            director_list = director.split(',')
            current_film.append(imdbRating)
            current_film.append(rated)
            current_film.append(runtime)
            current_film.append(released)
            final_list = final_list + title
            if len(director_list) > 2:
                del director_list[2:]
            if len(director_list) < 2:
                director_list.append('')
            for i in director_list:
                print(final_list)
                print(title, 'Director(s):', i)
                final_list = final_list + ',' + i
            current_film_list = ['imdb rating', 'rating', 'run time', 'release date']
            writer_list = writers.split(',')
            if len(writer_list) > 4:
                del writer_list[4:]
            if len(writer_list) < 4:
                for i in (range(0, 4-len(writer_list))):
                    writer_list.append('')
            if len(actor_list) > 4:
                del actor_list[4:]
            if len(actor_list) < 4:
                for i in (range(0, 4-len(actor_list))):
                    actor_list.append('')
            print(len(genre_list))
            if len(genre_list) > 4:
                del genre_list[4:]
            if len(genre_list) < 4:
                for i in range(0, (4-len(genre_list))):
                    genre_list.append('')
            j = 0
            ep_num = ep_num[-3:]
            final_list = final_list + ',' + ep_num
            for i in current_film:
                print(title, ep_num, current_film_list[j], ':', i)
                j = j + 1
                final_list = final_list + ',' + i

            for i in genre_list:
                print(title, 'genre:', i)
                final_list = final_list + ',' + i

            for i in actor_list:
                print(title, 'actor:', i)
                final_list = final_list + ',' + i

            for i in writer_list:
                print(title, 'writer:', i)
                final_list = final_list + ',' + i
            final_list = final_list + ',' + plot + ',' + poster + ',' + imdbID + ',' + awards + ',' + metascore
            final_list = final_list + '\n'
            print('final list', final_list)
            f = open('movies_out.csv', 'a')
            f.write(final_list)
            dir1 = director_list[0]
            if len(director_list) == 2:
                dir2 = director_list[1]
            else:
                dir2 = ''
            gen1 = genre_list[0]
            gen2 = genre_list[1]
            gen3 = genre_list[2]
            gen4 = genre_list[3]
            act1 = actor_list[0]
            act2 = actor_list[1]
            act3 = actor_list[2]
            act4 = actor_list[3]
            wr1 = writer_list[0]
            wr2 = writer_list[1]
            wr3 = writer_list[2]
            wr4 = writer_list[3]
            description = plot
            na = 'No information yet'
            hju = na
            hsa = na
            hsz = na
            hca = na
            hg1 = na
            hg2 = na
            months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
                      'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
            if released == 'N/A':
                released = '0000-00-00'
            else:
                monthSlice = released[3:-5]
                month = months[monthSlice]
                released = released[7:] + "-" + month + "-" + released[:2]
            #description = description.replace('\'', '\'\'')
            if sql == "insert":
                sqlFile = open("sqlinsert.txt", "a")
                sqlString = "INSERT INTO whm (title, dir1, dir2, ep, imdb, imdbID, rating, runtime, date, gen1, gen2, gen3, gen4," \
                            " act1, act2, act3, act4, wr1, wr2, wr3, wr4, description, poster, hju, hsa, hsz, hca, hg1, hg2) " \
                            "VALUES (\"" + title + "\",\"" + dir1 + "\",\"" + dir2 + "\",\"" + ep_num + "\",\"" + imdbRating + "\",\"" + imdbID + "\" ,\"" + rated + "\",\"" + \
                            runtime + "\",\"" + released + "\",\"" + gen1 + "\",\"" + gen2 + "\",\"" + gen3 + "\",\"" + gen4 + "\",\"" + act1 + "\",\"" + \
                            act2 + "\",\"" + act3 + "\",\"" + act4 + "\",\"" + wr1 + "\",\"" + wr2 + "\",\"" + wr3 + "\",\"" + wr4 + "\",\"" + \
                            description + "\",\"" + poster + "\",\"" + hju + "\",\"" + hsa + "\",\"" + hsz + "\",\"" + hca + "\",\"" + hg1 + "\",\"" + \
                            hg2 + "\");\n"
                sqlFile.write(sqlString)
            elif sql == "update":
                # try:
                #     os.remove("sqlupdate.txt")
                # except:
                #     continue
                sqlFileUpdate = open("sqlupdate.txt", "a")
                sqlStringUpdate = "UPDATE whm SET title= \"" + title + "\", dir1= \"" + dir1 + "\", dir2= \"" + dir2 \
                                  + "\", imdb = \"" + imdbRating + "\", rating = \"" + rated + "\", runtime = \"" + runtime +\
                                  "\", date = \"" + released + "\", gen1 = \"" + gen1 + "\", gen2 = \"" + gen2 + "\"," \
                                  "gen3= \"" + gen3 + "\", gen4 = \"" + gen4 + "\", act1 = \"" + act1 + "\",act2 = \"" + \
                                  act2 + "\", act3 = \"" + act3 + "\", act4 = \"" + act4 + \
                                  "\", wr1 = \"" + wr1 + "\", wr2 = \"" + wr2 + "\", wr3 = \"" + wr3 + "\", wr4 = \"" + wr4 + \
                                  "\", description = \"" + description + "\", poster = \"" + poster + \
                                  "\" WHERE ep = " + ep_num + ";"
                # sqlStringUpdate = "UPDATE whm SET imdbID = \"" + imdbID + "\" WHERE ep = " + ep_num + ";"
                sqlFileUpdate.write(sqlStringUpdate)



def main():
    ep_num_start = int(input("Select episode number to start with: "))
    ep_num_stop = int(input("Select episode number to end with: "))
    sql = input("Insert or update?\n")
    sql = sql.lower()
    xml_generator(ep_num_start, ep_num_stop)
    parse(sql)


main()
