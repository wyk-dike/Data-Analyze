import pandas as pd
import matplotlib.pyplot as plt

class TopArtistsAnalysis:
    def __init__(self, df):
        self.df = df

    def analyze(self):
        top_founder = self.df.groupby('founder')['play_count'].sum().nlargest(10)
        # print(top_founder)
        self.visualize(top_founder)

    @staticmethod
    def visualize(top_founder):
        total = top_founder.sum()
        print(total)

        ax = top_founder.plot(kind='bar', figsize=(10, 6), color='coral')
        plt.title("Most popular artists", fontsize=16)
        plt.xlabel("Artist", fontsize=12)
        plt.ylabel("Number of plays", fontsize=12)
        plt.xticks(rotation=45)

        # 在每个柱状图顶部标注数值
        for index, value in enumerate(top_founder):
            plt.text(index, value + 5, str(value), ha='center', fontsize=10)

            # 调整底部边距，确保文本不会被裁剪
            # plt.subplots_adjust(bottom=0.2)

            # 在图表下方显示总和
            plt.text(
                0.01, 1.05,  # 坐标为 (x, y)，以图表范围为单位
                f"Total Play Counts: {total}",
                ha='center', fontsize=12, color='black', transform=ax.transAxes
            )
        plt.grid(True, axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()
