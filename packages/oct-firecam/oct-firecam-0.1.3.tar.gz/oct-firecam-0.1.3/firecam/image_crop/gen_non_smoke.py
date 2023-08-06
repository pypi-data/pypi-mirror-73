# Copyright 2020 Open Climate Tech Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""

Reads data from csv export of "first image" subsheet of Cropped Images sheet
to generate all the segments of the image that don't contain smoke.  These will be
used for non-smoke training set. 

"""

import os, sys
from firecam.lib import settings
from firecam.lib import collect_args
from firecam.lib import goog_helper
from firecam.lib import img_archive
from firecam.lib import rect_to_squares

import re
import logging
import csv
from PIL import Image


def checkCoords(coords, cropInfo):
    if (coords[0] > cropInfo[2]) or (coords[2] < cropInfo[0]) or (coords[1] > cropInfo[3]) or (coords[3] < cropInfo[1]):
        return False
    else:
        logging.warning('Skipping intersection: %s, %s', coords, cropInfo)
        return True



def main():
    reqArgs = [
        ["o", "outputDir", "local directory to save images and segments"],
        ["i", "inputCsv", "csvfile with contents of Cropped Images"],
    ]
    optArgs = [
        ["s", "startRow", "starting row"],
        ["e", "endRow", "ending row"],
        ["d", "display", "(optional) specify any value to display image and boxes"],
    ]
    args = collect_args.collectArgs(reqArgs, optionalArgs=optArgs, parentParsers=[goog_helper.getParentParser()])
    startRow = int(args.startRow) if args.startRow else 0
    endRow = int(args.endRow) if args.endRow else 1e9

    googleServices = goog_helper.getGoogleServices(settings, args)
    cameraCache = {}
    with open(args.inputCsv) as csvFile:
        csvreader = csv.reader(csvFile)
        for (rowIndex, csvRow) in enumerate(csvreader):
            if rowIndex < startRow:
                continue
            if rowIndex > endRow:
                logging.warning('Reached end row: %d, %d', rowIndex, endRow)
                exit(0)
            logging.warning('row %d: %s', rowIndex, csvRow[:2])
            [cameraName, cropName] = csvRow[:2]
            if not cameraName:
                continue
            fileName = re.sub('_Crop[^.]+', '', cropName) # get back filename for whole image
            # TODO: update to img_archive.download...
            # dirID = getCameraDir(googleServices['drive'], cameraCache, fileName)
            # localFilePath = os.path.join(args.outputDir, fileName)
            # if not os.path.isfile(localFilePath):
            #     goog_helper.downloadFile(googleServices['drive'], dirID, fileName, localFilePath)
            # logging.warning('local %s', fileName)
            cropInfo = re.findall('_Crop_(\d+)x(\d+)x(\d+)x(\d+)', cropName)
            if len(cropInfo) != 1:
                logging.error('Failed to parse crop info %s, %s', cropName, cropInfo)
                exit(1)
            cropInfo = list(map(lambda x: int(x), cropInfo[0]))
            logging.warning('Dims: %s', cropInfo)
            imgOrig = Image.open(localFilePath)
            rect_to_squares.cutBoxesFiles(imgOrig, args.outputDir, fileName, lambda x: checkCoords(x, cropInfo))


if __name__=="__main__":
    main()
