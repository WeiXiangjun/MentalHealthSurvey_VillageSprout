"""家长问卷批量复算入口。"""
import argparse
import pandas as pd
from analysis_common import read_matrix, require_columns, numeric_summary, frequency_table, wilcoxon_pair, spearman_pair, write_outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output_dir")
    args = parser.parse_args()
    data = read_matrix(args.input)
    numeric = ["P_Q1_UNDERSTAND", "P_Q2_SATISFY", "P_Q5_IMPORTANCE", "P_Q6_KNOWLEDGE"]
    categorical = ["P_Q3_INTENSITY", "P_Q4_EVAL", "P_Q7_BIN"]
    require_columns(data, numeric + categorical)
    tests = pd.DataFrame([
        wilcoxon_pair(data, "P_Q1_UNDERSTAND", "P_Q2_SATISFY"),
        wilcoxon_pair(data, "P_Q6_KNOWLEDGE", "P_Q5_IMPORTANCE"),
        spearman_pair(data, "P_Q1_UNDERSTAND", "P_Q2_SATISFY"),
        spearman_pair(data, "P_Q3_INTENSITY", "P_Q2_SATISFY"),
    ])
    write_outputs(args.output_dir,
                  描述统计=numeric_summary(data, numeric + categorical[:2]),
                  频数分布=frequency_table(data, numeric + categorical),
                  统计检验=tests)


if __name__ == "__main__":
    main()

