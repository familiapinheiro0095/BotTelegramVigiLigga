from openpyxl import Workbook
import pandas as pd

# Listas auxiliares do Toolkit (copiadas do bot.py)
TOOLKIT_EPI_B2B = ['LUVA ALTA TENSÃO ORION 2,5KV 500V + LUVA DE COBERTURA', 'PERNEIRA COURO', 'COLETE REFLETIVO']
TOOLKIT_FERRAMENTAL_B2C = ['MÁQUINA DE FUSÃO (ALINHAMENTO PELA CASCA)', 'EXTENSÃO ELÉTRICA EM CABO PP - 10A (20 METROS)', 'FURADEIRA ELÉTRICA', 'CANETA LASER', 'DECAPADOR DE CABO', 'CANETA P/ LIMPEZA CONECTOR DE FIBRA 2,5mm SC/ST/FC', 'CANETA P/ LIMPEZA CONECTOR DE FIBRA LC/PC 1.25mm', 'ALICATE CRIMPADOR', 'BROCA CURTA PARA CONCRETO', 'BROCA CURTA PARA FERRO', 'BROCA CURTA PARA MADEIRA', 'BROCA LONGA PARA CONCRETO', 'BROCA LONGA PARA MADEIRA', 'TESTADOR DE CABO UTP/RJ45/RJ11', 'IDENTIFICADOR DE FIBRA ATIVA', 'PINCEL LARGO 102MM', 'KIT LIMPEZA DOMÉSTICA (VASSOURA E PÁ)']
TOOLKIT_FERRAMENTAL_B2B_REDES = ['MÁQUINA DE FUSÃO (ALINHAMENTO PELO NÚCLEO)', 'DETECTOR DE TENSÃO ALTA/BAIXA', 'DECAPADOR DE CABO CIRCULAR LONGITUDINAL', 'OTDR FIBRA ATIVA 39 DB (EQUIPES DE REDE E B2B)', 'MEDIDOR DE DISTÂNCIA', 'ROLETADOR DE TUBO LOOSE', 'ROLETADOR DE CABO', 'FACÃO 12 POLEGADAS', 'LAMPADA PORTATIL / NOTURNO', 'LATERNA HOLOFOTE LONGO ALCANCE', 'KIT MESA E CADEIRA PARA FOSC/FIST', 'LANTERNA DE SINALIZAÇÃO', 'MICROSCÓPIO (FIBER INSPECTION PROBE)', 'TALHA ALAVANCA DE 3M 3TON', 'FOICE', 'TENDA', 'MAÇARICO BICO PORTATIL GÁS MAPP', 'GUARDA SOL']
TOOLKIT_MATERIAL_B2B_REDES = ['ALCOOL ISOPROPILICO', 'CINTA DE AÇO']
TOOLKIT_MATERIAL_B2C = ['ESTICADOR', 'ETIQUETA DE IDENTIFICAÇÃO DE CABO ÓPTICO', 'FITA HELLERMAN', 'GABARITO', 'CANETA RETROPROGETOR PONTA MÉDIA PRETA', 'CABO ÓPTICO', 'INTERNO LOW FRICTION;1 FIBRA', 'CONECTOR ÓPTICO CAMPO; DROP COMPACTO', 'PROTETOR EMENDA FIBRA OPTC 40MMXD 1,5MM', 'PROTETOR EMENDA FIBRA OPTC 60MMXD 1,0MM', 'FITA ISOLANTE – TPT', 'FITA DE AUTO FUSÃO', 'CABO ÓPTICO PRÉ-CONECTORIZADO AIRBOND MINI DROP SC APC', 'CORDÃO ÓPTICO SC APC', 'CINTA DE AÇO', 'ETIQUETA WI-FI LIGGA', 'ESPIRAL TUBE 1/2', 'FECHO DE AÇO', 'FIXA FIO', 'PLAQUETA DE IDENTIFICAÇÃO LIGGA', 'PITÃO COM BUCHA 6 / 8 / 10 MM', 'SUPORTE DROP (SDA) OU ROLDANA COMPATÍVEL', 'LUBRIFICANTE', 'GRAXA DE SILICONE OU VASELINA SÓLIDA']

UNIFORME_TOOLKIT = [
    'CALCA ANTICHAMA COM FAIXA (NR10)',
    'CAMISETA MANGA CURTA 100% USO GERAL',
    'JALECO ANTICHAMA C/FAIXA MANGA LONGA',
    'JAQUETA FR COM FAIXA REFLEX ANTI-CHAMA'
]
VEICULO_TOOLKIT = [
    'ESTADO DO VEÍCULO',
    'ESTADO DOS PNEUS',
    'IDENTIFICAÇÃO DO VEÍCULO',
    'SUPORTE DAS ESCADAS',
    'FAROIS DIANTEIROS',
    'FARÓIS TRASEIROS',
    'PISCA ALERTA',
    'CHAVE DE RODA',
    'MACACO'
]
# Estrutura dos formulários extraída de FORM_SECTIONS
FORM_SECTIONS = {
    'B2C': {
        'Inconformidades em rede externa': ['Identificação no DROP', 'Identificação da NAP/DIO', 'Reserva técnica DROP', 'Fechamento da NAP', 'Vedação da NAP'],
        'Equipagem de poste externo': ['Equipagem do poste Concessionária', 'Esticador'],
        'Trajeto - DROP - Externo': ['Altura do DROP', 'Proximidade com a rede elétrica', 'Passagem do DROP Externo', 'Equipagem do poste cliente', 'Plaqueta Ligga', 'Reutilização de DROP', 'Emendas no DROP', 'Atenuação da fibra', 'Ponto de fixação no beiral/fachada'],
        'Dentro do ambiente do cliente': ['Acomodação do DROP óptico na ONT', 'Nível de Sinal', 'Passagem do DROP interno', 'Wi-Fi Configuração', 'Wi-Fi etiqueta', 'Wi-Fi Cobertura', 'Teste de velocidade', 'Bucha de acabamento'],
        'Processos': ['Lançamento de materiais no WFM', 'DESCONEXÃO DE OUTRAS OPERADORAS', 'TV OU INTERFONE', 'PARALIZAÇÃO DE OUTROS CLIENTES LIGGA', 'DESCUMPRIMENTO DE ACORDO EM ATA', 'CANCELAMENTO CHURN', 'ENDEREÇO DA INSTALAÇÃO', 'NÃO HABILITAR O GPS DO SMARTPHONE', 'NÃO ABERTURA DE BOLETIM DE OCORRENCIA EM CASOS DE VANDALISMO', 'FOTOS NO WFM', 'CUMPRIMENTO DE AGENDA', 'CÓDIGO DE BAIXA UTILIZADO', 'PENDENCIAMENTO REALIZADO CORRETAMENTE?'],
        'Monitoria': ['LIMPEZA DO CONECTOR DA ONT', 'CLIENTE ORIENTADO SOBRE O DEFEITO', 'USO INCORRETO DE FERRAMENTAL/MATERIAL', 'CONFIRMAÇÃO DO PRODUTO', 'CRACHÁ', 'IDENTIFICAÇÃO DO VEÍCULO', 'UNIFORME', 'ADORNOS', 'ATENDIMENTO AO CLIENTE', 'PRO-PÉ', 'EPI E EPC - USO', 'EPI E EPC - ESTADO DE CONSERVAÇÃO'],
        'Inconformidades em atendimento técnico': ['WI-FI EXPLICAÇÃO REDES 2.4 E 5.8 GHz', 'APP LIGGA E FOLDER BOAS VINDAS', 'DIVULGAÇÃO DE TELEFONES', 'ORGANIZAÇÃO E LIMPEZA']
    },
    'B2B/Redes': {
        'Instalação e Rede Externa - Rede Óptica': ['Identificação do cliente', 'Identificação da caixa FOSC', 'Organização da FOSC', 'Caixa correta de acordo com projeto', 'Sobra técnica em FOSC (Externa)'],
        'Equipagem do Poste - Externo': ['Equipagem do Poste Concessionária', 'Ancoragem Poste Concessionária', 'Organização (Raquete)', 'Plaqueta de identificação', 'Espinamento'],
        'Trajeto - Cabo Cliente - Externo': ['Altura do Cabo', 'Proximidade Rede Elétrica', 'Trajeto até o poste do cliente', 'Equipagem do Poste Cliente', 'Plaqueta de identificação Poste Padrão', 'Metragem correta com Projeto', 'Rota do Cabo segue o Projeto', 'Enviado AS-Built'],
        'Dentro do Ambiente do Cliente - Linha de Assinante - Rede Óptica': ['Acomodação da PTO do Cliente', 'Níveis de sinal dentro do Padrão Ligga', 'Organização Rede Interna(Bucha de Vedação)', 'EDD Configurado e testado', 'Etiqueta com Contrato'],
        'Processos': ['Não acompanhamento de troca de poste', 'Não cumprimento de Notificação recebida de Órgãos Públicos ou Companhias de Energia', 'Não realização ou comprovação da Manutenção Preventiva conforme meta mensal', 'Não correção de nível de sinal óptico de enlaces de clientes GPON conforme meta mensal', 'Não entrega de atualização de cadastro de caixas de emenda conforme meta mensal', 'Manutenção assumida pela CONTRATANTE que tenha transcorrido 50% do tempo previsto no SLA e a CONTRATADA não tenha iniciado a atividade em campo ou um serviço não seja executado no prazo ou na data agendada sem uma justificativa aceita', 'Manutenção provisória não transformada em definitiva dentro do prazo de 10 dias.', 'Falta de identificação (crachá/veículo/uniforme)', 'Uniforme de funcionário da Contratada sujo, rasgado ou em mal estado de conservação', 'Não entrega ou falhas em AS-BUILT', 'Não utilização dos equipamentos de segurança individual ou coletivo (EPI / EPC)', 'Falta de identificação na caixa NAP ou caixa de emenda', 'Utilização de equipamentos ópticos (máquina de fusão, OTDR, Power Meter) descalibrados ou fora do período da validade da aferição', 'Veículo em mau estado de conservação', 'Equipes sem o ferramental ou equipamentos ópticos (máquina de fusão, OTDR, Power Meter) necessários para o atendimento de eventos de manutenção', 'Não preenchimento ou atualização das informações referentes ao controle, consumo e inventário de materiais disponibilizado pela CONTRATANTEm', 'Lançamento de materiais no WFM']
    },
    'Toolkit': {
        'EPC': ['CONE SINALIZADOR REFLETIVO (PADRAO COPEL 5unid)', 'BANDEIRA DE SINALIZAÇÃO (ESCADAS) - BANDEIROLA', 'FITA ZEBRADA'],
        'EPI': ['BOTINA DE SEGURANÇA C/ CA ATIVO', 'CAPACETE COM ABA TOTAL E JUGULAR (CLASSE B)', 'CAPA DE CHUVA - CONJUNTO JAQUETA E CALÇA - COM REFLETIVO', 'MOSQUETÃO', 'CINTO DE SEGURANÇA TIPO PARAQUEDISTA - 4 PONTOS', 'TALABARTE DE SEGURANÇA DE POSICIONAMENTO AJUSTAVEL', 'TALABARTE DE SEGURANÇA Y', 'LUVA MULTITATO PU', 'LUVA SEG COURO VAQUETA', 'LUVA ALTA TENSÃO ORION 2,5KV 500V + LUVA DE COBERTURA', 'CANETA DETECTORA DE TENSÃO - SONORA', 'LANTERNA DE CABEÇA (LED)', 'ÓCULOS DE SEGURANÇA (Incolor ou fumê)', 'DEGRAU NIVELADOR DE ESCADA', 'PLATAFORMA PARA ESCADA', 'MANTA P/ ISOLAÇÃO C/ VELCRO', 'PROTETOR SOLAR (< QUE FATOR 30)', 'CORDA 12MM 16 METROS', 'CINTA C/ CATRATA DE AMARRAÇÃO DE ESCADA', 'ESCADA DE FIBRA EXTENSIVA 7,2M', 'ESCADA INDOOR ARTICULADA 8 DEGRAUS', 'PERNEIRA COURO', 'COLETE REFLETIVO'],
        'Instalação e Rede Externa - Rede Óptica': ['Identificação do cliente', 'Identificação da caixa FOSC', 'Organização da FOSC', 'Caixa correta de acordo com projeto', 'Sobra técnica em FOSC (Externa)'],
        'Equipagem do Poste - Externo': ['Equipagem do Poste Concessionária', 'Ancoragem Poste Concessionária', 'Organização (Raquete)', 'Plaqueta de identificação', 'Espinamento'],
        'Trajeto - Cabo Cliente - Externo': ['Altura do Cabo', 'Proximidade Rede Elétrica', 'Trajeto até o poste do cliente', 'Equipagem do Poste Cliente', 'Plaqueta de identificação Poste Padrão', 'Metragem correta com Projeto', 'Rota do Cabo segue o Projeto', 'Enviado AS-Built'],
        'Dentro do Ambiente do Cliente - Linha de Assinante - Rede Óptica': ['Acomodação da PTO do Cliente', 'Níveis de sinal dentro do Padrão Ligga', 'Organização Rede Interna(Bucha de Vedação)', 'EDD Configurado e testado', 'Etiqueta com Contrato'],
        'Processos': ['Não acompanhamento de troca de poste', 'Não cumprimento de Notificação recebida de Órgãos Públicos ou Companhias de Energia', 'Não realização ou comprovação da Manutenção Preventiva conforme meta mensal', 'Não correção de nível de sinal óptico de enlaces de clientes GPON conforme meta mensal', 'Não entrega de atualização de cadastro de caixas de emenda conforme meta mensal', 'Manutenção assumida pela CONTRATANTE que tenha transcorrido 50% do tempo previsto no SLA e a CONTRATADA não tenha iniciado a atividade em campo ou um serviço não seja executado no prazo ou na data agendada sem uma justificativa aceita', 'Manutenção provisória não transformada em definitiva dentro do prazo de 10 dias.', 'Falta de identificação (crachá/veículo/uniforme)', 'Uniforme de funcionário da Contratada sujo, rasgado ou em mal estado de conservação', 'Não entrega ou falhas em AS-BUILT', 'Não utilização dos equipamentos de segurança individual ou coletivo (EPI / EPC)', 'Falta de identificação na caixa NAP ou caixa de emenda', 'Utilização de equipamentos ópticos (máquina de fusão, OTDR, Power Meter) descalibrados ou fora do período da validade da aferição', 'Veículo em mau estado de conservação', 'Equipes sem o ferramental ou equipamentos ópticos (máquina de fusão, OTDR, Power Meter) necessários para o atendimento de eventos de manutenção', 'Não preenchimento ou atualização das informações referentes ao controle, consumo e inventário de materiais disponibilizado pela CONTRATANTEm', 'Lançamento de materiais no WFM']
    }
}

# Remove caracteres inválidos dos nomes das abas
import pandas as pd

def sanitize_sheet_name(name):
    for c in ['/', '\\', ':', '?', '*', '[', ']']:
        name = name.replace(c, ' ')
    return name[:31]

with pd.ExcelWriter('itens_formularios.xlsx', engine='openpyxl') as writer:
    for form, secoes in FORM_SECTIONS.items():
        sheet_name = sanitize_sheet_name(form)
        rows = []
        for secao, itens in secoes.items():
            for item in itens:
                rows.append({'Seção': secao, 'Item': item})
        df = pd.DataFrame(rows)
        try:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
        except Exception as e:
            print(f'Erro ao criar aba {sheet_name}: {e}')

print('Arquivo itens_formularios.xlsx atualizado.')
