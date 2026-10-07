import streamlit as st
from datetime import datetime, timedelta
import re

# =========================================================
# 페이지 설정
# =========================================================

st.set_page_config(
    page_title="TripFlow",
    page_icon="✈️",
    layout="wide"
)

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background: #f7f8fc;
}

/* 전체 여백 */
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* Hero */
.hero {
    text-align: center;
    padding: 55px 20px 40px 20px;
}

.hero-title {
    font-size: 52px;
    font-weight: 800;
    letter-spacing: -2px;
    margin-bottom: 12px;
}

.hero-subtitle {
    font-size: 18px;
    color: #777;
    line-height: 1.7;
}

/* 입력 카드 */
.input-card {
    background: white;
    padding: 30px;
    border-radius: 22px;
    border: 1px solid #eeeeee;
    margin-bottom: 20px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.03);
}

/* 질문 */
.question {
    font-size: 20px;
    font-weight: 750;
    margin-bottom: 8px;
}

/* 설명 */
.description {
    color: #888;
    font-size: 14px;
    margin-bottom: 12px;
}

/* 결과 카드 */
.result-card {
    background: white;
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 15px;
    border: 1px solid #eeeeee;
}

/* 일정 */
.day-title {
    font-size: 26px;
    font-weight: 800;
    margin-top: 25px;
    margin-bottom: 5px;
}

.day-info {
    color: #777;
    margin-bottom: 18px;
}

/* 장소 */
.place-card {
    background: white;
    border: 1px solid #eeeeee;
    border-radius: 15px;
    padding: 18px;
    margin-bottom: 12px;
}

.place-time {
    color: #777;
    font-size: 14px;
    font-weight: 600;
}

.place-name {
    font-size: 19px;
    font-weight: 750;
    margin-top: 5px;
}

/* 요약 */
.summary {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 28px;
    border-radius: 22px;
    margin-bottom: 25px;
}

.summary-title {
    font-size: 25px;
    font-weight: 800;
}

.summary-item {
    margin-top: 15px;
}

.summary-number {
    font-size: 25px;
    font-weight: 800;
}

/* 태그 */
.tag {
    display: inline-block;
    background: #f0f2ff;
    color: #555;
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 12px;
    margin-right: 5px;
}

/* 버튼 */
.stButton > button {
    border-radius: 13px;
    height: 52px;
    font-size: 16px;
    font-weight: 700;
}

/* 입력창 */
.stTextInput input,
.stTextArea textarea {
    border-radius: 12px;
}

/* Footer */
.footer {
    text-align: center;
    color: #999;
    padding: 30px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# Session State
# =========================================================

if "generated" not in st.session_state:
    st.session_state.generated = False

if "itinerary" not in st.session_state:
    st.session_state.itinerary = []


# =========================================================
# 예시 장소 데이터
# 나중에 실제 API 데이터로 교체
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
# 예시 맛집 데이터
# =========================================================

RESTAURANTS = [

    {
        "name": "제주 흑돼지 맛집",
        "category": "흑돼지",
        "rating": 4.7,
        "price": "₩20,000 ~ ₩35,000",
        "area": "제주시"
    },

    {
        "name": "바다뷰 해산물 식당",
        "category": "해산물",
        "rating": 4.6,
        "price": "₩15,000 ~ ₩30,000",
        "area": "동부"
    },

    {
        "name": "애월 갈치조림",
        "category": "갈치조림",
        "rating": 4.5,
        "price": "₩18,000 ~ ₩30,000",
        "area": "서부"
    }

]


# =========================================================
# 유틸 함수
# =========================================================

def format_minutes(minutes):

    hours = minutes // 60
    mins = minutes % 60

    if hours == 0:
        return f"{mins}분"

    if mins == 0:
        return f"{hours}시간"

    return f"{hours}시간 {mins}분"


# =========================================================
# 날짜 파싱
# =========================================================

def parse_date(date_text):

    date_text = date_text.strip()

    formats = [
        "%Y.%m.%d",
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%Y. %m. %d.",
        "%Y년 %m월 %d일"
    ]

    for fmt in formats:

        try:
            return datetime.strptime(
                date_text,
                fmt
            ).date()

        except ValueError:
            pass

    return None


# =========================================================
# 장소 이름 정리
# =========================================================

def parse_places(text):

    # 쉼표 / 줄바꿈 / 슬래시 등을 기준으로 분리
    places = re.split(
        r",|\n|/|·",
        text
    )

    places = [
        place.strip()
        for place in places
        if place.strip()
    ]

    return places


# =========================================================
# 장소 데이터 찾기
# =========================================================

def find_place_data(place):

    # 정확히 일치
    if place in PLACE_DATA:
        return PLACE_DATA[place]

    # 일부 이름이 일치하는 경우
    for name, data in PLACE_DATA.items():

        if place in name or name in place:
            return data

    # 실제 API 연결 전 임시 기본값
    return {
        "category": "관광",
        "stay": 90,
        "area": "미정",
        "emoji": "📍"
    }


# =========================================================
# 여행 일정 생성
# =========================================================

def generate_itinerary(
    places,
    start_date,
    end_date,
    travel_style,
    start_hour,
    end_hour
):

    total_days = (
        end_date - start_date
    ).days + 1

    if not places:
        return []

    # 장소 데이터 정리
    place_objects = []

    for place in places:

        data = find_place_data(place)

        place_objects.append({
            "name": place,
            **data
        })

    # 지역별 그룹
    groups = {}

    for place in place_objects:

        area = place["area"]

        if area not in groups:
            groups[area] = []

        groups[area].append(place)

    areas = list(groups.keys())

    # 하루 최대 장소 수
    if travel_style == "여유롭게":
        max_places = 2

    elif travel_style == "빡빡하게":
        max_places = 4

    else:
        max_places = 3

    itinerary = []

    remaining = place_objects.copy()

    for day_index in range(total_days):

        if not remaining:
            break

        # 지역 분산
        selected = []

        current_area = None

        # 아직 남은 장소 중 첫 번째 지역 선택
        current_area = remaining[0]["area"]

        candidates = [
            place
            for place in remaining
            if place["area"] == current_area
        ]

        selected = candidates[:max_places]

        # 지역에 장소가 너무 적으면 다른 지역 추가
        if len(selected) < max_places:

            for place in remaining:

                if place not in selected:

                    selected.append(place)

                if len(selected) >= max_places:
                    break

        # 선택한 장소 제거
        for place in selected:

            if place in remaining:
                remaining.remove(place)

        # 일정 시간 계산
        current_minutes = start_hour * 60

        # 숙소 → 첫 장소
        current_minutes += 30

        total_travel = 30
        total_stay = 0

        schedule = []

        for index, place in enumerate(selected):

            arrival = current_minutes

            stay = place["stay"]

            start_time = arrival
            end_time = arrival + stay

            # 하루 종료시간을 넘으면 조정
            if end_time > end_hour * 60:

                break

            schedule.append({

                "name": place["name"],

                "emoji": place["emoji"],

                "category": place["category"],

                "area": place["area"],

                "start": start_time,

                "end": end_time,

                "stay": stay

            })

            total_stay += stay

            # 다음 장소 이동
            if index < len(selected) - 1:

                travel_time = 20 + index * 10

                current_minutes = (
                    end_time + travel_time
                )

                total_travel += travel_time

        itinerary.append({

            "day": day_index + 1,

            "date": start_date + timedelta(
                days=day_index
            ),

            "area": current_area,

            "schedule": schedule,

            "travel": total_travel,

            "stay": total_stay

        })

    return itinerary


# =========================================================
# 시간 표시
# =========================================================

def time_string(minutes):

    hour = minutes // 60
    minute = minutes % 60

    return f"{hour:02d}:{minute:02d}"


# =========================================================
# HERO
# =========================================================

st.markdown("""
<div class="hero">

<div class="hero-title">
✈️ TripFlow
</div>

<div class="hero-subtitle">
가고 싶은 곳과 여행 정보만 알려주세요.<br>
복잡한 일정은 TripFlow가 알아서 정리해드릴게요.
</div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# 여행지
# =========================================================

st.markdown("""
<div class="input-card">

<div class="question">
📍 어디로 여행하시나요?
</div>

<div class="description">
도시나 여행지를 자유롭게 입력해주세요.
</div>

</div>
""", unsafe_allow_html=True)

destination = st.text_input(
    "여행지",
    placeholder="예: 제주도",
    label_visibility="collapsed"
)


# =========================================================
# 숙소
# =========================================================

st.markdown("""
<div class="input-card">

<div class="question">
🏨 어디에서 머무르시나요?
</div>

<div class="description">
숙소 이름을 입력해주세요. 정확한 위치는 나중에 자동으로 확인합니다.
</div>

</div>
""", unsafe_allow_html=True)

hotel = st.text_input(
    "숙소",
    placeholder="예: 제주 애월 ○○호텔",
    label_visibility="collapsed"
)


# =========================================================
# 날짜
# =========================================================

st.markdown("""
<div class="input-card">

<div class="question">
📅 언제 떠나시나요?
</div>

<div class="description">
날짜를 직접 입력해주세요. 예: 2026.10.20
</div>

</div>
""", unsafe_allow_html=True)

date_col1, date_col2 = st.columns(2)

with date_col1:

    start_date_text = st.text_input(
        "여행 시작일",
        placeholder="2026.10.20"
    )

with date_col2:

    end_date_text = st.text_input(
        "여행 종료일",
        placeholder="2026.10.23"
    )


# =========================================================
# 가고 싶은 장소
# =========================================================

st.markdown("""
<div class="input-card">

<div class="question">
❤️ 가고 싶은 곳을 알려주세요.
</div>

<div class="description">
쉼표로 여러 장소를 구분해주세요. 꼭 가고 싶은 곳이라면 모두 적어주세요.
</div>

</div>
""", unsafe_allow_html=True)

places_text = st.text_area(
    "가고 싶은 곳",
    placeholder="예: 성산일출봉, 우도, 협재해수욕장, 한라산",
    height=120,
    label_visibility="collapsed"
)


# =========================================================
# 여행 스타일
# =========================================================

st.markdown("""
<div class="input-card">

<div class="question">
🌿 어떤 여행을 하고 싶으신가요?
</div>

<div class="description">
여행의 분위기나 원하는 조건을 자유롭게 적어주세요.
</div>

</div>
""", unsafe_allow_html=True)

travel_preference = st.text_area(
    "여행 스타일",
    placeholder=(
        "예: 너무 빡빡하지 않게 여행하고 싶어요. "
        "맛집과 카페를 많이 가고 싶고 아침에는 천천히 출발하고 싶어요."
    ),
    height=120,
    label_visibility="collapsed"
)


# =========================================================
# 이동수단
# =========================================================

st.markdown("""
<div class="input-card">

<div class="question">
🚗 어떻게 이동하시나요?
</div>

<div class="description">
이동수단을 자유롭게 입력해주세요.
</div>

</div>
""", unsafe_allow_html=True)

transport = st.text_input(
    "이동수단",
    placeholder="예: 렌터카 / 대중교통 / 택시",
    label_visibility="collapsed"
)


# =========================================================
# 여행 일정 생성
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)

generate_button = st.button(
    "✨ 내 여행 일정 만들어보기",
    use_container_width=True,
    type="primary"
)


# =========================================================
# 입력 검증 + 생성
# =========================================================

if generate_button:

    errors = []

    # 여행지
    if not destination.strip():
        errors.append("여행지를 입력해주세요.")

    # 숙소
    if not hotel.strip():
        errors.append("숙소를 입력해주세요.")

    # 날짜
    start_date = parse_date(start_date_text)
    end_date = parse_date(end_date_text)

    if start_date is None:
        errors.append(
            "여행 시작일을 올바른 형식으로 입력해주세요. "
            "(예: 2026.10.20)"
        )

    if end_date is None:
        errors.append(
            "여행 종료일을 올바른 형식으로 입력해주세요. "
            "(예: 2026.10.23)"
        )

    if (
        start_date is not None
        and end_date is not None
        and end_date < start_date
    ):
        errors.append(
            "여행 종료일은 시작일보다 빠를 수 없습니다."
        )

    # 장소
    places = parse_places(places_text)

    if not places:
        errors.append(
            "가고 싶은 장소를 하나 이상 입력해주세요."
        )

    # 에러 출력
    if errors:

        for error in errors:
            st.error(error)

    else:

        # -------------------------------------------------
        # 여행 스타일 간단 분석
        # -------------------------------------------------

        preference_lower = (
            travel_preference.lower()
        )

        if any(
            word in preference_lower
            for word in [
                "여유",
                "천천히",
                "느긋",
                "편하게"
            ]
        ):

            travel_style = "여유롭게"

        elif any(
            word in preference_lower
            for word in [
                "많이",
                "빡빡",
                "최대한",
                "알차게"
            ]
        ):

            travel_style = "빡빡하게"

        else:

            travel_style = "보통"

        # -------------------------------------------------
        # 출발/종료시간 분석
        # -------------------------------------------------

        start_hour = 9
        end_hour = 21

        # 아침 늦게
        if any(
            word in preference_lower
            for word in [
                "아침에 늦",
                "천천히 출발",
                "늦게 출발"
            ]
        ):

            start_hour = 10

        # 일찍 출발
        if any(
            word in preference_lower
            for word in [
                "일찍",
                "아침 일찍"
            ]
        ):

            start_hour = 7

        # 늦게까지
        if any(
            word in preference_lower
            for word in [
                "늦게까지",
                "밤까지",
                "밤에도"
            ]
        ):

            end_hour = 23

        # -------------------------------------------------
        # 일정 생성
        # -------------------------------------------------

        with st.spinner(
            "여행지와 이동 동선을 분석하고 있어요..."
        ):

            itinerary = generate_itinerary(
                places=places,
                start_date=start_date,
                end_date=end_date,
                travel_style=travel_style,
                start_hour=start_hour,
                end_hour=end_hour
            )

            st.session_state.itinerary = itinerary
            st.session_state.generated = True

        st.success(
            "여행 계획을 완성했어요! 아래에서 확인해보세요."
        )


# =========================================================
# 결과
# =========================================================

if st.session_state.generated:

    itinerary = st.session_state.itinerary

    st.divider()

    # -----------------------------------------------------
    # 여행 기본 요약
    # -----------------------------------------------------

    total_places = sum(
        len(day["schedule"])
        for day in itinerary
    )

    total_travel = sum(
        day["travel"]
        for day in itinerary
    )

    total_stay = sum(
        day["stay"]
        for day in itinerary
    )

    total_days = (
        itinerary[-1]["date"]
        - itinerary[0]["date"]
    ).days + 1

    st.markdown(
        f"""
        <div class="summary">

        <div class="summary-title">
        ✈️ {destination} 여행
        </div>

        <p>
        🏨 {hotel}
        </p>

        <div style="
            display:flex;
            gap:45px;
            flex-wrap:wrap;
        ">

        <div class="summary-item">
        <div>여행 기간</div>
        <div class="summary-number">
        {total_days}일
        </div>
        </div>

        <div class="summary-item">
        <div>방문 장소</div>
        <div class="summary-number">
        {total_places}곳
        </div>
        </div>

        <div class="summary-item">
        <div>예상 이동</div>
        <div class="summary-number">
        {format_minutes(total_travel)}
        </div>
        </div>

        <div class="summary-item">
        <div>관광 시간</div>
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
    # 지도 + 일정
    # -----------------------------------------------------

    map_col, schedule_col = st.columns(
        [1, 1.25]
    )

    with map_col:

        st.subheader("🗺️ 여행 경로")

        st.markdown(
            """
            <div style="
                height:500px;
                background:#eef0f5;
                border-radius:20px;
                display:flex;
                align-items:center;
                justify-content:center;
                text-align:center;
                color:#777;
                font-size:18px;
            ">

            🗺️<br>
            실제 지도 API 연결 예정

            </div>
            """,
            unsafe_allow_html=True
        )

        st.caption(
            "현재 버전에서는 지도 API 연결 전입니다."
        )

    # -----------------------------------------------------
    # 일정
    # -----------------------------------------------------

    with schedule_col:

        st.subheader("📅 상세 일정")

        for day in itinerary:

            date_string = day["date"].strftime(
                "%Y.%m.%d"
            )

            st.markdown(
                f"""
                <div class="day-title">
                DAY {day['day']}
                </div>

                <div class="day-info">
                {date_string}
                · 📍 {day['area']}
                · 🚗 이동 {format_minutes(day['travel'])}
                </div>
                """,
                unsafe_allow_html=True
            )

            for item in day["schedule"]:

                st.markdown(
                    f"""
                    <div class="place-card">

                    <div class="place-time">
                    {time_string(item['start'])}
                    ~
                    {time_string(item['end'])}
                    </div>

                    <div class="place-name">
                    {item['emoji']}
                    {item['name']}
                    </div>

                    <br>

                    <span class="tag">
                    {item['category']}
                    </span>

                    <span class="tag">
                    {item['area']}
                    </span>

                    <p>
                    예상 체류시간:
                    <b>{format_minutes(item['stay'])}</b>
                    </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.divider()


# =========================================================
# 맛집
# =========================================================

if st.session_state.generated:

    st.header("🍜 일정에 어울리는 맛집")

    st.caption(
        "현재는 예시 데이터입니다. "
        "다음 단계에서 실제 장소 검색 API와 연결합니다."
    )

    restaurant_cols = st.columns(3)

    for i, restaurant in enumerate(
        RESTAURANTS
    ):

        with restaurant_cols[i]:

            st.markdown(
                f"""
                <div class="result-card">

                <h3>
                🍜 {restaurant['name']}
                </h3>

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

st.markdown(
    """
    <div class="footer">
    TripFlow · 내가 가고 싶은 곳으로 만드는 여행
    </div>
    """,
    unsafe_allow_html=True
)
