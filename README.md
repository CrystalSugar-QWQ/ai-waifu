# ai-waifu
<a href="https://www.python.org">
    <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python">
</a>

本项目的目的是做一个ai-waifu兼ai-vtuber[效果视频](https://www.bilibili.com/video/BV1zu4y1U7Ae/?share_source=copy_web&vd_source=be871ab215f9686e9cf85ae02546df3f)  
如果有使用本项目的代码请注明出处（拒绝未经允许的商业行为），谢谢  
ps:有问题或技术支持请联系+Q：1262852040  

## 📖项目结构

- `blivedm`:[bilibili直播间弹幕获取](https://github.com/xfgryujk/blivedm)
- `chatglm`:依赖chatglm2的[openai_api.py](https://github.com/THUDM/ChatGLM2-6B/blob/main/openai_api.py)运行，并简单加入了角色设定功能，虽然使用效果并不理想，设定了4k的上下文
- `chatgpt`:老面孔了,除了费钱没什么不好。记得在`./config.py`内填入[openai API](https://platform.openai.com/account/api-keys)，同样拥有角色设定功能，4k的上下文，但是效果更佳
- `listen2text`:利用`SpeechRecognition`、`pyaudio`库制作出麦克风实时监听并转成文字的功能。内部还有使用百度语音转文字的接口,于[百度智能云](https://console.bce.baidu.com/ai/#/ai/speech/overview/index)获取秘钥，[参考视频](https://www.bilibili.com/video/BV1PN41127GF/?share_source=copy_web&vd_source=be871ab215f9686e9cf85ae02546df3f&t=228)为什么用别人的视频，开始摆烂诶嘿~
- `sport`:给vtube studio准备的动作库，如有需要定制修改请联系我
- `voice_tts`:利用[VOICEVOX](https://voicevox.hiroshiba.jp/)制作的tts语音输出，请记住运行程序前一定要打开这个`VOICEVOX\run.exe`！
- `vtube`:利用[vtube studio api](https://github.com/DenchiSoft/VTubeStudio)控制`vtube studio`软件，语音输出和动作输出均在`sport_and_tts.py`中，需要二次开发请注意


## 环境配置
python：3.10  
1、下载源代码  
2、安装依赖库  
`pip install -r requirements.txt`  
3、进入`./config.py`配置你的api（按需填写），[openai API](https://platform.openai.com/account/api-keys)、[百度智能云](https://console.bce.baidu.com/ai/#/ai/speech/overview/index)、[百度翻译开放平台](https://fanyi-api.baidu.com/api/trans/product/desktop),进入后会有注释引导  
4、[下载虚拟音频线软件](https://vb-audio.com/Cable/index.htm),安装时请使用**管理员权限**打开,跳提示了务必自己翻译看看写的什么  
5、打开Vtube studio,找到设置启用API选项并打开,麦克风配置里打开使用麦克风,选择麦克风为`CABLE Output`,  
动作输入将Mouth Open的输入改为`VoiceFrequency`。  
6、这一步请不要忘了设置,涉及到口型匹配和侦听语音  
打开音量合成器,将python的输入改成`你的麦克风`,输出改为`CABLE Input `  
打开系统的更多声音设置,再录制里找到`CABLE Output`右键点击**属性**,找到**侦听**勾选`侦听此设备`,播放设备选择你的**默认扬声器**  
如果出现噪音，在更多声音设置找到`CABLE Output`、`CABLE Input`，右键点击**属性**，找到**高级**选择最高音质`24位192000Hz`、`2通道24位192000Hz`  


## 运行
1、打开voicevox,注意不是打开VOICEVOX.exe,而是`run.exe`，以及打开vtube studio  
2、进入`blivedm/sample`.py,在`TEST_ROOM_IDS`填入直播间id,  
再找到`class MyHandler(blivedm.BaseHandler)`函数，`_on_danmaku`里面有触发问答的方式,比如弹幕里提到`白糖`和`。`,就会回复  
3、运行`run.py`，vtube studio会弹出插件提示，只需要同意一次即可  
4、启动后若频繁触发语音录入,请进入`listen2text`中,找到`audio = listen2text.audio_listen(THRESHOLD = 600.0)`函数中的音量阈值参数`THRESHOLD`,调高它,反之无法触发调小它，直到一个合适的值  
5、字幕功能，仅限OBS上使用，选择文本获取`input.txt`、`output.txt`即可  
6、完事，有问题请联系我，粉丝q群：592364636。（ 撅 达咩 ）  


## 特殊说明
`./vtube/sport_R.py`里有录制动作的函数，有需要自取使用  


## BUG说明
VTS的动作库有点少，凑合用。  
想用先凑合用，下次就改，下次一定。  
