# 高影响力歌单分析

import ConnectDB
import pandas as pd
import matplotlib.pyplot as plt

class MusicInfluence:
    def __init__(self):
        self.connectDB = ConnectDB.ConnectDB()

    def getData(self):
        self.connectDB.createConnect()
        result = self.connectDB.selectAll()
        self.connectDB.closeConnect()
        return result  # json

    def run(self):
        dataList = self.getData()
        DF = pd.DataFrame(dataList)

        # 计算影响力的简单指标 (播放量+收藏量)
        DF['influence_score'] = DF['play_count'] + DF['save_count'].clip(lower=0)

        # 筛选出 影响力 排名前10的歌单
        topInfluenceScore = DF.sort_values(by='influence_score', ascending=False).head(10)

        # 绘制影响力柱状图
        # x轴：歌单名称
        # y轴：影响力指标
        # 找到一个支持中文的字体（如 SimHei）
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 设置字体样式
        plt.rcParams['axes.unicode_minus'] = False  # 避免负号显示异常
        # plt.rcParams['axes.formatter.useoffset'] = False
        plt.figure(figsize=(20, 16))
        bar = plt.bar(topInfluenceScore['name'], topInfluenceScore['influence_score'], color='salmon')
        # 显示数字在每个柱子上
        plt.bar_label(bar, label_type='edge', fmt='%.0f')

        plt.title("Список самых популярных песен (Top 10)")
        plt.xlabel("Название списка песен")
        plt.ylabel("Показатели воздействия")
        plt.xticks(rotation=45)
        plt.show()



# MusicInfluence().run()