# -*- coding:utf-8 -*-
# __author__ = "shitou6"
import logging
import logging.config
import os
import time
import traceback
from bs4 import BeautifulSoup
import lxml


class spider:
    def __init__(self):
        self.movies_data = {}
        self.vip_data = []
        self.data_time=time.time()
        self.flag=False
        self.time_str=""
    def get_movie_text(self):
        """
        获取电影主页内容
        :return:
        """
        import AutoRequests
        url = "https://maoyan.com/cinema/12916?poi=4267320"
        return AutoRequests.GetUrlContent(url)

    def parse(self):
        if self.flag and time.time()-self.data_time < 300:
            print("跳过抓数据")
            return None
        self.flag=True
        self.data_time=time.time()
        self.time_str=time.strftime("%H:%M:%S",time.localtime(self.data_time))
        self.movies_data.clear()
        self.vip_data.clear()
        text = self.get_movie_text()
        soup = BeautifulSoup(text, 'lxml')
        # movies_id_list =  soup.find('div', class_="movie-list").find_all("div", class_="movie")
        movies = soup.find_all('div', class_='show-list')
        if not movies:
            file=open("error.html","w").write(text)
            print("error.html以写入")
        for each in movies:  # 遍历每个电影
            dates = each.find('div', class_="show-date").find_all('span', class_="date-item")
            movie_name = (each.find('h3', class_="movie-name").get_text())
            self.movies_data.setdefault(movie_name, {})
            movie_info = {
                "info": str(each.find("div", class_="movie-desc").text).replace("\n", " "),
                # "movie_id": movies_id_list[movies.index(each)]["data-movieid"]
            }
            self.movies_data[movie_name]['movie_info'] = movie_info
            plist = list(each.find_all('div', class_='plist-container'))
            self.movies_data[movie_name].setdefault("movies_day", [])
            for each_p in plist:  # 遍历每一天
                try:
                    movies_day = ("{}日".format(dates[plist.index(each_p)].get_text()))
                    temp_dict = {movies_day: []}
                    dangqi = each_p.find('tbody').find_all('tr')
                    for each_tr in dangqi:  # 遍历每一天的每一个档期
                        things = each_tr.find_all('td')
                        begin_time = things[0].find('span', class_='begin-time').get_text()
                        end_time = str(things[0].find('span', class_='end-time').get_text()).replace("散场", "")
                        banben = things[1].get_text()
                        ting = things[2].get_text().split('-')[0]
                        print_str = (
                            "开场：{}，结束：{}，类型：{}，大厅：{}".format(begin_time, end_time, banben, ting).replace("\n", ""))
                        # print(print_str)
                        temp_dict[movies_day].append(print_str)
                        if begin_time == "18:00":

                            self.vip_data.append("{} | {} | {}".format(movie_name, movies_day, print_str))
                    self.movies_data[movie_name]["movies_day"].append(temp_dict)
                except:
                    pass
        self.movies_data.setdefault('vip', self.vip_data)
        return None
    def find_movie(self, movie_name):
        self.parse()
        data = self.movies_data
        for key in data.keys():
            if movie_name in key or movie_name == key:
                dd = data[key]['movies_day']
                return dd
        return None

    def find_vip_movie(self):
        self.parse()
        data = self.movies_data
        now_data = data['vip']

        def return_item(ss):
            return int(ss.split('|')[1].split(' ')[2].split('月')[1][:-1])
        now_data.sort(key=return_item)
        return now_data

    def return_vip_movie_text(self):
        try:
            send_message=""
            now_data = self.find_vip_movie()
            send_message+="正在查询会员场电影信息"
            send_message = ""
            for each in now_data:
                ss = str(each).split('|')
                send_message += '电影名称:' + ss[0] + '\n'
                send_message += '时间:' + ss[1] + '\n'
                t1=ss[2].split('类型')[0].strip(" ")
                t2="类型"+ss[2].split('类型')[1]
                send_message+=t1+"\n"+t2+"\n"
                send_message += "---------------------------\n"
            send_message+="数据查询时间:"+self.time_str+"\n"
            send_message += "****打印完毕****"
            return send_message
        except:
            traceback.print_exc()
            return "会员查询功能出错QAQ"

    def return_movie_text(self,name):
        text=""
        data=self.find_movie(name)
        if data:
            for day in data[0:5]:
                for key,value in day.items():
                    text+="时间:{}\n".format(key)
                    for i in value:
                        text+=i+"\n"

                text+="---------------------------\n"
            text += "数据查询时间:" + self.time_str + "\n"
            return text
        else:
            return "没有查询到和《{}》相关的电影".format(name)



if __name__ == '__main__':
    a = spider()
    print(a.return_vip_movie_text())
    time.sleep(2)
    print(a.return_vip_movie_text())
    time.sleep(4)
    print(a.return_vip_movie_text())
    # print(a.return_movie_text("我和我的"))