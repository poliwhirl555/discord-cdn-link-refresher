import requests
import time

def refresh_cdn_link(expired_links: list[str], auth_token : str):
    post_request_url = "https://discord.com/api/v10/attachments/refresh-urls"

    headers = {
        "Authorization": f"Bot {auth_token}",
        "Content-Type": "application/json",
        "User-Agent": "RefresherBot (https://github.com/poliwhirl555/discord-cdn-link-refresher, v0.1.0)"
    }

    # Need to add something to check if the link list is longer than 50, and to split it up if it is

    request_load = {
        "attachment_urls": expired_links
    }

    r = requests.post(post_request_url, headers = headers, json = request_load)

    while r.status_code == 429:
        retry_delay = int(r.headers.get("Retry-After"))
        time.sleep(retry_delay + 5)
        r = requests.post(post_request_url, headers = headers, json = request_load)

    
def chunk_list(to_chunk : list, chunk_size = 50):
    for i in range(0, len(to_chunk), chunk_size):
        yield to_chunk[i: i + chunk_size]



def main():
    print("Hello from discord-cdn-link-refresher!")


if __name__ == "__main__":
    main()
