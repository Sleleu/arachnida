#!/bin/python3
import requests
import argparse
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import time
import signal

RED = "\033[0;31m"
BLUE = "\033[0;34m"
PURPLE = "\033[0;35m"
CYAN = "\033[0;36m"
LIGHT_RED = "\033[1;31m"
LIGHT_GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
LIGHT_BLUE = "\033[1;34m"
LIGHT_PURPLE = "\033[1;35m"
LIGHT_CYAN = "\033[1;36m"
LIGHT_GREEN = "\033[1;32m"
BOLD = "\033[1m"
END = "\033[0m"

ascii_header = """
  ██████  ██▓███   ██▓▓█████▄ ▓█████  ██▀███  
▒██    ▒ ▓██░  ██▒▓██▒▒██▀ ██▌▓█   ▀ ▓██ ▒ ██▒
░ ▓██▄   ▓██░ ██▓▒▒██▒░██   █▌▒███   ▓██ ░▄█ ▒
  ▒   ██▒▒██▄█▓▒ ▒░██░░▓█▄   ▌▒▓█  ▄ ▒██▀▀█▄  
▒██████▒▒▒██▒ ░  ░░██░░▒████▓ ░▒████▒░██▓ ▒██▒
▒ ▒▓▒ ▒ ░▒▓▒░ ░  ░░▓   ▒▒▓  ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░
░ ░▒  ░ ░░▒ ░      ▒ ░ ░ ▒  ▒  ░ ░  ░  ░▒ ░ ▒░
░  ░  ░  ░░        ▒ ░ ░ ░  ░    ░     ░░   ░ 
      ░            ░     ░       ░  ░   ░     
                       ░                      
			Created by : https://github.com/Sleleu
"""

g_downloaded_files = set()
g_img_captured = 0

def getResponse(url: str):
	try:
		response = requests.get(url)
		return (response)
	except:
		print("Error: impossible to get a response from url")
		exit(1)

def getImgSrc(images, url):
	img_src = []
	for image in images:
		src = image.get('src')
		img_src.append(requests.compat.urljoin(url, src)) # in case of non absolute image url in htmldata
	return(img_src)

def isValidExtension(img_response): # check for mime type of the content
	valid_mime_types = ["image/jpg", "image/jpeg", "image/png", "image/bmp", "image/gif"]
	content_type = img_response.headers.get('content-type')
	if content_type in valid_mime_types:
		return (True)
	return (False)

def isImageElement(img_path): # check for extension of the image path
	valid_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif"]
	for extension in valid_extensions:
		if img_path.endswith(extension):
			return (True)
	return (False)

def displayStatImage(image_url: str, img_content: bytes, img_name=None):
	if img_name is not None:
		print(f"{YELLOW}|- {img_name} -|{LIGHT_CYAN} Already downloaded{END}")
	else:
		img_size = len(img_content)
		print(f"{LIGHT_CYAN}|- Download ", end="")
		print(f"{YELLOW}{(img_size / 1000):.2f} kb -| ", end="")
		print(f"{LIGHT_GREEN}{image_url}{END}")

def downloadImage(image_url, path):
	global g_img_captured
	if image_url in g_downloaded_files: # check cache
		return
	img_response = requests.head(image_url)
	if isValidExtension(img_response):
		img_response = requests.get(image_url)
		if (img_response.status_code != 200):
			print(f"Cannot download {image_url}")
			return
		img_content = img_response.content
		img_name = os.path.basename(urlparse(image_url).path)  # To avoid url params
		img_path = os.path.join(path, img_name)
		if not isImageElement(img_path) or os.path.isdir(img_path):
			return
		if os.path.exists(img_path): # If image is already downloaded
			displayStatImage(image_url, img_content, img_name)
			g_downloaded_files.add(image_url)
			return
		with open(img_path, 'wb') as img_file:  # write in binary the content of the image
			img_file.write(img_content)
		displayStatImage(image_url, img_content)
		g_downloaded_files.add(image_url)
		g_img_captured += 1 # different variable because cache contain urls of precedent images captured

def spider(url: str, path: str, depth_level: int):
	if (depth_level == 0):
		return
	response = getResponse(url) # get response object from url
	html_data = response.text
	soup = BeautifulSoup(html_data, 'html.parser')
	images =  soup.find_all('img')
	img_src = getImgSrc(images, url) # get url of each image
	for image in img_src:
		downloadImage(image, path)

	links = soup.find_all('a')
	for link in links:
		href = link.get('href')
		if href:
			if href.startswith("/"):
				href = urljoin(url, href)
			if href.startswith("#"):
				continue
			if urlparse(href).netloc == urlparse(url).netloc: # avoid scraping another domain name
				spider(href, path, depth_level - 1)

def parse_arguments():
	desc = "The spider program allow you to extract all the images from a website, \
			recursively, by providing a url as a parameter."
	parser = argparse.ArgumentParser(description=desc)
	parser.add_argument("-p", "--path", help="indicates the path where the downloaded files will be saved. If not specified, './data/' will be used.")
	parser.add_argument("-r", "--recursive", action="store_true", help="recursively downloads the images in a URL received as a parameter")
	parser.add_argument("-l", "--max-depth", type=int, default=5, help="indicates the maximum depth level of the recursive download. Default is 5.")
	parser.add_argument("URL", help="URL to scrape")
	return (parser.parse_args())

def getPath(path):
	if not path:
		return ("./data/")
	if path.endswith('/'):
		return (path)
	else:
		return (path + '/')

if __name__ == "__main__":
	print(f"{LIGHT_GREEN}{ascii_header}{END}")
	start_time = time.time()

	args = parse_arguments()
	url = args.URL
	path = getPath(args.path)
	if args.recursive:
			depth_level = args.max_depth
	else:
		depth_level = 1
	if not os.path.exists(path): # create the directory path if it does not exist
		os.makedirs(path)
	spider(url, path, depth_level)

	end_time = time.time()
	print(f"{YELLOW}| Scrapping time: {round(end_time - start_time, 3)} seconds |", end="")
	print(f"{LIGHT_PURPLE}| Images captured: {g_img_captured} |{END}")