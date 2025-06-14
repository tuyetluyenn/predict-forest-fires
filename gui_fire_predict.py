import streamlit as st
import pandas as pd
import joblib

# Cấu hình reset mặc định
default_values = {
    "month": 1,
    "FFMC": 0.0,
    "DMC": 0.0,
    "DC": 0.0,
    "ISI": 0.0,
    "temperature": 0.0,
    "RH": 0.0,
    "wind": 0.0,
    "rain": 0.0,
    "region": 1,
}

# Reset form nếu nhấn nút Xóa
if "reset" not in st.session_state:
    st.session_state.reset = False

if st.session_state.reset:
    for key, val in default_values.items():
        st.session_state[key] = val
    st.session_state.reset = False  # reset lại trạng thái

st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1615092296061-e2ccfeb2f3d6?q=80&w=2070&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    .block-container {
        background-color: rgba(0, 0, 0, 0) !important;
    }
    div[data-testid="stVerticalBlock"] {
        background-color: white;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .stTextInput > div > input,
    .stNumberInput > div > input,
    .stTextArea > div > textarea {
        color: black; /* chuyển lại màu chữ cho dễ đọc */
    }
    .stButton button {
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        border: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🔥 Dự đoán nguy cơ cháy rừng")

if "result_msg" in st.session_state and st.session_state.result_msg:
    st.markdown(
        f"<div style='text-align:center; font-size:20px; font-weight:bold; margin-bottom:20px;'>{st.session_state.result_msg}</div>",
        unsafe_allow_html=True
    )

col1, col2 = st.columns(2)

with col1:
    month = st.number_input("Tháng", 1, 12, key="month")
    FFMC = st.number_input("FFMC (Fine Fuel Moisture Code)", key="FFMC", min_value=0.0, help="Chỉ số độ ẩm của lớp cỏ khô, lá khô trên bề mặt. Giá trị càng cao cho thấy vật liệu dễ bén lửa hơn.")
    DMC = st.number_input("DMC (Duff Moisture Code)", key="DMC", min_value=0.0, help="Phản ánh độ khô của lớp hữu cơ nằm dưới lớp mặt đất. Chỉ số cao thể hiện khả năng cháy âm ỉ mạnh và lan rộng.")
    DC = st.number_input("DC (Drought Code)", key="DC", min_value=0.0, help="Chỉ số hạn hán, dại diện cho độ khô hạn sâu trong đất. Giá trị cao đồng nghĩa với nguy cơ cháy kéo dài và khó kiểm soát.")
    ISI = st.number_input("ISI (Initial Spread Index)", key="ISI", min_value=0.0, help="Chỉ số đánh giá tốc độ lan truyền ban đầu của đám cháy. Chỉ số càng cao, nguy cơ cháy lan nhanh càng lớn.")

with col2:
    temperature = st.number_input("Nhiệt độ (°C)", key="temperature", min_value=0.0)
    RH = st.number_input("Độ ẩm tương đối (%)", key="RH", min_value=0.0)
    wind = st.number_input("Tốc độ gió (km/h)", key="wind", min_value=0.0)
    rain = st.number_input("Lượng mưa (mm)", key="rain", min_value=0.0)
    region = st.selectbox(
        "Khu vực",
        options=[1, 2, 3],
        format_func=lambda x: {1: "Montesinho – Bồ Đào Nha", 2: "Bejaia – Algeria", 3: "Sidi Bel-Abbes – Algeria"}[x],
        key="region"
    )

# Nút dự đoán và nút xóa
col_btn1, col_btn2 = st.columns([1, 1])

with col_btn1:
    predict_btn = st.button("Dự đoán", use_container_width=True)

with col_btn2:
    clear_btn = st.button("Xóa", use_container_width=True)

# Xử lý sự kiện
if predict_btn:
    model = joblib.load("rf_model.pkl")
    df = pd.DataFrame([[st.session_state.month, st.session_state.FFMC, st.session_state.DMC,
                        st.session_state.DC, st.session_state.ISI, st.session_state.temperature,
                        st.session_state.RH, st.session_state.wind, st.session_state.rain,
                        st.session_state.region]],
                      columns=['month', 'FFMC', 'DMC', 'DC', 'ISI', 'temperature', 'RH', 'wind', 'rain', 'region'])

    result = model.predict(df)[0]
    if result == 1:
        st.session_state.result_msg = "<span style='color:red'>🔥 CẢNH BÁO: CÓ NGUY CƠ CHÁY RỪNG!</span>"
    else:
        st.session_state.result_msg = "<span style='color:green'>✅ KHÔNG có nguy cơ cháy rừng</span>"

    st.rerun() 

if clear_btn:
    st.session_state.reset = True
    st.session_state.result_msg = "" 
    st.rerun()  
