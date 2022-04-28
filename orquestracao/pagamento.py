from flask import Flask, jsonify
import json

servico = Flask(__name__)

CARTOES_ESTATICO = "cartoes.json"

def carregar_cartoes():
    carregado, cartoes = False, None
    try:
        with open(CARTOES_ESTATICO, "r") as arquivo_cartoes:
            cartoes = json.load(arquivo_cartoes)
            arquivo_cartoes.close()

            carregado = True
    except:
        # vai para log de erro
        pass

    return carregado, cartoes

@servico.route("/executar/<string:bandeira>/<string:numero>/<string:validade>/<int:codigo>/<float:total>/")
def executar(bandeira, numero, validade, codigo, total):
    resultado, mensagem = "Erro" , "Cartão Inválido"

    carregado, cartoes = carregar_cartoes()
    if carregado:
        cartoes_da_bandeira = cartoes[bandeira]
        for cartao in cartoes_da_bandeira:
            if cartao["numero"] == numero and cartao["validade"] == validade and cartao["codigo"] == codigo:
            resultado, mensagem = "sucesso", "pagamento confirmado"

            break

    return jsonify(
        resultado = resultado,
        mensagem = mensagem,
        total = total
        )

if __name__ == "__main__":
    servico.run(
        host = "0.0.0.0",
        port = "5002",
        debug = True
    )
