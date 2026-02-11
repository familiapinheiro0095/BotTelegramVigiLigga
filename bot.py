import os
import warnings
warnings.filterwarnings("ignore")
import logging
from uuid import uuid4
from dotenv import load_dotenv
from datetime import datetime
from PIL import Image
import pandas as pd
from telegram import (Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton)
from telegram.ext import (ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler)
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from telegram import ReplyKeyboardRemove
from telegram.constants import ParseMode, ChatAction
import json
import asyncio

# Lista de itens do Toolkit
TOOLKIT_ITENS = [
    #EPC
    {"item": "CONE SINALIZADOR REFLETIVO PADRÃO COPEL 5 UNID", "secao": "EPC", "segmentos":["B2C", "B2B", "Redes"]},
    {"item": "BANDEIRA DE SINALIZAÇÃO (ESCADAS) BANDEIROLA", "secao": "EPC", "segmentos":["B2C", "B2B", "Redes"]},
    {"item": "FITA ZEBRADA", "secao": "EPC", "segmentos":["B2C", "B2B", "Redes"]},

    #EPI
    {"item": "BOTINA DE SEGURANÇA C/ CA ATIVO", "secao": "EPI", "segmentos": ["B2C", "B2B", "Redes"]},
    {"item": "CAPACETE COM ABA TOTAL E JUGULAR (CLASSE B)", "secao": "EPI", "segmentos": ["B2C", "B2B", "Redes"]},
    {"item": "CAPA DE CHUVA CONJUNTO JAQUETA E CALÇA COM REFLETIVO", "secao": "EPI", "segmentos": ["B2C", "B2B", "Redes"]},
    {"item": "MOSQUETÃO", "secao": "EPI", "segmentos": ["B2C", "B2B", "Redes"]},
    {"item": "CINTO DE SEGURANÇA TIPO PARAQUEDISTA 4 PONTOS", "secao": "EPI", "segmentos": ["B2C", "B2B", "Redes"]},
    {"item": "TALABARTE DE SEGURANÇA DE POSICIONAMENTO AJUSTAVEL", "secao": "EPI", "segmentos": ["B2C", "B2B", "Redes"]},
    {"item": "TALABARTE DE SEGURANÇA Y", "secao": "EPI", "segmentos": ["B2C", "B2B", "Redes"]},
    {"item": "LUVA MULTITATO PU", "secao": "EPI", "segmentos": ["B2C"]},
    {"item": "LUVA SEG COURO VAQUETA", "secao": "EPI", "segmentos": ["B2C", "B2B", "Redes"]},
    {"item": "LUVA ALTA TENSÃO ORION 2,5KV 500V LUVA DE COBERTURA", "secao": "EPI", "segmentos": ["B2B", "Redes"]},
    {"item": "CANETA DETECTORA DE TENSÃO SONORA", "secao": "EPI", "segmentos": ["B2B", "Redes"]},
    {"item": "LANTERNA DE CABEÇA (LED)", "secao": "EPI", "segmentos": ["B2C", "B2B", "Redes"]},
    {"item": "ÓCULOS DE SEGURANÇA (INCOLOR OU FUMÊ)", "secao": "EPI", "segmentos": ["B2C", "B2B", "Redes"]},
    {"item": "DEGRAU NIVELADOR DE ESCADA", "secao": "EPI", "segmentos": ["B2C", "B2B", "Redes"]},
    {"item": "PLATAFORMA PARA ESCADA", "secao": "EPI", "segmentos": ["B2C", "B2B", "Redes"]},
    {"item": "MANTA P/ ISOLAÇÃO C/ VELCRO", "secao": "EPI", "segmentos": ["B2C", "B2B", "Redes"]},
    {"item": "PROTETOR SOLAR (< QUE FATOR 30)", "secao": "EPI", "segmentos": ["B2C", "B2B", "Redes"]},
    {"item": "CORDA 12MM 16 METROS", "secao": "EPI", "segmentos": ["B2C", "B2B", "Redes"]},
    {"item": "CINTA C/ CATRATA DE AMARRAÇÃO DE ESCADA", "secao": "EPI", "segmentos": ["B2C", "B2B", "Redes"]},
    {"item": "ESCADA DE FIBRA EXTENSIVA 7,2M", "secao": "EPI", "segmentos": ["B2C", "B2B", "Redes"]},
    {"item": "ESCADA INDOOR ARTICULADA 8 DEGRAUS", "secao": "EPI", "segmentos": ["B2C"]},
    {"item": "PERNEIRA COURO", "secao": "EPI", "segmentos": ["B2B", "Redes"]},
    {"item": "COLETE REFLETIVO", "secao": "EPI", "segmentos": ["B2B"]},
    # Ferramental
    {"item": "MÁQUINA DE FUSÃO (ALINHAMENTO PELA CASCA)", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "MÁQUINA DE FUSÃO (ALINHAMENTO PELO NÚCLEO)", "secao": "Ferramental", "segmentos": ["B2B", "Redes"]},
    {"item": "FITA GUIA (ALMA AÇO) PVC", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "CHAVE DE BAP 1/4", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "CHAVE DE BAP 1/8 MM", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "CHAVE DE GUARITA - CAIXA SUBTERRANEA", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "PÉ DE CABRA 595-610MM", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "CHAVE PHILIPS 1/4X5,5 (Isolada)", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "CHAVE PHILIPS 1/8X3 (Isolada)", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "BOLSA DE LONA P/ FERRAMENTAS", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "BOLSA EM LONA (BORNAL)", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "CHAVE DG (DISTR. GERAL -PRÉDIOS)", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "SUPORTE (CAVALETE) PARA BOBINA", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "ESTILETE TRAPEZOIDAL PROFISSIONAL", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "INVERSOR 300W", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "EXTENSÃO ELÉTRICA EM CABO PP - 10A (20 METROS)", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "FURADEIRA ELÉTRICA", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "POWER METER PON", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "CANETA DETECTORA DE TENSÃO", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "DETECTOR DE TENSÃO ALTA/BAIXA", "secao": "Ferramental", "segmentos": ["B2B", "Redes"]},
    {"item": "CANETA LASER", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "CLIVADOR / CLIVADOR DE FIBRA DE ALTA PRECISÃO", "secao": "Ferramental", "segmentos": ["B2C", "B2B", "Redes"]},
    {"item": "DECAPADOR DE ACRILATO", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "DECAPADOR DE CABO", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "DECAPADOR DE CABO CIRCULAR LONGITUDINAL", "secao": "Ferramental", "segmentos": ["B2B", "Redes"]},
    {"item": "CANETA P/ LIMPEZA CONECTOR DE FIBRA 2,5MM SC/ST/FC", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "CANETA P/ LIMPEZA CONECTOR DE FIBRA LC/PC 1.25mm", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "OTDR FIBRA ATIVA 39 DB (EQUIPES DE REDE E B2B)", "secao": "Ferramental", "segmentos": ["B2B", "Redes"]},
    {"item": "MEDIDOR DE DISTÂNCIA", "secao": "Ferramental", "segmentos": ["B2B", "Redes"]},
    {"item": "ALICATE DE BICO MEIA CANA 6¨ ISOLADO", "secao": "Ferramental", "segmentos": ["B2C", "B2B", "Redes"]},
    {"item": "ALICATE CRIMPADOR", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "ALICATE DE CORTE DIAGONAL 6 ISOLADO", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "ALICATE UNIVERSAL 8 ISOLADO", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "BROCA CURTA PARA CONCRETO", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "BROCA CURTA PARA FERRO", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "BROCA CURTA PARA MADEIRA", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "BROCA LONGA PARA CONCRETO", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "BROCA LONGA PARA MADEIRA", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "MÁQUINA DE CINTAR POSTE (FUSIMEC)", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "TESTADOR DE CABO UTP/RJ45/RJ11", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "IDENTIFICADOR DE FIBRA ATIVA", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "MARTELO 25MM (195)", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "PINCEL LARGO 102MM", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "KIT LIMPEZA DOMÉSTICA (VASSOURA E PÁ)", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "GARRAFA DA ÁGUA", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "VARA DE MANOBRA", "secao": "Ferramental", "segmentos": ["B2C"]},
    {"item": "ROLETADOR DE TUBO LOOSE", "secao": "Ferramental", "segmentos": ["B2B", "Redes"]},
    {"item": "ROLETADOR DE CABO", "secao": "Ferramental", "segmentos": ["B2B", "Redes"]},
    {"item": "FACÃO 12 POLEGADAS", "secao": "Ferramental", "segmentos": ["B2B", "Redes"]},
    {"item": "LAMPADA PORTATIL / NOTURNO", "secao": "Ferramental", "segmentos": ["B2B", "Redes"]},
    {"item": "LATERNA HOLOFOTE LONGO ALCANCE", "secao": "Ferramental", "segmentos": ["B2B", "Redes"]},
    {"item": "KIT MESA E CADEIRA PARA FOSC/FIST", "secao": "Ferramental", "segmentos": ["B2B", "Redes"]},
    {"item": "LANTERNA DE SINALIZAÇÃO", "secao": "Ferramental", "segmentos": ["B2B", "Redes"]},
    {"item": "MICROSCÓPIO (FIBER INSPECTION PROBE)", "secao": "Ferramental", "segmentos": ["B2B", "Redes"]},
    {"item": "TALHA ALAVANCA DE 3M 3TON", "secao": "Ferramental", "segmentos": ["B2B", "Redes"]},
    {"item": "FOICE", "secao": "Ferramental", "segmentos": ["B2B", "Redes"]},
    {"item": "TENDA", "secao": "Ferramental", "segmentos": ["B2B", "Redes"]},
    {"item": "MAÇARICO BICO PORTATIL GÁS MAPP", "secao": "Ferramental", "segmentos": ["B2B", "Redes"]},
    {"item": "GUARDA SOL", "secao": "Ferramental", "segmentos": ["B2B", "Redes"]},
    # Material
    {"item": "ALCOOL ISOPROPILICO", "secao": "Material", "segmentos": ["B2C", "B2B", "Redes"]},
    {"item": "ESTICADOR", "secao": "Material", "segmentos": ["B2C"]},
    {"item": "ETIQUETA DE IDENTIFICAÇÃO DE CABO ÓPTICO", "secao": "Material", "segmentos": ["B2C"]},
    {"item": "FITA HELLERMAN", "secao": "Material", "segmentos": ["B2C"]},
    {"item": "GABARITO", "secao": "Material", "segmentos": ["B2C"]},
    {"item": "CANETA RETROPROGETOR PONTA MÉDIA PRETA", "secao": "Material", "segmentos": ["B2C"]},
    {"item": "CABO ÓPTICO, INTERNO, LOW FRICTION,1 FIBRA", "secao": "Material", "segmentos": ["B2C"]},
    {"item": "CONECTOR ÓPTICO; CAMPO; DROP COMPACTO", "secao": "Material", "segmentos": ["B2C"]},
    {"item": "PROTETOR, EMENDA; FIBRA; OPTC = 40MMXD = 1,5MM", "secao": "Material", "segmentos": ["B2C"]},
    {"item": "PROTETOR, EMENDA; FIBRA; OPTC = 60MMXD =1,0MM", "secao": "Material", "segmentos": ["B2C"]},
    {"item": "FITA ISOLANTE TPT", "secao": "Material", "segmentos": ["B2C"]},
    {"item": "FITA DE AUTO FUSÃO", "secao": "Material", "segmentos": ["B2C"]},
    {"item": "CABO ÓPTICO PRÉ-CONECTORIZADO AIRBOND MINI DROP SC APC", "secao": "Material", "segmentos": ["B2C"]},
    {"item": "CORDÃO ÓPTICO SC APC", "secao": "Material", "segmentos": ["B2C"]},
    {"item": "CINTA DE AÇO", "secao": "Material", "segmentos": ["B2B", "Redes"]},
    {"item": "ETIQUETA WI-FI LIGGA", "secao": "Material", "segmentos": ["B2C"]},
    {"item": "ESPIRAL TUBE 1/2", "secao": "Material", "segmentos": ["B2C"]},
    {"item": "FECHO DE AÇO", "secao": "Material", "segmentos": ["B2C"]},
    {"item": "FIXA FIO", "secao": "Material", "segmentos": ["B2C"]},
    {"item": "PLAQUETA DE IDENTIFICAÇÃO LIGGA", "secao": "Material", "segmentos": ["B2C"]},
    {"item": "PITÃO COM BUCHA 6 / 8 / 10 MM", "secao": "Material", "segmentos": ["B2C"]},
    {"item": "SUPORTE DROP (SDA) OU ROLDANA COMPATÍVEL", "secao": "Material", "segmentos": ["B2C"]},
    {"item": "LUBRIFICANTE, GRAXA DE SILICONE OU VASELINA SÓLIDA", "secao": "Material", "segmentos": ["B2C", "B2B", "Redes"]},
    # Uniforme
    {"item": "CRACHÁ DE IDENTIFICAÇÃO", "secao": "Uniforme", "segmentos": ["B2C", "B2B", "Redes"]},
    {"item": "CALCA ANTICHAMA COM FAIXA (NR10)", "secao": "Uniforme", "segmentos": ["B2C", "B2B", "Redes"]},
    {"item": "CAMISETA MANGA CURTA 100% USO GERAL", "secao": "Uniforme", "segmentos": ["B2C", "B2B", "Redes"]},
    {"item": "JALECO ANTICHAMA C/FAIXA MANGA LONGA", "secao": "Uniforme", "segmentos": ["B2C", "B2B", "Redes"]},
    {"item": "JAQUETA FR COM FAIXA REFLEX ANTI-CHAMA", "secao": "Uniforme", "segmentos": ["B2C", "B2B", "Redes"]},
    # Veículo
    {"item": "ESTADO DO VEÍCULO", "secao": "Veículo", "segmentos": ["B2C", "B2B", "Redes"]},
    {"item": "ESTADO DOS PNEUS", "secao": "Veículo", "segmentos": ["B2C", "B2B", "Redes"]},
    {"item": "IDENTIFICAÇÃO DO VEÍCULO", "secao": "Veículo", "segmentos": ["B2C", "B2B", "Redes"]},
    {"item": "SUPORTE DAS ESCADAS", "secao": "Veículo", "segmentos": ["B2C", "B2B", "Redes"]},
    {"item": "FAROIS DIANTEIROS", "secao": "Veículo", "segmentos": ["B2C", "B2B", "Redes"]},
    {"item": "FARÓIS TRASEIROS", "secao": "Veículo", "segmentos": ["B2C", "B2B", "Redes"]},
    {"item": "PISCA ALERTA", "secao": "Veículo", "segmentos": ["B2C", "B2B", "Redes"]},
    {"item": "CHAVE DE RODA", "secao": "Veículo", "segmentos": ["B2C", "B2B", "Redes"]},
    {"item": "MACACO", "secao": "Veículo", "segmentos": ["B2C", "B2B", "Redes"]},
]
# ... existing code ...

# Dicionário de parceiros responsáveis
parceiros_responsaveis = {}

# Carregar variáveis de ambiente
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Configuração de logging
logging.basicConfig(
    filename='bot.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Lista de administradores
ADMINS = ['alexandrecarvalho95']
ADMIN_CHAT_IDS = [] # Será preenchido quando um admin usar o bot
PENDING_REQUESTS = {} # Armazena {username: chat_id} dos pedidos pendentes
PENDING_NAME_REQUESTS = {} # Armazena {request_id: {name, chat_id, username}}
USER_NAME_MAP = {}

# Caminhos para arquivos de dados
USUARIOS_AUTORIZADOS_PATH = 'usuarios_autorizados.json'
USER_NAME_MAP_PATH = 'user_name_map.json'
PARCEIROS_RESPONSAVEIS_PATH = 'parceiros_responsaveis.json'
USUARIO_REGIONAL_PATH = 'usuario_regional.json'

# Carregar dados existentes
def carregar_dados():
    global USUARIOS_AUTORIZADOS, USER_NAME_MAP, parceiros_responsaveis
    
    # Carregar usuários autorizados
    try:
        with open(USUARIOS_AUTORIZADOS_PATH, 'r') as f:
            data = json.load(f)
            USUARIOS_AUTORIZADOS = {username: None for username in data} if isinstance(data, list) else data
    except Exception:
        USUARIOS_AUTORIZADOS = {}

    # Carregar mapeamento de nomes
    try:
        with open(USER_NAME_MAP_PATH, 'r') as f:
            USER_NAME_MAP = json.load(f)
    except Exception:
        USER_NAME_MAP = {}

    # Carregar parceiros responsáveis
    try:
        with open(PARCEIROS_RESPONSAVEIS_PATH, 'r', encoding='utf-8') as f:
            parceiros_responsaveis = json.load(f)
    except Exception:
        parceiros_responsaveis = {}

# Carregar dados ao iniciar
carregar_dados()

# Funções para salvar dados
def salvar_usuarios_autorizados():
    with open(USUARIOS_AUTORIZADOS_PATH, 'w') as f:
        json.dump(USUARIOS_AUTORIZADOS, f, indent=2)

def salvar_user_name_map():
    with open(USER_NAME_MAP_PATH, 'w') as f:
        json.dump(USER_NAME_MAP, f, indent=2)

def salvar_parceiros_responsaveis():
    with open(PARCEIROS_RESPONSAVEIS_PATH, 'w', encoding='utf-8') as f:
        json.dump(parceiros_responsaveis, f, ensure_ascii=False, indent=2)

def ler_usuario_regional():
    try:
        with open(USUARIO_REGIONAL_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def salvar_usuario_regional(mapeamento):
    with open(USUARIO_REGIONAL_PATH, 'w', encoding='utf-8') as f:
        json.dump(mapeamento, f, ensure_ascii=False, indent=2)

# Estados da conversa
(
    TIPO_FORMULARIO, NOME, TECNICO, EMPRESA, REGIONAL, DATA, DATA_EXEC_CONTRATO, CONTRATO, ID_ATIVIDADE,
    TIPO_ATIVIDADE, MOTIVACAO, INCONFORMIDADES, OBSERVACOES, CONFIRMACAO,
    FOTO_INCONFORME, CONFIRMA_FOTO_INCONFORME, PEDIR_NOME_NOVO, AREA_ATUACAO,
    SETOR_TECNICO, FOTO_FINAL_TOOLKIT,
    APROVAR_EMPRESA_NOME, APROVAR_TECNICO_NOME
) = range(22)
   
# Funções para gerenciar nomes preenchedores
def ler_nomes_preenchedores():
    try:
        with open('nomes_preenchedores.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

def salvar_nomes_preenchedores(nomes):
    with open('nomes_preenchedores.json', 'w', encoding='utf-8') as f:
        json.dump(nomes, f, ensure_ascii=False, indent=2)

# Funções para gerenciar empresas por regional
def ler_empresas_regional():
    try:
        with open('empresas_regional.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def salvar_empresas_regional(empresas_regional):
    with open('empresas_regional.json', 'w', encoding='utf-8') as f:
        json.dump(empresas_regional, f, ensure_ascii=False, indent=2)

# Funções para gerenciar técnicos por regional
def ler_tecnicos_por_regional():
    try:
        with open('tecnicos_por_regional.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def salvar_tecnicos_por_regional(tecnicos_data):
    with open('tecnicos_por_regional.json', 'w', encoding='utf-8') as f:
        json.dump(tecnicos_data, f, ensure_ascii=False, indent=2)

# Função para buscar contratos pendentes
def buscar_contratos_pendentes(regional_usuario, username=None, empresa=None):
    try:
        df = pd.read_excel('excel/relatorio_unico.xlsx', sheet_name=None)
        df_all = pd.concat(df.values(), ignore_index=True)
        if 'ID Atividade' not in df_all.columns or 'Regional' not in df_all.columns:
            return []
        df_regional = df_all[df_all['Regional'] == regional_usuario]
        if empresa and 'Empresa' in df_regional.columns:
            df_regional = df_regional[df_regional['Empresa'] == empresa]
        if username and 'parceiro_username' in df_regional.columns:
            df_regional = df_regional[df_regional['parceiro_username'] == username]
        colunas_nc = [col for col in df_regional.columns if col not in ['ID Atividade', 'Regional', 'Status', 'Contrato', 'Técnico', 'Empresa', 'Preenchedor', 'Data Fiscalização', 'Tipo', 'Data Preenchimento', 'Motivação', 'Observações', 'Data Execução Contrato', 'Tipo Atividade', 'Área de Atuação', 'Setor', 'Corrigido', 'parceiro_username']]
        df_nc = df_regional[df_regional[colunas_nc].eq('Não Conforme').any(axis=1)]
        if 'Corrigido' in df_nc.columns:
            df_nc = df_nc[df_nc['Corrigido'] != True]
        return df_nc['ID Atividade'].dropna().unique().tolist()
    except Exception as e:
        logging.error(f"Erro ao buscar contratos pendentes: {e}")
        return []

# Função para buscar itens não conformes
def buscar_itens_nao_conformes(id_atividade):
    try:
        df = pd.read_excel('excel/relatorio_unico.xlsx', sheet_name=None)
        df_all = pd.concat(df.values(), ignore_index=True)
        linha = df_all[df_all['ID Atividade'] == id_atividade]
        if linha.empty:
            return []
        linha = linha.iloc[0]
        itens_nc = [col for col in df_all.columns if linha.get(col) == 'Não Conforme']
        return itens_nc
    except Exception as e:
        logging.error(f"Erro ao buscar itens não conformes: {e}")
        return []

# Função para marcar contrato como corrigido
def marcar_contrato_corrigido(id_atividade):
    try:
        df = pd.read_excel('excel/relatorio_unico.xlsx', sheet_name=None)
        for sheet, df_sheet in df.items():
            mask = df_sheet['ID Atividade'] == id_atividade
            if mask.any():
                df_sheet.loc[mask, 'Corrigido'] = True
                df[sheet] = df_sheet
        with pd.ExcelWriter('excel/relatorio_unico.xlsx', mode='w') as writer:
            for sheet, df_sheet in df.items():
                df_sheet.to_excel(writer, sheet_name=sheet, index=False)
    except Exception as e:
        logging.error(f"Erro ao marcar contrato corrigido: {e}")

# Handler para iniciar o bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username
    nome_usuario = user.first_name or username
    username_at = f"@{username}" if not username.startswith("@") else username

    # Verificar se usuário tem username
    if not username:
        await update.message.reply_text(
            f"❌ {nome_usuario}, para usar este bot, você precisa de um nome de usuário no Telegram.\n\n"
            "Como definir seu username?\n"
            "1. Abra o Telegram e vá em Configurações.\n"
            "2. Toque em 'Editar Perfil'.\n"
            "3. Defina um nome de usuário único (exemplo: @seunome).\n\n"
            "Depois, volte aqui e digite /start novamente para pedir autorização."
        )
        return ConversationHandler.END

    # Verificar se é parceiro (só pode usar /corrigir)
    if (username in parceiros_responsaveis or username_at in parceiros_responsaveis) and username not in ADMINS:
        await update.message.reply_text(
            f"{nome_usuario}, seu perfil é de parceiro. Você só pode acessar o menu de correção de vistorias usando o comando /corrigir."
        )
        return ConversationHandler.END

    # Registrar admin
    if username in ADMINS and update.effective_chat.id not in ADMIN_CHAT_IDS:
        ADMIN_CHAT_IDS.append(update.effective_chat.id)
        logging.info(f"Admin @{username} com chat_id {update.effective_chat.id} registrado.")
        await tutorial_adm(update, context)

    # Atualizar chat_id se usuário foi pré-autorizado
    if username in USUARIOS_AUTORIZADOS and USUARIOS_AUTORIZADOS.get(username) is None:
        USUARIOS_AUTORIZADOS[username] = update.effective_chat.id
        salvar_usuarios_autorizados()
        logging.info(f"Chat ID para o usuário pré-autorizado @{username} foi atualizado.")
        await update.message.reply_text(f"✅ {nome_usuario}, seu acesso, que foi pré-autorizado por um admin, agora está ativo! Pode continuar.")
        context.user_data['tutorial_enviado'] = True
        await tutorial_usuario(update, context)

    # Se usuário não autorizado
    if username not in ADMINS and username not in USUARIOS_AUTORIZADOS:
        logging.warning(f"Acesso negado para o usuário não autorizado: @{username}")
        PENDING_REQUESTS[username] = update.effective_chat.id
        await update.message.reply_text(
            f"❌ {nome_usuario}, acesso negado. Um pedido de autorização para seu usuário (@{username}) foi enviado aos administradores.\n\n"
            "Assim que um administrador aprovar seu acesso, você receberá uma mensagem de confirmação.\n\n"
            "<b>O que fazer depois de ser autorizado?</b>\n"
            "- Assim que receber a mensagem de aprovação, digite /start ou envie qualquer mensagem aqui no bot para começar a usar.\n"
            "- Se mudar seu username no Telegram, peça autorização novamente.\n\n"
            "Se tiver dúvidas, peça ajuda ao seu administrador."
            , parse_mode='HTML'
        )
        for admin_id in ADMIN_CHAT_IDS:
            try:
                keyboard = [[InlineKeyboardButton("Autorizar", callback_data=f"autorizar_{username}"), InlineKeyboardButton("Não Autorizar", callback_data=f"negar_{username}")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await context.bot.send_message(chat_id=admin_id, text=f"🔔 Pedido de acesso do usuário: @{username}", reply_markup=reply_markup)
            except Exception as e:
                logging.error(f"Falha ao notificar admin com chat_id {admin_id}: {e}")
        return ConversationHandler.END
    
    logging.info(f"Usuário autorizado: @{username}")
    
    # Iniciar formulário
    botoes = [["Fiscalização B2C"], ["Fiscalização B2B/Redes"], ["Fiscalização Toolkit"]]
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    await asyncio.sleep(1.2)
    await update.message.reply_text(
        f"Olá, {nome_usuario}! 👋\nQue bom te ver por aqui. Por favor, selecione o tipo de vistoria que deseja realizar:",
        reply_markup=ReplyKeyboardMarkup(botoes, one_time_keyboard=True, resize_keyboard=True)
    )
    return TIPO_FORMULARIO

async def receber_tipo_formulario(update: Update, context: ContextTypes.DEFAULT_TYPE):
    resposta = update.message.text.strip()
    if resposta == "Fiscalização B2C":
        context.user_data['form_type'] = 'B2C'
    elif resposta == "Fiscalização B2B/Redes":
        context.user_data['form_type'] = 'B2B/Redes'
    elif resposta == "Fiscalização Toolkit":
        context.user_data['form_type'] = 'Toolkit'
    else:
        botoes = [["Fiscalização B2C"], ["Fiscalização B2B/Redes"], ["Fiscalização Toolkit"]]
        await update.message.reply_text(
            "Opção inválida. Por favor, selecione um tipo de vistoria.",
            reply_markup=ReplyKeyboardMarkup(botoes, one_time_keyboard=True, resize_keyboard=True)
        )
        return TIPO_FORMULARIO

    # Verificar se nome já está preenchido
    if context.user_data.get('nome'):
        username = update.effective_user.username
        regional = ler_usuario_regional().get(username)
        if not regional:
            await update.message.reply_text("Sua regional não está cadastrada. Peça para um administrador autorizar seu acesso corretamente.")
            return ConversationHandler.END
        context.user_data['regional'] = regional
        empresas = ler_empresas_regional().get(regional, [])
        if not empresas:
            await update.message.reply_text("Nenhuma empresa cadastrada para sua regional. Peça ao ADM para cadastrar.")
            return ConversationHandler.END
        botoes = [[e] for e in empresas]
        await update.message.reply_text(
            f"Selecione a empresa da sua regional ({regional}):",
            reply_markup=ReplyKeyboardMarkup(botoes, one_time_keyboard=True, resize_keyboard=True)
        )
        return EMPRESA if context.user_data['form_type'] != 'Toolkit' else 'EMPRESA_TOOLKIT'
    else:
        # Pedir nome
        nomes = ler_nomes_preenchedores()
        if nomes:
            botoes = [[nome] for nome in nomes]
            botoes.append(["Meu nome não está na lista"])
            await update.message.reply_text(
                "Por favor, selecione seu nome:",
                reply_markup=ReplyKeyboardMarkup(botoes, one_time_keyboard=True, resize_keyboard=True)
            )
            return NOME
        else:
            await update.message.reply_text("Olá! Nenhum preenchedor cadastrado. Peça a um administrador para cadastrar e depois digite /start para começar.")
            return ConversationHandler.END

async def obter_nome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nome = update.message.text.strip()

    if nome == "Meu nome não está na lista":
        await update.message.reply_text(
            "Por favor, digite seu nome completo para solicitar a inclusão:",
            reply_markup=ReplyKeyboardRemove()
        )
        return PEDIR_NOME_NOVO

    nomes = ler_nomes_preenchedores()
    if nome not in nomes:
        botoes = [[n] for n in nomes]
        botoes.append(["Meu nome não está na lista"])
        await update.message.reply_text(
            "Nome inválido. Por favor, selecione um nome da lista ou a opção para adicionar seu nome.",
            reply_markup=ReplyKeyboardMarkup(botoes, one_time_keyboard=True, resize_keyboard=True)
        )
        return NOME
    
    context.user_data['nome'] = nome
    form_type = context.user_data.get('form_type')
    
    if form_type == 'Toolkit':
        regionais = ler_empresas_regional().keys()
        botoes = [[r] for r in regionais]
        await update.message.reply_text(
            "Selecione a Regional fiscalizada:",
            reply_markup=ReplyKeyboardMarkup(botoes, one_time_keyboard=True, resize_keyboard=True)
        )
        return 'REGIONAL_TOOLKIT'
    else:
        regionais = ler_empresas_regional().keys()
        botoes = [[r] for r in regionais]
        await update.message.reply_text(
            "Selecione a Regional:",
            reply_markup=ReplyKeyboardMarkup(botoes, one_time_keyboard=True, resize_keyboard=True)
        )
        return REGIONAL

async def solicitar_inclusao_nome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    novo_nome = update.message.text.strip()
    user = update.effective_user
    username = user.username
    chat_id = update.effective_chat.id

    # Notificar admins
    request_id = str(uuid4())
    PENDING_NAME_REQUESTS[request_id] = {'name': novo_nome, 'chat_id': chat_id, 'username': username}

    for admin_id in ADMIN_CHAT_IDS:
        try:
            keyboard = [
                [InlineKeyboardButton("Adicionar Nome", callback_data=f"add_name_{request_id}"),
                InlineKeyboardButton("Ignorar", callback_data=f"ign_name_{request_id}")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.send_message(
                chat_id=admin_id,
                text=f"🔔 Pedido de inclusão de preenchedor:\n\nUsuário: @{username}\nNome Solicitado: {novo_nome}",
                reply_markup=reply_markup)
        except Exception as e:
            logging.error(f"Falha ao notificar admin {admin_id} sobre novo nome: {e}")

    await update.message.reply_text(
        "✅ Sua solicitação para adicionar o nome foi enviada aos administradores. "
        "Você será notificado quando for aprovado. Para um novo lançamento, digite /start.")
    return ConversationHandler.END

async def obter_regional(update: Update, context: ContextTypes.DEFAULT_TYPE):
    regional = update.message.text.strip()
    regionais = ler_empresas_regional().keys()
    if regional not in regionais:
        botoes = [[r] for r in regionais]
        await update.message.reply_text(
            "Regional inválida. Selecione uma das opções abaixo ou digite /start para reiniciar.",
            reply_markup=ReplyKeyboardMarkup(botoes, one_time_keyboard=True, resize_keyboard=True)
        )
        return REGIONAL
    context.user_data['regional'] = regional
    empresas = ler_empresas_regional().get(regional, [])
    if not empresas:
        await update.message.reply_text("Nenhuma empresa cadastrada para essa regional. Peça ao ADM para cadastrar.")
        return REGIONAL
    botoes = [[e] for e in empresas]
    await update.message.reply_text(
        "Selecione a empresa:",
        reply_markup=ReplyKeyboardMarkup(botoes, one_time_keyboard=True, resize_keyboard=True)
    )
    return EMPRESA if context.user_data['form_type'] != 'Toolkit' else 'EMPRESA_TOOLKIT'

async def obter_empresa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    empresa = update.message.text.strip()
    regional = context.user_data.get('regional')
    empresas_regional = ler_empresas_regional()
    empresas = empresas_regional.get(regional, [])
    
    empresa_info = None
    if empresas and isinstance(empresas[0], dict):
        for e in empresas:
            if e.get('nome') == empresa:
                empresa_info = e
                break
    else:
        empresa_info = {'nome': empresa, 'segmentos': ['B2C', 'B2B', 'Redes']}
    
    if not empresa_info:
        await update.message.reply_text("Empresa não cadastrada para sua regional. Peça ao ADM para cadastrar.")
        return EMPRESA
    
    context.user_data['empresa'] = empresa
    segmentos = empresa_info.get('segmentos', ['B2C', 'B2B', 'Redes'])
    
    # Definir setor técnico se só houver um segmento
    if len(segmentos) == 1:
        context.user_data['setor_tecnico'] = segmentos[0]
    else:
        # Perguntar segmento
        botoes = [[s] for s in segmentos]
        await update.message.reply_text(
            f"A empresa '{empresa}' atende mais de um segmento. Selecione o segmento do técnico fiscalizado:",
            reply_markup=ReplyKeyboardMarkup(botoes, one_time_keyboard=True, resize_keyboard=True)
        )
        return SETOR_TECNICO
    
    # Buscar técnicos
    tecnicos_data = ler_tecnicos_por_regional()
    tecnicos = tecnicos_data.get(regional, {}).get(empresa, [])
    if not tecnicos:
        await update.message.reply_text(
            f"Nenhum técnico cadastrado para a empresa '{empresa}' na regional '{regional}'.\n"
            f"Peça ao ADM para cadastrar usando:\n/addtecnico {regional} {empresa} NOME_DO_TECNICO")
        return EMPRESA
    
    botoes = [[t] for t in tecnicos]
    await update.message.reply_text(
        "Selecione o técnico:",
        reply_markup=ReplyKeyboardMarkup(botoes, one_time_keyboard=True, resize_keyboard=True))
    return TECNICO

async def obter_tecnico(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tecnico = update.message.text.strip()
    empresa = context.user_data.get('empresa')
    regional = context.user_data.get('regional')
    tecnicos_data = ler_tecnicos_por_regional()
    tecnicos = tecnicos_data.get(regional, {}).get(empresa, [])
    
    if tecnico not in tecnicos:
        # Solicitar aprovação ao admin
        context.user_data['tecnico_solicitante_chat_id'] = update.effective_chat.id
        context.user_data['tecnico_solicitante_nome'] = tecnico
        for admin_id in ADMIN_CHAT_IDS:
            keyboard = [
                [InlineKeyboardButton("Aprovar e Editar", callback_data=f"aprovar_tecnico_{regional}_{empresa}_{tecnico}"),
                 InlineKeyboardButton("Rejeitar", callback_data=f"rejeitar_tecnico_{regional}_{empresa}_{tecnico}")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.send_message(
                chat_id=admin_id,
                text=f"Solicitação de inclusão de técnico:\nRegional: {regional}\nEmpresa: {empresa}\nTécnico sugerido: {tecnico}",
                reply_markup=reply_markup)
        await update.message.reply_text(
            "Técnico não cadastrado. Solicitação enviada ao administrador para aprovação. Aguarde a resposta.")
        return TECNICO
    
    context.user_data['tecnico'] = tecnico
    await update.message.reply_text("Informe a data da fiscalização:")
    dias = [[str(d).zfill(2)] for d in range(1, 32)]
    await update.message.reply_text(
        "Selecione o DIA:",
        reply_markup=ReplyKeyboardMarkup(dias, one_time_keyboard=True, resize_keyboard=True))
    context.user_data['data_fiscalizacao'] = {}
    return DATA

async def obter_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip()
    
    # Se ainda não selecionou o dia
    if 'dia' not in context.user_data['data_fiscalizacao']:
        if not (texto.isdigit() and 1 <= int(texto) <= 31):
            dias = [[str(d).zfill(2)] for d in range(1, 32)]
            await update.message.reply_text(
                "Dia inválido. Selecione um dia da lista ou digite /start para reiniciar.",
                reply_markup=ReplyKeyboardMarkup(dias, one_time_keyboard=True, resize_keyboard=True))
            return DATA
        context.user_data['data_fiscalizacao']['dia'] = texto.zfill(2)
        meses = [[str(m).zfill(2)] for m in range(1, 13)]
        await update.message.reply_text(
            "Selecione o MÊS:",
            reply_markup=ReplyKeyboardMarkup(meses, one_time_keyboard=True, resize_keyboard=True))
        return DATA
    
    # Se ainda não selecionou o mês
    if 'mes' not in context.user_data['data_fiscalizacao']:
        if not (texto.isdigit() and 1 <= int(texto) <= 12):
            meses = [[str(m).zfill(2)] for m in range(1, 13)]
            await update.message.reply_text(
                "Mês inválido. Selecione um mês da lista ou digite /start para reiniciar.",
                reply_markup=ReplyKeyboardMarkup(meses, one_time_keyboard=True, resize_keyboard=True))
            return DATA
        context.user_data['data_fiscalizacao']['mes'] = texto.zfill(2)
        anos = [['2024'], ['2025']]
        await update.message.reply_text(
            "Selecione o ANO:",
            reply_markup=ReplyKeyboardMarkup(anos, one_time_keyboard=True, resize_keyboard=True))
        return DATA
    
    # Selecionou ano, monta a data
    if texto not in ['2024', '2025']:
        anos = [['2024'], ['2025']]
        await update.message.reply_text(
            "Ano inválido. Selecione um ano da lista ou digite /start para reiniciar.",
            reply_markup=ReplyKeyboardMarkup(anos, one_time_keyboard=True, resize_keyboard=True))
        return DATA
    
    context.user_data['data_fiscalizacao']['ano'] = texto
    data_fisc_str = "{dia}/{mes}/{ano}".format(**context.user_data['data_fiscalizacao'])

    try:
        data_fisc_obj = datetime.strptime(data_fisc_str, "%d/%m/%Y").date()
        if data_fisc_obj > datetime.now().date():
            await update.message.reply_text("❌ Data da fiscalização não pode ser no futuro. Por favor, insira novamente.")
            dias = [[str(d).zfill(2)] for d in range(1, 32)]
            await update.message.reply_text(
                "Selecione o DIA:",
                reply_markup=ReplyKeyboardMarkup(dias, one_time_keyboard=True, resize_keyboard=True))
            context.user_data['data_fiscalizacao'] = {}
            return DATA
    except ValueError:
        await update.message.reply_text("❌ Data inválida (ex: 31/02). Por favor, insira novamente.")
        dias = [[str(d).zfill(2)] for d in range(1, 32)]
        await update.message.reply_text(
            "Selecione o DIA:",
            reply_markup=ReplyKeyboardMarkup(dias, one_time_keyboard=True, resize_keyboard=True))
        context.user_data['data_fiscalizacao'] = {}
        return DATA

    context.user_data['data'] = data_fisc_str
    form_type = context.user_data.get('form_type')
    
    if form_type == 'Toolkit':
        await update.message.reply_text("Vamos iniciar a verificação do Toolkit.")
        return await iniciar_inconformidades(update, context)
    else:
        await update.message.reply_text("Informe a data da execução do contrato:")
        dias = [[str(d).zfill(2)] for d in range(1, 32)]
        await update.message.reply_text(
            "Selecione o DIA:",
            reply_markup=ReplyKeyboardMarkup(dias, one_time_keyboard=True, resize_keyboard=True))
        context.user_data['data_exec'] = {}
        return DATA_EXEC_CONTRATO
    
    async def iniciar_inconformidades(update: Update, context: ContextTypes.DEFAULT_TYPE):
    form_type = context.user_data.get('form_type')
    secoes_do_formulario = FORM_SECTIONS.get(form_type, {})
    
    context.user_data['secoes_restantes'] = list(secoes_do_formulario.keys())
    context.user_data['inconformes'] = {}
    context.user_data['fotos_inconformes'] = {}

    return await proxima_secao(update, context)

async def proxima_secao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data['secoes_restantes']:
        await update.message.reply_text("Todas as seções foram concluídas. Escreva as observações:")
        return OBSERVACOES

    secao_atual = context.user_data['secoes_restantes'].pop(0)
    context.user_data['secao_atual'] = secao_atual
    form_type = context.user_data.get('form_type')
    secoes_do_formulario = FORM_SECTIONS.get(form_type, {})
    itens_base = secoes_do_formulario[secao_atual].copy()

    # Filtra itens do Toolkit com base no segmento (setor_tecnico)
    if form_type == 'Toolkit':
        setor = context.user_data.get('setor_tecnico')
        itens_filtrados = [i['item'] for i in TOOLKIT_ITENS if i['secao'] == secao_atual and setor in i['segmentos']]
        if not itens_filtrados:
            return await proxima_secao(update, context)
        context.user_data['itens_restantes'] = itens_filtrados
    else:
        context.user_data['itens_restantes'] = itens_base

    botoes = [[item] for item in context.user_data['itens_restantes']]
    botoes.append(['Pular'])

    await update.message.reply_text(
        f"Seção: {secao_atual}\nSelecione os itens NÃO CONFORMES ou envie 'Pular' para pular esta seção.",
        reply_markup=ReplyKeyboardMarkup(botoes, one_time_keyboard=True, resize_keyboard=True))
    return INCONFORMIDADES

async def receber_inconformidade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    form_type = context.user_data.get('form_type')
    texto = update.message.text.strip()
    secao = context.user_data['secao_atual']

    if texto.lower() == 'pular':
        return await proxima_secao(update, context)

    if texto not in context.user_data['itens_restantes']:
        botoes = [[item] for item in context.user_data['itens_restantes']]
        botoes.append(['Pular'])
        await update.message.reply_text(
            "Por favor, selecione uma das opções disponíveis nos botões.",
            reply_markup=ReplyKeyboardMarkup(botoes, one_time_keyboard=True, resize_keyboard=True))
        return INCONFORMIDADES

    # Armazena como não conforme
    context.user_data.setdefault('inconformes', {}).setdefault(secao, []).append(texto)
    
    # Itens que NÃO precisam de foto
    itens_sem_foto_dentro_cliente = [
        'Acomodação do DROP óptico na ONT',
        'Nível de Sinal',
        'Wi-Fi Configuração',
        'Wi-Fi Cobertura',
        'Teste de velocidade'
    ]

    async def avancar_ou_repetir_item(item_registrado):
        context.user_data['itens_restantes'].remove(item_registrado)
        if context.user_data['itens_restantes']:
            botoes = [[i] for i in context.user_data['itens_restantes']]
            botoes.append(['Pular'])
            await update.message.reply_text(
                f"Item '{item_registrado}' registrado. Selecione outro ou 'Pular' para ir para a próxima seção.",
                reply_markup=ReplyKeyboardMarkup(botoes, one_time_keyboard=True, resize_keyboard=True))
            return INCONFORMIDADES
        else:
            return await proxima_secao(update, context)

    # Lógica de fluxo específica
    if form_type == 'Toolkit':
        return await avancar_ou_repetir_item(texto)
    elif form_type == 'B2C':
        # Seção Processos ou Inconformidades em atendimento técnico: nunca pede foto
        if secao in ['Processos', 'Inconformidades em atendimento técnico']:
            return await avancar_ou_repetir_item(texto)
        # Seção Dentro do ambiente do cliente, para os itens específicos: não pede foto
        elif secao == 'Dentro do ambiente do cliente' and texto in itens_sem_foto_dentro_cliente:
            return await avancar_ou_repetir_item(texto)
        # Demais casos do B2C: pede foto normalmente
        else:
            context.user_data.setdefault('fotos_inconformes', {}).setdefault(secao, {})
            context.user_data['item_inconforme_atual'] = (secao, texto)
            await update.message.reply_text(f"Envie a foto para o item '{texto}':")
            return FOTO_INCONFORME
    else: # B2B/Redes pedem foto normalmente
        context.user_data.setdefault('fotos_inconformes', {}).setdefault(secao, {})
        context.user_data['item_inconforme_atual'] = (secao, texto)
        await update.message.reply_text(f"Envie a foto para o item '{texto}':")
        return FOTO_INCONFORME

async def receber_foto_inconforme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    secao, item = context.user_data['item_inconforme_atual']
    photo = await update.message.photo[-1].get_file()
    pasta = "fotos"
    os.makedirs(pasta, exist_ok=True)
    caminho = os.path.join(pasta, f"{uuid4()}.jpg")
    await photo.download_to_drive(caminho)
    context.user_data['fotos_inconformes'][secao].setdefault(item, []).append(caminho)
    context.user_data['foto_inconforme_atual'] = caminho
    await update.message.reply_text(
        "A foto está boa?",
        reply_markup=ReplyKeyboardMarkup([["Sim"], ["Não"]], one_time_keyboard=True, resize_keyboard=True))
    return CONFIRMA_FOTO_INCONFORME

async def confirma_foto_inconforme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    resposta = update.message.text.strip()
    secao, item = context.user_data['item_inconforme_atual']

    if resposta not in ["Sim", "Não"]:
        await update.message.reply_text(
            "Resposta inválida. Selecione 'Sim' ou 'Não', ou digite /start para reiniciar.",
            reply_markup=ReplyKeyboardMarkup([["Sim"], ["Não"]], one_time_keyboard=True, resize_keyboard=True))
        return CONFIRMA_FOTO_INCONFORME

    # Remove o item atual da lista de itens restantes se ainda estiver lá
    if item in context.user_data['itens_restantes']:
        context.user_data['itens_restantes'].remove(item)

    if resposta == "Sim":
        # Se ainda há itens, segue para o próximo
        if context.user_data['itens_restantes']:
            botoes = [[i] for i in context.user_data['itens_restantes']]
            botoes.append(['Pular'])
            await update.message.reply_text(
                f"Item '{item}' registrado. Selecione outro ou envie 'Pular' para ir para a próxima seção.",
                reply_markup=ReplyKeyboardMarkup(botoes, one_time_keyboard=True, resize_keyboard=True))
            return INCONFORMIDADES
        else:
            # Vai para a próxima seção
            return await proxima_secao(update, context)
    else: # Resposta == "Não"
        # Pede a foto novamente
        await update.message.reply_text(f"Envie novamente a foto para o item '{item}':")
        return FOTO_INCONFORME

async def obter_observacoes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Se esta função foi chamada por fluxo anterior, envie a lista de inconformes e peça as observações
    if update.message and update.message.text and update.message.text.strip() != "":
        context.user_data['observacoes'] = update.message.text
        form_type = context.user_data.get('form_type')
        if form_type == 'Toolkit':
            await update.message.reply_text("Por favor, envie a foto final (técnico, uniforme, veículo e ferramental).")
            return FOTO_FINAL_TOOLKIT
        else:
            await pedir_confirmacao(update, context)
            return CONFIRMACAO
    
    # Caso contrário, envie a lista de inconformes e peça as observações
    inconformes = context.user_data.get('inconformes', {})
    if inconformes and any(inconformes.values()):
        mensagem = '<b>Itens não conformes registrados até o momento:</b>\n'
        for secao, itens in inconformes.items():
            if itens:
                mensagem += f'\n<b>{secao}:</b>'
                for item in itens:
                    mensagem += f'\n- {item}'
        await update.message.reply_text(mensagem, parse_mode='HTML')
    await update.message.reply_text("Quais as observações?")
    return OBSERVACOES

async def receber_foto_final_toolkit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = await update.message.photo[-1].get_file()
    pasta = "fotos"
    os.makedirs(pasta, exist_ok=True)
    caminho = os.path.join(pasta, f"toolkit_{uuid4()}.jpg")
    await photo.download_to_drive(caminho)
    context.user_data['foto_final'] = caminho
    await update.message.reply_text("Foto final recebida.")
    await pedir_confirmacao(update, context)
    return CONFIRMACAO

async def pedir_confirmacao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Todos os lançamentos estão corretos?\nClique em CONFIRMAR para finalizar, VOLTAR para ajustar ou /cancelar para abortar.",
        reply_markup=ReplyKeyboardMarkup([["CONFIRMAR"], ["VOLTAR"]], one_time_keyboard=True, resize_keyboard=True))
    return CONFIRMACAO

async def voltar_formulario(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Permite ao usuário voltar para a etapa de observações."""
    await update.message.reply_text("Você voltou para a etapa de observações. Por favor, insira as observações novamente:", reply_markup=ReplyKeyboardRemove())
    return OBSERVACOES

async def finalizar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dados = context.user_data
    user = update.effective_user
    nome_usuario = user.first_name or user.username

    # Validação dos campos obrigatórios
    form_type = dados.get('form_type')
    if form_type == 'B2C':
        campos_obrigatorios = ['nome', 'tecnico', 'empresa', 'regional', 'data', 'data_exec_contrato', 'contrato', 'id_atividade', 'tipo_atividade', 'motivacao']
    elif form_type == 'B2B/Redes':
        campos_obrigatorios = ['nome', 'tecnico', 'empresa', 'regional', 'data', 'data_exec_contrato', 'contrato', 'id_atividade', 'tipo_atividade', 'area_atuacao']
    else: # Toolkit
        campos_obrigatorios = ['nome', 'tecnico', 'empresa', 'regional', 'data', 'setor_tecnico', 'foto_final']

    faltando = [campo for campo in campos_obrigatorios if not dados.get(campo)]
    if faltando:
        await update.message.reply_text(
            f"❌ {nome_usuario}, os seguintes campos obrigatórios não foram preenchidos: {', '.join(faltando)}.\n"
            "Por favor, reinicie o lançamento e preencha todos os campos.")
        return ConversationHandler.END

    # Associar parceiro responsável antes de salvar
    regional = dados.get('regional')
    empresa = dados.get('empresa')
    parceiro_username = None
    for username, info in parceiros_responsaveis.items():
        if info.get('regional') == regional and info.get('empresa') == empresa:
            parceiro_username = username
            break
    dados['parceiro_username'] = parceiro_username if parceiro_username else ''
    dados['Corrigido'] = False

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    await asyncio.sleep(1.2)
    await update.message.reply_text(f"{nome_usuario}, estamos finalizando e gerando seu relatório...", reply_markup=ReplyKeyboardRemove())

    # Caminhos corretos
    os.makedirs('pdfs', exist_ok=True)
    os.makedirs('excel', exist_ok=True)

    # Usar caminhos relativos
    if form_type == 'Toolkit':
        empresa = dados.get('empresa', 'empresa').replace(' ', '_')
        tecnico = dados.get('tecnico', 'tecnico').replace(' ', '_')
        caminho_pdf = os.path.join('pdfs', f"toolkit_{empresa}_{tecnico}.pdf")
    else:
        caminho_pdf = os.path.join('pdfs', f"{dados.get('id_atividade', 'sem_id')}.pdf")
    caminho_excel = os.path.join('excel', 'relatorio_unico.xlsx')

    # Gerar o PDF e Excel
    gerar_pdf_com_logo(caminho_pdf, dados)
    gerar_excel_conforme_nao_conforme(caminho_excel, dados)
    
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    await asyncio.sleep(1.2)
    await update.message.reply_text(f"✅ Prontinho, {nome_usuario}! Seu relatório foi gerado e salvo com sucesso! Se precisar de mais alguma coisa, é só chamar! 👍")
    
    with open(caminho_pdf, 'rb') as pdf_file:
        await context.bot.send_document(chat_id=update.effective_chat.id, document=pdf_file)

    # Enviar PDF para o parceiro responsável, se houver
    if parceiro_username:
        user_key = parceiro_username[1:] if parceiro_username.startswith('@') else parceiro_username
        chat_id = USUARIOS_AUTORIZADOS.get(user_key)
        if chat_id:
            try:
                with open(caminho_pdf, 'rb') as pdf_file:
                    await context.bot.send_document(chat_id=chat_id, document=pdf_file)
            except Exception as e:
                logging.error(f"Falha ao enviar PDF para parceiro {parceiro_username}: {e}")

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    await asyncio.sleep(1.2)
    await update.message.reply_text(f"Lançamento de vistoria registrado com sucesso, {nome_usuario}! Caso deseje lançar mais, é só chamar 👍")
    return ConversationHandler.END

async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Operação cancelada.")
    return ConversationHandler.END

def gerar_pdf_com_logo(caminho_pdf, dados):
    c = canvas.Canvas(caminho_pdf, pagesize=A4)
    width, height = A4
    y = height - 50
    form_type = dados.get('form_type', 'B2C')
    
    # Título do formulário
    if form_type == 'Toolkit':
        nome_fiscalizado = dados.get('tecnico', '')
        empresa = dados.get('empresa', '')
        titulo = f"Relatório de Fiscalização Toolkit - {nome_fiscalizado} ({empresa})"
    else:
        nome = dados.get("tecnico", "")
        empresa = dados.get("empresa", "")
        titulo = f"Relatório de Fiscalização - {nome} ({empresa})"
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, titulo)
    y -= 30
    
    # Logo
    try:
        logo_path = 'logo.png'
        c.drawImage(logo_path, width - 130, y - 20, width=80, height=40, preserveAspectRatio=True, mask='auto')
    except Exception as e:
        print(f"Erro ao adicionar logo: {e}")
    
    # Informações básicas
    c.setFont("Helvetica", 12)
    y -= 20
    campos_base = [
        ('Nome', 'nome'), ('Técnico', 'tecnico'), ('Empresa', 'empresa'),
        ('Regional', 'regional'), ('Data', 'data'), ('Contrato', 'contrato'),
        ('Id_atividade', 'id_atividade'), ('Tipo_atividade', 'tipo_atividade'),
        ('Motivação', 'motivacao')
    ]
    
    if form_type == 'B2B/Redes':
        campos_base.append(('Área de Atuação', 'area_atuacao'))
    if form_type == 'Toolkit':
        campos_base = [('Nome', 'nome'), ('Técnico', 'tecnico'), ('Empresa', 'empresa'), ('Regional', 'regional'), ('Data', 'data'), ('Setor', 'setor_tecnico'), ('Motivação', 'motivacao')]
    
    for label, chave in campos_base:
        if dados.get(chave):
            c.drawString(50, y, f"{label}: {dados.get(chave, '')}")
            y -= 20
    
    y -= 10 # Espaço extra
    
    # Seções e Itens Não Conformes
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Itens Não Conformes:")
    y -= 20
    c.setFont("Helvetica", 10)
    
    if not any(dados.get('inconformes', {}).values()):
        c.drawString(55, y, "Nenhum item não conforme registrado.")
        y -= 20
    else:
        for secao, itens in dados.get('inconformes', {}).items():
            if not itens: continue
            if y < 50:
                c.showPage()
                y = height - 50
            c.setFont("Helvetica-Bold", 11)
            c.drawString(55, y, f"Seção: {secao}")
            y -= 15
            c.setFont("Helvetica", 10)
            for item in itens:
                if y < 40:
                    c.showPage()
                    y = height - 50
                c.drawString(60, y, f"- {item}")
                y -= 12
    
    y -= 10
    
    # Observações
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Observações:")
    y -= 20
    c.setFont("Helvetica", 10)
    texto_obs = dados.get('observacoes', 'Nenhuma.')
    linhas = texto_obs.split('\n')
    for linha in linhas:
        if y < 40:
            c.showPage()
            y = height - 50
        c.drawString(55, y, linha)
        y -= 12
    
    # Fotos
    if form_type == 'Toolkit' and dados.get('foto_final'):
        c.showPage()
        y = height - 100
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Foto Final da Vistoria")
        y -= 20
        try:
            c.drawImage(dados['foto_final'], 50, y-400, width=400, height=400, preserveAspectRatio=True)
        except Exception as e:
            c.drawString(50, y, f"Erro ao carregar imagem: {e}")
    elif any(dados.get('fotos_inconformes', {}).values()):
        c.showPage()
        y = height - 50
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Fotos das Não Conformidades")
        y -= 30
        for secao, itens_fotos in dados.get('fotos_inconformes', {}).items():
            for item, fotos in itens_fotos.items():
                for foto_path in fotos:
                    if y < 250:
                        c.showPage()
                        y = height - 50
                    c.setFont("Helvetica-Bold", 11)
                    c.drawString(50, y, f"Seção: {secao}")
                    y -= 15
                    c.setFont("Helvetica", 10)
                    c.drawString(50, y, f"Item: {item}")
                    y -= 210
                    try:
                        c.drawImage(foto_path, 50, y, width=200, height=200, preserveAspectRatio=True)
                    except Exception as e:
                        c.drawString(50, y, f"Erro ao carregar imagem: {e}")
                    y -= 20
    
    c.save()

def gerar_excel_conforme_nao_conforme(caminho_excel, dados):
    form_type = dados.get('form_type', 'B2C')
    if form_type == 'B2C':
        sheet_name = 'Fiscalização B2C'
    elif form_type == 'B2B/Redes':
        sheet_name = 'Fiscalização B2B-Redes'
    else: # Toolkit
        sheet_name = 'Fiscalização Toolkit'
    
    registro = {
        'Data Preenchimento': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        'Preenchedor': dados.get('nome'),
        'Técnico': dados.get('tecnico'),
        'Empresa': dados.get('empresa'),
        'Regional': dados.get('regional'),
        'Data Fiscalização': dados.get('data'),
        'Motivação': dados.get('motivacao', ''),
        'parceiro_username': dados.get('parceiro_username', ''),
        'Corrigido': False,
        'form_type': form_type
    }
    
    if form_type == 'B2C':
        registro.update({
            'Data Execução Contrato': dados.get('data_exec_contrato', ''),
            'Contrato': dados.get('contrato'),
            'ID Atividade': dados.get('id_atividade'),
            'Tipo Atividade': dados.get('tipo_atividade')
        })
    elif form_type == 'B2B/Redes':
        registro.update({
            'Data Execução Contrato': dados.get('data_exec_contrato', 'N/A'),
            'Contrato': dados.get('contrato', 'N/A'),
            'ID Atividade': dados.get('id_atividade', 'N/A'),
            'Tipo Atividade': dados.get('tipo_atividade', 'N/A'),
            'Área de Atuação': dados.get('area_atuacao', 'N/A')
        })
    elif form_type == 'Toolkit':
        registro['Setor'] = dados.get('setor_tecnico', 'N/A')
        registro['Data Execução Contrato'] = 'N/A'
        registro['Contrato'] = 'N/A'
        registro['ID Atividade'] = 'N/A'
        registro['Tipo Atividade'] = 'N/A'
        registro['Área de Atuação'] = 'N/A'
    
    registro['Observações'] = dados.get('observacoes', '')
    
    secoes_do_formulario = FORM_SECTIONS.get(form_type, {})
    
    if form_type == 'Toolkit':
        setor = dados.get('setor_tecnico')
        for secao, _ in secoes_do_formulario.items():
            secao_nc = False
            itens_secao = [i['item'] for i in TOOLKIT_ITENS if i['secao'] == secao and setor in i['segmentos']]
            itens_todos_secao = [i['item'] for i in TOOLKIT_ITENS if i['secao'] == secao]
            for item in itens_todos_secao:
                if setor in [seg for i in TOOLKIT_ITENS if i['item'] == item for seg in i['segmentos']]:
                    if secao in dados.get('inconformes', {}) and item in dados['inconformes'][secao]:
                        registro[item] = 'Não Conforme'
                        secao_nc = True
                    else:
                        registro[item] = 'Conforme'
                else:
                    registro[item] = 'N/A'
            registro[f"Status {secao}"] = 'Não Conforme' if secao_nc else 'Conforme'
    else:
        setores_todos = ['B2C', 'B2B', 'Redes']
        setor_usuario = dados.get('setor_tecnico', None)
        for secao, itens in secoes_do_formulario.items():
            secao_nc = False
            for item in itens:
                if secao in dados.get('inconformes', {}) and item in dados['inconformes'][secao]:
                    registro[item] = 'Não Conforme'
                    secao_nc = True
                else:
                    if item not in registro:
                        registro[item] = 'Conforme'
            # Preencher N/A para campos de setor/área não aplicáveis
            if form_type in ['B2C', 'B2B/Redes']:
                for setor in setores_todos:
                    if setor_usuario and setor != setor_usuario and setor in secao:
                        for item in itens:
                            if item not in registro or registro[item] == 'Conforme':
                                registro[item] = 'N/A'
            registro[f"Status {secao}"] = 'Não Conforme' if secao_nc else 'Conforme'
    
    df_novo = pd.DataFrame([registro])
    
    try:
        if os.path.exists(caminho_excel):
            with pd.ExcelWriter(caminho_excel, mode='a', if_sheet_exists='overlay') as writer:
                try:
                    df_existente = pd.read_excel(caminho_excel, sheet_name=sheet_name)
                    df_final = pd.concat([df_existente, df_novo], ignore_index=True)
                    df_final.to_excel(writer, sheet_name=sheet_name, index=False)
                except Exception:
                    df_novo.to_excel(writer, sheet_name=sheet_name, index=False)
        else:
            with pd.ExcelWriter(caminho_excel, mode='w') as writer:
                df_novo.to_excel(writer, sheet_name=sheet_name, index=False)
    except Exception as e:
        logging.error(f"Erro ao escrever no Excel: {e}")
        print(f"Erro ao salvar Excel: {e}")
        df_novo.to_excel(f"relatorio_erro_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx", index=False)

   async def autorizar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.username
    if user not in ADMINS:
        await update.message.reply_text("❌ Você não tem permissão para autorizar usuários.")
        return
    if not context.args:
        await update.message.reply_text("Informe o usuário a ser autorizado. Exemplo: /autorizar @usuario")
        return
    novo_usuario = context.args[0].lstrip('@')
    if novo_usuario in USUARIOS_AUTORIZADOS:
        await update.message.reply_text(f"⚠️ Usuário @{novo_usuario} já estava autorizado.")
        return
    context.user_data['novo_usuario_autorizado'] = novo_usuario
    # Pergunta a regional
    regionais = ler_empresas_regional().keys()
    botoes = [[r] for r in regionais]
    await update.message.reply_text(
        f"Para qual regional @{novo_usuario} pertence?",
        reply_markup=ReplyKeyboardMarkup(botoes, one_time_keyboard=True, resize_keyboard=True))
    return REGIONAL_AUTORIZACAO

async def receber_regional_autorizacao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    regional = update.message.text.strip()
    novo_usuario = context.user_data.get('novo_usuario_autorizado')
    if not novo_usuario:
        await update.message.reply_text("Erro interno. Tente novamente.")
        return ConversationHandler.END

    # Autoriza o usuário e salva a regional
    user_chat_id = PENDING_REQUESTS.get(novo_usuario)
    USUARIOS_AUTORIZADOS[novo_usuario] = user_chat_id
    salvar_usuarios_autorizados()
    mapeamento = ler_usuario_regional()
    mapeamento[novo_usuario] = regional
    salvar_usuario_regional(mapeamento)
    await update.message.reply_text(f"✅ Usuário @{novo_usuario} foi autorizado para a regional {regional}.")
    
    # Notifica o usuário que foi aprovado
    if novo_usuario in PENDING_REQUESTS:
        user_chat_id = PENDING_REQUESTS.pop(novo_usuario)
        try:
            await context.bot.send_message(
                chat_id=user_chat_id,
                text="✅ Seu acesso foi autorizado! Digite /start ou envie qualquer mensagem para começar a usar o bot.\n\n"
                     "<b>O que você pode fazer:</b>\n"
                     "- Preencher vistorias de fiscalização.\n"
                     "- Corrigir relatórios de não conformidade (se for parceiro).\n"
                     "- Consultar comandos disponíveis com /list.\n\n"
                     "Se tiver dúvidas, envie /list para ver todos os comandos.",
                parse_mode='HTML')
        except Exception as e:
            logging.error(f"Falha ao notificar usuário @{novo_usuario} sobre aprovação: {e}")
    
    context.user_data.pop('novo_usuario_autorizado', None)
    return ConversationHandler.END

async def remover_autorizacao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.username
    if user not in ADMINS:
        await update.message.reply_text("❌ Você não tem permissão para cancelar usuários.")
        return
    if not context.args:
        await update.message.reply_text("Informe o usuário a ser removido. Exemplo: /removerautorizacao @usuario")
        return
    usuario_remover = context.args[0].lstrip('@')
    if usuario_remover in USUARIOS_AUTORIZADOS:
        chat_id_remover = USUARIOS_AUTORIZADOS.pop(usuario_remover)
        salvar_usuarios_autorizados()
        # Remove o nome do preenchedor associado, se houver
        nome_preenchedor = USER_NAME_MAP.pop(usuario_remover, None)
        if nome_preenchedor:
            nomes = ler_nomes_preenchedores()
            if nome_preenchedor in nomes:
                nomes.remove(nome_preenchedor)
                salvar_nomes_preenchedores(nomes)
            salvar_user_name_map()
            await update.message.reply_text(f"✅ Acesso do usuário @{usuario_remover} e seu nome de preenchedor '{nome_preenchedor}' foram removidos.")
        else:
            await update.message.reply_text(f"✅ Acesso do usuário @{usuario_remover} foi removido.")
        # Notifica o usuário removido, se tivermos o chat_id
        if chat_id_remover:
            try:
                await context.bot.send_message(
                    chat_id=chat_id_remover,
                    text="❌ Seu acesso ao bot foi removido por um administrador.")
            except Exception as e:
                logging.error(f"Falha ao notificar usuário @{usuario_remover} sobre remoção: {e}")
    else:
        await update.message.reply_text("⚠️ Usuário não encontrado na lista de autorizados.")

async def add_preenchedor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.username
    if user not in ADMINS:
        await update.message.reply_text("❌ Você não tem permissão para adicionar preenchedores.")
        return
    if not context.args:
        await update.message.reply_text("Uso: /addpreenchedor NOME COMPLETO")
        return
    nome_preenchedor = " ".join(context.args)
    nomes = ler_nomes_preenchedores()
    if nome_preenchedor in nomes:
        await update.message.reply_text(f"Preenchedor '{nome_preenchedor}' já cadastrado.")
        return
    nomes.append(nome_preenchedor)
    salvar_nomes_preenchedores(nomes)
    await update.message.reply_text(f"✅ Preenchedor '{nome_preenchedor}' adicionado com sucesso.")

async def remove_preenchedor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.username
    if user not in ADMINS:
        await update.message.reply_text("❌ Você não tem permissão para remover preenchedores.")
        return
    if not context.args:
        await update.message.reply_text("Uso: /removepreenchedor NOME COMPLETO")
        return
    nome_preenchedor = " ".join(context.args)
    nomes = ler_nomes_preenchedores()
    if nome_preenchedor not in nomes:
        await update.message.reply_text(f"Preenchedor '{nome_preenchedor}' não encontrado.")
        return
    nomes.remove(nome_preenchedor)
    salvar_nomes_preenchedores(nomes)
    await update.message.reply_text(f"✅ Preenchedor '{nome_preenchedor}' removido com sucesso.")

async def add_empresa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.username
    if user not in ADMINS:
        await update.message.reply_text("❌ Você não tem permissão para adicionar empresas.")
        return
    if len(context.args) < 2:
        await update.message.reply_text("Uso: /addempresa REGIONAL NOME_DA_EMPRESA")
        return
    regional = context.args[0].upper()
    nome_empresa = " ".join(context.args[1:])
    empresas_regional = ler_empresas_regional()
    if regional not in empresas_regional:
        empresas_regional[regional] = []
    if nome_empresa in empresas_regional[regional]:
        await update.message.reply_text(f"Empresa '{nome_empresa}' já cadastrada na regional {regional}.")
        return
    empresas_regional[regional].append(nome_empresa)
    salvar_empresas_regional(empresas_regional)
    await update.message.reply_text(f"✅ Empresa '{nome_empresa}' adicionada à regional {regional}.")

async def remove_empresa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.username
    if user not in ADMINS:
        await update.message.reply_text("❌ Você não tem permissão para remover empresas.")
        return
    if len(context.args) < 2:
        await update.message.reply_text("Uso: /removeempresa REGIONAL NOME_DA_EMPRESA")
        return
    regional = context.args[0].upper()
    nome_empresa = " ".join(context.args[1:])
    empresas_regional = ler_empresas_regional()
    if regional not in empresas_regional or nome_empresa not in empresas_regional[regional]:
        await update.message.reply_text(f"Empresa '{nome_empresa}' não encontrada na regional {regional}.")
        return
    empresas_regional[regional].remove(nome_empresa)
    salvar_empresas_regional(empresas_regional)
    await update.message.reply_text(f"✅ Empresa '{nome_empresa}' removida da regional {regional}.")

async def add_tecnico(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.username
    if user not in ADMINS:
        await update.message.reply_text("❌ Você não tem permissão para adicionar técnicos.")
        return
    if len(context.args) < 3:
        await update.message.reply_text("Uso: /addtecnico REGIONAL NOME_DA_EMPRESA NOME_COMPLETO_TECNICO")
        return
    regional = context.args[0].upper()
    nome_empresa = context.args[1]
    nome_tecnico = " ".join(context.args[2:])
    tecnicos_data = ler_tecnicos_por_regional()
    if regional not in tecnicos_data:
        tecnicos_data[regional] = {}
    if nome_empresa not in tecnicos_data[regional]:
        tecnicos_data[regional][nome_empresa] = []
    if nome_tecnico in tecnicos_data[regional][nome_empresa]:
        await update.message.reply_text(f"Técnico '{nome_tecnico}' já cadastrado para a empresa '{nome_empresa}' na regional {regional}.")
        return
    tecnicos_data[regional][nome_empresa].append(nome_tecnico)
    salvar_tecnicos_por_regional(tecnicos_data)
    await update.message.reply_text(f"✅ Técnico '{nome_tecnico}' adicionado à empresa '{nome_empresa}' na regional {regional}.")

async def remove_tecnico(update:     

# Definir o estado para a regional (caso não esteja definido)
REGIONAL_AUTORIZACAO = 1000

# ConversationHandler para o fluxo de autorização
conv_autorizar_handler = ConversationHandler(
    entry_points=[CommandHandler('autorizar', autorizar)],
    states={
        REGIONAL_AUTORIZACAO: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_regional_autorizacao)]
    },
    fallbacks=[CommandHandler('cancelar', cancelar)]
)
application.add_handler(conv_autorizar_handler)

# Remover qualquer CommandHandler simples de '/autorizar' (se existir)
# application.add_handler(CommandHandler('autorizar', autorizar))
