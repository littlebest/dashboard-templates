// 公共 JS - 数据大屏工具集
window.Dashboard = (function() {
  const TEXT_COLOR = '#8aa0c0';
  const AXIS_COLOR = 'rgba(74,144,226,0.2)';
  const PALETTE = ['#00d4ff', '#a855f7', '#ff6b35', '#10b981', '#f59e0b', '#ec4899', '#3b82f6', '#06b6d4'];

  // 创建图表实例，自动绑定resize
  function createChart(domId, option) {
    const dom = document.getElementById(domId);
    if (!dom) return null;
    const chart = echarts.init(dom, null, { renderer: 'canvas' });
    chart.setOption(option);
    return chart;
  }

  // 通用折线图样式
  function lineStyle(color, isArea = true) {
    const style = { color, width: 2 };
    if (isArea) {
      style.areaStyle = {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: color + '66' },
          { offset: 1, color: color + '00' }
        ])
      };
    }
    return style;
  }

  // 通用柱状渐变
  function barGradient(color) {
    return new echarts.graphic.LinearGradient(0, 0, 0, 1, [
      { offset: 0, color },
      { offset: 1, color: color + '33' }
    ]);
  }

  // 通用坐标轴样式
  function axisStyle() {
    return {
      axisLine: { lineStyle: { color: AXIS_COLOR } },
      axisLabel: { color: TEXT_COLOR, fontSize: 11 },
      splitLine: { lineStyle: { color: AXIS_COLOR, type: 'dashed' } }
    };
  }

  // 时间更新
  function startClock(elementId) {
    function update() {
      const el = document.getElementById(elementId);
      if (el) el.textContent = new Date().toLocaleString('zh-CN', { hour12: false });
    }
    update();
    return setInterval(update, 1000);
  }

  // 自动resize所有图表
  function bindResize(...charts) {
    const handler = () => charts.forEach(c => c && c.resize());
    window.addEventListener('resize', handler);
    return handler;
  }

  // 数字滚动动画
  function rollingNumber(elementId, target, duration = 2000) {
    const el = document.getElementById(elementId);
    if (!el) return;
    const start = 0;
    const startTime = Date.now();
    function tick() {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const current = Math.floor(start + (target - start) * eased);
      el.textContent = current.toLocaleString();
      if (progress < 1) requestAnimationFrame(tick);
    }
    tick();
  }

  return {
    TEXT_COLOR, AXIS_COLOR, PALETTE,
    createChart, lineStyle, barGradient, axisStyle,
    startClock, bindResize, rollingNumber
  };
})();