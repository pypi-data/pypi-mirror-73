from urllib.request import urlopen
import urllib.request
import re
import pkgutil

filter = pkgutil.get_data(__package__, 'safesearch.txt').decode('utf-8').replace("\r","").split("\n")

class BlockedWordError(Exception):
	"""A blocked word has been found in the video! Don't use safesearch filter if you want to ignore this error!"""

class Video:
	def __init__(self, search, **kwargs):
		self.safe = False
		if "safesearch" in kwargs:
			self.safe = kwargs["safesearch"]
		self.query = search
		self.url = None
		self.data = None
		self.url = None
		self.code = None
		self.id = None
		self.nsfw = False
		self.video_title = None
		self.video_description = None
	def search(self):
		if not self.url:
			url = "https://www.youtube.com/results?search_query=" + self.query.replace(' ','+')
			html = urlopen(url)
			nonecode = html.read()
			code = str(nonecode)
			f = code.find("watch?v=")
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
			self.url = url
		if not self.id:
			x,y = self.url.split("watch?v=")
			self.id = y
		if not self.code:
			html = urlopen(self.url)
			pagenonecode = html.read()
			code = str(pagenonecode)
			self.code = code
		if self.safe:
			global filter
			if not self.video_title:
				titlepattern = '<meta itemprop="name" content="(.*?)">'
				titlee = re.search(titlepattern, self.code).group(1)
				self.video_title = titlee
			if not self.video_description:
				descpattern = '"shortDescription":"(.*?)","'
				description = str(re.search(descpattern, self.code).group(1))
				description = description.encode().decode('unicode_escape')
				self.video_description = description
			for word in filter:
				word = word.lower()
				titlee = self.video_title.lower()
				desc = self.video_description.lower()
				query = self.query.lower()
				if word not in query and word not in titlee and word not in desc:
					self.nsfw = False
				else:
					self.nsfw = True
					break
		if self.safe:
			if self.nsfw:
				Error = BlockedWordError("A blocked word detected in the result video! Don't use safesearch to ignore this error!")
				raise Error
			else:
				if self.url != None and "watch?v=" in self.url:
					return self.url
				else:
					return None
		else:
			return self.url
	def title(self):
		if not self.url:
			url = "https://www.youtube.com/results?search_query=" + self.query.replace(' ','+')
			html = urlopen(url)
			nonecode = html.read()
			code = str(nonecode)
			f = code.find("watch?v=")
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
			self.url = url
		if not self.id:
			x,y = self.url.split("watch?v=")
			self.id = y
		if not self.code:
			html = urlopen(self.url)
			pagenonecode = html.read()
			code = str(pagenonecode)
			self.code = code
		if not self.video_title:
			titlepattern = '<meta itemprop="name" content="(.*?)">'
			title = re.search(titlepattern, self.code).group(1)
			self.video_title = title
		if not self.video_description:
			descpattern = '"shortDescription":"(.*?)","'
			description = str(re.search(descpattern, self.code).group(1))
			description = description.encode().decode('unicode_escape')
			self.video_description = description
		if self.safe:
			global filter
			for word in filter:
				if word.lower() not in self.video_title.lower() and word.lower() not in self.video_description.lower() and word.lower() not in self.query.lower():
					self.nsfw = False
				else:
					self.nsfw = True
					break
		if self.safe:
			if self.nsfw:
				Error = BlockedWordError("A blocked word detected in the result video! Don't use safesearch to ignore this error!")
				raise Error
			else:
				if self.video_title != None:
					return self.video_title
		else:
			return self.video_title
	def channel_url(self):
		if not self.url:
			url = "https://www.youtube.com/results?search_query=" + self.query.replace(' ','+')
			html = urlopen(url)
			nonecode = html.read()
			code = str(nonecode)
			f = code.find("watch?v=")
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
			self.url = url
		if not self.id:
			x,y = self.url.split("watch?v=")
			self.id = y
		if not self.code:
			html = urlopen(self.url)
			pagenonecode = html.read()
			code = str(pagenonecode)
			self.code = code
		if not self.video_title:
			titlepattern = '<meta itemprop="name" content="(.*?)">'
			title = re.search(titlepattern, self.code).group(1)
			self.video_title = title
		if not self.video_description:
			descpattern = '"shortDescription":"(.*?)","'
			description = str(re.search(descpattern, self.code).group(1))
			description = description.encode().decode('unicode_escape')
			self.video_description = description
		channelurlpattern = '{"url":"/channel/(.*?)",'
		channel_url = re.search(channelurlpattern, self.code).group(1)
		channel_url = "https://www.youtube.com/channel/" + channel_url
		return url
	def thumbnail_url(self):
		if not self.url:
			url = "https://www.youtube.com/results?search_query=" + self.query.replace(' ','+')
			html = urlopen(url)
			nonecode = html.read()
			code = str(nonecode)
			f = code.find("watch?v=")
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
			self.url = url
		if not self.code:
			html = urlopen(self.url)
			pagenonecode = html.read()
			code = str(pagenonecode)
			self.code = code
		if not self.id:
			x,y = self.url.split("watch?v=")
			self.id = y
		if not self.video_title:
			titlepattern = '<meta itemprop="name" content="(.*?)">'
			title = re.search(titlepattern, self.code).group(1)
			self.video_title = title
		if not self.video_description:
			descpattern = '"shortDescription":"(.*?)","'
			description = str(re.search(descpattern, self.code).group(1))
			description = description.encode().decode('unicode_escape')
			self.video_description = description
		x,keywords = self.url.split("watch?v=")
		thumb = "http://i.ytimg.com/vi/" + keywords + "/0.jpg"
		return thumb
	def thumbnail_save(self, filename=None):
		if not self.url:
			url = "https://www.youtube.com/results?search_query=" + self.query.replace(' ','+')
			html = urlopen(url)
			nonecode = html.read()
			code = str(nonecode)
			f = code.find("watch?v=")
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
			self.url = url
		if not self.id:
			x,y = self.url.split("watch?v=")
			self.id = y
		if not self.code:
			html = urlopen(self.url)
			pagenonecode = html.read()
			code = str(pagenonecode)
			self.code = code
		if not self.video_title:
			titlepattern = '<meta itemprop="name" content="(.*?)">'
			title = re.search(titlepattern, self.code).group(1)
			self.video_title = title
		if not self.video_description:
			descpattern = '"shortDescription":"(.*?)","'
			description = str(re.search(descpattern, self.code).group(1))
			description = description.encode().decode('unicode_escape')
			self.video_description = description
		if not filename:
			titlepattern = '<meta itemprop="name" content="(.*?)">'
			title = re.search(titlepattern, self.code).group(1)
			filename = title + ".jpg"
		x,keywords = self.url.split("watch?v=")
		thumb = "http://i.ytimg.com/vi/" + keywords + "/0.jpg"
		try:
			urllib.request.urlretrieve(thumb, filename)
		except IsADirectoryError:
			titlepattern = '<meta itemprop="name" content="(.*?)">'
			title = re.search(titlepattern, self.code).group(1)
			if filename.endswith("/"):
				filename = filename + title + ".jpg"
			else:
				filename = filename + "/" + title + ".jpg"
			urllib.request.urlretrieve(thumb, filename)
	def duration(self):
		if not self.url:
			url = "https://www.youtube.com/results?search_query=" + self.query.replace(' ','+')
			html = urlopen(url)
			nonecode = html.read()
			code = str(nonecode)
			f = code.find("watch?v=")
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
			self.url = url
		if not self.id:
			x,y = self.url.split("watch?v=")
			self.id = y
		if not self.code:
			html = urlopen(self.url)
			pagenonecode = html.read()
			code = str(pagenonecode)
			self.code = code
		if not self.video_title:
			titlepattern = '<meta itemprop="name" content="(.*?)">'
			title = re.search(titlepattern, self.code).group(1)
			self.video_title = title
		if not self.video_description:
			descpattern = '"shortDescription":"(.*?)","'
			description = str(re.search(descpattern, self.code).group(1))
			description = description.encode().decode('unicode_escape')
			self.video_description = description
		durationpattern = '<meta itemprop="duration" content="(.*?)">'
		duration = re.search(durationpattern, self.code).group(1)
		mp = "PT(.*?)M"
		minutes = re.search(mp, duration).group(1)
		sp = f"PT{minutes}M(.*?)S"
		seconds = re.search(sp, duration).group(1)
		duration = []
		duration.append(str(seconds))
		duration.append(str(minutes))
		duration.append("0")
		if int(minutes) > 60:
			hours, mins = divmod(int(minutes), 60)
			duration[1] = mins
			duration[2] = hours
		if len(str(duration[0])) < 2:
			duration[0] = f"0{duration[0]}"
		if len(str(duration[1])) < 2:
			duration[1] = f"0{duration[1]}"
		if len(str(duration[2])) < 2:
			duration[2] = f"0{duration[2]}"
		duration = f"{duration[2]}:{duration[1]}:{duration[0]}"
		return duration
	def view_count(self):
		if not self.url:
			url = "https://www.youtube.com/results?search_query=" + self.query.replace(' ','+')
			html = urlopen(url)
			nonecode = html.read()
			code = str(nonecode)
			f = code.find("watch?v=")
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
			self.url = url
		if not self.id:
			x,y = self.url.split("watch?v=")
			self.id = y
		if not self.code:
			html = urlopen(self.url)
			pagenonecode = html.read()
			code = str(pagenonecode)
			self.code = code
		if not self.video_title:
			titlepattern = '<meta itemprop="name" content="(.*?)">'
			title = re.search(titlepattern, self.code).group(1)
			self.video_title = title
		if not self.video_description:
			descpattern = '"shortDescription":"(.*?)","'
			description = str(re.search(descpattern, self.code).group(1))
			description = description.encode().decode('unicode_escape')
			self.video_description = description
		viewspattern = '{"viewCount":{"simpleText":"(.*?) views"}'
		views = re.search(viewspattern, self.code).group(1)
		return views
	def like_count(self):
		if not self.url:
			url = "https://www.youtube.com/results?search_query=" + self.query.replace(' ','+')
			html = urlopen(url)
			nonecode = html.read()
			code = str(nonecode)
			f = code.find("watch?v=")
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
			self.url = url
		if not self.id:
			x,y = self.url.split("watch?v=")
			self.id = y
		if not self.code:
			html = urlopen(self.url)
			pagenonecode = html.read()
			code = str(pagenonecode)
			self.code = code
		if not self.video_title:
			titlepattern = '<meta itemprop="name" content="(.*?)">'
			title = re.search(titlepattern, self.code).group(1)
			self.video_title = title
		if not self.video_description:
			descpattern = '"shortDescription":"(.*?)","'
			description = str(re.search(descpattern, self.code).group(1))
			description = description.encode().decode('unicode_escape')
			self.video_description = description
		likepattern = '{"label":"(.*?) likes"}}'
		likes = re.search(likepattern, self.code).group(1)
		return likes
	def dislike_count(self):
		if not self.url:
			url = "https://www.youtube.com/results?search_query=" + self.query.replace(' ','+')
			html = urlopen(url)
			nonecode = html.read()
			code = str(nonecode)
			f = code.find("watch?v=")
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
			self.url = url
		if not self.id:
			x,y = self.url.split("watch?v=")
			self.id = y
		if not self.code:
			html = urlopen(self.url)
			pagenonecode = html.read()
			code = str(pagenonecode)
			self.code = code
		if not self.video_title:
			titlepattern = '<meta itemprop="name" content="(.*?)">'
			title = re.search(titlepattern, self.code).group(1)
			self.video_title = title
		if not self.video_description:
			descpattern = '"shortDescription":"(.*?)","'
			description = str(re.search(descpattern, self.code).group(1))
			description = description.encode().decode('unicode_escape')
			self.video_description = description
		dislikepattern = '{"accessibility":{"accessibilityData":{"label":"(.*?) dislikes"}}'
		dislikes = re.search(dislikepattern, self.code)
		dislikes = dislikes.group(1).split()
		dislikes = dislikes[len(dislikes)-1]
		dislikes= dislikes.split('"')
		dislikes = dislikes[len(dislikes)-1]
		return dislikes
	def average_rating(self):
		if not self.url:
			url = "https://www.youtube.com/results?search_query=" + self.query.replace(' ','+')
			html = urlopen(url)
			nonecode = html.read()
			code = str(nonecode)
			f = code.find("watch?v=")
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
			self.url = url
		if not self.id:
			x,y = self.url.split("watch?v=")
			self.id = y
		if not self.code:
			html = urlopen(self.url)
			pagenonecode = html.read()
			code = str(pagenonecode)
			self.code = code
		if not self.video_title:
			titlepattern = '<meta itemprop="name" content="(.*?)">'
			title = re.search(titlepattern, self.code).group(1)
			self.video_title = title
		if not self.video_description:
			descpattern = '"shortDescription":"(.*?)","'
			description = str(re.search(descpattern, self.code).group(1))
			description = description.encode().decode('unicode_escape')
			self.video_description = description
		likepattern = '{"label":"(.*?) likes"}}'
		likes = re.search(likepattern, self.code).group(1)
		dislikepattern = '{"accessibility":{"accessibilityData":{"label":"(.*?) dislikes"}}'
		dislikes = re.search(dislikepattern, self.code)
		dislikes = dislikes.group(1).split()
		dislikes = dislikes[len(dislikes)-1]
		dislikes= dislikes.split('"')
		dislikes = dislikes[len(dislikes)-1]
		a = likes.split(",")
		a = likes.split(",")
		a = "".join(a)
		b = dislikes.split(",")
		b = "".join(b)
		likes = a
		dislikes = b
		x = float(likes) / 5
		y = float(dislikes) / x
		rating = 5 - y
		return rating
	def channel_name(self):
		if not self.url:
			url = "https://www.youtube.com/results?search_query=" + self.query.replace(' ','+')
			html = urlopen(url)
			nonecode = html.read()
			code = str(nonecode)
			f = code.find("watch?v=")
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
			self.url = url
		if not self.id:
			x,y = self.url.split("watch?v=")
			self.id = y
		if not self.code:
			html = urlopen(self.url)
			pagenonecode = html.read()
			code = str(pagenonecode)
			self.code = code
		if not self.video_title:
			titlepattern = '<meta itemprop="name" content="(.*?)">'
			title = re.search(titlepattern, self.code).group(1)
			self.video_title = title
		if not self.video_description:
			descpattern = '"shortDescription":"(.*?)","'
			description = str(re.search(descpattern, self.code).group(1))
			description = description.encode().decode('unicode_escape')
			self.video_description = description
		channelnamepattern = '<link itemprop="name" content="(.*?)">'
		channel_name = re.search(channelnamepattern, self.code).group(1)
		return channel_name
	def description(self):
		if not self.url:
			url = "https://www.youtube.com/results?search_query=" + self.query.replace(' ','+')
			html = urlopen(url)
			nonecode = html.read()
			code = str(nonecode)
			f = code.find("watch?v=")
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
			self.url = url
		if not self.id:
			x,y = self.url.split("watch?v=")
			self.id = y
		if not self.code:
			html = urlopen(self.url)
			pagenonecode = html.read()
			code = str(pagenonecode)
			self.code = code
		if not self.video_title:
			titlepattern = '<meta itemprop="name" content="(.*?)">'
			title = re.search(titlepattern, self.code).group(1)
			self.video_title = title
		if not self.video_description:
			descpattern = '"shortDescription":"(.*?)","'
			description = str(re.search(descpattern, self.code).group(1))
			description = description.encode().decode('unicode_escape')
			self.video_description = description
		if self.safe:
			global filter
			for word in filter:
				if word.lower() not in self.video_title.lower() and word.lower() not in self.video_description.lower() and word.lower() not in self.query.lower():
					self.nsfw = False
				else:
					self.nsfw = True
					break
		if self.safe:
			if self.nsfw:
				Error = BlockedWordError("A blocked word detected in the result video! Don't use safesearch to ignore this error!")
				raise Error
			else:
				if self.video_description != None:
					return self.video_description
		else:
			return self.video_description
class ExtractInfo:
	def __init__(self,url):
		if url.startswith("https://youtu.be"):
			x,y = url.split("https://youtu.be/")
			url = "https://www.youtube.com/watch?v=" + y
		self.url = url
		html = urlopen(url)
		nonecode = html.read()
		code = str(nonecode)
		self.code = code
	def title(self):
		titlepattern = '<meta itemprop="name" content="(.*?)">'
		title = re.search(titlepattern, self.code).group(1)
		return title
	def channel_url(self):
		channelurlpattern = '{"url":"/channel/(.*?)",'
		channel_url = re.search(channelurlpattern, self.code).group(1)
		channel_url = "https://www.youtube.com/channel/" + channel_url
		return url
	def thumbnail_url(self):
		x,keywords = self.url.split("watch?v=")
		thumb = "http://i.ytimg.com/vi/" + keywords + "/0.jpg"
		return thumb
	def thumbnail_save(self, filename=None):
		if not filename:
			titlepattern = '<meta itemprop="name" content="(.*?)">'
			title = re.search(titlepattern, self.code).group(1)
			filename = title + ".jpg"
		x,keywords = self.url.split("watch?v=")
		thumb = "http://i.ytimg.com/vi/" + keywords + "/0.jpg"
		try:
			urllib.request.urlretrieve(thumb, filename)
		except IsADirectoryError:
			titlepattern = '<meta itemprop="name" content="(.*?)">'
			title = re.search(titlepattern, self.code).group(1)
			if filename.endswith("/"):
				filename = filename + title + ".jpg"
			else:
				filename = filename + "/" + title + ".jpg"
			urllib.request.urlretrieve(thumb, filename)
	def duration(self):
		durationpattern = '<meta itemprop="duration" content="(.*?)">'
		duration = re.search(durationpattern, self.code).group(1)
		mp = "PT(.*?)M"
		minutes = re.search(mp, duration).group(1)
		sp = f"PT{minutes}M(.*?)S"
		seconds = re.search(sp, duration).group(1)
		duration = []
		duration.append(str(seconds))
		duration.append(str(minutes))
		duration.append("0")
		if int(minutes) > 60:
			hours, mins = divmod(int(minutes), 60)
			duration[1] = mins
			duration[2] = hours
		if len(str(duration[0])) < 2:
			duration[0] = f"0{duration[0]}"
		if len(str(duration[1])) < 2:
			duration[1] = f"0{duration[1]}"
		if len(str(duration[2])) < 2:
			duration[2] = f"0{duration[2]}"
		duration = f"{duration[2]}:{duration[1]}:{duration[0]}"
		return duration
	def view_count(self):
		viewspattern = '{"viewCount":{"simpleText":"(.*?) views"}'
		views = re.search(viewspattern, self.code).group(1)
		return views
	def like_count(self):
		likepattern = '{"label":"(.*?) likes"}}'
		likes = re.search(likepattern, self.code).group(1)
		return likes
	def dislike_count(self):
		dislikepattern = '{"accessibility":{"accessibilityData":{"label":"(.*?) dislikes"}}'
		dislikes = re.search(dislikepattern, self.code)
		dislikes = dislikes.group(1).split()
		dislikes = dislikes[len(dislikes)-1]
		dislikes= dislikes.split('"')
		dislikes = dislikes[len(dislikes)-1]
		return dislikes
	def average_rating(self):
		likepattern = '{"label":"(.*?) likes"}}'
		likes = re.search(likepattern, self.code).group(1)
		dislikepattern = '{"accessibility":{"accessibilityData":{"label":"(.*?) dislikes"}}'
		dislikes = re.search(dislikepattern, self.code)
		dislikes = dislikes.group(1).split()
		dislikes = dislikes[len(dislikes)-1]
		dislikes= dislikes.split('"')
		dislikes = dislikes[len(dislikes)-1]
		a = likes.split(",")
		a = "".join(a)
		b = dislikes.split(",")
		b = "".join(b)
		likes = a
		dislikes = b
		x = float(likes) / 5
		y = float(dislikes) / x
		rating = 5 - y
		return rating
	def channel_name(self):
		channelnamepattern = '<link itemprop="name" content="(.*?)">'
		channel_name = re.search(channelnamepattern, self.code).group(1)
		return channel_name
	def description(self):
		descpattern = '"shortDescription":"(.*?)","'
		description = str(re.search(descpattern, self.code).group(1))
		description = description.encode().decode('unicode_escape')
		description = str(description).replace("\\n","\n")
		return description