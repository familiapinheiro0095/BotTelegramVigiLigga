import pandas as pd
import json

# Caminho do arquivo Excel exportado da tabela
CAMINHO_EXCEL = 'itens_toolkit.xlsx'  # Altere para o nome correto do seu arquivo

# Lê o Excel e monta o dicionário TOOLKIT_SECTIONS

def montar_toolkit_sections_do_excel(caminho_excel):
    df = pd.read_excel(caminho_excel)
    df = df.fillna('')
    toolkit = {}
    for _, row in df.iterrows():
        secao = str(row.get('Seção', '')).strip()
        item = str(row.get('Itens', '')).strip()
        segmentos_raw = row.get('Segmento', '')
        segmentos = []
        if pd.notna(segmentos_raw):
            try:
                segmentos = [s.strip() for s in str(segmentos_raw).split(',') if s.strip()]
            except Exception:
                segmentos = []
        if not secao or not item or not segmentos:
            continue
        if secao not in toolkit:
            toolkit[secao] = []
        toolkit[secao].append({
            'item': item,
            'segmento': segmentos
        })
    return toolkit

if __name__ == '__main__':
    toolkit_dict = montar_toolkit_sections_do_excel(CAMINHO_EXCEL)
    # Salva como JSON para facilitar importação no bot
    with open('toolkit_sections.json', 'w', encoding='utf-8') as f:
        json.dump(toolkit_dict, f, ensure_ascii=False, indent=2)
    print('toolkit_sections.json gerado com sucesso!')
