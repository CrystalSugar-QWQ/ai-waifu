# ai-waifu
本项目主旨是做一个ai-waifu,能灵活自由聊天的ai  
由于作者刚学习python一个月,能力有限见谅  
想更改设定于openao/identity.txt里更改
有问题或技术支持请联系+Q：1262852040  
python版本3.10  
## 使用的外部软件
1、下载Vtube studio软件，于steam上下载即可  
2、[下载voicevox语音合成软件](https://voicevox.hiroshiba.jp/)  
3、[下载虚拟音频线软件](https://vb-audio.com/Cable/index.htm),安装时请使用管理员权限打开  
## 如何使用
1、安装python库  
`pip install -r requirements.txt`  
2、打开Vtube studio,找到启用API选项并打开,麦克风配置里打开使用麦克风,选择麦克风为**CABLE Output**,  
   动作输入将Mouth Smile的输入改为**VoiceVolume**,将Mouth Open的输入改为**VoiceFrequency**  
3、打开voicevox,注意不是打开VOICEVOX.exe,而是**run.exe**  
4、找到config.py文件，填入你[openai API](https://platform.openai.com/account/api-keys)  
5、启动前打开音量合成器,将程序的输入改成**你的麦克风**,输出改为**CABLE Input**  
再打开系统的更多声音设置,再录制里找到**CABLE Output**右键点击属性,找到侦听勾选**侦听此设备**,播放设备选择你的默认扬声器（你不做这步是听不见语音的）  
6、启动后若频繁触发语音录入,请进入VoiceRW/tts.py中,找到`audio_listien`函数中的音量阈值参数,调高它,反之无法触发调小它  
7、B站直播间弹幕获取也是有的,进入blivedm/sample.py,在`TEST_ROOM_IDS`填入直播间id,  
再找到`class MyHandler(blivedm.BaseHandler)`函数，`_on_danmaku`里面有触发问答的方式,比如弹幕里提到**白糖**,AI就会回复  
`if "白糖" in message.msg:`触发是这一段捏,可以多改改设定成只回复特定话题  
