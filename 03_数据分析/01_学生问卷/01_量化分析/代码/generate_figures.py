"""根据学生问卷正式分析工作簿生成Nature风格量化图。"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager

UNIT = Path(__file__).resolve().parents[2]
WORKBOOK = UNIT / "学生问卷正式分析.xlsx"
OUTPUT = Path(__file__).resolve().parent.parent / "图"
OUTPUT.mkdir(parents=True, exist_ok=True)

font_manager.fontManager.addfont(r"C:\Windows\Fonts\NotoSansSC-VF.ttf")
plt.rcParams.update({"font.family": "Noto Sans SC", "axes.unicode_minus": False})
CN = font_manager.FontProperties(fname=r"C:\Windows\Fonts\NotoSansSC-VF.ttf")
EN = font_manager.FontProperties(fname=r"C:\Windows\Fonts\times.ttf")
PALETTE = ["#2E5AAC", "#4CC9F0", "#D9D9D9", "#FFB000", "#D1495B"]

def style(ax):
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(width=.8, length=3, labelsize=9)
    ax.grid(axis="x", color="#E6E6E6", linewidth=.6, zorder=0)

freq = pd.read_excel(WORKBOOK, sheet_name="量化_频数分布", header=1).dropna(subset=["变量"])
order = ["了解程度", "满意程度"]
labels = {"了解程度":"了解程度", "满意程度":"满意程度"}
fig, ax = plt.subplots(figsize=(8.6, 3.1), constrained_layout=True)
left = [0.0] * len(order)
for score in range(1, 6):
    values = []
    for variable in order:
        row = freq[(freq["变量"] == variable) & (freq["编码"] == score)]
        values.append(float(row["比例"].iloc[0]) if len(row) else 0)
    ax.barh(range(len(order)), values, left=left, color=PALETTE[score-1], height=.56,
            label=str(score), edgecolor="white", linewidth=.6)
    left = [a+b for a,b in zip(left, values)]
ax.set_yticks(range(len(order)), [labels[x] for x in order], fontproperties=CN)
ax.set_xlim(0,1); ax.set_xticks([0,.25,.5,.75,1], ["0","25","50","75","100"])
ax.set_xlabel("回答比例（%）", fontproperties=CN)
ax.set_title("学生对学校心理健康教育的了解与满意分布", loc="left", fontproperties=CN, fontsize=12)
ax.legend(title="评分", ncol=1, frameon=False, bbox_to_anchor=(1.01,.5), loc="center left",
          prop=CN, title_fontproperties=CN, borderaxespad=0)
style(ax)
for ext in ("png","svg"): fig.savefig(OUTPUT / f"图1_了解与满意分布.{ext}", dpi=600, bbox_inches="tight")
plt.close(fig)

desc = pd.read_excel(WORKBOOK, sheet_name="量化_描述统计", header=1)
groups = desc.iloc[:3, 10:20].dropna(subset=["年级编码"])
fig, ax = plt.subplots(figsize=(7.8,3.8), constrained_layout=True)
x = range(len(groups)); width=.34
ax.bar([i-width/2 for i in x], groups["了解均值"], width, color="#2E5AAC", label="了解程度")
ax.bar([i+width/2 for i in x], groups["满意均值"], width, color="#D1495B", label="满意程度")
ax.errorbar([i-width/2 for i in x], groups["了解均值"], yerr=groups["了解SD"], fmt="none", ecolor="#222222", capsize=3, lw=.8)
ax.errorbar([i+width/2 for i in x], groups["满意均值"], yerr=groups["满意SD"], fmt="none", ecolor="#222222", capsize=3, lw=.8)
ax.set_xticks(list(x), [f"编码组{g}" for g in groups["年级编码"].astype(str)], fontproperties=CN)
ax.set_ylim(0,5.25); ax.set_ylabel("平均分", fontproperties=CN)
ax.set_title("匿名年级编码组的了解与满意程度", loc="left", fontproperties=CN, fontsize=12)
ax.legend(frameon=False, prop=CN, bbox_to_anchor=(1.01,.5), loc="center left", borderaxespad=0)
style(ax)
for ext in ("png","svg"): fig.savefig(OUTPUT / f"图2_年级编码组比较.{ext}", dpi=600, bbox_inches="tight")
plt.close(fig)
