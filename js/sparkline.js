/* ============================================================
   sparkline.js - SVG 기반 미니 차트 렌더러
   ============================================================ */

let _sparkId = 0;

/**
 * SVG 스파크라인 생성
 * @param {number[]} values - 가격 배열
 * @param {object}  opts
 * @param {number}  opts.width
 * @param {number}  opts.height
 * @param {string}  opts.upColor   - 상승 색
 * @param {string}  opts.downColor - 하락 색
 * @param {string}  opts.forceColor - 강제 색 (null이면 자동)
 * @returns {string} SVG HTML string
 */
function createSparkline(values, opts = {}) {
  const {
    width     = 100,
    height    = 30,
    upColor   = '#22c55e',
    downColor = '#ef4444',
    forceColor = null,
  } = opts;

  if (!values || values.length < 2) {
    return '<span class="spark-empty">-</span>';
  }

  const min = Math.min(...values);
  const max = Math.max(...values);
  const range = max - min || 1;
  const pad = 2;

  const toX = (i) => (i / (values.length - 1)) * width;
  const toY = (v) => pad + (1 - (v - min) / range) * (height - pad * 2);

  const pts = values.map((v, i) => `${toX(i).toFixed(1)},${toY(v).toFixed(1)}`).join(' ');
  const firstX = toX(0).toFixed(1);
  const lastX  = toX(values.length - 1).toFixed(1);
  const botY   = height.toFixed(1);
  const areaPts = `${firstX},${botY} ${pts} ${lastX},${botY}`;

  const isUp = values[values.length - 1] >= values[0];
  const color = forceColor || (isUp ? upColor : downColor);
  const id = `sg${++_sparkId}`;

  return `<svg width="100%" height="${height}" viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none" class="sparkline">
    <defs>
      <linearGradient id="${id}" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="${color}" stop-opacity="0.25"/>
        <stop offset="100%" stop-color="${color}" stop-opacity="0"/>
      </linearGradient>
    </defs>
    <polygon points="${areaPts}" fill="url(#${id})"/>
    <polyline points="${pts}" fill="none" stroke="${color}" stroke-width="1.5"
      stroke-linejoin="round" stroke-linecap="round" vector-effect="non-scaling-stroke"/>
  </svg>`;
}

/**
 * 테마 변경 시 SVG 색 재적용이 필요 없도록 CSS 변수로 색 관리
 * → 실제 색은 JS에서 직접 hex로 주입 (테마에 따라 app.js에서 호출)
 */
function getChartColors() {
  const isDark = document.documentElement.dataset.theme === 'dark';
  return {
    up:   isDark ? '#22c55e' : '#16a34a',
    down: isDark ? '#ef4444' : '#dc2626',
  };
}
