# -*- coding: utf-8 -*-
"""
Basic script to harvest images from a IIIF manifest, allowing for a few common
issues.

To use, set the following parameters (below):
    manifest_url: The full URL of the object manifest
    
    region, scale, rotation: The (string) parameters to be sent to the IIIF image
        image server, according to the IIIF Image API
    
    out_folder: The destination folder for the images. Will be created if it
        doesn't exist already. MUST END WITH TRAILING SLASH.
        
        Note that ANY EXISTING CONTENT WILL BE OVER-
        WRITTEN. The user will be given a warning before proceeding.
        
        Use the home variable to specify the user's home directory, or other
        directories relative to it (e.g. home + "/out/")
        
Output:
    The manifest.json file and all images found will be downloaded and saved
    in the out_folder director.
    
Created on Wed Nov 27 16:30:38 2019

@author: peterstokes
"""

import sys
import io
import os
import json
import requests
from os.path import expanduser
from PIL import Image

# Set up the constants. You will not normally want to change these

# Constant strings, established by the IIIF standard.
# You only change these if your manifests or image server behaves differently 
# from expected (e.g. if the IIIF standard is changed).
PARAM_TEMPLATE = "%s/%s/%s"
ORIG_PARAM_STRING = "full/full/0" # Original parameters expected in manifest URL 
IMG_FILENAME = "default"        # Expected name of image file, without extension
EXTENSIONS = { "image/jpeg" : ".jpg",
            "image/tiff" : ".tif"}
DEFAULT_EXTENSION = EXTENSIONS["image/jpeg"]


# If set to True then all the images will be saved to disk.
SAVE_IMAGES = False

# Specifies which sequence and image number to use, and which canvas for the sample URL
SEQUENCE_NUMBER = 0
IMAGE_NUMBER = 0
SAMPLE_CANVAS = 0

# Constants for the status bar displayed to the user
SB_LENGTH = 40
SB_FSTRING = "[%-" + str(SB_LENGTH) + "s] %d%%\t%s"

# String constants used to create the list of URLs saved to a file in save_imagelist()

# String template used for each line in the list of images.
# First parameter is the URL, second is the label
# Choose the format for your needs, or add a new one as required
# It will help also to change OUTPUT_EXTENSION to match your file type.
#OUTPUT_TEMPLATE = '"%s"\t"%s"\n'                # CSV format
#OUTPUT_TEMPLATE = "<tr><td>%s</td><td>%s</td></tr>\n"             # HTML table row
OUTPUT_TEMPLATE = "<tr><td><a href='%s'><img src='%s'/></a></td><td>%s</td></tr>\n" # HTML with Image
#OUTPUT_EXTENSION = "csv"
OUTPUT_EXTENSION = "html"
OUTPUT_FILENAME = "images"


# Set up parameters: you will want to change these depending on your case
# TODO: Ideally these should be modifiable via command-line flags
manifest_url = "https://iiif.bodleian.ox.ac.uk/iiif/manifest/441db95d-cdff-472e-bb2d-b46f043db82d.json"
#manifest_url = "https://iiif.bodleian.ox.ac.uk/iiif/manifest/441db95d-cdff-472e-bb2d-b46f043db82d.json"
region = "full"
scale = "pct:20"
rotation = "0"
# TODDO: Ideally the out_folder would depend on some sort of object identifier.
# In practice the manifest IDs seem to be too unpredictable or meaningless to
# use directly.
home = expanduser("~")                  # Gets the user's home directory
out_folder = home + "/out/"
new_param_string = PARAM_TEMPLATE % (region, scale, rotation)


def url_from_resource(resource):
    """
    Get image URL and format from a IIIF manifest resource element.
    
    Some (older?) manifests don't include the parameters (size, rotation etc),
    so we need to check and add if necessary.
    """
    
    url_in = resource["@id"]
    if (url_in.find(ORIG_PARAM_STRING) == -1):
        res_url = url_in + "/" + new_param_string + "/" + IMG_FILENAME + DEFAULT_EXTENSION
    else:
        res_url = url_in.replace(ORIG_PARAM_STRING, new_param_string)
        
    # Try to get the file format from the manifest. 
    # If we can't find it then assume DEFAULT_EXTENSION
    try:
        res_format = EXTENSIONS[resource["format"]]
    except KeyError:
        # Can't identify the image type so use the default
        sys.stderr.write("No file type detected; assuming", DEFAULT_EXTENSION)
        res_format = DEFAULT_EXTENSION

    return (res_url, res_format)


def save_images(images, im_extension):
    """ Downloads and saves the images from a list.
    
    Input parameters: expects a list of (url, label) tuples, where
        url is a string containing the URL of a IIIF-compliant image, and
        label is a string label (short description) of the image
        
    Result is all the images saved in the directory out_folder, with image names 
        based on the label.
        A basic progress bar is also displayed to the user
    """
    
    print("Downloading images...")
    sys.stdout.write(SB_FSTRING % ("", 0, ""))
    for (image_url, label) in images:
        # Download and save the image
        # Check image is returned and that server doesn't throw error
        res = requests.get(image_url)
        try:
            image = Image.open(io.BytesIO(res.content))
        except OSError:
            # Apparently we had a problem loading the image
            # Try loading as text instead, and display a message to the user
            # TODO: This assumes a IIIF request error, in which case the server should
            # have returned a message (string). We should also check for other
            # types of error (e.g. HTTP errors), which should be recorded in the 
            # requests object.
            # TODO: Ideally we should also check the info.json in advance of the
            # request, to ensure that the server can handle the request parameters.
            sys.stderr.write("\nError detected downloading file " + res.url+"\n")
            sys.stderr.write(res.text)
            sys.stderr.write("\r\r\r")
            pass
        fname = out_folder + label + im_extension
        image.save(fname)
        
        # Update and show the status bar to inform the user of progress
        i = images.index((image_url, label))+1
        sys.stdout.write("\r")
        prop = i / len(images)
        sys.stdout.write(SB_FSTRING % ('='*int(prop*SB_LENGTH), prop*100, "Image " + fname))
        sys.stdout.flush()
        
def save_imagelist(images):
    """ Builds and saves a file of the URLs of images in a list.
    
    Input parameters: expects a list of (url, label) tuples, where
        url is a string containing the URL of a IIIF-compliant image, and
        label is a string label (short description) of the image
        
    Result is a text file saved in the directory out_folder, containing
        each URL and label processed according to the string template in 
        OUTPUT_TEMPLATE.
        The file name is OUTPUT_FILENAME with extension OUTPUT_EXTENSION.
    """

    im_str = ""
    for im in images:
        url_temp, label = im
        im_str += OUTPUT_TEMPLATE % (url_temp, url_temp, label)
    
    im_str = "<html><head>Images</head><body>" + im_str + "</body></html>"
    
    with open(out_folder + OUTPUT_FILENAME + "." + OUTPUT_EXTENSION, "w") as outfile:
        outfile.write(im_str)
    outfile.close()

def warn(msg_string):
    """ Simple function to warn user of something and give a chance to exit."""
    print(msg_string)
    resp = input("Continue? [Y/n] ")
    if (resp[0].upper() != 'Y'):
        print("OK; exiting now")
        sys.exit()


# Download the manifest
res = requests.get(manifest_url)
#res.encoding = 'utf8'            # Uncomment if there's an encoding error
manifest = res.json()

# Get the list of canvases (assuming only one sequence)
canv_list = manifest["sequences"][SEQUENCE_NUMBER]["canvases"]

# Generate sample URL and check that we really want to go ahead
print("Found", len(canv_list), "canvases")
resource_sample = canv_list[SAMPLE_CANVAS]["images"][IMAGE_NUMBER]["resource"]
url_sample, format_sample = url_from_resource(resource_sample)
print("Example URL is", url_sample)
print("Extension for detected file type is", format_sample)
warn("")

# Check that the folder exists, and create it if necessary
# Also check for existing contents, so as not to overwrite everything
if not(os.path.exists(out_folder)):
    os.makedirs(out_folder)
    
if os.path.exists(out_folder+"manifest.json"):
    warn("WARNING: There appears to already be content in folder " + out_folder)

# Save the manifest as a record
with open(out_folder + "manifest.json", "w") as outfile:
    json.dump(manifest, outfile)

# Now work through the list of images
im_list = []
for c in canv_list:
    # Get the URL and other details of the image
    resource = c["images"][IMAGE_NUMBER]["resource"]
    
    img_url, extension = url_from_resource(resource)
    label = c["label"]
    
    im_list.append((img_url, label))
    
if SAVE_IMAGES:
    save_images(im_list, extension)

save_imagelist(im_list)
    
print("\nDone!")
