import streamlit as st

# 1. Configuração da Página
st.set_page_config(page_title="IA AVIATOR - CRASH ANALYZER", layout="wide")

# 2. Estilização Visual
st.markdown("""
<style>
    .main { background-color: #020617; color: #f8fafc; }
    .stButton>button { width: 100%; border-radius: 12px; height: 50px; font-weight: bold; }
    .signal-15 { background: #1e3a8a; border: 2px solid #3b82f6; padding: 20px; border-radius: 15px; text-align: center; }
    .signal-10x { background: #701a75; border: 2px solid #d946ef; padding: 20px; border-radius: 15px; text-align: center; animation: pulse 1.5s infinite; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.7; } 100% { opacity: 1; } }
</style>
""", unsafe_allow_html=True)

# 3. Inicialização do Histórico
if 'aviator_hist' not in st.session_state:
    st.session_state.aviator_hist = []

# --- FUNÇÕES DE MOTOR ---
def analisar_aviator():
    h = st.session_state.aviator_hist
    if len(h) < 5: return None
    
    baixas = 0
    for v in h:
        if v < 1.3: baixas += 1
        else: break
        
    g10x = 0
    for v in h:
        if v < 10: g10x += 1
        else: break

    if baixas >= 3:
        return {"sug": "ENTRADA 1.5x / 2.0x", "tipo": "recup"}
    if g10x >= 35:
        return {"sug": "BUSCAR 10.0x (ROSA)", "tipo": "rosa"}
    return None

# --- INTERFACE ---
st.title("✈️ IA AVIATOR - ESTRATÉGIA")

col_input, col_status = st.columns([1, 1.2])

with col_input:
    st.subheader("📥 Registrar Vela")
    valor_vela = st.number_input("Valor da vela:", min_value=1.0, step=0.01, format="%.2f")
    if st.button("REGISTRAR", use_container_width=True):
        st.session_state.aviator_hist.insert(0, valor_vela)
        st.rerun()
    
    st.divider()
    st.write("📜 **Histórico:**")
    for val in st.session_state.aviator_hist[:10]:
        cor = "#d946ef" if val >= 10 else "#3b82f6" if val >= 2 else "#94a3b8"
        st.markdown(f"<span style='color:{cor}; font-weight:bold;'>{val}x</span>", unsafe_allow_html=True)

with col_status:
    st.subheader("🔮 Previsão de Ciclo")
    res = analisar_aviator()
    
    if res:
        estilo = "signal-10x" if res['tipo'] == "rosa" else "signal-15"
        st.markdown(f"<div class='{estilo}'><h3>{res['sug']}</h3></div>", unsafe_allow_html=True)
    else:
        st.info("Aguardando mais dados para análise...")

    if st.session_state.aviator_hist:
        conta_g10 = 0
        for x in st.session_state.aviator_hist:
            if x < 10: conta_g10 += 1
            else: break
        st.metric("Giros sem 10x", f"{conta_g10}")

if st.button("🗑️ LIMPAR"):
    st.session_state.aviator_hist = []
    st.rerun()
