import streamlit as st
from datetime import datetime, date, timedelta
import math
import re

st.set_page_config(
    page_title="Triply - 여행 플래너",
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
    color: #202124;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

h1,h2,h3,h4,h5,h6 {
    color: #202124 !important;
}

p,span,label,div {
    color: #202124;
}

.hero {
    background: linear-gradient(135deg,#6d4aff,#8d70ff);
    border-radius: 28px;
    padding: 42px 44px;
    margin-bottom: 30px;
}

.hero h1 {
    color: white !important;
    font-size: 44px;
    margin: 0;
    font-weight: 800;
}

.hero p {
    color: rgba(255,255,255,.9) !important;
    font-size: 17px;
    margin-top: 10px;
}

.section-title {
    font-size: 23px;
    font-weight: 800;
    margin: 28px 0 15px;
}

.stTextInput input,
.stTextArea textarea {
    background: white !important;
    color: #202124 !important;
    -webkit-text-fill-color: #202124 !important;
    border: 1px solid #d9dce5 !important;
    border-radius: 13px !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #999 !important;
    -webkit-text-fill-color: #999 !important;
}

.stDateInput input {
    background: white !important;
    color: #202124 !important;
    -webkit-text-fill-color: #202124 !important;
    border-radius: 13px !important;
}

.stDateInput label,
.stTextInput label,
.stTextArea label {
    color: #202124 !important;
    font-weight: 700 !important;
}

.stButton button {
    width: 100%;
    border: none !important;
    border-radius: 14px !important;
    background: #6d4aff !important;
    color: white !important;
    font-weight: 800 !important;
    padding: 13px !important;
}

.stButton button:hover {
    background: #5736d5 !important;
    color: white !important;
}

.info-card {
    background: white;
    border: 1px solid #e6e8ef;
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 12px;
    box-shadow: 0 3px 12px rgba(0,0,0,.035);
}

.day-header {
    background: #eeeaff;
    color: #5d3fd0 !important;
    border-radius: 14px;
    padding: 14px 18px;
    font-weight: 800;
    margin-top: 25px;
    margin-bottom: 12px;
}

.timeline {
    position: relative;
    padding-left: 12px;
}

.timeline-item {
    background: white;
    border: 1px solid #e6e8ef;
    border-radius: 17px;
    padding: 18px;
    margin-bottom: 10px;
}

.timeline-time {
    color: #6947df !important;
    font-size: 14px;
    font-weight: 800;
}

.timeline-title {
    color: #202124 !important;
    font-size: 19px;
    font-weight: 800;
    margin-top: 5px;
}

.timeline-desc {
    color: #666 !important;
    margin-top: 5px;
    font-size: 14px;
}

.badge {
    display: inline-block;
    padding: 5px 10px;
    background: #f0ecff;
    color: #6544d8 !important;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    margin-right: 5px;
}

.summary {
    background: linear-gradient(135deg,#6d4aff,#8265ed);
    color: white;
    border-radius: 20px;
    padding: 24px;
    margin-top: 15px;
}

.summary h3,
.summary p,
.summary strong {
    color: white !important;
}

.restaurant {
    background: white;
    border: 1px solid #e6e8ef;
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 10px;
}

.restaurant h4 {
    color: #202124 !important;
    margin: 0 0 7px;
}

.restaurant p {
    color: #666 !important;
}

.footer {
    text-align: center;
    color: #999 !important;
    padding: 30px 0;
}
</style>
""", unsafe_allow_html=True)


# =========================
# 장소 데이터
# =========================
PLACES = {
    "성산일출봉": {
        "area": "성산",
        "duration": 100,
        "type": "관광"
    },
    "섭지코지": {
        "area": "성산",
        "duration": 90,
        "type": "관광"
    },
    "우도": {
        "area": "우도",
        "duration": 300,
        "type": "관광"
    },
    "월정리": {
        "area": "동부",
        "duration": 100,
        "type": "관광"
    },
    "함덕해수욕장": {
        "area": "동부",
        "duration": 100,
        "type": "관광"
    },
    "동문시장": {
        "area": "제주시",
        "duration": 90,
        "type": "관광"
    },
    "용두암": {
        "area": "제주시",
        "duration": 60,
        "type": "관광"
    },
    "협재해수욕장": {
        "area": "서부",
        "duration": 120,
        "type": "관광"
    },
    "애월": {
        "area": "서부",
        "duration": 120,
        "type": "관광"
    },
    "오설록": {
        "area": "서부",
        "duration": 120,
        "type": "관광"
    }
}


# =========================
# 지역별 이동시간
# =========================
AREA_DISTANCE = {
    ("제주시","동부"): 45,
    ("제주시","성산"): 70,
    ("제주시","서부"): 50,
    ("제주시","우도"): 90,
    ("동부","성산"): 35,
    ("동부","서부"): 70,
    ("동부","우도"): 60,
    ("성산","서부"): 90,
    ("성산","우도"): 30,
    ("서부","우도"): 120
}


def travel_time(area1, area2):
    if area1 == area2:
        return 15

    return AREA_DISTANCE.get(
        (area1, area2),
        AREA_DISTANCE.get((area2, area1), 60)
    )


# =========================
# 입력 장소 정리
# =========================
def parse_places(text):
    text = text.replace("\n", ",")
    text = text.replace("/", ",")
    text = text.replace("·", ",")

    result = []

    for item in text.split(","):
        item = item.strip()

        if item and item not in result:
            result.append(item)

    return result


def find_place_data(name):
    if name in PLACES:
        return PLACES[name]

    for key in PLACES:
        if key in name or name in key:
            return PLACES[key]

    return {
        "area": "제주",
        "duration": 90,
        "type": "관광"
    }


# =========================
# 여행 스타일 분석
# =========================
def analyze_style(text):
    text = text.lower()

    if any(x in text for x in [
        "여유",
        "느긋",
        "천천히",
        "편하게",
        "빡빡하지 않"
    ]):
        return {
            "name": "여유롭게",
            "start": 9,
            "end": 20,
            "buffer": 25
        }

    if any(x in text for x in [
        "빡빡",
        "많이",
        "최대한",
        "알차",
        "많은 곳"
    ]):
        return {
            "name": "알차게",
            "start": 8,
            "end": 21,
            "buffer": 10
        }

    return {
        "name": "균형 있게",
        "start": 9,
        "end": 20,
        "buffer": 15
    }


# =========================
# 장소를 지역별로 묶기
# =========================
def group_places(places):
    groups = {}

    for place in places:
        data = find_place_data(place)
        area = data["area"]

        if area not in groups:
            groups[area] = []

        groups[area].append(place)

    return groups


# =========================
# 일정 분배
# =========================
def distribute_places(places, days):
    groups = group_places(places)

    # 지역을 최대한 같은 날짜에 배치
    region_groups = list(groups.values())

    result = [[] for _ in range(days)]

    # 큰 지역부터 배치
    region_groups.sort(
        key=lambda x: len(x),
        reverse=True
    )

    for group in region_groups:
        # 현재 가장 적은 장소가 들어간 날짜
        target = min(
            range(days),
            key=lambda i: len(result[i])
        )

        result[target].extend(group)

    return result


# =========================
# 하루 일정 생성
# =========================
def create_day_schedule(
    places,
    day_start,
    day_end,
    buffer_time
):
    schedule = []

    current = day_start
    previous_area = None

    for index, place in enumerate(places):
        data = find_place_data(place)

        # 이동
        if previous_area:
            move = travel_time(
                previous_area,
                data["area"]
            )

            current += timedelta(
                minutes=move
            )

        if current.hour >= day_end:
            break

        arrival = current

        duration = data["duration"]

        departure = arrival + timedelta(
            minutes=duration
        )

        if departure.hour > day_end:
            break

        schedule.append({
            "place": place,
            "area": data["area"],
            "arrival": arrival,
            "departure": departure,
            "duration": duration
        })

        current = departure + timedelta(
            minutes=buffer_time
        )

        previous_area = data["area"]

    return schedule


# =========================
# 시간 표시
# =========================
def time_text(dt):
    return dt.strftime("%H:%M")


# =========================
# 헤더
# =========================
st.markdown("""
<div class="hero">
    <h1>✈️ Triply</h1>
    <p>
        가고 싶은 곳만 입력하세요.
        이동 동선과 시간까지 고려해서 여행 일정을 자동으로 만들어드릴게요.
    </p>
</div>
""", unsafe_allow_html=True)


# =========================
# 여행 기본 정보
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

date_col1, date_col2 = st.columns(2)

with date_col1:
    start_date = st.date_input(
        "여행 시작일",
        value=date.today()
    )

with date_col2:
    end_date = st.date_input(
        "여행 종료일",
        value=date.today() + timedelta(days=2)
    )

places_text = st.text_area(
    "가고 싶은 장소",
    placeholder="예: 성산일출봉, 우도, 섭지코지, 월정리, 함덕해수욕장",
    height=120
)

preference = st.text_area(
    "여행 스타일",
    placeholder="예: 너무 빡빡하지 않게 하고 싶고 카페도 가고 싶어요.",
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

if st.button("✨ 내 여행 일정 만들기"):

    if not destination.strip():
        st.error("여행지를 입력해주세요.")
        st.stop()

    if end_date < start_date:
        st.error("종료일은 시작일보다 빠를 수 없습니다.")
        st.stop()

    places = parse_places(places_text)

    if not places:
        st.error("가고 싶은 장소를 입력해주세요.")
        st.stop()

    days = (end_date - start_date).days + 1

    style = analyze_style(preference)

    # 일정 분배
    daily_places = distribute_places(
        places,
        days
    )

    # =========================
    # 요약
    # =========================
    st.markdown(
        '<div class="section-title">여행 요약</div>',
        unsafe_allow_html=True
    )

    st.markdown(f"""
    <div class="summary">
        <h3>📍 {destination}</h3>
        <p><strong>숙소</strong>　{hotel if hotel else "미입력"}</p>
        <p>
            <strong>여행 기간</strong>　
            {start_date.strftime("%Y.%m.%d")}
            ~
            {end_date.strftime("%Y.%m.%d")}
        </p>
        <p><strong>여행 일수</strong>　{days}일</p>
        <p><strong>이동수단</strong>　{transport if transport else "미입력"}</p>
        <p><strong>일정 스타일</strong>　{style["name"]}</p>
    </div>
    """, unsafe_allow_html=True)


    # =========================
    # 일정
    # =========================
    st.markdown(
        '<div class="section-title">🗓️ 자동 생성된 여행 일정</div>',
        unsafe_allow_html=True
    )

    total_places = 0
    total_minutes = 0

    for day_index in range(days):

        current_date = start_date + timedelta(
            days=day_index
        )

        day_places = daily_places[day_index]

        day_schedule = create_day_schedule(
            day_places,
            current_date.replace(
                hour=style["start"],
                minute=0
            ),
            style["end"],
            style["buffer"]
        )

        st.markdown(
            f"""
            <div class="day-header">
                DAY {day_index + 1}
                ·
                {current_date.strftime("%m월 %d일")}
            </div>
            """,
            unsafe_allow_html=True
        )

        if not day_schedule:
            st.markdown(
                """
                <div class="info-card">
                    여유로운 자유시간으로 남겨두었습니다.
                </div>
                """,
                unsafe_allow_html=True
            )
            continue

        for item_index, item in enumerate(day_schedule):

            total_places += 1
            total_minutes += item["duration"]

            st.markdown(
                f"""
                <div class="timeline-item">
                    <div class="timeline-time">
                        {time_text(item["arrival"])}
                        ~
                        {time_text(item["departure"])}
                    </div>

                    <div class="timeline-title">
                        {item["place"]}
                    </div>

                    <div>
                        <span class="badge">
                            {item["area"]}
                        </span>
                        <span class="badge">
                            {item["duration"] // 60}시간
                            {item["duration"] % 60 if item["duration"] % 60 else ""}분
                        </span>
                    </div>

                    <div class="timeline-desc">
                        장소 이동과 체류시간을 고려해 자동 배치된 일정입니다.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # 다음 장소 이동시간
            if item_index < len(day_schedule) - 1:
                next_item = day_schedule[item_index + 1]

                move_minutes = travel_time(
                    item["area"],
                    next_item["area"]
                )

                st.markdown(
                    f"""
                    <div style="
                        text-align:center;
                        color:#888 !important;
                        font-size:13px;
                        padding:4px;
                    ">
                        🚗 다음 장소까지 약 {move_minutes}분 이동
                    </div>
                    """,
                    unsafe_allow_html=True
                )


    # =========================
    # 통계
    # =========================
    st.markdown(
        '<div class="section-title">📊 일정 요약</div>',
        unsafe_allow_html=True
    )

    hours = total_minutes // 60
    minutes = total_minutes % 60

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="info-card">
                <strong>방문 장소</strong>
                <h2>{total_places}곳</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="info-card">
                <strong>예상 관광시간</strong>
                <h2>{hours}시간 {minutes}분</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="info-card">
                <strong>여행 스타일</strong>
                <h2>{style["name"]}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )


    # =========================
    # 맛집 / 카페
    # =========================
    st.markdown(
        '<div class="section-title">🍴 식사 & 카페</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="restaurant">
        <h4>🍽️ 점심시간</h4>
        <p>
            오전 일정과 오후 일정 사이에 약 1시간의 식사시간을
            자동으로 배치할 수 있습니다.
        </p>
    </div>

    <div class="restaurant">
        <h4>☕ 카페</h4>
        <p>
            실제 장소 데이터를 연결하면 현재 동선에서 가장 가까운
            카페와 맛집을 자동으로 추천할 수 있습니다.
        </p>
    </div>
    """, unsafe_allow_html=True)


    # =========================
    # 지도
    # =========================
    st.markdown(
        '<div class="section-title">🗺️ 여행 동선</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="info-card">
        <h3>실제 지도 API 연결 예정</h3>
        <p>
            현재는 일정 최적화 구조를 먼저 구현한 상태입니다.
            다음 단계에서는 실제 장소 좌표와 도로 이동시간을 연결해서
            지도 위에 하루별 이동경로를 표시할 수 있습니다.
        </p>
    </div>
    """, unsafe_allow_html=True)


st.markdown("""
<div class="footer">
    Triply · 나만의 여행 일정을 더 쉽게
</div>
""", unsafe_allow_html=True)
