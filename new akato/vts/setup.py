import vts.uutils as utils
import json

file_json = "config.json"   # 秘钥保存文件位置

async def init(websocket):
    with open(file_json, "r") as config_file:     # 读文件
        data = json.load(config_file)
        if data['authenticationkey'] == "":     # 判断是否没有令牌
            authtoken = await utils.vtube_token(websocket)
            confirm = await utils.vtube_plugin(websocket, authtoken)
            print("[VTS API KEY]:", authtoken)
            data["authenticationkey"] = authtoken
        else:
            authtoken = data['authenticationkey']
            confirm = await utils.vtube_plugin(websocket, authtoken)
            if confirm is False:
                authtoken = await utils.vtube_token(websocket)
                confirm = await utils.vtube_plugin(websocket, authtoken)
                data["authenticationkey"] = authtoken
            print("[VTS API KEY]:", authtoken)
        config_file.close()
    config = {
        "authenticationkey": data["authenticationkey"],
    }
    config_file = open(file_json, "w")
    config_file.write(json.dumps(config))
    config_file.close()
