from flask import Flask, jsonify
import json

servico = Flask(__name__)

ESTOQUE_ESTATICO = "estoque.json"

def carregar_estoque():
    carregado, estoque = False, None
    try:
        with open(ESTOQUE_ESTATICO, "r") as arquivo_estoque:
            estoque = json.load(arquivo_estoque)
            arquivo_estoque.close()

            carregado = True
    except:
        # vai para log de erro
        pass

    return carregado, estoque

@servico.route("/executar/<string:categoria>/<int:id_produto>/<int:quantidade>/")
def executar(categoria, id_produto, quantidade):
    resultado, mensagem = "erro", "produto não encontrado"
    carrinho = {
        "produto": None,
        "total": 0.0
    }

    carregado,estoque = carregar_estoque()
    if carregado:
        estoque_categoria = estoque[categoria]
        for produto in estoque_categoria:
            if id_produto == produto["id"]:
                if quantidade <= produto["quantidade"]:
                    resultado,mensagem = "sucesso", "produto em estoque"
                    carrinho = {
                        "produto":produto["descricao"],
                        "total":quantidade* produto["preco"]
                    }
                else:
                    mensagem = "quantidade indisponivel"
                    
                break
            
    return jsonify(
        resultado = resultado,
        mensagem = mensagem,
        carrinho = carrinho
        )

if __name__ == "__main__":
servico.run(
    host = 0.0.0.0,
    port = "5001",
    debug = True
    )