import json
import asyncio
import keyboard

import vtube

file_json = "./vtube/config.json"   # 秘钥保存文件位置

async def init(websocket):
    with open(file_json, "r") as config_file:     # 读文件
        data = json.load(config_file)
        if data['authenticationkey'] == "":     # 判断是否没有令牌
            authtoken = await vtube.vtube_token(websocket)
            confirm = await vtube.vtube_plugin(websocket, authtoken)
            # print("[VTS API KEY]:", authtoken)
            data["authenticationkey"] = authtoken
        else:
            authtoken = data['authenticationkey']
            confirm = await vtube.vtube_plugin(websocket, authtoken)
            if confirm is False:
                authtoken = await vtube.vtube_token(websocket)
                confirm = await vtube.vtube_plugin(websocket, authtoken)
                data["authenticationkey"] = authtoken
            # print("[VTS API KEY]:", authtoken)
        config_file.close()
    config = {
        "authenticationkey": data["authenticationkey"],
    }
    config_file = open(file_json, "w")
    config_file.write(json.dumps(config))
    config_file.close()


async def vtube_read(websocket, sport_file):
    data = []
    while 1:
        # await uutils.vtube_control(websocket, parameter_values)
        parameter_values = await vtube.vtube_request(websocket)
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
        await vtube.vtube_control(websocket, data[i])
        await asyncio.sleep(0.02)
    return data[len(data) - 1]