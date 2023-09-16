#!/bin/python3
import requests
import argparse
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import time

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

def isValidExtension(img_response):
	valid_mime_types = ["image/jpg", "image/jpeg", "image/png", "image/bmp", "image/gif"]
	content_type = img_response.headers.get('content-type')
	if content_type in valid_mime_types:
		return (True)
	return (False)

def downloadImage(image_url, path):
	img_response = requests.head(image_url)
	if isValidExtension(img_response):
		img_content = requests.get(image_url).content
		img_name = os.path.basename(urlparse(image_url).path)  # To avoid url params
		img_path = os.path.join(path, img_name)
		if os.path.isdir(img_path):
			return
		open(img_path, 'wb').write(img_content)  # write in binary the content of the image

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
			if urlparse(href).netloc == urlparse(url).netloc:
				spider(href, path, depth_level - 1)

def parse_arguments():
	desc = "The spider program allow you to extract all the images from a website, \
			recursively, by providing a url as a parameter."
	parser = argparse.ArgumentParser(description=desc)
	parser.add_argument("-p", "--path", help="indicates the path where the downloaded files will be saved. If not specified, './data/' will be used.")
	parser.add_argument("-r", "--recursive", help="recursively downloads the images in a URL received as a parameter")
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
	start_time = time.time()

	args = parse_arguments()
	url = args.URL
	path = getPath(args.path)
	depth_level = 2
	if not os.path.exists(path): # create the directory path if it does not exist
		os.makedirs(path)
	spider(url, path, depth_level)

	end_time = time.time()
	print(f"Execution time: {round(end_time - start_time, 3)} seconds")