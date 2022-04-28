from flask import Flask, jsonify
import json

servico = Flask(__name__)

ENDERECOS_ESTATICOS = "enderecos.json"

def carregar_enderecos():
    carregado, enderecos = False, None
    try:
        with open(ENDERECOS_ESTATICOS, "r") as arquivos_enderecos:
            enderecos = json.load(arquivos_enderecos)
            arquivos_enderecos.close()

            carregado = True
    except:
        # vai para log de erro
        pass

    return carregado, enderecos

@servico.route("/executar/<int:id_produto>/<string:modalidade>/<int:localizador>/")
def executar(id_produto, modalidade, localizador):
    resultado, mensagem = "erro", "endereço não encontrado"

    carregado, enderecos = carregar_enderecos()
    if carregado:
        enderecos_da_modalidade = enderecos[modalidade]
        for endereco in enderecos_da_modalidade:
            if endereco["localizador"] == localizador:
                resultado, mensagem = "sucesso", "enviando produto com id "+id_produto + " para o endereço " + endereco["endereco"]+ ", "+ endereco["numero"]+ ", " +endereco["cep"]+ ", "+ endereco["cidade"]
            break

    return jsonify(
        resultado = resultado,
        mensagem = mensagem
    )


if __name__ == "__main__":
    servico.run(
        host = "0.0.0.0",
        port = "5003",
        debug = True
    )

