#! /usr/bin/env python3

import os
import requests
import re

descriptions_path = 'supplier-data/descriptions/'
image_path = 'supplier-data/images/'

text_files = sorted(os.listdir(descriptions_path))
jpeg_images = sorted([image_name for image_name in os.listdir(
    image_path) if '.jpeg' in image_name])

fruits = []
fruit_count = 0

for file in text_files:
    format = ['name', 'weight', 'description']

    with open(descriptions_path + file, 'r') as f:
        fruit = {}
        contents = f.read().split("\n")[0:3]
        contents[1] = int((re.search(r'\d+', contents[1])).group())

        counter = 0
        for content in contents:
            fruit[format[counter]] = content
            counter += 1

        fruit['image_name'] = jpeg_images[fruit_count]

        fruits.append(fruit)
        fruit_count += 1

for item in fruits:
    response = requests.post('http://127.0.0.1:80/fruits/', json=item)

    if response.status_code != 201:
        raise Exception('POST error status={}'.format(response.status_code))
    else:
        print('Created feedback ID: {}'.format(response.json()['id']))
