import streamlit as st
from PIL import Image
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input


st.set_page_config(page_title="ML & NN", layout="wide")
tab1, tab2, tab3, tab4 = st.tabs(["Machine Learning", "Neural Network", "Demo Machine Learning", "Demo Neural Network"])

with open("model/svm_model.pkl", "rb") as file:
    svm_model = pickle.load(file)

with open("model/rf_model.pkl", "rb") as file:
    rf_model = pickle.load(file)

with tab1:
    import streamlit as st

    st.write("ผมได้หาข้อมูลมาจากเว็บ Kaggle ซึ่งเก็บข้อมูลหลายๆ อย่างไว้ ผมได้เลือก  "
    "[Heart Disease Dataset](https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset)")

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

    st.write("เริ่มแรกผมได้ตรวจสอบข้อมูล head and tail ในตารางว่า มีค่า Nan มั้ย ในรูปจะเห็นว่ามีค่า Nan", unsafe_allow_html=True)
    st.image("photo/check_dataset_svm1.png")

    st.write("จากนั้นผมก็มาดูแต่ละ Column มีค่า Null เท่าไหร่ แล้ว Sum ออกมาดูจำนวน", unsafe_allow_html=True)
    st.image("photo/null_sum.png")

    st.write("พอเราได้เห็นจำนวนทั้งหมดของค่า Null ผมเลยได้ทำการจัดการค่าหาย ใช้ ค่ามัธยฐาน (median) เติมค่าในคอลัมน์ 'chol' เพราะอาจมีค่า outlier ได้"
    "แล้วต่อมาได้ทำ ลบแถวที่ยังมี missing values หลังเติมค่าแล้ว และ ลบคอลัมน์ที่มีค่าว่างเกิน 50% ของแถวทั้งหมด", unsafe_allow_html=True)
    st.image("photo/put_data.png")

    st.write("แปลงค่า Target เป็น 0 และ 1 แล้วถ้าค่ามากกว่า 0.5 จะกำหนดเป็น 1 น้อยกว่านั้นเป็น 0", unsafe_allow_html=True)
    st.image("photo/target.png")

    st.write("ผมแยก featrures และ Target "
    "หลังจากนั้นก็ทำการ split ข้อมูลแบ่งเป็น train 80% กับ test 20% โดยให้ random state = 42", unsafe_allow_html=True)
    st.image("photo/spilt.png")

    st.write("หลังจากนั้นผมก็เรียกใช้ model Support Vector Regression โดยเป็นการใช้แนวคิดของ Support Vector Machine กับ Classification "
    "เพราะ เหมาะกับข้อมูลที่แยกกันได้ดีในเชิงเส้น ต่อมาผมก็เรียกใช้ model RandomForest เป็นอัลกอริธึม Machine Learning ที่ใช้ การรวมกันของหลายๆ Decision Trees โดย สร้างหลายๆ Decision Trees"
    " แต่ละต้นไม้เรียนรู้ข้อมูลที่สุ่มมา ทำให้มีความแตกต่างกัน'", unsafe_allow_html=True)
    st.image("photo/Train.png")
    
with tab2:
    st.write("ผมเริ่มหาจากการหาข้อมูลภายใน Kaggle แล้วได้เลือก "
    "dataset ของ [Cats-vs-Dogs](https://www.kaggle.com/datasets/shaunthesheep/microsoft-catsvsdogs-dataset/data)"
    "")
    st.title("เนื้อหาเกี่ยวกับ")
    st.write("เป็นการแยกรูปภาพว่า จะเป็นสัตว์ชนิดไหน 'หมา' หรือ 'แมว' ชุดข้อมูลทั้งหมดรวมกัน20000ภาพ")
    st.title("Features มีดังนี้")
    st.markdown("""
    - **รูปแมว**: 10000รูป
    - **รูปหมา**: 10000รูป
    - **แต่ผมนำมาใช้จริงแค่ 1040 รูป เพราะ ผมกลัวข้อมูลมันจะใหญ่เกินไป 
    """)
    st.image("photo/dog-cat.jpg")
    
    st.write("ผมได้ตรวจสอบว่า dataset มีภาพที่ถูกต้อง ไม่มีไฟล์แปลกปลอม")
    st.image("photo/nn7.png")

    st.write("ต่อมาผมได้ตรวจสอบว่าภาพมีขนาดใกล้เคียงกัน หรือมีภาพที่เสียหายมั้ย")
    st.image("photo/nn6.png")

    st.write("อ่านภาพจากโฟลเดอร์ Cat และ Dog และทำการแยกประเภทของไฟล์ jpg, png, jpeg จำกัดจำนวนรูปภาพ 1040รูป ขนาดรูปภาพ 224x224 และ แปลงป้ายกำกับเป็น 1 (Dog) และ 0 (Cat)", unsafe_allow_html=True)
    st.image("photo/nn1.png")

    st.write("จำกัดจำนวนรูปภาพ 520รูปต่อคลาส และ รวมข้อมูลทั้งหมดเป็นอาร์เรย์ data และ labels", unsafe_allow_html=True)
    st.image("photo/nn2.png")

    st.write("ใช้ ImageDataGenerator เพื่อเพิ่มข้อมูลภาพโดย หมุนภาพสุ่ม ,เลื่อนภาพสุ่ม, ขยาย/ย่อภาพ, พลิกภาพ", unsafe_allow_html=True)
    st.image("photo/nn3.png")

    st.write("โหลดโมเดล MobileNetV2 และกำหนดค่า Fine-Tuning ล็อกเลเยอร์ทั้งหมด ยกเว้น 30 เลเยอร์สุดท้าย จากนั้นสร้างโมเดล"
    "ใช้ GlobalAveragePooling2D ลดขนาดฟีเจอร์แมพ,เพิ่ม Dense Layer ขนาด 128 นิวรอน, ใช้Dropout 0.5 เพื่อป้องกัน Overfitting ใช้ Optimizer Adam(learning_rate=0.00001)", unsafe_allow_html=True)
    st.image("photo/nn4.png")

    st.write("จากนั้นมาฝึกโมเดลโดยใช้ Data Augmentation กำหนด batch_size = 32 และ ใช้ 10 epochs", unsafe_allow_html=True)
    st.image("photo/nn5.png")

with tab3:
      st.title("Demo Machine Learning: Heart Disease Prediction")
      model_choice = st.radio("เลือกโมเดลที่ต้องการใช้", ["SVM", "Random Forest"])

      # รับค่าจากผู้ใช้
      age = st.number_input("อายุ", min_value=20, max_value=100, value=50)
      sex = st.selectbox("เพศ", [("ชาย", 1), ("หญิง", 0)], format_func=lambda x: x[0])[1]
      cp = st.selectbox("อาการเจ็บหน้าอก", [("ไม่มีอาการ", 0), ("เจ็บแบบไม่รุนแรง", 1), ("เจ็บแบบรุนแรง", 2), ("เจ็บมาก", 3)], format_func=lambda x: x[0])[1]
      trestbps = st.number_input("ความดันโลหิตขณะพัก (mm Hg)", min_value=80, max_value=200, value=120)
      chol = st.number_input("ระดับคอเลสเตอรอล (mg/dl)", min_value=100, max_value=400, value=200)
      fbs = st.selectbox("ระดับน้ำตาลในเลือดขณะอดอาหาร", [("ปกติ", 0), ("สูง", 1)], format_func=lambda x: x[0])[1]
      restecg = st.selectbox("ผลตรวจคลื่นไฟฟ้าหัวใจ", [("ปกติ", 0), ("ST-T wave abnormality", 1), ("ventricular hypertrophy", 2)], format_func=lambda x: x[0])[1]
      thalach = st.number_input("อัตราการเต้นของหัวใจสูงสุดที่วัดได้ (bpm)", min_value=50, max_value=220, value=150)
      exang = st.selectbox("มีอาการเจ็บหน้าอกขณะออกกำลังกายหรือไม่", [("ไม่มี", 0), ("มี", 1)], format_func=lambda x: x[0])[1]
      oldpeak = st.number_input("ระดับ ST depression", min_value=0.0, max_value=6.0, value=1.0, step=0.1)
      slope = st.selectbox("ลักษณะของ ST segment slope", [("Upsloping", 0), ("Flat", 1), ("Downsloping", 2)], format_func=lambda x: x[0])[1]
      ca = st.number_input("จำนวนหลอดเลือดที่ตรวจพบด้วยสี", min_value=0, max_value=4, value=1)
      thal = st.selectbox("ประเภทของ Thalassemia", [("ไม่ทราบค่า", 0), ("Fixed defect", 1), ("Normal", 2), ("Reversible defect", 3)], format_func=lambda x: x[0])[1]

      # ปุ่มทำนาย
      if st.button("Prediction"):
          input_features = np.array([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])

          if model_choice == "SVM":
              prediction = svm_model.predict(input_features)[0]
          else:
              prediction = rf_model.predict(input_features)[0]

          if prediction == 1:
            st.error(f"⚠️ มีความเสี่ยงเป็นโรคหัวใจ ({model_choice} Model)")
          else:
            st.success(f"✅ ไม่มีภาวะโรคหัวใจ ({model_choice} Model)")

with tab4:
    st.title("Demo Neural Network")
    st.title("🐶🐱 Cat vs Dog Classifier")
    st.write("<h4 style='text-align: ;'>MobilenetV2</h4>", unsafe_allow_html=True)
    st.image("photo/Graph.png")

    # โหลดโมเดล
    model = tf.keras.models.load_model("model/mobilenetv2_cat_dog.h5")

    # ฟังก์ชันทำนายภาพ
    def predict_image(image):
        img = Image.open(image)  # เปิดภาพจากไฟล์อัพโหลด
        img = img.resize((224, 224))  # Resize ภาพให้ตรงกับโมเดล
        img_array = img_to_array(img)  # แปลงเป็น array
        img_array = preprocess_input(img_array)  # ปรับค่าตาม MobileNetV2
        img_array = np.expand_dims(img_array, axis=0)  # เพิ่มมิติให้ TensorFlow ใช้ได้

        prediction = model.predict(img_array)[0][0]  # ทำนายผล
        return "🐶 Dog" if prediction > 0.5 else "🐱 Cat"

    # อัพโหลดภาพเฉพาะใน tab4
    uploaded_file = st.file_uploader("📤 Upload an image...", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:  # ตรวจสอบว่ามีไฟล์อัพโหลด
        st.image(uploaded_file)
        label = predict_image(uploaded_file)  # ส่งไฟล์ไปให้ฟังก์ชันทำนาย
        st.write(f"### ✅ Prediction: {label}")