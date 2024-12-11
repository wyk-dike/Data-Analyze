# 统计不同年份和月份的歌单数量，绘制 时间序列图 和 柱状图。

import ConnectDB
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class DateAndCreation:
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
        # 转换 creation_date 为 datetime 格式
        DF['creation_date'] = pd.to_datetime(DF['creation_date'])

        # 按年份统计
        DF['year'] = DF['creation_date'].dt.year
        yearlyCounts = DF['year'].value_counts().sort_index()
        # 绘制年份柱状图
        plt.figure(figsize=(10, 6))
        ax = yearlyCounts.plot(kind='bar', color='skyblue')
        # 添加顶部数值
        for p in ax.patches:
            ax.annotate(f'{p.get_height():.0f}',  # 显示数值，格式为整数
                        (p.get_x() + p.get_width() / 2., p.get_height()),  # 放置位置：顶部中央
                        ha='center', va='center',  # 水平和垂直居中
                        fontsize=12, color='black', xytext=(0, 10), textcoords='offset points')  # 适当偏移
        plt.title("Количество созданных песенных листов (по годам)")
        plt.xlabel("Год")
        plt.ylabel("Количество песенных листов")
        plt.xticks(rotation=45)
        plt.show()

        # 按月份统计（跨年的月份分布）
        # 按年月分组，并将 'month' 转换为 datetime 类型（转换为该月的第一天）
        DF['month'] = DF['creation_date'].dt.to_period('M').dt.to_timestamp()
        monthlyCounts = DF['month'].value_counts().sort_index()
        # 绘制月份时间序列图
        plt.figure(figsize=(20, 8))
        pMonth = monthlyCounts.plot(kind='line', marker='o', linestyle='-', color='orange')
        pMonth.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # 设置年月格式
        # 设置 X 轴的刻度位置，使其每年一个刻度
        pMonth.xaxis.set_major_locator(mdates.YearLocator(1))  # 每年一个刻度
        pMonth.xaxis.set_minor_locator(mdates.MonthLocator())  # 每个月一个次刻度
        plt.title("Количество созданных песенных листов (по месяцам)")
        plt.xlabel("Месяц")
        plt.ylabel("Количество песенных листов")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.show()

        # print(DF[['creation_date','year','month']])




# DateAndCreation().run()