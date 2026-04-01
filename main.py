import os
from  typing import List  
from dotenv import load_dotenv
import boto3

load_dotenv()

# Credenciais AWS
AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION: str = os.getenv("AWS_REGION")
BUCKET_NAME: str = os.getenv("BUCKET_NAME")

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

def ler_arquivos_pasta(pasta_local: str) -> List[str]:
    
    # lista de arquivos na pasta local
    arquivos: List[str] = []

    # List todos os arquivos na pasta local e adiciona à lista de arquivos
    for arquivo in os.listdir(pasta_local):
        caminho_completo = os.path.join(pasta_local, arquivo)
        arquivos.append(caminho_completo)
    return arquivos     

def fazer_upload_s3(arquivos: List[str]) -> None:
    for arquivo_com_caminho in arquivos:
        nome_arquivo_s3 = os.path.basename(arquivo_com_caminho)
        s3_client.upload_file(arquivo_com_caminho, BUCKET_NAME, nome_arquivo_s3)
        print(f"Arquivo {nome_arquivo_s3} enviado para o bucket {BUCKET_NAME} com sucesso.")

def delete_arquivos_locais(arquivos: List[str]) -> None:
    for arquivo in arquivos:
        os.remove(arquivo)
        print(f"Arquivo {arquivo} deletado localmente com sucesso.")        

def executar_backup(PASTA_LOCAL: str) -> None:

    lista_arquivos: List[str] = []
    
    lista_arquivos = ler_arquivos_pasta(PASTA_LOCAL)

    if lista_arquivos:
        fazer_upload_s3(lista_arquivos)
        delete_arquivos_locais(lista_arquivos)
    else:
        print("Nenhum arquivo encontrado na pasta local para backup.")


def main():
    PASTA_LOCAL: str = os.getenv("PASTA_LOCAL")

    executar_backup(PASTA_LOCAL)


if __name__ == "__main__":
    main()
