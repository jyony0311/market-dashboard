import streamlit as st
import pandas as pd
import re
import time

try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except Exception:
    PLOTLY_AVAILABLE = False


st.set_page_config(
    page_title="BizDoctor",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================
# 디자인 CSS
# =========================
st.markdown("""
<style>
    html, body, [class*="css"] {
        font-family: Pretendard, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(124, 58, 237, 0.18), transparent 30%),
            radial-gradient(circle at top right, rgba(37, 99, 235, 0.14), transparent 28%),
            linear-gradient(180deg, #F8FAFC 0%, #EEF2FF 100%);
    }

    section[data-testid="stSidebar"] {
        background: rgba(255,255,255,0.78);
        backdrop-filter: blur(18px);
        border-right: 1px solid rgba(148,163,184,0.28);
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 38px;
        border-radius: 32px;
        color: white;
        background:
            radial-gradient(circle at 12% 20%, rgba(96,165,250,0.55), transparent 28%),
            radial-gradient(circle at 92% 12%, rgba(168,85,247,0.58), transparent 30%),
            linear-gradient(135deg, #020617 0%, #0F172A 38%, #312E81 100%);
        box-shadow: 0 25px 80px rgba(15,23,42,0.25);
        margin-bottom: 24px;
    }

    .eyebrow {
        display: inline-flex;
        padding: 7px 14px;
        border-radius: 999px;
        background: rgba(255,255,255,0.13);
        border: 1px solid rgba(255,255,255,0.18);
        font-size: 13px;
        font-weight: 800;
        color: #DBEAFE;
        margin-bottom: 16px;
    }

    .hero-title {
        font-size: 60px;
        line-height: 1.05;
        font-weight: 950;
        letter-spacing: -2.6px;
        margin-bottom: 14px;
    }

    .hero-title span {
        background: linear-gradient(90deg, #60A5FA, #A78BFA, #F0ABFC);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-sub {
        font-size: 19px;
        color: #CBD5E1;
        max-width: 850px;
        line-height: 1.65;
        margin-bottom: 22px;
    }

    .hero-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 14px;
        margin-top: 20px;
    }

    .hero-mini {
        padding: 16px 17px;
        border-radius: 19px;
        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.16);
    }

    .hero-mini b {
        display: block;
        font-size: 15px;
        margin-bottom: 6px;
    }

    .hero-mini span {
        font-size: 13px;
        color: #CBD5E1;
        line-height: 1.45;
    }

    .section-title {
        font-size: 25px;
        font-weight: 900;
        letter-spacing: -0.8px;
        margin: 12px 0 14px 0;
        color: #0F172A;
    }

    .metric-card {
        min-height: 132px;
        padding: 23px;
        border-radius: 25px;
        background: rgba(255,255,255,0.86);
        border: 1px solid rgba(226,232,240,0.95);
        box-shadow: 0 16px 38px rgba(15,23,42,0.08);
    }

    .metric-label {
        font-size: 14px;
        color: #64748B;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 38px;
        color: #111827;
        font-weight: 950;
        letter-spacing: -1.5px;
        margin-bottom: 5px;
    }

    .metric-sub {
        font-size: 13px;
        color: #64748B;
        font-weight: 650;
        line-height: 1.5;
    }

    .comparison-card {
        padding: 24px;
        border-radius: 26px;
        background: white;
        border: 1px solid #E2E8F0;
        box-shadow: 0 18px 45px rgba(15,23,42,0.07);
        margin-bottom: 18px;
    }

    .comparison-title {
        font-size: 17px;
        font-weight: 900;
        color: #334155;
        margin-bottom: 16px;
    }

    .comparison-row {
        display: flex;
        justify-content: space-between;
        gap: 14px;
        padding: 10px 0;
        border-bottom: 1px dashed #E2E8F0;
        font-weight: 750;
        color: #475569;
    }

    .comparison-row b {
        color: #0F172A;
        text-align: right;
    }

    .problem-card {
        padding: 16px 17px;
        border-radius: 18px;
        background: #FFF7ED;
        border: 1px solid #FED7AA;
        color: #9A3412;
        font-weight: 750;
        margin-bottom: 10px;
        line-height: 1.55;
    }

    .success-card {
        padding: 16px 17px;
        border-radius: 18px;
        background: #ECFDF5;
        border: 1px solid #A7F3D0;
        color: #047857;
        font-weight: 750;
        margin-bottom: 10px;
        line-height: 1.55;
    }

    .grade-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 9px 16px;
        border-radius: 999px;
        background: linear-gradient(135deg, #EEF2FF, #E0E7FF);
        color: #4338CA;
        font-size: 18px;
        font-weight: 950;
        border: 1px solid #C7D2FE;
    }

    .chat-wrap {
        padding: 24px;
        border-radius: 27px;
        background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%);
        border: 1px solid #E2E8F0;
        box-shadow: 0 18px 50px rgba(15,23,42,0.08);
        margin-bottom: 18px;
    }

    .user-bubble {
        max-width: 72%;
        margin-left: auto;
        padding: 16px 18px;
        border-radius: 22px 22px 6px 22px;
        background: linear-gradient(135deg, #2563EB, #7C3AED);
        color: white;
        font-weight: 800;
        line-height: 1.55;
        margin-bottom: 14px;
    }

    .ai-bubble {
        max-width: 88%;
        padding: 18px 20px;
        border-radius: 22px 22px 22px 6px;
        background: #F1F5F9;
        color: #0F172A;
        font-weight: 650;
        line-height: 1.65;
        margin-bottom: 14px;
        border: 1px solid #E2E8F0;
    }

    .strategy-card {
        padding: 18px 19px;
        border-radius: 20px;
        background: white;
        border: 1px solid #E2E8F0;
        box-shadow: 0 12px 30px rgba(15,23,42,0.06);
        margin-bottom: 12px;
    }

    .strategy-number {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 31px;
        height: 31px;
        border-radius: 10px;
        background: linear-gradient(135deg, #2563EB, #7C3AED);
        color: white;
        font-weight: 950;
        margin-right: 8px;
    }

    .impact {
        text-align: center;
        padding: 28px;
        border-radius: 28px;
        background: linear-gradient(135deg, #020617, #312E81);
        color: white;
        box-shadow: 0 20px 55px rgba(15,23,42,0.22);
    }

    .impact-number {
        font-size: 46px;
        font-weight: 950;
        letter-spacing: -1.8px;
        background: linear-gradient(90deg, #60A5FA, #A78BFA, #F0ABFC);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .report-card {
        padding: 25px;
        border-radius: 25px;
        background: white;
        border: 1px solid #E2E8F0;
        box-shadow: 0 18px 45px rgba(15,23,42,0.07);
        line-height: 1.75;
    }

    .step-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 14px;
    }

    .step-card {
        padding: 18px;
        border-radius: 20px;
        background: rgba(255,255,255,0.86);
        border: 1px solid #E2E8F0;
        box-shadow: 0 12px 30px rgba(15,23,42,0.06);
    }

    .step-icon {
        font-size: 28px;
        font-weight: 950;
        margin-bottom: 8px;
        color: #4F46E5;
    }

    .step-card b {
        display: block;
        font-size: 16px;
        margin-bottom: 5px;
        color: #0F172A;
    }

    .step-card span {
        font-size: 13px;
        color: #64748B;
        line-height: 1.5;
    }

    @media (max-width: 900px) {
        .hero-grid, .step-grid {
            grid-template-columns: 1fr;
        }
        .hero-title {
            font-size: 42px;
        }
    }
</style>
""", unsafe_allow_html=True)


# =========================
# 엑셀 자동 추출
# =========================
LABEL_MAP = {
    "sales": ["월매출", "월 매출", "매출액", "매출"],
    "other_cost": ["기타운영비", "기타 운영비", "기타비용", "운영비", "재료비", "관리비"],
    "total_cost_raw": ["월총비용", "월 총비용", "총비용", "비용합계"],
    "rent": ["임대료", "월세", "임차료", "월 임대료"],
    "labor_cost": ["인건비", "급여", "직원급여", "월 인건비"],
    "staff": ["직원수", "직원 수", "종업원", "인원"],
    "customers": ["일방문자수", "일 방문자 수", "방문자수", "방문객", "고객수"],
    "repeat_customers": ["재방문고객수", "재방문 고객 수", "재방문자수", "재방문자", "단골고객수", "단골 고객 수"],
    "avg_price": ["객단가", "평균구매액", "평균 구매액"]
}

KOREAN_LABEL = {
    "sales": "월 매출(만원)",
    "other_cost": "기타 운영비(만원)",
    "rent": "월 임대료(만원)",
    "labor_cost": "월 인건비(만원)",
    "staff": "직원 수",
    "customers": "일 방문자 수",
    "repeat_customers": "일 재방문 고객 수",
    "avg_price": "객단가(원)"
}


def normalize_text(text):
    return re.sub(r"\s+", "", str(text)).lower()


def parse_number(value):
    if pd.isna(value):
        return None

    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).replace(",", "").strip()

    if not re.search(r"\d", text):
        return None

    match = re.search(r"-?\d+(\.\d+)?", text)
    if match:
        return float(match.group())

    return None


def adjust_unit(num, raw_value, key):
    raw_text = str(raw_value)

    if key in ["sales", "other_cost", "total_cost_raw", "rent", "labor_cost"]:
        if "원" in raw_text and "만원" not in raw_text and num >= 10000:
            num = num / 10000
        elif num >= 100000:
            num = num / 10000

    return int(round(num))


def find_nearby_number(df, row, col, key):
    candidates = []

    for c in range(col + 1, min(col + 6, df.shape[1])):
        raw = df.iat[row, c]
        num = parse_number(raw)
        if num is not None:
            candidates.append((num, raw))

    for r in range(row + 1, min(row + 5, df.shape[0])):
        raw = df.iat[r, col]
        num = parse_number(raw)
        if num is not None:
            candidates.append((num, raw))

    if candidates:
        num, raw = candidates[0]
        return adjust_unit(num, raw, key)

    return None


def extract_excel_values(uploaded_file):
    results = {}

    try:
        xls = pd.ExcelFile(uploaded_file)

        for sheet in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet, header=None)

            for r in range(df.shape[0]):
                for c in range(df.shape[1]):
                    cell = df.iat[r, c]
                    cell_text = normalize_text(cell)

                    for key, labels in LABEL_MAP.items():
                        if key in results:
                            continue

                        for label in labels:
                            if normalize_text(label) in cell_text:
                                num = parse_number(cell)

                                if num is not None:
                                    results[key] = adjust_unit(num, cell, key)
                                else:
                                    nearby = find_nearby_number(df, r, c, key)
                                    if nearby is not None:
                                        results[key] = nearby

        if "total_cost_raw" in results and "other_cost" not in results:
            rent = results.get("rent", 0)
            labor = results.get("labor_cost", 0)
            results["other_cost"] = max(0, results["total_cost_raw"] - rent - labor)

        results.pop("total_cost_raw", None)

        return results

    except Exception as e:
        st.sidebar.error("엑셀 파일을 읽는 중 오류가 발생했습니다.")
        st.sidebar.write(e)
        return {}


# =========================
# 진단 로직
# =========================
def calculate_revisit_rate(customers, repeat_customers):
    if customers <= 0:
        return 0
    rate = int(round((repeat_customers / customers) * 100))
    return max(0, min(100, rate))


def calculate_marketing_score(marketing_channels, posting_frequency, review_management):
    channel_score = min(len(marketing_channels) * 12, 50)

    frequency_score_map = {
        "거의 안 함": 5,
        "월 1~2회": 15,
        "주 1~2회": 25,
        "주 3회 이상": 30
    }

    review_score_map = {
        "거의 안 함": 5,
        "가끔 답변": 10,
        "정기적으로 답변": 15,
        "리뷰 이벤트와 연계": 20
    }

    score = (
        channel_score +
        frequency_score_map.get(posting_frequency, 5) +
        review_score_map.get(review_management, 5)
    )

    return min(100, score)


def score_profit(margin):
    if margin >= 30:
        return 90
    elif margin >= 20:
        return 75
    elif margin >= 10:
        return 60
    else:
        return 40


def score_cost(cost_ratio):
    if cost_ratio <= 60:
        return 90
    elif cost_ratio <= 70:
        return 75
    elif cost_ratio <= 80:
        return 60
    else:
        return 40


def score_labor(labor_ratio):
    if labor_ratio <= 25:
        return 90
    elif labor_ratio <= 35:
        return 75
    elif labor_ratio <= 45:
        return 60
    else:
        return 40


def score_rent(rent_ratio):
    if rent_ratio <= 10:
        return 90
    elif rent_ratio <= 15:
        return 75
    elif rent_ratio <= 20:
        return 60
    else:
        return 40


def grade(total):
    if total >= 85:
        return "A"
    elif total >= 70:
        return "B"
    elif total >= 55:
        return "C"
    else:
        return "D"


def grade_comment(total):
    if total >= 85:
        return "우수한 경영 상태입니다."
    elif total >= 70:
        return "기본 구조는 양호하나 개선 여지가 있습니다."
    elif total >= 55:
        return "핵심 지표 개선이 필요한 상태입니다."
    else:
        return "전반적인 경영 구조 점검이 필요합니다."


def analyze_business(
    sales,
    other_cost,
    rent,
    labor_cost,
    staff,
    customers,
    repeat_customers,
    avg_price,
    marketing_channels,
    posting_frequency,
    review_management
):
    total_cost = other_cost + rent + labor_cost
    revisit_rate = calculate_revisit_rate(customers, repeat_customers)
    marketing_score = calculate_marketing_score(marketing_channels, posting_frequency, review_management)

    profit = sales - total_cost
    margin = (profit / sales) * 100 if sales > 0 else 0
    cost_ratio = (total_cost / sales) * 100 if sales > 0 else 0
    other_cost_ratio = (other_cost / sales) * 100 if sales > 0 else 0
    rent_ratio = (rent / sales) * 100 if sales > 0 else 0
    labor_ratio = (labor_cost / sales) * 100 if sales > 0 else 0

    profitability = score_profit(margin)
    cost_efficiency = score_cost(cost_ratio)
    labor_efficiency = score_labor(labor_ratio)
    rent_stability = score_rent(rent_ratio)
    customer_score = revisit_rate
    marketing = marketing_score
    growth = int((customer_score + marketing) / 2)

    total_score = int(
        profitability * 0.25 +
        cost_efficiency * 0.20 +
        labor_efficiency * 0.15 +
        customer_score * 0.15 +
        marketing * 0.10 +
        rent_stability * 0.10 +
        growth * 0.05
    )

    problems = []
    strategies = []

    if profitability < 65:
        problems.append("수익성이 낮아 매출 대비 실제 이익 창출 능력이 부족합니다.")
        strategies.append("객단가를 높일 수 있는 세트 메뉴, 프리미엄 메뉴, 추가 구매 전략을 도입합니다.")

    if cost_efficiency < 65:
        problems.append("월 총비용 비율이 높아 비용 효율성이 낮습니다.")
        strategies.append("기타 운영비, 임대료, 인건비를 분리하여 비용 절감 우선순위를 설정합니다.")

    if labor_efficiency < 65:
        problems.append("인건비 부담이 높아 수익성이 약화되고 있습니다.")
        strategies.append("직원 근무 시간과 업무 배치를 재조정하여 인건비 효율을 개선합니다.")

    if rent_stability < 65:
        problems.append("매출 대비 임대료 부담이 높아 고정비 안정성이 낮습니다.")
        strategies.append("임대료 부담을 고려하여 매출 목표 재설정 또는 공간 활용 효율화를 검토합니다.")

    if customer_score < 50:
        problems.append("재방문율이 낮아 고객 유지 전략이 필요합니다.")
        strategies.append("스탬프 쿠폰, 멤버십, 단골 이벤트를 통해 재방문율을 높입니다.")

    if marketing < 50:
        problems.append("마케팅 활용도가 낮아 신규 고객 유입이 부족할 수 있습니다.")
        strategies.append("SNS 홍보, 리뷰 이벤트, 지역 타깃 홍보를 통해 신규 고객 유입을 강화합니다.")

    if len(problems) == 0:
        problems.append("현재 경영 상태는 비교적 안정적입니다.")
        strategies.append("현재 구조를 유지하되, 매출 변화와 비용 구조를 지속적으로 모니터링합니다.")

    return {
        "sales": sales,
        "other_cost": other_cost,
        "rent": rent,
        "labor_cost": labor_cost,
        "total_cost": total_cost,
        "staff": staff,
        "customers": customers,
        "repeat_customers": repeat_customers,
        "avg_price": avg_price,
        "revisit_rate": revisit_rate,
        "marketing_channels": marketing_channels,
        "posting_frequency": posting_frequency,
        "review_management": review_management,
        "marketing_score": marketing_score,
        "profit": profit,
        "margin": margin,
        "cost_ratio": cost_ratio,
        "other_cost_ratio": other_cost_ratio,
        "rent_ratio": rent_ratio,
        "labor_ratio": labor_ratio,
        "profitability": profitability,
        "cost_efficiency": cost_efficiency,
        "labor_efficiency": labor_efficiency,
        "customer_score": customer_score,
        "marketing": marketing,
        "rent_stability": rent_stability,
        "growth": growth,
        "total_score": total_score,
        "grade": grade(total_score),
        "grade_comment": grade_comment(total_score),
        "problems": problems,
        "strategies": strategies
    }


def metric_card(label, value, sub=""):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)


def make_report_text(r):
    channels_text = ", ".join(r["marketing_channels"]) if r["marketing_channels"] else "활용 채널 없음"
    consulting = generate_ai_consulting(r)

    roadmap_week = " / ".join(consulting["one_week"])
    roadmap_month = " / ".join(consulting["one_month"])
    roadmap_quarter = " / ".join(consulting["three_month"])
    actions_text = chr(10).join([f"- {a}" for a in consulting["actions"]])

    return f"""
[BizDoctor One-Page 경영 진단 리포트]

■ 1. 핵심 요약
- 종합 진단: {r['total_score']}점 / {r['grade']}등급
- 한 줄 의견: {consulting['summary']}
- 우선 개선 영역: {consulting['priority_text']}

■ 2. 주요 숫자
- 월 매출: {r['sales']:,}만원
- 월 총비용: {r['total_cost']:,}만원
- 월 순이익: {r['profit']:,}만원
- 수익률: {r['margin']:.1f}%
- 총비용 비율: {r['cost_ratio']:.1f}%

■ 3. 비용 구조
- 기타 운영비: {r['other_cost']:,}만원 ({r['other_cost_ratio']:.1f}%)
- 임대료: {r['rent']:,}만원 ({r['rent_ratio']:.1f}%)
- 인건비: {r['labor_cost']:,}만원 ({r['labor_ratio']:.1f}%)

■ 4. 고객·마케팅 지표
- 일 방문자 수: {r['customers']}명
- 일 재방문 고객 수: {r['repeat_customers']}명
- 재방문율: {r['revisit_rate']}%
- 마케팅 채널: {channels_text}
- 업데이트 빈도: {r['posting_frequency']}
- 리뷰 관리: {r['review_management']}
- 마케팅 활용도: {r['marketing_score']}점

■ 5. 우선 실행 전략
{actions_text}

■ 6. 실행 로드맵
- 이번 주: {roadmap_week}
- 1개월 내: {roadmap_month}
- 3개월 내: {roadmap_quarter}

■ 7. 메모
본 리포트는 입력된 경영 데이터를 기반으로 한 캡스톤 디자인 프로토타입 결과입니다.
실제 경영 성과와 차이가 있을 수 있으며, 의사결정 보조 자료로 활용할 수 있습니다.
"""


# =========================
# AI 컨설팅 생성 로직
# =========================
def generate_ai_consulting(r):
    consulting = []
    priorities = []
    action_plan = []

    # 수익성 분석
    if r["margin"] < 10:
        consulting.append(f"수익률이 {r['margin']:.1f}%로 낮습니다. 월 매출 {r['sales']:,}만원 중 총비용이 {r['total_cost']:,}만원을 차지해 실제 남는 이익이 부족한 구조입니다. 단순 매출 증가보다 비용 구조 조정과 객단가 개선이 우선입니다.")
        priorities.append(("수익성 개선", r["profitability"]))
        action_plan.append("대표 메뉴 구성 재검토, 세트 메뉴·추가 옵션 도입, 저마진 상품 축소")
    elif r["margin"] < 20:
        consulting.append(f"수익률은 {r['margin']:.1f}%로 보통 수준이지만 안정적인 이익 구조라고 보기는 어렵습니다. 비용이 조금만 증가해도 순이익이 빠르게 줄어들 수 있습니다.")
        priorities.append(("수익률 안정화", r["profitability"]))
        action_plan.append("원가율 높은 항목 점검, 객단가 상승 상품 추가, 할인 이벤트 남발 제한")
    else:
        consulting.append(f"수익률은 {r['margin']:.1f}%로 비교적 양호합니다. 현재는 이익 구조를 유지하면서 고객 유지율과 마케팅 효율을 높이는 전략이 적합합니다.")

    # 비용 구조 분석
    if r["cost_ratio"] > 80:
        consulting.append(f"총비용 비율이 {r['cost_ratio']:.1f}%로 매우 높습니다. 매출의 대부분이 비용으로 빠져나가고 있어 비용 효율성 지표가 낮게 평가됩니다. 기타 운영비 {r['other_cost']:,}만원, 임대료 {r['rent']:,}만원, 인건비 {r['labor_cost']:,}만원 중 절감 가능성이 큰 항목부터 점검해야 합니다.")
        priorities.append(("총비용 절감", r["cost_efficiency"]))
        action_plan.append("고정비·변동비 분리표 작성, 재료비/관리비 월별 비교, 불필요한 구독·소모품 비용 정리")
    elif r["cost_ratio"] > 70:
        consulting.append(f"총비용 비율이 {r['cost_ratio']:.1f}%로 다소 높은 편입니다. 비용 통제 없이는 매출이 증가해도 순이익 증가 폭이 제한될 수 있습니다.")
        priorities.append(("비용 효율 관리", r["cost_efficiency"]))
        action_plan.append("월별 비용 항목을 3개 그룹으로 나누고, 절감 목표를 5~10%로 설정")
    else:
        consulting.append(f"총비용 비율은 {r['cost_ratio']:.1f}%로 비교적 안정적입니다. 현재 비용 구조를 유지하면서 매출 확대 전략을 병행할 수 있습니다.")

    # 인건비 분석
    if r["labor_ratio"] > 45:
        consulting.append(f"인건비율이 {r['labor_ratio']:.1f}%로 높습니다. 직원 수 {r['staff']}명 기준으로 현재 매출 대비 인력 운영 부담이 큽니다. 시간대별 방문자 수를 기준으로 근무 배치를 조정할 필요가 있습니다.")
        priorities.append(("인건비 효율화", r["labor_efficiency"]))
        action_plan.append("피크타임/비피크타임 구분, 시간대별 근무표 조정, 반복 업무 자동화 또는 셀프 주문 방식 검토")
    elif r["labor_ratio"] > 35:
        consulting.append(f"인건비율은 {r['labor_ratio']:.1f}%로 주의가 필요합니다. 인력을 줄이기보다는 업무 배치와 시간 운영 효율을 먼저 점검하는 것이 좋습니다.")
        priorities.append(("근무 배치 최적화", r["labor_efficiency"]))
        action_plan.append("요일별 방문자 수 확인, 직원별 역할 분담표 작성, 한가한 시간대 근무시간 조정")
    else:
        consulting.append(f"인건비율은 {r['labor_ratio']:.1f}%로 비교적 안정적입니다. 현재 인력 운영 구조는 큰 문제보다 유지·관리 관점에서 접근하면 됩니다.")

    # 임대료 분석
    if r["rent_ratio"] > 20:
        consulting.append(f"임대료율이 {r['rent_ratio']:.1f}%로 높습니다. 임대료는 단기간에 줄이기 어려운 고정비이므로, 동일 공간에서 더 많은 매출을 만드는 공간 활용 전략이 필요합니다.")
        priorities.append(("고정비 부담 완화", r["rent_stability"]))
        action_plan.append("공간 회전율 개선, 비는 시간대 예약/이벤트 운영, 테이블 회전 시간 단축 전략 검토")
    elif r["rent_ratio"] > 15:
        consulting.append(f"임대료율은 {r['rent_ratio']:.1f}%로 다소 부담이 있습니다. 매출이 감소하면 고정비 부담이 빠르게 커질 수 있으므로 안정 매출 확보가 중요합니다.")
        priorities.append(("임대료 안정성 관리", r["rent_stability"]))
        action_plan.append("평일 비수기 프로모션, 예약 고객 확보, 단골 고객 대상 재방문 혜택 운영")
    else:
        consulting.append(f"임대료율은 {r['rent_ratio']:.1f}%로 안정적인 편입니다. 고정비 부담보다 고객 확보와 객단가 개선에 집중할 여지가 있습니다.")

    # 재방문율 분석
    if r["revisit_rate"] < 30:
        consulting.append(f"재방문율이 {r['revisit_rate']}%로 낮습니다. 일 방문자 {r['customers']}명 중 재방문 고객이 {r['repeat_customers']}명에 그쳐 신규 고객 유입에 의존하는 구조일 가능성이 큽니다. 단골화 전략이 가장 중요합니다.")
        priorities.append(("재방문율 개선", r["customer_score"]))
        action_plan.append("스탬프 쿠폰, 재방문 할인, 2회 방문 고객 대상 혜택, 단골 고객 리스트 관리")
    elif r["revisit_rate"] < 50:
        consulting.append(f"재방문율은 {r['revisit_rate']}%로 개선 여지가 있습니다. 이미 방문한 고객이 다시 올 이유를 명확히 만들어야 합니다.")
        priorities.append(("고객 유지 강화", r["customer_score"]))
        action_plan.append("후기 작성 고객 쿠폰, 생일/기념일 혜택, 시즌 메뉴 재방문 유도")
    else:
        consulting.append(f"재방문율은 {r['revisit_rate']}%로 양호합니다. 기존 고객 유지 기반이 있으므로 단골 고객을 통한 추천 유입 전략을 강화할 수 있습니다.")

    # 마케팅 분석
    channels_text = ", ".join(r["marketing_channels"]) if r["marketing_channels"] else "활용 채널 없음"
    if r["marketing_score"] < 50:
        consulting.append(f"마케팅 활용도는 {r['marketing_score']}점으로 낮습니다. 현재 활용 채널은 {channels_text}이며, 업데이트 빈도는 {r['posting_frequency']}, 리뷰 관리는 {r['review_management']} 수준입니다. 신규 고객 유입을 위해 온라인 노출을 강화해야 합니다.")
        priorities.append(("마케팅 활성화", r["marketing"]))
        action_plan.append("네이버 플레이스 정보 최신화, 인스타그램 주 2회 게시, 리뷰 답변 루틴화, 후기 이벤트 운영")
    elif r["marketing_score"] < 75:
        consulting.append(f"마케팅 활용도는 {r['marketing_score']}점으로 보통 수준입니다. 채널은 활용하고 있지만 운영 빈도나 리뷰 관리가 더 체계화되면 유입 효과를 높일 수 있습니다.")
        priorities.append(("마케팅 운영 체계화", r["marketing"]))
        action_plan.append("채널별 역할 분리: 네이버는 검색 유입, 인스타그램은 이미지 홍보, 리뷰는 신뢰도 강화")
    else:
        consulting.append(f"마케팅 활용도는 {r['marketing_score']}점으로 양호합니다. 현재 채널 운영을 유지하면서 성과가 좋은 채널에 집중하는 것이 좋습니다.")

    priorities = sorted(priorities, key=lambda x: x[1])
    top_priorities = priorities[:3]

    if top_priorities:
        priority_text = " → ".join([p[0] for p in top_priorities])
    else:
        priority_text = "현재 구조 유지 및 성장 전략 강화"

    one_week = []
    one_month = []
    three_month = []

    if any("비용" in p[0] or "인건비" in p[0] or "고정비" in p[0] for p in top_priorities):
        one_week.append("최근 1개월 비용 항목을 기타 운영비·임대료·인건비로 분리 정리")
        one_month.append("절감 가능한 비용 항목을 선정하고 5~10% 절감 목표 설정")
        three_month.append("비용 절감 후 수익률 변화를 비교하여 유지 여부 결정")

    if any("재방문" in p[0] or "고객" in p[0] for p in top_priorities):
        one_week.append("재방문 고객 기준을 정하고 단골 고객 기록 방식 만들기")
        one_month.append("스탬프 쿠폰 또는 재방문 혜택을 실제 운영")
        three_month.append("재방문율을 다시 측정해 고객 유지 효과 확인")

    if any("마케팅" in p[0] for p in top_priorities):
        one_week.append("네이버 플레이스와 인스타그램 기본 정보 최신화")
        one_month.append("주 1~2회 콘텐츠 업로드와 리뷰 답변 루틴 운영")
        three_month.append("채널별 유입 효과를 비교해 집중 채널 선정")

    if not one_week:
        one_week.append("현재 지표를 기준값으로 저장하고 월별 비교표 작성")
        one_month.append("객단가 상승 또는 고객 증가를 위한 소규모 실험 진행")
        three_month.append("매출·비용·재방문율 변화를 종합 비교하여 성장 전략 조정")

    return {
        "summary": f"현재 매장은 {r['grade']}등급, {r['total_score']}점으로 평가됩니다. 우선순위는 {priority_text}입니다.",
        "details": consulting,
        "priority_text": priority_text,
        "actions": action_plan[:5],
        "one_week": one_week,
        "one_month": one_month,
        "three_month": three_month
    }


# =========================
# 핵심 문제 영역 상세 진단
# =========================
def issue_level(score):
    if score >= 85:
        return "우수", "✅"
    elif score >= 70:
        return "양호", "🟢"
    elif score >= 55:
        return "주의", "🟡"
    else:
        return "위험", "🔴"


def generate_issue_cards(r):
    issues = []

    # 수익성
    level, icon = issue_level(r["profitability"])
    if r["margin"] < 10:
        diagnosis = "순이익이 낮아 매출이 발생해도 실제 남는 금액이 부족합니다."
        action = "객단가 상승, 저마진 메뉴 축소, 세트 구성 개선이 우선입니다."
    elif r["margin"] < 20:
        diagnosis = "수익성은 보통 수준이지만 비용 증가에 취약한 구조입니다."
        action = "할인 이벤트를 줄이고 고마진 상품 비중을 늘리는 것이 좋습니다."
    else:
        diagnosis = "수익성은 비교적 안정적입니다. 현재 이익 구조를 유지하면서 성장 전략을 병행할 수 있습니다."
        action = "고객 유지와 마케팅 효율을 높여 매출 확대에 집중합니다."
    issues.append({
        "name": "수익성",
        "score": r["profitability"],
        "level": level,
        "icon": icon,
        "value": f"수익률 {r['margin']:.1f}%",
        "basis": f"순이익 {r['profit']:,}만원 = 월 매출 {r['sales']:,}만원 - 월 총비용 {r['total_cost']:,}만원",
        "diagnosis": diagnosis,
        "action": action
    })

    # 비용 효율성
    level, icon = issue_level(r["cost_efficiency"])
    if r["cost_ratio"] > 80:
        diagnosis = "월 총비용이 매출 대비 매우 높아 순이익을 압박하고 있습니다."
        action = "기타 운영비, 임대료, 인건비 중 가장 큰 항목부터 절감 가능성을 점검합니다."
    elif r["cost_ratio"] > 70:
        diagnosis = "비용 비율이 다소 높아 매출 증가가 곧바로 이익 증가로 이어지기 어렵습니다."
        action = "월별 비용 항목을 고정비와 변동비로 나누고 5~10% 절감 목표를 설정합니다."
    else:
        diagnosis = "비용 구조는 비교적 안정적입니다. 급격한 비용 증가 여부를 계속 관찰하면 됩니다."
        action = "현재 비용 구조를 기준값으로 저장하고 월별 변화를 관리합니다."
    issues.append({
        "name": "비용효율성",
        "score": r["cost_efficiency"],
        "level": level,
        "icon": icon,
        "value": f"총비용 비율 {r['cost_ratio']:.1f}%",
        "basis": f"총비용 {r['total_cost']:,}만원 = 기타 운영비 {r['other_cost']:,}만원 + 임대료 {r['rent']:,}만원 + 인건비 {r['labor_cost']:,}만원",
        "diagnosis": diagnosis,
        "action": action
    })

    # 인건비
    level, icon = issue_level(r["labor_efficiency"])
    if r["labor_ratio"] > 45:
        diagnosis = "인건비 부담이 커서 인력 운영 효율 개선이 필요합니다."
        action = "피크타임 중심 근무 배치, 반복 업무 단축, 업무별 역할 분담을 점검합니다."
    elif r["labor_ratio"] > 35:
        diagnosis = "인건비율은 주의 구간입니다. 인력을 줄이기보다 배치 효율을 먼저 확인해야 합니다."
        action = "요일·시간대별 방문자 수를 기준으로 근무표를 조정합니다."
    else:
        diagnosis = "인건비율은 비교적 안정적입니다. 현재 운영 방식을 유지해도 무리가 적습니다."
        action = "서비스 품질을 유지하면서 바쁜 시간대 대응력을 높입니다."
    issues.append({
        "name": "인건비효율",
        "score": r["labor_efficiency"],
        "level": level,
        "icon": icon,
        "value": f"인건비율 {r['labor_ratio']:.1f}%",
        "basis": f"월 인건비 {r['labor_cost']:,}만원 / 월 매출 {r['sales']:,}만원, 직원 수 {r['staff']}명",
        "diagnosis": diagnosis,
        "action": action
    })

    # 임대료
    level, icon = issue_level(r["rent_stability"])
    if r["rent_ratio"] > 20:
        diagnosis = "임대료 부담이 높아 고정비 안정성이 낮습니다."
        action = "공간 회전율, 예약 운영, 비는 시간대 매출 전략을 강화합니다."
    elif r["rent_ratio"] > 15:
        diagnosis = "임대료율은 다소 부담이 있는 구간입니다. 매출이 줄면 고정비 부담이 커질 수 있습니다."
        action = "평일 비수기 프로모션과 단골 고객 재방문 전략으로 안정 매출을 확보합니다."
    else:
        diagnosis = "임대료율은 안정적입니다. 고정비 부담보다 고객 확보와 매출 확대에 집중할 수 있습니다."
        action = "현재 공간을 활용해 객단가와 방문 빈도를 높이는 전략을 운영합니다."
    issues.append({
        "name": "임대료안정성",
        "score": r["rent_stability"],
        "level": level,
        "icon": icon,
        "value": f"임대료율 {r['rent_ratio']:.1f}%",
        "basis": f"월 임대료 {r['rent']:,}만원 / 월 매출 {r['sales']:,}만원",
        "diagnosis": diagnosis,
        "action": action
    })

    # 재방문율
    level, icon = issue_level(r["customer_score"])
    if r["revisit_rate"] < 30:
        diagnosis = "재방문율이 낮아 신규 고객 유입에 의존하는 구조일 가능성이 큽니다."
        action = "스탬프 쿠폰, 2회 방문 혜택, 단골 고객 기록을 우선 도입합니다."
    elif r["revisit_rate"] < 50:
        diagnosis = "재방문율은 개선 여지가 있습니다. 다시 방문할 이유를 더 명확히 만들어야 합니다."
        action = "후기 쿠폰, 시즌 메뉴, 멤버십 혜택으로 재방문 동기를 강화합니다."
    else:
        diagnosis = "재방문율은 양호합니다. 기존 고객 기반을 활용한 추천 전략이 가능합니다."
        action = "단골 고객 추천 혜택과 리뷰 이벤트를 통해 신규 고객으로 확장합니다."
    issues.append({
        "name": "고객관리",
        "score": r["customer_score"],
        "level": level,
        "icon": icon,
        "value": f"재방문율 {r['revisit_rate']}%",
        "basis": f"일 재방문 고객 {r['repeat_customers']}명 / 일 방문자 {r['customers']}명",
        "diagnosis": diagnosis,
        "action": action
    })

    # 마케팅
    level, icon = issue_level(r["marketing"])
    channels_text = ", ".join(r["marketing_channels"]) if r["marketing_channels"] else "활용 채널 없음"
    if r["marketing_score"] < 50:
        diagnosis = "마케팅 활용도가 낮아 신규 고객 유입 기회가 부족할 수 있습니다."
        action = "네이버 플레이스 기본 정보 정리, 인스타그램 주 2회 게시, 리뷰 답변 루틴을 시작합니다."
    elif r["marketing_score"] < 75:
        diagnosis = "마케팅은 운영 중이지만 채널별 역할과 성과 관리가 더 필요합니다."
        action = "채널별 목표를 나누고 저장 수, 리뷰 수, 문의 수 같은 성과 지표를 관리합니다."
    else:
        diagnosis = "마케팅 활용도는 양호합니다. 이제는 성과가 좋은 채널에 집중할 단계입니다."
        action = "조회 수보다 저장, 문의, 예약, 재방문으로 이어지는 채널에 집중합니다."
    issues.append({
        "name": "마케팅",
        "score": r["marketing"],
        "level": level,
        "icon": icon,
        "value": f"마케팅 활용도 {r['marketing_score']}점",
        "basis": f"활용 채널: {channels_text} / 업데이트: {r['posting_frequency']} / 리뷰 관리: {r['review_management']}",
        "diagnosis": diagnosis,
        "action": action
    })

    # 성장성
    level, icon = issue_level(r["growth"])
    if r["growth"] < 50:
        diagnosis = "고객 유지와 마케팅 지표가 함께 낮아 성장 동력이 부족합니다."
        action = "재방문 혜택과 온라인 노출 개선을 동시에 진행해야 합니다."
    elif r["growth"] < 70:
        diagnosis = "성장성은 보통 수준입니다. 고객 유지와 신규 유입 중 약한 부분을 보완하면 개선 가능합니다."
        action = "재방문율과 마케팅 점수를 월별로 비교하면서 성장 실험을 운영합니다."
    else:
        diagnosis = "성장성은 양호합니다. 현재 고객 기반과 채널 운영을 확장 전략으로 연결할 수 있습니다."
        action = "추천 이벤트, 신메뉴 캠페인, 단골 대상 프로모션으로 확장합니다."
    issues.append({
        "name": "성장성",
        "score": r["growth"],
        "level": level,
        "icon": icon,
        "value": f"성장성 점수 {r['growth']}점",
        "basis": f"재방문율 {r['revisit_rate']}%와 마케팅 활용도 {r['marketing_score']}점을 종합 반영",
        "diagnosis": diagnosis,
        "action": action
    })

    return sorted(issues, key=lambda x: x["score"])


# =========================
# 마케팅 채널별 활용 전략
# =========================
def generate_marketing_playbook(r):
    selected = r.get("marketing_channels", [])
    playbook = []

    channel_templates = {
        "네이버 플레이스": {
            "goal": "검색 유입과 방문 전환 강화",
            "action": "대표 사진 5장 이상 정리, 영업시간·메뉴·가격 최신화, 방문 후 리뷰 요청 문구 준비",
            "content": "메뉴 사진, 매장 외관, 위치 안내, 대표 메뉴 소개, 리뷰 답변",
            "metric": "저장 수, 길찾기 클릭, 전화/예약 클릭, 리뷰 수"
        },
        "인스타그램": {
            "goal": "브랜드 이미지와 신규 고객 관심 유도",
            "action": "릴스/스토리 중심으로 주 2회 업로드, 대표 메뉴 제작 과정이나 고객 반응을 짧게 노출",
            "content": "릴스, 메뉴 비주얼, 비하인드, 이벤트 안내, 고객 후기 리그램",
            "metric": "조회 수, 저장 수, 프로필 방문, DM 문의"
        },
        "블로그": {
            "goal": "검색 기반 신뢰도와 상세 정보 제공",
            "action": "월 2회 이상 지역명+업종 키워드로 후기형 글 작성 또는 체험 후기 확보",
            "content": "매장 소개, 대표 메뉴 리뷰, 가격 정보, 이용 방법, 지역 키워드 후기",
            "metric": "검색 노출, 유입 수, 체류 시간, 예약/문의 전환"
        },
        "카카오채널": {
            "goal": "단골 고객 재방문 유도",
            "action": "친구 추가 QR을 매장에 배치하고, 신메뉴·쿠폰·휴무 공지를 월 2회 발송",
            "content": "쿠폰, 신메뉴 소식, 재방문 혜택, 예약 안내, 단골 전용 이벤트",
            "metric": "친구 수, 메시지 클릭률, 쿠폰 사용률, 재방문 고객 수"
        },
        "배달앱/예약앱": {
            "goal": "즉시 구매와 예약 전환 강화",
            "action": "메뉴 사진, 옵션 구성, 리뷰 답변, 시간대별 할인 쿠폰을 정리해 전환율 개선",
            "content": "대표 메뉴 구성, 세트 메뉴, 리뷰 이벤트, 시간대 쿠폰, 예약 안내",
            "metric": "주문/예약 수, 전환율, 리뷰 평점, 재주문율"
        },
        "지역 커뮤니티": {
            "goal": "동네 기반 신뢰와 입소문 확보",
            "action": "지역 카페·동네 커뮤니티에 홍보성보다 정보성 게시글과 이벤트를 운영",
            "content": "동네 행사, 할인 안내, 지역 주민 혜택, 사장님 스토리, 후기 공유",
            "metric": "댓글 수, 문의 수, 쿠폰 사용률, 신규 방문자 수"
        },
        "오프라인 홍보": {
            "goal": "매장 내 재방문과 현장 전환 강화",
            "action": "스탬프 카드, 테이블 QR, 입구 안내물, 포장 쿠폰을 통해 방문 고객을 재방문 고객으로 전환",
            "content": "QR 안내문, 스탬프 카드, 영수증 쿠폰, 테이블 메뉴판, 재방문 혜택",
            "metric": "쿠폰 회수율, QR 접속 수, 재방문 고객 수, 객단가"
        }
    }

    if not selected:
        selected = ["네이버 플레이스", "인스타그램", "오프라인 홍보"]

    for ch in selected:
        if ch in channel_templates:
            item = channel_templates[ch].copy()
            item["channel"] = ch
            playbook.append(item)

    # 부족한 채널 추천
    recommendations = []
    if "네이버 플레이스" not in selected:
        recommendations.append("네이버 플레이스는 검색 유입의 기본 채널이므로 우선 추가하는 것이 좋습니다.")
    if r["revisit_rate"] < 50 and "카카오채널" not in selected:
        recommendations.append("재방문율 개선을 위해 카카오채널 또는 쿠폰 기반 CRM 채널을 추가하는 것이 좋습니다.")
    if r["marketing_score"] < 60 and "인스타그램" not in selected:
        recommendations.append("브랜드 노출 강화를 위해 인스타그램 릴스/스토리 운영을 추가하는 것이 좋습니다.")

    return playbook, recommendations


def generate_advanced_roadmap(r):
    playbook, recommendations = generate_marketing_playbook(r)
    main_channel = playbook[0]["channel"] if playbook else "네이버 플레이스"

    week_tasks = [
        "현재 지표 기준값 저장: 매출, 총비용, 재방문율, 마케팅 활용도 기록",
        "네이버 플레이스·인스타그램·리뷰 상태를 점검하고 누락 정보 정리",
        f"핵심 채널 1순위 선정: {main_channel} 중심으로 운영 시작"
    ]

    month_tasks = [
        "주 2회 콘텐츠 업로드 루틴 운영: 대표 메뉴, 후기, 이벤트, 매장 분위기 콘텐츠 제작",
        "리뷰 요청 문구와 답변 템플릿을 만들고 신규 리뷰에 48시간 안에 답변",
        "재방문 쿠폰 또는 스탬프 혜택을 실제 운영하여 재방문 고객 수 측정"
    ]

    quarter_tasks = [
        "채널별 성과 비교: 조회 수, 저장 수, 리뷰 수, 쿠폰 사용률, 재방문율 확인",
        "성과가 낮은 채널은 운영 빈도를 줄이고 성과가 높은 채널에 콘텐츠 집중",
        "월별 리포트를 저장하여 매출·비용·고객 지표 변화 추세를 비교"
    ]

    if r["revisit_rate"] < 50:
        week_tasks.append("재방문 고객 판별 기준을 정하고 계산 방식을 통일")
        month_tasks.append("2회 방문 고객 대상 혜택을 만들어 단골 전환 실험")
        quarter_tasks.append("재방문율 목표를 현재 대비 10%p 개선으로 설정하고 결과 비교")

    if r["marketing_score"] < 60:
        week_tasks.append("프로필 사진, 대표 메뉴 사진, 가격 정보 등 기본 노출 요소 보완")
        month_tasks.append("리뷰 이벤트와 SNS 공유 이벤트를 동시에 운영")
        quarter_tasks.append("마케팅 채널별 유입 효과를 비교해 핵심 채널 2개만 집중 운영")

    if r["cost_ratio"] > 75:
        week_tasks.append("마케팅 실행 전 예산 한도를 정해 비용 증가를 방지")
        month_tasks.append("무료·저비용 채널 중심으로 홍보하고 광고비 지출은 제한")
        quarter_tasks.append("마케팅 비용 대비 매출 증가분을 비교해 ROI 기준 설정")

    return {
        "week": week_tasks,
        "month": month_tasks,
        "quarter": quarter_tasks,
        "recommendations": recommendations
    }


# =========================
# 사이드바
# =========================
DEFAULT_VALUES = {
    "sales": 2000,
    "other_cost": 700,
    "rent": 300,
    "labor_cost": 600,
    "staff": 3,
    "customers": 80,
    "repeat_customers": 28,
    "avg_price": 8000
}

DEFAULT_MARKETING = {
    "marketing_channels": ["인스타그램", "네이버 플레이스"],
    "posting_frequency": "주 1~2회",
    "review_management": "가끔 답변"
}

for key, value in DEFAULT_VALUES.items():
    if key not in st.session_state:
        st.session_state[key] = value

for key, value in DEFAULT_MARKETING.items():
    if key not in st.session_state:
        st.session_state[key] = value

st.sidebar.markdown("""
<div style="padding: 12px 4px 8px 4px;">
    <div style="font-size: 30px; font-weight: 950; letter-spacing: -1px;">🩺 비즈닥터</div>
    <div style="font-size: 13px; color: #64748B; font-weight: 750; margin-top: 4px;">
        AI 기반 소상공인 경영 진단 프로토타입
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.divider()
st.sidebar.subheader("엑셀 데이터 업로드")

uploaded_excel = st.sidebar.file_uploader(
    "기존 경영 진단 엑셀 파일 업로드",
    type=["xlsx", "xls"]
)

if uploaded_excel is not None:
    extracted_values = extract_excel_values(uploaded_excel)

    if extracted_values:
        st.sidebar.success("엑셀에서 일부 데이터를 찾았습니다.")

        preview_df = pd.DataFrame({
            "항목": [KOREAN_LABEL.get(k, k) for k in extracted_values.keys()],
            "추출값": list(extracted_values.values())
        })

        st.sidebar.dataframe(preview_df, use_container_width=True)

        if st.sidebar.button("엑셀 값 입력칸에 반영", use_container_width=True):
            for k, v in extracted_values.items():
                if k in DEFAULT_VALUES:
                    st.session_state[k] = int(v)
            st.rerun()

    else:
        st.sidebar.warning("자동 추출된 값이 없습니다. 직접 입력해주세요.")

st.sidebar.divider()

if st.sidebar.button("시연용 샘플 데이터 불러오기", use_container_width=True):
    for key, value in DEFAULT_VALUES.items():
        st.session_state[key] = value
    for key, value in DEFAULT_MARKETING.items():
        st.session_state[key] = value
    st.rerun()

st.sidebar.subheader("경영 데이터 입력")

sales = st.sidebar.number_input("월 매출 (만원)", min_value=0, step=100, key="sales")
other_cost = st.sidebar.number_input("기타 운영비 (임대료·인건비 제외, 만원)", min_value=0, step=100, key="other_cost")
rent = st.sidebar.number_input("월 임대료 (만원)", min_value=0, step=10, key="rent")
labor_cost = st.sidebar.number_input("월 인건비 (만원)", min_value=0, step=50, key="labor_cost")

calculated_total_cost = other_cost + rent + labor_cost
st.sidebar.info(f"월 총비용 = 기타 운영비 + 임대료 + 인건비 = {calculated_total_cost:,}만원")

staff = st.sidebar.number_input("직원 수", min_value=0, step=1, key="staff")
customers = st.sidebar.number_input("일 방문자 수", min_value=0, step=5, key="customers")
repeat_customers = st.sidebar.number_input("일 재방문 고객 수", min_value=0, step=1, key="repeat_customers")

if repeat_customers > customers and customers > 0:
    st.sidebar.warning("재방문 고객 수가 일 방문자 수보다 큽니다. 계산에서는 최대 100%로 반영됩니다.")

avg_price = st.sidebar.number_input("객단가 (원)", min_value=0, step=500, key="avg_price")

calculated_revisit_rate = calculate_revisit_rate(customers, repeat_customers)
st.sidebar.info(
    f"재방문율 = 재방문 고객 수 ÷ 일 방문자 수 = {repeat_customers}명 ÷ {customers}명 = {calculated_revisit_rate}%"
)

st.sidebar.subheader("마케팅 채널 활용")

marketing_channels = st.sidebar.multiselect(
    "활용 중인 마케팅 채널",
    ["인스타그램", "네이버 플레이스", "블로그", "카카오채널", "배달앱/예약앱", "지역 커뮤니티", "오프라인 홍보"],
    key="marketing_channels"
)

posting_frequency = st.sidebar.selectbox(
    "콘텐츠/공지 업데이트 빈도",
    ["거의 안 함", "월 1~2회", "주 1~2회", "주 3회 이상"],
    key="posting_frequency"
)

review_management = st.sidebar.selectbox(
    "리뷰 관리 수준",
    ["거의 안 함", "가끔 답변", "정기적으로 답변", "리뷰 이벤트와 연계"],
    key="review_management"
)

marketing_score = calculate_marketing_score(marketing_channels, posting_frequency, review_management)
st.sidebar.info(
    f"마케팅 활용도 = 채널 {len(marketing_channels)}개 + 업데이트 빈도 + 리뷰 관리 = {marketing_score}점"
)

analyze_btn = st.sidebar.button("AI 경영 진단 시작", use_container_width=True)

if analyze_btn:
    if sales == 0:
        st.sidebar.warning("월 매출을 입력해주세요.")
    else:
        with st.spinner("AI가 경영 데이터를 분석하고 있습니다..."):
            time.sleep(0.6)

        st.session_state["result"] = analyze_business(
            sales,
            other_cost,
            rent,
            labor_cost,
            staff,
            customers,
            repeat_customers,
            avg_price,
            marketing_channels,
            posting_frequency,
            review_management
        )


# =========================
# 메인 화면
# =========================
st.markdown("""
<div class="hero">
    <div class="eyebrow">AI Business Doctor · Excel to Insight</div>
    <div class="hero-title"><span>BizDoctor</span></div>
    <div class="hero-sub">
        기존 엑셀 진단 데이터를 업로드하면 주요 경영 데이터를 자동 추출하고,
        월 총비용·재방문율·마케팅 활용도를 근거 기반으로 산출하여 경영 상태를 진단합니다.
    </div>
    <div class="hero-grid">
        <div class="hero-mini"><b>🧮 총비용 자동 산출</b><span>기타 운영비 + 임대료 + 인건비 합산</span></div>
        <div class="hero-mini"><b>👥 재방문율 자동 계산</b><span>재방문 고객 수 ÷ 일 방문자 수 기반</span></div>
        <div class="hero-mini"><b>📱 마케팅 채널 점수화</b><span>인스타그램·네이버·블로그 등 선택 반영</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

if "result" not in st.session_state:
    st.markdown('<div class="section-title">시연 흐름</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="step-grid">
        <div class="step-card"><div class="step-icon">01</div><b>엑셀 업로드</b><span>기존 경영 진단 엑셀 파일을 업로드합니다.</span></div>
        <div class="step-card"><div class="step-icon">02</div><b>비용 구조화</b><span>기타 운영비·임대료·인건비를 분리합니다.</span></div>
        <div class="step-card"><div class="step-icon">03</div><b>고객·마케팅 진단</b><span>재방문율과 마케팅 활용도를 자동 산출합니다.</span></div>
        <div class="step-card"><div class="step-icon">04</div><b>전략 리포트</b><span>개선 전략과 시뮬레이션 결과를 제공합니다.</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.info("왼쪽 사이드바에서 엑셀 파일을 업로드하거나 시연용 샘플 데이터를 불러온 뒤, [AI 경영 진단 시작] 버튼을 눌러주세요.")

else:
    r = st.session_state["result"]

    tab1, tab2, tab3, tab4 = st.tabs(["📊 진단 대시보드", "🧠 AI 컨설팅", "📈 시뮬레이션", "📄 리포트"])

    with tab1:
        st.markdown('<div class="section-title">종합 진단 대시보드</div>', unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            metric_card("종합 점수", f"{r['total_score']}점", r["grade_comment"])
        with c2:
            metric_card("진단 등급", f"{r['grade']} 등급", "AI 경영 주치의 평가")
        with c3:
            metric_card("월 순이익", f"{r['profit']:,}만원", f"월 매출 {r['sales']:,}만원 기준")
        with c4:
            metric_card("월 총비용", f"{r['total_cost']:,}만원", f"매출 대비 {r['cost_ratio']:.1f}%")

        st.markdown("")

        cost_left, cost_right = st.columns([1.1, 1])

        with cost_left:
            st.markdown(f"""
            <div class="comparison-card">
                <div class="comparison-title">월 총비용 산출 구조</div>
                <div class="comparison-row"><span>기타 운영비</span><b>{r['other_cost']:,}만원</b></div>
                <div class="comparison-row"><span>임대료</span><b>{r['rent']:,}만원</b></div>
                <div class="comparison-row"><span>인건비</span><b>{r['labor_cost']:,}만원</b></div>
                <div class="comparison-row"><span>월 총비용</span><b>{r['total_cost']:,}만원</b></div>
            </div>
            """, unsafe_allow_html=True)

        with cost_right:
            st.markdown(f"""
            <div class="comparison-card">
                <div class="comparison-title">비용 비율 진단</div>
                <div class="comparison-row"><span>기타 운영비율</span><b>{r['other_cost_ratio']:.1f}%</b></div>
                <div class="comparison-row"><span>임대료율</span><b>{r['rent_ratio']:.1f}%</b></div>
                <div class="comparison-row"><span>인건비율</span><b>{r['labor_ratio']:.1f}%</b></div>
                <div class="comparison-row"><span>수익률</span><b>{r['margin']:.1f}%</b></div>
            </div>
            """, unsafe_allow_html=True)

        customer_left, customer_right = st.columns([1.1, 1])

        with customer_left:
            st.markdown(f"""
            <div class="comparison-card">
                <div class="comparison-title">재방문율 산출 근거</div>
                <div class="comparison-row"><span>일 방문자 수</span><b>{r['customers']}명</b></div>
                <div class="comparison-row"><span>일 재방문 고객 수</span><b>{r['repeat_customers']}명</b></div>
                <div class="comparison-row"><span>재방문율</span><b>{r['revisit_rate']}%</b></div>
            </div>
            """, unsafe_allow_html=True)

        with customer_right:
            channels_text = ", ".join(r["marketing_channels"]) if r["marketing_channels"] else "활용 채널 없음"
            st.markdown(f"""
            <div class="comparison-card">
                <div class="comparison-title">마케팅 활용도 산출 근거</div>
                <div class="comparison-row"><span>활용 채널</span><b>{channels_text}</b></div>
                <div class="comparison-row"><span>업데이트 빈도</span><b>{r['posting_frequency']}</b></div>
                <div class="comparison-row"><span>리뷰 관리</span><b>{r['review_management']}</b></div>
                <div class="comparison-row"><span>마케팅 활용도</span><b>{r['marketing_score']}점</b></div>
            </div>
            """, unsafe_allow_html=True)

        left, right = st.columns([1.35, 1])

        with left:
            st.subheader("7대 진단 지표")

            labels = ["수익성", "비용효율성", "인건비효율", "고객관리", "마케팅", "임대료안정성", "성장성"]
            values = [
                r["profitability"],
                r["cost_efficiency"],
                r["labor_efficiency"],
                r["customer_score"],
                r["marketing"],
                r["rent_stability"],
                r["growth"]
            ]

            if PLOTLY_AVAILABLE:
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=values + [values[0]],
                    theta=labels + [labels[0]],
                    fill="toself",
                    name="진단 점수"
                ))
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                    showlegend=False,
                    height=420,
                    margin=dict(l=30, r=30, t=20, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                chart_data = pd.DataFrame({"지표": labels, "점수": values})
                st.bar_chart(chart_data.set_index("지표"))

        with right:
            st.subheader("핵심 문제 영역")
            issue_cards = generate_issue_cards(r)

            st.markdown(f"""
            <div style="margin-bottom: 14px;">
                <span class="grade-badge">{r['grade']} 등급 · {r['total_score']}점</span>
                <div style="font-size: 14px; color: #64748B; font-weight: 750; margin-top: 10px;">
                    낮은 점수 순으로 우선 점검할 지표를 보여줍니다.
                </div>
            </div>
            """, unsafe_allow_html=True)

            for item in issue_cards[:5]:
                st.markdown(f"""
                <div class="comparison-card">
                    <div class="comparison-title">{item['icon']} {item['name']} · {item['level']} · {item['score']}점</div>
                    <div class="comparison-row"><span>현재값</span><b>{item['value']}</b></div>
                    <div class="comparison-row"><span>근거</span><b>{item['basis']}</b></div>
                    <div style="font-size:14px; color:#334155; font-weight:750; line-height:1.6; margin-top:12px;">
                        {item['diagnosis']}
                    </div>
                    <div style="font-size:13px; color:#4F46E5; font-weight:800; line-height:1.6; margin-top:10px;">
                        제안: {item['action']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with st.expander("전체 7대 지표 상세 보기"):
                for item in issue_cards:
                    st.markdown(f"**{item['icon']} {item['name']} · {item['level']} · {item['score']}점**")
                    st.write(f"현재값: {item['value']}")
                    st.write(f"근거: {item['basis']}")
                    st.write(f"진단: {item['diagnosis']}")
                    st.write(f"제안: {item['action']}")
                    st.divider()

    with tab2:
        st.markdown('<div class="section-title">AI 경영 컨설팅</div>', unsafe_allow_html=True)
        consulting = generate_ai_consulting(r)

        st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
        st.markdown('<div class="user-bubble">우리 매장의 현재 경영 상태를 구체적으로 분석해주세요.</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="ai-bubble">
            🩺 <b>종합 진단</b><br>
            {consulting['summary']}
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.subheader("세부 진단 의견")
        for idx, detail in enumerate(consulting["details"], 1):
            st.markdown(f"""
            <div class="strategy-card">
                <span class="strategy-number">{idx}</span>
                <b>{detail}</b>
            </div>
            """, unsafe_allow_html=True)

        st.subheader("우선 실행 전략")
        for idx, action in enumerate(consulting["actions"], 1):
            st.markdown(f"""
            <div class="strategy-card">
                <span class="strategy-number">{idx}</span>
                <b>{action}</b>
            </div>
            """, unsafe_allow_html=True)

        st.subheader("마케팅 채널별 활용 전략")
        playbook, marketing_recommendations = generate_marketing_playbook(r)

        for item in playbook:
            st.markdown(f"""
            <div class="comparison-card">
                <div class="comparison-title">📌 {item['channel']} · {item['goal']}</div>
                <div class="comparison-row"><span>실행 방법</span><b>{item['action']}</b></div>
                <div class="comparison-row"><span>추천 콘텐츠</span><b>{item['content']}</b></div>
                <div class="comparison-row"><span>확인 지표</span><b>{item['metric']}</b></div>
            </div>
            """, unsafe_allow_html=True)

        if marketing_recommendations:
            st.subheader("추가 추천 채널")
            for rec in marketing_recommendations:
                st.markdown(f"""
                <div class="problem-card">💡 {rec}</div>
                """, unsafe_allow_html=True)

        st.subheader("고급 실행 로드맵")
        advanced_roadmap = generate_advanced_roadmap(r)
        roadmap_col1, roadmap_col2, roadmap_col3 = st.columns(3)

        with roadmap_col1:
            st.markdown("""
            <div class="comparison-card">
                <div class="comparison-title">1단계 · 이번 주 세팅</div>
            """, unsafe_allow_html=True)
            for item in advanced_roadmap["week"]:
                st.markdown(f"- {item}")
            st.markdown("</div>", unsafe_allow_html=True)

        with roadmap_col2:
            st.markdown("""
            <div class="comparison-card">
                <div class="comparison-title">2단계 · 1개월 실행</div>
            """, unsafe_allow_html=True)
            for item in advanced_roadmap["month"]:
                st.markdown(f"- {item}")
            st.markdown("</div>", unsafe_allow_html=True)

        with roadmap_col3:
            st.markdown("""
            <div class="comparison-card">
                <div class="comparison-title">3단계 · 3개월 최적화</div>
            """, unsafe_allow_html=True)
            for item in advanced_roadmap["quarter"]:
                st.markdown(f"- {item}")
            st.markdown("</div>", unsafe_allow_html=True)

        st.caption("※ 현재 버전은 입력된 경영 데이터와 규칙 기반 진단 로직을 활용한 AI 컨설팅 프로토타입입니다.")

    with tab3:
        st.markdown('<div class="section-title">개선 전략 시뮬레이션</div>', unsafe_allow_html=True)

        s1, s2, s3 = st.columns(3)
        with s1:
            price_up = st.slider("가격 인상률 (%)", 0, 20, 5)
        with s2:
            cost_down = st.slider("총비용 절감률 (%)", 0, 20, 10)
        with s3:
            customer_up = st.slider("고객 증가율 (%)", 0, 30, 10)

        new_sales = int(r["sales"] * (1 + price_up / 100) * (1 + customer_up / 100))
        new_total_cost = int(r["total_cost"] * (1 - cost_down / 100))
        new_profit = new_sales - new_total_cost
        new_margin = (new_profit / new_sales) * 100 if new_sales > 0 else 0
        profit_delta = new_profit - r["profit"]

        b1, b2, b3 = st.columns([1, 1, 1.1])

        with b1:
            st.markdown(f"""
            <div class="comparison-card">
                <div class="comparison-title">현재 상태</div>
                <div class="comparison-row"><span>매출</span><b>{r['sales']:,}만원</b></div>
                <div class="comparison-row"><span>월 총비용</span><b>{r['total_cost']:,}만원</b></div>
                <div class="comparison-row"><span>순이익</span><b>{r['profit']:,}만원</b></div>
                <div class="comparison-row"><span>수익률</span><b>{r['margin']:.1f}%</b></div>
            </div>
            """, unsafe_allow_html=True)

        with b2:
            st.markdown(f"""
            <div class="comparison-card">
                <div class="comparison-title">개선 후 예상</div>
                <div class="comparison-row"><span>매출</span><b>{new_sales:,}만원</b></div>
                <div class="comparison-row"><span>월 총비용</span><b>{new_total_cost:,}만원</b></div>
                <div class="comparison-row"><span>순이익</span><b>{new_profit:,}만원</b></div>
                <div class="comparison-row"><span>수익률</span><b>{new_margin:.1f}%</b></div>
            </div>
            """, unsafe_allow_html=True)

        with b3:
            st.markdown(f"""
            <div class="impact">
                <div style="font-weight: 850; color: #CBD5E1;">예상 개선 효과</div>
                <div class="impact-number">{profit_delta:+,}만원</div>
                <div style="font-size: 14px; color: #CBD5E1; line-height: 1.65;">
                    가격 {price_up}% 조정, 총비용 {cost_down}% 절감,<br>
                    고객 {customer_up}% 증가 가정
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.caption("※ 본 결과는 입력값 기반 시뮬레이션이며 실제 결과와 차이가 있을 수 있습니다.")

    with tab4:
        st.markdown('<div class="section-title">경영 개선 리포트</div>', unsafe_allow_html=True)

        consulting = generate_ai_consulting(r)
        report_text = make_report_text(r)
        channels_text = ", ".join(r["marketing_channels"]) if r["marketing_channels"] else "활용 채널 없음"

        st.markdown(f"""
        <div class="report-card">
            <div style="display:flex; justify-content:space-between; gap:16px; align-items:flex-start; flex-wrap:wrap;">
                <div>
                    <div style="font-size:14px; color:#64748B; font-weight:800;">BizDoctor One-Page Report</div>
                    <h2 style="margin:6px 0 4px 0;">경영 진단 요약 리포트</h2>
                    <div style="color:#475569; font-weight:700;">{consulting['summary']}</div>
                </div>
                <div style="text-align:right;">
                    <div class="grade-badge">{r['grade']} 등급</div>
                    <div style="font-size:34px; font-weight:950; margin-top:10px; color:#111827;">{r['total_score']}점</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        r1, r2, r3, r4 = st.columns(4)
        with r1:
            metric_card("월 매출", f"{r['sales']:,}만원", "입력 매출 기준")
        with r2:
            metric_card("월 총비용", f"{r['total_cost']:,}만원", f"매출 대비 {r['cost_ratio']:.1f}%")
        with r3:
            metric_card("월 순이익", f"{r['profit']:,}만원", f"수익률 {r['margin']:.1f}%")
        with r4:
            metric_card("우선 개선", consulting["priority_text"].split(" → ")[0], consulting["priority_text"])

        st.markdown("")

        report_col1, report_col2 = st.columns([1, 1])

        with report_col1:
            st.markdown(f"""
            <div class="comparison-card">
                <div class="comparison-title">비용 구조 요약</div>
                <div class="comparison-row"><span>기타 운영비</span><b>{r['other_cost']:,}만원 / {r['other_cost_ratio']:.1f}%</b></div>
                <div class="comparison-row"><span>임대료</span><b>{r['rent']:,}만원 / {r['rent_ratio']:.1f}%</b></div>
                <div class="comparison-row"><span>인건비</span><b>{r['labor_cost']:,}만원 / {r['labor_ratio']:.1f}%</b></div>
                <div class="comparison-row"><span>총비용</span><b>{r['total_cost']:,}만원</b></div>
            </div>
            """, unsafe_allow_html=True)

        with report_col2:
            st.markdown(f"""
            <div class="comparison-card">
                <div class="comparison-title">고객·마케팅 요약</div>
                <div class="comparison-row"><span>재방문율</span><b>{r['repeat_customers']}명 ÷ {r['customers']}명 = {r['revisit_rate']}%</b></div>
                <div class="comparison-row"><span>마케팅 채널</span><b>{channels_text}</b></div>
                <div class="comparison-row"><span>업데이트 빈도</span><b>{r['posting_frequency']}</b></div>
                <div class="comparison-row"><span>마케팅 점수</span><b>{r['marketing_score']}점</b></div>
            </div>
            """, unsafe_allow_html=True)

        st.subheader("핵심 문제 상세 요약")
        issue_cards = generate_issue_cards(r)
        for item in issue_cards[:3]:
            st.markdown(f"""
            <div class="comparison-card">
                <div class="comparison-title">{item['icon']} {item['name']} · {item['level']} · {item['score']}점</div>
                <div class="comparison-row"><span>현재값</span><b>{item['value']}</b></div>
                <div class="comparison-row"><span>판단 근거</span><b>{item['basis']}</b></div>
                <div style="font-size:14px; color:#334155; font-weight:750; line-height:1.6; margin-top:12px;">{item['diagnosis']}</div>
                <div style="font-size:13px; color:#4F46E5; font-weight:800; line-height:1.6; margin-top:10px;">제안: {item['action']}</div>
            </div>
            """, unsafe_allow_html=True)

        st.subheader("핵심 실행 전략")
        for idx, action in enumerate(consulting["actions"], 1):
            st.markdown(f"""
            <div class="strategy-card">
                <span class="strategy-number">{idx}</span>
                <b>{action}</b>
            </div>
            """, unsafe_allow_html=True)

        st.subheader("실행 로드맵")
        advanced_roadmap = generate_advanced_roadmap(r)
        road1, road2, road3 = st.columns(3)
        with road1:
            st.markdown("""
            <div class="comparison-card">
                <div class="comparison-title">1단계 · 이번 주 세팅</div>
            """, unsafe_allow_html=True)
            for item in advanced_roadmap["week"]:
                st.markdown(f"- {item}")
            st.markdown("</div>", unsafe_allow_html=True)

        with road2:
            st.markdown("""
            <div class="comparison-card">
                <div class="comparison-title">2단계 · 1개월 실행</div>
            """, unsafe_allow_html=True)
            for item in advanced_roadmap["month"]:
                st.markdown(f"- {item}")
            st.markdown("</div>", unsafe_allow_html=True)

        with road3:
            st.markdown("""
            <div class="comparison-card">
                <div class="comparison-title">3단계 · 3개월 최적화</div>
            """, unsafe_allow_html=True)
            for item in advanced_roadmap["quarter"]:
                st.markdown(f"- {item}")
            st.markdown("</div>", unsafe_allow_html=True)

        st.subheader("마케팅 채널별 활용 전략")
        playbook, marketing_recommendations = generate_marketing_playbook(r)
        for item in playbook:
            st.markdown(f"""
            <div class="comparison-card">
                <div class="comparison-title">📌 {item['channel']} · {item['goal']}</div>
                <div class="comparison-row"><span>실행 방법</span><b>{item['action']}</b></div>
                <div class="comparison-row"><span>추천 콘텐츠</span><b>{item['content']}</b></div>
                <div class="comparison-row"><span>확인 지표</span><b>{item['metric']}</b></div>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("텍스트 리포트 원문 보기"):
            st.text_area("리포트 원문", report_text, height=360)

        st.download_button(
            label="📄 One-Page 리포트 다운로드",
            data=report_text.encode("utf-8-sig"),
            file_name="BizDoctor_OnePage_Report.txt",
            mime="text/plain",
            use_container_width=True
        )
