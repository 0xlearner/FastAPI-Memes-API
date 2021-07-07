import os as _os
import dotenv as _dotenv
import praw as _praw
import urllib.parse as _parse
import aiofiles
import aiohttp
import asyncio

_dotenv.load_dotenv()

def _create_reddit_client():
    client = _praw.Reddit(
        client_id = _os.environ["CLIENT_ID"],
        client_secret = _os.environ["CLIENT_SECRET"],
        user_agent = _os.environ["USER_AGENT"],

    )
    return client

def _is_image(post):
    try:
        return post.post_hint == "image"
    except AttributeError:
        return False

def _get_image_urls(client: _praw.Reddit, subreddit_name: str, limit: int):
    hot_memes = client.subreddit(subreddit_name).hot(limit=limit)
    image_urls = list()
    for post in hot_memes:
        if _is_image(post):
            image_urls.append(post.url)

    return image_urls

def _get_image_name(image_url: str) -> str:
    image_name = _parse.urlparse(image_url)
    return _os.path.basename(image_name.path)

def _create_folder(folder_name: str):
    """
    If the folder does not exist then create the folder
    using the given name
    """
    try:
        _os.mkdir(folder_name)
    except FileExistsError as e:
        print('The file path already exists!')
    else:
        print("Folder created!")


async def fetch_memes(session, url, subreddit_name):
    """
    Collects the images from the urls and stores them into
    the folders named after their subreddits
    """

    image_name = _get_image_name(url)
    _create_folder(subreddit_name)
    async with session.get(url) as response:

        if response.status == 200:
            async with aiofiles.open(f'{subreddit_name}/{image_name}', mode='wb') as file:
                await file.write(await response.read())
                await file.close()


async def main(image_urls:list, subreddit_name: str):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for image in image_urls:
            tasks.append(await fetch_memes(session, image, subreddit_name))

    data = await asyncio.gather(*tasks)
    return data




if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    subreddit_name = 'memes'
    limit = 20
    client = _create_reddit_client()
    images_urls = _get_image_urls(client=client, subreddit_name=subreddit_name, limit=limit)
    try:
        loop.run_until_complete(main(images_urls, subreddit_name))
    except Exception as e:
        print(e)