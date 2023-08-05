# danksearch

danksearch is an async library to search youtube without using any API's.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install danksearch.

```bash
pip install danksearch
```

## Usage

General usage looks like

```python
import danksearch, asyncio

async def searchvideo():
    video=danksearch.Video()
    await video.search("spooky scary skeletons")
    print(video.url)

asyncio.run(searchvideo())
```

For grabbing a list of video urls(max 40)

```python
import danksearch, asyncio
async def getvideos():
    videolist=danksearch.VideoList()
    await videolist.search("yes")
    print(videolist.videos)

asyncio.run(getvideos())
```

## BetterVideo(Beta)

BetterVideo is a new feature in danksearch that aims to be faster and extinguishes the need of retrying.

```python
import danksearch, asyncio
async def getvideos():
    video=danksearch.BetterVideo()
    await video.search("yes")
    print(video.url) #also has video.links for a full list of results


asyncio.run(getvideos())
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://github.com/actualdankcoder/danksearch-discord/blob/master/LICENSE)