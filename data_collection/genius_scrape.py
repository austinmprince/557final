import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import time
import numpy as np

# load songs
data = pd.read_csv("data/genius_hip_hop_lyrics.csv")
genius_urls = data["url"]

# if possible, return the artist from the genius website
# otherwise, return False if it cannot be found
def get_artist(url):
	# send the HTTP request to the url to get the webpage html
	req = urllib.request.Request(url, headers={"User-Agent" : "Mozilla/5.0"})

	try:
		with urllib.request.urlopen(req) as response:
			html = str(response.read())
	except urllib.error.HTTPError:
		return False

	# parse the HTML to get the artist name
	try:
		soup = BeautifulSoup(html, "lxml")
		artist = soup.find("a", {"class" : "header_with_cover_art-primary_info-primary_artist"}).text
	except:
		return False
	return artist

# add a column for the artist from genius
data["artist_genius"] = np.nan

i = 0
for url in genius_urls:
	time.sleep(5)
	artist = get_artist(url)
	if artist:
		data.loc[i, "artist_genius"] = artist
		print(artist)

	i += 1

data.to_csv("data/genius_hip_hop_lyrics2.csv")
