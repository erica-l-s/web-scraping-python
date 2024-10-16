import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

# Base URL que será preenchida com a palavra-chave dinamicamente
base_url = 'https://www.yourfirm.de/suche/all/?fulltext={}&sort=Datum&page={}'

# Cabeçalhos para evitar bloqueio por User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'
}

# Defina as palavras-chave que você deseja procurar no título
palavras_chave = ["backend"]

# Lista para armazenar todas as vagas de todas as palavras-chave
dados_vagas = []

# Loop para cada palavra-chave
for palavra in palavras_chave:
    # Substitui espaços por '+' na palavra-chave e codifica para uso na URL
    palavra_formatada = palavra.replace(" ", "+")
    palavra_codificada = quote(palavra_formatada)
    
    # Loop para percorrer as requisições AJAX (simulando rolagem)
    for page in range(1, 10):  # Pode ajustar a quantidade de páginas carregadas
        # Faz a requisição simulando a "rolagem" com a palavra-chave codificada
        url = base_url.format(palavra_codificada, page)
        response = requests.get(url, headers=headers)

        # Caso o site retorne dados em HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Encontrar todas as vagas
        vagas = soup.find_all('div', class_='sc-b2039713-27')  # Ajuste de acordo com a estrutura HTML correta

        if not vagas:
            print(f"Nenhuma vaga encontrada para a palavra '{palavra}', interrompendo a busca nesta página.")
            break

        # Loop para extrair informações de cada vaga
        for vaga in vagas:
            # Extrair título, empresa, etc.
            link_tag = vaga.find('a')
            titulo = vaga.find('h2', class_='sc-b2039713-22').get_text(strip=True) if vaga.find('h2', class_='sc-b2039713-22') else 'Título não encontrado'
            local = vaga.find('div', class_='sc-b2039713-16').get_text(strip=True) if vaga.find('div', class_='sc-b2039713-16') else 'Local não encontrado'
            empresa = vaga.find('p', class_='sc-b2039713-8').get_text(strip=True) if vaga.find('p', class_='sc-b2039713-8') else 'Empresa não encontrada'
            data = vaga.find('p', class_='sc-b2039713-10').get_text(strip=True) if vaga.find('p', class_='sc-b2039713-10') else 'Data não encontrada'
            link = vaga.find('a')['href'] if vaga.find('a') else 'Link não encontrado'

            # Verificar se a palavra-chave está no título
            if palavra.lower() in titulo.lower():  # Ignora maiúsculas e minúsculas
                # Adicionar os dados da vaga à lista
                dados_vagas.append({
                    'Keyword': palavra,
                    'Title': titulo,
                    'Location': local,
                    'Company': empresa,
                    'Date': data,
                    'Link': f'https://www.yourfirm.de{link}'
                })

                # Exibir resultado
                print(f'Keyword: {palavra}')
                print(f'Title: {titulo}')
                print(f'Location: {local}')
                print(f'Company: {empresa}')
                print(f'Date: {data}')
                print(f'Link: https://www.yourfirm.de{link}')
                print('-' * 40)

# Criar um DataFrame do pandas a partir da lista de dados após a coleta de todas as vagas
df_vagas = pd.DataFrame(dados_vagas)

# Exportar o DataFrame para um arquivo Excel
excel_file = 'backend_vagas.xlsx'
df_vagas.to_excel(excel_file, index=False)

print(f'Dados exportados com sucesso para {excel_file}.')

