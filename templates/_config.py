"""
大屏生成器 - 批量生成剩余18个行业大屏
策略：使用统一模板，差异化配置（标题/KPI/图表）
"""

import json
import os

# 每个行业的两套大屏配置
TEMPLATES = {
    # 2. 零售 - 门店经营分析
    't2_retail_store': {
        'title': '门店经营分析大屏', 'subtitle': 'RETAIL STORE DASHBOARD',
        'kpis': [('销售额', '1286', '万', '+12.5%', 'up'),
                 ('毛利额', '380', '万', '+8.2%', 'up'),
                 ('客流量', '2.3', '万人', '+5.1%', 'up'),
                 ('坪效', '85', '元/㎡', '-2.3%', 'down')],
        'charts': [
            {'id': 'r1', 'title': '销售趋势（按门店）', 'type': 'multi_line'},
            {'id': 'r2', 'title': '各门店毛利排名', 'type': 'horizontal_bar'},
            {'id': 'r3', 'title': '客单价分布', 'type': 'histogram'},
            {'id': 'r4', 'title': '转化漏斗', 'type': 'funnel'},
            {'id': 'r5', 'title': '费用占比', 'type': 'pie'},
            {'id': 'r6', 'title': '门店利润分布', 'type': 'group_bar'}
        ]
    },
    # 3. 电商 - 经营总览
    't3_ecommerce_overview': {
        'title': '电商经营总览', 'subtitle': 'E-COMMERCE OVERVIEW',
        'theme': 'purple',
        'kpis': [('GMV', '1856', '万', '+18.2%', 'up'),
                 ('订单量', '12.4', '万单', '+15.3%', 'up'),
                 ('客单价', '149', '元', '+2.5%', 'up'),
                 ('复购率', '38.5', '%', '+5.2%', 'up')],
        'charts': [
            {'id': 'e1', 'title': 'GMV 趋势（双轴）', 'type': 'dual_axis'},
            {'id': 'e2', 'title': '支付渠道占比', 'type': 'pie'},
            {'id': 'e3', 'title': '品类销售 TOP', 'type': 'horizontal_bar'},
            {'id': 'e4', 'title': '转化漏斗', 'type': 'funnel'},
            {'id': 'e5', 'title': '地区分布', 'type': 'map'},
            {'id': 'e6', 'title': '新老客占比', 'type': 'pie'}
        ]
    },
    # 4. 物流 - 成本分析
    't4_logistics_cost': {
        'title': '物流成本分析大屏', 'subtitle': 'LOGISTICS COST ANALYSIS',
        'kpis': [('物流总成本', '285', '万', '+5.2%', 'up'),
                 ('单订单成本', '23', '元/单', '-1.5%', 'down'),
                 ('运费占比', '65', '%', '+2%', 'up'),
                 ('异常赔付', '8.5', '万', '-12%', 'down')],
        'charts': [
            {'id': 'l1', 'title': '成本结构（月）', 'type': 'stacked_bar'},
            {'id': 'l2', 'title': '运输方式占比', 'type': 'pie'},
            {'id': 'l3', 'title': '线路成本排名', 'type': 'horizontal_bar'},
            {'id': 'l4', 'title': '仓库成本对比', 'type': 'group_bar'},
            {'id': 'l5', 'title': '成本趋势', 'type': 'multi_line'},
            {'id': 'l6', 'title': '异常赔付明细', 'type': 'table'}
        ]
    },
    # 5. 财务 - 经营利润
    't5_finance_profit': {
        'title': '经营利润分析大屏', 'subtitle': 'PROFIT ANALYSIS',
        'theme': 'green',
        'kpis': [('营业收入', '3856', '万', '+15.2%', 'up'),
                 ('净利润', '520', '万', '+12.8%', 'up'),
                 ('毛利率', '38.5', '%', '+1.5%', 'up'),
                 ('费用率', '22.3', '%', '-0.5%', 'down')],
        'charts': [
            {'id': 'f1', 'title': '收入成本趋势', 'type': 'dual_axis'},
            {'id': 'f2', 'title': '费用结构', 'type': 'pie'},
            {'id': 'f3', 'title': '产品利润分布', 'type': 'pie'},
            {'id': 'f4', 'title': '客户利润排名', 'type': 'horizontal_bar'},
            {'id': 'f5', 'title': '预算完成率', 'type': 'progress'},
            {'id': 'f6', 'title': '利润偏差原因', 'type': 'horizontal_bar'}
        ]
    },
    # 6. 销售 - 目标达成
    't6_sales_target': {
        'title': '销售目标达成大屏', 'subtitle': 'SALES TARGET DASHBOARD',
        'theme': 'light',
        'kpis': [('年度目标', '1.2', '亿', '-', 'up'),
                 ('实际完成', '4200', '万', '+5.2%', 'up'),
                 ('完成率', '42', '%', '+3%', 'up'),
                 ('预测达成', '95', '%', '-', 'up')],
        'charts': [
            {'id': 's1', 'title': '目标完成进度', 'type': 'progress'},
            {'id': 's2', 'title': '区域销售排名', 'type': 'horizontal_bar'},
            {'id': 's3', 'title': '销售趋势（季度）', 'type': 'line'},
            {'id': 's4', 'title': 'TOP销售员', 'type': 'horizontal_bar'},
            {'id': 's5', 'title': '目标缺口分析', 'type': 'group_bar'},
            {'id': 's6', 'title': '预测完成率', 'type': 'line'}
        ]
    },
    # 7. 人力 - 组织结构
    't7_hr_org': {
        'title': '组织结构分析大屏', 'subtitle': 'HR ORGANIZATION',
        'theme': 'green',
        'kpis': [('总人数', '1280', '人', '+5.2%', 'up'),
                 ('部门数', '32', '个', '+2', 'up'),
                 ('平均司龄', '3.8', '年', '+0.2', 'up'),
                 ('流动率', '8.5', '%', '-1%', 'down')],
        'charts': [
            {'id': 'h1', 'title': '部门人数分布', 'type': 'pie'},
            {'id': 'h2', 'title': '职级结构', 'type': 'stacked_bar'},
            {'id': 'h3', 'title': '学历构成', 'type': 'pie'},
            {'id': 'h4', 'title': '年龄分布', 'type': 'histogram'},
            {'id': 'h5', 'title': '人员流动（进出）', 'type': 'group_bar'},
            {'id': 'h6', 'title': '部门人均产出', 'type': 'horizontal_bar'}
        ]
    },
    # 8. 项目 - 进度管理
    't8_project_progress': {
        'title': '项目进度管理大屏', 'subtitle': 'PROJECT PROGRESS',
        'theme': 'light',
        'kpis': [('项目总数', '28', '个', '+3', 'up'),
                 ('进行中', '15', '个', '+2', 'up'),
                 ('延期项目', '4', '个', '-1', 'down'),
                 ('里程碑完成', '82', '%', '+5%', 'up')],
        'charts': [
            {'id': 'p1', 'title': '项目状态分布', 'type': 'pie'},
            {'id': 'p2', 'title': '里程碑完成率（按项目）', 'type': 'horizontal_bar'},
            {'id': 'p3', 'title': '进度偏差（计划vs实际）', 'type': 'group_bar'},
            {'id': 'p4', 'title': '风险项目数', 'type': 'progress'},
            {'id': 'p5', 'title': '问题关闭率趋势', 'type': 'line'},
            {'id': 'p6', 'title': '项目延期 TOP', 'type': 'horizontal_bar'}
        ]
    },
    # 9. 设备 - OEE
    't9_equipment_oee': {
        'title': 'OEE 设备效率大屏', 'subtitle': 'EQUIPMENT OEE',
        'kpis': [('OEE', '78.5', '%', '+2.5%', 'up'),
                 ('稼动率', '88.2', '%', '+1.8%', 'up'),
                 ('性能效率', '92.5', '%', '+1.2%', 'up'),
                 ('良品率', '96.3', '%', '+0.5%', 'up')],
        'charts': [
            {'id': 'eq1', 'title': 'OEE 三损分解', 'type': 'stacked_bar'},
            {'id': 'eq2', 'title': '各设备 OEE 对比', 'type': 'horizontal_bar'},
            {'id': 'eq3', 'title': '停机类型分布', 'type': 'pie'},
            {'id': 'eq4', 'title': '速度损失趋势', 'type': 'line'},
            {'id': 'eq5', 'title': '设备效率等级', 'type': 'progress'},
            {'id': 'eq6', 'title': '质量损失明细', 'type': 'table'}
        ]
    },
    # 10. 供应链 - 库存健康
    't10_supply_inventory': {
        'title': '库存健康分析大屏', 'subtitle': 'INVENTORY HEALTH',
        'theme': 'light',
        'kpis': [('库存金额', '2850', '万', '+5.2%', 'up'),
                 ('周转率', '6.8', '次', '+0.5', 'up'),
                 ('呆滞库存', '180', '万', '-12%', 'down'),
                 ('缺货率', '3.5', '%', '-1%', 'down')],
        'charts': [
            {'id': 'i1', 'title': '库存金额趋势', 'type': 'dual_axis'},
            {'id': 'i2', 'title': '库龄分布', 'type': 'pie'},
            {'id': 'i3', 'title': '呆滞 TOP10', 'type': 'horizontal_bar'},
            {'id': 'i4', 'title': '出入库流量', 'type': 'line'},
            {'id': 'i5', 'title': '安全库存覆盖率', 'type': 'progress'},
            {'id': 'i6', 'title': '品类周转排名', 'type': 'horizontal_bar'}
        ]
    },
}

print(f"已配置 {len(TEMPLATES)} 个模板")
for key in TEMPLATES:
    print(f"  - {key}")