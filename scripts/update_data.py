# -*- coding: utf-8 -*-
"""
update_data.py - StockScope 데이터 업데이트 스크립트
실행: python scripts/update_data.py

필요 패키지: pip install yfinance pandas requests
"""

import json
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

import yfinance as yf
import pandas as pd
import numpy as np

# ──────────────────────────────────────────────────────────
# 설정
# ──────────────────────────────────────────────────────────
OUTPUT_DIR = Path(__file__).parent.parent / "data"
OUTPUT_DIR.mkdir(exist_ok=True)

KST = timezone(timedelta(hours=9))
NOW = datetime.now(KST)
TODAY = NOW.strftime("%Y-%m-%dT%H:%M:00")

# 모든 티커 + 종목명 + 통화
STOCKS = {
    # 주요지수 ETF
    "VTI":       {"name": "미국전체",         "currency": "USD"},
    "VOO":       {"name": "S&P500",       "currency": "USD"},
    "QQQ":       {"name": "나스닥100",     "currency": "USD"},
    "DIA":       {"name": "다우",          "currency": "USD"},
    "IWM":       {"name": "러셀2000",      "currency": "USD"},
    # 배당 ETF
    "DGRO":      {"name": "배당성장 5년",       "currency": "USD"},
    "VIG":       {"name": "배당성장 10년",      "currency": "USD"},
    "SCHD":      {"name": "배당우량",       "currency": "USD"},
    "SPYD":      {"name": "고배당",         "currency": "USD"},
    # 섹터 ETF
    "XLK":       {"name": "기술섹터",           "currency": "USD"},
    "XLV":       {"name": "헬스케어섹터",       "currency": "USD"},
    "XLY":       {"name": "경기소비재섹터",     "currency": "USD"},
    "XLP":       {"name": "필수소비재섹터",     "currency": "USD"},
    "XLF":       {"name": "금융섹터",           "currency": "USD"},
    "XLI":       {"name": "산업재섹터",         "currency": "USD"},
    "XLU":       {"name": "유틸리티섹터",       "currency": "USD"},
    "XLB":       {"name": "소재섹터",           "currency": "USD"},
    "XLE":       {"name": "에너지섹터",         "currency": "USD"},
    "XLC":       {"name": "커뮤니케이션섹터",   "currency": "USD"},
    # 크립토
    "IBIT":      {"name": "비트코인 ETF",   "currency": "USD"},
    "FBTC":      {"name": "비트코인 ETF-F", "currency": "USD"},
    "ETHA":      {"name": "이더리움 ETF",   "currency": "USD"},
    "COIN":      {"name": "코인베이스",     "currency": "USD"},
    "MSTR":      {"name": "스트래티지",     "currency": "USD"},
    "MARA":      {"name": "마라톤 디지털",  "currency": "USD"},
    "RIOT":      {"name": "라이엇 플랫폼",  "currency": "USD"},
    "CLSK":      {"name": "클린스파크",     "currency": "USD"},
    "HOOD":      {"name": "로빈후드",       "currency": "USD"},
    "BITQ":      {"name": "크립토 기업 ETF", "currency": "USD"},
    # 스테이블코인 관련
    "CRCL":      {"name": "서클",           "currency": "USD"},
    # 채권
    "TLT":       {"name": "장기국채",       "currency": "USD"},
    "AGG":       {"name": "채권종합",       "currency": "USD"},
    "HYG":       {"name": "하이일드채권",   "currency": "USD"},
    # 원자재
    "GLD":       {"name": "금",             "currency": "USD"},
    "SLV":       {"name": "은",             "currency": "USD"},
    "CPER":      {"name": "구리",           "currency": "USD"},
    "USO":       {"name": "WTI 원유",       "currency": "USD"},
    "UNG":       {"name": "천연가스",       "currency": "USD"},
    "DBC":       {"name": "원자재종합",     "currency": "USD"},
    "DBA":       {"name": "농산물",         "currency": "USD"},
    # 지역 ETF
    "VGK":       {"name": "유럽",           "currency": "USD"},
    "EWJ":       {"name": "일본",           "currency": "USD"},
    "EEM":       {"name": "신흥국",         "currency": "USD"},
    "KWEB":      {"name": "중국",           "currency": "USD"},
    "EWZ":       {"name": "브라질",         "currency": "USD"},
    # 빅테크
    "AAPL":      {"name": "애플",               "currency": "USD"},
    "MSFT":      {"name": "마이크로소프트",      "currency": "USD"},
    "GOOGL":     {"name": "구글",               "currency": "USD"},
    "AMZN":      {"name": "아마존",             "currency": "USD"},
    "TSLA":      {"name": "테슬라",             "currency": "USD"},
    "META":      {"name": "메타",               "currency": "USD"},
    "NVDA":      {"name": "엔비디아",           "currency": "USD"},
    # 반도체
    "ASML":      {"name": "ASML",               "currency": "USD"},
    "AMD":       {"name": "AMD",                "currency": "USD"},
    "TSM":       {"name": "TSMC",               "currency": "USD"},
    "INTC":      {"name": "인텔",               "currency": "USD"},
    "QCOM":      {"name": "퀄컴",               "currency": "USD"},
    "AVGO":      {"name": "브로드컴",           "currency": "USD"},
    # 결제/금융
    "JPM":       {"name": "JP모건",             "currency": "USD"},
    "V":         {"name": "비자",               "currency": "USD"},
    "MA":        {"name": "마스터카드",         "currency": "USD"},
    "PYPL":      {"name": "페이팔",             "currency": "USD"},
    "BAC":       {"name": "BOA",                "currency": "USD"},
    # 자동차/EV
    "F":         {"name": "포드",               "currency": "USD"},
    "GM":        {"name": "GM",                 "currency": "USD"},
    "RIVN":      {"name": "리비안",             "currency": "USD"},
    # 미디어/통신
    "NFLX":      {"name": "넷플릭스",           "currency": "USD"},
    "DIS":       {"name": "디즈니",             "currency": "USD"},
    "VZ":        {"name": "버라이즌",           "currency": "USD"},
    "T":         {"name": "AT&T",               "currency": "USD"},
    # SW/클라우드
    "ADBE":      {"name": "어도비",             "currency": "USD"},
    "CRM":       {"name": "세일즈포스",         "currency": "USD"},
    "ADSK":      {"name": "오토데스크",         "currency": "USD"},
    "PLTR":      {"name": "팔란티어",           "currency": "USD"},
    # 유통/소비재
    "WMT":       {"name": "월마트",             "currency": "USD"},
    "COST":      {"name": "코스트코",           "currency": "USD"},
    "XOM":       {"name": "엑손모빌",           "currency": "USD"},
    "MCD":       {"name": "맥도날드",           "currency": "USD"},
    "NKE":       {"name": "나이키",             "currency": "USD"},
    "SBUX":      {"name": "스타벅스",           "currency": "USD"},
    "KO":        {"name": "코카콜라",           "currency": "USD"},
    # 헬스케어
    "UNH":       {"name": "유나이티드헬스",     "currency": "USD"},
    "JNJ":       {"name": "존슨앤존슨",         "currency": "USD"},
    "PFE":       {"name": "화이자",             "currency": "USD"},
    "LLY":       {"name": "일라이릴리",         "currency": "USD"},
    # 기타 대형주
    "BRK-B":     {"name": "버크셔해서웨이",     "currency": "USD"},
    "ORCL":      {"name": "오라클",             "currency": "USD"},
}

ALL_TICKERS = list(STOCKS.keys())


# ──────────────────────────────────────────────────────────
# MACD 계산
# ──────────────────────────────────────────────────────────
def calc_macd(series, fast=12, slow=26, signal=9):
    ema_fast   = series.ewm(span=fast,   adjust=False).mean()
    ema_slow   = series.ewm(span=slow,   adjust=False).mean()
    macd_line  = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram  = macd_line - signal_line
    return histogram


# ──────────────────────────────────────────────────────────
# RSI 계산
# ──────────────────────────────────────────────────────────
def calc_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = (-delta.clip(upper=0)).rolling(period).mean()
    rs = gain / loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi


# ──────────────────────────────────────────────────────────
# 히스토리 다운샘플 (3년 → 주봉)
# ──────────────────────────────────────────────────────────
def downsample_weekly(series):
    return series.resample('W').last().dropna()


# ──────────────────────────────────────────────────────────
# 메인 업데이트
# ──────────────────────────────────────────────────────────
def fetch_all():
    print(f"\n[StockScope] 데이터 업데이트 시작: {TODAY}")
    print(f"  총 {len(ALL_TICKERS)}개 티커 다운로드 중...")

    # 3년치 일봉 일괄 다운로드
    raw = yf.download(
        ALL_TICKERS,
        period="3y",
        auto_adjust=True,
        progress=True,
        group_by="ticker",
        threads=True,
    )

    result = {"updated": TODAY, "stocks": {}}

    for ticker in ALL_TICKERS:
        meta = STOCKS[ticker]
        try:
            # 멀티인덱스 처리
            if len(ALL_TICKERS) == 1:
                hist = raw["Close"].dropna()
            else:
                try:
                    hist = raw["Close"][ticker].dropna()
                except KeyError:
                    hist = raw[ticker]["Close"].dropna()

            if hist.empty or len(hist) < 10:
                print(f"  SKIP {ticker}: 데이터 없음")
                result["stocks"][ticker] = {"name": meta["name"], "currency": meta["currency"]}
                continue

            price      = float(hist.iloc[-1])
            prev_close = float(hist.iloc[-2]) if len(hist) >= 2 else price

            # 일간 수익률
            change_pct = (price - prev_close) / prev_close * 100

            # 주간 수익률 (5 거래일 전)
            idx_5 = max(0, len(hist) - 6)
            price_5d = float(hist.iloc[idx_5])
            week_pct = (price - price_5d) / price_5d * 100

            # 52주 고점 & MDD
            hist_1y = hist.iloc[-252:]
            high_52w = float(hist_1y.max())
            mdd_52w  = (price - high_52w) / high_52w * 100

            # RSI
            rsi_series = calc_rsi(hist)
            rsi_clean  = rsi_series.dropna()
            rsi = float(rsi_clean.iloc[-1]) if not rsi_clean.empty else None

            # MACD histogram
            macd_hist_series = calc_macd(hist)
            macd_clean = macd_hist_series.dropna()
            if len(macd_clean) >= 2:
                macd_hist = float(macd_clean.iloc[-1])
                macd_prev = float(macd_clean.iloc[-2])
                macd_up   = macd_hist > macd_prev
            else:
                macd_hist = None
                macd_up   = None

            # 히스토리 배열 (스파크라인용, 소수점 2자리)
            def to_list(s):
                return [round(float(v), 2) for v in s.values]

            hist_30d_raw = hist.iloc[-30:]
            hist_1y_raw  = hist.iloc[-252:]
            hist_3y_raw  = downsample_weekly(hist)  # 주봉 다운샘플

            result["stocks"][ticker] = {
                "name":       meta["name"],
                "currency":   meta["currency"],
                "price":      round(price, 2),
                "change_pct": round(change_pct, 2),
                "week_pct":   round(week_pct, 2),
                "mdd_52w":    round(mdd_52w, 2),
                "rsi":        round(rsi, 1) if rsi is not None else None,
                "macd_hist":  round(macd_hist, 3) if macd_hist is not None else None,
                "macd_up":    bool(macd_up) if macd_up is not None else None,
                "hist_30d":   to_list(hist_30d_raw),
                "hist_1y":    to_list(hist_1y_raw),
                "hist_3y":    to_list(hist_3y_raw),
            }
            rsi_str  = f"{rsi:.1f}"  if rsi is not None  else "-"
            macd_str = f"{macd_hist:.3f}" if macd_hist is not None else "-"
            print(f"  OK {ticker:15s}  ${price:>10.2f}  daily:{change_pct:+.2f}%  RSI:{rsi_str}  MACD:{macd_str}")

        except Exception as e:
            print(f"  ERR {ticker}: {e}")
            result["stocks"][ticker] = {"name": meta["name"], "currency": meta["currency"]}

    return result


def save_json(data):
    path = OUTPUT_DIR / "stocks.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
    size_kb = path.stat().st_size / 1024
    print(f"\n  저장 완료: {path}  ({size_kb:.1f} KB)")


if __name__ == "__main__":
    t0 = time.time()
    data = fetch_all()

    ok = sum(1 for v in data["stocks"].values() if v.get("price"))
    print(f"\n  성공: {ok}/{len(ALL_TICKERS)} 티커")

    save_json(data)
    print(f"  소요 시간: {time.time()-t0:.1f}초")
    print("  완료!\n")
