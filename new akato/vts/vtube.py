import asyncio
import websockets
import vts.setup as setup
import vts.uutils as uutils
import json
import keyboard
import random

vtube_api = 'ws://127.0.0.1:8001'

sport_file = "sport9.json"


async def vtube_read(websocket):
    data = []
    while 1:
        # await uutils.vtube_control(websocket, parameter_values)
        parameter_values = await uutils.vtube_request(websocket)
        print(parameter_values)
        data.append(parameter_values)
        await asyncio.sleep(0.02)
        if keyboard.is_pressed('RIGHT_SHIFT'):
            break
    with open(sport_file, "w") as f:
        json.dump(data, f)


async def vtube_sportout(websocket, file):
    with open(file, "r") as config_file:     # 读文件
        data = json.load(config_file)
    for i in range(len(data)):
        await uutils.vtube_control(websocket, data[i])
        await asyncio.sleep(0.02)


async def vtube_run(shared_data):
    # 连接上服务器：
    try:
        websocket = await websockets.connect(vtube_api)
    except Exception:
        print("[VTS 无法连接]")
        return

    print(websocket)
    # 初始化
    await setup.init(websocket)

    while True:
        if shared_data.value == 1:  # 眨眼
            await vtube_sportout(websocket, "vts/sport1.json")
            shared_data.value = 0   
        elif shared_data.value == 2:    # 晃头
            await vtube_sportout(websocket, "vts/sport2.json")
            shared_data.value = 0  
        elif shared_data.value == 3:    # 四处看
            await vtube_sportout(websocket, "vts/sport3.json")
            shared_data.value = 0
        elif shared_data.value == 4:    # 蔑视
            await vtube_sportout(websocket, "vts/sport4.json")
            shared_data.value = 0
        else:
            nn = random.randint(0,10)
            if nn < 3:
                await vtube_sportout(websocket, "vts/sport7.json")
            elif nn >= 3 and nn < 6:
                await vtube_sportout(websocket, "vts/sport8.json")
            elif nn >= 6 and nn < 9:
                await vtube_sportout(websocket, "vts/sport9.json")
            elif nn == 9:   #日常小幅度晃头
                await vtube_sportout(websocket, "vts/sport5.json")
            elif nn == 10:  #日常小幅度低头
                await vtube_sportout(websocket, "vts/sport6.json")
        # await vtube_read(websocket)
        # await uutils.vtube_request(websocket)


def vtube_worker(shared_data):
    # 创建事件循环
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)

    # 运行协程
    loop.run_until_complete(vtube_run(shared_data))
    loop.close()


if __name__ == '__main__':
    vtube_worker()
