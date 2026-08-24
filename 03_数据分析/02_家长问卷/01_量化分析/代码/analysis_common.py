"""三类问卷共用的可复现分析函数。"""
from __future__ import annotations

from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy import stats


def read_matrix(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    raise ValueError("输入必须是 .xlsx、.xls 或 .csv 文件。")


def require_columns(data: pd.DataFrame, columns: list[str]) -> None:
    missing = [name for name in columns if name not in data.columns]
    if missing:
        raise ValueError(f"缺少必要字段：{', '.join(missing)}")


def numeric_summary(data: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    rows = []
    for name in columns:
        values = pd.to_numeric(data[name], errors="coerce").dropna()
        rows.append({
            "变量": name,
            "有效n": int(values.size),
            "均值": values.mean(),
            "标准差": values.std(ddof=1),
            "中位数": values.median(),
            "最小值": values.min(),
            "最大值": values.max(),
        })
    return pd.DataFrame(rows)


def frequency_table(data: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    blocks = []
    for name in columns:
        counts = data[name].value_counts(dropna=False).rename_axis("取值").reset_index(name="人数")
        counts.insert(0, "变量", name)
        counts["比例"] = counts["人数"] / len(data)
        blocks.append(counts)
    return pd.concat(blocks, ignore_index=True)


def wilcoxon_pair(data: pd.DataFrame, left: str, right: str) -> dict:
    paired = data[[left, right]].apply(pd.to_numeric, errors="coerce").dropna()
    if paired.empty or np.allclose(paired[left], paired[right]):
        return {"变量1": left, "变量2": right, "n": len(paired), "W": np.nan, "p": np.nan, "说明": "无可检验差异或无有效配对"}
    result = stats.wilcoxon(paired[left], paired[right], zero_method="wilcox")
    return {"变量1": left, "变量2": right, "n": len(paired), "W": result.statistic, "p": result.pvalue, "说明": "Wilcoxon配对符号秩检验"}


def spearman_pair(data: pd.DataFrame, left: str, right: str) -> dict:
    paired = data[[left, right]].apply(pd.to_numeric, errors="coerce").dropna()
    rho, p = stats.spearmanr(paired[left], paired[right])
    return {"变量1": left, "变量2": right, "n": len(paired), "rho": rho, "p": p, "说明": "Spearman等级相关"}


def kruskal_groups(data: pd.DataFrame, outcome: str, group: str) -> dict:
    frame = data[[outcome, group]].copy()
    frame[outcome] = pd.to_numeric(frame[outcome], errors="coerce")
    frame = frame.dropna()
    groups = [part[outcome].to_numpy() for _, part in frame.groupby(group) if len(part)]
    if len(groups) < 2:
        return {"因变量": outcome, "分组变量": group, "H": np.nan, "p": np.nan, "说明": "有效组数不足"}
    result = stats.kruskal(*groups)
    return {"因变量": outcome, "分组变量": group, "H": result.statistic, "p": result.pvalue, "说明": "Kruskal-Wallis检验"}


def write_outputs(output_dir: str | Path, **tables: pd.DataFrame) -> None:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(output_dir / "analysis_outputs.xlsx", engine="openpyxl") as writer:
        for name, table in tables.items():
            table.to_excel(writer, sheet_name=name[:31], index=False)
    metadata = {"tables": list(tables), "note": "由指定输入数据、变量配置和统计方法生成；输出应与正式分析工作簿逐项核对。"}
    (output_dir / "run_metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
