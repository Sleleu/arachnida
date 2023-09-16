#!/bin/python3
import requests
import sys
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

if __name__ == "__main__":
	try:
		assert len(sys.argv) > 1, "Usage: ./spider.py -option <url>"
	except AssertionError as Error:
		print(Error)
		exit(1)
	url = sys.argv[1]
	path = "./data/"
	spider(url, path)