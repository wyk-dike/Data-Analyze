import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from matplotlib import pyplot as plt
from lishunyao.musician_stats_analysis import MusicianStatsAnalysis

# 测试 MusicianStatsAnalysis 的 analyze 方法
def test_musician_stats_analysis():
    # 创建一个测试数据框
    data = {
        'founder': ['Artist A', 'Artist B', 'Artist C', 'Artist A', 'Artist B', 'Artist D'],
        'play_count': [100, 200, 150, 300, 400, 250],
        'music_count': [10, 20, 15, 30, 40, 25]
    }
    df = pd.DataFrame(data)

    # 创建 MusicianStatsAnalysis 实例
    analysis = MusicianStatsAnalysis(df)

    # 使用 mock 来测试 visualize 是否被正确调用
    with patch.object(MusicianStatsAnalysis, 'visualize', wraps=MusicianStatsAnalysis.visualize) as mock_visualize:
        analysis.analyze()

        # 检查 visualize 是否被调用
        mock_visualize.assert_called_once()

        # 获取传递给 visualize 的参数
        args, kwargs = mock_visualize.call_args
        founder_stats = args[0]

        # 验证 founder_stats 是否正确
        expected_founder_stats = pd.DataFrame({
            'total_play_count': df.groupby('founder')['play_count'].sum(),
            'total_music_count': df.groupby('founder')['music_count'].sum()
        }).sort_values(by='total_play_count', ascending=False).head(10)
        pd.testing.assert_frame_equal(founder_stats, expected_founder_stats)

# 测试 visualize 方法
def visualize(founder_stats, use_tight_layout=True, show_plot=True):
    total = founder_stats['total_music_count'].sum()
    ax = founder_stats['total_music_count'].plot(kind='bar', figsize=(10, 6), color='coral')
    plt.title("Number of songs written by the most popular musicians", fontsize=16)
    plt.xlabel("Musicians", fontsize=12)
    plt.ylabel("Number of songs", fontsize=12)
    plt.xticks(rotation=45)

    # 在每个柱状图顶部标注数值
    for index, value in enumerate(founder_stats['total_music_count']):
        plt.text(index, value + 5, str(value), ha='center', fontsize=10)

    # 在图表下方显示总和
    plt.text(
        0.01, 1.05,
        f"Total Songs: {total}",
        ha='center', fontsize=12, color='black', transform=ax.transAxes
    )

    plt.grid(True, axis='y', linestyle='--', alpha=0.7)

    if use_tight_layout:
        plt.tight_layout()  # 调整布局避免文字被裁剪

    if show_plot:
        plt.show()