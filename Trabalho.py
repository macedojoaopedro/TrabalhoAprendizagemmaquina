# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Perguntar o caminho do arquivo
caminho_arquivo = input("Digite o caminho do arquivo (CSV): ")

# Carregar dados
if caminho_arquivo.endswith('.csv'):
    dados = pd.read_csv(caminho_arquivo)
else:
    print("Formato de arquivo não suportado. Use CSV.")
    exit()

# Resumo Estatístico
print("\nResumo Estatístico:")
print(f"Quantidade de dados carregados: {dados.shape[0]}")
print(f"Quantidade de homens: {(dados['Gender'] == 'Male').sum()}")
print(f"Quantidade de mulheres: {(dados['Gender'] == 'Female').sum()}")
print(f"Registros sem informação sobre educação dos pais: {dados['Parent_Education_Level'].isna().sum()}")

# Mostrar os nomes de acordo com o gênero
print("\nNomes dos homens:")
print(dados[dados['Gender'] == 'Male']['First_Name'].to_list())

print("\nNomes das mulheres:")
print(dados[dados['Gender'] == 'Female']['First_Name'].to_list())

# Limpeza de Dados
dados = dados.dropna(subset=['Parent_Education_Level'])  # Remove onde escolaridade dos pais é nulo
mediana_presenca = dados['Attendance (%)'].median()
dados['Attendance (%)'] = dados['Attendance (%)'].fillna(mediana_presenca)

print("\nDados após limpeza:")
print(f"Nova quantidade de dados: {dados.shape[0]}")
print(f"Somatório de presença: {dados['Attendance (%)'].sum():.2f}")

# Consulta de dados
coluna = input("\nDigite o nome da coluna que deseja analisar (ex: Sleep_Hours_per_Night, Final_Score, Midterm_Score, Age): ")

if coluna in dados.columns:
    media = dados[coluna].mean()
    mediana = dados[coluna].median()
    moda = dados[coluna].mode()[0]
    desvio_padrao = dados[coluna].std()

    print(f"\nAnálise da coluna '{coluna}':")
    print(f"Média: {media:.2f}")
    print(f"Mediana: {mediana:.2f}")
    print(f"Moda: {moda}")
    print(f"Desvio Padrão: {desvio_padrao:.2f}")
else:
    print("Coluna inválida.")

# Gráficos
# 1. Dispersão: Sleep Hours per Night x Final Score
plt.figure(figsize=(8, 6))
sns.scatterplot(data=dados, x='Sleep_Hours_per_Night', y='Final_Score')
plt.title('Horas de Sono x Nota Final')
plt.xlabel('Horas de Sono por Noite')
plt.ylabel('Nota Final')
plt.grid(True)
plt.show()

# 2. Gráfico de barras: Idade x Média das Notas Intermediárias
plt.figure(figsize=(8, 6))
media_notas_idade = dados.groupby('Age')['Midterm_Score'].mean()
media_notas_idade.plot(kind='bar', color='skyblue')
plt.title('Idade x Média das Notas Intermediárias')
plt.xlabel('Idade')
plt.ylabel('Média das Notas Intermediárias')
plt.grid(True)
plt.show()

# 3. Gráfico de pizza para idades agrupadas
def categorizar_idade(idade):
    if idade <= 17:
        return 'Até 17'
    elif 18 <= idade <= 21:
        return '18 a 21'
    elif 22 <= idade <= 24:
        return '22 a 24'
    else:
        return '25 ou mais'

dados['Faixa_Etaria'] = dados['Age'].apply(categorizar_idade)
faixa_etaria_contagem = dados['Faixa_Etaria'].value_counts()

plt.figure(figsize=(7, 7))
faixa_etaria_contagem.plot.pie(autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
plt.title('Distribuição de Idades')
plt.ylabel('')
plt.show()
