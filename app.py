import streamlit as st

st.set_page_config(page_title="IA SPEEDWAY ANALYZER", layout="wide")

# Estilização para Mobile e Desktop
st.markdown("""
<style>
    .main { background-color: #020617; color: white; }
    .stButton>button { height: 70px; border-radius: 15px; font-weight: bold; font-size: 20px; }
    .status-box { background: #1e293b; border: 2px solid #334155; padding: 20px; border-radius: 15px; text-align: center; }
    .signal-on { background: #064e3b; border: 2px solid #22c55e; padding: 20px; border-radius: 15px; text-align: center; animation: pulse 2s infinite; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.8; } 100% { opacity: 1; } }
</style>
""", unsafe_allow_html=True)

if 'h_speed' not in st.session_state:
    st.session_state.h_speed = []

def reg_speed(v):
    st.session_state.h_speed.insert(0, v)

st.title("🏍️ IA SPEEDWAY - MAXIMAS")

col_input, col_analysis = st.columns([1, 1.2])

with col_input:
    st.subheader("📥 Registrar Vencedor")
    st.write("Selecione o piloto que venceu a corrida:")
    
    # Grid de botões para os 4 pilotos
    c1, c2 = st.columns(2)
    if c1.button("PILOTO 1", key="sp1", use_container_width=True): reg_speed(1); st.rerun()
    if c2.button("PILOTO 2", key="sp2", use_container_width=True): reg_speed(2); st.rerun()
    
    c3, c4 = st.columns(2)
    if c3.button("PILOTO 3", key="sp3", use_container_width=True): reg_speed(3); st.rerun()
    if c4.button("PILOTO 4", key="sp4", use_container_width=True): reg_speed(4); st.rerun()

    st.divider()
    if st.button("🗑️ LIMPAR HISTÓRICO"):
        st.session_state.h_speed = []
        st.rerun()

with col_analysis:
    st.subheader("🛰️ Análise de Máximas")
    
    if len(st.session_state.h_speed) < 5:
        st.info("Aguardando registro de pelo menos 5 corridas para gerar sinais...")
    else:
        # Calcular atraso (Gap) para cada piloto
        atrasos = {1: 0, 2: 0, 3: 0, 4: 0}
        for p in range(1, 5):
            for res in st.session_state.h_speed:
                if res != p:
                    atrasos[p] += 1
                else:
                    break
        
        # Exibir métricas de atraso
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("P1", f"{atrasos[1]}g")
        m2.metric("P2", f"{atrasos[2]}g")
        m3.metric("P3", f"{atrasos[3]}g")
        m4.metric("P4", f"{atrasos[4]}g")

        # Lógica de Sinal (Dutching nos 2 com maior atraso)
        sorted_atrasos = sorted(atrasos.items(), key=lambda x: x[1], reverse=True)
        p_alvo1, gap1 = sorted_atrasos[0]
        p_alvo2, gap2 = sorted_atrasos[1]

        # Se o maior atraso for >= 8 giros, gera sinal
        if gap1 >= 8:
            st.markdown(f"""
                <div class="signal-on">
                    <h2 style='color:white; margin:0;'>🎯 SINAL CONFIRMADO</h2>
                    <p style='color:#22c55e; font-weight:bold;'>ENTRADA: PILOTOS {p_alvo1} E {p_alvo2}</p>
                    <small style='color:white;'>Estratégia: Cobrir as duas maiores probabilidades</small>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="status-box">
                    <h3>Aguardando Máxima</h3>
                    <p>Próximo alvo provável: Piloto {p_alvo1}</p>
                </div>
            """, unsafe_allow_html=True)

    st.write("📜 **Últimos resultados:**")
    st.write(st.session_state.h_speed[:10])
