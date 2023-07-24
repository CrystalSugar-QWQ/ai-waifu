# 测试程序-录制动作
import vts_sports.Vts as Vts
import websockets
import asyncio

sport_file = "./sport/special/wink1.json"

parameter_values = [{"id": "FaceAngleX", "value": 0}, 
                        {"id": "FaceAngleY", "value": 0}, 
                        {"id": "FaceAngleZ", "value": 0},
                        {"id": "EyeOpenLeft", "value": 10},
                        {"id": "EyeOpenRight", "value": 10},
                        {"id": "EyeRightX", "value": 0},
                        {"id": "EyeRightY", "value": 0},
                        {"id": "Brows", "value": 0.55},
                        {"id": "MouthSmile", "value": 0.6}]


async def vtube_run():
    # 连接上服务器,并初始化
    try:
        websocket = await websockets.connect('ws://127.0.0.1:8001')
        await Vts.init(websocket)
        print("[VTS 初始化完成]")
    except Exception:
        print("[VTS 无法连接]")
        return

    # parameter = await Vts.value_homing(websocket, parameter_values)

    await asyncio.sleep(1)
    print("3")
    await asyncio.sleep(1)
    print("2")
    await asyncio.sleep(1)
    print("1")
    print("[开始录制]")
    await Vts.vtube_read(websocket, sport_file)
    print("[结束录制]")
    await asyncio.sleep(1)
    print("3")
    await asyncio.sleep(1)
    print("2")
    await asyncio.sleep(1)
    print("1")
    print("[开始播放]")
    await Vts.vtube_sportout(websocket, sport_file)
    print("[播放结束]")

    # 摆烂CV式写法，开摆~


asyncio.run(vtube_run())

