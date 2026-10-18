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

RISK_FREE_RATE = 4.5  # 연간 무위험 수익률 (%) — 미국 단기채 기준

# 모든 티커 + 종목명 + 통화
# NOTE: TOP 20 category in js/config.js uses US-listed market-cap ranking.
STOCKS = {
    # 주요지수 ETF
    "VOO":       {"name": "S&P500",       "currency": "USD"},
    "QQQ":       {"name": "나스닥100",     "currency": "USD"},
    "DIA":       {"name": "다우",          "currency": "USD"},
    "IWM":       {"name": "러셀2000",      "currency": "USD"},
    # 배당 ETF
    "DGRO":      {"name": "배당성장 5년",       "currency": "USD"},
    "VIG":       {"name": "배당성장 10년",      "currency": "USD"},
    "SCHD":      {"name": "배당우량",       "currency": "USD"},
    "SPYD":      {"name": "고배당",         "currency": "USD"},
    "JEPI":      {"name": "JP모건 커버드콜", "currency": "USD"},
    "JEPQ":      {"name": "나스닥 커버드콜", "currency": "USD"},
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
    "BTC-USD":   {"name": "비트코인",       "currency": "USD"},
    "ETH-USD":   {"name": "이더리움",       "currency": "USD"},
    "SOL-USD":   {"name": "솔라나",         "currency": "USD"},
    "IBIT":      {"name": "비트코인 ETF",   "currency": "USD"},
    "FBTC":      {"name": "비트코인 ETF-F", "currency": "USD"},
    "ETHA":      {"name": "이더리움 ETF",   "currency": "USD"},
    "COIN":      {"name": "코인베이스",     "currency": "USD"},
    "MSTR":      {"name": "스트래티지",     "currency": "USD"},
    "MARA":      {"name": "마라톤 디지털",  "currency": "USD"},
    "RIOT":      {"name": "라이엇 플랫폼",  "currency": "USD"},
    "HOOD":      {"name": "로빈후드",       "currency": "USD"},
    "BITQ":      {"name": "크립토 기업 ETF", "currency": "USD"},
    # 스테이블코인 관련
    "CRCL":      {"name": "서클",           "currency": "USD"},
    # 채권
    "TLT":       {"name": "장기국채",       "currency": "USD"},
    "AGG":       {"name": "채권종합",       "currency": "USD"},
    "HYG":       {"name": "하이일드채권",   "currency": "USD"},
    "BIL":       {"name": "단기국채",       "currency": "USD"},
    # 원자재
    "GLD":       {"name": "금",             "currency": "USD"},
    "SLV":       {"name": "은",             "currency": "USD"},
    "CPER":      {"name": "구리",           "currency": "USD"},
    "USO":       {"name": "WTI 원유",       "currency": "USD"},
    "UNG":       {"name": "천연가스",       "currency": "USD"},
    "DBC":       {"name": "원자재종합",     "currency": "USD"},
    "DBA":       {"name": "농산물",         "currency": "USD"},
    "PPLT":      {"name": "백금",           "currency": "USD"},
    "WEAT":      {"name": "밀",             "currency": "USD"},
    # 지역 ETF
    "VGK":       {"name": "유럽",           "currency": "USD"},
    "EWJ":       {"name": "일본",           "currency": "USD"},
    "EEM":       {"name": "신흥국",         "currency": "USD"},
    "MCHI":      {"name": "중국",           "currency": "USD"},
    "EWZ":       {"name": "브라질",         "currency": "USD"},
    "INDA":      {"name": "인도",           "currency": "USD"},
    "EWY":       {"name": "한국",           "currency": "USD"},
    "EWT":       {"name": "대만",           "currency": "USD"},
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
    "TXN":       {"name": "텍사스인스트루먼트",  "currency": "USD"},
    "AVGO":      {"name": "브로드컴",           "currency": "USD"},
    "MU":        {"name": "마이크론",           "currency": "USD"},
    "ARM":       {"name": "ARM홀딩스",          "currency": "USD"},
    "AMAT":      {"name": "어플라이드머티리얼즈", "currency": "USD"},
    "LRCX":      {"name": "램리서치",           "currency": "USD"},
    # 결제/금융
    "JPM":       {"name": "JP모건",             "currency": "USD"},
    "V":         {"name": "비자",               "currency": "USD"},
    "MA":        {"name": "마스터카드",         "currency": "USD"},
    "BAC":       {"name": "BOA",                "currency": "USD"},
    "WFC":       {"name": "웰스파고",           "currency": "USD"},
    "GS":        {"name": "골드만삭스",         "currency": "USD"},
    "MS":        {"name": "모건스탠리",         "currency": "USD"},
    "BLK":       {"name": "블랙록",             "currency": "USD"},
    "AXP":       {"name": "아메리칸익스프레스", "currency": "USD"},
    "SCHW":      {"name": "찰스슈왑",           "currency": "USD"},
    # 자동차/EV
    "F":         {"name": "포드",               "currency": "USD"},
    "GM":        {"name": "GM",                 "currency": "USD"},
    "RIVN":      {"name": "리비안",             "currency": "USD"},
    "TM":        {"name": "토요타",             "currency": "USD"},
    "RACE":      {"name": "페라리",             "currency": "USD"},
    "UBER":      {"name": "우버",               "currency": "USD"},
    # 미디어/통신
    "NFLX":      {"name": "넷플릭스",           "currency": "USD"},
    "DIS":       {"name": "디즈니",             "currency": "USD"},
    "VZ":        {"name": "버라이즌",           "currency": "USD"},
    "T":         {"name": "AT&T",               "currency": "USD"},
    "SPOT":      {"name": "스포티파이",         "currency": "USD"},
    "ROKU":      {"name": "로쿠",               "currency": "USD"},
    "TMUS":      {"name": "T모바일",            "currency": "USD"},
    # SW/클라우드
    "ORCL":      {"name": "오라클",             "currency": "USD"},
    "PANW":      {"name": "팔로알토",           "currency": "USD"},
    "ADBE":      {"name": "어도비",             "currency": "USD"},
    "CRM":       {"name": "세일즈포스",         "currency": "USD"},
    "PLTR":      {"name": "팔란티어",           "currency": "USD"},
    "SNOW":      {"name": "스노우플레이크",     "currency": "USD"},
    "NOW":       {"name": "서비스나우",         "currency": "USD"},
    "SHOP":      {"name": "쇼피파이",           "currency": "USD"},
    "NET":       {"name": "클라우드플레어",     "currency": "USD"},
    "DDOG":      {"name": "데이터독",           "currency": "USD"},
    # 유통/소비재
    "WMT":       {"name": "월마트",             "currency": "USD"},
    "COST":      {"name": "코스트코",           "currency": "USD"},
    "HD":        {"name": "홈디포",             "currency": "USD"},
    "XOM":       {"name": "엑손모빌",           "currency": "USD"},
    "MCD":       {"name": "맥도날드",           "currency": "USD"},
    "NKE":       {"name": "나이키",             "currency": "USD"},
    "SBUX":      {"name": "스타벅스",           "currency": "USD"},
    "KO":        {"name": "코카콜라",           "currency": "USD"},
    "TGT":       {"name": "타겟",               "currency": "USD"},
    "PG":        {"name": "P&G",                "currency": "USD"},
    "PM":        {"name": "필립모리스",         "currency": "USD"},
    # 헬스케어
    "UNH":       {"name": "유나이티드헬스",     "currency": "USD"},
    "JNJ":       {"name": "존슨앤존슨",         "currency": "USD"},
    "PFE":       {"name": "화이자",             "currency": "USD"},
    "LLY":       {"name": "일라이릴리",         "currency": "USD"},
    "ABBV":      {"name": "애브비",             "currency": "USD"},
    "MRK":       {"name": "머크",               "currency": "USD"},
    "NVO":       {"name": "노보노디스크",       "currency": "USD"},
    "TMO":       {"name": "써모피셔",           "currency": "USD"},
    "AMGN":      {"name": "암젠",               "currency": "USD"},
    "ISRG":      {"name": "인튜이티브서지컬",   "currency": "USD"},
    # 기타 대형주
    "BRK-B":     {"name": "버크셔해서웨이",     "currency": "USD"},
    # 한국 인기 ETF (코스피)
    "360750.KS": {"name": "TIGER 미국S&P500",     "currency": "KRW"},
    "133690.KS": {"name": "TIGER 미국나스닥100",  "currency": "KRW"},
    "381180.KS": {"name": "TIGER 미국테크TOP10",  "currency": "KRW"},
    "446720.KS": {"name": "SOL 미국배당다우존스", "currency": "KRW"},
    "069500.KS": {"name": "KODEX 200",            "currency": "KRW"},
    "122630.KS": {"name": "KODEX 레버리지",       "currency": "KRW"},
    "114800.KS": {"name": "KODEX 인버스",         "currency": "KRW"},
    "252670.KS": {"name": "KODEX 인버스2X",       "currency": "KRW"},
    "411060.KS": {"name": "ACE KRX금현물",        "currency": "KRW"},
    "273130.KS": {"name": "KODEX 종합채권",         "currency": "KRW"},
    # 테마형 ETF
    "396500.KS": {"name": "TIGER 반도체TOP10",      "currency": "KRW"},
    "463250.KS": {"name": "TIGER K방산&우주",       "currency": "KRW"},
    "395160.KS": {"name": "KODEX AI반도체",         "currency": "KRW"},
    "487230.KS": {"name": "KODEX 미국AI전력인프라", "currency": "KRW"},
    "445290.KS": {"name": "KODEX 로봇액티브",       "currency": "KRW"},
    "0023A0.KS": {"name": "SOL 미국양자컴퓨팅",    "currency": "KRW"},
    "476690.KS": {"name": "TIGER 비만치료제",       "currency": "KRW"},
    # 한국 시가총액 상위 (코스피)
    "005930.KS": {"name": "삼성전자",           "currency": "KRW"},
    "000660.KS": {"name": "SK하이닉스",         "currency": "KRW"},
    "373220.KS": {"name": "LG에너지솔루션",     "currency": "KRW"},
    "207940.KS": {"name": "삼성바이오로직스",   "currency": "KRW"},
    "005380.KS": {"name": "현대차",             "currency": "KRW"},
    "329180.KS": {"name": "HD현대중공업",       "currency": "KRW"},
    "402340.KS": {"name": "SK스퀘어",           "currency": "KRW"},
    "012450.KS": {"name": "한화에어로스페이스", "currency": "KRW"},
    "034020.KS": {"name": "두산에너빌리티",     "currency": "KRW"},
    "105560.KS": {"name": "KB금융",             "currency": "KRW"},
    "000270.KS": {"name": "기아",               "currency": "KRW"},
    "068270.KS": {"name": "셀트리온",           "currency": "KRW"},
    "028260.KS": {"name": "삼성물산",           "currency": "KRW"},
    "035420.KS": {"name": "NAVER",              "currency": "KRW"},
    "055550.KS": {"name": "신한지주",           "currency": "KRW"},
    "042660.KS": {"name": "한화오션",           "currency": "KRW"},
    "012330.KS": {"name": "현대모비스",         "currency": "KRW"},
    "032830.KS": {"name": "삼성생명",           "currency": "KRW"},
    "015760.KS": {"name": "한국전력",           "currency": "KRW"},
    "086790.KS": {"name": "하나금융지주",       "currency": "KRW"},
}

ALL_TICKERS = list(STOCKS.keys())

# 기본 TOP 20 폴백 목록 (API 조회 실패 시 사용)
DEFAULT_US_TOP20 = [
    "NVDA", "AAPL", "GOOGL", "MSFT", "AMZN", "TSM", "META", "AVGO", "TSLA", "BRK-B",
    "WMT", "LLY", "JPM", "XOM", "V", "JNJ", "ASML", "MA", "ORCL", "COST",
]

DEFAULT_KR_TOP20 = [
    "005930.KS", "000660.KS", "207940.KS", "373220.KS", "005380.KS",
    "034020.KS", "012450.KS", "329180.KS", "105560.KS", "402340.KS",
    "000270.KS", "068270.KS", "028260.KS", "055550.KS", "035420.KS",
    "042660.KS", "012330.KS", "032830.KS", "015760.KS", "086790.KS",
]

# 미국 대형주 한글 종목명 사전 (신규 TOP 20 진입 대비)
US_KR_NAMES = {
    **{k: v["name"] for k, v in STOCKS.items() if v["currency"] == "USD"},
    "HD":   "홈디포",
    "CVX":  "셰브론",
    "NVO":  "노보노디스크",
    "SAP":  "SAP",
    "CSCO": "시스코",
    "PEP":  "펩시코",
    "LIN":  "린데",
    "AZN":  "아스트라제네카",
    "BABA": "알리바바",
    "SHEL": "셸",
    "ACN":  "액센츄어",
    "IBM":  "IBM",
    "GE":   "GE에어로스페이스",
    "CAT":  "캐터필러",
    "INTU": "인튜이트",
    "TXN":  "텍사스인스트루먼트",
    "BKNG": "부킹홀딩스",
    "UBER": "우버",
}

# PER이 의미 없는 티커 (채권·원자재·크립토·배당·지역 ETF)
NO_PER_TICKERS = {
    # 채권
    "TLT", "AGG", "HYG", "BIL", "273130.KS",
    # 원자재
    "GLD", "SLV", "CPER", "USO", "UNG", "DBC", "DBA", "PPLT", "WEAT", "411060.KS",
    # 크립토 코인 및 ETF
    "BTC-USD", "ETH-USD", "SOL-USD",
    "IBIT", "FBTC", "ETHA", "BITQ",
    # 배당·커버드콜 ETF
    "DGRO", "VIG", "SCHD", "SPYD", "JEPI", "JEPQ",
    # 지역 ETF
    "VGK", "EWJ", "EEM", "MCHI", "EWZ", "INDA", "EWY", "EWT",
    # 섹터 ETF
    "XLK", "XLV", "XLY", "XLP", "XLF", "XLI", "XLU", "XLB", "XLE", "XLC",
}


# ──────────────────────────────────────────────────────────
# 네이버 금융 (한국 종목 PER·배당률 및 시가총액 순위)
# ──────────────────────────────────────────────────────────
import re as _re
import requests as _requests

_NAVER_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}


def fetch_kr_top20():
    """네이버 금융에서 코스피 시가총액 상위 20개 종목(우선주·ETF 제외)을 동적으로 조회."""
    ranked = []
    try:
        url = 'https://m.stock.naver.com/api/stocks/marketValue/KOSPI?page=1&pageSize=50'
        r = _requests.get(url, headers=_NAVER_HEADERS, timeout=10)
        if r.status_code == 200:
            items = r.json().get('stocks', [])
            for it in items:
                if it.get('stockEndType') and it.get('stockEndType') != 'stock':
                    continue
                code = (it.get('itemCode') or '').strip()
                name = (it.get('stockName') or '').strip()
                if len(code) != 6 or not code.endswith('0'):
                    continue  # 우선주 제외 (보통주 코드는 0으로 끝남)
                if name.endswith(('우', '우B', '우C', '우(전환)')):
                    continue
                ticker = f"{code}.KS"
                clean_name = STOCKS.get(ticker, {}).get("name") or name
                ranked.append({"name": clean_name, "ticker": ticker, "currency": "KRW"})
                if len(ranked) >= 20:
                    break
    except Exception as e:
        print(f"  [Rank] KR TOP 20 조회 실패: {e}")

    if len(ranked) < 20:
        print("  [Rank] KR TOP 20 기본 목록으로 폴백")
        seen = {x["ticker"] for x in ranked}
        for t in DEFAULT_KR_TOP20:
            if t not in seen:
                ranked.append({
                    "name": STOCKS.get(t, {}).get("name", t),
                    "ticker": t,
                    "currency": "KRW",
                })
                if len(ranked) >= 20:
                    break

    return ranked[:20]


def _normalize_us_ticker(sym):
    """네이버/야후 미국 티커 표준화 및 동일 기업 중복 클래스 통합."""
    sym = _re.sub(r'[\s\.]+', '-', sym.strip().upper())
    if sym in ("GOOG", "GOOGL"):
        return "GOOGL"
    if sym in ("BRK-A", "BRK-B"):
        return "BRK-B"
    return sym


def _clean_kr_stock_name(ticker, raw_name):
    if ticker in US_KR_NAMES:
        return US_KR_NAMES[ticker]
    if ticker in STOCKS:
        return STOCKS[ticker]["name"]
    name = (raw_name or ticker).strip()
    name = _re.sub(r'\s*(Class\s*[A-Z]|ADR|보통주|우선주|\([A-Z]\))\s*$', '', name, flags=_re.IGNORECASE).strip()
    return name or ticker


def fetch_us_top20():
    """네이버 해외증시(NASDAQ + NYSE) 시가총액 순위를 조회하여 미국 상장 상위 20개 종목 반환."""
    candidates = {}  # ticker -> (market_value, item_dict)
    try:
        for exch in ("NASDAQ", "NYSE"):
            url = f'https://api.stock.naver.com/stock/exchange/{exch}/marketValue?page=1&pageSize=35'
            r = _requests.get(url, headers=_NAVER_HEADERS, timeout=10)
            if r.status_code != 200:
                continue
            items = r.json().get('stocks', [])
            for it in items:
                if it.get('stockEndType') and it.get('stockEndType') not in ('stock', 'equity'):
                    continue
                raw_sym = it.get('symbolCode') or it.get('reutersCode', '').split('.')[0]
                if not raw_sym:
                    continue
                ticker = _normalize_us_ticker(raw_sym)
                if ticker in NO_PER_TICKERS:
                    continue
                mv_raw = str(it.get('marketValue') or '0').replace(',', '').strip()
                try:
                    mv = float(mv_raw)
                except ValueError:
                    mv = 0.0
                name = _clean_kr_stock_name(ticker, it.get('stockName'))
                if ticker not in candidates or mv > candidates[ticker][0]:
                    candidates[ticker] = (mv, {"name": name, "ticker": ticker, "currency": "USD"})
    except Exception as e:
        print(f"  [Rank] US TOP 20 네이버 조회 실패: {e}")

    if len(candidates) >= 20:
        sorted_items = [item for _, item in sorted(candidates.values(), key=lambda x: x[0], reverse=True)]
        return sorted_items[:20]

    print("  [Rank] US TOP 20 기본 후보 목록으로 폴백")
    ranked = [item for _, item in sorted(candidates.values(), key=lambda x: x[0], reverse=True)]
    seen = {x["ticker"] for x in ranked}
    for t in DEFAULT_US_TOP20:
        if t not in seen:
            ranked.append({
                "name": _clean_kr_stock_name(t, t),
                "ticker": t,
                "currency": "USD",
            })
            if len(ranked) >= 20:
                break
    return ranked[:20]


def fetch_naver_bulk(code6_list):
    """네이버 금융으로 KR 종목 PER·배당률(분배율) 일괄 취득.
    반환: {code6: (per, div_yield)}

    - 주식: polling API (eps/dv 필드)
    - ETF:  ETF basic API (dividendYieldTtm 필드, PER=None)
    """
    result = {}

    # 1) polling API로 주식 데이터 취득
    etf_codes = []
    try:
        codes_str = ','.join(code6_list)
        url = f'https://polling.finance.naver.com/api/realtime?query=SERVICE_ITEM:{codes_str}'
        r = _requests.get(url, headers=_NAVER_HEADERS, timeout=10)
        if r.status_code == 200:
            items = r.json().get('result', {}).get('areas', [{}])[0].get('datas', [])
            for it in items:
                code = it.get('cd', '')
                nv  = it.get('nv') or 0
                eps = it.get('eps')
                dv  = it.get('dv')
                per = round(nv / eps, 1) if eps and eps > 0 and nv else None
                div_yield = round(dv / nv * 100, 2) if dv and dv > 0 and nv else None
                result[code] = (per, div_yield)
                if per is None and div_yield is None:
                    etf_codes.append(code)   # ETF로 추정 → 별도 조회
    except Exception as e:
        print(f'  [Naver] polling 실패: {e}')
        etf_codes = code6_list

    # 2) ETF basic API로 분배율 취득 (per=None 유지)
    for code in etf_codes:
        try:
            url = f'https://m.stock.naver.com/api/etf/{code}/basic'
            r = _requests.get(url, headers=_NAVER_HEADERS, timeout=6)
            if r.status_code != 200:
                continue
            d = r.json()
            raw = d.get('dividendYieldTtm')   # 이미 % 단위
            div_yield = round(float(raw), 2) if raw else None
            result[code] = (None, div_yield)
        except Exception:
            pass

    return result


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
# 히스토리 다운샘플 (5년 → 주봉)
# ──────────────────────────────────────────────────────────
def downsample_weekly(series):
    return series.resample('W').last().dropna()


# ──────────────────────────────────────────────────────────
# 메인 업데이트
# ──────────────────────────────────────────────────────────
def fetch_all():
    print(f"\n[StockScope] 데이터 업데이트 시작: {TODAY}")

    # 1) 시가총액 기준 TOP 20 / KR TOP 20 동적 조회 및 STOCKS 등록
    print("  [Rank] US TOP 20 & KR TOP 20 시가총액 순위 조회 중...")
    us_top20 = fetch_us_top20()
    kr_top20 = fetch_kr_top20()
    for item in us_top20 + kr_top20:
        t = item["ticker"]
        if t not in STOCKS:
            STOCKS[t] = {"name": item["name"], "currency": item["currency"]}

    all_tickers = list(STOCKS.keys())
    print(f"  [Rank] US TOP 20 (1~5위): {[x['ticker'] for x in us_top20[:5]]}")
    print(f"  [Rank] KR TOP 20 (1~5위): {[x['name'] for x in kr_top20[:5]]}")
    print(f"  총 {len(all_tickers)}개 티커 다운로드 중...")

    # 5년치 일봉 일괄 다운로드
    raw = yf.download(
        all_tickers,
        period="5y",
        auto_adjust=True,
        progress=True,
        group_by="ticker",
        threads=True,
    )

    result = {
        "updated": TODAY,
        "rankings": {
            "top20": us_top20,
            "kr-top20": kr_top20,
        },
        "stocks": {},
    }

    # 한국 종목 PER·배당률 일괄 조회 (네이버 금융)
    kr_codes = [t.split('.')[0] for t in all_tickers if t.endswith('.KS')]
    naver_data = fetch_naver_bulk(kr_codes)
    print(f"  [Naver] {len(naver_data)}/{len(kr_codes)}개 KR 종목 데이터 취득")

    # S&P500 벤치마크 다운로드 (미국 ETF 베타 계산용)
    print("  [Beta] ^GSPC (S&P500) 벤치마크 다운로드 중...")
    try:
        gspc_raw = yf.download("^GSPC", period="2y", auto_adjust=True, progress=False)
        gspc_hist = gspc_raw["Close"].squeeze().dropna()
    except Exception as e:
        print(f"  [Beta] ^GSPC 다운로드 실패: {e}")
        gspc_hist = None

    us_mcap = {}  # ticker -> marketCap (USD)

    for ticker in all_tickers:
        meta = STOCKS[ticker]
        try:
            # 멀티인덱스 처리
            if len(all_tickers) == 1:
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

            # 52주 고점 & MDD & YoY (연간 수익률)
            hist_1y = hist.iloc[-252:]
            high_52w = float(hist_1y.max())
            mdd_52w  = (price - high_52w) / high_52w * 100
            price_1y = float(hist_1y.iloc[0])
            year_pct = (price - price_1y) / price_1y * 100

            # YTD (해당 연도 첫 거래일 종가 대비)
            current_year = hist.index[-1].year
            hist_ytd = hist[hist.index.year == current_year]
            if not hist_ytd.empty and len(hist_ytd) >= 1:
                price_ytd_start = float(hist_ytd.iloc[0])
                ytd_pct = (price - price_ytd_start) / price_ytd_start * 100
            else:
                ytd_pct = None

            # 샤프 지수 (1년 기준)
            if len(hist) >= 30:
                daily_rets = hist.pct_change().dropna().iloc[-252:]
                annual_vol = daily_rets.std() * np.sqrt(252) * 100  # %로 변환
                sharpe = round((year_pct - RISK_FREE_RATE) / annual_vol, 2) if annual_vol > 0 else None
            else:
                sharpe = None

            # RSI
            rsi_series = calc_rsi(hist)
            rsi_clean  = rsi_series.dropna()
            rsi = float(rsi_clean.iloc[-1]) if not rsi_clean.empty else None
            rsi_30d = [round(float(v), 1) for v in rsi_clean.iloc[-30:].values] if not rsi_clean.empty else []

            # MACD histogram (가격 대비 % 정규화 → USD/KRW 비교 가능)
            macd_hist_series = calc_macd(hist)
            macd_clean = macd_hist_series.dropna()
            if len(macd_clean) >= 2:
                macd_hist = float(macd_clean.iloc[-1]) / price * 100
                macd_prev = float(macd_clean.iloc[-2]) / price * 100
                macd_up   = macd_hist > macd_prev
            else:
                macd_hist = None
                macd_up   = None
            if len(macd_clean) >= 2:
                macd_30d_series = macd_clean.iloc[-30:]
                hist_30d_aligned = hist.reindex(macd_30d_series.index)
                macd_30d = [round(float(v) / float(p) * 100, 4)
                            for v, p in zip(macd_30d_series.values, hist_30d_aligned.values)]
            else:
                macd_30d = []

            # 히스토리 배열 (스파크라인용, 소수점 2자리)
            def to_list(s):
                return [round(float(v), 2) for v in s.values]

            hist_30d_raw = hist.iloc[-30:]
            hist_1y_raw  = hist.iloc[-252:]
            hist_3y_raw  = downsample_weekly(hist)  # 주봉 다운샘플

            # 배당률 + PER
            if ticker.endswith('.KS'):
                # 한국 종목 → 네이버 금융 (사전 일괄 조회 결과 사용)
                code6 = ticker.split('.')[0]
                per, div_yield = naver_data.get(code6, (None, None))
                if ticker in NO_PER_TICKERS:
                    per = None
                upside_pct = None
                beta = None
            else:
                # 미국 종목 → yfinance
                try:
                    info = yf.Ticker(ticker).info
                    mcap = info.get('marketCap')
                    if mcap and mcap > 0:
                        us_mcap[ticker] = float(mcap)
                    div_rate = info.get('trailingAnnualDividendRate') or 0
                    div_yield = round(float(div_rate) / price * 100, 2) if div_rate and price else None
                    if div_yield is None:
                        # ETF 분배율은 dividendYield 필드(이미 % 단위)에 있음
                        dy = info.get('dividendYield')
                        div_yield = round(float(dy), 2) if dy else None
                    if div_yield and div_yield > 25:  # 25% 초과는 데이터 오류로 처리
                        div_yield = None
                    pe = info.get('trailingPE')
                    per = round(float(pe), 1) if pe and ticker not in NO_PER_TICKERS else None
                    target = info.get('targetMeanPrice')
                    upside_pct = round((float(target) - price) / price * 100, 1) if target and price else None
                    b = info.get('beta')
                    beta = round(float(b), 2) if b is not None else None
                    # yfinance beta가 None인 경우(주로 ETF) → S&P500 대비 직접 계산
                    if beta is None and gspc_hist is not None and len(hist) >= 100:
                        try:
                            stock_rets = hist.iloc[-252:].pct_change().dropna()
                            bench_rets = gspc_hist.pct_change().dropna()
                            aligned = stock_rets.index.intersection(bench_rets.index)
                            sr, br = stock_rets[aligned], bench_rets[aligned]
                            if len(sr) >= 100:
                                beta = round(float(np.cov(sr, br)[0, 1] / np.var(br, ddof=1)), 2)
                        except Exception:
                            pass
                except Exception:
                    div_yield = None
                    per = None
                    upside_pct = None
                    beta = None

            # 200일 이평선
            ma200_full = hist.rolling(200).mean()
            ma200_30d  = [round(float(v), 2) if pd.notna(v) else None for v in ma200_full.iloc[-30:].values]
            ma200_1y   = [round(float(v), 2) if pd.notna(v) else None for v in ma200_full.iloc[-252:].values]
            ma200_3y_weekly  = ma200_full.resample('W').last()
            ma200_3y_aligned = ma200_3y_weekly.reindex(hist_3y_raw.index)
            ma200_3y   = [round(float(v), 2) if pd.notna(v) else None for v in ma200_3y_aligned.values]

            result["stocks"][ticker] = {
                "name":       meta["name"],
                "currency":   meta["currency"],
                "price":      round(price, 2),
                "change_pct": round(change_pct, 2),
                "year_pct":   round(year_pct, 2),
                "ytd_pct":    round(ytd_pct, 2) if ytd_pct is not None else None,
                "mdd_52w":    round(mdd_52w, 2),
                "beta":       beta,
                "sharpe":     sharpe,
                "per":        per,
                "upside_pct": upside_pct,
                "div_yield":  div_yield,
                "rsi":        round(rsi, 1) if rsi is not None else None,
                "rsi_30d":    rsi_30d,
                "macd_hist":  round(macd_hist, 4) if macd_hist is not None else None,
                "macd_up":    bool(macd_up) if macd_up is not None else None,
                "macd_30d":   macd_30d,
                "hist_30d":   to_list(hist_30d_raw),
                "hist_1y":    to_list(hist_1y_raw),
                "hist_3y":    to_list(hist_3y_raw),
                "ma200_30d":  ma200_30d,
                "ma200_1y":   ma200_1y,
                "ma200_3y":   ma200_3y,
            }
            rsi_str  = f"{rsi:.1f}"  if rsi is not None  else "-"
            macd_str = f"{macd_hist:.3f}" if macd_hist is not None else "-"
            print(f"  OK {ticker:15s}  ${price:>10.2f}  daily:{change_pct:+.2f}%  RSI:{rsi_str}  MACD:{macd_str}")

        except Exception as e:
            print(f"  ERR {ticker}: {e}")
            result["stocks"][ticker] = {"name": meta["name"], "currency": meta["currency"]}

    # yfinance 시가총액(marketCap)이 충분히 수집된 경우 US TOP 20 순위를 최신 시가총액 기준으로 재정렬
    if len(us_mcap) >= 20:
        # us_top20 후보 + 전체 개별 미국 주식 중 시총 상위 20개 추출
        pool = {item["ticker"]: item for item in us_top20}
        for t, mcap in us_mcap.items():
            if t not in NO_PER_TICKERS and not t.endswith('.KS') and t not in ("VOO", "QQQ", "DIA", "IWM"):
                if t not in pool:
                    pool[t] = {"name": STOCKS[t]["name"], "ticker": t, "currency": "USD"}
        sorted_us = sorted(pool.values(), key=lambda x: us_mcap.get(x["ticker"], 0), reverse=True)
        result["rankings"]["top20"] = sorted_us[:20]

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
    print(f"\n  성공: {ok}/{len(data['stocks'])} 티커")

    save_json(data)
    print(f"  소요 시간: {time.time()-t0:.1f}초")
    print("  완료!\n")
