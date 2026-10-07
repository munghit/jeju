import streamlit as st
from datetime import date, timedelta
from math import ceil

# =========================================================
# 기본 설정
# =========================================================

st.set_page_config(
    page_title="TripFlow",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>
    .main {
        background-color: #f7f8fc;
    }

    .hero {
        padding: 45px 20px 35px 20px;
        text-align: center;
    }

    .hero h1 {
        font-size: 46px;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .hero p {
        font-size: 18px;
        color: #666;
    }

    .card {
        background: white;
        padding: 22px;
        border-radius: 18px;
        border: 1px solid #eeeeee;
        margin-bottom: 15px;
    }

    .day-title {
        font-size: 25px;
        font-weight: 800;
        margin-bottom: 15px;
    }

    .timeline {
        border-left: 3px solid #dddddd;
        padding-left: 20px;
        margin-left: 10px;
    }

    .place {
        background: #ffffff;
        border-radius: 14px;
        padding: 15px;
        margin-bottom: 12px;
        border: 1px solid #eeeeee;
    }

    .time {
        color: #666;
        font-size: 14px;
        font-weight: 600;
    }

    .tag {
        display: inline-block;
        background: #f0f2ff;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 13px;
        margin-right: 5px;
    }

    .summary {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 25px;
    }

    .summary-number {
        font-size: 27px;
        font-weight: 800;
    }

    .stButton > button {
        border-radius: 12px;
        height: 48px;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# Session State
# =========================================================

if "places" not in st.session_state:
    st.session_state.places = []

if "generated" not in st.session_state:
    st.session_state.generated = False

if "itinerary" not in st.session_state:
    st.session_state.itinerary = []


# =========================================================
# 장소 데이터
# 초안에서는 예시 데이터 사용
# =========================================================

PLACE_DATA = {
    "성산일출봉": {
        "category": "자연",
        "stay": 120,
        "area": "동부",
        "emoji": "🌋"
    },
    "우도": {
        "category": "자연",
        "stay": 180,
        "area": "동부",
        "emoji": "🏝️"
    },
    "협재해수욕장": {
        "category": "자연",
        "stay": 90,
        "area": "서부",
        "emoji": "🏖️"
    },
    "애월 카페거리": {
        "category": "카페",
        "stay": 120,
        "area": "서부",
        "emoji": "☕"
    },
    "동문시장": {
        "category": "시장",
        "stay": 90,
        "area": "제주시",
        "emoji": "🛍️"
    },
    "한라산": {
        "category": "자연",
        "stay": 300,
        "area": "중부",
        "emoji": "⛰️"
    },
    "섭지코지": {
        "category": "자연",
        "stay": 90,
        "area": "동부",
        "emoji": "🌊"
    },
    "오설록 티 뮤지엄": {
        "category": "관광",
        "stay": 90,
        "area": "서부",
        "emoji": "🍵"
    }
}


# =========================================================
# 가상 맛집 데이터
# =========================================================

RESTAURANTS = [
    {
        "name": "제주 흑돼지 맛집",
        "category": "흑돼지",
        "rating": 4.7,
        "price": "₩20,000~₩35,000",
        "area": "제주시"
    },
    {
        "name": "바다뷰 해산물 식당",
        "category": "해산물",
        "rating": 4.6,
        "price": "₩15,000~₩30,000",
        "area": "동부"
    },
    {
        "name": "애월 갈치조림",
        "category": "갈치조림",
        "rating": 4.5,
        "price": "₩18,000~₩30,000",
        "area": "서부"
    }
]


# =========================================================
# 함수
# =========================================================

def format_minutes(minutes):
    hours = minutes // 60
    mins = minutes % 60

    if hours == 0:
        return f"{mins}분"

    if mins == 0:
        return f"{hours}시간"

    return f"{hours}시간 {mins}분"


def generate_itinerary(
    places,
    start_date,
    end_date,
    travel_style,
    start_time,
    end_time
):

    days = (end_date - start_date).days + 1

    if not places:
        return []

    # 지역별 그룹
    groups = {}

    for place in places:
        data = PLACE_DATA.get(place)

        if not data:
            continue

        area = data["area"]

        if area not in groups:
            groups[area] = []

        groups[area].append(place)

    # 여행일수에 맞게 지역 분배
    areas = list(groups.keys())

    itinerary = []

    for day_index in range(days):

        if not areas:
            break

        area = areas[day_index % len(areas)]

        today_places = groups[area]

        # 하루에 들어갈 장소 수
        if travel_style == "여유롭게":
            max_places = 2
        elif travel_style == "빡빡하게":
            max_places = 4
        else:
            max_places = 3

        selected = today_places[:max_places]

        # 사용된 장소 제거
        groups[area] = today_places[max_places:]

        # 남은 장소가 있으면 다음 날에 처리
        current_minutes = start_time.hour * 60 + start_time.minute

        schedule = []

        # 가상의 숙소 출발
        current_minutes += 30

        total_travel = 30
        total_stay = 0

        for index, place in enumerate(selected):

            data = PLACE_DATA[place]

            arrival = current_minutes

            stay = data["stay"]

            total_stay += stay

            start_hour = arrival // 60
            start_minute = arrival % 60

            end = arrival + stay

            end_hour = end // 60
            end_minute = end % 60

            schedule.append({
                "place": place,
                "emoji": data["emoji"],
                "category": data["category"],
                "start": f"{start_hour:02d}:{start_minute:02d}",
                "end": f"{end_hour:02d}:{end_minute:02d}",
                "stay": stay
            })

            # 다음 장소 이동
            if index < len(selected) - 1:
                travel_time = 20 + index * 10
                current_minutes = end + travel_time
                total_travel += travel_time

        itinerary.append({
            "day": day_index + 1,
            "date": start_date + timedelta(days=day_index),
            "area": area,
            "schedule": schedule,
            "travel": total_travel,
            "stay": total_stay
        })

    return itinerary


# =========================================================
# HERO
# =========================================================

st.markdown("""
<div class="hero">

<h1>✈️ TripFlow</h1>

<p>
숙소와 가고 싶은 곳만 알려주세요.<br>
나머지는 가장 효율적인 여행 코스로 만들어드릴게요.
</p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# 여행 기본정보
# =========================================================

st.subheader("🧳 여행 정보")

col1, col2 = st.columns(2)

with col1:

    destination = st.text_input(
        "📍 여행지",
        placeholder="예: 제주도"
    )

    hotel = st.text_input(
        "🏨 숙소",
        placeholder="예: 제주 애월 ○○호텔"
    )

with col2:

    start_date = st.date_input(
        "📅 여행 시작일",
        value=date.today()
    )

    end_date = st.date_input(
        "📅 여행 종료일",
        value=date.today() + timedelta(days=3)
    )


# =========================================================
# 이동수단
# =========================================================

st.subheader("🚗 이동수단")

transport = st.radio(
    "주 이동수단",
    [
        "🚗 렌터카",
        "🚌 대중교통",
        "🚕 택시",
        "🚶 도보"
    ],
    horizontal=True
)


# =========================================================
# 여행 스타일
# =========================================================

st.subheader("✨ 여행 스타일")

col1, col2, col3 = st.columns(3)

with col1:
    travel_style = st.selectbox(
        "여행 강도",
        [
            "여유롭게",
            "보통",
            "빡빡하게"
        ]
    )

with col2:
    start_hour = st.slider(
        "하루 시작 시간",
        6,
        12,
        9
    )

with col3:
    end_hour = st.slider(
        "하루 종료 시간",
        17,
        24,
        21
    )


# =========================================================
# 가고 싶은 장소
# =========================================================

st.subheader("❤️ 가고 싶은 곳")

available_places = list(PLACE_DATA.keys())

selected_places = st.multiselect(
    "방문하고 싶은 장소를 선택하세요.",
    available_places,
    placeholder="장소를 선택해주세요."
)

st.session_state.places = selected_places


# =========================================================
# 장소 미리보기
# =========================================================

if selected_places:

    st.markdown("### 선택한 장소")

    cols = st.columns(3)

    for i, place in enumerate(selected_places):

        data = PLACE_DATA[place]

        with cols[i % 3]:

            st.markdown(
                f"""
                <div class="card">

                <h3>{data['emoji']} {place}</h3>

                <span class="tag">{data['category']}</span>
                <span class="tag">{data['area']}</span>

                <p>
                예상 체류시간<br>
                <b>{format_minutes(data['stay'])}</b>
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# 일정 생성
# =========================================================

st.markdown("")

if st.button(
    "✨ 최적의 여행 일정 만들기",
    use_container_width=True,
    type="primary"
):

    if not destination:
        st.warning("여행지를 입력해주세요.")

    elif not hotel:
        st.warning("숙소를 입력해주세요.")

    elif not selected_places:
        st.warning("가고 싶은 장소를 하나 이상 선택해주세요.")

    elif end_date < start_date:
        st.error("여행 종료일을 확인해주세요.")

    else:

        with st.spinner("여행 동선을 계산하고 있습니다..."):

            start_time = start_date

            from datetime import datetime

            start_time_obj = datetime.strptime(
                f"{start_hour}:00",
                "%H:%M"
            )

            end_time_obj = datetime.strptime(
                f"{end_hour}:00",
                "%H:%M"
            )

            itinerary = generate_itinerary(
                selected_places,
                start_date,
                end_date,
                travel_style,
                start_time_obj,
                end_time_obj
            )

            st.session_state.itinerary = itinerary
            st.session_state.generated = True

        st.success("여행 일정이 완성되었습니다!")


# =========================================================
# 일정 출력
# =========================================================

if st.session_state.generated:

    st.divider()

    st.header("🗺️ 나의 여행 일정")

    itinerary = st.session_state.itinerary

    total_travel = sum(
        day["travel"]
        for day in itinerary
    )

    total_stay = sum(
        day["stay"]
        for day in itinerary
    )

    total_places = sum(
        len(day["schedule"])
        for day in itinerary
    )

    # -----------------------------------------------------
    # 전체 요약
    # -----------------------------------------------------

    st.markdown(
        f"""
        <div class="summary">

        <h2>✈️ {destination} 여행</h2>

        <p>{hotel}</p>

        <div style="display:flex; gap:50px; flex-wrap:wrap;">

        <div>
        <div>방문 장소</div>
        <div class="summary-number">{total_places}곳</div>
        </div>

        <div>
        <div>예상 이동시간</div>
        <div class="summary-number">
        {format_minutes(total_travel)}
        </div>
        </div>

        <div>
        <div>관광시간</div>
        <div class="summary-number">
        {format_minutes(total_stay)}
        </div>
        </div>

        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # 지도 자리
    # -----------------------------------------------------

    map_col, schedule_col = st.columns([1, 1.25])

    with map_col:

        st.subheader("🗺️ 여행 경로")

        st.info(
            "현재는 지도 API 연결 전입니다.\n\n"
            "다음 단계에서 실제 지도와 이동 경로를 연결할 예정입니다."
        )

        st.markdown(
            """
            <div style="
                height:420px;
                background:#eef0f5;
                border-radius:20px;
                display:flex;
                align-items:center;
                justify-content:center;
                color:#777;
                font-size:18px;
            ">
            🗺️ MAP API 영역
            </div>
            """,
            unsafe_allow_html=True
        )

    # -----------------------------------------------------
    # 일정
    # -----------------------------------------------------

    with schedule_col:

        st.subheader("📅 상세 일정")

        for day in itinerary:

            st.markdown(
                f"""
                <div class="day-title">
                DAY {day['day']} · {day['date'].strftime('%m/%d')}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.caption(
                f"📍 {day['area']} · "
                f"🚗 이동 {format_minutes(day['travel'])}"
            )

            for item in day["schedule"]:

                st.markdown(
                    f"""
                    <div class="place">

                    <div class="time">
                    {item['start']} ~ {item['end']}
                    </div>

                    <h3>
                    {item['emoji']} {item['place']}
                    </h3>

                    <span class="tag">
                    {item['category']}
                    </span>

                    <p>
                    예상 체류시간:
                    <b>{format_minutes(item['stay'])}</b>
                    </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("---")


# =========================================================
# 맛집 추천
# =========================================================

if st.session_state.generated:

    st.header("🍜 일정 주변 맛집")

    cols = st.columns(3)

    for i, restaurant in enumerate(RESTAURANTS):

        with cols[i]:

            st.markdown(
                f"""
                <div class="card">

                <h3>🍜 {restaurant['name']}</h3>

                <p>
                ⭐ <b>{restaurant['rating']}</b>
                </p>

                <p>
                🍽 {restaurant['category']}<br>
                💰 {restaurant['price']}<br>
                📍 {restaurant['area']}
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# Footer
# =========================================================

st.divider()

st.caption(
    "TripFlow · 나만의 여행 동선을 만들어보세요 ✈️"
)
