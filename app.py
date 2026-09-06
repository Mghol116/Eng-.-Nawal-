import base64
import io
import os
import time
from google import genai
from google.genai import types
from PIL import Image
import streamlit as st

# ==========================================
# 1. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="منصة معالم الجوف الذكية", page_icon="🇸🇦", layout="centered"
)

# ==========================================
# 2. تحويل الصورة إلى Base64 وتطبيق الـ CSS
# ==========================================
image_path = "banner.jpg"

if os.path.exists(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    bg_image_style = f"""
    <style>
    /* جعل الصورة خلفية لكامل الصفحة وتوسيط المحتوى داخل الصفحة عمودياً */
    .stApp {{
        background-image: url('data:image/jpeg;base64,{encoded_string}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        display: flex;
        justify-content: center;
        align-items: center;
    }}

    /* ضبط الحاوية الخضراء وتوسيطها في منتصف الشاشة */
    .stMainBlockContainer {{
        background-color: rgba(13, 27, 18, 0.85);
        padding: 2.5rem;
        border-radius: 16px;
        margin-top: auto !important;
        margin-bottom: auto !important;
        backdrop-filter: blur(3px);
        width: 100%;
        max-width: 700px;
    }}

    /* إزالة المسافة الفارغة العلوية التلقائية في Streamlit */
    .stAppHeader {{
        background-color: transparent !important;
    }}
    
    div[data-testid="stHeader"] {{
        height: 0rem;
    }}

    /* ضبط حجم وتنسيق العنوان الرئيسي */
    h1 {{
        font-size: 1.8rem !important;
        color: #e2d1a3 !important;
    }}

    /* ألوان النصوص والتحسينات */
    h2, h3, p, label, .stMarkdown {{
        color: #e2d1a3 !important;
    }}

    /* أزرار الرفع والملفات */
    .stButton>button, div[data-testid="stFileUploader"] {{
        background-color: #1b3824 !important;
        border: 1px solid #c5a059 !important;
        color: #ffffff !important;
        border-radius: 8px;
    }}
    </style>
    """
    st.markdown(bg_image_style, unsafe_allow_html=True)

# ==========================================
# 3. قراءة المفتاح بمرونة (محلي + سحابي)
# ==========================================
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    API_KEY = "AIzaSyA9MCj4YVLYX5RovL8K_a3xLTXVSRgJisM"

# ==========================================
# 4. الواجهة الرئيسية
# ==========================================
st.title("🇸🇦 منصة معالم الجوف الذكية - اليوم الوطني 96")
st.write("أهلاً بك يا بعد حيي! قم بإرفاق صورة لأحد معالم السعودية")

uploaded_file = st.file_uploader(
    "اختر صورة معلم تاريخي ...", type=["jpg", "png", "jpeg"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="الصورة المرفوعة للموقع", use_container_width=True)

    with st.spinner(
        "جاري معالجة الصورة عبر خوارزميات الرؤية الحاسوبية والذكاء الاصطناعي..."
    ):
        try:
            img_byte_arr = io.BytesIO()
            image_format = image.format if image.format else "JPEG"
            image.save(img_byte_arr, format=image_format)
            img_bytes = img_byte_arr.getvalue()

            mime_type = f"image/{image_format.lower()}"
            if image_format.lower() == "jpg":
                mime_type = "image/jpeg"

            image_part = types.Part.from_bytes(
                data=img_bytes, mime_type=mime_type
            )

            client = genai.Client(api_key=API_KEY)

            prompt = """
            أنت خبير تراث وتاريخ لمنطقة الجوف بالمملكة العربية السعودية.
            قم بتحليل هذه الصورة وتعرف على المعلم الموجود فيها تلقائياً (مثل قصر مارد، قلعة زعبل، أعمدة الرجاجيل، بئر سيسرا، حي الدرع).
            قدّم تقريراً مستنسخاً باللغة العربية بالتنسيق التالي بدقة:
            
            📍 **التقرير التاريخي للمعلم:**
            * **اسم المعلم:** [اسم المعلم]
            * **الموقع:** [الموقع في الجوف]
            * **نبذة تاريخية:** [شرح مختصر وتاريخي عن المعلم]
            * **دور التقنية:** تم تحليله وتوثيقه عبر نظام ذكاء اصطناعي وطني لدعم السياحة والتراث.
            """

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=[image_part, prompt],
            )

            st.success("تم التعرف على المعلم بنجاح! 🎉")
            st.markdown(response.text)

        except Exception as e:
            st.error(f"حدث خطأ أثناء تحليل الصورة: {e}")

st.markdown("---")
st.markdown("إعداد الطالبة: نوال سمير الشمروخي")
