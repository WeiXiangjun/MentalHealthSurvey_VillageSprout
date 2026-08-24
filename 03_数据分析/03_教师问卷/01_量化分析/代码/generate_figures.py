"""根据教师问卷正式分析工作簿生成Nature风格量化图。"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import font_manager

UNIT = Path(__file__).resolve().parents[2]
WORKBOOK = UNIT / "教师问卷正式分析.xlsx"
OUTPUT = Path(__file__).resolve().parent.parent / "图"
OUTPUT.mkdir(parents=True, exist_ok=True)
font_manager.fontManager.addfont(r"C:\Windows\Fonts\NotoSansSC-VF.ttf")
plt.rcParams.update({"font.family": "Noto Sans SC", "axes.unicode_minus": False})
CN = font_manager.FontProperties(fname=r"C:\Windows\Fonts\NotoSansSC-VF.ttf")

def style(ax):
    ax.spines[["top","right"]].set_visible(False)
    ax.grid(axis="x",color="#E6E6E6",linewidth=.6,zorder=0)
    ax.tick_params(width=.8,length=3,labelsize=9)

key = pd.read_excel(WORKBOOK, sheet_name="量化_关键结果", header=1).dropna(subset=["指标"])
plot = key.iloc[[0,1,2,3,4,7,11,12,13,14,15,16]].copy()
labels = plot["指标"].str.replace("有","",regex=False).str.slice(0,16)
yes = plot["积极/存在"].astype(float); no=plot["否定/不存在"].astype(float); unk=plot["不清楚/其他"].astype(float)
fig, ax = plt.subplots(figsize=(9.7,6.2), constrained_layout=True); y=range(len(plot))
ax.barh(y,yes,color="#2E5AAC",label="积极/存在")
ax.barh(y,no,left=yes,color="#D1495B",label="否定/不存在")
ax.barh(y,unk,left=yes+no,color="#B7B7B7",label="不清楚/其他")
ax.set_yticks(list(y),labels,fontproperties=CN); ax.invert_yaxis(); ax.set_xlim(0,17)
ax.set_xlabel("教师人数（n=17）",fontproperties=CN)
ax.set_title("教师对学校心理健康教育关键环节的认知",loc="left",fontproperties=CN,fontsize=12)
ax.legend(frameon=False,ncol=1,prop=CN,bbox_to_anchor=(1.01,.5),loc="center left",borderaxespad=0)
style(ax)
for ext in ("png","svg"): fig.savefig(OUTPUT/f"图1_关键环节认知.{ext}",dpi=600,bbox_inches="tight")
plt.close(fig)

unknown = pd.read_excel(WORKBOOK, sheet_name="量化_不清楚率", header=1).dropna(subset=["指标（重点题）"]).head(8)
fig, ax = plt.subplots(figsize=(8.0,4.5), constrained_layout=True)
y = list(range(len(unknown)))
cmap = colors.LinearSegmentedColormap.from_list("uncertainty", ["#BDBDBD", "#FF9A62", "#C9182B"])
values = unknown["不清楚比例"].astype(float)
scaled = (values - values.min()) / max(values.max() - values.min(), 1e-9)
ax.barh(y, values, color=[cmap(v) for v in scaled], height=.62)
ax.invert_yaxis(); ax.set_xlim(0,1); ax.set_xticks([0,.2,.4,.6,.8,1],["0","20","40","60","80","100"])
ax.set_xlabel("不清楚比例（%）",fontproperties=CN)
ax.set_yticks(y, unknown["指标（重点题）"], fontproperties=CN)
ax.set_title("制度与资源信息中的高不确定项目",loc="left",fontproperties=CN,fontsize=12)
for i,v in enumerate(unknown["不清楚比例"]): ax.text(v+.015,i,f"{v:.1%}",va="center",fontsize=9)
style(ax)
for ext in ("png","svg"): fig.savefig(OUTPUT/f"图2_高不确定项目.{ext}",dpi=600,bbox_inches="tight")
plt.close(fig)
