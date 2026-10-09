from typing import Protocol

class Embedder(Protocol):
    def embed(self, text:str) -> list[float]:
        ...
class DemoEmbedder:
    def embed(self,text:str)-> list[float]:
        return [float(len(text)),float(len(text.split())) ] 
class FixedEmbedder:
    def embed(self,text:str)->list[float]:
        return[0.1,0.2,0.3]
def prepare_vector(text:str,embedder:Embedder)->list[float]:
    return embedder.embed(text)
def prepare_documents(
        texts: list[str],
        embedder: Embedder,) -> list[list[float]]:
    return[prepare_vector(text,embedder) for text in texts]
                     
def main()-> None:
    embedder=DemoEmbedder()
    vector=prepare_vector("Merhaba dünya",embedder)
    print(vector)
    
    fixed_embedder=FixedEmbedder()
    fixed_vector=prepare_vector("Merhaba dünya",fixed_embedder)
    print(fixed_vector)
    documents=["Merhaba dünya","private LLM sistemi"]

    vectors=prepare_documents(documents,DemoEmbedder())
    print(vectors)
    
    fixed_vectors= prepare_documents(documents,FixedEmbedder())
    print(fixed_vectors)

if __name__ == "__main__":
    main()