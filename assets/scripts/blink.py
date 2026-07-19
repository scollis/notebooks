import asyncio
from aiohttp import ClientSession
from blinkpy.blinkpy import Blink
from blinkpy.auth import Auth
from blinkpy.helpers.util import json_load
from datetime import datetime

async def start():
    blink = Blink()
    auth = Auth(await json_load("/Users/scollis/circus.text"))
    blink.auth = auth
    await blink.start()
    for name, camera in blink.cameras.items():
        print(name)                   # Name of the camera
        print(camera.attributes)      # Print available attributes of camera

    now = datetime.utcnow().strftime("%Y%m%d-%H%M")
    camera = blink.cameras['Ellingwood Ridge ']
    await camera.snap_picture()       # Take a new picture with the camera
    await blink.refresh()             # Get new information from server
    await camera.image_to_file('/Users/scollis/blinks/Ellingwood_'+now+'.jpg')
    camera = blink.cameras['Cabin from road ']
    await camera.snap_picture()       # Take a new picture with the camera
    await blink.refresh()             # Get new information from server
    await camera.image_to_file('/Users/scollis/blinks/Cabin_'+now+'.jpg')
    camera = blink.cameras['Tram tracks']
    await camera.snap_picture()       # Take a new picture with the camera
    await blink.refresh()             # Get new information from server
    await camera.image_to_file('/Users/scollis/blinks/TramTracks_'+now+'.jpg')
    camera = blink.cameras['Backyard']
    await camera.snap_picture()       # Take a new picture with the camera
    await blink.refresh()             # Get new information from server
    await camera.image_to_file('/Users/scollis/blinks/Backyard_'+now+'.jpg')
    return blink

if __name__ == "__main__":
    blink = asyncio.run(start())