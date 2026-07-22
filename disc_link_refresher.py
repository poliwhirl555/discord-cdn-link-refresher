import requests
import time

def refresh_cdn_link(expired_links: list[str], auth_token : str) -> list[dict]:
    '''
    Uses the Discord API to get new versions of expired CDN links. Returns a list of dicts of format {"original": expired_link, "refreshed": refreshed_link}.
    
    :param expired_links: List of expired Discord CDN links
    :type expired_links: list[str]
    :param auth_token: Authentication token for the Discord API
    :type auth_token: str
    :return: list of dicts of format {"original": expired_link, "refreshed": refreshed_link}
    :rtype: list[dict]
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

    return refreshed_old_pairs


    
def chunk_list(to_chunk : list, chunk_size = 50):
    for i in range(0, len(to_chunk), chunk_size):
        yield to_chunk[i: i + chunk_size]



def main():
    print("Hello from discord-cdn-link-refresher!")


if __name__ == "__main__":
    main()
