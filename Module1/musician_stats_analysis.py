import pandas as pd
from matplotlib import pyplot as plt


class MusicianStatsAnalysis:
    def __init__(self, df):
        self.df = df

    def analyze(self):
        founder_play_count = self.df.groupby('founder')['play_count'].sum()
        founder_music_count = self.df.groupby('founder')['music_count'].sum()
        founder_stats = pd.DataFrame({
            'total_play_count': founder_play_count,
            'total_music_count': founder_music_count
        }).sort_values(by='total_play_count', ascending=False).head(10)
        # print(founder_stats)
        self.visualize(founder_stats)

    @staticmethod
    def visualize(founder_stats):
        # 计算 total_music_count 的总和
        total = founder_stats['total_music_count'].sum()
        # print(total)
        ax = founder_stats['total_music_count'].plot(kind='bar', figsize=(10, 6), color='coral')
        plt.title("Number of songs written by the most popular musicians", fontsize=16)
        plt.xlabel("Musicians", fontsize=12)
        plt.ylabel("Number of songs", fontsize=12)
        plt.xticks(rotation=45)

        # 在每个柱状图顶部标注数值
        for index, value in enumerate(founder_stats['total_music_count']):
            plt.text(index, value + 5, str(value), ha='center', fontsize=10)

            # 调整底部边距，确保文本不会被裁剪
            # plt.subplots_adjust(bottom=0.2)

            # 在图表下方显示总和
            plt.text(
                0.01, 1.05,  # 坐标为 (x, y)，以图表范围为单位
                f"Total Songs: {total}",
                ha='center', fontsize=12, color='black', transform=ax.transAxes
            )

        plt.grid(True, axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()  # 调整布局避免文字被裁剪
        plt.show()
