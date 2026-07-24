#!/usr/bin/env python3
"""批量生成剩余 16 个行业模板"""
import os

TEMPLATE_DIR = '/tmp/dashboard_system/templates'

# 配置：(文件名, 标题, 副标题, 主题, KPI列表, 图表列表)
TEMPLATES = [
    # 电商
    ('t3_ecommerce_overview', '电商经营总览', 'E-COMMERCE OVERVIEW', 'purple',
     [('GMV', '1856', '万', '+18.2%', 'up'), ('订单量', '12.4', '万单', '+15.3%', 'up'),
      ('客单价', '149', '元', '+2.5%', 'up'), ('复购率', '38.5', '%', '+5.2%', 'up')],
     ['GMV趋势（双轴）','支付渠道占比','品类销售TOP','转化漏斗','地区分布','新老客占比']),

    ('t3_ecommerce_profit', '电商费用利润大屏', 'E-COMMERCE PROFIT', 'purple',
     [('销售收入', '1286', '万', '+12.5%', 'up'), ('推广费用', '185', '万', '+8.5%', 'up'),
      ('物流成本', '92', '万', '+5.2%', 'up'), ('净利率', '12.8', '%', '+1.5%', 'up')],
     ['收入成本趋势','费用结构','利润分品类','ROI渠道对比','退款损失明细','成本占比']),

    # 物流
    ('t4_logistics_cost', '物流成本分析大屏', 'LOGISTICS COST', '',
     [('物流总成本', '285', '万', '+5.2%', 'up'), ('单订单成本', '23', '元', '-1.5%', 'down'),
      ('运费占比', '65', '%', '+2%', 'up'), ('异常赔付', '8.5', '万', '-12%', 'down')],
     ['成本结构（月）','运输方式占比','线路成本排名','仓库成本对比','成本趋势','异常赔付明细']),

    ('t4_logistics_delivery', '运输履约大屏', 'LOGISTICS DELIVERY', '',
     [('准时发货率', '92.5', '%', '+2.1%', 'up'), ('准时送达率', '88.3', '%', '+1.5%', 'up'),
      ('破损率', '0.8', '%', '-0.3%', 'down'), ('客户投诉', '15', '起', '-5', 'down')],
     ['履约时长分布','承运商绩效','运输异常率','准时率趋势','破损类型','投诉原因']),

    # 财务
    ('t5_finance_profit', '经营利润分析大屏', 'PROFIT ANALYSIS', 'green',
     [('营业收入', '3856', '万', '+15.2%', 'up'), ('净利润', '520', '万', '+12.8%', 'up'),
      ('毛利率', '38.5', '%', '+1.5%', 'up'), ('费用率', '22.3', '%', '-0.5%', 'down')],
     ['收入成本趋势','费用结构','产品利润分布','客户利润排名','预算完成率','利润偏差原因']),

    ('t5_finance_cashflow', '现金流预警大屏', 'CASH FLOW ALERT', 'green',
     [('现金余额', '1285', '万', '-', 'up'), ('净现金流', '+185', '万', '-', 'up'),
      ('应收账款', '485', '万', '+5.2%', 'up'), ('安全线', '125', '%', '-', 'up')],
     ['现金流趋势','流入流出','应收账龄','应付明细','资金缺口预测','回款率']),

    # 销售
    ('t6_sales_target', '销售目标达成大屏', 'SALES TARGET', 'light',
     [('年度目标', '1.2', '亿', '-', 'up'), ('实际完成', '4200', '万', '+5.2%', 'up'),
      ('完成率', '42', '%', '+3%', 'up'), ('预测达成', '95', '%', '-', 'up')],
     ['目标完成进度','区域销售排名','销售趋势（季）','TOP销售员','目标缺口分析','预测完成率']),

    ('t6_sales_customer', '客户经营分析大屏', 'CUSTOMER ANALYTICS', 'light',
     [('客户总数', '1280', '家', '+15.2%', 'up'), ('新客户', '85', '家', '+12%', 'up'),
      ('复购率', '42.5', '%', '+5.2%', 'up'), ('客户流失', '3.5', '%', '-1%', 'down')],
     ['客户分级分布','新客老客对比','客户贡献TOP','复购周期','流失预警','客户利润']),

    # 人力
    ('t7_hr_org', '组织结构分析大屏', 'HR ORGANIZATION', 'green',
     [('总人数', '1280', '人', '+5.2%', 'up'), ('部门数', '32', '个', '+2', 'up'),
      ('平均司龄', '3.8', '年', '+0.2', 'up'), ('流动率', '8.5', '%', '-1%', 'down')],
     ['部门人数分布','职级结构','学历构成','年龄分布','人员流动','部门人均产出']),

    ('t7_hr_efficiency', '人效分析大屏', 'HR EFFICIENCY', 'green',
     [('人均收入', '85', '万', '+12%', 'up'), ('人均利润', '12.5', '万', '+8%', 'up'),
      ('人工费用率', '18.5', '%', '-1%', 'down'), ('投入产出', '3.2', '倍', '+0.3', 'up')],
     ['人均收入排名','人效趋势','人工成本占比','部门人效对比','人均产能','人员投入产出']),

    # 项目
    ('t8_project_progress', '项目进度管理大屏', 'PROJECT PROGRESS', 'light',
     [('项目总数', '28', '个', '+3', 'up'), ('进行中', '15', '个', '+2', 'up'),
      ('延期项目', '4', '个', '-1', 'down'), ('里程碑完成', '82', '%', '+5%', 'up')],
     ['项目状态分布','里程碑完成率','进度偏差','风险项目数','问题关闭率','项目延期TOP']),

    ('t8_project_profit', '项目利润与回款大屏', 'PROJECT PROFIT', 'light',
     [('合同金额', '2850', '万', '+15%', 'up'), ('项目毛利', '685', '万', '+12%', 'up'),
      ('已回款', '1580', '万', '+8%', 'up'), ('毛利率', '24', '%', '+1%', 'up')],
     ['项目利润对比','回款进度','收入确认','成本结构','应收账款','项目现金流']),

    # 设备
    ('t9_equipment_fault', '设备故障分析大屏', 'EQUIPMENT FAULT', '',
     [('故障次数', '45', '次', '-8', 'down'), ('停机时长', '128', '小时', '-15', 'down'),
      ('修复时间', '2.5', '小时', '-0.3', 'down'), ('停机损失', '85', '万', '-12%', 'down')],
     ['故障趋势','故障类型分布','设备故障排名','停机时长TOP','故障规律','维修成本']),

    ('t9_equipment_oee', 'OEE设备效率大屏', 'EQUIPMENT OEE', '',
     [('OEE', '78.5', '%', '+2.5%', 'up'), ('稼动率', '88.2', '%', '+1.8%', 'up'),
      ('性能效率', '92.5', '%', '+1.2%', 'up'), ('良品率', '96.3', '%', '+0.5%', 'up')],
     ['OEE三损分解','各设备OEE','停机类型','速度损失','设备效率等级','质量损失明细']),

    # 供应链
    ('t10_supply_inventory', '库存健康分析大屏', 'INVENTORY HEALTH', 'light',
     [('库存金额', '2850', '万', '+5.2%', 'up'), ('周转率', '6.8', '次', '+0.5', 'up'),
      ('呆滞库存', '180', '万', '-12%', 'down'), ('缺货率', '3.5', '%', '-1%', 'down')],
     ['库存金额趋势','库龄分布','呆滞TOP10','出入库流量','安全库存覆盖率','品类周转排名']),

    ('t10_supply_supplier', '供应商绩效管理大屏', 'SUPPLIER PERFORMANCE', 'light',
     [('供应商数', '128', '家', '+5', 'up'), ('准时交付率', '92.5', '%', '+1.5%', 'up'),
      ('采购金额', '1856', '万', '+12%', 'up'), ('质量合格率', '96.8', '%', '+0.5%', 'up')],
     ['供应商绩效排名','交付准时率','价格波动','质量异常','供应商集中度','评分分布']),
]

def gen_kpis(kpis):
    out = []
    for label, value, unit, trend, ttype in kpis:
        cls = 'trend-up' if ttype == 'up' else 'trend-down'
        icon = '▲' if ttype == 'up' else '▼'
        out.append(f'  <div class="kpi-card"><div class="kpi-label">{label}</div><div class="kpi-value">{value}<span class="kpi-unit">{unit}</span></div><div class="kpi-trend {cls}">{icon} {trend}</div></div>')
    return '\n'.join(out)

def gen_chart_cards(charts):
    out = []
    for i, c in enumerate(charts, 1):
        # 前4个单格，后2个跨2列
        span = '' if i <= 4 else ' style="grid-column: span 2;"'
        out.append(f'  <div class="card"{span}><div class="card-title">{c}</div><div class="chart" id="c{i}"></div></div>')
    return '\n'.join(out)

def gen_chart_scripts(charts):
    """每个图表不同的简单配置"""
    palette = "['#00d4ff', '#a855f7', '#ff6b35', '#10b981', '#f59e0b', '#ec4899']"
    months = "['1月','2月','3月','4月','5月','6月','7月','8月']"
    scripts = []
    for i, c in enumerate(charts, 1):
        # 根据图表类型生成不同配置
        if '趋势' in c or '双轴' in c:
            scripts.append(f"""charts.c{i} = Dashboard.createChart('c{i}', {{
  backgroundColor: 'transparent',
  tooltip: {{ trigger: 'axis' }},
  legend: {{ top: 0, textStyle: {{ color: Dashboard.TEXT_COLOR }} }},
  grid: {{ left: '8%', right: '5%', top: '20%', bottom: '10%' }},
  xAxis: {{ type: 'category', data: {months}, ...Dashboard.axisStyle() }},
  yAxis: {{ type: 'value', ...Dashboard.axisStyle() }},
  series: [
    {{ name: '本期', type: 'line', smooth: true, data: [320,280,350,410,380,450,420,480], ...Dashboard.lineStyle('#00d4ff') }},
    {{ name: '同期', type: 'line', smooth: true, data: [280,250,310,360,340,400,380,430], lineStyle: {{ color: '#a855f7', width: 2, type: 'dashed' }} }}
  ]
}});""")
        elif '占比' in c or '结构' in c or '分布' in c and 'TOP' not in c and '排名' not in c and '库龄' not in c and '类型' not in c:
            scripts.append(f"""charts.c{i} = Dashboard.createChart('c{i}', {{
  backgroundColor: 'transparent',
  tooltip: {{ trigger: 'item' }},
  legend: {{ bottom: 0, textStyle: {{ color: Dashboard.TEXT_COLOR, fontSize: 10 }} }},
  series: [{{
    type: 'pie', radius: ['40%','70%'],
    itemStyle: {{ borderRadius: 4, borderColor: '#0a1530', borderWidth: 2 }},
    label: {{ color: '#fff', fontSize: 11 }},
    data: [
      {{ value: 35, name: '类别A', itemStyle: {{ color: '#00d4ff' }} }},
      {{ value: 25, name: '类别B', itemStyle: {{ color: '#a855f7' }} }},
      {{ value: 20, name: '类别C', itemStyle: {{ color: '#ff6b35' }} }},
      {{ value: 12, name: '类别D', itemStyle: {{ color: '#10b981' }} }},
      {{ value: 8, name: '类别E', itemStyle: {{ color: '#f59e0b' }} }}
    ]
  }}]
}});""")
        elif 'TOP' in c or '排名' in c:
            scripts.append(f"""charts.c{i} = Dashboard.createChart('c{i}', {{
  backgroundColor: 'transparent',
  tooltip: {{ trigger: 'axis', axisPointer: {{ type: 'shadow' }} }},
  grid: {{ left: '5%', right: '10%', top: '5%', bottom: '5%', containLabel: true }},
  xAxis: {{ type: 'value', show: false }},
  yAxis: {{ type: 'category', inverse: true, data: ['项目A','项目B','项目C','项目D','项目E','项目F','项目G','项目H'], axisLine: {{ show: false }}, axisTick: {{ show: false }}, axisLabel: {{ color: Dashboard.TEXT_COLOR, fontSize: 10 }} }},
  series: [{{
    type: 'bar', barWidth: 12,
    data: [85,78,72,65,58,52,45,38],
    itemStyle: {{
      borderRadius: [0,4,4,0],
      color: function(p) {{
        const colors = Dashboard.PALETTE;
        return new echarts.graphic.LinearGradient(0,0,1,0,[
          {{offset:0,color:colors[p.dataIndex%8]+'33'}},
          {{offset:1,color:colors[p.dataIndex%8]}}
        ]);
      }}
    }},
    label: {{ show: true, position: 'right', formatter: '{{c}}', color: '#fff' }}
  }}]
}});""")
        elif '漏斗' in c:
            scripts.append(f"""charts.c{i} = Dashboard.createChart('c{i}', {{
  backgroundColor: 'transparent',
  tooltip: {{ trigger: 'item' }},
  series: [{{
    type: 'funnel', left: '10%', right: '10%', top: '5%', bottom: '5%', width: '80%',
    sort: 'descending', gap: 4,
    label: {{ show: true, position: 'inside', color: '#fff', fontSize: 13 }},
    data: [
      {{ value: 100, name: '阶段1', itemStyle: {{ color: '#00d4ff' }} }},
      {{ value: 80, name: '阶段2', itemStyle: {{ color: '#06b6d4' }} }},
      {{ value: 60, name: '阶段3', itemStyle: {{ color: '#a855f7' }} }},
      {{ value: 40, name: '阶段4', itemStyle: {{ color: '#3b82f6' }} }},
      {{ value: 20, name: '阶段5', itemStyle: {{ color: '#ff6b35' }} }}
    ]
  }}]
}});""")
        elif '完成率' in c or '覆盖率' in c or '安全' in c:
            scripts.append(f"""charts.c{i} = Dashboard.createChart('c{i}', {{
  backgroundColor: 'transparent',
  series: [{{
    type: 'gauge', startAngle: 200, endAngle: -20, min: 0, max: 100,
    progress: {{ show: true, width: 18,
      itemStyle: {{ color: new echarts.graphic.LinearGradient(0,0,1,0,[
        {{offset:0,color:'#00d4ff'}},{{offset:1,color:'#a855f7'}}]) }} }},
    axisLine: {{ lineStyle: {{ width: 18, color: [[1,'rgba(74,144,226,0.15)']] }} }},
    pointer: {{ show: false }}, axisTick: {{ show: false }}, splitLine: {{ show: false }}, axisLabel: {{ show: false }},
    anchor: {{ show: false }},
    detail: {{ valueAnimation: true, fontSize: 36, color: '#fff', formatter: '{{value}}%', offsetCenter: [0,'10%'] }},
    title: {{ offsetCenter: [0,'40%'], fontSize: 14, color: Dashboard.TEXT_COLOR }},
    data: [{{ value: {50 + i*5}, name: '{c}' }}]
  }}]
}});""")
        elif '分布' in c and '年龄' in c:
            scripts.append(f"""charts.c{i} = Dashboard.createChart('c{i}', {{
  backgroundColor: 'transparent',
  tooltip: {{ trigger: 'axis' }},
  grid: {{ left: '8%', right: '8%', top: '10%', bottom: '10%' }},
  xAxis: {{ type: 'category', data: ['<25','25-30','30-35','35-40','40-50','>50'], ...Dashboard.axisStyle() }},
  yAxis: {{ type: 'value', ...Dashboard.axisStyle() }},
  series: [{{
    type: 'bar', barWidth: 24,
    data: [120, 280, 380, 280, 180, 40],
    itemStyle: {{
      color: function(p) {{
        return new echarts.graphic.LinearGradient(0,0,0,1,[
          {{offset:0,color:Dashboard.PALETTE[p.dataIndex]+'CC'}},
          {{offset:1,color:Dashboard.PALETTE[p.dataIndex]+'33'}}
        ]);
      }},
      borderRadius: [4,4,0,0]
    }}
  }}]
}});""")
        elif '对比' in c or '（' in c:
            scripts.append(f"""charts.c{i} = Dashboard.createChart('c{i}', {{
  backgroundColor: 'transparent',
  tooltip: {{ trigger: 'axis', axisPointer: {{ type: 'shadow' }} }},
  legend: {{ top: 0, textStyle: {{ color: Dashboard.TEXT_COLOR }} }},
  grid: {{ left: '5%', right: '5%', top: '15%', bottom: '8%' }},
  xAxis: {{ type: 'category', data: {months}, ...Dashboard.axisStyle() }},
  yAxis: {{ type: 'value', ...Dashboard.axisStyle() }},
  series: [
    {{ name: 'A', type: 'bar', data: [120,150,180,220,260,300,340,380], itemStyle: {{ color: Dashboard.barGradient('#00d4ff'), borderRadius: [4,4,0,0] }}, barWidth: 14 }},
    {{ name: 'B', type: 'bar', data: [80,100,120,150,180,200,230,260], itemStyle: {{ color: Dashboard.barGradient('#a855f7'), borderRadius: [4,4,0,0] }}, barWidth: 14 }}
  ]
}});""")
        else:
            # 默认折线
            scripts.append(f"""charts.c{i} = Dashboard.createChart('c{i}', {{
  backgroundColor: 'transparent',
  tooltip: {{ trigger: 'axis' }},
  grid: {{ left: '8%', right: '5%', top: '10%', bottom: '10%' }},
  xAxis: {{ type: 'category', data: {months}, ...Dashboard.axisStyle() }},
  yAxis: {{ type: 'value', ...Dashboard.axisStyle() }},
  series: [{{
    type: 'line', smooth: true,
    data: [120,135,128,148,162,155,178,185],
    ...Dashboard.lineStyle('#00d4ff')
  }}]
}});""")
    return '\n\n'.join(scripts)

def gen_template(filename, title, subtitle, theme, kpis, charts):
    theme_css = ''
    if theme == 'purple':
        theme_css = 'body { background: radial-gradient(ellipse at center, #2d1b4e 0%, #1a0d33 50%, #0a0518 100%); }'
    elif theme == 'green':
        theme_css = 'body { background: radial-gradient(ellipse at center, #1a3a2e 0%, #0d2618 50%, #050f0a 100%); }'
    elif theme == 'light':
        theme_css = 'body { background: linear-gradient(135deg, #f0f4ff 0%, #d9e3f0 100%); color: #1a2a4e; } .card { background: rgba(255,255,255,0.9); border-color: rgba(74,144,226,0.2); } .card-title { color: #1a2a4e; } .kpi-card { background: rgba(255,255,255,0.95); border-color: rgba(74,144,226,0.3); } .kpi-label, .kpi-trend { color: #4a5568; } .kpi-value { background: linear-gradient(90deg, #1a2a4e, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; } .kpi-unit { color: #a855f7; -webkit-text-fill-color: #a855f7; }'

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
<link rel="stylesheet" href="../common/dashboard.css">
<style>
body {{ padding: 20px; {theme_css} }}
.header {{ text-align: center; margin-bottom: 20px; }}
.header h1 {{ font-size: 28px; background: linear-gradient(90deg, #00d4ff, #a855f7, #ff6b35); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: 4px; }}
.header .sub {{ font-size: 12px; color: #4a90e2; letter-spacing: 6px; margin-top: 4px; }}
.time {{ position: fixed; top: 20px; right: 30px; color: #00d4ff; font-family: 'Courier New', monospace; }}
.grid {{ display: grid; grid-template-columns: repeat(4, 1fr); grid-template-rows: 160px 220px 220px; gap: 16px; max-width: 1600px; margin: 0 auto; }}
.kpi-card {{ background: linear-gradient(135deg, rgba(22,33,62,0.9), rgba(15,25,50,0.95)); border: 1px solid rgba(168,85,247,0.4); border-radius: 8px; padding: 18px; text-align: center; position: relative; overflow: hidden; }}
.kpi-card::before {{ content: ''; position: absolute; inset: 0; background: linear-gradient(45deg, transparent 30%, rgba(168,85,247,0.1) 50%, transparent 70%); animation: shimmer 3s infinite; }}
@keyframes shimmer {{ 0% {{ transform: translateX(-100%); }} 100% {{ transform: translateX(100%); }} }}
.kpi-label {{ font-size: 12px; color: #8aa0c0; margin-bottom: 6px; position: relative; }}
.kpi-value {{ font-size: 32px; font-weight: 700; background: linear-gradient(90deg, #00d4ff, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-family: 'Courier New', monospace; position: relative; }}
.kpi-unit {{ font-size: 12px; color: #a855f7; margin-left: 4px; -webkit-text-fill-color: #a855f7; }}
.kpi-trend {{ font-size: 11px; margin-top: 4px; position: relative; }}
.trend-up {{ color: #10b981; }} .trend-down {{ color: #ef4444; }}
.chart {{ width: 100%; height: calc(100% - 30px); }}
</style>
</head>
<body>
<div class="time" id="time"></div>
<div class="header">
  <h1>{title}</h1>
  <div class="sub">{subtitle}</div>
</div>

<div class="grid">
{gen_kpis(kpis)}

{gen_chart_cards(charts)}
</div>

<script src="../common/dashboard.js"></script>
<script>
Dashboard.startClock('time');
const charts = {{}};

{gen_chart_scripts(charts)}
</script>
</body>
</html>"""

# 批量生成
print(f"开始批量生成 {len(TEMPLATES)} 个模板...")
for filename, title, subtitle, theme, kpis, charts in TEMPLATES:
    content = gen_template(filename, title, subtitle, theme, kpis, charts)
    path = f'{TEMPLATE_DIR}/{filename}.html'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✓ {filename}.html ({len(content)} bytes)")

print(f"\n完成！共 {len(TEMPLATES)} 个模板生成")