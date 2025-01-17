import pandas as pd
import cv2
from PIL import Image
import skimage.metrics as ski
import os
from pathlib import Path
from src import preprocess as pre


def ssimImage(df):
    """"""
    dim = df.shape

    img = Image.new("RGB", (dim[0], dim[1]), color="red")
    pixels = img.load()

    for row in df.itertuples():
        # Need row index for assignment
        for c in range(1, len(row)):
            # Capture data point @ [row, column]
            data = row[c]

            freq = int(255 * data)

            pixels[row[0], c - 1] = (0, freq, 0)

    return img


# 2. Construct the argument parse and parse the arguments
def ssim(first, second):
    """"""
    # 3. Load the two input images
    imageA = cv2.imread(first)
    imageB = cv2.imread(second)

    # 4. Convert the images to grayscale
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    # 5. Compute the Structural Similarity Index (SSIM) between the two
    #    images, ensuring that the difference image is returned
    (score, diff) = ski.structural_similarity(
        grayA, grayB, gaussian_weights=True, full=True
    )
    diff = (diff * 255).astype("uint8")

    # print("SSIM: {}".format(diff))
    return score


def createSSIMimage(data_directory):
    """"""
    parseDir = Path(data_directory).rglob("*.png")

    all = sorted(
        parseDir, key=lambda i: os.path.splitext(os.path.basename(i))[0]
    )
    files = [x for x in all]

    df = pd.DataFrame()
    temp = []
    i = 0
    for A in files:
        fileA = (str(A).split("'"))[0]
        for B in files:
            fileB = (str(B).split("'"))[0]
            temp.append(ssim(fileA, fileB))

        df[i] = temp
        temp = []
        i += 1

    # Generate Image
    return ssimImage(df)


##
##
##
def mse(first, second):
    """"""
    # Load the two input images
    imageA = cv2.imread(first)
    imageB = cv2.imread(second)
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    # return mean_squared_error(imageA, imageB)
    return ski.mean_squared_error(imageA, imageB)


def mseImage(df):
    """"""
    dim = df.shape

    img = Image.new("RGB", (dim[0], dim[1]), color="red")
    pixels = img.load()

    for row in df.itertuples():
        # Need row index for assignment
        for c in range(1, len(row)):
            # Capture data point @ [row, column]
            data = row[c]

            freq = int(255 * data)

            pixels[row[0], c - 1] = (0, 255 - freq, 0)

    return img


def createMSEimage(data_directory):
    """"""
    parseDir = Path(data_directory).rglob("*.png")

    all = sorted(
        parseDir, key=lambda i: os.path.splitext(os.path.basename(i))[0]
    )
    files = [x for x in all]

    df = pd.DataFrame()
    temp = []
    i = 0
    for A in files:
        fileA = (str(A).split("'"))[0]
        for B in files:
            fileB = (str(B).split("'"))[0]
            temp.append(mse(fileA, fileB))

        df[i] = temp
        temp = []
        i += 1

    # Generate Image
    return mseImage(takeLog(df))


def takeLog(df):
    """"""
    maxVal = df.max().max()
    shape = df.shape
    log_freq = pd.DataFrame(0, index=range(shape[0]), columns=range(shape[1]))
    if maxVal <= 1:
        return log_freq

    for row in df.itertuples():
        # Need row index for assignment
        for c in range(1, len(row)):
            # Capture data point @ [row, column]
            data = row[c]
            # print(data, end="")
            # Expecting 0.5 -> inf (nan)
            d = pre.log_base(maxVal, data)

            # # -inf or < 0
            # if(d < 0): l = d * -1
            # # inf or > 0
            # else: l = d
            # print(f"Data: {data} ... logit: {d}")

            # row[0] = Index ; c = columns
            # Offest Columns by the included index
            log_freq.loc[row[0], c - 1] = d

    # print("Calculated Logit")

    return log_freq