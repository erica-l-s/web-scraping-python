import pandas as pd
import requests
from bs4 import BeautifulSoup

# URL base que carrega os dados via AJAX
base_url = 'https://www.yourfirm.de/suche/all/?fulltext=Softwareentwickler%2Fin&sort=Datum&page={}'

# Cabeçalhos para evitar bloqueio por User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'
}

# Defina as palavras-chave que você deseja procurar no título
palavras_chave = ["C++"]

# Lista para armazenar as vagas
dados_vagas = []

# Loop para percorrer as requisições AJAX (simulando rolagem)
for page in range(1, 10):  # Pode ajustar a quantidade de páginas carregadas
    # Faz a requisição simulando a "rolagem"
    url = base_url.format(page)
    response = requests.get(url, headers=headers)

    # Caso o site retorne dados em HTML
    soup = BeautifulSoup(response.content, 'html.parser')
 

    
    # Encontrar todas as vagas
    vagas = soup.find_all('div', class_='sc-b2039713-27')  # Ajuste de acordo com a estrutura HTML correta

    if not vagas:
        print("Nenhuma vaga encontrada, interrompendo.")
        break
    
    
    # Loop para extrair informações de cada vaga
    for vaga in vagas:
        # Extrair título, empresa, etc.
        link_tag = vaga.find('a')
        titulo = link_tag['title'] if link_tag and 'title' in link_tag.attrs else 'Título não encontrado'
        local = vaga.find('div', class_='sc-b2039713-16').get_text(strip=True) if vaga.find('div', class_='sc-b2039713-16') else 'Local não encontrado'
        empresa = vaga.find('p', class_='sc-b2039713-8').get_text(strip=True) if vaga.find('p', class_='sc-b2039713-8') else 'Empresa não encontrada'
        link = vaga.find('a')['href'] if vaga.find('a') else 'Link não encontrado'
        
              
        # Verificar se o título contém alguma das palavras-chave
        if any(palavra in titulo for palavra in palavras_chave):
            
            # Adicionar os dados da vaga à lista
            dados_vagas.append({
                'Título': titulo,
                'Local': local,
                'Empresa': empresa,
                'Link': f'https://www.yourfirm.de{link}'
            })
            # Exibir resultado apenas se o título contém as palavras-chave
            print(f'Título: {titulo}')
            print(f'Local: {local}')
            print(f'Empresa: {empresa}')
            print(f'Link: https://www.yourfirm.de{link}')
            print('-' * 40)
    
# Criar um DataFrame do pandas a partir da lista de dados
df_vagas = pd.DataFrame(dados_vagas)
# Exportar o DataFrame para um arquivo Excel
excel_file = 'vagas_encontradas.xlsx'

df_vagas.to_excel(excel_file, index=False)

print(f'Dados exportados com sucesso para {excel_file}.')
            
    