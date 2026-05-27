import firebase_admin
from firebase_admin import credentials, firestore

# 1. Inicializa o Firebase
try:
    cred = credentials.Certificate("serviceAccountKey.json")
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    print("✅ Firebase inicializado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao ler serviceAccountKey.json: {e}")
    exit()

db = firestore.client()

# Dados brutos dos filmes para alimentar o laço do seed
mock_api_response = [
    { 'title': 'John Wick 4', 'temp_cat_id': 1, 'poster_path': 'https://image.tmdb.org/t/p/w500/vZloFAK7NmvMGKE7VkF5UHaz0I.jpg', 'trailer': 'https://www.youtube.com/watch?v=yjRHZEUamCc' },
    { 'title': 'Mad Max: Estrada da Fúria', 'temp_cat_id': 1, 'poster_path': 'https://image.tmdb.org/t/p/w500/8tZYtuWezp8JbcsvHYO0O46tFbo.jpg', 'trailer': 'https://www.youtube.com/watch?v=hEJnMQG9ev8' },
    { 'title': '007: Sem Tempo para Morrer', 'temp_cat_id': 1, 'poster_path': 'https://image.tmdb.org/t/p/w500/i9rEpT8C3w76jnX3647Yg9w2P6w.jpg', 'trailer': 'https://www.youtube.com/watch?v=A9bAepYiDRI' },
    
    { 'title': 'As Branquelas', 'temp_cat_id': 2, 'poster_path': 'https://image.tmdb.org/t/p/w500/aHTUpo45qy9QYIOnVITGGqLoVcA.jpg', 'trailer': 'https://www.youtube.com/watch?v=SEOewMc_scU' },
    { 'title': 'Avatar 2', 'temp_cat_id': 2, 'poster_path': 'https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg', 'trailer': 'https://www.youtube.com/watch?v=x5pZI-DmtrE' },
    
    { 'title': 'À Procura da Felicidade', 'temp_cat_id': 3, 'poster_path': 'https://image.tmdb.org/t/p/w500/lBYOKAMcxIvuk9s9hMuecB9dPBV.jpg', 'trailer': 'https://www.youtube.com/watch?v=DMOBlEcRuw8' },
    { 'title': 'O Pianista', 'temp_cat_id': 3, 'poster_path': 'https://image.tmdb.org/t/p/w500/2hFvxCCWrTmCYwfy7yum0GKRi3Y.jpg', 'trailer': 'https://www.youtube.com/watch?v=cZp9SgN7Hrc' },
    
    { 'title': 'Duna: Parte 2', 'temp_cat_id': 4, 'poster_path': 'https://image.tmdb.org/t/p/w500/1pdfLvkbY9ohJlCjQH2CZjjYVvJ.jpg', 'trailer': 'https://www.youtube.com/watch?v=U2Qp5pL3ovA' },
    { 'title': 'Interestelar', 'temp_cat_id': 4, 'poster_path': 'https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg', 'trailer': 'https://www.youtube.com/watch?v=frD_IiY_fIE' },
    { 'title': 'Devoradores de Estrelas', 'temp_cat_id': 4, 'poster_path': 'https://image.tmdb.org/t/p/w500/4D7D7R3PmsbC6F57e7X07VvEwhG.jpg', 'trailer': 'https://www.youtube.com/watch?v=8tIwN7wUPgc' },
    
    { 'title': 'Invocação do Mal', 'temp_cat_id': 5, 'poster_path': 'https://image.tmdb.org/t/p/w500/wVYREutTvI2tmxr6ujrHT704wGF.jpg', 'trailer': 'https://www.youtube.com/watch?v=k10ETZ42qBh' },
    { 'title': 'Hereditário', 'temp_cat_id': 5, 'poster_path': 'https://image.tmdb.org/t/p/w500/4GFPuL14eXi66V96xBWY73Y9PfR.jpg', 'trailer': 'https://www.youtube.com/watch?v=V6wWKNij_vM' },
    
    { 'title': 'Nosso Planeta', 'temp_cat_id': 6, 'poster_path': 'https://image.tmdb.org/t/p/w500/ovDgO2LPfwdVRfvScAqo9aMiIW.jpg', 'trailer': 'https://www.youtube.com/watch?v=aETNYyrqNYE' },
]

categories_to_create = {
    1: "Ação",
    2: "Comédia",
    3: "Drama",
    4: "Ficção Científica",
    5: "Terror",
    6: "Documentário"
}

def seed_database():
    print("🚀 Iniciando a estruturação do banco de dados (Firebase)...")
    
    # PASSO 1: Criar as Categorias e capturar os IDs alfanuméricos gerados
    generated_category_ids = {}
    cat_collection = db.collection("categories")
    
    for temp_id, title in categories_to_create.items():
        doc_ref = cat_collection.document()
        cat_data = {"id": doc_ref.id, "title": title}
        doc_ref.set(cat_data)
        generated_category_ids[temp_id] = doc_ref.id
        print(f"📁 Categoria criada: {title} (ID Firebase: {doc_ref.id})")

    print("-" * 40)

    # PASSO 2: Criar os Filmes mapeados conforme as chaves exatas do seu MovieCreate
    movie_batch = db.batch()
    movie_collection = db.collection("movies")

    for movie in mock_api_response:
        doc_ref = movie_collection.document()
        real_category_firebase_id = generated_category_ids.get(movie["temp_cat_id"])
        
        # Estrutura idêntica ao seu Pydantic Model e ao banco de dados
        movie_data = {
            "id": doc_ref.id,                                   # Injetado para o MovieResponse
            "title": movie["title"],
            "description": f"Sinopse oficial do filme {movie['title']}, pronto para exibição na plataforma.",
            "category_ids": [real_category_firebase_id],        # Atende: List[str]
            "price": 29.90,                                     # Atende: gt=0
            "year": "2023",
            "duration": "1h 30min",
            "image_url": movie["poster_path"],                  # Atende: Optional[str]
            "url_movie": movie["trailer"]                       # Atende: url_movie string
        }
        
        movie_batch.set(doc_ref, movie_data)
        print(f"🎬 Preparando filme: {movie['title']}")

    # PASSO 3: Executar a transação em lote (batch) no Firebase
    movie_batch.commit()
    print(f"\n🎉 Sucesso! Banco populado em perfeita sincronia com o seu Schema!")

if __name__ == "__main__":
    seed_database()