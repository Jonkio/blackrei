import streamlit as st
import pandas as pd

st.set_page_config(page_title="IA AVIATOR - CRASH ANALYZER", layout="wide")

st.markdown("""
<style>
    .main { background-color: #020617; color: #f8fafc; }
    .stButton>button { width: 100%; border-radius: 12px; height: 50px; font-weight: bold; }
    .metric-card { padding: 15px; border-radius: 12px; text-align: center; background: #1e293b; border: 1px solid #334155; }
    .signal-15 { background: #1e3a8a; border: 2px solid #3b82f6; padding: 20px; border-radius: 15px; text-align: center; }
    .signal-10x { background: #701a75; border: 2px solid #d946ef; padding: 20px; border-radius: 15px; text-align: center; animation: pulse 1.5s infinite; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.7; } 100% { opacity: 1; } }
</style>
""", unsafe_allow_html=True)

if 'aviator_hist' not in st.session_state:
    st.session_state.aviator_hist = []

def reg_v(val):
    st.session_state.aviator_hist.insert(0, val)

# --- MOTOR DE ANÁLISE ---
def analisar_aviator():
    h = st.session_state.aviator_hist
    if len(h) < 5: return None
    
    baixas_seguidas = 0
    for v in h:
        if v < 1.3: baixas_seguidas += 1
        else: break
        
    giros_sem_10x = 0
    for v in h:
        if v < 10: giros_sem_10x += 1
        else: break

    if baixas_seguidas >= 3:
        return {"sug": "ENTRADA 1.5x / 2.0x", "tipo": "recuperacao", "conf": 91}
    if giros_sem_10x >= 35:
        return {"sug": "BUSCAR 10.0x (VELA ROSA)", "tipo": "rosa", "conf": 75}
    
    return None

# --- INTERFACE ---
st.title("✈️ IA AVIATOR - ESTRATÉGIA DE MULTIPLICADOR")

c_in, c_out = st.columns([1, 1.2])

with c_in:
    st.subheader("📥 Registrar Multiplicador")
    val = st.number_input("Valor da última vela:", min_value=1.0, step=0.01, format="%.2f")
    if st.button("REGISTRAR VELA", use_container_width=True):
        reg_v(val)
        st.rerun()
    
    st.divider()
    st.write("📜 **Últimos Resultados:**")
    # CORREÇÃO AQUI: Mudança na forma de exibir a cor e o valor
    for v in st.session_state.aviator_hist[:12]:
        cor_vela = "#d946ef" if v >= 10 else "#3b82f6" if v >= 2 else "#94a3b8"
        st.markdown(f"<span style='color:{cor_vela}; font-weight:bold; font-size:18px;'>{v}x</span>", unsafe_allow_html=True)

with c_out:
    st.subheader("🔮 Previsão de Cic
