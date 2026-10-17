# Busca semântica de esportes com ChromaDB

Projeto em Python para a atividade de busca semântica.  
Usa 12 documentos sobre modalidades esportivas, treinamento e saúde.  
Cada registro tem ID, texto e metadados `categoria` e `tipo`.  
O ChromaDB salva a coleção na pasta `chroma_db` do projeto.

## Executar no PyCharm

1. Abra **esta pasta** (`busca_semantica_esportes`) como projeto no PyCharm.
2. Configure um interpretador Python 3.12 ou mais recente, de preferência em um ambiente virtual novo.
3. No terminal do PyCharm, instale as dependências:

   ```powershell
   pip install chromadb sentence-transformers
   python -m pip install -r requirements.txt
   ```

4. Abra `main.py` e clique em **Run** ou execute no terminal:

   ```powershell
   python main.py
   ```

   No PyCharm, mantenha **Working directory** apontando para a pasta `busca_semantica_esportes`. Assim, `path="chroma_db"` usa o banco correto.

5. Depois de `main.py`, execute `banco_esporte.py` para ver a dimensão de um embedding e `ver_banco_esporte.py` para inspecionar todos os registros.

Na primeira execução, `sentence-transformers` pode baixar o modelo `all-MiniLM-L6-v2`; é necessária conexão com a internet apenas nesse momento.  
Depois o modelo fica no cache local.  
Não é preciso iniciar um servidor ChromaDB.  
Execute novamente sem receio: `upsert` atualiza os mesmos 12 IDs.

## Estrutura

- `main.py`: cria/atualiza a coleção e faz as consultas.
- `banco_esporte.py`: mostra os embeddings da coleção e a dimensão de um deles.
- `ver_banco_esporte.py`: lista IDs, documentos, metadados e início dos embeddings.
- `chroma_db/`: banco persistido, criado por `main.py` e incluído no ZIP.

Os três arquivos seguem a forma direta:
- configuração do modelo;
- Acesso à coleção e 
- Comandos de consulta no corpo do script.

## O que a saída demonstra

- `collection.count()` mostra o total de registros.
- `banco.py` usa `collection.get(..., include=["embeddings"])` e `len(...)` para mostrar as dimensões.
- Três perguntas mostram os três documentos mais próximos, com ID, texto, metadados e distância.
- Distância menor indica maior proximidade no espaço vetorial.
- Uma consulta usa `where={"categoria": "treinamento"}`.
- A pergunta "Qual esporte utiliza uma bike em competições?" busca o documento sobre ciclismo mesmo usando palavras diferentes.

Os resultados aparecem no console do PyCharm ao executar `main.py`. 
Uma cópia da saída verificada está em `resultados.txt`.

## Por que um banco vetorial consegue encontrar um documento relevante mesmo quando a pergunta não contém exatamente as mesmas palavras do documento armazenado?

O modelo transforma o texto do documento e a pergunta em **embeddings**, ou seja, vetores numéricos.  
Textos de significados parecidos tendem a ocupar regiões próximas nesse espaço, mesmo quando usam palavras diferentes.  
O ChromaDB compara a distância entre o vetor da pergunta e os vetores armazenados e retorna os documentos mais próximos.  
Assim, a busca considera relações de sentido em vez de depender apenas da coincidência literal de palavras.  
A qualidade dos resultados depende do modelo de embeddings e dos textos cadastrados.
