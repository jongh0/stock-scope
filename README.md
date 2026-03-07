# StockScope

미국 주식 · ETF 모니터링 대시보드

**라이브 데모:** https://jongh0.github.io/stock-scope/

---

## 카테고리

| 카테고리 | 종목 |
|----------|------|
| 주요지수 | VOO, QQQ, DIA, IWM, TLT, AGG, HYG |
| TOP 20 | 시가총액 상위 20개 종목 |
| 섹터 ETF | XLK ~ XLC (10개 섹터) |
| 원자재 ETF | GLD, SLV, CPER, USO, UNG, DBC, DBA |
| 배당 ETF | DGRO, VIG, SCHD, SPYD |
| 지역 ETF | VGK, EWJ, EEM, KWEB, EWZ |
| 크립토 | IBIT, FBTC, ETHA, COIN, MSTR, MARA, RIOT, CLSK, HOOD, BITQ, CRCL, PYPL |
| 빅테크 | AAPL, MSFT, GOOGL, AMZN, TSLA, META, NVDA |
| 반도체 | NVDA, AVGO, ASML, AMD, TSM, INTC, QCOM |
| 결제·금융 | JPM, V, MA, PYPL, BAC |
| 자동차·EV | TSLA, F, GM, RIVN |
| 미디어·통신 | NFLX, DIS, VZ, T |
| SW·클라우드 | ADBE, CRM, ADSK, PLTR |
| 소비재 | WMT, COST, MCD, NKE, SBUX, KO |
| 헬스케어 | UNH, JNJ, PFE, LLY |

## 표시 항목

- 현재가 · 일간(%) · 주간(%) · MDD · RSI(14) · MACD
- 30일 / 1년 / 3년 스파크라인 차트
- 컬럼 클릭 정렬 · 라이트/다크 테마 · 모바일 반응형

## 실행

```
start.bat     # 로컬 서버 시작 → http://localhost:8080
update.bat    # 데이터 수동 갱신
```

## 데이터

- 소스: [yfinance](https://github.com/ranaroussi/yfinance) (Yahoo Finance)
- 갱신: GitHub Actions 매시간 자동 실행 (`.github/workflows/update.yml`)
- 저장: `data/stocks.json` (86개 티커)

## 요구사항

```
pip install yfinance pandas numpy requests
```
