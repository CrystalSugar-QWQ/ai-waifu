# 测试程序-录制动作
import vtube
import websockets
import asyncio

sport_file = "./sport/special/wink1.json"


async def vtube_run():
    # 连接上服务器,并初始化
    try:
        websocket = await websockets.connect('ws://127.0.0.1:8001')
        await vtube.init(websocket)
        print("[VTS 初始化完成]")
    except Exception:
        print("[VTS 无法连接]")
        return

    await asyncio.sleep(1)
    print("3", end="", flush=True)
    await asyncio.sleep(1)
    print("2", end="", flush=True)
    await asyncio.sleep(1)
    print("1", end="", flush=True)
    print("[开始录制]")
    await vtube.vtube_read(websocket, sport_file)
    print("[结束录制]")
    await asyncio.sleep(1)
    print("3", end="", flush=True)
    await asyncio.sleep(1)
    print("2", end="", flush=True)
    await asyncio.sleep(1)
    print("1", end="", flush=True)
    print("[开始播放]")
    await vtube.vtube_sportout(websocket, sport_file)
    print("[播放结束]")

    # 摆烂CV式写法，开摆~

def run():
    asyncio.run(vtube_run())
