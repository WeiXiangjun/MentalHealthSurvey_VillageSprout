"""基于编码员1的逐题编码生成学生开放题展示图，并排除非实质性代码。"""

from collections import Counter
from pathlib import Path
import math
import re
import textwrap

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import font_manager


ROOT = Path(__file__).resolve().parents[3]
INPUT = ROOT / "学生问卷正式分析.xlsx"
OUTPUT = Path(__file__).resolve().parents[1] / "图"
FONT = Path(r"C:\Windows\Fonts\NotoSansSC-VF.ttf")
LOW = (0.70, 0.70, 0.70)
HIGH = (0.76, 0.05, 0.12)
EXCLUDED_CODES = {"无实质回答", "无明确期望", "其他/含义不明", "排除文本"}


def set_style() -> None:
    font_manager.fontManager.addfont(str(FONT))
    plt.rcParams.update({
        "font.family": "Noto Sans SC", "axes.unicode_minus": False,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.titleweight": "bold", "figure.dpi": 140,
    })


def split_codes(value: object) -> list[str]:
    if pd.isna(value):
        return []
    return [item.strip() for item in re.split(r"[；;、，,\n]+", str(value)) if item.strip()]


def code_counter(series: pd.Series) -> Counter:
    counter: Counter = Counter()
    for value in series:
        counter.update(code for code in split_codes(value) if code not in EXCLUDED_CODES)
    return counter


def code_color(value: int, maximum: int):
    t = (value / maximum) ** 0.55
    return tuple(a + (b - a) * t for a, b in zip(LOW, HIGH))


def save_wordcloud(counter: Counter, stem: str) -> None:
    if not counter:
        return
    items = counter.most_common(50)
    maximum = items[0][1]
    fig, ax = plt.subplots(figsize=(12, 7), dpi=150)
    ax.set_axis_off()
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    axes_box = ax.get_window_extent(renderer)
    placed = []
    for word, value in items:
        size = 18 + 70 * (value / maximum) ** 0.62
        for step in range(700):
            angle = step * 0.54
            radius = 0.012 * (step ** 0.68)
            x = 0.5 + radius * math.cos(angle)
            y = 0.5 + 0.62 * radius * math.sin(angle)
            if not (0.04 < x < 0.96 and 0.06 < y < 0.94):
                continue
            artist = ax.text(x, y, word, transform=ax.transAxes, ha="center", va="center",
                             fontsize=size, color=code_color(value, maximum), fontweight="bold")
            fig.canvas.draw()
            box = artist.get_window_extent(renderer).expanded(1.06, 1.12)
            if axes_box.contains(*box.get_points()[0]) and axes_box.contains(*box.get_points()[1]) \
                    and not any(box.overlaps(other) for other in placed):
                placed.append(box)
                break
            artist.remove()
    fig.savefig(OUTPUT / f"{stem}.png", dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def save_frequency(counter: Counter, stem: str) -> None:
    pd.DataFrame(counter.most_common(), columns=["编码", "频次"]).to_csv(
        OUTPUT / f"{stem}.csv", index=False, encoding="utf-8-sig"
    )


def save_theme_chart(items: list[tuple[str, str, Counter]]) -> None:
    fig, axes = plt.subplots(3, 1, figsize=(9.2, 10.2), constrained_layout=True)
    for ax, (_question, title, counter) in zip(axes, items):
        data = counter.most_common(10)
        labels = [textwrap.fill(name, 12) for name, _ in data][::-1]
        values = [value for _, value in data][::-1]
        max_value = max(values, default=1)
        colors = []
        for value in values:
            t = (value / max_value) ** 0.55
            colors.append(tuple(a + (b - a) * t for a, b in zip(LOW, HIGH)))
        ax.barh(labels, values, color=colors, height=0.62)
        ax.set_title(title, loc="left", fontsize=11)
        ax.set_xlabel("提及次数")
        ax.grid(axis="x", color="#E6E6E6", linewidth=0.6, zorder=0)
        ax.set_axisbelow(True)
        for index, value in enumerate(values):
            ax.text(value + max_value * 0.015, index, str(value), va="center", fontsize=8.5)
        ax.set_xlim(0, max_value * 1.13)
    for suffix in ("png", "svg"):
        fig.savefig(OUTPUT / f"学生开放题主题分布.{suffix}",
                    dpi=600 if suffix == "png" else None, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    set_style()
    records = pd.read_excel(INPUT, sheet_name="质性_编码员1逐条", header=1)
    specs = [
        ("Q3", "课程主题编码", "学生Q3：偏好课程主题", "学生_Q3_课程主题编码"),
        ("Q4", "活动编码", "学生Q4：偏好活动形式", "学生_Q4_活动形式编码"),
        ("Q5", "期望编码", "学生Q5：改进期望", "学生_Q5_改进期望编码"),
    ]
    items = []
    for question, column, title, stem in specs:
        counter = code_counter(records[column])
        save_frequency(counter, f"{stem}_频次")
        save_wordcloud(counter, f"{stem}_词云")
        items.append((question, title, counter))
    save_theme_chart(items)


if __name__ == "__main__":
    main()
