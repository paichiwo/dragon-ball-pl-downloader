#!/usr/bin/env python3

import os
import requests
from bs4 import BeautifulSoup
from cda_downloader import CDA


def create_links_list(basic_link):
    # Ask user how many links to create and make a list of links

    start = int(input("What's the starting episode number ?: "))
    total = int(input("What's the total number of episodes ?: "))
    links_list = []
    for link_end in range(start, total+1):
        full_link = basic_link + str(link_end)
        links_list.append(full_link)
    return links_list


def get_cda_links(links_list):
    # Using links_list start iterating over pages, get links from embedded video and make film_links list

    film_links_list = []
    for link in links_list:
        a = requests.get(link)
        soup = BeautifulSoup(a.content, 'lxml')
        cda_links = soup.find_all('iframe')
        for cda_link in cda_links:
            print(cda_link['src'])
            film_links_list.append(cda_link['src'])
            # Count and display percentage
            full_list = len(links_list)
            empty_list = len(film_links_list)
            percentage = round(100 * empty_list / full_list, 2)
            print("{} %".format(percentage))
    return film_links_list


def create_cda_links_file(film_links_list):
    # Write contents of film_links_list to cda_links.txt file

    with open("cda_links.txt", "w") as f:
        for entry in film_links_list:
            f.write(entry + "\n")
        # Check if file was created
        if os.path.exists('cda_links.txt'):
            print('cda_links.txt successfully created')


def download_files():
    # Download files from cda_links.txt?

    user_input = input("Do you want to download? [y/n]: ")
    if user_input != "y":
        return
    # Cda_downloader module init
    cda = CDA(multithreading=2, progress_bar=True)
    # Iterate over links to download and save files to downloads folder
    count = 0
    list_of_counts = []
    with open('cda_links.txt', 'r') as f:
        full_list = len([x for x in f])
        f.seek(0)
        for link in f:
            cda.download_videos(path="/download/", urls=link)
            # Count and display percentage
            count += 1
            list_of_counts.append(count)
            empty_list = len(list_of_counts)
            percentage = round(100 * empty_list / full_list, 2)
            print("{} %".format(percentage))


def main():

    basic_link = 'https://dbpolska.net/anime/d/dragon_ball_z/'
    links_list = create_links_list(basic_link)
    film_links_list = get_cda_links(links_list)
    create_cda_links_file(film_links_list)
    download_files()


if __name__ == "__main__":
    main()
