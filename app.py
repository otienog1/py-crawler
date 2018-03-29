from bs4 import BeautifulSoup
import requests
# from urllib.parse import urlparse
# import time

# Governments that preach peace but endorse war
# Pastors that preach charity but own private jetz
# We will not let exam results decide our fate

class AppCrawler:
	def __init__(self, starting_url, depth):
		self.starting_url = starting_url
		self.depth = depth
		self.current_depth = 0
		self.depth_links = []
		self.pages = []
		self.already_crawled = []

	def crawl(self):
		page = self.get_page_from_link(self.starting_url)

		self.pages.append(page)
		self.depth_links.append(page.links)

		while self.current_depth < self.depth:
			current_links = []
			for link in self.depth_links[self.current_depth]:
				# time.sleep(5)
				if self.already_crawled.count(link) < 1:
					try:
						current_page = self.get_page_from_link(link)

						current_links.extend(current_page.links)

						print(
							"Title: "+current_page.title+
							"\nDescription: "+current_page.description+
							"\nKeyWords: "+current_page.description+
							"\nurl: "+current_page.url+"\n"
						)

						self.already_crawled.append(link)
						self.pages.append(current_page)

					except:
						print("An Error has occurred while trying to get "+ link)
						self.already_crawled.append(link)
				# else:
					# print(link+" Has already been crawled")

			self.current_depth += 1
			# self.depth +=1
			self.depth_links.append(current_links)

	def get_page_from_link(self, url):
			
		try:
			start_page = requests.get(url)
			tree = BeautifulSoup(start_page.text, "html.parser")
			# requests.packages.urllib3

			title = tree.title.text or tree.find('meta', {"property": "og:title"})['content']
			if title is None:
				title = ""

			description = tree.find('meta', {"name": "description"}) or tree.find('meta', {"property": "og:description"})
			if description is not None:
				description = description['content']
			else:
				description = ""

			keywords = tree.find('meta', {"name": "keywords"}) or tree.find('meta', {"property": "og:keywords"})
			if keywords is not None:
				keywords = keywords['content']
			else:
				keywords = ""

			links = tree.find_all("a")

			href = []

			for link in links:
				try:
					link = link['href']

					if link[:] == '#' or link[:1] == '#':
						continue
					elif link[:1] == '/' and link[:2] != '//':
						link = 'https://google.com' + link
					elif link[:2] == '//':
						link = 'http:' + link
					elif link[:6] == 'mailto':
						continue

					href.append(link)
				except:
					print('Href error '+link)
					# print(link)
					continue

			page = Page(title, description, keywords, url, href)

			return page
		except:
			print("unable to connect to "+url)

class Page:
	def __init__(self, title, description, keywords, url, links):
		self.title = title
		self.description = description
		self.keywords = keywords
		self.url = url
		self.links = links

		return

	def __str__(self):
		return ("Title: " + self.title +
				"\nDescription: " +
				self.description + "\nKeyWords: " +
				self.keywords + "\n"
				)

bot = AppCrawler('https://google.com/', 5)
bot.crawl()

# for page in bot.pages:
#     print(page)
