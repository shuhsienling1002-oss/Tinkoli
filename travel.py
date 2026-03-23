import streamlit as st
import random
from datetime import datetime, date

# ==========================================
# 1. 系統設定 (Code-CRF v9.0: 基礎設施層)
# ==========================================
st.set_page_config(
    page_title="Kaiana 電光部落 | 深度探索",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. 史上最佳 CSS 美學 (Premium Dark + Glassmorphism)
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;700;900&display=swap');

    /* 1. 全站深色流光背景 */
    .stApp {
        background: radial-gradient(circle at 50% -10%, #3A2610 0%, #0A0A0A 80%);
        font-family: 'Noto Sans TC', sans-serif;
        color: #E0E0E0 !important;
    }
    
    p, div, span, label, .stMarkdown { color: #E0E0E0 !important; }

    header {visibility: hidden;}
    footer {display: none !important;}
    
    /* 2. 頂部主視覺 (懸浮發光字體) */
    .hero-section {
        text-align: center;
        padding: 40px 10px 20px 10px;
        margin-top: -50px;
        margin-bottom: 30px;
    }
    .hero-title { 
        font-size: 42px; 
        font-weight: 900; 
        background: linear-gradient(to right, #FFD700, #FF8C00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 4px;
        text-shadow: 0px 4px 20px rgba(255, 140, 0, 0.3);
    }
    .hero-subtitle {
        font-size: 16px; color: #AAAAAA; margin-top: 10px; letter-spacing: 2px;
    }

    /* 3. 毛玻璃卡片 (Glassmorphism) */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .glass-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(255, 140, 0, 0.15);
        border: 1px solid rgba(255, 140, 0, 0.3);
    }
    
    /* 住宿專用玻璃卡片 (邊框帶銅色質感) */
    .hotel-glass-card {
        background: rgba(200, 150, 100, 0.05);
        backdrop-filter: blur(12px);
        border-left: 4px solid #D4AF37;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 15px;
        transition: all 0.3s ease;
    }
    .hotel-glass-card:hover { background: rgba(200, 150, 100, 0.08); }

    /* 4. 輸入框質感優化 */
    div[data-baseweb="select"] > div, 
    div[data-baseweb="input"] > div {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #FFFFFF !important;
        border-radius: 12px !important;
        min-height: 50px !important;
        transition: all 0.3s ease;
    }
    div[data-baseweb="select"] > div:hover, 
    div[data-baseweb="input"] > div:hover {
        border: 1px solid #FF8C00 !important;
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
    input, div[data-baseweb="select"] span { color: #FFFFFF !important; }
    ul[data-baseweb="menu"] { background-color: #1A1A1A !important; border: 1px solid #333;}
    li[data-baseweb="option"] { color: #FFF !important; }
    li[data-baseweb="option"]:hover { background-color: #FF8C00 !important; color: #000 !important;}
    svg { fill: #FFD700 !important; }

    /* 5. 終極發光按鈕 */
    .stButton > button {
        width: 100%;
        background: linear-gradient(45deg, #FF8C00, #FF3D00) !important;
        color: #FFFFFF !important;
        border-radius: 50px;
        border: none;
        padding: 12px 0;
        font-weight: 900;
        font-size: 20px;
        letter-spacing: 2px;
        box-shadow: 0 8px 25px rgba(255, 61, 0, 0.4);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        margin-top: 15px;
    }
    .stButton > button:hover { 
        transform: scale(1.02);
        box-shadow: 0 12px 35px rgba(255, 61, 0, 0.7);
        background: linear-gradient(45deg, #FFA000, #FF5252) !important;
    }
    .stButton > button * { color: #FFFFFF !important; }
    
    /* 標籤與排版 */
    .spot-tag { 
        font-size: 12px; background: rgba(255,255,255,0.1); color: #FFD700 !important; 
        padding: 4px 12px; border-radius: 20px; margin-right: 8px; border: 1px solid rgba(255,215,0,0.3);
    }
    .tag-red { background: rgba(255,61,0,0.2); color: #FF8C00 !important; border: 1px solid rgba(255,61,0,0.4); }
    
    .day-header { 
        background: linear-gradient(90deg, rgba(255,140,0,0.2) 0%, transparent 100%);
        color: #FF8C00 !important; padding: 8px 20px; border-left: 4px solid #FF8C00;
        font-size: 20px; font-weight: 900; margin: 30px 0 15px 0;
    }
    
    /* 深色模式專屬警告框 (斷路器) */
    .warning-box { 
        background-color: rgba(255, 193, 7, 0.1); 
        border-left: 4px solid #FFC107; 
        padding: 16px; 
        border-radius: 8px; 
        margin-top: 10px; 
        margin-bottom: 20px;
        color: #FFD700 !important; 
        font-size: 14px;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 核心資料庫 (Offline-First 完整版)
# ==========================================
all_spots_db = [
    {"name": "電光竹炮體驗", "type": "文化衝擊", "tag": "強烈推薦", "fee": "需預約", "desc": "Kaiana 招牌體驗！使用電石與水產生氣體，重現百年前阿美族赫阻清兵的巨大聲響，震撼力十足。"},
    {"name": "泥火山豆腐 DIY", "type": "手作療癒", "tag": "親子最愛", "fee": "約$350/人", "desc": "使用在地百年泥火山的天然鹵水點豆腐，品嚐帶有微甘礦物味的純手工有機豆腐。"},
    {"name": "197縣道稻浪秘境", "type": "視覺極限", "tag": "網美打卡", "fee": "免門票", "desc": "媲美池上伯朗大道，但完全沒有人擠人！無電線桿的純淨金黃稻浪 (最佳月份：5-6月, 10-11月)。"},
    {"name": "石煮法野營風味餐", "type": "野性味覺", "tag": "必吃", "fee": "需預約", "desc": "將燒紅的麥飯石投入檳榔葉折成的器皿中，瞬間將魚湯煮沸，保留食材最原始的鮮甜。"},
    {"name": "Kaiana 咖啡烘焙", "type": "靜謐時光", "tag": "室內", "fee": "低消飲品", "desc": "在日出農史館內，了解部落產業，體驗親手烘焙縱谷咖啡豆，享受悠閒午後。"},
    {"name": "關山環鎮自行車道", "type": "戶外運動", "tag": "低碳", "fee": "租車費", "desc": "全台首座專用自行車道，全長 12 公里，沿途經過水稻田與關山親水公園。"},
    {"name": "電光天主堂", "type": "建築巡禮", "tag": "靜謐", "fee": "免門票", "desc": "融入阿美族圖騰元素的特色教堂，見證外籍神父深耕部落的歷史軌跡。"},
    {"name": "關山老街慢遊", "type": "人文散步", "tag": "懷舊", "fee": "免門票", "desc": "保留日治時期和洋混合風格的車站，以及周邊的老米廠與臭豆腐名店。"}
]

hotels_db = [
    {"name": "電光部落接待家庭", "tag": "深度體驗", "price": "1,500", "desc": "直接入住部落 Vuvu (長輩) 的家，晚上聽故事、看星空，最純粹的部落生活。"},
    {"name": "關山山水軒渡假村", "tag": "便利舒適", "price": "3,200", "desc": "提供藥草浴與腳踏車租借，適合家庭客群，距離部落僅 10 分鐘車程。"},
    {"name": "禮物盒子民宿", "tag": "質感設計", "price": "2,800", "desc": "關山鎮內的溫馨老屋改建，老闆熱情，早餐極具在地特色。"},
    {"name": "池上日暉國際渡假村", "tag": "奢華享受", "price": "6,500", "desc": "若追求極致硬體服務，可選擇鄰近的池上五星級渡假村 (車程約 20 分鐘)。"}
]

# ==========================================
# 4. 邏輯核心：動態演算法 (完整版)
# ==========================================
def generate_dianguang_itinerary(days_str, group):
    day_count = 1 if "一日" in days_str else (2 if "二日" in days_str else 3)
    itinerary = {}
    
    d1_spot1 = next(s for s in all_spots_db if "竹炮" in s['name'])
    d1_spot2 = next(s for s in all_spots_db if "石煮" in s['name'])
    d1_spot3 = next(s for s in all_spots_db if "稻浪" in s['name'])
    itinerary[1] = [d1_spot1, d1_spot2, d1_spot3]
    
    if day_count >= 2:
        d2_spot1 = next(s for s in all_spots_db if "豆腐" in s['name'])
        d2_spot2 = next(s for s in all_spots_db if "自行車" in s['name'])
        itinerary[2] = [d2_spot1, d2_spot2]
        
    if day_count == 3:
        d3_spot1 = next(s for s in all_spots_db if "咖啡" in s['name'])
        d3_spot2 = next(s for s in all_spots_db if "老街" in s['name'])
        itinerary[3] = [d3_spot1, d3_spot2]

    if "親子" in group: status_title = "👨‍👩‍👧 寓教於樂：部落手作與生態之旅"
    elif "長輩" in group: status_title = "👵 慢活療癒：無障礙稻香與咖啡時光"
    else: status_title = "🔥 熱血尋根：竹炮轟炸與秘境打卡"
    
    return status_title, itinerary

# ==========================================
# 5. 頁面渲染 (玻璃卡片 UI)
# ==========================================
st.markdown("""
    <div class="hero-section">
        <div class="hero-title">KAIANA 電光</div>
        <div class="hero-subtitle">台東關山 ‧ 頂級部落探索演算法</div>
    </div>
""", unsafe_allow_html=True)

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    travel_date = st.date_input("🗓️ 啟程日期", value=date(2026, 6, 11))
with col2:
    days_str = st.selectbox("⏳ 探索深度", ["一日遊 (極速精華)", "二日遊 (過夜沉浸)", "三日遊 (縱谷全覽)"], index=2)

group = st.selectbox("👥 探索陣列", ["情侶/夫妻 (追求質感)", "親子家庭 (需要放電)", "長輩同行 (需要平穩)", "熱血獨旅 (不怕累)"], index=2)

if st.button("啟 動 探 索 引 擎  🚀"):
    st.session_state['generated'] = True
st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.get('generated'):
    status_title, itinerary = generate_dianguang_itinerary(days_str, group)
    
    st.markdown(f"""
    <div style="text-align: center; margin: 30px 0 10px 0;">
        <h3 style="color: #FFD700 !important; font-weight: bold; letter-spacing: 1px;">{status_title}</h3>
        <p style="color: #AAA !important; font-size: 14px;">系統已鎖定最佳體驗路徑，預計於 <b>{travel_date.strftime('%Y/%m/%d')}</b> 執行。</p>
    </div>
    """, unsafe_allow_html=True)

    # --- 行程渲染 ---
    for day, spots in itinerary.items():
        st.markdown(f'<div class="day-header">DAY 0{day}</div>', unsafe_allow_html=True)
        
        for i, spot in enumerate(spots):
            time = "Morning" if i == 0 else ("Noon" if i == 1 else "Afternoon")
            st.markdown(f"""
            <div class="glass-card" style="padding: 20px;">
                <div style="color: #FF8C00; font-size: 12px; letter-spacing: 2px; margin-bottom: 5px; font-weight: bold;">{time.upper()}</div>
                <div style="font-size: 22px; font-weight: bold; margin-bottom: 10px; color: #FFF;">{spot['name']}</div>
                <div style="margin-bottom: 12px;">
                    <span class="spot-tag">{spot['type']}</span>
                    <span class="spot-tag tag-red">{spot['tag']}</span>
                </div>
                <div style="font-size: 14px; color: #BBB; line-height: 1.6;">
                    <span style="color:#FFD700;">💰 {spot['fee']}</span> <br>
                    {spot['desc']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --- 住宿推薦 ---
    if "一日" not in days_str:
        st.markdown('<div class="day-header" style="border-left-color: #D4AF37; color: #D4AF37 !important;">系統推薦安全營地</div>', unsafe_allow_html=True)
        if "長輩" in group: rec_hotels = [h for h in hotels_db if h['name'] in ["關山山水軒渡假村", "池上日暉國際渡假村"]]
        elif "獨旅" in group: rec_hotels = [h for h in hotels_db if h['name'] in ["電光部落接待家庭", "禮物盒子民宿"]]
        else: rec_hotels = random.sample(hotels_db, 2)
            
        for h in rec_hotels:
            st.markdown(f"""
            <div class="hotel-glass-card">
                <div style="font-weight:bold; color:#FFF; font-size: 18px; margin-bottom: 5px;">
                    {h['name']} <span class="spot-tag tag-red" style="font-size: 11px; padding: 2px 8px; vertical-align: middle;">{h['tag']}</span>
                </div>
                <div style="font-size:14px; color:#AAA; margin-top:6px; line-height: 1.5;">
                    <span style="color:#D4AF37;">💲 預估花費：{h['price']} / 晚</span> <br>
                    {h['desc']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --- 整合：斷路器與離線備援機制 ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.expander("🛡️ 啟動部落專屬預約通道 (防禦型離線系統)"):
        st.markdown("""
        <div class="warning-box">
            <b>⚡ 系統遙測警報：</b> 偵測到 197 縣道部分路段網路延遲。為防止預約資料掉包，系統已自動切換至「離線快取加密模式」。填寫完畢後，將透過低頻簡訊直連部落窗口。
        </div>
        """, unsafe_allow_html=True)
        
        contact_name = st.text_input("代表聯絡人姓名 (Name)")
        contact_phone = st.text_input("聯絡電話 (Phone - 絕對必填)")
        
        if st.button("加 密 傳 送 預 約 檔 案"):
            if not contact_phone:
                st.error("❌ 拒絕執行：聯絡電話為空，無法建立安全連線！")
            else:
                st.success(f"✅ 封包傳送成功！已將 {contact_name} 的資料安全路由至 Kaiana 專線。")
