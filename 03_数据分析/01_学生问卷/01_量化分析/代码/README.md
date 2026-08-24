# 代码说明

- `analysis_common.py`：通用描述统计、频数分布和非参数检验函数。
- `run_quantitative_analysis.py`：学生问卷完整统计流程；输入为待补充的原始逐份作答矩阵。
- `generate_figures.py`：读取正式分析工作簿并生成高分辨率PNG与SVG图；图例置于绘图区外，避免与标题、数据重叠。

运行环境建议：Python 3.11、pandas、numpy、scipy、matplotlib、openpyxl。
