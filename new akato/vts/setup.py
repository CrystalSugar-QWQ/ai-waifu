import vts.uutils as uutils
import json


async def init(websocket):
    with open("vts/config.json", "r") as config_file:     # 读文件
        data = json.load(config_file)
        if data['authenticationkey'] == "":     # 判断是否没有令牌
            authtoken = await uutils.vtube_token(websocket)
            print("[VTS API KEY]:", authtoken)
            data["authenticationkey"] = authtoken
        else:
            authtoken = data['authenticationkey']
            confirm = await uutils.vtube_plugin(websocket, authtoken)
            if confirm is False:
                authtoken = await uutils.vtube_token(websocket)
                data["authenticationkey"] = authtoken
            print("[VTS API KEY]:", authtoken)
    config_file.close()
    config = {
        "authenticationkey": data["authenticationkey"],
    }
    config_file = open("vts/config.json", "w")
    config_file.write(json.dumps(config))
    config_file.close()
