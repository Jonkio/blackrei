import streamlit as st
import pandas as pd

# 1. Configuração de Layout Ultra-Wide e Tema Escuro Profundo
st.set_page_config(page_title="BLACKJACK IA - COMANDO ABSOLUTO", layout="wide")

# CSS Personalizado para Interface Profissional e Intuitiva
st.markdown("""
<style>
    .main { background-color: #020617; color: #f8fafc; }
    .stButton>button { width: 100%; border-radius: 10px; height: 50px; font-weight: bold; font-size: 16px; }
    
    /* Cores dos Botões de Cartas */
    .stButton>button[key^="btn_low"] { background-color: #166534; color: white; border: 1px solid #22c55e; } /* Baixas - Green */
    .stButton>button[key^="btn_neu"] { background-color: #334155; color: white; border: 1px solid #94a3b8; } /* Neutras - Gray */
    .stButton>button[key^="btn_hig"] { background-color: #991b1b; color: white; border: 1px solid #ef4444; } /* Altas - Red */
    
    /* Painéis de Métrica */
    .metric-panel {
        background: rgba(30, 41, 59, 0.5); padding: 20px; border-radius: 15px;
        text-align: center; border: 1px solid #334155; margin-bottom: 15px;
    }
    
    /* Cores de Decisão */
    .decision-hit { background-color: #ef4444; color: white; padding: 15px; border-radius: 10px; font-weight: bold; font-size: 20px; text-align: center; animation: pulse 1s infinite; }
    .decision-stand { background-color: #16a34a; color: white; padding: 15px; border-radius: 10px; font-weight: bold; font-size: 20px; text-align: center; }
    .decision-double { background-color: #ca8a04; color: white; padding: 15px; border-radius: 10px; font-weight: bold; font-size: 20px; text-align: center; }
    .decision-split { background-color: #9333ea; color: white; padding: 15px; border-radius: 10px; font-weight: bold; font-size: 20px; text-align: center; }

    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
        100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
    }
</style>
""", unsafe_allow_html=True)

# 2. Inicialização de Memória e Estado do Jogo
if 'rc' not in st.session_state:
    st.session_state.rc = 0          # Running Count (Contagem Corrente)
    st.session_state.cp = 0          # Cards Played (Cartas Jogadas)
    st.session_state.dr = 8.0        # Decks Remaining (Baralhos Restantes)
    st.session_state.player_hand = []
    st.session_state.dealer_card = None
    st.session_state.history = []

# --- MOTOR MATEMÁTICO 1: CONTAGEM DE CARTAS (SISTEMA HI-LO) ---
def registrar_carta(carta):
    low = ['2', '3', '4', '5', '6']
    high = ['10', 'J', 'Q', 'K', 'A']
    
    # Atualiza a contagem baseada no valor da carta
    if carta in low: st.session_state.rc += 1
    elif carta in high: st.session_state.rc -= 1
    
    # Incrementa total de cartas jogadas e estima baralhos restantes
    st.session_state.cp += 1
    # Baseado em 8 baralhos padrão de cassino ao vivo (416 cartas)
    st.session_state.dr = max(0.5, 8.0 - (st.session_state.cp / 52))
    st.session_state.history.insert(0, carta)

# --- MOTOR MATEMÁTICO 2: ESTRATÉGIA BÁSICA (A JOGADA PERFEITA) ---
def obter_jogada_perfeita(mao_player, carta_dealer):
    if not mao_player or not carta_dealer: return "Aguardando cartas..."
    
    # Mapeamento de cartas para valores inteiros
    v_map = {'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':10,'Q':10,'K':10,'A':11}
    
    try:
        p_cards = [v_map[c] for c in mao_player]
        d_card = v_map[carta_dealer]
    except KeyError: return "Erro no registro."

    p_sum = sum(p_cards)
    is_soft = 11 in p_cards and p_sum <= 21
    is_pair = len(mao_player) == 2 and mao_player[0] == mao_player[1]

    # Lógica de Decisão Simplificada (Estratégia Básica para 8 baralhos)
    # 1. Par (Split) - Prioridade Máxima
    if is_pair:
        p_val = p_cards[0]
        if p_val in [8, 11]: return "SPLIT" # Sempre splitar A,A e 8,8
        if p_val == 10: return "STAND" # Nunca splitar 10,10
        if p_val == 9 and d_card not in [7, 10, 11]: return "SPLIT"
        if p_val == 7 and d_card <= 7: return "SPLIT"
        if p_val == 6 and d_card <= 6: return "SPLIT"
        if p_val == 4 and d_card in [5, 6]: return "SPLIT"
        if p_val in [2, 3] and d_card <= 7: return "SPLIT"

    # 2. Mão Soft (Com Ás)
    if is_soft:
        other_card_sum = p_sum - 11
        if other_card_sum >= 8: return "STAND" # Soft 19+
        if other_card_sum == 7: # Soft 18
            if d_card >= 9: return "HIT"
            if d_card in [3, 4, 5, 6]: return "DOUBLE"
            return "STAND"
        if other_card_sum == 6 and d_card in [3, 4, 5, 6]: return "DOUBLE" # Soft 17
        if other_card_sum == 5 and d_card in [4, 5, 6]: return "DOUBLE" # Soft 16
        if other_card_sum == 4 and d_card in [4, 5, 6]: return "DOUBLE" # Soft 15
        if other_card_sum == 3 and d_card in [5, 6]: return "DOUBLE" # Soft 14
        if other_card_sum == 2 and d_card in [5, 6]: return "DOUBLE" # Soft 13
        return "HIT" # Padrão para mãos Soft baixas

    # 3. Mão Hard (Sem Ás ativo)
    if p_sum >= 17: return "STAND"
    if p_sum >= 13: # Hard 13-16
        if d_card <= 6: return "STAND"
        return "HIT"
    if p_sum == 12: # Hard 12
        if d_card in [4, 5, 6]: return "STAND"
        return "HIT"
    if p_sum == 11: return "DOUBLE" # Hard 11 sempre dobra
    if p_sum == 10: # Hard 10
        if d_card <= 9: return "DOUBLE"
        return "HIT"
    if p_sum == 9: # Hard 9
        if d_card in [3, 4, 5, 6]: return "DOUBLE"
        return "HIT"
    
    # Menor que 9
    return "HIT"

# --- INTERFACE DE COMANDO ---
st.title("🃏 BLACKJACK IA - COMANDO ABSOLUTO")

# Sidebar para Gestão do Baralho e Histórico
with st.sidebar:
    st.header("⚙️ Gestão do Baralho")
    # Indicadores Visuais de Deck
    st.write(f"Cartas na Mesa: **{st.session_state.cp}**")
    st.write(f"Shoe Restante: **{st.session_state.dr:.1f} baralhos**")
    st.progress(st.session_state.dr / 8.0)
    
    if st.button("🔄 Resetar Shoe (Embaralhou)", type="primary"):
        st.session_state.rc = 0
        st.session_state.cp = 0
        st.session_state.player_hand = []
        st.session_state.dealer_card = None
        st.session_state.history = []
        st.rerun()
    
    st.divider()
    st.subheader("📜 Fluxo de Cartas")
    st.write(", ".join(st.session_state.history[:30]))

# Layout Principal: 3 Colunas de Análise
c_input, c_decisao, c_gestao = st.columns([1, 1.2, 1])

# COLUNA 1: Entrada Rápida de Dados (Onde você clica)
with c_input:
    st.subheader("📥 Registro Rápido")
    cartas_ordenadas = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
    
    col_l, col_n, col_h = st.columns(3)
    col_l.caption("Baixas (+1)")
    col_n.caption("Neutras (0)")
    col_h.caption("Altas (-1)")

    # Botões de clique rápido com cores intuitivas
    for idx, card in enumerate(cartas_ordenadas):
        if idx <= 4: # 2-6 (Baixas)
            if col_l.button(card, key=f"btn_low_{card}"): registrar_carta(card); st.rerun()
        elif idx <= 7: # 7-9 (Neutras)
            if col_n.button(card, key=f"btn_neu_{card}"): registrar_carta(card); st.rerun()
        else: # 10-A (Altas)
            if col_h.button(card, key=f"btn_hig_{card}"): registrar_carta(card); st.rerun()

# COLUNA 2: O Motor de Decisão (O que fazer)
with c_decisao:
    st.subheader("🧠 A Jogada Perfeita")
    
    # Controles para montar a mão atual
    col_p, col_d = st.columns(2)
    
    with col_p:
        st.write("Sua Mão:")
        c1, c2 = st.columns(2)
        p1 = c1.selectbox("C1", ["-"] + cartas_ordenadas, key="p1")
        p2 = c2.selectbox("C2", ["-"] + cartas_ordenadas, key="p2")
        st.session_state.player_hand = [c for c in [p1, p2] if c != "-"]

    with col_d:
        st.write("Dealer (Cima):")
        st.session_state.dealer_card = st.selectbox("Carta", ["-"] + cartas_ordenadas, key="dc")

    # Cálculo e Exibição da Decisão
    if len(st.session_state.player_hand) == 2 and st.session_state.dealer_card and st.session_state.dealer_card != "-":
        decisao = obter_jogada_perfeita(st.session_state.player_hand, st.session_state.dealer_card)
        
        # Mapeamento de estilo para a decisão
        estilo = "decision-hit"
        texto = "PEDIR (HIT)"
        
        if decisao == "STAND": estilo = "decision-stand"; texto = "PARAR (STAND)"
        elif decisao == "DOUBLE": estilo = "decision-double"; texto = "DOBRAR (DOUBLE)"
        elif decisao == "SPLIT": estilo = "decision-split"; texto = "DIVIDIR (SPLIT)"
        
        st.markdown(f'<div class="{estilo}">{texto}</div>', unsafe_allow_html=True)
    else:
        st.info("Selecione sua mão e a carta do Dealer para ver a jogada.")

# COLUNA 3: Gestão de Aposta (Quanto apostar)
with c_gestao:
    st.subheader("💰 Gestão de Aposta")
    
    # Cálculo do True Count (O "Santo Graal" do Blackjack)
    tc = st.session_state.rc / st.session_state.dr if st.session_state.dr > 0 else 0
    
    st.markdown(f"""
        <div class="metric-panel">
            <small>Running Count (Hi-Lo)</small>
            <h2 style="color: #60a5fa;">{st.session_state.rc}</h2>
        </div>
        <div class="metric-panel" style="border: 2px solid #fbbf24;">
            <small>TRUE COUNT (CONTAGEM REAL)</small>
            <h1 style="color: #fbbf24; font-size: 50px;">{tc:.2f}</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Recomendação de Aposta baseada no True Count
    if tc >= 3:
        st.success("🔥 FOGO NO SHOE: Aposta Alta (4x Mínima)")
    elif tc >= 2:
        st.success("📈 Vantagem Boa: Aposta Média (2x Mínima)")
    elif tc <= -1:
        st.error("⚠️ Mesa Pobre: Aposta Mínima (Cuidado)")
    else:
        st.info("⚖️ Mesa Neutra: Aposta Mínima")
