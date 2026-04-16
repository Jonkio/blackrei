import streamlit as st

st.set_page_config(page_title="IA SPEEDWAY - CONFIRMAÇÃO REAL", layout="wide")

# Estilização
st.markdown("""
<style>
    .main { background-color: #020617; color: white; }
    .stButton>button { height: 60px; border-radius: 12px; font-weight: bold; font-size: 18px; }
    .btn-selected { background-color: #3b82f6 !important; color: white !important; border: 2px solid white !important; }
    .history-ball { 
        display: inline-block; width: 35px; height: 35px; line-height: 35px; 
        border-radius: 50%; text-align: center; font-weight: bold; margin: 3px; 
        border: 1px solid #475569;
    }
    .pos-1 { background-color: #facc15; color: black; } /* Dourado */
    .pos-2 { background-color: #94a3b8; color: black; } /* Prata */
    .signal-card { background: #064e3b; border: 2px solid #22c55e; padding: 20px; border-radius: 15px; text-align: center; }
</style>
""", unsafe_allow_html=True)

# Inicialização de variáveis de seleção
if 'venc_sel' not in st.session_state: st.session_state.venc_sel = None
if 'plac_sel' not in st.session_state: st.session_state.plac_sel = None
if 'h_speed_full' not in st.session_state: st.session_state.h_speed_full = []

def confirmar_entrada():
    if st.session_state.venc_sel and st.session_state.plac_sel:
        # Salva o par (1º, 2º) no histórico
        st.session_state.h_speed_full.insert(0, {
            "1": st.session_state.venc_sel,
            "2": st.session_state.plac_sel
        })
        # Reseta as seleções para a próxima rodada
        st.session_state.venc_sel = None
        st.session_state.plac_sel = None
    else:
        st.error("Selecione o 1º e o 2º colocado antes de clicar em OK!")

st.title("🏍️ SPEEDWAY PRO - REGISTRO DUPLO")

col_input, col_view = st.columns([1.3, 1])

with col_input:
    st.subheader("🏁 Selecione o Pódio")
    
    # Seleção do Primeiro
    st.write("🏆 **QUEM GANHOU? (1º)**")
    c1, c2, c3, c4 = st.columns(4)
    for i, col in enumerate([c1, c2, c3, c4], 1):
        if col.button(f"P{i}", key=f"win_{i}", help="Vencedor", 
                      type="primary" if st.session_state.venc_sel == i else "secondary"):
            st.session_state.venc_sel = i
            st.rerun()

    # Seleção do Segundo
    st.write("🥈 **QUEM FOI O 2º?**")
    p1, p2, p3, p4 = st.columns(4)
    for i, col in enumerate([p1, p2, p3, p4], 1):
        # Desabilita o botão do piloto que já foi selecionado como 1º
        disabled = (st.session_state.venc_sel == i)
        if col.button(f"P{i}", key=f"pla_{i}", disabled=disabled,
                      type="primary" if st.session_state.plac_sel == i else "secondary"):
            st.session_state.plac_sel = i
            st.rerun()

    st.divider()
    
    # Botão de Confirmação Final
    if st.button("✅ CONFIRMAR E ENVIAR (OK)", use_container_width=True):
        confirmar_entrada()
        st.rerun()

with col_view:
    st.subheader("📊 Análise e Histórico")
    
    if st.session_state.h_speed_full:
        # Cálculo de Atrasos (Maximas)
        h = st.session_state.h_speed_full
        atraso_podio = {i: 0 for i in range(1, 5)}
        
        for i in range(1, 5):
            for corrida in h:
                if corrida["1"] != i and corrida["2"] != i:
                    atraso_podio[i] += 1
                else:
                    break
        
        # Exibição de Alerta de Máxima
        alvo = max(atraso_podio, key=atraso_podio.get)
        if atraso_podio[alvo] >= 6:
            st.markdown(f"""
                <div class="signal-card">
                    <h3>🎯 ENTRADA SUGERIDA</h3>
                    <p>Piloto <b>{alvo}</b> para terminar em 1º ou 2º</p>
                    <small>Atraso Atual: {atraso_podio[alvo]} corridas</small>
                </div>
            """, unsafe_allow_html=True)

        st.write("---")
        st.write("📜 **Últimas Corridas (Vencedor / 2º):**")
        
        # Histórico Visual (Estilo Football Studio)
        for corrida in h[:15]:
            st.markdown(f"""
                <div style='display: flex; align-items: center; margin-bottom: 5px;'>
                    <span class="history-ball pos-1">{corrida['1']}</span>
                    <span style='margin: 0 10px;'>➔</span>
                    <span class="history-ball pos-2">{corrida['2']}</span>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Aguardando o primeiro registro de pódio...")

if st.button("🗑️ RESETAR SISTEMA"):
    st.session_state.h_speed_full = []
    st.session_state.venc_sel = None
    st.session_state.plac_sel = None
    st.rerun()
