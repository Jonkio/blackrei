import streamlit as st
import pandas as pd

st.set_page_config(page_title="IA BAC BO - ANALYZER", layout="wide")

st.markdown("""
<style>
    .main { background-color: #020617; color: #f8fafc; }
    .stButton>button { width: 100%; border-radius: 12px; height: 60px; font-weight: bold; font-size: 18px; }
    .card-bac { padding: 20px; border-radius: 15px; text-align: center; border: 2px solid #334155; margin-bottom: 15px; }
    .player-win { background: #1e3a8a; border-color: #3b82f6; }
    .banker-win { background: #450a0a; border-color: #ef4444; }
    .tie-win { background: #3f2b05; border-color: #eab308; }
    .signal-box { background: #064e3b; border: 2px solid #22c55e; padding: 20px; border-radius: 15px; text-align: center; animation: pulse 2s infinite; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.8; } 100% { opacity: 1; } }
</style>
""", unsafe_allow_html=True)

if 'bac_hist' not in st.session_state:
    st.session_state.bac_hist = []

def reg_bac(venc):
    st.session_state.bac_hist.insert(0, venc)

# --- MOTOR DE ANÁLISE ---
def analisar_bacbo():
    h = st.session_state.bac_hist
    if len(h) < 6: return None
    
    # Transforma em string para ler padrões (P=Player, B=Banker, T=Tie)
    s = "".join([x[0] for x in h[:10]])
    
    # 1. Quebra de Sequência (Anti-Tendência)
    if s.startswith("PPPP"): return {"sug": "BANKER", "conf": 88, "motivo": "Exaustão de Sequência Player"}
    if s.startswith("BBBB"): return {"sug": "PLAYER", "conf": 88, "motivo": "Exaustão de Sequência Banker"}
    
    # 2. Padrão de Alternância (Xadrez)
    if s.startswith("PBPB") or s.startswith("BPBP"):
        sug = "PLAYER" if s[0] == "B" else "BANKER"
        return {"sug": sug, "conf": 92, "motivo": "Padrão Xadrez (Alternância)"}
    
    # 3. Padrão de Duplas
    if s.startswith("PPBB") or s.startswith("BBPP"):
        sug = "PLAYER" if s[0] == "B" else "BANKER"
        return {"sug": sug, "conf": 85, "motivo": "Seguindo Padrão de Duplas"}

    return None

# --- INTERFACE ---
st.title("🎲 IA BAC BO - ESTRATÉGIA DE DADOS")

col_reg, col_prev = st.columns([1, 1.2])

with col_reg:
    st.subheader("📥 Registrar Vencedor")
    c1, c2, c3 = st.columns(3)
    if c1.button("🔵 JOGADOR", key="btn_p"): reg_bac("PLAYER"); st.rerun()
    if c2.button("🟡 EMPATE", key="btn_t"): reg_bac("TIE"); st.rerun()
    if c3.button("🔴 BANCA", key="btn_b"): reg_bac("BANKER"); st.rerun()
    
    st.divider()
    st.write("📜 **Histórico Recente:**")
    if st.session_state.bac_hist:
        for i, res in enumerate(st.session_state.bac_hist[:8]):
            cor = "blue" if res == "PLAYER" else "red" if res == "BANKER" else "orange"
            st.markdown(f"{i+1}º: <b style='color:{cor}'>{res}</b>", unsafe_allow_html=True)

with col_prev:
    st.subheader("🔮 Análise de Tendência")
    analise = analisar_bacbo()
    
    if analise:
        cor_text = "#3b82f6" if analise['sug'] == "PLAYER" else "#ef4444"
        st.markdown(f"""
            <div class="signal-box">
                <small>{analise['motivo']}</small>
                <h1 style="color:{cor_text}; font-size:60px; margin:10px 0;">{analise['sug']}</h1>
                <p>Confiança: {analise['conf']}%</p>
            </div>
        """, unsafe_allow_html=True)
        st.warning("⚠️ Dica: Em caso de perda, use no máximo 1 Martingale ou espere o próximo sinal.")
    else:
        st.info("Aguardando mais 6 registros para confirmar padrão de mesa...")

if st.button("🗑️ LIMPAR HISTÓRICO"):
    st.session_state.bac_hist = []
    st.rerun()
