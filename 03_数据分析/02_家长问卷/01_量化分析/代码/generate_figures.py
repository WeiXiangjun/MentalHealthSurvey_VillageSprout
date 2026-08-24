"""根据家长问卷正式分析工作簿生成Nature风格量化图。"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager

UNIT = Path(__file__).resolve().parents[2]
WORKBOOK = UNIT / "家长问卷正式分析.xlsx"
OUTPUT = Path(__file__).resolve().parent.parent / "图"
OUTPUT.mkdir(parents=True, exist_ok=True)
font_manager.fontManager.addfont(r"C:\Windows\Fonts\NotoSansSC-VF.ttf")
plt.rcParams.update({"font.family": "Noto Sans SC", "axes.unicode_minus": False})
CN = font_manager.FontProperties(fname=r"C:\Windows\Fonts\NotoSansSC-VF.ttf")
PALETTE = ["#2E5AAC", "#4CC9F0", "#D9D9D9", "#FFB000", "#D1495B"]

def style(ax):
    ax.spines[["top","right"]].set_visible(False)
    ax.grid(axis="x", color="#E6E6E6", linewidth=.6, zorder=0)
    ax.tick_params(width=.8, length=3, labelsize=9)

freq = pd.read_excel(WORKBOOK, sheet_name="量化_频数分布", header=1).dropna(subset=["变量"])
order = ["了解学校心理教育","满意学校心理教育","家长心理知识","重视子女心理"]
short = ["了解学校工作","满意学校工作","家长心理知识","重视子女心理"]
fig, ax = plt.subplots(figsize=(8.8,4.2), constrained_layout=True); left=[0.0]*len(order)
for score in range(1,6):
    values=[]
    for variable in order:
        row=freq[(freq["变量"]==variable)&(freq["编码"]==score)]
        values.append(float(row["比例"].iloc[0]) if len(row) else 0)
    ax.barh(range(len(order)), values, left=left, color=PALETTE[score-1], height=.58,
            label=str(score), edgecolor="white", linewidth=.6)
    left=[a+b for a,b in zip(left,values)]
ax.set_yticks(range(len(order)),short,fontproperties=CN); ax.invert_yaxis()
ax.set_xlim(0,1); ax.set_xticks([0,.25,.5,.75,1],["0","25","50","75","100"])
ax.set_xlabel("回答比例（%）",fontproperties=CN)
ax.set_title("家长认知、评价与重视程度分布",loc="left",fontproperties=CN,fontsize=12)
ax.legend(title="评分",ncol=1,frameon=False,bbox_to_anchor=(1.01,.5),loc="center left",
          prop=CN,title_fontproperties=CN,borderaxespad=0)
style(ax)
for ext in ("png","svg"): fig.savefig(OUTPUT/f"图1_认知评价与重视分布.{ext}",dpi=600,bbox_inches="tight")
plt.close(fig)

activity = pd.read_excel(WORKBOOK, sheet_name="量化_活动评价", header=1).dropna(subset=["评价编码"])
fig, ax = plt.subplots(figsize=(7.2,3.6), constrained_layout=True)
y = list(range(len(activity)))
ax.barh(y, activity["占有效评价比例"], color=["#A7A7A7","#4CC9F0","#2E5AAC","#D1495B"], height=.6)
ax.set_xlim(0,.55); ax.set_xticks([0,.1,.2,.3,.4,.5],["0","10","20","30","40","50"])
ax.set_xlabel("占有效评价比例（%）",fontproperties=CN)
ax.set_yticks(y, activity["有效评价"], fontproperties=CN)
ax.set_title("参与学校活动的家长对活动的评价",loc="left",fontproperties=CN,fontsize=12)
for i,v in enumerate(activity["占有效评价比例"]): ax.text(v+.01,i,f"{v:.1%}",va="center",fontsize=9)
style(ax)
for ext in ("png","svg"): fig.savefig(OUTPUT/f"图2_学校活动评价.{ext}",dpi=600,bbox_inches="tight")
plt.close(fig)
