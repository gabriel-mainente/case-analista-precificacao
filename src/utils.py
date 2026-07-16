import pandas as pd

# Lê arquivos CSV e trata potenciais erros de carregamento
def carregar_dados(caminho_arquivo,header_linha):
    try:
        df = pd.read_excel(caminho_arquivo, engine='openpyxl', header = header_linha)
        
        
        return df
    except Exception as e:
        print(f"Erro ao carregar {caminho_arquivo}: {e}")
        return None

#Padroniza nomes de colunas e tipos de dados em uma única passagem
def padronizar_colunas(df):
    
    # Limpeza dos nomes das colunas
    df.columns = (df.columns.str.replace(' ', '_')
                  .str.replace('.', '', regex=False)
                  .str.replace('*', '', regex=False)
                  .str.strip())
    
    # Conversão de datas (Tratamento para quando a data é lida como texto ou erro)
    # errors = 'coerce' transforma dados inválidos em NaT
    if 'Dt_Criação_Sol' in df.columns:
        df['Dt_Criação_Sol'] = pd.to_datetime(df['Dt_Criação_Sol'], dayfirst=True, errors='coerce')
    
    # Garantir que as chaves de merge sejam sempre string sem casas decimais
    colunas_chave = ['ID_da_Cotação_do_SAP', 'Cód_Expedição', 'Material']
    for col in colunas_chave:
        if col in df.columns:
            # Converte para string, remove '.0' se existir e remove espaços
            df[col] = df[col].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
            
    return df