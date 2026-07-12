 
import streamlit as st
import pandas as pd
import random

# 1. CONFIGURAÇÃO DA PÁGINA (Responsivo para celular)
st.set_page_config(
    page_title="Meu Mercadinho Verde",
    page_icon="🍏",
    layout="centered", 
    initial_sidebar_state="collapsed" 
)

# 2. ESTILIZAÇÃO CUSTOMIZADA (Fundo Verde, Ipês Amarelos nas laterais e UI Limpa)
st.markdown("""
    <style>
    /* Fundo principal verde escuro */
    .stApp {
        background-color: #0B2415;
        color: #E8F5E9;
    }
    
    /* Decoração com 3 Ipês Amarelos na Esquerda */
    .stApp::before {
        content: "🌳 🌳 🌳";
        position: fixed;
        left: 20px;
        top: 30%;
        font-size: 40px;
        writing-mode: vertical-rl;
        text-orientation: upright;
        opacity: 0.8;
        z-index: 0;
    }

    /* Decoração com 3 Ipês Amarelos na Direita */
    .stApp::after {
        content: "🌳 🌳 🌳";
        position: fixed;
        right: 20px;
        top: 30%;
        font-size: 40px;
        writing-mode: vertical-rl;
        text-orientation: upright;
        opacity: 0.8;
        z-index: 0;
    }

    /* Garantir que o conteúdo do app fique por cima dos ipês e legível */
    .block-container {
        position: relative;
        z-index: 1;
        background-color: rgba(11, 36, 21, 0.9); /* Leve transparência para destacar o centro */
        padding: 20px;
        border-radius: 10px;
    }

    /* Estilo dos cards de produto */
    .product-card {
        background-color: #163824;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        border: 1px solid #2E7D32;
    }
    
    /* Estilo do Card de Patrocinadores */
    .sponsor-card {
        background-color: #fbc02d;
        color: #0b2415;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        font-size: 14px;
        margin-bottom: 10px;
        border: 2px solid #f9a825;
    }

    /* Botões padrões */
    .stButton>button {
        background-color: #2E7D32 !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #4CAF50 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. BANCO DE DADOS EM MEMÓRIA
if 'produtos' not in st.session_state:
    dados_iniciais = {
        'id': [1, 2, 3],
        'nome': ['Maçã Argentina (Kg)', 'Arroz Integral 1kg', 'Café Torrado 500g'],
        'preco': [12.50, 7.80, 14.90],
        'avaliacoes': [5, 4, 5], 
        'qtd_avaliacoes': [1, 1, 1]
    }
    st.session_state.produtos = pd.DataFrame(dados_iniciais)

if 'carrinho' not in st.session_state:
    st.session_state.carrinho = {}

# 🌟 NOVO: Inicializa o salvamento da Chave Pix no sistema
if 'chave_pix' not in st.session_state:
    st.session_state.chave_pix = "mercadinhoverde@email.com"

df_produtos = st.session_state.produtos

# --- NAVEGAÇÃO SECRETA ---
menu = st.sidebar.radio("Navegação", ["Loja", "Área Restrita"])

# =====================================================================
# ÁREA DO CLIENTE
# =====================================================================
if menu == "Loja":
    st.title("🍏 Mercadinho Verde")
    st.write("Seja bem-vindo! Escolha seus produtos abaixo.")
    
    # SEÇÃO DE PATROCINADORES (No topo dos produtos)
    st.write("---")
    st.markdown("<h4 style='color: #FBC02D;'>⭐ Nossos Patrocinadores</h4>", unsafe_allow_html=True)
    
    col_pat1, col_pat2, col_pat3 = st.columns(3)
    with col_pat1:
        st.markdown('<div class="sponsor-card">🚜 Sítio Amarelo</div>', unsafe_allow_html=True)
    with col_pat2:
        st.markdown('<div class="sponsor-card">🥛 Laticínios Ipê</div>', unsafe_allow_html=True)
    with col_pat3:
        st.markdown('<div class="sponsor-card">🥖 Panificadora Silva</div>', unsafe_allow_html=True)
        
    st.write("---")
    
    # Listagem de Produtos
    if df_produtos.empty:
        st.info("Nenhum produto disponível no momento. Volte mais tarde!")
    else:
        for index, row in df_produtos.iterrows():
            with st.container():
                nota_media = row['avaliacoes'] / row['qtd_avaliacoes']
                st.markdown(f"""
                <div class="product-card">
                    <h3>{row['nome']}</h3>
                    <p style="font-size: 18px; color: #81C784; font-weight: bold;">R$ {row['preco']:.2f}</p>
                    <p style="font-size: 14px; color: #A5D6A7;">⭐ {nota_media:.1f} ({row['qtd_avaliacoes']} avaliações)</p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button(f"🛒 Adicionar", key=f"add_{row['id']}"):
                        p_id = row['id']
                        st.session_state.carrinho[p_id] = st.session_state.carrinho.get(p_id, 0) + 1
                        st.toast(f"{row['nome']} adicionado!", icon="🛒")
                        
                with col2:
                    nota = st.selectbox("Avaliar:", [5, 4, 3, 2, 1], key=f"nota_{row['id']}")
                    if st.button("Enviar Nota", key=f"btn_nota_{row['id']}"):
                        st.session_state.produtos.loc[st.session_state.produtos['id'] == row['id'], 'avaliacoes'] += nota
                        st.session_state.produtos.loc[st.session_state.produtos['id'] == row['id'], 'qtd_avaliacoes'] += 1
                        st.success("Obrigado pela avaliação!")
                        st.rerun()
                st.write("")

    # --- CARRINHO E PAGAMENTO ---
    st.write("---")
    st.header("🛒 Seu Carrinho")
    
    ids_existentes = df_produtos['id'].tolist() if not df_produtos.empty else []
    for c_id in list(st.session_state.carrinho.keys()):
        if c_id not in ids_existentes:
            del st.session_state.carrinho[c_id]

    if not st.session_state.carrinho:
        st.info("Seu carrinho está vazio.")
    else:
        total = 0.0
        for p_id, qtd in list(st.session_state.carrinho.items()):
            prod = df_produtos[df_produtos['id'] == p_id].iloc[0]
            subtotal = prod['preco'] * qtd
            total += subtotal
            st.write(f"**{prod['nome']}** x {qtd} = R$ {subtotal:.2f}")
        
        st.markdown(f"### **Total: R$ {total:.2f}**")
        
        if st.button("Limpar Carrinho"):
            st.session_state.carrinho = {}
            st.rerun()
            
        st.write("---")
        st.subheader("📱 Pagamento via PIX")
        st.write("Clique no botão abaixo para gerar a chave de pagamento configurada.")
        
        if st.button("Pagar com PIX"):
            # Exibe dinamicamente a chave definida na área restrita
            st.warning("Realize a transferência para a chave Pix abaixo:")
            st.info(f"🔑 **Chave PIX:** {st.session_state.chave_pix}")
            
            # Formatação limpa do código copia e cola utilizando a chave atualizada
            chave_limpa = st.session_state.chave_pix.replace("@", "").replace("-", "").replace(" ", "")
            chave_ficticia = f"00020126360014BR.GOV.BCB.PIX0114{chave_limpa[:15]}{random.randint(100,999)}"
            
            st.write("Código Copia e Cola:")
            st.code(chave_ficticia, language="text")
            st.success("Após realizar o pagamento, envie o comprovante para o nosso WhatsApp!")

# =====================================================================
# ÁREA DO ADMINISTRADOR (Escondida)
# =====================================================================
elif menu == "Área Restrita":
    st.title("🔒 Área do Administrador")
    
    senha = st.text_input("Digite a senha de acesso:", type="password")
    
    if senha == "admin123":
        st.success("Acesso liberado!")
        
        # 🌟 NOVA FUNCIONALIDADE: GERENCIADOR DA CHAVE PIX 🌟
        st.subheader("⚙️ Configurações de Pagamento")
        with st.expander("Mudar Chave PIX da Loja", expanded=True):
            st.write(f"Chave Pix atual ativa: `{st.session_state.chave_pix}`")
            nova_chave = st.text_input("Digite a nova Chave Pix (E-mail, Telefone, CNPJ ou Aleatória):", value=st.session_state.chave_pix)
            
            if st.button("Salvar Nova Chave Pix"):
                if nova_chave.strip():
                    st.session_state.chave_pix = nova_chave.strip()
                    st.success("Chave Pix atualizada com sucesso!")
                    st.rerun()
                else:
                    st.error("A chave Pix não pode ser salva em branco.")
        
        st.write("---")
        st.subheader("📦 Produtos em Estoque")
        
        if df_produtos.empty:
            st.info("Nenhum produto cadastrado.")
        else:
            st.dataframe(df_produtos[['id', 'nome', 'preco']], hide_index=True, use_container_width=True)
            
            st.write("---")
            st.subheader("🗑️ Remover Produtos")
            st.write("Selecione o produto que deseja excluir permanentemente:")
            
            opcoes_excluir = {f"{row['id']} - {row['nome']}": row['id'] for _, row in df_produtos.iterrows()}
            produto_selecionado = st.selectbox("Escolha o produto:", list(opcoes_excluir.keys()))
            
            st.markdown("""
                <style>
                div.stButton > button[key^="btn_remover"] {
                    background-color: #D32F2F !important;
                }
                div.stButton > button[key^="btn_remover"]:hover {
                    background-color: #C62828 !important;
                }
                </style>
            """, unsafe_allow_html=True)
            
            if st.button("Apagar Produto Selecionado", key="btn_remover"):
                id_para_remover = opcoes_excluir[produto_selecionado]
                st.session_state.produtos = st.session_state.produtos[st.session_state.produtos['id'] != id_para_remover]
                st.success("Produto removido com sucesso!")
                st.rerun()
        
        st.write("---")
        st.subheader("➕ Adicionar Novo Produto")
        novo_nome = st.text_input("Nome do Produto")
        novo_preco = st.number_input("Preço (R$)", min_value=0.0, value=1.0, step=0.5)
        
        if st.button("Cadastrar Produto"):
            if novo_nome:
                novo_id = int(st.session_state.produtos['id'].max() + 1) if not st.session_state.produtos.empty else 1
                nova_linha = pd.DataFrame([{
                    'id': novo_id,
                    'nome': novo_nome,
                    'preco': novo_preco,
                    'avaliacoes': 5,
                    'qtd_avaliacoes': 1
                }])
                st.session_state.produtos = pd.concat([st.session_state.produtos, nova_linha], ignore_index=True)
                st.success(f"'{novo_nome}' cadastrado com sucesso!")
                st.rerun()
            else:
                st.error("Por favor, digite o nome do produto.")
                
    elif senha != "":
        st.error("Senha incorreta!")













 
