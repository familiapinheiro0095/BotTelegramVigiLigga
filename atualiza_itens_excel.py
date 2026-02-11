import pandas as pd

# FORM_SECTIONS extraído automaticamente do bot.py (trecho resumido)
FORM_SECTIONS = {
    'B2C': {
        'Inconformidades em rede externa': ['Identificação no DROP', 'Identificação da NAP/DIO', 'Reserva técnica DROP', 'Fechamento da NAP', 'Vedação da NAP'],
        'Equipagem de poste externo': ['Equipagem do poste Concessionária', 'Esticador']
    },
    'Toolkit': {
        'EPI': ['BOTINA DE SEGURANÇA C/ CA ATIVO', 'CAPACETE COM ABA TOTAL E JUGULAR (CLASSE B)', 'PERNEIRA COURO', 'COLETE REFLETIVO']
    }
}

# Cria um Excel com uma aba para cada formulário, cada aba com colunas: Seção, Item

def sanitize_sheet_name(name):
    return name.replace('/', '-').replace('\\', '-').replace(':', '-').replace('?', '').replace('*', '').replace('[', '').replace(']', '')[:31]

with pd.ExcelWriter('itens_formularios.xlsx', engine='openpyxl') as writer:
    for form, secoes in FORM_SECTIONS.items():
        sheet_name = sanitize_sheet_name(form)
        for c in ['/', '\\', ':', '?', '*', '[', ']']:
            sheet_name = sheet_name.replace(c, ' ')
        sheet_name = sheet_name[:31]
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
