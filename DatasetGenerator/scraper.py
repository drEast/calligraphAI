#################################################
# Google scraper:                               #
# create a data set from google images          #
# using specific searching keywords             #
#################################################
import os
import requests

import utils as utils

# settings:
GOOGLE_URL = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&&q='
PATH_OUT = '../data/data_calligraphy'

USER_HEADER = {
    'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}

# Google url extensions to search for specific predominate colors
COLOR_CODE = [
    '&tbs=ic%3Agray%2Cisz',
    '&tbs=ic%3Aspecific%2Cisc%3Ared%2Cisz',
    '&tbs=ic%3Aspecific%2Cisc%3Aorange%2Cisz',
    '&tbs=ic%3Aspecific%2Cisc%3Ayellow%2Cisz',
    '&tbs=ic%3Aspecific%2Cisc%3Agreen%2Cisz',
    '&tbs=ic%3Aspecific%2Cisc%3Ateal%2Cisz',
    '&tbs=ic%3Aspecific%2Cisc%3Ablue%2Cisz',
    '&tbs=ic%3Aspecific%2Cisc%3Apurple%2Cisz',
    '&tbs=ic%3Aspecific%2Cisc%3Apink%2Cisz',
    '&tbs=ic%3Aspecific%2Cisc%3Ared%2Cisz'
]

# Google url extensions to search for specific sizes
SIZE_CODE = [
    '%3Am',
    '%3Al'
]

# entry for the image search
search_terms = [
    'arabic calligraphy',
    # 'arabic calligraphy names',
    'خط اسم'
]


def create_set(keywords, amount=10):
    """ Saves specific number of images for each keyword to given location.

    keywords: list of search terms
    amount: amount of images for each keyword
    path_out: path to the output folder
    """
    utils.create_folder(PATH_OUT)

    idx = 0
    for keyword in keywords:
        scrap_keyword(keyword, amount, idx)
        idx += amount


def scrap_keyword(keyword, amount, idx_start):
    """ Saves specific number of images for given keyword.

    keyword: search term for the google search
    amount: amount of images for this keyword
    idx_start: starting index number for the file name
    """
    search_url = google_url(keyword)
    links = extract_links(search_url, amount)

    for idx, link in enumerate(links):
        print(str(idx) + '/' + str(len(links)))
        download_img_by_url(link, idx_start+idx)


def download_img_by_url(url, idx):
    """ Saves an image at an url as jpg.

    url: download link
    idx: index number of the image used for name assignment
    """
    try:
        response_img = requests.get(url)
        img_name = str(idx) + '.jpg'
        img_path = os.path.join(PATH_OUT, img_name)
        with open(img_path, 'wb') as file:
            file.write(response_img.content)
    except (requests.exceptions.ConnectionError, requests.exceptions.SSLError):
        print("ConnectionError: Failed to download image " + str(idx))


def extract_links(search_url, max_amount):
    """ Extract a certain amount of image links to a given search_url.
    """
    amount = 0
    links = []

    # toggle between different color and size combination to receive different results for each search
    for mode in range(len(COLOR_CODE) * len(SIZE_CODE)):
        print('Extract links with mode ' + str(mode))

        # create url for specific color and size
        color_idx = int(mode/len(SIZE_CODE))
        size_idx = mode % len(SIZE_CODE)
        search_url_specific = search_url + COLOR_CODE[color_idx] + SIZE_CODE[size_idx]

        # search and store the links
        links_dated = search_by_url(search_url_specific)
        links += links_dated
        amount += len(links_dated)
        if amount > max_amount:
            break  # enough links collected
    return links[0:max_amount]


def search_by_url(search_url):
    """ Extract the image links to a given search_url. """
    response_html = requests.get(search_url, headers=USER_HEADER).text
    image_endings = ['.png\"', '.jpg\"', '.JPEG\"', '.tif\"', '.gif\"']

    # find the position of the image extensions
    end_positions = []
    for extension in image_endings:
        endings = [i + len(extension) - 2 for i in range(len(response_html)) if response_html.startswith(extension, i)]
        end_positions += endings

    # extract the full link by their end position
    links = []
    for idx_end in end_positions:
        idx_start = idx_end
        while response_html[idx_start] != "\"":
            idx_start -= 1
        link = response_html[idx_start+1:idx_end+1]
        # discard images that are not search related links
        if link.startswith("https://"):
            link = link.replace('\\u003d', '=')
            links.append(link)
    return links


def google_url(keyword):
    """ Provides google image search url.
     keyword: search term
     """
    # modify keyword to fit search url
    while '  ' in keyword:
        keyword = keyword.replace('  ', ' ')
    keyword = keyword.replace(' ', '+')

    url = GOOGLE_URL + keyword
    return url


if __name__ == '__main__':
    create_set(search_terms, amount=1000)

'''
Discussion:

I) Many scrappers I got inspirations from use more sophisticated ways to parse the html file such as the packages
BeautifulSoup and json. Although, it is more elegant style-wise, I came across many scrappers which lost their 
functionality since google changed the html structure. Therefore, I decided to use the crude method on character 
parsing searching for the image extensions.

II) A image search by url yields approximately 100 links to images. I did not find a simple way to increase this. 
Since to my knowledge search by date range is deactivated by google, the search for different sizes and colors were
chosen to receive a larger amount of images. Beware that this can completely screw up your data set composition. Here, 
I start with black and white images. For e.g. classification of animals only black and white images will not represent
the truth. Since I plan to transform all images to binary color space before using them, this should in theory not
cause a problem here.

Any thoughts are welcome here ;)
'''
