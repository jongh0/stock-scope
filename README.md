# StockScope

주식 · ETF 모니터링 대시보드

**라이브 데모:** https://jongh0.github.io/stock-scope/

---

## 카테고리

| 카테고리 | 내용 |
|----------|------|
| 주요지수 | VOO, QQQ, DIA, IWM, TLT, AGG, HYG |
| TOP 20 | 미국 상장 종목 시가총액 상위 20개 |
| KR TOP 20 | 코스피 시가총액 상위 20개 종목 |
| KR ETF | 국내 인기 ETF + 테마형 ETF (방산·AI·로봇·바이오·양자 등) |
| 섹터 ETF | XLK ~ XLC (10개 섹터) |
| 원자재 ETF | GLD, SLV, CPER, USO, UNG, DBC, DBA |
| 배당 ETF | DGRO, VIG, SCHD, SPYD |
| 지역 ETF | VGK, EWJ, EEM, MCHI, EWZ |
| 크립토 | IBIT, FBTC, ETHA, COIN, MSTR, MARA, RIOT, CLSK, HOOD, BITQ, CRCL |
| 빅테크 | AAPL, MSFT, GOOGL, AMZN, TSLA, META, NVDA |
| 반도체 | NVDA, AVGO, ASML, AMD, TSM, INTC, QCOM |
| 결제·금융 | JPM, V, MA, PYPL, BAC |
| 자동차·EV | TSLA, F, GM, RIVN |
| 미디어·통신 | NFLX, DIS, VZ, T |
| SW·클라우드 | ADBE, CRM, ADSK, PLTR |
| 소비재 | WMT, COST, MCD, NKE, SBUX, KO |
| 헬스케어 | UNH, JNJ, PFE, LLY |

## 표시 항목

| 항목 | 설명 |
|------|------|
| 현재가 | USD / KRW 자동 구분 |
| 일간(%) · 주간(%) | 등락률 |
| MDD | 52주 고점 대비 최대 낙폭 |
| PER | Trailing P/E |
| 배당률 | Trailing 12개월 기준 |
| RSI(14) | 미니 라인 차트 + 수치 (30/70 기준선) |
| MACD | 미니 히스토그램 차트 + 수치 (가격 대비 % 정규화) |
| 30일 · 1년 · 5년 | SVG 스파크라인 (200일 이동평균선 포함) |

- 컬럼 클릭 정렬
- 라이트/다크 테마
- 모바일 반응형 카드 뷰 (스와이프 그룹 전환)

## 실행

```
start.bat     # 로컬 서버 시작 → http://localhost:8080
update.bat    # 데이터 수동 갱신 (패키지 자동 설치 포함)
```

## 데이터

- 소스: [yfinance](https://github.com/ranaroussi/yfinance) (Yahoo Finance)
- 갱신: GitHub Actions 매시간 자동 실행 (`.github/workflows/update.yml`)
- 저장: `data/stocks.json` (약 120개 티커)
- 기간: 5년치 일봉 다운로드 (3년 이상 주봉 다운샘플)

## 요구사항

```
pip install yfinance pandas numpy requests
```
