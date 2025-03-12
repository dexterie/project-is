import streamlit as st

st.set_page_config(page_title="ML & NN Demo", layout="wide")

tab1, tab2, tab3, tab4 = st.tabs(["Machine Learning", "Neural Network", "Demo Machine Learning", "Demo Neural Network"])

with tab1:
    st.write("ผมได้หาข้อมูลมาจากเว็บ Kaggle ซึ่งเก็บข้อมูลหลายๆ อย่างไว้ ผมได้เลือก Dataset ของ Heart Disease")
    st.title("เนื้อหาเกี่ยวกับ")
    st.write("โรคหัวใจ โดยใช้คุณลักษณะทางกายภาพ และผลตรวจสุขภาพของบุคคล วิเคราะห์ปัจจัยเสี่ยงจากโรคหัวใจ ได้แก่ "
             "เช่น อายุ, เพศ, ระดับคอเลสเตอรอล, ความดันโลหิต, อัตราการเต้นของหัวใจ")
    
    st.title("Features มีดังนี้")
    st.markdown("""
    - **age**: อายุของบุคคล
    - **sex**: เพศ (1 = ชาย, 0 = หญิง)
    - **cp**: ประเภทของอาการเจ็บหน้าอก (ค่าตั้งแต่ 0 ถึง 3)
      - 0: ไม่มีอาการ
      - 1: เจ็บแบบไม่รุนแรง
      - 2: เจ็บแบบรุนแรง
      - 3: เจ็บมาก
    - **trestbps**: ความดันโลหิตขณะพัก (mm Hg)
    - **chol**: ระดับคอเลสเตอรอลในเลือด (mg/dl)
    - **fbs**: ระดับน้ำตาลในเลือดขณะอดอาหาร (>120 mg/dl)
      - 0 = ปกติ
      - 1 = สูง
    - **restecg**: ผลตรวจคลื่นไฟฟ้าหัวใจ (ECG)
      - 0: ปกติ
      - 1: มี ST-T wave abnormality
      - 2: แสดงภาวะ ventricular hypertrophy
    - **thalach**: อัตราการเต้นของหัวใจสูงสุดที่วัดได้ (bpm)
    - **exang**: มีอาการเจ็บหน้าอกขณะออกกำลังกายหรือไม่
      - 0 = ไม่มี
      - 1 = มี
    - **oldpeak**: ระดับ ST depression (ค่าลดลงของ ST segment ใน ECG)
    - **slope**: ลักษณะของ ST segment slope
      - 0: Upsloping
      - 1: Flat
      - 2: Downsloping
    - **ca**: จำนวนหลอดเลือดที่ตรวจพบด้วยสี (ค่าตั้งแต่ 0 ถึง 4)
    - **thal**: ประเภทของ Thalassemia
      - 0: ไม่ทราบค่า
      - 1: Fixed defect (ความผิดปกติถาวร)
      - 2: Normal (ปกติ)
      - 3: Reversible defect (ความผิดปกติที่กลับมาเป็นปกติได้)
    """)

    st.title("Target")
    st.markdown("""
    - **target**: มีภาวะโรคหัวใจหรือไม่
      - 0 = ปกติ (ไม่มีโรคหัวใจ)
      - 1 = เป็นโรคหัวใจ
    """)

with tab2:
    st.title("Neural Network Model")
    st.write("หน้านี้ใช้สำหรับทำนายข้อมูลด้วย Neural Network")

with tab3:
    st.title("Demo Machine Learning")
    st.write("หน้านี้ใช้สำหรับเดโมการทำงานของ Machine Learning Model")

with tab4:
    st.title("Demo Neural Network")
    st.write("หน้านี้ใช้สำหรับเดโมการทำงานของ Neural Network Model")
