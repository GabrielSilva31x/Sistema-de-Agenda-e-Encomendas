from datetime import datetime, timezone, timedelta
from urllib.parse import quote_plus
from Consultas import *
import random
import bcrypt
import re

class Controles():
    # O Controle cria um acesso para a classe de consultas.
    def __init__(self):
        self.consulta = ConsultaSQL()
    
    # Verifica as credenciais, pegando a entrada e comparando com oq foi consultado no banco de dados.
    def Verificação_de_Credenciais(self, tel, senha):
        try:
            # Formata e valida o telefone enviado pelo usuário
            respost_tel = self.Trata_Telefone(tel)

            # Se o telefone for inválido, interrompe o login e retorna o motivo do erro.
            if respost_tel["valido"] == False:
                return {"sucesso": False, "erro": respost_tel["erro"]}

            # Guarda o telefone já formatado e limpo.
            tel_cliente = respost_tel["texto_formatado"]

            # Busca no banco de dados as contas vinculadas a esse telefone.
            BDs = self.consulta.Login_Select_Contas(tel_cliente)

            # Se a busca no banco voltar vazia, avisa que o usuário não existe.
            if not BDs:
                return {"sucesso": False, "erro": "Usuário não encontrado!"}

            # Pega os dados do primeiro usuário encontrado na lista.
            usuario = BDs[0]
            # Recupera a senha criptografada (hash) que está salva no banco.
            hash_senha = usuario["senha"]
            # Converte a senha digitada e o hash do banco para bytes (exigência do bcrypt).
            senha_bytes = senha.encode('utf-8')
            hash_bytes = hash_senha.encode('utf-8')

            # Verifica se a senha digitada bate com a senha criptografada do banco.
            if bcrypt.checkpw(senha_bytes, hash_bytes):
                # Se estiver correta, faz o login e retorna o nome e telefone do cliente.
                return {"sucesso": True, "nome_cliente": usuario['nome'], "telefone_cliente": usuario['tel_cliente']}
            else: # Se a senha não bater, bloqueia o acesso e avisa
                return {"sucesso": False, "erro": "Senha incorreta!"}
                        
        # Captura qualquer falha e retorna a descrição do erro técnico.
        except Exception as erro:
            return {"sucesso": False, "erro": str(erro)}
                       
    # Tratador das entrada de dados do usuario para cadastro no BDs.
    def Controle_Dados_Cadastros(self, nome_entrada, tel_entrada, senha_entrada):
        try:
            # Formata e valida o telefone enviado pelo usuário.
            respost_tel = self.Trata_Telefone(tel_entrada)

            # Se o telefone for inválido, interrompe o login e retorna o motivo do erro.
            if respost_tel["valido"] == False:
                return {"sucesso": False, "erro": respost_tel["erro"]}

            # Guarda o telefone já formatado e limpo.
            tel_cliente = respost_tel["texto_formatado"]

            # Validações do tamanho da senha (máximo de 6 e mínimo de 4 caracteres).
            if len(senha_entrada) > 6:
                return f"Maxímo é de 6 digitos!"
            elif len(senha_entrada) < 4:
                return f"Minimo é de 4 digitos!"

            # Converte a senha para bytes, gera um "salt" e cria o hash criptografado
            senha_bytes = senha_entrada.encode('utf-8')
            salt = bcrypt.gensalt()
            hash = bcrypt.hashpw(senha_bytes, salt)

            # Transforma o hash de volta para texto para poder salvar no banco.
            senha_client = hash.decode('utf-8')

            # Envia os dados tratados (nome, telefone e senha protegida) para o banco de dados.
            self.consulta.Cadastro_Insert(nome_entrada, tel_cliente, senha_client)
            # Retorna que o cadastro foi um sucesso
            return {"sucesso": True, "erro": None}
            
        
        # Captura qualquer falha e retorna a descrição do erro técnico.
        except Exception as erro:
            return {"sucesso": False, "erro": str(erro)}
                       
    # Função que trata a senha nova e atualiza no BDs, caso o usuário tenha esquecido.
    def Atualizador_de_Senha(self, tel_client):
        try:
            # Formata e valida o telefone enviado pelo usuário
            respost_tel = self.Trata_Telefone(tel_client)

            # Se o telefone for inválido, interrompe o login e retorna o motivo do erro.
            if respost_tel["valido"] == False:
                return {"sucesso": False, "erro": respost_tel["erro"]}

            # Guarda o telefone já formatado e limpo.
            tel_cliente = respost_tel["texto_formatado"]

            # Consultar contato no BDs para validação.
            dados = self.consulta.Login_Select_Contas(tel_cliente)
            

            # Gerar uma senha de 6 digitos aleatorios para substituir a senha antiga.
            codigo = str(random.randint(100000, 999999))
            print(f"senha: {codigo}")
        
            # Converte a nova senha em hash
            senha_bytes = codigo.encode('utf-8')
            salt = bcrypt.gensalt()
            hash = bcrypt.hashpw(senha_bytes, salt)
            senha_nova = hash.decode('utf-8')

            # atualizar no BDs.
            self.consulta.Atualizar_Senha_Login(tel_cliente, senha_nova)

            # Apontando para o inicio da lista antes de percorre lá.
            usuario = dados[0]

            # Redirecionar a nova senha para o usuario via whatsApp com Mensagem por meio do N8N.
            Msg_puro = f"Olá, {usuario['nome']}. Essa é sua nova senha para acessar nosso site. \nNão a compartilhe com mais ninguém. \nNova senha: {codigo}."
            Msg_format = quote_plus(Msg_puro)
        
            url_final = f"https://wa.me/{usuario['tel_cliente']}?text={Msg_format}"
            return {"sucesso": True, "erro": None, "url": url_final}
        
        # Captura qualquer falha e retorna a descrição do erro técnico.
        except Exception as erro:
            return {"sucesso": False, "erro": str(erro)}
                      
    # Vai Fazer o controle de exibição correta de produtos nos slots da vitrine no site.    
    def Controle_Vitrine_Produtos(self):
        try:
            # Consultar a Tabela dos produtos.
            dados_produtos = self.consulta.Vitrine_Dados_Produtos()

            # Verificar se a Qtd. do produto está acima de 0 usando loops e listas.
            Vitrine_Prudutos = []

            # Loop que percorre a lista dos dados dos produtos validando a quantidade.
            for produto in dados_produtos:
                if produto["Qtd."] > 0:
                    Vitrine_Prudutos.append(produto)
            return {"sucesso": True, "dados_vitrine": Vitrine_Prudutos}
        
        # Captura qualquer falha e retorna a descrição do erro atual
        except Exception as erro:
            return {"sucesso": False, "erro": str(erro)}
                      
    # Vai Fazer o controle de exibição correta de serviços nos slots da vitrine no site.    
    def Controle_Vitrine_Servicos(self):
        try:
            # Consultar a Tabela dos Serviços.
            Vitrine_Servicos = self.consulta.Vitrine_Dados_Servicos()
            return {"sucesso": True, "dados_vitrine": Vitrine_Servicos}

        # Captura qualquer falha e retorna a descrição do erro atual
        except Exception as erro:
            return {"sucesso": False, "erro": str(erro)}
                      
    # Verifica-se a quantidade do que foi encomendado, está abaixo do limite do estoque.
    def Controle_da_Encomendas(self, id_prod, qtd_prod, tel_client):
        try:
            # Formata o valor da quantidade do produto em número inteiro.
            qtd_prod = int(qtd_prod)

            # Formata e valida o telefone enviado pelo usuário
            respost_tel = self.Trata_Telefone(tel_client)

            # Se o telefone for inválido, interrompe o login e retorna o motivo do erro.
            if respost_tel["valido"] == False:
                return {"sucesso": False, "erro": respost_tel["erro"]}

            # Guarda o telefone já formatado e limpo.
            tel_cliente = respost_tel["texto_formatado"]

            # Verifica-se o número não ultrapassa os limites.
            if qtd_prod < 1 or qtd_prod > 5:
                return {"sucesso": False, "erro": "Quantidade é min: 1 ou max: 5"}
            
            # Chama a função de consulta ao dados do produto e cliente.
            retorno_prod = self.consulta.Select_Info_Produto(id_prod)
            dados_client = self.consulta.Login_Select_Contas(tel_cliente)

            # Verificar se qtd_prod <= Qtd. da tabela_produtos
            if isinstance(retorno_prod, list) and len(retorno_prod) > 0:
                dados_prod = retorno_prod[0]
            elif isinstance(retorno_prod, dict):
                dados_prod = retorno_prod
            else:
                dados_prod = None

            # Se a busca no banco voltar vazia, avisa que o produto não encontrado no banco.
            if not dados_prod:
                return {"sucesso": False, "erro": "Produto não Encontrado no banco de dados."}

            estoque_banco = int(dados_prod.get("Qtd.", 0))
            quantidade_desejada = int(qtd_prod)

            # Agora a comparação nunca mais vai quebrar, porque são dois números inteiros reais!
            if quantidade_desejada <= estoque_banco:
                dados_encomenda = self.consulta.Insercao_Dados_Encomenda(id_prod, qtd_prod, tel_cliente)
                print(dados_encomenda)
                # Faz a conta da subtração e envia para atualizar
                novo_estoque = estoque_banco - quantidade_desejada
                result = self.consulta.Atualizar_Estoque(id_prod, novo_estoque)
                print(result)
                
            else:
                return {"sucesso": False, "erro": f"Estoque insuficiente. Qtd atual: {dados_prod.get('Qtd.', 0)}"}

            # Apontando para o inicio das lista dos dados dos usuarios.
            usuario = dados_client[0] if isinstance(dados_client, list) else dados_client
            encomenda = dados_encomenda[0] if isinstance(dados_encomenda, list) else dados_encomenda
            produto = dados_prod

            # Formatando o valores para retornos
            valor_float = float(produto['valor'])
            valor_real = valor_float / 100 if valor_float > 100000 else valor_float
            valor_formatado = f"R$ {valor_real:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        
            # Calculo para exibir na mensagem
            total_real = qtd_prod * valor_real
            total_formatado = f"R$ {total_real:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

            # Redirecionar o usuario ao zap do vendedor (link).
            Msg_puro = (
                f"*NOVA ENCOMENDA RECEBIDA* \n\n"
                f"*Encomenda de N°:* {encomenda.get('id_encomendas', encomenda.get('id', 'N/A'))}\n"
                f"*Cliente:* {usuario['nome']}\n"
                f"*Quantidade::* {qtd_prod}x\n"
                f"*Preço Unitário:* R$ {valor_formatado}\n"
                f"*Valor Total a Pagar:* R$ {total_formatado}\n\n"
                f"*Aguarde um instante que o vendedor já lhe atenderá.*"
            )

            # Formata Mensagem a ser envia junto com o cliente ao vendedor.
            Msg_format = quote_plus(Msg_puro)
            whats_vendedor = "Número do Vendedor"

            # Link que direciona o cliente ao whatsApp do vendedor + mensagem de confirmação da operação.
            url_final = f"https://wa.me/{whats_vendedor}?text={Msg_format}"
            return {"sucesso": True, "url": url_final}
        
        # Captura qualquer falha e retorna a descrição do erro Técnico.
        except Exception as erro:
            return {"sucesso": False, "erro": str(erro)}
                      
    # Contrele para inserção dos dados para agendamento e retornos.
    def Controle_de_Agendamentos(self, tel_client, id_servico, data, hora):
        try:
            # Formata e valida o telefone enviado pelo usuário
            respost_tel = self.Trata_Telefone(tel_client)

            # Se o telefone for inválido, interrompe o login e retorna o motivo do erro.
            if respost_tel["valido"] == False:
                return {"sucesso": False, "erro": respost_tel["erro"]}

            # Guarda o telefone já formatado e limpo.
            tel_cliente = respost_tel["texto_formatado"]

            # Formatar a (Data/Hora) do agendamento antes de ser salvo no BDs.
            data_hora_entrada = datetime.strptime(f"{data} {hora}","%Y-%m-%d %H:%M")
            fuso_brasil = timezone(timedelta(hours=-3))
            data_hora_fuso = data_hora_entrada.replace(tzinfo=fuso_brasil)
            data_hora_final = data_hora_fuso.isoformat()

            # Chamar a função de inserir ao Banco.
            dados = self.consulta.Insercao_Dados_Agendamentos(tel_cliente, id_servico, data_hora_final)
            dicionario_returno = dict(sucesso=True, erro=None)
            return dicionario_returno
        
        # Captura qualquer falha e retorna a descrição do erro atual
        except Exception as erro:
            return {"sucesso": False, "erro": str(erro)}
                      
    # Função que vai verificar se o horario já foi reservado caso sim não exibi no site como opções.
    def Filtro_de_Horarios(self, data_escolhida):
        try:
            # Vai consultar os data/horarios na tabela de agendamentos no BDs.
            dados_de_agendamentos = self.consulta.Select_Horarios_Agenda(data_escolhida)
            
            # Vai consultar na tabela de horarios no BDs.
            horarios_definidos = self.consulta.Select_Info_Horarios()

            # Retorno dos horarios definidos.
            if isinstance(horarios_definidos, list) and len(horarios_definidos) > 0:
                horarios_definidos = [
                    item["horarios"][:5] for item in horarios_definidos 
                    if isinstance(item, dict) and "horarios" in item
                ]

            # Vai fatiar a data/hora para visualizar apenas a hora e comparar com os horarios da tabela horarios. 
            horarios_ocupados = []
            if isinstance(dados_de_agendamentos, list):
                horarios_ocupados = [
                    datetime.fromisoformat(item["data_hora"].replace(" ", "T")).astimezone(timezone(timedelta(hours=-3))).strftime("%H:%M")
                    for item in dados_de_agendamentos if isinstance(item, dict) and "data_hora" in item
            ] 

            # Vai fazer a subtração dos horarios agendados da lista de horarios retornados da tabela.
            horarios_disponiveis = list(set(horarios_definidos) - set(horarios_ocupados))
            horarios_disponiveis.sort() 

            # Retorna ao Backend apenas os horarios que sobrou para lista da caixa de entrada (horario).
            return horarios_disponiveis
        
        # Captura qualquer falha e retorna a descrição do erro atual
        except Exception as erro:
            return {"sucesso": False, "erro": str(erro)}

    # Trata o telefone de entrada antes de inserir ou consultar.
    def Trata_Telefone(self, tel_bruto):
        try:
            # Remove qualquer caractere que não seja número (limpeza total)
            tel_limpo = re.sub(r'\D', '', tel_bruto)
    
            # Validação de tamanho padrão brasileiro com DDD tem exatamente 11 dígitos
            if len(tel_limpo) != 11:
                return {
                    "valido": False, 
                    "texto_formatado": None, 
                    "erro": f"Telefone Inválido! Deve conter 11 dígitos com DDD (digitados: {len(tel_limpo)})."
            }
    
            # Aplica a máscara/formatação: (XX) XXXXX-XXXX
            ddd = tel_limpo[0:2]
            nono_digito = tel_limpo[2]
            primeira_metade = tel_limpo[3:7]
            segunda_metade = tel_limpo[7:11]

            # Formatando o telefone para ser salvo ao banco de dados.
            tel_formatado = f"({ddd}) {nono_digito}{primeira_metade}-{segunda_metade}"
            return {
                "valido": True, 
                "texto_formatado": tel_formatado, 
                "erro": None
            }
        
        # Captura qualquer falha e retorna a descrição do erro Técnico.
        except Exception as erro:
            print("debug1")
            return {"sucesso": False, "erro": str(erro)}
                     