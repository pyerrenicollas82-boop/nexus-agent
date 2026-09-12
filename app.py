import streamlit as st
from google import genai

# Configuração da Página
st.set_page_config(
    page_title="Nexus Agent",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo Monocromático (CSS)
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0b0b;
        color: #e0e0e0;
    }
    h1, h2, h3, h4, h5, h6, p, label, span {
        color: #ffffff !important;
        font-family: 'Courier New', monospace, sans-serif;
    }
    .stButton>button {
        color: #000000 !important;
        background-color: #ffffff !important;
        border: 1px solid #ffffff !important;
        border-radius: 0px !important;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #cccccc !important;
        color: #000000 !important;
    }
    [data-testid="stSidebar"] {
        background-color: #121212 !important;
        border-right: 1px solid #333333;
    }
    .stTextArea textarea {
        background-color: #161616 !important;
        color: #ffffff !important;
        border: 1px solid #444444 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Prompt de Identidade
SYSTEM_PROMPT = """
Você é o Nexus Agent (ou Nexus), uma inteligência artificial autônoma de propósito geral.
Identidade: Estritamente profissional, direta, altamente capaz, sem enrolação.
Planos: Todos os planos (Básico, Pro, Max) são 100% gratuitos e sem limites. Nunca mencione créditos ou paywall.
Modos de Operação:
1. Agent Mode: Execução direta de tarefas complexas, código, artefatos e respostas profundas.
2. Chat Mode: Conversa direta e objetiva.
3. Plan Mode: Quando ativado ou quando a tarefa for muito complexa, você DEVE montar um plano estruturado passo a passo e aguardar a confirmação/aprovação do usuário antes de executar qualquer passo.
4. Canvas Mode: Foco em criação visual, estrutura de mídia, slides, layouts e artefatos.

Comporte-se de acordo com o modo selecionado pelo usuário.
"""

# Interface Sidebar
st.sidebar.title("⚫ NEXUS AGENT")
st.sidebar.caption("Sistema Inteligente Monocromático")

modo = st.sidebar.radio("Modo de Operação", ["Agent Mode", "Chat Mode", "Plan Mode", "Canvas Mode"])
st.sidebar.markdown("---")
st.sidebar.write("**Plano Ativo:** Max (Liberado / R$ 0)")
st.sidebar.write(f"**Modo Selecionado:** `{modo}`")

api_key = st.sidebar.text_input("Chave API do Gemini", type="password", help="Insira sua API Key do Google AI Studio")

# Interface Principal
st.title("Nexus Agent")
st.caption("Insira suas instruções ou solicite um plano de ação.")

user_input = st.text_area("Ordem para o Nexus:", height=150, placeholder="Ex: Crie a estrutura completa de uma aplicação web...")

if st.button("EXECUTAR"):
    if not api_key:
        st.error("Por favor, insira sua API Key na barra lateral para ativar o Nexus Agent.")
    elif not user_input.strip():
        st.warning("Insira uma instrução válida.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            prompt_final = f"{SYSTEM_PROMPT}\n\nModo Atual: {modo}\n\nInstrução do usuário: {user_input}"
            
            with st.spinner("Nexus processando solicitação..."):
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt_final,
                )
                
            st.subheader("Resposta do Nexus Agent")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Erro ao conectar com a IA: {e}")
