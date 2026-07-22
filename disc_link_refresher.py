import requests
import time
import argparse
import html
import os


def refresh_cdn_links(expired_links: list[str], auth_token : str) -> dict:
    '''
    Uses the Discord API to get new versions of expired CDN links. Returns a dict of format {expired_link : refreshed_link}.
    
    :param expired_links: List of expired Discord CDN links
    :type expired_links: list[str]
    :param auth_token: Authentication token for the Discord API
    :type auth_token: str
    :return: a dict of format {expired_link : refreshed_link}
    :rtype: dict
    '''
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

    return { link_pair["original"] : link_pair["refreshed"] for link_pair in refreshed_old_pairs}

def chunk_list(to_chunk : list, chunk_size = 50):
    for i in range(0, len(to_chunk), chunk_size):
        yield to_chunk[i: i + chunk_size]

def refresh_cdn_link(expired_link : str, auth_token : str) -> str:
    """
    Refresh a single Discord CDN link.
    
    :param expired_link: the expired Discord CDN link
    :type expired_link: str
    :param auth_token: Authentication token for the Discord API
    :type auth_token: str
    :return: Refreshed, working version of the expired link
    :rtype: str
    """

    refreshed = refresh_cdn_links([expired_link], auth_token)
    return next(iter(refreshed.values()))

def refresh_cdn_links_no_old(expired_links: list[str], auth_token : str) -> list[str]:
    """
    Use Discord API to get refreshed cdn links from expired cdn links. Returns only the new links with no association to the old ones.
    
    :param expired_links: List of expired Discord CDN links
    :type expired_links: list[str]
    :param auth_token: Authentication token for the Discord API
    :type auth_token: str
    :return: A list of the new, refreshed links as strings
    :rtype: list[str]
    """
    return list(refresh_cdn_links(expired_links, auth_token).values())

def refresh_links_in_file(file_path : str):
    # Stub
    # Remember to do html escapes, just in case
    return



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--link", action = "store", help = "single Discord CDN link to refresh")
    parser.add_argument("-lf", "--link-file", action = "store", help = "a file to refresh and replace the Discord CDN links in")
    parser.add_argument("-t", "--token", action = "store", help = "Discord API authentication token")
    args = parser.parse_args()

    if not args.token:
        args.token = os.environ["DISCORD_TOKEN"]

    if args.link_file:
        refresh_links_in_file(args.link_file)

    if args.link:
        print(refresh_cdn_link(args.link))

    # Debug
    test_link_list = [html.unescape("https://cdn.discordapp.com/attachments/1424247441405771958/1424247677830435007/A_Grim_Hunt-1_.png?ex=6a5a5443&amp;is=6a5902c3&amp;hm=601a5f08f402ef47e2e9c514bc5a427f15a03fe8f2869aad55a920f78ba47b26&amp;")]
    refreshed = refresh_cdn_links(test_link_list, args.token)
    print(next(iter(refreshed.values())))

if __name__ == "__main__":
    main()
