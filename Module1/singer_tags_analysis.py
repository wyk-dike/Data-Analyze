from matplotlib import pyplot as plt


class SingerTagsAnalysis:
    def __init__(self, df):
        self.df = df

    def analyze(self):
        tag_analysis = self.df.groupby("tab").agg(
            tag_usage=("tab", "count")
        ).sort_values("tag_usage", ascending=False).head(10)
        print(tag_analysis)
        self.visualize(tag_analysis)

    @staticmethod
    def visualize(tag_analysis):
        colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#CC99FF', '#FFB266', '#85E085', '#B3B3FF', '#FF9966',
                  '#E6E600']
        tag_analysis.plot(kind="pie",y='tag_usage', figsize=(8, 8), autopct='%1.1f%%', legend=False, colors=colors)
        plt.title("The singer's favorite music genre", fontsize=16)
        plt.ylabel('')
        plt.show()
        # tag_analysis.plot(kind='bar', figsize=(10, 6), color='blue')
        # plt.title("The singer's favorite music genre", fontsize=16)
        # plt.xlabel("Music genre", fontsize=12)
        # plt.ylabel("Number of tags", fontsize=12)
        # plt.xticks(rotation=45)
        # plt.grid(True, axis='y', linestyle='--', alpha=0.7)
        # plt.show()
