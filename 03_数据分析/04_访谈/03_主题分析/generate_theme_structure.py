"""根据访谈主题整合表生成主题结构图。"""

from pathlib import Path
import textwrap

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch
import pandas as pd


UNIT = Path(__file__).resolve().parents[1]
WORKBOOK = UNIT / "访谈正式分析.xlsx"
OUTPUT = Path(__file__).resolve().parent / "图"
OUTPUT.mkdir(parents=True, exist_ok=True)
font_manager.fontManager.addfont(r"C:\Windows\Fonts\NotoSansSC-VF.ttf")
plt.rcParams.update({"font.family": "Noto Sans SC", "axes.unicode_minus": False})


def wrap(text: str, width: int) -> str:
    return "\n".join(textwrap.wrap(str(text), width=width, break_long_words=True))


def main() -> None:
    themes = pd.read_excel(WORKBOOK, sheet_name="主题整合结果", header=1).dropna(subset=["主题编号"])
    fig, ax = plt.subplots(figsize=(12, 7.4), constrained_layout=True)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis("off")
    ax.text(6, 7.55, "学校心理健康教育访谈主题结构", ha="center", va="center",
            fontsize=18, fontweight="bold", color="#1F2937")
    ax.text(6, 7.05, "两位编码员平行独立编码后，经对照与主题整合形成", ha="center", va="center",
            fontsize=10.5, color="#5B6470")

    center = FancyBboxPatch((4.05, 3.0), 3.9, 1.25, boxstyle="round,pad=0.05,rounding_size=0.12",
                            facecolor="#17365D", edgecolor="none")
    ax.add_patch(center)
    ax.text(6, 3.63, "学校心理健康教育的\n现实运行与支持边界", ha="center", va="center",
            color="white", fontsize=15, fontweight="bold")

    positions = [(0.45, 5.15), (4.05, 5.15), (7.65, 5.15), (1.95, 0.45), (6.05, 0.45)]
    colors = ["#4C78A8", "#72A0C1", "#4F9D8A", "#D29B4B", "#C76B5D"]
    for row, (x, y), color in zip(themes.to_dict("records"), positions, colors):
        w, h = 3.9, 1.35
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05,rounding_size=0.10",
                             facecolor=color, edgecolor="white", linewidth=1.2, alpha=0.96)
        ax.add_patch(box)
        ax.text(x + w / 2, y + 0.93, f"{row['主题编号']}  {row['主主题']}", ha="center", va="center",
                color="white", fontsize=11.5, fontweight="bold")
        ax.text(x + w / 2, y + 0.38, wrap(row["包含的二级范畴"], 23), ha="center", va="center",
                color="white", fontsize=8.4)
        start_x = x + w / 2
        start_y = y if y > 3 else y + h
        end_y = 4.25 if y > 3 else 3.0
        ax.annotate("", xy=(6, end_y), xytext=(start_x, start_y),
                    arrowprops=dict(arrowstyle="-|>", color="#89929D", lw=1.1,
                                    connectionstyle="arc3,rad=0.05"), zorder=0)

    ax.text(0.45, 0.08, "注：主题结构图用于展示主题间关系，不以词频替代质性解释。", fontsize=9, color="#606770")
    for suffix in ("png", "svg"):
        fig.savefig(OUTPUT / f"访谈主题结构图.{suffix}", dpi=600 if suffix == "png" else None,
                    bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
