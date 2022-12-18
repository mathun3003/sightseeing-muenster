import logging
import sys
import multiprocessing
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
from datetime import datetime
from multiprocessing import freeze_support
import os
import zipfile

from bing_image_downloader import downloader


sights = ['Schloss Münster',
          'Prinzipalmarkt Münster',
          'kiepenkerl denkmal münster',
          'St. Paulus Dom Münster',
          'LWL-Museum für kunst und kultur münster',
          'Erbdrostenhof münster',
          'Sankt Lamberti Münster']


def _zipdir(src, dst, zip_name):
    """
    Function creates zip archive from src in dst location. The name of archive is zip_name.
    :param src: Path to directory to be archived.
    :param dst: Path where archived dir will be stored.
    :param zip_name: The name of the archive.
    :return: None
    """
    ### destination directory
    os.chdir(dst)
    ### zipfile handler
    ziph = zipfile.ZipFile(zip_name, 'w')
    ### writing content of src directory to the archive
    for root, dirs, files in os.walk(src):
        for file in files:
            ### In this case the structure of zip archive will be:
            ###       C:\Users\BO\Desktop\20200307.zip\Audacity\<content of Audacity dir>
            # ziph.write(os.path.join(root, file), arcname=os.path.join(root.replace(os.path.split(src)[0], ""), file))

            ### In this case the structure of zip archive will be:
            ###       C:\Users\BO\Desktop\20200307.zip\<content of Audacity dir>
            ziph.write(os.path.join(root, file), arcname=os.path.join(root.replace(src, ""), file))
    ziph.close()


def scraping(query: str, download_folder='data', num_images=100):
    """
    Scraper function using the bild image downloader package.
    :param num_images: number of images that should be scraped
    :param download_folder: download folder in current working directory
    :param query: sight to be scraped
    :return: images to specified download folder
    """
    # logger.info(f'{"=" * 10} Downloding for the sight - {query} {"=" * 10}')
    downloader.download(query, limit=num_images,
                        output_dir=download_folder,
                        adult_filter_off=True,
                        force_replace=True,
                        timeout=60,
                        verbose=True,
                        filter='photo')
    # logger.info(f'{"=" * 10} Finished downloding for the sight - {query} {"=" * 10}')

    _zipdir(f'./data/{query}', f'./data/{query}', f'{query}.zip')

    location = f'./data/{query}'
    path = os.path.join(location, dir)

    os.remove(path)
    pass


def bing_scraper(query: str, count: int, adult='off'):
    adlt = adult  # can be set to 'moderate'
    sear = query.strip()
    sear = sear.replace(' ', '+')
    URL = 'https://bing.com/images/search?q=' + sear + '&safeSearch=' + adlt + '&count=' + count
    print(URL)
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    headers = {"user-agent": USER_AGENT}
    resp = requests.get(URL, headers=headers)
    results = []
    soup = BeautifulSoup(resp.content, "html.parser")
    print(soup)
    wow = soup.find_all('a', class_='iusc')
    for i in wow:
        try:
            print(eval(i['m'])['murl'])
            print()
        except:
            pass
    pass


if __name__ == '__main__':
    # multiprocessing pool object
    pool = multiprocessing.Pool()
    pool.map(scraping, sights)

    # for sight in sights:
    #     try:
    #         scraping(sight, num_images=500)
    #     except:
    #         continue
