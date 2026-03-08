/* ============================================================
   config.js - StockScope 종목 그룹 설정
   ============================================================ */

const GROUPS = [
  {
    id: 'us-index',
    name: '주요지수',
    stocks: [
      { name: 'S&P500',     ticker: 'VOO' },
      { name: '나스닥100',  ticker: 'QQQ' },
      { name: '다우',       ticker: 'DIA' },
      { name: '러셀2000',   ticker: 'IWM' },
      { name: '장기국채',   ticker: 'TLT' },
      { name: '채권종합',   ticker: 'AGG' },
      { name: '하이일드채권', ticker: 'HYG' },
    ],
  },
  {
    id: 'top20',
    name: 'TOP 20',
    // 2026 기준 미국 시가총액 상위 20개 종목
    stocks: [
      { name: '애플',           ticker: 'AAPL' },   // ~$3.5T
      { name: '엔비디아',       ticker: 'NVDA' },   // ~$2.8T
      { name: '마이크로소프트', ticker: 'MSFT' },   // ~$2.7T
      { name: '아마존',         ticker: 'AMZN' },   // ~$2.2T
      { name: '구글',           ticker: 'GOOGL' },  // ~$2.0T
      { name: '메타',           ticker: 'META' },   // ~$1.7T
      { name: '테슬라',         ticker: 'TSLA' },   // ~$1.3T
      { name: 'TSMC',           ticker: 'TSM' },    // ~$1.0T
      { name: '브로드컴',       ticker: 'AVGO' },   // ~$0.8T
      { name: '버크셔해서웨이', ticker: 'BRK-B' },  // ~$0.75T
      { name: '일라이릴리',     ticker: 'LLY' },    // ~$0.7T
      { name: '월마트',         ticker: 'WMT' },    // ~$0.65T
      { name: 'JP모건',         ticker: 'JPM' },    // ~$0.6T
      { name: '비자',           ticker: 'V' },      // ~$0.55T
      { name: '마스터카드',     ticker: 'MA' },     // ~$0.5T
      { name: '유나이티드헬스', ticker: 'UNH' },    // ~$0.45T
      { name: '엑손모빌',       ticker: 'XOM' },    // ~$0.45T
      { name: '코스트코',       ticker: 'COST' },   // ~$0.4T
      { name: '오라클',         ticker: 'ORCL' },   // ~$0.4T
      { name: '넷플릭스',       ticker: 'NFLX' },   // ~$0.38T
    ],
  },
  {
    id: 'kr-top20',
    name: 'KR TOP 20',
    // 2025 기준 코스피 시가총액 상위 20개 (우선주 제외)
    stocks: [
      { name: '삼성전자',       ticker: '005930.KS', currency: 'KRW' },  // ~710조
      { name: 'SK하이닉스',     ticker: '000660.KS', currency: 'KRW' },  // ~474조
      { name: 'LG에너지솔루션', ticker: '373220.KS', currency: 'KRW' },  // ~86조
      { name: '삼성바이오로직스', ticker: '207940.KS', currency: 'KRW' }, // ~79조
      { name: '현대차',         ticker: '005380.KS', currency: 'KRW' },  // ~61조
      { name: 'HD현대중공업',   ticker: '329180.KS', currency: 'KRW' },  // ~53조
      { name: 'SK스퀘어',       ticker: '402340.KS', currency: 'KRW' },  // ~49조
      { name: '한화에어로스페이스', ticker: '012450.KS', currency: 'KRW' }, // ~49조
      { name: '두산에너빌리티', ticker: '034020.KS', currency: 'KRW' },  // ~48조
      { name: 'KB금융',         ticker: '105560.KS', currency: 'KRW' },  // ~48조
      { name: '기아',           ticker: '000270.KS', currency: 'KRW' },  // ~48조
      { name: '셀트리온',       ticker: '068270.KS', currency: 'KRW' },  // ~42조
      { name: '삼성물산',       ticker: '028260.KS', currency: 'KRW' },  // ~41조
      { name: 'NAVER',          ticker: '035420.KS', currency: 'KRW' },  // ~38조
      { name: '신한지주',       ticker: '055550.KS', currency: 'KRW' },  // ~37조
      { name: '한화오션',       ticker: '042660.KS', currency: 'KRW' },  // ~35조
      { name: '현대모비스',     ticker: '012330.KS', currency: 'KRW' },  // ~34조
      { name: '삼성생명',       ticker: '032830.KS', currency: 'KRW' },  // ~32조
      { name: '한국전력',       ticker: '015760.KS', currency: 'KRW' },  // ~30조
      { name: '하나금융지주',   ticker: '086790.KS', currency: 'KRW' },  // ~29조
    ],
  },
  {
    id: 'kr-etf',
    name: 'KR ETF',
    // 2025 기준 순자산 상위 국내 ETF (금리형 중복 제외)
    stocks: [
      { name: 'TIGER 미국S&P500',     ticker: '360750.KS', currency: 'KRW' },
      { name: 'TIGER 미국나스닥100',  ticker: '133690.KS', currency: 'KRW' },
      { name: 'TIGER 미국테크TOP10',  ticker: '381180.KS', currency: 'KRW' },
      { name: 'SOL 미국배당다우존스', ticker: '446720.KS', currency: 'KRW' },
      { name: 'KODEX 200',            ticker: '069500.KS', currency: 'KRW' },
      { name: 'KODEX 레버리지',       ticker: '122630.KS', currency: 'KRW' },
      { name: 'KODEX 인버스',         ticker: '114800.KS', currency: 'KRW' },
      { name: 'KODEX 인버스2X',       ticker: '252670.KS', currency: 'KRW' },
      { name: 'TIGER 원자재선물',     ticker: '139320.KS', currency: 'KRW' },
      { name: 'KODEX 종합채권',       ticker: '273130.KS', currency: 'KRW' },
      // 테마형
      { name: 'TIGER K방산&우주',     ticker: '463250.KS', currency: 'KRW' },
      { name: 'KODEX AI반도체',       ticker: '395160.KS', currency: 'KRW' },
      { name: 'KODEX 미국AI전력인프라', ticker: '487230.KS', currency: 'KRW' },
      { name: 'KODEX 로봇액티브',     ticker: '445290.KS', currency: 'KRW' },
      { name: 'TIGER 코스닥바이오',   ticker: '261070.KS', currency: 'KRW' },
      { name: 'SOL 미국양자컴퓨팅',   ticker: '0023A0.KS', currency: 'KRW' },
      { name: 'TIGER 비만치료제',     ticker: '476690.KS', currency: 'KRW' },
    ],
  },
  {
    id: 'sector',
    name: '섹터 ETF',
    stocks: [
      { name: '기술',       ticker: 'XLK' },
      { name: '헬스케어',   ticker: 'XLV' },
      { name: '경기소비재', ticker: 'XLY' },
      { name: '필수소비재', ticker: 'XLP' },
      { name: '금융',       ticker: 'XLF' },
      { name: '산업재',     ticker: 'XLI' },
      { name: '유틸리티',   ticker: 'XLU' },
      { name: '소재',       ticker: 'XLB' },
      { name: '에너지',     ticker: 'XLE' },
      { name: '커뮤니케이션', ticker: 'XLC' },
    ],
  },
  {
    id: 'commodity',
    name: '원자재 ETF',
    stocks: [
      { name: '금',       ticker: 'GLD' },
      { name: '은',       ticker: 'SLV' },
      { name: '구리',     ticker: 'CPER' },
      { name: 'WTI 원유', ticker: 'USO' },
      { name: '천연가스', ticker: 'UNG' },
      { name: '원자재종합', ticker: 'DBC' },
      { name: '농산물',   ticker: 'DBA' },
    ],
  },
  {
    id: 'dividend',
    name: '배당 ETF',
    stocks: [
      { name: '배당성장 5년', ticker: 'DGRO' },
      { name: '배당성장 10년', ticker: 'VIG' },
      { name: '배당우량',     ticker: 'SCHD' },
      { name: '고배당',       ticker: 'SPYD' },
    ],
  },
  {
    id: 'regional',
    name: '지역 ETF',
    stocks: [
      { name: '유럽',    ticker: 'VGK' },
      { name: '일본',    ticker: 'EWJ' },
      { name: '신흥국',  ticker: 'EEM' },
      { name: '중국',    ticker: 'KWEB' },
      { name: '브라질',  ticker: 'EWZ' },
    ],
  },
  {
    id: 'crypto',
    name: '크립토',
    stocks: [
      { name: '비트코인 ETF',   ticker: 'IBIT' },   // BlackRock BTC ETF
      { name: '비트코인 ETF-F', ticker: 'FBTC' },   // Fidelity BTC ETF
      { name: '이더리움 ETF',   ticker: 'ETHA' },   // BlackRock ETH ETF
      { name: '코인베이스',     ticker: 'COIN' },   // 거래소 + USDC 스테이블코인
      { name: '스트래티지',     ticker: 'MSTR' },   // BTC 대량 보유 (구 MicroStrategy)
      { name: '마라톤 디지털',  ticker: 'MARA' },   // BTC 채굴
      { name: '라이엇 플랫폼',  ticker: 'RIOT' },   // BTC 채굴
      { name: '클린스파크',     ticker: 'CLSK' },   // BTC 채굴
      { name: '로빈후드',       ticker: 'HOOD' },   // 크립토 거래 + 스테이블코인
      { name: '크립토 기업 ETF', ticker: 'BITQ' },  // Bitwise 크립토 기업 ETF
      // 스테이블코인 관련
      { name: '서클',           ticker: 'CRCL' },  // USDC 발행사
      { name: '페이팔',         ticker: 'PYPL' },  // PYUSD 스테이블코인
    ],
  },
  {
    id: 'bigtech',
    name: '빅테크',
    stocks: [
      { name: '애플',           ticker: 'AAPL' },
      { name: '마이크로소프트', ticker: 'MSFT' },
      { name: '구글',           ticker: 'GOOGL' },
      { name: '아마존',         ticker: 'AMZN' },
      { name: '테슬라',         ticker: 'TSLA' },
      { name: '메타',           ticker: 'META' },
      { name: '엔비디아',       ticker: 'NVDA' },
    ],
  },
  {
    id: 'semiconductor',
    name: '반도체',
    stocks: [
      { name: '엔비디아', ticker: 'NVDA' },
      { name: '브로드컴', ticker: 'AVGO' },
      { name: 'ASML',    ticker: 'ASML' },
      { name: 'AMD',     ticker: 'AMD' },
      { name: 'TSMC',    ticker: 'TSM' },
      { name: '인텔',    ticker: 'INTC' },
      { name: '퀄컴',    ticker: 'QCOM' },
    ],
  },
  {
    id: 'finance',
    name: '결제·금융',
    stocks: [
      { name: 'JP모건',    ticker: 'JPM' },
      { name: '비자',      ticker: 'V' },
      { name: '마스터카드', ticker: 'MA' },
      { name: '페이팔',    ticker: 'PYPL' },
      { name: 'BOA',       ticker: 'BAC' },
    ],
  },
  {
    id: 'auto',
    name: '자동차·EV',
    stocks: [
      { name: '테슬라',  ticker: 'TSLA' },
      { name: '포드',    ticker: 'F' },
      { name: 'GM',      ticker: 'GM' },
      { name: '리비안',  ticker: 'RIVN' },
    ],
  },
  {
    id: 'media',
    name: '미디어·통신',
    stocks: [
      { name: '넷플릭스', ticker: 'NFLX' },
      { name: '디즈니',   ticker: 'DIS' },
      { name: '버라이즌', ticker: 'VZ' },
      { name: 'AT&T',     ticker: 'T' },
    ],
  },
  {
    id: 'software',
    name: 'SW·클라우드',
    stocks: [
      { name: '어도비',     ticker: 'ADBE' },
      { name: '세일즈포스', ticker: 'CRM' },
      { name: '오토데스크', ticker: 'ADSK' },
      { name: '팔란티어',   ticker: 'PLTR' },
    ],
  },
  {
    id: 'consumer',
    name: '소비재',
    stocks: [
      { name: '월마트',    ticker: 'WMT' },
      { name: '코스트코',  ticker: 'COST' },
      { name: '맥도날드',  ticker: 'MCD' },
      { name: '나이키',    ticker: 'NKE' },
      { name: '스타벅스',  ticker: 'SBUX' },
      { name: '코카콜라',  ticker: 'KO' },
    ],
  },
  {
    id: 'healthcare',
    name: '헬스케어',
    stocks: [
      { name: '유나이티드헬스', ticker: 'UNH' },
      { name: '존슨앤존슨',    ticker: 'JNJ' },
      { name: '화이자',        ticker: 'PFE' },
      { name: '일라이릴리',    ticker: 'LLY' },
    ],
  },
];

// 모든 유니크 티커 추출
const ALL_TICKERS = [...new Set(GROUPS.flatMap(g => g.stocks.map(s => s.ticker)))];

// 티커 → 종목명 매핑 (중복 시 첫 번째 우선)
const TICKER_NAMES = {};
GROUPS.forEach(g => g.stocks.forEach(s => {
  if (!TICKER_NAMES[s.ticker]) TICKER_NAMES[s.ticker] = s.name;
}));

// 티커 → 통화 매핑
const TICKER_CURRENCY = {};
GROUPS.forEach(g => g.stocks.forEach(s => {
  TICKER_CURRENCY[s.ticker] = s.currency || 'USD';
}));
