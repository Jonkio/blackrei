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
    
    # Contagem de velas baixas (abaixo de 1.2x)
    baixas_seguidas = 0
    for v in h:
        if v < 1.2: baixas_seguidas += 1
        else: break
        
    # Busca por 10x (Vela Rosa)
    giros_sem_10x = 0
    for v in h:
        if v < 10: giros_sem_10x += 1
        else: break

    # Lógica de Sinal
    if baixas_seguidas >= 3:
        return {"sug": "ENTRADA 1.5x / 2.0x", "tipo": "recuperacao", "conf": 91}
    if giros_sem_10x >= 25:
        return {"sug": "BUSCAR 10.0x (VELA ROSA)", "tipo": "rosa", "conf": 75}
    
    return None

# --- INTERFACE ---
st.title("✈️ IA AVIATOR - ESTRATÉGIA DE MULTIPLICADOR")

c_in, c_out = st.columns([1, 1.2])

with c_in:
    st.subheader("📥 Registrar Multiplicador")
    val = st.number_input("Valor da última vela:", min_value=1.0, step=0.1, format="%.2f")
    if st.button("REGISTRAR VELA", use_container_width=True):
        reg_v(val)
        st.rerun()
    
    st.divider()
    st.write("📜 **Últimos Resultados:**")
    for v in st.session_state.aviator_hist[:10]:
        cor = "#d946ef" if v >= 10 else "#3b82f6" if v >= 2 else "#94a3b8"
        st.markdown(f"<b style='color:{cor}'>{v:.2x}x</b>", unsafe_allow_html=True)

with c_out:
    st.subheader("🔮 Previsão de Ciclo")
    res = analisar_aviator()
    
    if res:
        estilo = "signal-10x" if res['tipo'] == "rosa" else "signal-15"
        st.markdown(f"""
            <div class="{estilo}">
                <h3>{res['sug']}</h3>
                <p>Confiança Estimada: {res['conf']}%</p>
                <small>Baseado no tempo de recuperação do algoritmo</small>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Aguardando mais dados para identificar o ciclo de pagamento...")

    st.divider()
    # Contador de Gaps
    if st.session_state.aviator_hist:
        g10 = 0
        for x in st.session_state.aviator_hist:
            if x < 10: g10 += 1
            else: break
        st.metric("Giros desde a última 10x", f"{g10}")
