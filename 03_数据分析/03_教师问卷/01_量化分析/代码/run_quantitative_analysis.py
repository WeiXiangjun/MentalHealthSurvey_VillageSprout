"""教师问卷批量描述入口；小样本默认不自动进行广泛推断检验。"""
import argparse
from analysis_common import read_matrix, require_columns, numeric_summary, frequency_table, write_outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output_dir")
    parser.add_argument("--numeric", nargs="*", default=[])
    parser.add_argument("--categorical", nargs="*", default=[])
    args = parser.parse_args()
    if not args.numeric and not args.categorical:
        raise ValueError("请按变量字典通过 --numeric 或 --categorical 指定至少一个字段。")
    data = read_matrix(args.input)
    require_columns(data, args.numeric + args.categorical)
    outputs = {"频数分布": frequency_table(data, args.numeric + args.categorical)}
    if args.numeric:
        outputs["描述统计"] = numeric_summary(data, args.numeric)
    write_outputs(args.output_dir, **outputs)


if __name__ == "__main__":
    main()

