import streamlit as st
import time
import random
from io import BytesIO

# --- 1. 核心相容性修復 ---
def safe_rerun():
    """自動判斷並執行重整"""
    try:
        st.rerun()
    except AttributeError:
        try:
            st.experimental_rerun()
        except:
            st.stop()

def safe_play_audio(text):
    """語音播放安全模式"""
    try:
        from gtts import gTTS
        # 使用印尼語 (id) 發音
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')
    except Exception as e:
        st.caption(f"🔇 (語音生成暫時無法使用)")

# --- 0. 系統配置 ---
st.set_page_config(page_title="Unit 20: O Sapikalic", page_icon="🚦", layout="centered")

# --- CSS 美化 (都會灰藍色調) ---
st.markdown("""
    <style>
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .source-tag { font-size: 12px; color: #aaa; text-align: right; font-style: italic; }
    
    /* 單字卡 */
    .word-card {
        background: linear-gradient(135deg, #ECEFF1 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
        border-bottom: 4px solid #546E7A;
    }
    .emoji-icon { font-size: 48px; margin-bottom: 10px; }
    .amis-text { font-size: 22px; font-weight: bold; color: #37474F; }
    .chinese-text { font-size: 16px; color: #7f8c8d; }
    
    /* 句子框 */
    .sentence-box {
        background-color: #ECEFF1;
        border-left: 5px solid #90A4AE;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }

    /* 按鈕 */
    .stButton>button {
        width: 100%; border-radius: 12px; font-size: 20px; font-weight: 600;
        background-color: #CFD8DC; color: #37474F; border: 2px solid #546E7A; padding: 12px;
    }
    .stButton>button:hover { background-color: #B0BEC5; border-color: #455A64; }
    .stProgress > div > div > div > div { background-color: #546E7A; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 資料庫 (Unit 20: User Fix) ---
vocab_data = [
    {"amis": "O Sapikalic", "chi": "交通工具 (用來乘坐的)", "icon": "🚗", "source": "User Fix"},
    {"amis": "Cinamalay", "chi": "火車", "icon": "🚂", "source": "User Fix"},
    {"amis": "Tosiya", "chi": "汽車", "icon": "🚘", "source": "Moedict: tosiya"},
    {"amis": "Tofay", "chi": "機車", "icon": "🛵", "source": "User Fix"},
    {"amis": "Hikoki", "chi": "飛機", "icon": "✈️", "source": "Moedict: hikoki"},
    {"amis": "Tamina", "chi": "船", "icon": "🚢", "source": "Moedict: tamina"},
    {"amis": "Lalan", "chi": "道路 / 路", "icon": "🛣️", "source": "Moedict: lalan"},
    {"amis": "Parakat", "chi": "駕駛 / 開車", "icon": "☸️", "source": "Moedict: parakat"},
    {"amis": "Mikalic", "chi": "乘坐 / 搭乘 / 登車", "icon": "💺", "source": "User Fix"},
    {"amis": "Paso", "chi": "公車 / 巴士", "icon": "🚌", "source": "User Fix"}, # 修正 Baso -> Paso
]

sentences = [
    {"amis": "Mikalic kako to paso.", "chi": "我搭公車。", "icon": "🚌", "source": "User Fix: Paso"}, # 修正
    {"amis": "Parakat ci mama to tosiya.", "chi": "爸爸開車。", "icon": "🚘", "source": "Pa-rakat (Drive)"},
    {"amis": "Mikalic to cinamalay a tayra i Posong.", "chi": "搭火車去台東。", "icon": "🚂", "source": "User Fix: Cinamalay"},
    {"amis": "Mikalic to tofay.", "chi": "騎機車。", "icon": "🛵", "source": "User Fix: Tofay"},
    {"amis": "Fangcal ko lalan.", "chi": "路很漂亮(好)。", "icon": "🛣️", "source": "Grammar: Fangcal"},
]

# --- 3. 隨機題庫 (User Fix Verified) ---
raw_quiz_pool = [
    {
        "q": "Mikalic kako to paso.",
        "audio": "Mikalic kako to paso",
        "options": ["我搭公車", "我開公車", "我看公車"],
        "ans": "我搭公車",
        "hint": "Mikalic 是乘坐/登車"
    },
    {
        "q": "Parakat ci mama to tosiya.",
        "audio": "Parakat ci mama to tosiya",
        "options": ["爸爸開車", "爸爸修車", "爸爸買車"],
        "ans": "爸爸開車",
        "hint": "Parakat 是駕駛"
    },
    {
        "q": "Mikalic to cinamalay.",
        "audio": "Mikalic to cinamalay",
        "options": ["搭火車", "搭飛機", "搭船"],
        "ans": "搭火車",
        "hint": "Cinamalay 是火車"
    },
    {
        "q": "單字測驗：Hikoki",
        "audio": "Hikoki",
        "options": ["飛機", "汽車", "機車"],
        "ans": "飛機",
        "hint": "在天上飛的"
    },
    {
        "q": "單字測驗：Tamina",
        "audio": "Tamina",
        "options": ["船", "車", "路"],
        "ans": "船",
        "hint": "在水上的交通工具"
    },
    {
        "q": "單字測驗：Tofay",
        "audio": "Tofay",
        "options": ["機車", "腳踏車", "汽車"],
        "ans": "機車",
        "hint": "兩個輪子的"
    },
    {
        "q": "「道路」的阿美語怎麼說？",
        "audio": None,
        "options": ["Lalan", "Omah", "Loma'"],
        "ans": "Lalan",
        "hint": "人走的 Lalan"
    },
    {
        "q": "單字測驗：Sapikalic",
        "audio": "Sapikalic",
        "options": ["交通工具 (乘坐用)", "房子", "衣服"],
        "ans": "交通工具 (乘坐用)",
        "hint": "用來 Mikalic 的東西"
    }
]

# --- 4. 狀態初始化 (洗牌邏輯) ---
if 'init' not in st.session_state:
    st.session_state.score = 0
    st.session_state.current_q_idx = 0
    st.session_state.quiz_id = str(random.randint(1000, 9999))
    
    # 抽題與洗牌
    selected_questions = random.sample(raw_quiz_pool, 3)
    final_questions = []
    for q in selected_questions:
        q_copy = q.copy()
        shuffled_opts = random.sample(q['options'], len(q['options']))
        q_copy['shuffled_options'] = shuffled_opts
        final_questions.append(q_copy)
        
    st.session_state.quiz_questions = final_questions
    st.session_state.init = True

# --- 5. 主介面 ---
st.markdown("<h1 style='text-align: center; color: #37474F;'>Unit 20: O Sapikalic</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>交通工具 (Paso Corrected)</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📚 詞彙與句型", "🎲 隨機挑戰"])

# === Tab 1: 學習模式 ===
with tab1:
    st.subheader("📝 核心單字")
    col1, col2 = st.columns(2)
    for i, word in enumerate(vocab_data):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="word-card">
                <div class="emoji-icon">{word['icon']}</div>
                <div class="amis-text">{word['amis']}</div>
                <div class="chinese-text">{word['chi']}</div>
                <div class="source-tag">src: {word['source']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔊 聽發音", key=f"btn_vocab_{i}"):
                safe_play_audio(word['amis'])

    st.markdown("---")
    st.subheader("🗣️ 實用句型")
    for i, s in enumerate(sentences):
        st.markdown(f"""
        <div class="sentence-box">
            <div style="font-size: 20px; font-weight: bold; color: #37474F;">{s['icon']} {s['amis']}</div>
            <div style="font-size: 16px; color: #555; margin-top: 5px;">{s['chi']}</div>
            <div class="source-tag">src: {s['source']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"▶️ 播放句型", key=f"btn_sent_{i}"):
            safe_play_audio(s['amis'])

# === Tab 2: 隨機挑戰模式 ===
with tab2:
    st.markdown("### 🎲 隨機評量")
    
    if st.session_state.current_q_idx < len(st.session_state.quiz_questions):
        q_data = st.session_state.quiz_questions[st.session_state.current_q_idx]
        
        st.progress((st.session_state.current_q_idx) / 3)
        st.markdown(f"**Question {st.session_state.current_q_idx + 1} / 3**")
        
        st.markdown(f"### {q_data['q']}")
        if q_data['audio']:
            if st.button("🎧 播放題目音檔", key=f"btn_audio_{st.session_state.current_q_idx}"):
                safe_play_audio(q_data['audio'])
        
        # 使用洗牌後的選項
        unique_key = f"q_{st.session_state.quiz_id}_{st.session_state.current_q_idx}"
        user_choice = st.radio("請選擇正確答案：", q_data['shuffled_options'], key=unique_key)
        
        if st.button("送出答案", key=f"btn_submit_{st.session_state.current_q_idx}"):
            if user_choice == q_data['ans']:
                st.balloons()
                st.success("🎉 答對了！")
                time.sleep(1)
                st.session_state.score += 100
                st.session_state.current_q_idx += 1
                safe_rerun()
            else:
                st.error(f"不對喔！提示：{q_data['hint']}")
                
    else:
        st.progress(1.0)
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; background-color: #CFD8DC; border-radius: 20px; margin-top: 20px;'>
            <h1 style='color: #37474F;'>🏆 挑戰成功！</h1>
            <h3 style='color: #333;'>本次得分：{st.session_state.score}</h3>
            <p>你已經學會怎麼搭車了！</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 再來一局 (重新抽題)", key="btn_restart"):
            st.session_state.score = 0
            st.session_state.current_q_idx = 0
            st.session_state.quiz_id = str(random.randint(1000, 9999))
            
            new_questions = random.sample(raw_quiz_pool, 3)
            final_qs = []
            for q in new_questions:
                q_copy = q.copy()
                shuffled_opts = random.sample(q['options'], len(q['options']))
                q_copy['shuffled_options'] = shuffled_opts
                final_qs.append(q_copy)
            
            st.session_state.quiz_questions = final_qs
            safe_rerun()

