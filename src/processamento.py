import pandas as pd
import os
from src.utils import carregar_dados, padronizar_colunas

def processar_base_precificacao(caminho_cotacoes, caminho_sf):
    df_cotacoes = padronizar_colunas(carregar_dados(caminho_cotacoes,2))
    df_sf = padronizar_colunas(carregar_dados(caminho_sf,0))
    
    # une dataframes
    df_final = pd.merge(df_cotacoes, 
                        df_sf[['ID_da_Cotação_do_SAP', 'Frete_Comercial', 'Chapa']], 
                        on='ID_da_Cotação_do_SAP', 
                        how='left')
    
    # Aplicando Regras de Negócio
    df_final = df_final.sort_values(by='Dt_Criação_Sol')
    df_final['chave'] = (df_final['Código_do_Cliente'].astype(str) + "_" + 
                         df_final['Material'].astype(str) + "_" + 
                         df_final['Cód_Expedição'].astype(str))
    
    filtro = df_final[
        (df_final['Status_da_Cotação'] == 'Aprovada') & 
        (df_final['TipoCotação'].isin(['Banda', 'Preço Fixo']))
    ].copy()
    
    
    resultado = filtro.groupby('chave').rolling('30D', on='Dt_Criação_Sol', closed='left')
    df_metricas = resultado.agg({
        'ID_da_Cotação_do_SAP': 'count',
        'Var_Preço_Proposto': 'sum'
    })
    df_metricas.columns = ['Qtd_30d', 'Soma_Var_30d']
    
    df_final = pd.merge(df_final, df_metricas, on='chave', how='left')
    
    df_final = df_final.drop(columns=['chave'])
    return df_final.fillna(0)

#Salva o dataframe processado na pasta data/trusted
def salvar_processado(df, nome_arquivo='base_final_tratada.csv'):
    caminho_destino = f'data/trusted/{nome_arquivo}'
    
    # Garante que a pasta exista antes de salvar
    os.makedirs('data/trusted', exist_ok=True)
    
    df.to_csv(caminho_destino, index=False)
    print(f"Arquivo salvo com sucesso em: {caminho_destino}")

if __name__ == "__main__":
    # Teste rápido
    df = processar_base_precificacao('data/raw/COTAÇÕES - CASE.xlsx', 
                                     'data/raw/SalesForce - CASE.xlsx')
    print("Processamento concluído com sucesso!")
    print(df.head())