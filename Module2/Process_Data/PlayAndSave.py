# 分析收藏-播放比率：计算收藏与播放的比率，筛选高质量歌单（播放量高但收藏低的歌单可能是“路人向”）。

import ConnectDB
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class PlayAndSave:
    def __init__(self):
        self.connectDB = ConnectDB.ConnectDB()

    def getData(self):
        self.connectDB.createConnect()
        result = self.connectDB.selectAll()
        self.connectDB.closeConnect()
        return result # json

    def run(self):
        dataList = self.getData()
        DF = pd.DataFrame(dataList)
        DF['save_play_ratio'] = DF['save_count'] / DF['play_count']
        # 将 0 和 -1 替换为 NaN
        DF['save_count'] = DF['save_count'].replace([0, -1], np.nan)
        DF['play_count'] = DF['play_count'].replace([0,-1], np.nan)
        # 删除含有 NaN 的行
        filteredDF = DF.dropna(subset=['save_count', 'play_count', 'save_play_ratio']) # 过滤后的数据
        # print(filteredDF[['save_count','play_count','save_play_ratio']])

        # 绘图
        # 可视化图片大小（英寸）
        plt.figure(figsize=(10, 6))
        # 散点图：播放量 vs 收藏量
        plt.scatter(
            filteredDF['play_count'],
            filteredDF['save_count'],
            c=filteredDF['save_play_ratio'],
            cmap='coolwarm',
            vmin=0.0015,
            vmax=0.015,
            alpha=0.6,
            edgecolors="w",
            s=30
        )
        plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0f}'))  # 设置 x 轴为常规数字格式
        # 添加颜色条
        plt.colorbar(label='Соотношение количества сохранений и воспроизведений')
        # 添加标签和标题
        plt.xlabel('Количество воспроизведений музыки')
        plt.ylabel('Количество сохранений музыки')
        plt.title('Связь между количеством сохранений и количеством воспроизведений')
        # 显示图形
        plt.tight_layout()
        plt.show()

# PlayAndSave().run()