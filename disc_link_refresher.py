import requests
import time
import argparse
import html
import os
import re
import sys
from pathlib import Path


def refresh_cdn_links(expired_links: list[str], auth_token : str = "", download_location : str = "", verbosity : int = 0) -> dict:
    '''
    Uses the Discord API to get new versions of expired CDN links. Returns a dict of format {expired_link \: refreshed_link}.

    :param expired_links: List of expired Discord CDN links
    :type expired_links: list[str]
    :param auth_token: Authentication token for the Discord API. Defaults to environmental variable DISCORD_TOKEN if none provided.
    :type auth_token: str
    :param download_location: if not empty, location to download and save the contents of the refreshed link
    :type download_location: str
    :param verbosity: level of verbosity to print outputs in console when running. 
        Default is 0 meaning no prints, 1 prints the refreshed links as they are acquired, 2 prints both the old links alongside the refreshed links
    :type verbosity: int
    :return: a dict of format {expired_link \: refreshed_link}
    :rtype: dict
    '''

    if not auth_token:
        auth_token = os.environ["DISCORD_TOKEN"]

    post_request_url = "https://discord.com/api/v10/attachments/refresh-urls"

    headers = {
        "Authorization": f"Bot {auth_token}",
        "Content-Type": "application/json",
        "User-Agent": "RefresherBot (https://github.com/poliwhirl555/discord-cdn-link-refresher, v0.1.0)"
    }

    refreshed_old_pairs = []
    
    if len(expired_links) > 50:
        url_lists_to_refresh = chunk_list(expired_links)
    else:
        url_lists_to_refresh = [expired_links]

    for link_list in url_lists_to_refresh:

        request_load = {
            "attachment_urls": link_list
        }
    
        r = requests.post(post_request_url, headers = headers, json = request_load)
    
        while r.status_code == 429:
            retry_delay = int(r.headers.get("Retry-After"))
            time.sleep(retry_delay + 5)
            r = requests.post(post_request_url, headers = headers, json = request_load)

        if not r.status_code == 200:
            r.raise_for_status()

        returned_data = r.json()

        refreshed_old_pairs.extend(returned_data["refreshed_urls"])

        if verbosity == 1:
            print(returned_data["refreshed_urls"][0]["refreshed"])
        elif verbosity == 2:
            print(returned_data["refreshed_urls"])

    return_dict = { link_pair["original"] : link_pair["refreshed"] for link_pair in refreshed_old_pairs}

    if download_location:
        download_links(list(return_dict.values()), download_location)

    return return_dict

def chunk_list(to_chunk : list, chunk_size = 50):
    for i in range(0, len(to_chunk), chunk_size):
        yield to_chunk[i: i + chunk_size]

def download_links(links : list[str], download_location : str):
    used_names = set()
    for link in links:
        r = requests.get(link, timeout = 30)

        if r.status_code == 200:
            name = get_media_name(link)
            name = disambiguate_media_name(used_names, name)
            used_names.add(name)
            save_path = Path(download_location) / name
            with open(save_path, "wb") as f:
                f.write(r.content)
        else:
            r.raise_for_status()

def get_media_name(media_link : str) -> str:
        last_slash = media_link.rfind("/")
        question_mark = media_link.find("?")
        if not question_mark == -1:
            return media_link[last_slash + 1 : question_mark]
        else:
            return media_link[last_slash + 1 : ]

def disambiguate_media_name(used_names : set[str], original_name : str):
    name = original_name
    number_add = 1
    while name in used_names:
        period = name.rfind(".")
        dash_number_pattern = re.compile(r"-\d+")
        dash_number = re.search(dash_number_pattern, name)

        if dash_number and len(dash_number.group()) > 0:
            dash = name.rfind(dash_number.group())
        else:
            dash = None

        if not dash:
            name = name[:period] + "-" + str(number_add) + name[period : ]
            number_add = number_add + 1
        else:
            number_add = int(dash_number.group()[1:]) + 1
            name = name[:dash] + "-" + str(number_add) + name[period : ]

    return name


def refresh_cdn_link(expired_link : str, auth_token : str = "", download_location: str = "", verbosity : int = 0) -> str:
    """
    Refresh a single Discord CDN link.
    
    :param expired_link: the expired Discord CDN link
    :type expired_link: str
    :param auth_token: Authentication token for the Discord API. Defaults to environmental variable DISCORD_TOKEN if none provided.
    :type auth_token: str
    :param download_location: if not empty, location to download and save the contents of the refreshed link
    :type download_location: str
    :param verbosity: level of verbosity to print outputs in console when running. 
        Default is 0 meaning no prints, 1 prints the refreshed links as they are acquired, 2 prints both the old links alongside the refreshed links
    :type verbosity: int
    :return: Refreshed, working version of the expired link
    :rtype: str
    """

    refreshed = refresh_cdn_links([expired_link], auth_token, download_location, verbosity)
    return next(iter(refreshed.values()))

def refresh_cdn_links_no_old(expired_links: list[str], auth_token : str = "", download_location: str = "", verbosity = 0) -> list[str]:
    """
    Use Discord API to get refreshed cdn links from expired cdn links. Returns only the new links with no association to the old ones.
    
    :param expired_links: List of expired Discord CDN links
    :type expired_links: list[str]
    :param auth_token: Authentication token for the Discord API. Defaults to environmental variable DISCORD_TOKEN if none provided.
    :type auth_token: str
    :param download_location: if not empty, location to download and save the contents of the refreshed links
    :type download_location: str
    :param verbosity: level of verbosity to print outputs in console when running. 
        Default is 0 meaning no prints, 1 prints the refreshed links as they are acquired, 2 prints both the old links alongside the refreshed links
    :type verbosity: int
    :return: A list of the new, refreshed links as strings
    :rtype: list[str]
    """
    return list(refresh_cdn_links(expired_links, auth_token, download_location, verbosity).values())

def refresh_links_in_file(file_path : str, auth_token : str = "", download_location: str = "", is_html : bool = False, verbosity : int = 0):
    """
    Refresh all links in a given file and create a copy of it with all expired links replaced by the new links.
    
    :param file_path: path of file with links to be refreshed
    :type file_path: str
    :param auth_token: Authentication token for the Discord API. Defaults to environmental variable DISCORD_TOKEN if none provided.
    :type auth_token: str
    :param download_location: if not empty, location to download and save the contents of the refreshed links
    :type download_location: str
    :param is_html: indicates to the function whether the file is an html file, to know if unescaping the links is necessary
    :type is_html: bool
    :param verbosity: level of verbosity to print outputs in console when running. 
        Default is 0 meaning no prints, 1 prints the refreshed links as they are acquired, 2 prints both the old links alongside the refreshed links
    :type verbosity: int
    """

    file_path_as_Path = Path(file_path)
    out_file_name = "refreshed-" + file_path_as_Path.name

    out_path = file_path_as_Path.parent / out_file_name

    with open(file_path, "r", encoding = "utf-8") as file, open(out_path, "w", encoding = "utf-8") as out:
        cdn_link_pattern = cdn_link_pattern = re.compile(r"https?://(?:cdn|media)\.discordapp\.(?:com|net)/attachments/[^\s\"\']*")

        links_already_done = dict()
        out_line = ""

        for line in file:
            out_line = line

            if is_html:
                line = html.unescape(line)

            found_links = re.findall(cdn_link_pattern, line)

            for link in found_links:
                already_done = links_already_done.get(link)

                if not already_done:
                    refreshed_link = refresh_cdn_link(link, auth_token, download_location, verbosity)
                    links_already_done[link] = refreshed_link
                    already_done = refreshed_link

                if is_html:
                    link = html.escape(link)
                    already_done = html.escape(already_done)
                
                out_line = out_line.replace(link, already_done)

            out.write(out_line) 

        

def fetch_links_in_file(file_path : str, is_html : bool = False, save_location : str = "") -> list[str]:
    """
    Utility function to find all the Discord cdn links in a given file
    
    :param file_path: path of file to search for links in
    :type file_path: str
    :param is_html: indicates to the function whether the file is an html file, to know if unescaping the links is necessary
    :type is_html: bool
    :param save_location: location to save a file listing all the found links
    :type save_location: str
    :return: a list of the links found in the file as strings
    :rtype: list[str]
    """
    cdn_link_pattern = cdn_link_pattern = re.compile(r"https?://(?:cdn|media)\.discordapp\.(?:com|net)/attachments/[^\s\"\']*")

    found_links = []
    already_inserted = set()

    with open(file_path, "r") as file:
        for line in file:
            if is_html:
                line = html.unescape(line)
            links = re.findall(cdn_link_pattern, line)
            for link in links:
                if not link in already_inserted:
                    found_links.append(link)
                    already_inserted.add(link)

    if save_location:
        with open(save_location, "w") as out:
            for link in found_links:
                out.write(link + "\n")

    return found_links


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--link", action = "store", help = "single Discord CDN link to refresh")
    parser.add_argument("-lf", "--link-file", action = "store", help = "a file to refresh and replace the Discord CDN links in")
    parser.add_argument("-ht", "--html", action = "store_true", default = False, help = "used with -lf or --link-file to indicate the argument file is in html and links need to be unescaped. Does nothing otherwise")
    parser.add_argument("-t", "--token", action = "store", help = "Discord API authentication token")
    parser.add_argument("-d", "--download", action = "store", nargs = "?", const = os.getcwd(), default = "", help = "download the media of any refreshed links to given directory, or the working directory if not specified")
    parser.add_argument("-v", "--verbosity", action = "count", default = 0, help = "print refreshed links as they arrive (helps with knowing that the program didn't freeze for large lists)")
    args = parser.parse_args()

    if args.link_file:
        refresh_links_in_file(args.link_file, args.token, args.download, args.html, args.verbosity)

    if args.link:
        print(refresh_cdn_link(args.link, args.token, args.download, 0))

    if len(sys.argv) == 1:
        # Add some sort of user input here.
        return

    # Debug
    # test_link_list = [html.unescape("https://cdn.discordapp.com/attachments/1424247441405771958/1424247677830435007/A_Grim_Hunt-1_.png?ex=6a5a5443&amp;is=6a5902c3&amp;hm=601a5f08f402ef47e2e9c514bc5a427f15a03fe8f2869aad55a920f78ba47b26&amp;")]
    # refreshed = refresh_cdn_links(test_link_list, args.token, args.download)
    # print(next(iter(refreshed.values())))

    # fetch_links_in_file("archive_(349) Test Chat Gif Discord_2026-07-20.html", "links-in-file", True)
    # refresh_links_in_file("archive_(349) Test Chat Gif Discord_2026-07-20.html", is_html = True)
    # fetch_links_in_file("refreshed-archive_(349) Test Chat Gif Discord_2026-07-20.html", "links-in-file2", True)

    # links = fetch_links_in_file("archive_(349) Test Chat Gif Discord_2026-07-20.html", is_html = True)
    # refreshed = refresh_cdn_links_no_old(links)
    # print(args.verbosity)
    # print(refreshed)


if __name__ == "__main__":
    main()
