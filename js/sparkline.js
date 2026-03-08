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
    width      = 100,
    height     = 30,
    upColor    = '#22c55e',
    downColor  = '#ef4444',
    forceColor = null,
    ma200      = null,
    maLine     = null,
    maColor    = '#f59e0b',
  } = opts;

  if (!values || values.length < 2) {
    return '<span class="spark-empty">-</span>';
  }

  const movingAvg = maLine || ma200;
  const validMa = movingAvg ? movingAvg.filter(v => v != null) : [];
  const min = Math.min(...values, ...validMa);
  const max = Math.max(...values, ...validMa);
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

  let maLineSvg = '';
  if (movingAvg && movingAvg.length >= 2) {
    const maPts = movingAvg
      .map((v, i) => v != null ? `${toX(i).toFixed(1)},${toY(v).toFixed(1)}` : null)
      .filter(Boolean)
      .join(' ');
    if (maPts) {
      maLineSvg = `<polyline points="${maPts}" fill="none" stroke="${maColor}" stroke-width="1" opacity="0.8" vector-effect="non-scaling-stroke"/>`;
    }
  }

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
    ${maLineSvg}
  </svg>`;
}

/**
 * RSI 라인 차트 (고정 0-100 스케일, 30/70 기준선 포함)
 * @param {number[]} values - RSI 값 배열
 * @param {object}  opts
 */
function createRsiChart(values, opts = {}) {
  const {
    width     = 56,
    height    = 22,
    upColor   = '#22c55e',
    downColor = '#ef4444',
    neutral   = '#64748b',
  } = opts;

  if (!values || values.length < 2) {
    return '<span class="spark-empty">-</span>';
  }

  const pad = 2;
  const h   = height - pad * 2;
  const toX = (i) => (i / (values.length - 1)) * width;
  const toY = (v) => pad + (1 - v / 100) * h;

  const y70  = toY(70).toFixed(1);
  const y30  = toY(30).toFixed(1);
  const pts  = values.map((v, i) => `${toX(i).toFixed(1)},${toY(v).toFixed(1)}`).join(' ');

  const cur  = values[values.length - 1];
  const lineColor = cur >= 70 ? downColor : cur <= 30 ? upColor : neutral;

  return `<svg width="100%" height="${height}" viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none" class="indicator-chart">
    <line x1="0" y1="${y70}" x2="${width}" y2="${y70}" stroke="${downColor}" stroke-width="0.7" stroke-dasharray="2,2" opacity="0.4"/>
    <line x1="0" y1="${y30}" x2="${width}" y2="${y30}" stroke="${upColor}"   stroke-width="0.7" stroke-dasharray="2,2" opacity="0.4"/>
    <polyline points="${pts}" fill="none" stroke="${lineColor}" stroke-width="1.5"
      stroke-linejoin="round" stroke-linecap="round" vector-effect="non-scaling-stroke"/>
  </svg>`;
}

/**
 * MACD 히스토그램 바 차트
 * @param {number[]} values - MACD hist 배열
 * @param {object}  opts
 */
function createMacdChart(values, opts = {}) {
  const {
    width     = 56,
    height    = 22,
    upColor   = '#22c55e',
    downColor = '#ef4444',
  } = opts;

  if (!values || values.length < 2) {
    return '<span class="spark-empty">-</span>';
  }

  const pad   = 2;
  const h     = height - pad * 2;
  const max   = Math.max(...values, 0);
  const min   = Math.min(...values, 0);
  const range = max - min || 1;
  const toY   = (v) => pad + (1 - (v - min) / range) * h;

  const zeroY = toY(0).toFixed(1);
  const n     = values.length;
  const barW  = width / n;
  const gap   = Math.max(barW * 0.15, 0.5);

  const bars = values.map((v, i) => {
    const x      = (i * barW + gap / 2).toFixed(1);
    const bw     = Math.max(barW - gap, 0.5).toFixed(1);
    const yVal   = toY(v);
    const yZero  = parseFloat(zeroY);
    const barTop = Math.min(yVal, yZero).toFixed(1);
    const barH   = Math.max(Math.abs(yVal - yZero), 1).toFixed(1);
    const color  = v >= 0 ? upColor : downColor;
    return `<rect x="${x}" y="${barTop}" width="${bw}" height="${barH}" fill="${color}" opacity="0.85"/>`;
  }).join('');

  return `<svg width="100%" height="${height}" viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none" class="indicator-chart">
    <line x1="0" y1="${zeroY}" x2="${width}" y2="${zeroY}" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
    ${bars}
  </svg>`;
}

/**
 * 테마 변경 시 SVG 색 재적용이 필요 없도록 CSS 변수로 색 관리
 * → 실제 색은 JS에서 직접 hex로 주입 (테마에 따라 app.js에서 호출)
 */
function getChartColors() {
  const isDark = document.documentElement.dataset.theme === 'dark';
  return {
    up:      isDark ? '#22c55e' : '#16a34a',
    down:    isDark ? '#ef4444' : '#dc2626',
    neutral: isDark ? '#64748b' : '#94a3b8',
  };
}
