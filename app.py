import base64
import streamlit as st
import json
import re
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from chatbot import run_chatbot

# Read and encode the image
with open("./art_smart_helper.png", "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode()

st.set_page_config(layout="wide", page_title="Chatbot com Streamlit")

# Inicia a flag que controla se o chat está aberto
if "chat_open" not in st.session_state:
    st.session_state.chat_open = False

# Lista de atividades (resumida para exemplo)
atividades = [
    "Construção Civil - Edificações - de edificação - de alvenaria",
    "Construção Civil - Edificações - de edificação - de madeira",
    "Construção Civil - Edificações - de edificação - em sistema pré-fabricado",
    "Construção Civil - Edificações - de edificação - em materiais mistos",
    "Construção Civil - Edificações - de edificação - em outros materiais"
    "Saneamento Ambiental - Sistema de Abastecimento de Água - de ensaio",
    "Saneamento Ambiental - Sistema de Abastecimento de Água - de análise",
    "Saneamento Ambiental - Sistema de Abastecimento de Água - de percolação de solo",
    "Saneamento Ambiental - Sistema de Abastecimento de Água - tratamento de água",
    "Saneamento Ambiental - Sistema de Abastecimento de Água - adução de água",
    "Saneamento Ambiental - Sistema de Abastecimento de Água - tanques ou reservatórios de água",
    "Saneamento Ambiental - Sistema de Esgoto/Resíduos - tratamento de efluentes líquidos domésticos",
    "Saneamento Ambiental - Sistema de Esgoto/Resíduos - tratamento de efluentes líquidos industriais",
    "Saneamento Ambiental - Sistema de Esgoto/Resíduos - tratamento de efluentes líquidos hospitalares",
    "Saneamento Ambiental - Sistema de Esgoto/Resíduos - tratamento de chorume",
    "Saneamento Ambiental - Sistema de Esgoto/Resíduos - domiciliares e de limpeza urbana",
    "Saneamento Ambiental - Sistema de Esgoto/Resíduos - industriais",
    "Saneamento Ambiental - Sistema de Esgoto/Resíduos - resíduos de saúde",
    "Saneamento Ambiental - Sistema de Esgoto/Resíduos - da construção civil",
    "Saneamento Ambiental - Sistema de Esgoto/Resíduos - incineração de resíduos sólidos de limpeza urbana",
    "Saneamento Ambiental - Sistema de Esgoto/Resíduos - incineração de resíduos sólidos industriais",
    "Saneamento Ambiental - Sistema de Esgoto/Resíduos - incineração de resíduos sólidos de serviços de saúde",
    "Saneamento Ambiental - Sistema de Esgoto/Resíduos - unidade de reciclagem de resíduos sólidos",
    "Saneamento Ambiental - Sistema de Esgoto/Resíduos - usina de compostagem de resíduos orgânicos",
    "Saneamento Ambiental - Sistema de Esgoto/Resíduos - plano de gerenciamento de resíduos",
    "Saneamento Ambiental - Sistema de Esgoto/Resíduos - disposição final de resíduos sólidos",
    "Saneamento Ambiental - Sistema de Esgoto/Resíduos - aterro sanitário",
    "Saneamento Ambiental - Sistema de Esgoto/Resíduos - sistemas de drenagem",
    "Saneamento Ambiental - Sistema de Esgoto/Resíduos - monitoramento ambiental de aterros",
    "Saneamento Ambiental - Sistema de Esgoto/Resíduos - monitoramento geotécnico em topografia de aterros",
    "Meio Ambiente - Controle e Monitoramento Ambiental - controle sanitário do ambiente",
    "Meio Ambiente - Controle e Monitoramento Ambiental - poluição",
    "Meio Ambiente - Controle e Monitoramento Ambiental - passivo ambiental",
    "Meio Ambiente - Controle e Monitoramento Ambiental - controle de uso do solo",
    "Meio Ambiente - Controle e Monitoramento Ambiental - controle de poluição ambiental",
    "Meio Ambiente - Diagnóstico e Caracterização Ambiental - caracterização do meio físico",
    "Meio Ambiente - Diagnóstico e Caracterização Ambiental - caracterização do meio biótico",
    "Meio Ambiente - Diagnóstico e Caracterização Ambiental - de caracterização fitossociológica",
    "Meio Ambiente - Diagnóstico e Caracterização Ambiental - caracterização do meio antrópico",
    "Meio Ambiente - Diagnóstico e Caracterização Ambiental - ensaio químico de solos",
    "Meio Ambiente - Diagnóstico e Caracterização Ambiental - diagnóstico ambiental",
    "Meio Ambiente - Diagnóstico e Caracterização Ambiental - prognóstico ambiental",
    "Meio Ambiente - Diagnóstico e Caracterização Ambiental - identificação de fontes poluidoras",
    "Meio Ambiente - Diagnóstico e Caracterização Ambiental - identificação e potencialização de impactos ambientais",
    "Meio Ambiente - Manejo e Gestão de Bacias Hidrográficas - de gestão de bacias hidrográficas",
    "Meio Ambiente - Manejo e Gestão de Bacias Hidrográficas - de recuperação de bacias hidrográficas",
    "Meio Ambiente - Manejo e Gestão de Bacias Hidrográficas - de caracterização de bacias hidrográficas",
    "Meio Ambiente - Recuperação Ambiental - biorremediação",
    "Meio Ambiente - Recuperação Ambiental - remediação em água",
    "Meio Ambiente - Recuperação Ambiental - remediação em solo",
    "Meio Ambiente - Recuperação Ambiental - remediação em água subterrânea",
    "Meio Ambiente - Recuperação Ambiental - recuperação ambiental",
    "Meio Ambiente - Recuperação Ambiental - mitigação ambiental",
    "Meio Ambiente - Tecnologia Ambiental - de tecnologia ambiental",
    "Meio Ambiente - Gestão Ambiental - de riscos ao meio ambiental",
    "Meio Ambiente - Gestão Ambiental - de resíduos sólidos",
    "Meio Ambiente - Gestão Ambiental - de adequação ambiental",
    "Meio Ambiente - Gestão Ambiental - de auditoria ambiental",
    "Meio Ambiente - Gestão Ambiental - de controle de qualidade ambiental",
    "Meio Ambiente - Gestão Ambiental - de estudos ambientais",
    "Meio Ambiente - Gestão Ambiental - de impacto ambiental",
    "Meio Ambiente - Gestão Ambiental - de educação ambiental",
    "Meio Ambiente - Gestão Ambiental - de modelagem ambiental",
    "Meio Ambiente - Gestão Ambiental - de planejamento ambiental",
    "Planejamento Urbano, Metropolitano e Regional - Planejamento Urbano - de plano diretor",
    "Levantamentos Topográficos Básicos - Levantamento Topográfico - de levantamento topográfico",
    "Geodésia - Geoprocessamento - de mapeamento técnico",
    "Geodésia - Georreferenciamento - de georreferenciamento",
    "Geodésia - Georreferenciamento - rural",
    "Agrimensura - Cadastro Técnico - urbano",
    "Agrimensura - Cadastro Técnico - rural",
    "Agrimensura - Parcelamento do Solo - urbano",
    "Agrimensura - Parcelamento do Solo - rural",
    "Prevenção e Controle de Riscos - Condições Ambientais de Conforto - de conforto acústico",
    "Proteção ao Meio Ambiente - Relatório de Impacto de Vizinhança Ambiental - RIVA - de Relatório de Impacto de Vizinhança Ambiental - RIVA",
]
# Unidades
unidades = ["", "m", "m²", "m³", "kg", "V", "W", "kWh", "L", "unid"]
# Prompt
prompt_observacao = ChatPromptTemplate.from_template(
    """Você é um engenheiro experiente encarregado de identificar atividades técnicas em descrições de projetos de engenharia. 

Sua função é identificar apenas atividades que estão descritas de forma **explícita ou com nomes muito semelhantes** à lista fornecida.  
Nunca deve inferir, deduzir ou adicionar atividades não mencionadas diretamente.

Para cada atividade identificada, informe:
- o nome da atividade (baseando-se na lista fornecida),
- a quantidade (se mencionada; caso contrário, use 1),
- a unidade de medida (se mencionada; caso contrário, deixe como string vazia: "")

A resposta deve ser sempre um JSON puro, **sem explicações ou comentários**.

---

**Exemplos**:

- Se a descrição for:  
  `"Projeto de edificação de 200 m² em alvenaria"`  
  e houver a atividade:  
  `"Construção Civil - Edificações - de edificação - de alvenaria"`  
  a saída será:  
  `[{{"atividade": "Construção Civil - Edificações - de edificação - de alvenaria", "quantidade": 200, "unidade": "m²"}}]`

- Se a descrição for:  
  `"Projeto de edificação em alvenaria"`  
  e houver a atividade:  
  `"Construção Civil - Edificações - de edificação - de alvenaria"`  
  a saída será:  
  `[{{"atividade": "Construção Civil - Edificações - de edificação - de alvenaria", "quantidade": 1, "unidade": ""}}]`

---

Com base na lista, identifique apenas as atividades que aparecem de forma explícita ou com nomes muito semelhantes.

Retorne o seguinte JSON puro:

[
  {{"atividade": "nome da atividade", "quantidade": número inteiro, "unidade": "texto"}}
]

---

A seguir está a descrição de um projeto e uma lista de atividades possíveis.

Descrição do projeto:
{descricao}

Lista de atividades possíveis:
{lista_atividades}
"""
)
prompt_correcao = ChatPromptTemplate.from_template(
    """Você é um revisor profissional de textos técnicos e acadêmicos. 

Seu objetivo é corrigir o texto fornecido, mantendo **a ideia, o conteúdo e a estrutura original**.  
Você deve realizar apenas **ajustes gramaticais, ortográficos, de concordância verbal e nominal**, evitando reescrever ou reformular ideias.

**Não modifique o estilo, a ordem das frases ou a intenção do autor.**  
Não inclua comentários, explicações ou observações na resposta — apenas o texto corrigido, pronto para uso.

---

Texto a ser revisado:
{texto}
"""
)

# Modelo da LLM
model = ChatGoogleGenerativeAI(
    model="models/gemini-2.0-flash",
    max_output_tokens=256,
    temperature=0.0,
)
chain_observacao = LLMChain(llm=model, prompt=prompt_observacao)
chain_correcao = LLMChain(llm=model, prompt=prompt_correcao)


# Extrator de JSON
def extrair_json(texto):
    match = re.search(r"\[\s*{.*?}\s*]", texto, re.DOTALL)
    if match:
        return json.loads(match.group(0))
    else:
        raise ValueError("JSON não encontrado na resposta do modelo.")


# Análise com uma llm
def analisar_observacao(texto):
    lista_formatada = "\n".join(f"- {a}" for a in atividades)
    raw_output = chain_observacao.run(
        {"descricao": texto, "lista_atividades": lista_formatada}
    )
    try:
        return extrair_json(raw_output)
    except Exception:
        return []


# Função que corrige a observação
def corrigir_observacao(texto):
    return chain_correcao.run({"texto": texto})


# --- CSS: apenas aumenta o tamanho da fonte ---
st.markdown(
    """
<style>
    html, body, [class*="css"] {
        font-size: 24px !important;
    }

    h1 {
        font-size: 72px !important;
        text-align: center;
        margin: 0 !important;
        line-height: 1.2;
    }

    label {
        font-size: 28px !important;
    }

    input, textarea, select {
        font-size: 28px !important;
    }

    .stButton > button {
        font-size: 26px !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

img_html = f"""
<div style='display:flex;justify-content:center;'>
    <img src="data:image/jpeg;base64,{encoded}" width="300"/>
</div>
"""
st.markdown(img_html, unsafe_allow_html=True)
st.markdown(
    "<h1>ART Smart Helper</h1>",
    unsafe_allow_html=True,
)

# --- Estado inicial ---
if "atividades_extraidas" not in st.session_state:
    st.session_state.atividades_extraidas = []

# --- Entradas principais ---
nome = st.text_input("Nome", value="João da Silva")
cpf = st.text_input("CPF", value="123.456.789-00")
n_crea = st.text_input("Nº CREA", value="12345678")

st.markdown("---")

participacao = st.text_input("Participação", value="Individual")
fidelidade = st.text_input("Fidelidade", value="")

observacao = st.text_area(
    "Observação",
    value=st.session_state.get("observacao_corrigida", ""),
    key="observacao_input",
)

# --- Botões lado a lado ---
col1, col2 = st.columns([1, 1])
with col1:
    corrigir = st.button("✏️ Corrigir")
with col2:
    analisar = st.button("✅ Analisar Observação")

# Análise e preenchimento automático
if analisar:
    resultado = analisar_observacao(observacao)
    if isinstance(resultado, list):
        if len(resultado) == 0:
            st.warning("Melhore sua observação")
        else:
            st.session_state.atividades_extraidas = resultado
            st.rerun()
    else:
        st.warning(resultado)

# Aplica a correção se o botão "Corrigir" for clicado
if corrigir:
    texto_corrigido = corrigir_observacao(st.session_state["observacao_input"])
    st.session_state["observacao_corrigida"] = texto_corrigido
    st.rerun()

# Renderiza edição de atividades detectadas
st.subheader("Atividades Detectadas (Editáveis)")
for i, item in enumerate(st.session_state.atividades_extraidas):
    col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
    with col1:
        atividade = st.selectbox(
            f"Atividade {i + 1}",
            atividades,
            index=atividades.index(item["atividade"])
            if item["atividade"] in atividades
            else 0,
            key=f"atividade_{i}",
        )
        st.session_state.atividades_extraidas[i]["atividade"] = atividade
    with col2:
        quantidade = st.number_input(
            "Qtd", min_value=0, value=item["quantidade"], key=f"quantidade_{i}"
        )
        st.session_state.atividades_extraidas[i]["quantidade"] = quantidade
    with col3:
        unidade = st.selectbox(
            "Unidade",
            unidades,
            index=unidades.index(item["unidade"]) if item["unidade"] in unidades else 0,
            key=f"unidade_{i}",
        )
        st.session_state.atividades_extraidas[i]["unidade"] = unidade
    with col4:
        if st.button("❌", key=f"remover_{i}"):
            st.session_state.atividades_extraidas.pop(i)
            st.rerun()

# Botão para abrir o chat — só aparece quando chat_open == False
if not st.session_state.chat_open:
    if st.button("Abrir Chatbot"):
        st.session_state.chat_open = True
        # Força um rerun, para atualizar a UI imediatamente
        st.rerun()

# Se a flag chat_open for True, mostramos o chat e o botão de fechar
if st.session_state.chat_open:
    st.write("---")
    # Botão para fechar o chat
    if st.button("Fechar Chatbot"):
        st.session_state.chat_open = False
        st.rerun()

    # Chama a função que renderiza o chatbot
    run_chatbot()

# Se o chat não estiver aberto, mostramos somente o conteúdo normal
if not st.session_state.chat_open:
    st.write("""
    Aqui fica a interface normal do seu aplicativo (gráficos, formulários, etc.). 
    Quando você clicar em **'Abrir Chatbot'**, o chat aparecerá abaixo.
    """)
