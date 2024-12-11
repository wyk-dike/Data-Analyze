from matplotlib import pyplot as plt, font_manager

from database import Database
from data_processing import DataProcessor
from top_artists_analysis import TopArtistsAnalysis
from musician_stats_analysis import MusicianStatsAnalysis
from audience_tags_analysis import AudienceTagsAnalysis
from singer_tags_analysis import SingerTagsAnalysis

if __name__ == "__main__":
    # 设置中文字体
    font = font_manager.FontProperties(fname='C:/Windows/Fonts/simhei.ttf')  # Windows 下的黑体字体路径
    plt.rcParams['font.family'] = font.get_name()

    db_config = {
        'host': 'localhost',
        'port': 5432,
        "dbname": "music_info",
        "user": "postgres",
        "password": "123456",
    }

    db = Database(db_config)
    table_name = 'music_info_json_table'
    df = db.fetch_data(table_name)

    # 数据预处理
    processor = DataProcessor()
    df_parsed = processor.parse_json_column(df, 'music_info_json')
    df_exploded = processor.explode_column(df_parsed, 'tab')

    # 数据分析与可视化
    TopArtistsAnalysis(df_parsed).analyze()
    MusicianStatsAnalysis(df_parsed).analyze()
    AudienceTagsAnalysis(df_exploded).analyze()
    SingerTagsAnalysis(df_exploded).analyze()
