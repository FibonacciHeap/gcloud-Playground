#!/usr/bin/env python
# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This script uses the Vision API's label detection capabilities to find a label
based on an image's content.

To run the example, install the necessary libraries by running:

    pip install -r requirements.txt

Run the script on an image to get a label, E.g.:

    ./label.py <path-to-image>
"""

# [START import_libraries]
import argparse
import base64
import io
import os

from google.cloud import vision


import googleapiclient.discovery
# [END import_libraries]

def detect_labels(path):
    """Detects labels in the file."""
    vision_client = vision.Client()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision_client.image(content=content)

    labels = image.detect_labels()

    print('Labels:')
    for label in labels:
        print(label.description)


def detect_properties(path):
    """Detects image properties in the file."""
    vision_client = vision.Client()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision_client.image(content=content)

    properties = image.detect_properties()
    print('Properties:')
    avg_red = 0
    avg_green = 0
    avg_blue = 0
    for prop in properties:
        for color in prop.colors:
            # color.pixel_fraction
            print('fraction: {}'.format(color.score))
            print('r: {}'.format(color.color.red))
            print('g: {}'.format(color.color.green))
            print('b: {}'.format(color.color.blue))
            avg_red += color.color.red * color.score
            avg_green += color.color.green * color.score
            avg_blue += color.color.blue * color.score
    print(round(avg_red), round(avg_green), round(avg_blue))

def main(photo_file):
    """Run a label request on a single image"""
    detect_labels(photo_file)
    print('\n')
    detect_properties(photo_file)

    # # [START authenticate]
    # service = googleapiclient.discovery.build('vision', 'v1')
    # # [END authenticate]

    # # [START construct_request]
    # with open(photo_file, 'rb') as image:
    #     image_content = base64.b64encode(image.read())
    #     service_request = service.images().annotate(body={
    #         'requests': [{
    #             'image': {
    #                 'content': image_content.decode('UTF-8')
    #             },
    #             'features': [{
    #                 'type': 'LABEL_DETECTION',
    #                 'maxResults': 1
    #             }]
    #         }]
    #     })
    #     # [END construct_request]
    #     # [START parse_response]
    #     response = service_request.execute()
    #     label = response['responses'][0]['labelAnnotations'][0]['description']
    #     print('Found label: %s for %s' % (label, photo_file))
    #     # [END parse_response]


# [START run_application]
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file', help='The image you\'d like to label.')
    args = parser.parse_args()
    main(args.image_file)
# [END run_application]
