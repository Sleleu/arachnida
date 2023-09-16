#!/bin/python3
import requests
import argparse
import os
from bs4 import BeautifulSoup

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

def spider(url: str, path: str):
	response = getResponse(url) # get response object from url
	html_data = response.text
	soup = BeautifulSoup(html_data, 'html.parser')
	images =  soup.find_all('img')
	img_src = getImgSrc(images, url) # get url of each image
	if not os.path.exists(path): # create the directory path if it does not exist
		os.makedirs(path)
	for image in img_src:
		img_content = requests.get(image).content
		open(path + image.split('/')[-1], 'wb').write(img_content) # write in binary the content of the image

def parse_arguments():
	desc = "The spider program allow you to extract all the images from a website, \
			recursively, by providing a url as a parameter."
	parser = argparse.ArgumentParser(description=desc)
	parser.add_argument("-p", "--path", help="indicates the path where the downloaded files will be saved. If not specified, './data/' will be used.")
	parser.add_argument("URL", help="URL to scrape")
	return	(parser.parse_args())

def getPath(path):
	if not path:
		return ("./data/")
	if path.endswith('/'):
		return (path)
	else:
		return (path + '/')

if __name__ == "__main__":
	args = parse_arguments()
	url = args.URL
	path = getPath(args.path)
	spider(url, path)