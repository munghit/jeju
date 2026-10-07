import streamlit as st
from datetime import datetime, timedelta
import re

st.set_page_config(
    page_title="여행 플래너",
    page_icon="✈️",
    layout="wide"
)

# =========================
# CSS
# =========================
st.markdown("""
<style>
.stApp {
    background: #f7f8fc;
    color: #222222;
}

html, body, [class*="css"] {
    font-family: Arial, sans-serif;
}

h1, h2, h3, h4, h5, h6 {
    color: #222222 !important;
}

p, span, div, label {
    color: #222222;
}

.stTextInput label,
.stTextArea label {
    color: #222222 !important;
    font-weight: 600;
}

.stTextInput input,
.stTextArea textarea {
    background-color: #ffffff !important;
    color: #222222 !important;
    -webkit-text-fill-color: #222222 !important;
    border: 1px solid #d9dce5 !important;
    border-radius: 12px !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #999999 !important;
    -webkit-text-fill-color: #999999 !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #7657e8 !important;
    box-shadow: 0 0 0 1px #7657e8 !important;
}

.stButton button {
    width: 100%;
    background: #6c4ce5 !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 20px !important;
    font-weight: 700 !important;
}

.stButton button:hover {
    background: #5738ca !important;
    color: white !important;
}

.hero {
    background: linear-gradient(135deg, #6c4ce5, #8c6ff0);
    padding: 42px;
    border-radius: 24px;
    margin-bottom: 30px;
    color: white;
}

.hero h1 {
    color: white !important;
    font-size: 42px;
    margin-bottom: 10px;
}

.hero p {
    color: rgba(255,255,255,0.9) !important;
    font-size: 17px;
}

.section-title {
    font-size: 24px;
    font-weight: 800;
    margin-top: 25px;
    margin-bottom: 15px;
    color: #222222;
}

.result-card {
    background: white;
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 14px;
    border: 1px solid #e5e7ef;
    box-shadow: 0 4px 15px rgba(0,0,0,0.04);
}

.result-card h3 {
    color: #222222 !important;
    margin-bottom: 6px;
}

.result-card p {
    color: #555555 !important;
}

.day-title {
    background: #eeeaff;
    color: #5639c7 !important;
    padding: 13px 18px;
    border-radius: 12px;
    font-weight: 800;
    margin-top: 25px;
    margin-bottom: 12px;
}

.place-card {
    background: white;
    border: 1px solid #e5e7ef;
    border-radius: 15px;
    padding: 16px;
    margin-bottom: 10px;
}

.place-card strong {
    color: #222222;
}

.place-card small {
    color: #777777;
}

.tag {
    display: inline-block;
    background: #eeeaff;
    color: #5b40c9 !important;
    border-radius: 20px;
    padding: 5px 11px;
    margin-right: 5px;
    font-size: 12px;
    font-weight: 700;
}

.summary {
    background: linear-gradient(135deg, #6c4ce5, #8468ed);
    border-radius: 20px;
    padding: 25px;
    margin-top: 25px;
}

.summary h3,
.summary p,
.summary strong {
    color: white !important;
}

.restaurant-card {
    background: white;
    border: 1px solid #e5e7ef;
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 12px;
}

.restaurant-card h4 {
    color: #222222 !important;
}

.restaurant-card p {
    color: #666666 !important;
}

hr {
    border: none;
    border-top: 1px solid #e2e4eb;
    margin: 30px 0;
}
</style>
""", unsafe_allow_html=True)


# =========================
# 샘플 장소 데이터
# =========================
PLACE_DATA = {
    "성산일출봉": {
        "area": "성산",
        "time": "08:00",
        "duration": 120,
        "description": "제주 동쪽을 대표하는 일출 명소"
    },
    "섭지코지": {
        "area": "성산",
        "time": "09:00",
        "duration": 90,
        "description": "해안 풍경을 즐기기 좋은 산책 명소"
    },
    "우도": {
        "area": "성산",
        "time": "08:00",
        "duration": 240,
        "description": "배를 타고 들어가는 제주 대표 섬 여행지"
    },
    "월정리": {
        "area": "동부",
        "time": "10:00",
        "duration": 120,
        "description": "해변과 카페가 유명한 지역"
    },
    "함덕해수욕장": {
        "area": "동부",
        "time": "09:00",
        "duration": 120,
        "description": "맑은 바다와 해변 산책을 즐길 수 있는 곳"
    },
    "동문시장": {
        "area": "제주시",
        "time": "09:00",
        "duration": 120,
        "description": "제주 대표 전통시장"
    },
    "용두암": {
        "area": "제주시",
        "time": "08:00",
        "duration": 60,
        "description": "제주시 도심에서 접근하기 좋은 해안 명소"
    },
    "협재해수욕장": {
        "area": "서부",
        "time": "09:00",
        "duration": 150,
        "description": "에메랄드빛 바다로 유명한 해수욕장"
    },
    "애월": {
        "area": "서부",
        "time": "10:00",
        "duration": 150,
        "description": "바다를 보며 카페와 산책을 즐기기 좋은 지역"
    },
    "오설록": {
        "area": "서부",
        "time": "09:00",
        "duration": 120,
        "description": "녹차밭과 티 뮤지엄으로 유명한 장소"
    }
}


# =========================
# 샘플 음식점
# =========================
RESTAURANTS = [
    {
        "name": "제주 흑돼지 맛집",
        "area": "제주시",
        "type": "흑돼지",
        "description": "제주에서 흑돼지를 즐기기 좋은 곳"
    },
    {
        "name": "해산물 맛집",
        "area": "성산",
        "type": "해산물",
        "description": "성산 주변에서 제주 해산물을 즐기기 좋은 곳"
    },
    {
        "name": "애월 바다 카페",
        "area": "서부",
        "type": "카페",
        "description": "바다 전망을 즐길 수 있는 카페"
    },
    {
        "name": "월정리 카페",
        "area": "동부",
        "type": "카페",
        "description": "월정리 해변 근처 카페"
    }
]


# =========================
# 함수
# =========================
def parse_date(text):
    text = text.strip()

    formats = [
        "%Y.%m.%d",
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%Y. %m. %d.",
        "%Y년 %m월 %d일"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass

    return None


def parse_places(text):
    if not text:
        return []

    text = text.replace("\n", ",")
    text = text.replace("/", ",")
    text = text.replace("·", ",")

    places = []

    for item in text.split(","):
        item = item.strip()

        if item and item not in places:
            places.append(item)

    return places


def analyze_preference(text):
    text = text.lower()

    if any(word in text for word in [
        "여유",
        "천천히",
        "느긋",
        "편하게"
    ]):
        style = "여유로운 일정"
    elif any(word in text for word in [
        "많이",
        "빡빡",
        "최대한",
        "알차게"
    ]):
        style = "알찬 일정"
    else:
        style = "균형 잡힌 일정"

    if any(word in text for word in [
        "늦게 출발",
        "천천히 출발"
    ]):
        start_hour = 10
    elif "일찍" in text:
        start_hour = 7
    else:
        start_hour = 9

    if any(word in text for word in [
        "늦게까지",
        "밤까지"
    ]):
        end_hour = 23
    else:
        end_hour = 20

    return style, start_hour, end_hour


def estimate_travel_time(area1, area2):
    if area1 == area2:
        return 10

    pairs = {
        ("제주시", "동부"): 45,
        ("제주시", "성산"): 70,
        ("제주시", "서부"): 50,
        ("동부", "성산"): 35,
        ("동부", "서부"): 70,
        ("성산", "서부"): 90
    }

    key = (area1, area2)

    if key in pairs:
        return pairs[key]

    reverse_key = (area2, area1)

    if reverse_key in pairs:
        return pairs[reverse_key]

    return 60


def generate_itinerary(places, days, start_hour, end_hour, style):
    itinerary = []

    if not places:
        return itinerary

    if days <= 0:
        days = 1

    chunks = [[] for _ in range(days)]

    for index, place in enumerate(places):
        chunks[index % days].append(place)

    for day_index, day_places in enumerate(chunks):
        if not day_places:
            continue

        current_time = start_hour * 60
        day_items = []
        previous_area = None

        for place in day_places:
            data = PLACE_DATA.get(
                place,
                {
                    "area": "제주",
                    "time": "09:00",
                    "duration": 90,
                    "description": "여행지"
                }
            )

            if previous_area:
                travel_time = estimate_travel_time(
                    previous_area,
                    data["area"]
                )
                current_time += travel_time

            hour = current_time // 60
            minute = current_time % 60

            if hour >= end_hour:
                break

            time_text = f"{hour:02d}:{minute:02d}"

            day_items.append({
                "time": time_text,
                "place": place,
                "area": data["area"],
                "duration": data["duration"],
                "description": data["description"]
            })

            current_time += data["duration"]
            previous_area = data["area"]

        itinerary.append({
            "day": day_index + 1,
            "items": day_items
        })

    return itinerary


# =========================
# 헤더
# =========================
st.markdown("""
<div class="hero">
    <h1>✈️ 여행 플래너</h1>
    <p>가고 싶은 곳과 여행 스타일만 입력하면 나만의 여행 일정을 만들어드려요.</p>
</div>
""", unsafe_allow_html=True)


# =========================
# 입력
# =========================
st.markdown(
    '<div class="section-title">여행 정보를 입력해주세요</div>',
    unsafe_allow_html=True
)

destination = st.text_input(
    "여행지",
    placeholder="예: 제주도"
)

hotel = st.text_input(
    "숙소",
    placeholder="예: 제주 시내 호텔"
)

col1, col2 = st.columns(2)

with col1:
    start_date_text = st.text_input(
        "여행 시작일",
        placeholder="예: 2026.10.20"
    )

with col2:
    end_date_text = st.text_input(
        "여행 종료일",
        placeholder="예: 2026.10.23"
    )

places_text = st.text_area(
    "가고 싶은 장소",
    placeholder="예: 성산일출봉, 섭지코지, 우도, 월정리, 함덕해수욕장",
    height=110
)

preference = st.text_area(
    "여행 스타일",
    placeholder="예: 너무 빡빡하지 않게 하고 싶고 맛집과 카페도 많이 가고 싶어요.",
    height=100
)

transport = st.text_input(
    "이동수단",
    placeholder="예: 렌터카"
)


# =========================
# 일정 생성
# =========================
st.markdown("")

if st.button("✨ 여행 일정 만들기"):
    if not destination.strip():
        st.error("여행지를 입력해주세요.")
        st.stop()

    if not start_date_text.strip() or not end_date_text.strip():
        st.error("여행 시작일과 종료일을 입력해주세요.")
        st.stop()

    start_date = parse_date(start_date_text)
    end_date = parse_date(end_date_text)

    if not start_date or not end_date:
        st.error(
            "날짜 형식을 확인해주세요. 예: 2026.10.20"
        )
        st.stop()

    if end_date < start_date:
        st.error("종료일은 시작일보다 빠를 수 없습니다.")
        st.stop()

    places = parse_places(places_text)

    if not places:
        st.error("가고 싶은 장소를 하나 이상 입력해주세요.")
        st.stop()

    days = (end_date - start_date).days + 1

    style, start_hour, end_hour = analyze_preference(
        preference
    )

    itinerary = generate_itinerary(
        places,
        days,
        start_hour,
        end_hour,
        style
    )

    # =========================
    # 여행 요약
    # =========================
    st.markdown(
        '<div class="section-title">여행 요약</div>',
        unsafe_allow_html=True
    )

    st.markdown(f"""
    <div class="summary">
        <h3>📍 {destination}</h3>
        <p><strong>숙소</strong>　{hotel if hotel else "입력하지 않음"}</p>
        <p><strong>기간</strong>　{start_date.strftime("%Y.%m.%d")} ~ {end_date.strftime("%Y.%m.%d")}</p>
        <p><strong>여행일</strong>　{days}일</p>
        <p><strong>이동수단</strong>　{transport if transport else "입력하지 않음"}</p>
        <p><strong>여행 스타일</strong>　{style}</p>
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # 일정
    # =========================
    st.markdown(
        '<div class="section-title">추천 일정</div>',
        unsafe_allow_html=True
    )

    for day in itinerary:
        actual_date = start_date + timedelta(days=day["day"] - 1)

        st.markdown(
            f"""
            <div class="day-title">
                DAY {day["day"]} · {actual_date.strftime("%m월 %d일")}
            </div>
            """,
            unsafe_allow_html=True
        )

        if not day["items"]:
            st.info("이 날에는 추천 일정이 없습니다.")
            continue

        for item in day["items"]:
            duration_hours = item["duration"] // 60

            if item["duration"] % 60:
                duration_text = (
                    f"{duration_hours}시간 "
                    f"{item['duration'] % 60}분"
                )
            else:
                duration_text = f"{duration_hours}시간"

            st.markdown(
                f"""
                <div class="place-card">
                    <div>
                        <span class="tag">{item["time"]}</span>
                        <span class="tag">{item["area"]}</span>
                    </div>
                    <br>
                    <strong style="font-size:19px;">
                        {item["place"]}
                    </strong>
                    <p>{item["description"]}</p>
                    <small>예상 체류시간 · {duration_text}</small>
                </div>
                """,
                unsafe_allow_html=True
            )

    # =========================
    # 지도
    # =========================
    st.markdown(
        '<div class="section-title">🗺️ 이동 경로</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="result-card">
        <h3>여행 경로 지도</h3>
        <p>
            현재 버전에서는 지도 API 연결 전 단계입니다.
            이후 실제 장소의 좌표를 이용해 이동 경로와 예상 이동시간을 표시할 수 있습니다.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # 맛집 / 카페
    # =========================
    st.markdown(
        '<div class="section-title">🍴 일정 주변 추천</div>',
        unsafe_allow_html=True
    )

    for restaurant in RESTAURANTS:
        st.markdown(
            f"""
            <div class="restaurant-card">
                <h4>{restaurant["name"]}</h4>
                <p>
                    <span class="tag">{restaurant["area"]}</span>
                    <span class="tag">{restaurant["type"]}</span>
                </p>
                <p>{restaurant["description"]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # =========================
    # 안내
    # =========================
    st.markdown("---")

    st.markdown("""
    <div style="text-align:center; padding:20px;">
        <p style="color:#888 !important;">
            여행 일정은 입력한 장소와 여행 스타일을 기준으로 구성됩니다.
        </p>
    </div>
    """, unsafe_allow_html=True)
