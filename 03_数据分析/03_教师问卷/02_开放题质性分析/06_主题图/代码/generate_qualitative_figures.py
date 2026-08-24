"""基于编码员1、按题号生成教师题内补充文本编码分布图。"""

from collections import Counter
from pathlib import Path
import textwrap

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import font_manager


ROOT = Path(__file__).resolve().parents[3]
INPUT = ROOT / "教师问卷正式分析.xlsx"
OUTPUT = Path(__file__).resolve().parents[1] / "图"
FONT = Path(r"C:\Windows\Fonts\NotoSansSC-VF.ttf")
LOW = (0.70, 0.70, 0.70)
HIGH = (0.76, 0.05, 0.12)
SPECS = [
    ("Q9", "任教科目补充"),
    ("Q14", "心理教师配置数量补充"),
    ("Q15", "心理学专业人数补充"),
    ("Q35", "教材版本补充"),
    ("Q43", "课时计算标准补充"),
    ("Q48", "危机干预流程补充"),
]


def set_style() -> None:
    font_manager.fontManager.addfont(str(FONT))
    plt.rcParams.update({
        "font.family": "Noto Sans SC", "axes.unicode_minus": False,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.titleweight": "bold", "figure.dpi": 140,
    })


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    set_style()
    records = pd.read_excel(INPUT, sheet_name="质性_编码员1逐条", header=1)
    panels = []
    for question, field in SPECS:
        subset = records[records["题号"] == question]
        counter = Counter(subset["编码员1代码"].dropna().astype(str))
        if not counter:
            continue
        panels.append((question, field, counter))

    fig, axes = plt.subplots(2, 3, figsize=(12.0, 6.8), constrained_layout=True)
    for ax, (question, field, counter) in zip(axes.flat, panels):
        data = counter.most_common(6)
        labels = [textwrap.fill(name, 10) for name, _ in data][::-1]
        values = [value for _, value in data][::-1]
        max_value = max(values, default=1)
        bar_colors = []
        for value in values:
            t = (value / max_value) ** 0.55
            bar_colors.append(tuple(a + (b - a) * t for a, b in zip(LOW, HIGH)))
        ax.barh(labels, values, color=bar_colors, height=0.58)
        ax.set_title(f"{question}  {field}", loc="left", fontsize=10)
        ax.set_xlabel("提及次数")
        ax.grid(axis="x", color="#E6E6E6", linewidth=0.6, zorder=0)
        ax.set_axisbelow(True)
        ax.set_xlim(0, max_value * 1.18)
        for index, value in enumerate(values):
            ax.text(value + max_value * 0.02, index, str(value), va="center", fontsize=8)
    for ax in axes.flat[len(panels):]:
        ax.axis("off")
    for suffix in ("png", "svg"):
        fig.savefig(OUTPUT / f"教师开放题主题分布.{suffix}",
                    dpi=600 if suffix == "png" else None, bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
