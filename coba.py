import gdown
import pandas as pd
import datetime
import os


# link download assets update
idFileAssets = "1DFRSfYc58Nk0QTpWY6bNp5HMfx32U-YO"
# url = "https://drive.usercontent.google.com/uc?id=1DFRSfYc58Nk0QTpWY6bNp5HMfx32U-YO"

output = "assetsFile.csv"

# gdown.download(id=idFileAssets, output=output)

pd.options.display.max_rows = 99
df = pd.read_csv('assetsFile.csv')

# print(df)
# timetamp
nowTimestamp = datetime.datetime.now(datetime.timezone.utc) # now is a datetime object

for x in range(df.index.size):
  tempLink = df.loc[x,"Links"]
  id = tempLink
  gdown.download_folder(id=id, output=f"assets/{int(nowTimestamp.timestamp())}")
#   print(x)

# # a file
# url = "https://drive.usercontent.google.com/uc?id=1DFRSfYc58Nk0QTpWY6bNp5HMfx32U-YO"
# output = "fcn8s_from_caffe.npz"
# gdown.download(url, output)

# # same as the above, but with the file ID
# id = "0B9P1L--7Wd2vNm9zMTJWOGxobkU"
# gdown.download(id=id, output=output)

# # same as the above, and you can copy-and-paste a URL from Google Drive with fuzzy=True
# url = "https://drive.google.com/file/d/0B9P1L--7Wd2vNm9zMTJWOGxobkU/view?usp=sharing"
# gdown.download(url=url, output=output, fuzzy=True)

# # Cached download with identity check via MD5 (or SHA1, SHA256, etc).
# # Pass postprocess function e.g., extracting compressed file.
# md5 = "md5:fa837a88f0c40c513d975104edf3da17"
# gdown.cached_download(url, output, hash=hash, postprocess=gdown.extractall)

# # a folder
# url = "https://drive.google.com/drive/folders/15uNXeRBIhVvZJIhL4yTw4IsStMhUaaxl"
# gdown.download_folder(url)

# same as the above, but with the folder ID
# id = "1dZCe6WVyvXiimdK_gnGJsAxBz4Z4lABl"
# gdown.download_folder(id=id)