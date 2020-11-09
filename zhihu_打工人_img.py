# -*- coding: UTF-8 -*-
import os
import urllib.request
import requests
import json
import re
import time

class spiderDemo:
    def __init__(self):
        # self.link_weibo = "https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D%23%E6%89%93%E5%B7%A5%E4%BA%BA%E8%AF%AD%E5%BD%95%23&page_type=searchall"
        self.link_zhihu = "https://api.zhihu.com/search_v3?advert_count=0&correction=1&lc_idx=0&limit=20&offset={}&q=打工人表情包"
        self.link_zhihu_index = "https://www.zhihu.com/api/v4/search_v3?t=general&q={}&correction=1&offset=0&limit=20&lc_idx=0&show_all_topics=0"
        # link = "https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D%23%E6%89%93%E5%B7%A5%E4%BA%BA%E8%AF%AD%E5%BD%95%23&page_type=searchall&page=2"
        self.headers = {
            'accept': '*/*',
            # 'accept-encoding': 'gzip, deflate, br',
            # 'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cookie': '',
            'referer': 'https://www.zhihu.com/search?type=content&q=%E6%89%93%E5%B7%A5%E4%BA%BA%E8%A1%A8%E6%83%85%E5%8C%85',
            # 'sec-fetch-dest': 'empty',
            # 'sec-fetch-mode': 'cors',
            # 'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
            # 'x-ab-param': 'tp_topic_style=0;zr_rec_answer_cp=open;pf_profile2_tab=0;se_ffzx_jushen1=0;qap_question_author=0;ls_video_commercial=0;li_video_section=1;li_svip_tab_search=1;tp_clubhyb=1;pf_noti_entry_num=2;li_pl_xj=0;li_catalog_card=1;tp_zrec=1;zr_intervene=0;li_car_meta=1;qap_question_visitor= 0;top_test_4_liguangyi=1;tp_contents=1;pf_creator_card=1;zw_sameq_sorce=999;tsp_hotlist_ui=3;zr_slotpaidexp=8;pf_adjust=1;li_edu_page=old;li_vip_verti_search=0;li_yxzl_new_style_a=1;li_sp_mqbk=0;zr_sim3=0;se_col_boost=1;zr_expslotpaid=2;tp_dingyue_video=0;li_paid_answer_exp=0;li_panswer_topic=0',
            # 'x-ab-pb': 'CkAPC9wLhgsnCuEL4Au0CtcLJQqbC9cKAQu1C1gLrAtSC0wLzwsHDJoL5Ar0C2ALlgsSC7kLAAzzCw8M7Ao+C0sLEiAAAAEGAQAAAAUAAQAAAAABAAsAAAAAAAAAAAEBAAEBAQ==',
            # 'x-api-version': '3.0.91',
            # 'x-app-za': 'OS=Web',
            # 'x-requested-with': 'fetch',
            'x-zse-83': '3_2.0',
            'x-zse-86': '1.0_a8YqnhU0FBtpoTF8YM2qHgXqUwFXbMt0BTF0bTUqoX2p'
        }
        self.filePath = './demo_zhihu.txt'
        self.curl = requests.Session()
        # self.remote()
        self.test1(kw="打工人表情包")

    def test1(self, kw):
        link = self.link_zhihu_index.format(kw)
        response = requests.get(link, headers=self.headers)
        print(response.text)
        # res = requests.get(url=link, headers=self.headers)
        # print(res.text)

    def test(self, keywords):
        img_list = []
        sum = 0
        for i in range(1, 5):
            try:
                link = self.link_zhihu.format(sum, keywords)
                response = self.curl.get(url=link, headers=self.headers)
                res_json = json.loads(response.text)
                res_json_data = res_json['data']
                for data_list in res_json_data:
                    if 'object' not in data_list.keys():
                        continue
                    if 'thumbnail_info' not in data_list['object'].keys():
                        continue
                    if 'thumbnails' not in data_list['object']['thumbnail_info'].keys():
                        continue
                    data_list_info = data_list['object']['thumbnail_info']['thumbnails']
                    if not data_list_info is None:
                        for info in data_list_info:
                            if 'url' in info.keys():
                                img_list.append(info['url'])
                                self.downloadImg(info['url'])
                print(img_list)
                sum += 20
            except Exception as e:
                print(e)

    def getInfo(self, link):
        try:
            data = self.curl.get(url=link, headers=self.headers, timeout=5)
            staus = data.raise_for_status()
        except:
            return False

        res = json.loads(data.text)
        lists = res['data']['cards']
        textLists = ''
        for list in lists:
            if 'mblog' in list.keys():
                # print(list['mblog']['raw_text'])
                text = list['mblog']['raw_text']
                strInfo = re.compile(r'#.*?#')
                strInfo2 = re.compile(r'\[.*?\]')
                text = strInfo.sub('', text).strip()
                text = strInfo2.sub('', text).strip()
                text = text.replace('\n\n', '\n').replace('\u200b', '')
                print(text)
                textLists = textLists + text
            else:
                pass
        return textLists + '\n'

    def remote(self):
        text_lists = []
        for i in range(1, 10):
            print('page=' + str(i))
            link = self.link
            if i > 1:
                link = link + '&page=' + str(i)
            text = self.getInfo(link)
            text_lists.append(text)
            time.sleep(1)
        print(text_lists)
        with open(self.filePath, 'a+', encoding='utf-8') as file:
            file.writelines(text_lists)

    def downloadImg(self, img_link):
        (filepath, tempfilename) = os.path.split(img_link)
        (filename, extension) = os.path.splitext(tempfilename)
        filename = './demoImg/' + filename + '.jpg'
        # 下载图片，并保存到文件夹中
        urllib.request.urlretrieve(img_link, filename=filename)



spiderDemo()
