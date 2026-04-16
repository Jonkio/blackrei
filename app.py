import streamlit as st

st.set_page_config(page_title="IA SPEEDWAY PRO - PÓDIO", layout="wide")

st.markdown("""
<style>
    .main { background-color: #020617; color: white; }
    .stButton>button { height: 60px; border-radius: 10px; font-weight: bold; }
    .gold { border: 2px solid #facc15 !important; color: #facc15 !important; }
    .silver { border: 2px solid #94a3b8 !important; color: #94a3b8 !important; }
    .signal-box { background: #064e3b; border: 2px solid #22c55e; padding: 20px; border-radius: 15px; text-align: center; }
</style>
""", unsafe_allow_html=True)

if 'h_speed_v' not in st.session_state: st.session_state.h_speed_v = [] # Vencedores
if 'h_speed_p' not in st.session_state: st.session_state.h_speed_p = [] # Segundos (Place)

st.title("🏍️ SPEEDWAY PRO - ANÁLISE DE PÓDIO")

c_input, c_analise = st.columns([1.2, 1])

with c_input:
    st.subheader("🏁 Registrar Resultado")
    
    # Registro do 1º Colocado
    st.write("🏆 **1º COLOCADO (Vencedor)**")
    v1, v2, v3, v4 = st.columns(4)
    if v1.button("P1", key="v1", help="Piloto 1 venceu"): st.session_state.h_speed_v.insert(0, 1); st.rerun()
    if v2.button("P2", key="v2"): st.session_state.h_speed_v.insert(0, 2); st.rerun()
    if v3.button("P3", key="v3"): st.session_state.h_speed_v.insert(0, 3); st.rerun()
    if v4.button("P4", key="v4"): st.session_state.h_speed_v.insert(0, 4); st.rerun()

    # Registro do 2º Colocado
    st.write("🥈 **2º COLOCADO (Place)**")
    p1, p2, p3, p4 = st.columns(4)
    if p1.button("P1", key="p1"): st.session_state.h_speed_p.insert(0, 1); st.rerun()
    if p2.button("P2", key="p2"): st.session_state.h_speed_p.insert(0, 2); st.rerun()
    if p3.button("P3", key="p3"): st.session_state.h_speed_p.insert(0, 3); st.rerun()
    if p4.button("P4", key="p4"): st.session_state.h_speed_p.insert(0, 4); st.rerun()

    if st.button("🗑️ LIMPAR TUDO"):
        st.session_state.h_speed_v = []
        st.session_state.h_speed_p = []
        st.rerun()

with c_analise:
    st.subheader("📊 Performance de Pódio")
    
    if len(st.session_state.h_speed_v) >= 5:
        # Cálculo de Atrasos para Vitória e para Pódio
        atrasos_v = {i: 0 for i in range(1, 5)}
        atrasos_podio = {i: 0 for i in range(1, 5)}
        
        for i in range(1, 5):
            # Atraso para vencer
            for res in st.session_state.h_speed_v:
                if res != i: atrasos_v[i] += 1
                else: break
            
            # Atraso para aparecer no pódio (1º ou 2º)
            for idx, res_v in enumerate(st.session_state.h_speed_v):
                res_p = st.session_state.h_speed_p[idx] if idx < len(st.session_state.h_speed_p) else None
                if res_v != i and res_p != i: atrasos_podio[i] += 1
                else: break

        # Exibição
        for i in range(1, 5):
            st.write(f"**Piloto {i}:** Sem vencer: `{atrasos_v[i]}g` | Fora do Pódio: `{atrasos_podio[i]}g` ")

        st.divider()
        
        # Lógica de Sinal Inteligente
        # Se um piloto está há muito tempo fora do pódio, a chance de ele ser 1º ou 2º é Gigante.
        alvo = max(atrasos_podio, key=atrasos_podio.get)
        if atrasos_podio[alvo] >= 6:
            st.markdown(f"""
                <div class="signal-box">
                    <h3>🎯 SINAL DE SEGURANÇA</h3>
                    <p>Entrar no <b>PILOTO {alvo}</b> para terminar em <b>1º ou 2º</b></p>
                    <small>Atraso de Pódio: {atrasos_podio[alvo]} corridas</small>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Registre 5 resultados (1º e 2º) para ativar a inteligência.")
