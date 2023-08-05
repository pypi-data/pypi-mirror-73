from urllib.request import urlopen
import youtube_dl

class Video:
	def __init__(self, search):
		self.query = search
		url = "https://www.youtube.com/results?search_query=" + self.query.replace(' ','+')
		html = urlopen(url)
		nonecode = html.read()
		code = str(nonecode)
		f = code.find("watch?v")
		urllist = []
		urllist.append(code[f])
		cnt = 1
		while True:
			char = code[f+cnt]
			if char == '"':
				break
			else:
				urllist.append(char)
				cnt += 1
		url = "https://www.youtube.com/" + "".join(urllist)
		opts = {}
		with youtube_dl.YoutubeDL(opts) as ytdl:
			data = ytdl.extract_info(url, download=False)
		self.url = url
		self.data = data
	def search(self):
		if self.url.endswith("'b'<!doctype html><"):
			return None
		else:
			return self.url
	def title(self):
		data = self.data
		title = data["title"]
		return title
	def channel_url(self):
		data = self.data
		url = data["channel_url"]
		return url
	def thumbnail(self):
		data = self.data
		thumb = data["thumbnail"]
		return thumb
	def duration(self):
		data = self.data
		duration = data["duration"]
		return duration
	def view_count(self):
		data = self.data
		count = data["view_count"]
		return count
	def like_count(self):
		data = self.data
		count = data["like_count"]
		return count
	def dislike_count(self):
		data = self.data
		count = data["dislike_count"]
		return count
	def average_rating(self):
		data = self.data
		rating = data["average_rating"]
		return rating
	def channel_name(self):
		data = self.data
		name = data["uploader"]
		return name
class ExtractInfo:
	def __init__(self,url):
		opts = {}
		with youtube_dl.YoutubeDL(opts) as ytdl:
			self.data = ytdl.extract_info(url, download=False)
			self.url = url
	def title(self):
		data = self.data
		title = data["title"]
		return title
	def channel_url(self):
		data = self.data
		url = data["channel_url"]
		return url
	def thumbnail(self):
		data = self.data
		thumb = data["thumbnail"]
		return thumb
	def duration(self):
		data = self.data
		duration = data["duration"]
		return duration
	def view_count(self):
		data = self.data
		count = data["view_count"]
		return count
	def like_count(self):
		data = self.data
		count = data["like_count"]
		return count
	def dislike_count(self):
		data = self.data
		count = data["dislike_count"]
		return count
	def average_rating(self):
		data = self.data
		rating = data["average_rating"]
		return rating
	def channel_name(self):
		data = self.data
		name = data["uploader"]
		return name