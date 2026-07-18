import streamlit as st
import pandas as pd
import os

# 1. 웹사이트 제목 및 서론
st.title("🍿 내 성향 속 숨은 미래: 진로 매칭 시네마")
st.write("3가지 성향 질문에 답하면, 베이즈 정리를 이용해 당신의 잠재적 진로를 추측하고 최적의 작품을 추천합니다.")
st.write("---")

# 2. 데이터베이스 정의 (내 컴퓨터 안의 로컬 이미지 파일 이름으로 수정!)
# 💡 팁: 실제 폴더에 넣은 사진 파일 이름과 아래 "포스터" 이름을 완전히 똑같이 맞춰주세요! (확장자 .jpg, .png 확인)
careers_profile = {
    "의학": {
        "Q1_인체": 0.95, "Q2_논리": 0.70, "Q3_이타심": 0.90, "사전확률": 0.15, 
        "추천작": "슬기로운 의사생활",
        "포스터": "dortor.webp"  # 폴더 안의 의학 관련 사진 이름
    },
    "과학/공학": {
        "Q1_기계": 0.95, "Q2_논리": 0.90, "Q3_창의성": 0.70, "사전확률": 0.15, 
        "추천작": "인터스텔라",
        "포스터": "inter.webp"   # 폴더 안의 우주/과학 사진 이름
    },
    "경영/금융": {
        "Q1_사회": 0.85, "Q2_논리": 0.85, "Q3_경쟁": 0.90, "사전확률": 0.15, 
        "추천작": "머니볼",
        "포스터": "money.webp"   # 폴더 안의 경영 사진 이름
    },
    "법조인": {
        "Q1_사회": 0.90, "Q2_논리": 0.95, "Q3_이타심": 0.75, "사전확률": 0.15, 
        "추천작": "비밀의 숲",
        "포스터": "raw.webp"     # 폴더 안의 법조인 사진 이름
    },
    "교육자": {
        "Q1_사회": 0.80, "Q2_감성": 0.85, "Q3_이타심": 0.95, "사전확률": 0.15, 
        "추천작": "죽은 시인의 사회",
        "포스터": "poet.webp"     # 폴더 안의 교육 사진 이름
    },
    "예술/미디어": {
        "Q1_예술": 0.95, "Q2_감성": 0.95, "Q3_창의성": 0.90, "사전확률": 0.15, 
        "추천작": "위플래쉬",
        "포스터": "plash.webp"     # 폴더 안의 예술 사진 이름
    },
    "심리학자": {
        "Q1_인체": 0.75, "Q2_감성": 0.90, "Q3_이타심": 0.90, "사전확률": 0.10, 
        "추천작": "인사이드 아웃",
        "포스터": "inside.webp"     # 폴더 안의 심리 사진 이름
    }
}

# 3. 메인 화면: 성향 테스트 퀴즈
st.subheader("📋 다음 질문에 솔직하게 답해 주세요")

q1 = st.radio(
    "💡 질문 1. 평소에 어떤 분야의 뉴스나 유튜브 영상을 볼 때 가장 흥미롭나요?",
    ["생명, 인체, 질병 치료 관련 (인체)", "로봇, AI, 우주, 전자기기 관련 (기계)", "경제, 트렌드, 사회적 이슈 관련 (사회)", "미술, 음악, 영화, 디자인 관련 (예술)"]
)

q2 = st.radio(
    "💡 질문 2. 문제를 해결할 때 당신의 스타일은 어떤가요?",
    ["철저한 데이터와 사실을 바탕으로 이성적으로 분석한다 (논리)", "상대방의 마음과 감정을 먼저 공감하고 직관을 따른다 (감성)"]
)

q3 = st.radio(
    "💡 질문 3. 일을 할 때 가장 큰 보람이나 자극을 느끼는 포인트는?",
    ["나의 능력으로 다른 사람을 돕거나 사회에 기여할 때 (이타심)", "남들이 생각하지 못한 참신한 아이디어를 세상에 내놓을 때 (창의성)", "치열하게 경쟁해서 목표를 달성하고 성과를 낼 때 (경쟁)"]
)

# 데이터 가공
user_ans1 = q1.split("(")[1].replace(")", "")
user_ans2 = q2.split("(")[1].replace(")", "")
user_ans3 = q3.split("(")[1].replace(")", "")

# 4. 베이즈 정리 계산 구동
posteriors = {}
total_evidence = 0

for career, profile in careers_profile.items():
    l1 = profile.get(f"Q1_{user_ans1}", 0.10)
    l2 = profile.get(f"Q2_{user_ans2}", 0.10)
    l3 = profile.get(f"Q3_{user_ans3}", 0.10)
    
    combined_likelihood = l1 * l2 * l3
    numerator = combined_likelihood * profile["사전확률"]
    posteriors[career] = numerator
    total_evidence += numerator

final_results = {}
for career, num in posteriors.items():
    final_results[career] = (num / total_evidence) if total_evidence > 0 else 0

sorted_careers = sorted(final_results.items(), key=lambda x: x[1], reverse=True)

# 5. 결과 대시보드 출력
st.write("---")
if st.button("🔮 나의 진로 성향 분석 및 영화 추천받기"):
    predicted_career = sorted_careers[0][0]
    predicted_prob = sorted_careers[0][1] * 100
    recommended_work = careers_profile[predicted_career]["추천작"]
    image_filename = careers_profile[predicted_career]["포스터"]
    
    st.subheader("🎯 알고리즘 분석 결과")
    st.success(f"당신의 답변 데이터 분석 결과, **[{predicted_career}]** 분야 성향일 확률이 **{predicted_prob:.2f}%**로 가장 높게 나타났습니다!")
    st.balloons()
    
    # 📸 화면 분할 레이아웃
    col_text, col_img = st.columns([2, 1])
    
    with col_text:
        st.markdown(f"### 🎬 추천 작품: **《 {recommended_work} 》**")
        st.write(f"당신의 학업적 성향과 논리 구조에 깊은 영감을 줄 수 있는 [{predicted_career}] 테마의 명작입니다.")
        
    with col_img:
        # 내 컴퓨터 폴더에 해당 파일이 실제로 있는지 확인 후 출력
        if os.path.exists(image_filename):
            st.image(image_filename, caption=f"{recommended_work} 포스터", use_container_width=True)
        else:
            st.warning(f"⚠️ 폴더 내에 '{image_filename}' 파일이 없습니다. 이름을 확인해 주세요!")
    
    st.write("---")
    st.subheader("📊 베이즈 정리 기반 확률 분석 리포트")
    df_report = pd.DataFrame(sorted_careers, columns=["예상 진로 분과", "매칭 확률"])
    df_report["매칭 확률"] = df_report["매칭 확률"].map(lambda x: f"{x*100:.2f}%")
    st.table(df_report)

# 6. 소감 한 줄 방명록 기능
st.write("---")
st.subheader("💬 추천 서비스 이용 소감 남기기")

if "reviews" not in st.session_state:
    st.session_state["reviews"] = [
        {"이름": "확통마스터", "소감": "진짜 베이즈 정리로 내 성향 맞춰서 소름 돋음;;"},
        {"이름": "영화조아", "소감": "발표용으로 퀄리티 대박이네요. 추천 영화 보러 갑니다."}
    ]

col1, col2 = st.columns([1, 3])
with col1:
    user_name = st.text_input("닉네임", max_chars=10, placeholder="홍길동")
with col2:
    user_review = st.text_input("한 줄 소감", placeholder="추천 결과에 대한 느낀 점을 남겨주세요!")

if st.button("소감 등록하기"):
    if user_name and user_review:
        st.session_state["reviews"].insert(0, {"이름": user_name, "소감": user_review})
        st.toast("소감이 성공적으로 등록되었습니다! 📝")
        st.rerun()
    else:
        st.warning("닉네임과 소감을 모두 입력해 주세요!")

st.write("### 📌 친구들이 남긴 소감 한 줄")
for review in st.session_state["reviews"]:
    st.write(f"**👤 {review['이름']}** : {review['소감']}")