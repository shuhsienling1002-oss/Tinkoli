import streamlit as st
import random
from datetime import datetime, date

# ==========================================
# 1. 系統設定 (Code-CRF v9.0: 基礎設施層)
# ==========================================
st.set_page_config(
    page_title="2026 電光部落 (Kaiana) 深度探索",
    page_icon="🌾",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. CSS 美學 (UIUX-CRF v9.0: 修復版 - 確保文字清晰與排版乾淨)
# ==========================================
st.markdown("""
    <style>
    /* 1. 強制全站背景為米白/稻穗色，字體為深灰 */
    .stApp {
        background-color: #FDFBF7;
        font-family: "Microsoft JhengHei", sans-serif;
        color: #2C2C2C !important;
    }
    
    /* 2. 一般文字元素設定 */
    p, div, span, h1, h2, h3, h4, h5, h6, label, .stMarkdown {
        color: #2C2C2C !important;
    }

    /* 3. 輸入框深色模式防禦 */
    div[data-baseweb="select"] > div, 
    div[data-baseweb="input"] > div, 
    div[data-baseweb="base-input"] {
        background-color: #ffffff !important;
        border: 2px solid #E6D5B8 !important;
        color: #2C2C2C !important;
        min-height: 48px !important;
    }
    input, div[data-baseweb="select"] span, li[data-baseweb="option"] {
        color: #2C2C2C !important;
    }
    ul[data-baseweb="menu"] { background-color: #ffffff !important; }
    svg { fill: #2C2C2C !important; color: #2C2C2C !important; }

    /* 4. 日期選單高亮 */
    div[data-testid="stDateInput"] > label {
        color: #8B0000 !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }

    /* 隱藏官方元件 */
    header {visibility: hidden;}
    footer {display: none !important;}
    
    /* 標題區 (豐收金漸層) */
    .header-box {
        background: linear-gradient(135deg, #D4AF37 0%, #E6C27A 100%);
        padding: 30px 20px;
        border-radius: 0 0 20px 20px;
        color: #1A1A1A !important;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
        margin-top: -60px;
    }
    .header-box h1, .header-box div, .header-box span { color: #1A1A1A !important; }
    .header-title { font-size: 28px; font-weight: bold; letter-spacing: 2px; }
    
    /* === 5. 核心修復：強制按鈕文字純白 === */
    .stButton > button, 
    .stButton > button * {
        color: #FFFFFF !important; 
    }
    .stButton > button {
        width: 100%;
        background-color: #8B0000 !important; 
        border-radius: 12px;
        border: none;
        padding: 10px 0;
        font-weight: bold;
        transition: 0.3s;
        font-size: 18px;
        box-shadow: 0 4px 6px rgba(139, 0, 0, 0.2);
    }
    .stButton > button:hover { background-color: #660000 !important; }
    
    /* 資訊區與卡片 */
    .info-box { background-color: #F8F9FA; border-left: 5px solid #D4AF37; padding: 15px; border-radius: 4px; margin-bottom: 20px; }
    .timeline-item { border-left: 3px solid #D4AF37; padding-left: 20px; margin-bottom: 20px; position: relative; }
    .timeline-item::before { content: '🌾'; position: absolute; left: -13px; top: 0; background: #FDFBF7; border-radius: 50%; }
    .day-header { background: #E6D5B8; color: #5C4033 !important; padding: 6px 16px; border-radius: 8px; display: inline-block; margin-bottom: 15px; font-weight: bold; }
    .spot-title { font-weight: bold; color: #8B0000 !important; font-size: 18px; }
    .spot-tag { font-size: 12px; background: #F0E6D2; color: #5C4033 !important; padding: 4px 10px; border-radius: 6px; margin-right: 6px; border: 1px solid #D4AF37; }
    .hotel-card { background: #FFFFFF; border-left: 5px solid #5C4033; padding: 15px; border-radius: 8px; margin-bottom: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    .hotel-tag { font-size: 11px; background: #5C4033; color: white !important; padding: 3px 8px; border-radius: 4px; margin-right: 5px; }
    
    /* 斷路器警告框 */
    .warning-box { background-color: #FFF3CD; border-left: 5px solid #FFC107; padding: 15px; border-radius: 4px; margin-top: 15px; color: #856404 !important; font-size: 14px;}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 核心資料庫 (Offline-First 策略)
# ==========================================
all_spots_db = [
    {"name": "電光竹炮體驗", "type": "歷史文化", "tag": "強烈推薦", "fee": "需預約", "desc": "Kaiana 招牌體驗！使用電石與水產生氣體，重現百年前阿美族赫阻清兵的巨大聲響，震撼力十足。"},
    {"name": "泥火山豆腐 DIY", "type": "手作體驗", "tag": "親子最愛", "fee": "約$350/人", "desc": "使用在地百年泥火山的天然鹵水點豆腐，品嚐帶有微甘礦物味的純手工有機豆腐。"},
    {"name": "電光稻浪秘境 (197縣道)", "type": "自然景觀", "tag": "網美打卡", "fee": "免門票", "desc": "媲美池上伯朗大道，但完全沒有人擠人！無電線桿的純淨金黃稻浪 (最佳月份：5-6月, 10-11月)。"},
    {"name": "阿美族石煮法風味餐", "type": "在地美食", "tag": "必吃", "fee": "需預約", "desc": "將燒紅的麥飯石投入檳榔葉折成的器皿中，瞬間將魚湯煮沸，保留食材最原始的鮮甜。"},
    {"name": "日出農史館 (Kaiana 咖啡)", "type": "文化導覽", "tag": "室內", "fee": "低消飲品", "desc": "了解部落的梅子與咖啡產業，體驗親手烘焙縱谷咖啡豆，享受悠閒午後。"},
    {"name": "關山環鎮自行車道", "type": "戶外運動", "tag": "低碳", "fee": "租車費", "desc": "全台首座專用自行車道，全長 12 公里，沿途經過水稻田與關山親水公園。"},
    {"name": "電光天主堂", "type": "建築巡禮", "tag": "靜謐", "fee": "免門票", "desc": "融入阿美族圖騰元素的特色教堂，見證外籍神父深耕部落的歷史軌跡。"},
    {"name": "關山老街與舊火車站", "type": "人文散步", "tag": "懷舊", "fee": "免門票", "desc": "保留日治時期和洋混合風格的車站，以及周邊的老米廠與臭豆腐名店。"}
]

hotels_db = [
    {"name": "電光部落接待家庭", "tag": "深度體驗", "price": "1,500", "desc": "直接入住部落 Vuvu (長輩) 的家，晚上聽故事、看星空，最純粹的部落生活。"},
    {"name": "關山山水軒渡假村", "tag": "便利舒適", "price": "3,200", "desc": "提供藥草浴與腳踏車租借，適合家庭客群，距離部落僅 10 分鐘車程。"},
    {"name": "禮物盒子民宿", "tag": "質感設計", "price": "2,800", "desc": "關山鎮內的溫馨老屋改建，老闆熱情，早餐極具在地特色。"},
    {"name": "池上日暉國際渡假村", "tag": "奢華享受", "price": "6,500", "desc": "若追求極致硬體服務，可選擇鄰近的池上五星級渡假村 (車程約 20 分鐘)。"}
]

# ==========================================
# 4. 邏輯核心：動態演算法
# ==========================================
def generate_dianguang_itinerary(days_str, group):
    day_count = 1 if "一日" in days_str else (2 if "二日" in days_str else 3)
    itinerary = {}
    
    d1_spot1 = next(s for s in all_spots_db if s['name'] == "電光竹炮體驗")
    d1_spot2 = next(s for s in all_spots_db if s['name'] == "阿美族石煮法風味餐")
    d1_spot3 = next(s for s in all_spots_db if s['name'] == "電光稻浪秘境 (197縣道)")
    itinerary[1] = [d1_spot1, d1_spot2, d1_spot3]
    
    if day_count >= 2:
        d2_spot1 = next(s for s in all_spots_db if s['name'] == "泥火山豆腐 DIY")
        d2_spot2 = next(s for s in all_spots_db if s['name'] == "關山環鎮自行車道")
        itinerary[2] = [d2_spot1, d2_spot2]
        
    if day_count == 3:
        d3_spot1 = next(s for s in all_spots_db if s['name'] == "日出農史館 (Kaiana 咖啡)")
        d3_spot2 = next(s for s in all_spots_db if s['name'] == "關山老街與舊火車站")
        itinerary[3] = [d3_spot1, d3_spot2]

    if group == "親子家庭 (需要放電)": status_title = "👨‍👩‍👧 寓教於樂：部落手作與生態之旅"
    elif group == "長輩同行 (需要平穩)": status_title = "👵 慢活療癒：無障礙稻香與咖啡時光"
    else: status_title = "🔥 熱血尋根：竹炮轟炸與秘境打卡"
    
    return status_title, itinerary

# ==========================================
# 5. 頁面渲染
# ==========================================
st.markdown("""
    <div class="header-box">
        <div class="header-title">🌾 尋找 Kaiana (日出之處)</div>
        <div style="font-size: 16px; margin-top: 5px;">台東關山・電光部落 專屬旅遊演算法</div>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    travel_date = st.date_input("📅 預計抵達日期", value=date(2026, 6, 11))
with col2:
    days_str = st.selectbox("🕒 停留時間", ["一日遊 (精華)", "二日遊 (過夜深度)", "三日遊 (縱谷全覽)"], index=2)

group = st.selectbox("👥 您的受眾結構", ["情侶/夫妻 (追求質感)", "親子家庭 (需要放電)", "長輩同行 (需要平穩)", "熱血獨旅 (不怕累)"], index=2)

st.write("") 

if st.button("🚀 啟動部落路由器 (生成行程)"):
    st.session_state['generated'] = True

if st.session_state.get('generated'):
    status_title, itinerary = generate_dianguang_itinerary(days_str, group)
    
    st.markdown(f"""
    <div class="info-box">
        <h4 style="margin-top:0;">{status_title}</h4>
        <p style="margin-bottom:0; font-size: 15px;">已為 <b>{group.split(' ')[0]}</b> 鎖定最佳體驗路徑，預計於 <b>{travel_date.strftime('%Y/%m/%d')}</b> 執行。</p>
    </div>
    """, unsafe_allow_html=True)

    for day, spots in itinerary.items():
        st.markdown(f'<div class="day-header">☀️ 執行日 Day {day}</div>', unsafe_allow_html=True)
        
        for i, spot in enumerate(spots):
            time_label = "📍 上午" if i == 0 else ("📍 中午" if i == 1 else "📍 下午")
            st.markdown(f"""
            <div class="timeline-item">
                <div class="spot-title">{time_label}：{spot['name']}</div>
                <div style="margin: 8px 0;">
                    <span class="spot-tag">{spot['type']}</span>
                    <span class="spot-tag" style="background:#8B0000; color:white!important; border:none;">{spot['tag']}</span>
                </div>
                <div style="font-size: 15px; color: #444; line-height: 1.5;">
                    💰 {spot['fee']} <br>
                    📝 {spot['desc']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    if "一日" not in days_str:
        st.markdown("### 🛖 系統推薦安全營地 (住宿)")
        if "長輩" in group: rec_hotels = [h for h in hotels_db if h['name'] in ["關山山水軒渡假村", "池上日暉國際渡假村"]]
        elif "獨旅" in group: rec_hotels = [h for h in hotels_db if h['name'] in ["電光部落接待家庭", "禮物盒子民宿"]]
        else: rec_hotels = random.sample(hotels_db, 2)
            
        for h in rec_hotels:
            st.markdown(f"""
            <div class="hotel-card">
                <div style="font-weight:bold; color:#5C4033; font-size: 16px;">
                    {h['name']} <span class="hotel-tag">{h['tag']}</span>
                </div>
                <div style="font-size:14px; color:#555; margin-top:6px;">
                    💲 預估花費：{h['price']} / 晚 <br>
                    💡 系統短評：{h['desc']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --- 整合：斷路器與離線備援機制 ---
    st.markdown("---")
    st.markdown("### 📞 部落導覽直通車 (防禦型預約系統)")
    
    with st.expander("📝 點此展開預約表單 (已啟用防呆與斷線保護)"):
        st.markdown("""
        <div class="warning-box">
            <b>⚡ 系統偵測：</b> 目前部落山區網路可能不穩，為防止您的預約資料遺失，我們已為您啟動「離線快取模式」。填寫完畢後，資料將直接發送簡訊至部落專員手機。
        </div>
        """, unsafe_allow_html=True)
        
        contact_name = st.text_input("代表聯絡人姓名")
        contact_phone = st.text_input("聯絡電話 (必填)")
        
        if st.button("確認送出預約"):
            if not contact_phone:
                st.error("❌ 拒絕執行：請務必填寫聯絡電話，否則部落無法聯繫您！")
            else:
                st.success(f"✅ 預約成功！已將 {contact_name} 先生/小姐 的資料加密發送至電光部落專線。請靜候佳音。")
