import os
import openai
import time
import random

# 填写注册OpenAI接口账号时获取的 OpenAI API Key
openai.api_key = "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"

TEXT=['你是最漂亮的女孩，甚至比电影里的都漂亮。',
      '我想和你发射爱的箭矢来兑现我对你的感情。',
      '搞不清关系吗？天上的星星陪伴月亮，而我陪伴你。',
      '花开一半，只为你着迷。',
      '有你相伴，这些风雨都变成情话。',
      '如果有一个时间机器，我一定要带你回到曾经……',
      '爱上你，让我知道什么是幸福。',
      '表面上的正经可以隐藏不住我内心的暧昧。',
      '今天我爱你，明天我也会爱你，大后天也爱，一直到永远。',
      '常常想，把你拥入怀中，紧紧抱住你，一起走完这段旅程。',
      '和你在一起的所有时光都灿烂耀眼，因为天气好，因为天气不好，因为天气正好。',
      '日出东方却落于西”翻译过来的意思是我爱你有开始就没有结束',
      '我想给你很多东西，比如，被理解、被信任、被支持 ，最想给你的，是偏爱。',
      '每一次看你，我都害怕我看错了，但最后看到你笑容，我才发现，我没有看错，你就是我想要的！',
      '假如岁月可以倒流，我愿意把和你在一起的时光随心所欲！',
      '我会把每一份情感都放在你梦寐以求的地方！',
      '你是我心里最美的音符，永远都不会消逝！'
      ]
# 打印爱心图案
def print_love():
    myData = "love"
    for char in myData.split():
        allChar = [random.choice(TEXT)]
        for y in range(12, -12, -1):
            lst = []
            lst_con = ''
            for x in range(-30, 30):
                formula = ((x * 0.05) ** 2 + (y * 0.1) ** 2 - 1) ** 3 - (x * 0.05) ** 2 * (y * 0.1) ** 3
                if formula <= 0:
                    lst_con += char[(x) % len(char)]
                else:
                    lst_con += ' '
            lst.append(lst_con)
            allChar += lst
        print('\n'.join(allChar))
        time.sleep(1)


# 提问
def chat(issue):
    # 访问OpenAI接口
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=issue,
        temperature=0.9,
        max_tokens=4000,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6
    )

    # 返回信息
    resText = response.choices[0].text
    return resText


if __name__ == '__main__':
    try:
        print_love()
        while True:
            issue = input('请可爱的小申开始提问叭：')
            if issue:
                print('小马的程序正在疯狂运转嗷，请等待...\r\n')
                txt = chat(issue)
                print(txt)
                r = input('继续宠幸：0,残忍拒绝：1 \r\n')
                if r == '0':
                    continue
                if r == '1':
                    break
            else:
                print('输入问题再按回车嗷，小宝贝！\r\n')
                continue
        input('输入任意键退出...')
    except Exception as e:
        print('程序出错啦，快联系小马同学来解决叭！')
        print(e)
        input('输入任意键退出...')
