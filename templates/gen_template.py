"""
大屏模板生成器 - 一键生成行业大屏
用法:
    python3 gen_template.py 行业ID 输出文件 配置JSON
"""

import json, sys

# 公共头部
HEADER = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
<link rel="stylesheet" href="../common/dashboard.css">
<style>
body {{ padding: 20px; }}
.header {{
  text-align: center;
  margin-bottom: 20px;
  position: relative;
  z-index: 1;
}}
.header h1 {{
  font-size: 28px;
  font-weight: 700;
  background: linear-gradient(90deg, #00d4ff, #a855f7, #ff6b35);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 4px;
}}
.header .sub {{
  font-size: 12px;
  color: #4a90e2;
  letter-spacing: 6px;
  margin-top: 4px;
}}
.time {{
  position: fixed; top: 20px; right: 30px;
  color: #00d4ff; font-size: 14px;
  font-family: 'Courier New', monospace;
}}
{theme_css}
</style>
</head>
<body>
<div class="time" id="time"></div>
<div class="header">
  <h1>{title}</h1>
  <div class="sub">{subtitle}</div>
</div>
<div class="grid">
{content}
</div>
<script src="../common/dashboard.js"></script>
<script>
Dashboard.startClock('time');
{init_script}
window.addEventListener('resize', () => {{
  Object.values(charts).forEach(c => c && c.resize());
}});
</script>
</body>
</html>"""

GRID_CSS = """.grid {
  display: grid;
  grid-template-columns: {cols};
  grid-template-rows: {rows};
  gap: 16px;
  max-width: 1600px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}
.chart {{ width: 100%; height: calc(100% - 30px); }}"""

# KPI卡片HTML
def kpi_card(label, value, unit, trend, trend_type='up'):
    cls = 'trend-up' if trend_type == 'up' else 'trend-down'
    icon = '▲' if trend_type == 'up' else '▼'
    return f"""  <div class="kpi-card">
    <div class="kpi-label">{label}</div>
    <div class="kpi-value">{value}<span class="kpi-unit">{unit}</span></div>
    <div class="kpi-trend {cls}">{icon} {trend}</div>
  </div>"""

def chart_card(title, dom_id, height=''):
    h_style = f' style="height:{height}"' if height else ''
    return f"""  <div class="card"{h_style}>
    <div class="card-title">{title}</div>
    <div class="chart" id="{dom_id}"></div>
  </div>"""

if __name__ == '__main__':
    # 测试：制造驾驶舱
    template = HEADER.format(
        title='生产经营驾驶舱',
        subtitle='MANUFACTURING CONTROL TOWER',
        theme_css=GRID_CSS.format(cols='repeat(4, 1fr)', rows='180px 220px 220px'),
        content='',
        init_script='const charts = {};'
    )
    print(template[:200])