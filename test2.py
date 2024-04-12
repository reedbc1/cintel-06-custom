import pandas as pd
import urllib.request

# Read CSV data from URL
url = "https://drive.google.com/file/d/1r0FjYhFnG9aBKBVMyEn6UGqUxUcnqki-/view?usp=sharing"
response = urllib.request.urlopen(url)
data = pd.read_csv(response)