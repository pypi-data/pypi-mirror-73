# Play Store Scrapper
Using this package you can easily scrap data from Google Play Store.

## Installation
```
pip install play-store-scrapper
```
### Environment Variables
Set the following Environment variables before running.

`GECKO_DRIVER_PATH` Path to Gecko Web Driver  (You also need Firefox to run this. For now no other browser option is added)

## Usage
```python
from play_store_scapper import PlayStore
store = PlayStore()
# Get Dict containing list of categories for 'apps' and 'games' separately
all_categories = store.get_categories()
# Each category in 'apps' or 'games' is a dict containing 'slug' and 'label' for that category
apps_in_category_0 = get_apps_in_category(all_categories['apps'][0]['slug'])
# Fetch App Details using the Google Play Store Id of the app
store.get_app_detail("com.cstayyab.beemy")
```

