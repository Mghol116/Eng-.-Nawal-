import io
import time
from google import genai
from google.genai import types
from PIL import Image
import streamlit as st

# ==========================================
# مفتاح الـ API الخاص بكِ
API_KEY = "AIzaSyA9MCj4YVLYX5RovL8K_a3xLTXVSRgJisM"
# ==========================================

st.set_page_config(
    page_title="منصة معالم الجوف الذكية", page_icon="🇸🇦", layout="centered"
)

st.title("🇸🇦 منصة معالم الجوف الذكية - اليوم الوطني 96")
st.write(
    "مرحباً بكِ في مشروعكِ الابتكاري! ارفعي صورة لأحد معالم الجوف وسيقوم"
    " الذكاء الاصطناعي بتحليلها والتعرف عليها تلقائياً."
)

uploaded_file = st.file_uploader(
    "اختر صورة معلم تاريخي في الجوف...", type=["jpg", "png", "jpeg"]
)

if uploaded_file is not None:
    # فتح الصورة وعرضها
    image = Image.open(uploaded_file)
    st.image(
        image, caption="الصورة المرفوعة للموقع", use_container_width=True
    )

    with st.spinner(
        "جاري معالجة الصورة عبر خوارزميات الرؤية الحاسوبية والذكاء"
        " الاصطناعي..."
    ):
        try:
            # تحويل الصورة إلى Bytes لمنع أخطاء الترميز (ASCII)
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

            # إنشاء العميل
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

            # استخدام النموذج المحدث والمطلوب
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