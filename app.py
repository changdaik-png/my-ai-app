import streamlit as st

# 1. 제목을 적어줘!
st.title("🎉 나의 첫 파이썬 웹사이트")

# 2. 글씨를 써줘!
st.write("와! HTML 없이 파이썬만으로 화면이 만들어졌어요.")

# 3. 입력칸을 만들어줘!
name = st.text_input("당신의 이름은 무엇인가요?")

# 4. 버튼을 만들고, 눌렀을 때 반응해줘!
if st.button("인사하기"):
    st.write(f"반가워요, {name}님! 파이썬의 세계에 오신 걸 환영합니다! 🎈")
    st.balloons()  # 풍선 날리기 효과!