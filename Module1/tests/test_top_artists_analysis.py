import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

from matplotlib import pyplot as plt

from lishunyao.top_artists_analysis import TopArtistsAnalysis

# 测试 TopArtistsAnalysis 的 analyze 方法
def test_top_artists_analysis():
    # 创建一个测试数据框
    data = {
        'founder': ['Artist A', 'Artist B', 'Artist C', 'Artist A', 'Artist B', 'Artist D'],
        'play_count': [100, 200, 150, 300, 400, 250]
    }
    df = pd.DataFrame(data)

    # 创建 TopArtistsAnalysis 实例
    analysis = TopArtistsAnalysis(df)

    # 使用 mock 来测试 visualize 是否被正确调用
    with patch.object(TopArtistsAnalysis, 'visualize', wraps=TopArtistsAnalysis.visualize) as mock_visualize:
        analysis.analyze()

        # 检查 visualize 是否被调用
        mock_visualize.assert_called_once()

        # 获取传递给 visualize 的参数
        args, kwargs = mock_visualize.call_args
        top_founder = args[0]

        # 验证 top_founder 是否正确
        expected_top_founder = df.groupby('founder')['play_count'].sum().nlargest(10)
        pd.testing.assert_series_equal(top_founder, expected_top_founder)

def visualize(top_founder, show_plot=True):
    total = top_founder.sum()
    print(total)

    ax = top_founder.plot(kind='bar', figsize=(10, 6), color='coral')
    plt.title("Most popular artists", fontsize=16)
    plt.xlabel("Artist", fontsize=12)
    plt.ylabel("Number of plays", fontsize=12)
    plt.xticks(rotation=45)

    for index, value in enumerate(top_founder):
        plt.text(index, value + 5, str(value), ha='center', fontsize=10)

    plt.text(
        0.01, 1.05,
        f"Total Play Counts: {total}",
        ha='center', fontsize=12, color='black', transform=ax.transAxes
    )
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)

    if show_plot:  # 控制是否调用这些方法
        plt.tight_layout()
        plt.show()