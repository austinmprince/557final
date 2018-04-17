# use the last.fm api instead of spotify
from urllib.request import urlopen
from urllib.parse import urlencode
import json
import numpy as np
import os

api_key = os.environ["LASTFM_API_KEY"]

# from the song and artist name, get the information from the last.fm API
def get_song_info(song, artist):
	params = {  "method" : "track.search", "track" : song, "artist" : artist, "api_key" : api_key,
	            "limit" : 10, "format" : "json" }

	url = "http://ws.audioscrobbler.com/2.0/?" + urlencode(params)

	with urlopen(url) as response:
		content = json.load(response)

	tracks = content["results"]["trackmatches"]["track"]
	if len(tracks) > 0:
		top_track = tracks[0]
		name = top_track["name"]
		artist = top_track["artist"]
		listeners = top_track["listeners"]
		info = {"name" : name, "artist" : artist, "listeners" : listeners}
		print("%s by %s" % (song, artist))
		print(info)
		print("")
		return info
	else:
		return False

# read in the song data dng et the number of listens from the last.fm API
def get_song_popularity():
	# load the song and artist data
	f = open("data/genius_hip_hop_lyrics_new_artist.csv", "r")
	content = f.readlines()
	f.close()

	#new_content = [content[0] + ",lastfm_song,lastfm_artist,lastfm_listeners"]
	new_content = []

	success_total = 0
	for row in content:
		row = row.strip()
		line = row.split("\t")
		song = line[3]
		artist = line[4]
		artist_genius = line[10]

		# get data from last.fm
		info = get_song_info(song, artist)

		# search using the artist from genius if nothing was found before
		if not info and (artist != artist_genius):
			info = get_song_info(song, artist_genius)

		if info:
			success_total += 1
			row += "\t%s\t%s\t%s" % (info["name"], info["artist"], info["listeners"])
		else:
			row += "\t\t\t"

		new_content.append(row)

	print(success_total)
	f = open("last_data.tsv", "w")
	f.write('\n'.join(new_content) + '\n')
	f.close()

def get_artist_lastfm(artist_name):
	params = {  "method" : "artist.getinfo", "artist" : artist_name, "api_key" : api_key, 
	            "format" : "json" }

	url = "http://ws.audioscrobbler.com/2.0/?" + urlencode(params)

	with urlopen(url) as response:
		content = json.load(response)

	info = content["artist"]
	name = info["name"]
	listeners = info["stats"]["listeners"]
	plays = info["stats"]["playcount"]
	return {"name" : name, "listeners" : listeners, "plays" : plays}

def get_artist_popularity(filename):
	# read in the tsv file with artist names
	f = open(filename, 'r')
	content = f.readlines()
	f.close()

	name_fixes = {"T.I" : "T.I.", "Lil Wayne" : "Lil' Wayne", "JAY Z" : "JAY-Z", 
	              "Double X Posse" : "Double XX Posse", "demigodz" : "The Demigodz", 
	              "Jeezy" : "Young Jeezy", 
	              "Lil Kim" : "Lil' Kim", "Double P" : "Double P."}

	new_content = [content[0].strip()]

	for line in content[1:]:
		line_data = line.strip().split('\t')
		if len(line_data) >= 11:
			lastfm_artist = line_data[10]

			if lastfm_artist in name_fixes.keys() or "Royce" in lastfm_artist:
				if "Royce" in lastfm_artist:
					lastfm_artist = "Royce da 5'9\""
				else:
					lastfm_artist = name_fixes[lastfm_artist]

				# fix ones where the artist name was incorrect
				info = get_artist_lastfm(lastfm_artist)
				line_data[12] = info["listeners"]
				line_data[13] = info["plays"]

				# fix the song listeners as well
				song_info = get_song_info(line_data[1], lastfm_artist)
				if song_info:
					line_data[11] = song_info["listeners"]

				# fix the lastfm artist name
				line_data[10] = lastfm_artist
				new_line = '\t'.join(line_data)
				new_content.append(new_line)
			else:
				new_content.append(line.strip())

			# new_line = "%s\t%s\t%s" % (line.strip(), info["listeners"], info["plays"])
			# new_content.append(new_line)

		else:
			new_content.append(line.strip())

	return '\n'.join(new_content) + '\n'

# new_data = get_artist_popularity("data/genius_hip_hop_lyrics_lastfm_cleaned.txt")
new_data = get_artist_popularity("data/lyrics_lastfm_artist_info.txt")
f = open("data/lyrics_lastfm_artist_info2.txt", 'w')
f.write(new_data)
f.close()

