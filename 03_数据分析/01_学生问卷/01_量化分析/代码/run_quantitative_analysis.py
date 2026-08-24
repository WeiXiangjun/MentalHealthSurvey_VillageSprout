"""学生问卷量化分析入口。字段名需与数据预处理变量字典一致。"""
from pathlib import Path
import argparse
import pandas as pd
from analysis_common import read_matrix, require_columns, numeric_summary, frequency_table, wilcoxon_pair, spearman_pair, kruskal_groups, write_outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output_dir")
    args = parser.parse_args()
    data = read_matrix(args.input)
    needed = ["S_Q1_UNDERSTAND", "S_Q2_SATISFY", "S_GRADE"]
    require_columns(data, needed)
    tests = pd.DataFrame([
        wilcoxon_pair(data, "S_Q1_UNDERSTAND", "S_Q2_SATISFY"),
        spearman_pair(data, "S_Q1_UNDERSTAND", "S_Q2_SATISFY"),
        kruskal_groups(data, "S_Q1_UNDERSTAND", "S_GRADE"),
        kruskal_groups(data, "S_Q2_SATISFY", "S_GRADE"),
    ])
    write_outputs(args.output_dir,
                  描述统计=numeric_summary(data, needed[:2]),
                  频数分布=frequency_table(data, needed),
                  统计检验=tests)


if __name__ == "__main__":
    main()
