import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from lishunyao.audience_tags_analysis import AudienceTagsAnalysis

# 测试 analyze 方法

def test_audience_tags_analysis():
    # 创建测试数据
    data = {
        "tab": ["Rock", "Pop", "Jazz", "Rock", "Pop", "Classical"],
        "play_count": [150, 200, 100, 250, 300, 50],
    }
    df = pd.DataFrame(data)

    # 创建 AudienceTagsAnalysis 实例
    analysis = AudienceTagsAnalysis(df)

    # 使用 mock 检查 visualize 是否被调用
    with patch.object(AudienceTagsAnalysis, 'visualize', wraps=AudienceTagsAnalysis.visualize) as mock_visualize:
        analysis.analyze()

        # 检查 visualize 是否被调用一次
        mock_visualize.assert_called_once()

        # 获取 visualize 的参数
        args, kwargs = mock_visualize.call_args
        tag_analysis = args[0]

        # 验证 tag_analysis 是否正确
        expected_tag_analysis = df.groupby("tab").agg(
            total_play_count=("play_count", "sum")
        ).sort_values("total_play_count", ascending=False).head(10)
        pd.testing.assert_frame_equal(tag_analysis, expected_tag_analysis)


def test_visualize():
    # 创建一个测试的 tag_analysis 数据
    tag_analysis = pd.DataFrame({
        "total_play_count": [500, 400, 300],
    }, index=["Pop", "Rock", "Jazz"])

    # 使用 MagicMock 替代 plot 和 show 方法
    with patch("pandas.DataFrame.plot", return_value=MagicMock()) as mock_plot:
        with patch("matplotlib.pyplot.show", return_value=MagicMock()) as mock_show:
            AudienceTagsAnalysis.visualize(tag_analysis)

            # 验证 plot 是否被调用
            mock_plot.assert_called_once()

            # 验证 show 是否被调用
            mock_show.assert_called_once()