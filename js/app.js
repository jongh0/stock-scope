/* ============================================================
   app.js - StockScope 메인 앱
   ============================================================ */

const _SUN_ICON  = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>`;
const _MOON_ICON = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`;

class StockScope {
  constructor() {
    this.data        = null;   // stocks.json 전체 데이터
    this.activeGroup = 'us-index';
    this.sortCol     = null;
    this.sortDir     = 1;      // 1=asc, -1=desc

    this._init();
  }

  async _init() {
    this._buildGroupNav();
    this._bindTheme();
    await this._loadData();
  }

  /* ── 그룹 네비게이션 ──────────────────────────────────── */
  _buildGroupNav() {
    const nav = document.getElementById('groupNav');
    GROUPS.forEach(g => {
      const btn = document.createElement('button');
      btn.className = 'group-btn' + (g.id === this.activeGroup ? ' active' : '');
      btn.dataset.id = g.id;
      btn.textContent = g.name;
      btn.addEventListener('click', () => this._selectGroup(g.id));
      nav.appendChild(btn);
    });
  }

  _selectGroup(id) {
    this.activeGroup = id;
    this.sortCol = null;
    this.sortDir = 1;
    document.querySelectorAll('.group-btn').forEach(b => {
      b.classList.toggle('active', b.dataset.id === id);
    });
    this._render();
  }

  /* ── 테마 ──────────────────────────────────────────────── */
  _bindTheme() {
    const btn = document.getElementById('themeBtn');
    const saved = localStorage.getItem('ss-theme') || 'dark';
    this._applyTheme(saved, btn);

    btn.addEventListener('click', () => {
      const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
      this._applyTheme(next, btn);
      localStorage.setItem('ss-theme', next);
      if (this.data) this._render();   // 스파크라인 색 재렌더
    });
  }

  _applyTheme(theme, btn) {
    document.documentElement.dataset.theme = theme;
    btn.innerHTML = theme === 'dark' ? _SUN_ICON : _MOON_ICON;
    btn.title = theme === 'dark' ? '라이트 모드' : '다크 모드';
  }

  /* ── 데이터 로드 ───────────────────────────────────────── */
  async _loadData() {
    const loading = document.getElementById('loading');
    const errMsg  = document.getElementById('errorMsg');
    loading.style.display = 'flex';

    try {
      const res = await fetch('data/stocks.json?_=' + Date.now());
      if (!res.ok) throw new Error(res.status);
      this.data = await res.json();
      loading.style.display = 'none';

      const upd = this.data.updated
        ? this.data.updated.slice(11, 16)
        : '-';
      document.getElementById('updatedLabel').textContent = '업데이트 ' + upd;

      this._render();
    } catch (e) {
      loading.style.display = 'none';
      errMsg.style.display = 'block';
      console.error('데이터 로드 실패:', e);
    }
  }

  /* ── 렌더링 ────────────────────────────────────────────── */
  _render() {
    const container = document.getElementById('tableContainer');
    const group = GROUPS.find(g => g.id === this.activeGroup);
    if (!group || !this.data) return;

    let stocks = group.stocks.map(s => ({
      ...s,
      ...(this.data.stocks?.[s.ticker] || {}),
    }));

    // 정렬
    if (this.sortCol) {
      stocks = this._sort(stocks, this.sortCol, this.sortDir);
    }

    container.innerHTML = this._buildTable(stocks, group.name);
    this._bindSort(container);
  }

  /* ── 정렬 ──────────────────────────────────────────────── */
  _sort(stocks, col, dir) {
    return [...stocks].sort((a, b) => {
      const va = a[col] ?? -Infinity;
      const vb = b[col] ?? -Infinity;
      return (va < vb ? -1 : va > vb ? 1 : 0) * dir;
    });
  }

  _bindSort(container) {
    container.querySelectorAll('th[data-col]').forEach(th => {
      th.addEventListener('click', () => {
        const col = th.dataset.col;
        if (this.sortCol === col) {
          this.sortDir *= -1;
        } else {
          this.sortCol = col;
          this.sortDir = -1;  // 숫자 컬럼은 기본 내림차순
        }
        this._render();
      });
    });
  }

  /* ── 테이블 HTML 생성 ──────────────────────────────────── */
  _buildTable(stocks, groupName) {
    const { up, down } = getChartColors();

    const sortArrow = (col) => {
      if (this.sortCol !== col) return '<span class="sort-arrow">⇅</span>';
      return `<span class="sort-arrow active">${this.sortDir > 0 ? '↑' : '↓'}</span>`;
    };

    const rows = stocks.map(s => this._buildRow(s, up, down)).join('');

    return `
      <div class="group-section">
        <div class="group-title">${groupName}
          <span class="group-count">${stocks.length}개</span>
        </div>
        <div class="table-wrap">
          <table class="stock-table">
            <thead>
              <tr>
                <th class="col-name">종목명</th>
                <th class="col-ticker">티커</th>
                <th class="col-price" data-col="price">현재가 ${sortArrow('price')}</th>
                <th class="col-pct" data-col="change_pct">일간(%) ${sortArrow('change_pct')}</th>
                <th class="col-pct col-week" data-col="week_pct">주간(%) ${sortArrow('week_pct')}</th>
                <th class="col-mdd" data-col="mdd_52w">MDD ${sortArrow('mdd_52w')}</th>
                <th class="col-rsi" data-col="rsi">RSI(14) ${sortArrow('rsi')}</th>
                <th class="col-macd" data-col="macd_hist">MACD ${sortArrow('macd_hist')}</th>
                <th class="col-spark">30일</th>
                <th class="col-spark">1년</th>
                <th class="col-spark">3년</th>
              </tr>
            </thead>
            <tbody>
              ${rows}
            </tbody>
          </table>
        </div>
      </div>
    `;
  }

  _buildRow(s, up, down) {
    const currency = TICKER_CURRENCY[s.ticker] || 'USD';
    const sym      = currency === 'KRW' ? '₩' : '$';
    const noData   = !s.price;

    // 현재가
    const priceStr = noData ? '-'
      : currency === 'KRW'
        ? sym + Math.round(s.price).toLocaleString()
        : sym + this._fmtPrice(s.price);

    // 일간 수익률
    const dayPct  = this._fmtPct(s.change_pct);
    const dayCls  = this._pctClass(s.change_pct);

    // 주간 수익률
    const weekPct = this._fmtPct(s.week_pct);
    const weekCls = this._pctClass(s.week_pct);

    // MDD (52w 고점 대비)
    const mddStr  = this._fmtPct(s.mdd_52w);
    const mddCls  = this._mddClass(s.mdd_52w);

    // RSI
    const rsiStr = s.rsi != null ? s.rsi.toFixed(1) : '-';
    const rsiCls = this._rsiClass(s.rsi);

    // MACD histogram
    const macdStr = this._fmtMacd(s.macd_hist);
    const macdCls = this._macdClass(s.macd_hist, s.macd_up);

    // 스파크라인
    const spark30  = createSparkline(s.hist_30d,  { width: 72, height: 26, upColor: up, downColor: down });
    const spark1y  = createSparkline(s.hist_1y,   { width: 72, height: 26, upColor: up, downColor: down });
    const spark3y  = createSparkline(s.hist_3y,   { width: 72, height: 26, upColor: up, downColor: down });

    const yahooUrl = `https://finance.yahoo.com/quote/${s.ticker}`;

    return `
      <tr class="stock-row" data-ticker="${s.ticker}">
        <td class="col-name">
          <span class="stock-name">${s.name}</span>
        </td>
        <td class="col-ticker">
          <a href="${yahooUrl}" target="_blank" class="ticker-link">${s.ticker}</a>
        </td>
        <td class="col-price">${priceStr}</td>
        <td class="col-pct ${dayCls}">${dayPct}</td>
        <td class="col-pct col-week ${weekCls}">${weekPct}</td>
        <td class="col-mdd">
          <span class="mdd-badge ${mddCls}">${mddStr}</span>
        </td>
        <td class="col-rsi">
          <span class="rsi-val ${rsiCls}">${rsiStr}</span>
        </td>
        <td class="col-macd">
          <span class="macd-val ${macdCls}">${macdStr}</span>
        </td>
        <td class="col-spark">${spark30}</td>
        <td class="col-spark">${spark1y}</td>
        <td class="col-spark">${spark3y}</td>
      </tr>
    `;
  }

  /* ── 포맷 유틸 ─────────────────────────────────────────── */
  _fmtPrice(v) {
    if (v == null) return '-';
    if (v >= 1000) return v.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    if (v >= 10)   return v.toFixed(2);
    return v.toFixed(4);
  }

  _fmtPct(v) {
    if (v == null) return '-';
    const sign = v > 0 ? '+' : '';
    return sign + v.toFixed(2) + '%';
  }

  _pctClass(v) {
    if (v == null) return '';
    if (v > 0)  return 'pos';
    if (v < 0)  return 'neg';
    return '';
  }

  _mddClass(v) {
    if (v == null) return '';
    if (v > -5)   return '';
    if (v > -10)  return 'mdd-mild';
    if (v > -20)  return 'mdd-moderate';
    if (v > -30)  return 'mdd-severe';
    return 'mdd-critical';
  }

  _rsiClass(v) {
    if (v == null) return '';
    if (v >= 70)  return 'rsi-high';
    if (v <= 30)  return 'rsi-low';
    return '';
  }

  _fmtMacd(v) {
    if (v == null) return '-';
    const sign = v > 0 ? '+' : '';
    const abs  = Math.abs(v);
    const dec  = abs >= 10 ? 1 : abs >= 1 ? 2 : 3;
    return sign + v.toFixed(dec);
  }

  _macdClass(hist, up) {
    if (hist == null) return '';
    // hist > 0 && up   → 강세 강화
    // hist > 0 && !up  → 강세 약화
    // hist < 0 && up   → 약세 개선
    // hist < 0 && !up  → 약세 강화
    if (hist > 0) return up ? 'macd-bull-strong' : 'macd-bull-weak';
    return up ? 'macd-bear-weak' : 'macd-bear-strong';
  }
}

/* ── 앱 시작 ────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  window.app = new StockScope();
});
