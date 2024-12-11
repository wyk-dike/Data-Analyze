from matplotlib import pyplot as plt


class AudienceTagsAnalysis:
    def __init__(self, df):
        self.df = df

    def analyze(self):
        tag_analysis = self.df.groupby("tab").agg(
            total_play_count=("play_count", "sum")
        ).sort_values("total_play_count", ascending=False).head(10)

        self.visualize(tag_analysis)

    @staticmethod
    def visualize(tag_analysis):
        tag_analysis.plot(kind='pie', y='total_play_count', figsize=(8, 8), autopct='%1.1f%%', legend=False, colors=plt.cm.Paired.colors)
        plt.title("The audience's favorite music genre", fontsize=16)
        plt.ylabel('')
        plt.show()
