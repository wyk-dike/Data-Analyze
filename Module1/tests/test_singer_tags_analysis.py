import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from lishunyao.singer_tags_analysis import SingerTagsAnalysis  # 假设类文件名为 singer_tags_analysis.py

# 测试 analyze 方法
def test_singer_tags_analysis():
    # 创建一个测试的 DataFrame 数据
    data = {
        "tab": ["Pop", "Rock", "Jazz", "Pop", "Jazz", "Rock", "Pop", "Rock", "Jazz", "Classical"],
    }
    df = pd.DataFrame(data)

    # 使用 MagicMock 替代 visualize 方法
    with patch.object(SingerTagsAnalysis, 'visualize', return_value=None) as mock_visualize:
        analysis = SingerTagsAnalysis(df)
        analysis.analyze()

        # 检查 visualize 是否被调用
        mock_visualize.assert_called_once()

        # 验证 tag_analysis 的内容
        expected_data = {
            "tag_usage": [3, 3, 3, 1],
        }
        expected_index = ["Jazz", "Pop", "Rock", "Classical"]  # 修复顺序以匹配 analyze 输出
        expected_tag_analysis = pd.DataFrame(expected_data, index=expected_index)
        expected_tag_analysis.index.name = "tab"  # 确保索引名称也匹配

        # 验证 visualize 方法接收到的参数与期望值一致
        pd.testing.assert_frame_equal(
            mock_visualize.call_args[0][0],  # 从 mock 中获取传递的参数
            expected_tag_analysis
        )

# 测试 visualize 方法
def test_visualize():
    # 创建一个测试的 tag_analysis 数据
    tag_analysis = pd.DataFrame({
        "tag_usage": [50, 30, 20],
    }, index=["Pop", "Rock", "Jazz"])

    # 使用 MagicMock 替代 plot 和 show 方法
    with patch("pandas.DataFrame.plot", return_value=MagicMock()) as mock_plot:
        with patch("matplotlib.pyplot.show", return_value=None) as mock_show:
            SingerTagsAnalysis.visualize(tag_analysis)

            # 验证 plot 是否被调用
            mock_plot.assert_called_once()

            # 验证 show 是否被调用
            mock_show.assert_called_once()