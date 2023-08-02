import sympy as sp
import asyncio

import vtube as Vts


# 正弦波函数，负责待机时动作,amplitude 振幅,frequency 频率,phase 相位,shifting 初始偏移
def sine_wave(time, amplitude = 2, frequency = 0.5, phase = 0, shifting = 0):
    # 定义符号变量
    x = sp.symbols('x')

    # 计算正弦波函数的表达式
    sin_expr = amplitude * sp.sin(2 * sp.pi * frequency * x + phase) + shifting

    # 计算正弦波函数的值，并将结果精确到8位小数
    value = sin_expr.subs(x, time).evalf(8)

    return float(value)


# 头，眼，眉，以及笑容, ！！！拒绝乱改！！！
async def waiting_model(time):
    #time = time / 100
    FaceAngleX = sine_wave(time,amplitude=1.5, frequency = 0.25)
    FaceAngleY = sine_wave(time,amplitude=1)
    FaceAngleZ = sine_wave(time,amplitude=2.5)
    EyeOpenLeft = EyeOpenRight = sine_wave(time, amplitude=10, shifting = 10)
    EyeRightX = sine_wave(time, amplitude=0.08, frequency = 0.25)
    EyeRightY = sine_wave(time, amplitude=0.05, frequency = 0.25)
    Brows = sine_wave(time,amplitude=0.025, shifting=0.55)
    MouthSmile = sine_wave(time, amplitude=0.08, shifting=0.6)


    parameter_values = [{"id": "FaceAngleX", "value": FaceAngleX}, 
                        {"id": "FaceAngleY", "value": FaceAngleY}, 
                        {"id": "FaceAngleZ", "value": FaceAngleZ},
                        {"id": "EyeOpenLeft", "value": EyeOpenLeft},
                        {"id": "EyeOpenRight", "value": EyeOpenRight},
                        {"id": "EyeRightX", "value": EyeRightX},
                        {"id": "EyeRightY", "value": EyeRightY},
                        {"id": "Brows", "value": Brows},
                        {"id": "MouthSmile", "value": MouthSmile}]
    # print(parameter_values)
    return parameter_values


# 不懂不要乱改参数，只因再改一下就会爆炸
async def value_homing(websocket, parameter_values, time_end = 0.5, FaceAngleX_end=0, FaceAngleY_end=0, FaceAngleZ_end=0, EyeOpen_end=10, EyeRightX_end=0, EyeRightY_end=0, Brows_end=0.55, MouthSmile_end=0.6):
    time = 0
    frequency = (1/(time_end*4))
    while True:
        FaceAngleX = sine_wave(time, frequency = frequency, amplitude = FaceAngleX_end-parameter_values[0]["value"], shifting = parameter_values[0]["value"])
        FaceAngleY = sine_wave(time, frequency = frequency, amplitude = FaceAngleY_end-parameter_values[1]["value"], shifting = parameter_values[1]["value"])
        FaceAngleZ = sine_wave(time, frequency = frequency, amplitude = FaceAngleZ_end-parameter_values[2]["value"], shifting = parameter_values[2]["value"])
        EyeOpen = sine_wave(time, frequency = frequency, amplitude = EyeOpen_end-parameter_values[3]["value"], shifting = parameter_values[3]["value"])
        EyeRightX = sine_wave(time, frequency = frequency, amplitude = EyeRightX_end-parameter_values[5]["value"], shifting = parameter_values[5]["value"])
        EyeRightY = sine_wave(time, frequency = frequency, amplitude = EyeRightY_end-parameter_values[6]["value"], shifting = parameter_values[6]["value"])
        Brows = sine_wave(time, frequency = frequency, amplitude = Brows_end-parameter_values[7]["value"], shifting = parameter_values[7]["value"])
        MouthSmile = sine_wave(time, frequency = frequency, amplitude = MouthSmile_end-parameter_values[8]["value"], shifting = parameter_values[8]["value"])
        parameter = [{"id": "FaceAngleX", "value": FaceAngleX}, 
                        {"id": "FaceAngleY", "value": FaceAngleY}, 
                        {"id": "FaceAngleZ", "value": FaceAngleZ},
                        {"id": "EyeOpenLeft", "value": EyeOpen},
                        {"id": "EyeOpenRight", "value": EyeOpen},
                        {"id": "EyeRightX", "value": EyeRightX},
                        {"id": "EyeRightY", "value": EyeRightY},
                        {"id": "Brows", "value": Brows},
                        {"id": "MouthSmile", "value": MouthSmile}]
        await Vts.vtube_control(websocket, parameter)
        await asyncio.sleep(0.02)
        if time == time_end:
            return parameter
        time += 0.02
        time = round(time, 2)


# 向右侧身wink
async def sport_wink1(websocket, parameter):
    time = 0
    time_end = [0.4, 0.3]   # 每条动作时间
    value = [[5, -10, 20, -0.5, -0.025, 0.1, 0.05, 0.05, 0.15],
             [1, -1.5, -3, 0, 0, -0.05, -0.025, -0.05, 0]]
    for i in range(0,2):
        frequency = (1/(time_end[i]*2))
        while True:
            FaceAngleX = sine_wave(time, frequency = frequency, amplitude = value[i][0], shifting = parameter[0]["value"])
            FaceAngleY = sine_wave(time, frequency = frequency, amplitude = value[i][1], shifting = parameter[1]["value"])
            FaceAngleZ = sine_wave(time, frequency = frequency, amplitude = value[i][2], shifting = parameter[2]["value"])
            EyeOpenLeft = sine_wave(time, frequency = frequency, amplitude = value[i][3], shifting = 0.5)
            EyeOpenRight = sine_wave(time, frequency = frequency, amplitude = value[i][4], shifting = 0.5)
            EyeRightX = sine_wave(time, frequency = frequency, amplitude = value[i][5], shifting = parameter[5]["value"])
            EyeRightY = sine_wave(time, frequency = frequency, amplitude = value[i][6], shifting = parameter[6]["value"])
            Brows = sine_wave(time, frequency = frequency, amplitude = value[i][7], shifting = parameter[7]["value"])
            MouthSmile = sine_wave(time, frequency = frequency, amplitude = value[i][8], shifting =  parameter[8]["value"])

            parameter_values = [{"id": "FaceAngleX", "value": FaceAngleX},
                                {"id": "FaceAngleY", "value": FaceAngleY},
                                {"id": "FaceAngleZ", "value": FaceAngleZ},
                                {"id": "EyeOpenLeft", "value": EyeOpenLeft},
                                {"id": "EyeOpenRight", "value": EyeOpenRight},
                                {"id": "EyeRightX", "value": EyeRightX},
                                {"id": "EyeRightY", "value": EyeRightY},
                                {"id": "Brows", "value": Brows},
                                {"id": "MouthSmile", "value": MouthSmile}]
            await Vts.vtube_control(websocket, parameter_values)
            await asyncio.sleep(0.02)
            
            if time >= time_end[i]:
                time = 0
                parameter = parameter_values
                break
            time += 0.02
            time = round(time, 2)


pink_face = False
black_face = False


async def expression(websocket, expression = None):
    global pink_face, black_face
    if expression == "脸红":
        if black_face is True:
            await Vts.vtube_hotkeys(websocket, "脸黑")
            black_face = False
        if pink_face is False:
            await Vts.vtube_hotkeys(websocket, "脸红")
            pink_face = True
    elif expression == "脸黑":
        if pink_face is True:
            await Vts.vtube_hotkeys(websocket, "脸红")
            pink_face = False
        if black_face is False:
            await Vts.vtube_hotkeys(websocket, "脸黑")
            black_face = False
    else:
        if pink_face is True:
            await Vts.vtube_hotkeys(websocket, "脸红")
            pink_face = False
        if black_face is True:
            await Vts.vtube_hotkeys(websocket, "脸黑")
            black_face = False
