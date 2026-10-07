# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

/* =====================================================
   전체 페이지
===================================================== */

.stApp {
    background-color: #f7f8fc;
    color: #222222;
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}


/* =====================================================
   기본 텍스트
===================================================== */

h1, h2, h3, h4, h5, h6 {
    color: #222222 !important;
}

p {
    color: #333333;
}


/* =====================================================
   Hero
===================================================== */

.hero {
    text-align: center;
    padding: 55px 20px 40px 20px;
}

.hero-title {
    color: #222222 !important;
    font-size: 52px;
    font-weight: 800;
    letter-spacing: -2px;
    margin-bottom: 12px;
}

.hero-subtitle {
    color: #666666 !important;
    font-size: 18px;
    line-height: 1.7;
}


/* =====================================================
   입력 카드
===================================================== */

.input-card {
    background-color: #ffffff;
    padding: 30px;
    border-radius: 22px;
    border: 1px solid #e5e5e5;
    margin-bottom: 10px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.04);
}

.question {
    color: #222222 !important;
    font-size: 20px;
    font-weight: 750;
    margin-bottom: 8px;
}

.description {
    color: #777777 !important;
    font-size: 14px;
    margin-bottom: 12px;
}


/* =====================================================
   Text Input
===================================================== */

.stTextInput label,
.stTextArea label {
    color: #333333 !important;
}

.stTextInput input,
.stTextArea textarea {

    background-color: #ffffff !important;

    color: #222222 !important;

    -webkit-text-fill-color: #222222 !important;

    border: 1px solid #d9d9d9 !important;

    border-radius: 12px !important;

    font-size: 16px !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {

    color: #999999 !important;

    -webkit-text-fill-color: #999999 !important;

    opacity: 1 !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus {

    border-color: #667eea !important;

    box-shadow: 0 0 0 1px #667eea !important;
}


/* =====================================================
   Selectbox
===================================================== */

.stSelectbox label {
    color: #333333 !important;
}

.stSelectbox div[data-baseweb="select"] > div {

    background-color: #ffffff !important;

    color: #222222 !important;

    border-color: #d9d9d9 !important;

    border-radius: 12px !important;
}


/* =====================================================
   Radio / Checkbox
===================================================== */

.stRadio label,
.stCheckbox label {

    color: #333333 !important;
}


/* =====================================================
   Button
===================================================== */

.stButton > button {

    background-color: #667eea !important;

    color: #ffffff !important;

    border: none !important;

    border-radius: 13px !important;

    height: 52px;

    font-size: 16px;

    font-weight: 700;

    transition: 0.2s;
}

.stButton > button:hover {

    background-color: #5968d8 !important;

    color: #ffffff !important;
}


/* =====================================================
   날짜 / 입력 관련
===================================================== */

input {
    color: #222222 !important;
}


/* =====================================================
   결과 카드
===================================================== */

.result-card {

    background-color: #ffffff;

    color: #222222;

    border-radius: 18px;

    padding: 22px;

    margin-bottom: 15px;

    border: 1px solid #eeeeee;

    box-shadow: 0 4px 15px rgba(0,0,0,0.03);
}

.result-card h3 {

    color: #222222 !important;
}

.result-card p {

    color: #555555 !important;
}


/* =====================================================
   일정
===================================================== */

.day-title {

    color: #222222 !important;

    font-size: 26px;

    font-weight: 800;

    margin-top: 25px;

    margin-bottom: 5px;
}

.day-info {

    color: #777777 !important;

    margin-bottom: 18px;
}


/* =====================================================
   장소 카드
===================================================== */

.place-card {

    background-color: #ffffff;

    color: #222222;

    border: 1px solid #eeeeee;

    border-radius: 15px;

    padding: 18px;

    margin-bottom: 12px;

    box-shadow: 0 3px 12px rgba(0,0,0,0.02);
}

.place-time {

    color: #777777 !important;

    font-size: 14px;

    font-weight: 600;
}

.place-name {

    color: #222222 !important;

    font-size: 19px;

    font-weight: 750;

    margin-top: 5px;
}

.place-card p {

    color: #555555 !important;
}


/* =====================================================
   Tag
===================================================== */

.tag {

    display: inline-block;

    background-color: #eef0ff;

    color: #4d5db5 !important;

    padding: 5px 10px;

    border-radius: 20px;

    font-size: 12px;

    margin-right: 5px;
}


/* =====================================================
   Summary
===================================================== */

.summary {

    background: linear-gradient(
        135deg,
        #667eea,
        #764ba2
    );

    color: #ffffff !important;

    padding: 28px;

    border-radius: 22px;

    margin-bottom: 25px;
}

.summary * {

    color: #ffffff !important;
}

.summary-title {

    color: #ffffff !important;

    font-size: 25px;

    font-weight: 800;
}

.summary-item {

    color: #ffffff !important;

    margin-top: 15px;
}

.summary-number {

    color: #ffffff !important;

    font-size: 25px;

    font-weight: 800;
}


/* =====================================================
   안내 메시지
===================================================== */

.stAlert {

    border-radius: 12px;
}


/* =====================================================
   Spinner
===================================================== */

.stSpinner > div {

    color: #667eea !important;
}


/* =====================================================
   Footer
===================================================== */

.footer {

    text-align: center;

    color: #999999 !important;

    padding: 30px;
}


/* =====================================================
   구분선
===================================================== */

hr {

    border-color: #e5e5e5 !important;
}

</style>
""", unsafe_allow_html=True)ㅍ
