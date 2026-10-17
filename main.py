from chromadb import PersistentClient
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction


DOCUMENTOS = [
    ("esp-01", "No futebol, duas equipes tentam marcar gols conduzindo a bola com os pés.",
     {"categoria": "modalidade", "tipo": "coletivo"}),

    ("esp-02", "No basquete, os jogadores somam pontos ao lançar a bola dentro da cesta adversária.",
     {"categoria": "modalidade", "tipo": "coletivo"}),

    ("esp-03", "No vôlei, cada equipe procura fazer a bola tocar o chão da quadra adversária por cima da rede.",
     {"categoria": "modalidade", "tipo": "coletivo"}),

    ("esp-04", "Na natação, os atletas percorrem uma piscina usando estilos como crawl, costas, peito e borboleta.",
     {"categoria": "modalidade", "tipo": "aquatico"}),

    ("esp-05", "No atletismo, provas de corrida, salto e arremesso medem velocidade, distância ou altura.",
     {"categoria": "modalidade", "tipo": "individual"}),

    ("esp-06", "No tênis, os participantes usam raquetes para rebater a bola sobre uma rede.",
     {"categoria": "modalidade", "tipo": "raquete"}),

    ("esp-07", "No ciclismo, o competidor pedala uma bicicleta em percursos de estrada ou pista.",
     {"categoria": "modalidade", "tipo": "individual"}),

    ("esp-08", "No judô, o praticante busca projetar ou imobilizar o adversário no tatame.",
     {"categoria": "modalidade", "tipo": "luta"}),

    ("esp-09", "O aquecimento prepara músculos e articulações antes do exercício e ajuda a reduzir lesões.",
     {"categoria": "treinamento", "tipo": "preparacao"}),

    ("esp-10", "A hidratação repõe a água perdida pelo suor durante a atividade física.",
     {"categoria": "saude", "tipo": "hidratacao"}),

    ("esp-11", "O descanso entre treinos permite a recuperação muscular e evita sobrecarga.",
     {"categoria": "treinamento", "tipo": "recuperacao"}),

    ("esp-12", "A corrida de longa distância exige resistência e controle do ritmo ao longo do percurso.",
     {"categoria": "treinamento", "tipo": "resistencia"}),
]

PERGUNTAS = [
    "Em qual esporte se fazem pontos acertando um alvo elevado?",
    "Como se chama a modalidade com provas de crawl e borboleta?",
    "Qual a importância da recuperação muscular entre treinos?",
]

PERGUNTA_SEM_PALAVRAS_IGUAIS = "Qual esporte utiliza uma bike em competições?"


embedding_fn = SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

client = PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="esportes",
    embedding_function=embedding_fn
)

# upsert evita duplicar documentos quando o arquivo é executado novamente.
collection.upsert(
    ids=[documento[0] for documento in DOCUMENTOS],
    documents=[documento[1] for documento in DOCUMENTOS],
    metadatas=[documento[2] for documento in DOCUMENTOS]
)

print("Documentos armazenados:", collection.count())

for numero, pergunta in enumerate(PERGUNTAS, start=1):
    resultado = collection.query(
        query_texts=[pergunta],
        n_results=3,
        include=["documents", "metadatas", "distances"]
    )

    print(f"\nConsulta {numero}: {pergunta}")
    for i in range(len(resultado["ids"][0])):
        print("ID:", resultado["ids"][0][i])
        print("Documento:", resultado["documents"][0][i])
        print("Metadata:", resultado["metadatas"][0][i])
        print("Distância:", resultado["distances"][0][i])
        print()

resultado_filtrado = collection.query(
    query_texts=[PERGUNTAS[2]],
    n_results=3,
    where={"categoria": "treinamento"},
    include=["documents", "metadatas", "distances"]
)

print("\nBusca filtrada na categoria 'treinamento':")
for i in range(len(resultado_filtrado["ids"][0])):
    print("ID:", resultado_filtrado["ids"][0][i])
    print("Documento:", resultado_filtrado["documents"][0][i])
    print("Metadata:", resultado_filtrado["metadatas"][0][i])
    print("Distância:", resultado_filtrado["distances"][0][i])
    print()

resultado_semantico = collection.query(
    query_texts=[PERGUNTA_SEM_PALAVRAS_IGUAIS],
    n_results=3,
    include=["documents", "metadatas", "distances"]
)

print("\nPergunta com palavras diferentes:", PERGUNTA_SEM_PALAVRAS_IGUAIS)
for i in range(len(resultado_semantico["ids"][0])):
    print("ID:", resultado_semantico["ids"][0][i])
    print("Documento:", resultado_semantico["documents"][0][i])
    print("Metadata:", resultado_semantico["metadatas"][0][i])
    print("Distância:", resultado_semantico["distances"][0][i])
    print()
