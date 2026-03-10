# StockScope

주식 · ETF 모니터링 대시보드

**라이브 데모:** https://jongh0.github.io/stock-scope/

---

## 카테고리

| 카테고리 | 내용 |
|----------|------|
| 주요지수 | VOO, QQQ, DIA, IWM, BIL, AGG, TLT, HYG |
| TOP 20 | 미국 상장 시가총액 상위 20개 |
| KR TOP 20 | 코스피 시가총액 상위 20개 |
| KR ETF | 국내 주요 ETF + 테마형 ETF (AI반도체·로봇·바이오·양자 등) |
| 섹터 ETF | XLK ~ XLB (10개 섹터) |
| 원자재 ETF | GLD, SLV, PPLT, CPER, USO, UNG, DBC, DBA, WEAT |
| 배당 ETF | VIG, DGRO, SCHD, SPYD, JEPI, JEPQ |
| 지역 ETF | VGK, EWJ, EWY, EWT, EEM, INDA, MCHI, EWZ |
| 크립토 | IBIT, FBTC, ETHA, BITQ, COIN, MSTR, HOOD, CRCL, MARA, RIOT, CLSK |
| 빅테크 | AAPL, MSFT, GOOGL, AMZN, TSLA, META, NVDA |
| 반도체 | NVDA, AVGO, ASML, TSM, ARM, AMD, QCOM, MU, AMAT, LRCX, INTC |
| 결제·금융 | JPM, BAC, GS, MS, V, MA, AXP, SCHW, PYPL, XYZ |
| 자동차·EV | TSLA, TM, GM, F, NIO, RIVN, LCID |
| 미디어·통신 | NFLX, DIS, SPOT, TMUS, VZ, T, ROKU |
| SW·클라우드 | MSFT, NOW, CRM, ADBE, SHOP, PLTR, SNOW, NET, DDOG, ADSK |
| 소비재 | AMZN, WMT, COST, PG, KO, PM, MCD, TGT, SBUX, NKE, LULU |
| 헬스케어 | UNH, LLY, ABBV, JNJ, MRK, AMGN, ISRG, PFE, DXCM |

## 표시 항목

현재가 · 일간(%) · YoY · YTD · MDD · 베타 · 샤프 · PER · 배당률 · RSI(14) · MACD · 30일/1년/5년 스파크라인

- 컬럼 클릭 정렬
- 지표 설명 모달 (헤더 `?` 버튼 → MDD · 베타 · 샤프 · PER · RSI · MACD 설명)
- 라이트/다크 테마
- 모바일 반응형 카드 뷰 (스와이프 그룹 전환)

## 실행

```
start.bat     # 로컬 서버 → http://localhost:8080
update.bat    # 데이터 갱신
```

## 데이터 출처

| 항목 | 출처 |
|------|------|
| 가격 · 차트 히스토리 | [yfinance](https://github.com/ranaroussi/yfinance) (Yahoo Finance) |
| 미국 종목 PER · 배당률 | yfinance |
| 한국 종목 PER · 배당률 | [네이버 금융](https://finance.naver.com) |

- 갱신: GitHub Actions 매시간 자동 실행
- 저장: `data/stocks.json` (약 86개 티커)

## 요구사항

```
pip install yfinance pandas numpy requests
```
