from supabase import create_client
from datetime import datetime


class ConsultaSQL():
    # O inicializador rodará automaticamente e estabelecendo a conexão com a BDs..
    def __init__(self):
        supabase_url = "Url do seu Banco de Dados"
        supabase_key = "Chave do seu Banco de Dados"
                
        # Conexão grudada na própria classe usando o 'self.'
        self.conexoes = create_client(supabase_url, supabase_key)
        
    # Consulta de informações da tabela_contas para verificação de credenciais na BDs.
    def Login_Select_Contas(self, tel):
        try:
            resultados = self.conexoes.table("Tabela_Contas").select("*").eq("tel_cliente", tel).execute()
            return resultados.data
        
        # Captura qualquer falha e retorna a descrição do erro Técnico.
        except Exception as erro:
            return {"sucesso": False, "erro": str(erro)}
        
    # Vai atualizar a Senha de um Usuario após ele acabar esquecendo em algum momento.
    def Atualizar_Senha_Login(self, tel_cliente, senha_cliente):
        try:
            self.conexoes.table("Tabela_Contas").update({"senha": senha_cliente}).eq("tel_cliente", tel_cliente).execute()
            return {"sucesso": True, "erro": None}
        
        # Captura qualquer falha e retorna a descrição do erro Técnico.
        except Exception as erro:
            return {"sucesso": False, "erro": str(erro)}
               
    # Função de inserir dados a tabela_contas na BDs.
    def Cadastro_Insert(self, nome_client, tel_client, senha_client):
        # Aplicando o tratamento de erros!
        try:        
            self.conexoes.table("Tabela_Contas").insert({ "tel_cliente": tel_client, "nome": nome_client, "senha": senha_client}).execute()
            return {"sucesso": True, "erro": None}
            
        # Captura qualquer falha e retorna a descrição do erro Técnico.
        except Exception as erro:
            return {"sucesso": False, "erro": str(erro)}
        
    # Consulta de informações da tabela_produtos na BDs.
    def Select_Info_Produto(self, id_produto):
        try:
            
            dados_produto = self.conexoes.table("Tabela_Produtos")\
                                     .select("*")\
                                     .eq("id_produtos", id_produto)\
                                     .execute()
        
            return dados_produto.data # Devolve a lista do Supabase [ { ... } ]
                
        # Captura qualquer falha e retorna a descrição do erro Técnico.
        except Exception as erro:
            return {"sucesso": False, "erro": str(erro)}

    # Consulta os Dados do produto para exibir na vitrines para encomendar.
    def Vitrine_Dados_Produtos(self):
        try:
            dados_prod = self.conexoes.table("Tabela_Produtos").select("*").execute()
            return dados_prod.data

        # Captura qualquer falha e retorna a descrição do erro Técnico.
        except Exception as erro:
            return {"sucesso": False, "erro": str(erro)}
    
    # Consulta os Dados do serviços para exibir na vitrines para agendamentos.
    def Vitrine_Dados_Servicos(self):
        try:
            dados_serve = self.conexoes.table("Tabela_Servicos").select("*").execute()
            return dados_serve.data

        # Captura qualquer falha e retorna a descrição do erro Técnico.
        except Exception as erro:
            return {"sucesso": False, "erro": str(erro)}
        
    # Atualiza os dados quantidade do produtos no estoque.
    def Atualizar_Estoque(self, id_produto, qtd_produto):
        try:
            self.conexoes.table("Tabela_Produtos").update({"Qtd.": qtd_produto}).eq("id_produtos", id_produto).execute()
            return {"sucesso": True, "erro": None}
                 
        # Captura qualquer falha e retorna a descrição do erro Técnico.
        except Exception as erro:
            return {"sucesso": False, "erro": str(erro)}
          
    # Consulta de informações da tabela_serviços na BDs.
    def Select_Info_Serviço(self, id_servico):
        try:
            dados_servico = self.conexoes.table("Tabela_Servicos").select("*").eq("id_servicos", id_servico).execute()
            return dados_servico.data

        # Captura qualquer falha e retorna a descrição do erro Técnico.
        except Exception as erro:
            return {"sucesso": False, "erro": str(erro)}
        
    # Consulta a tabela de agendamentos para consultar horarios.
    def Select_Horarios_Agenda(self, data):
        try:
            inicio_dia = f"{data}T00:00:00-03:00"
            fim_dia = f"{data}T23:59:59-03:00"

            dados = self.conexoes.table("Tabela_Agendamentos")\
                .select("data_hora")\
                    .gte("data_hora", inicio_dia)\
                        .lte("data_hora", fim_dia).execute()
            return dados.data

        # Captura qualquer falha e retorna a descrição do erro Técnico.
        except Exception as erro:
            return {"sucesso": False, "erro": str(erro)}
        
    # Consulta de informações da tabela_horarios na BDs.
    def Select_Info_Horarios(self):
        try:
            list_horarios = self.conexoes.table("Tabela_Horarios").select("horarios").execute()
            return list_horarios.data
        
        # Captura qualquer falha e retorna a descrição do erro Técnico.
        except Exception as erro:
            return {"sucesso": False, "erro": str(erro)}
            
    # Função de inserir dados a tabela_encomendas na BDs.
    def Insercao_Dados_Encomenda(self, id_produto, qtd_produto, tel_cliente):
        try:
            data_hora_atual = datetime.now().isoformat()
            # realizar a inserção na tabela de encomendas.
            self.conexoes.table("Tabela_Encomendas").insert({"cliente_tel": tel_cliente, "produto": int(id_produto), "Qtd.": int(qtd_produto), "hora": data_hora_atual}).execute()
            return {"sucesso": True, "erro": None}

        # Captura qualquer falha e retorna a descrição do erro Técnico.
        except Exception as erro:
            return {"sucesso": False, "erro": str(erro)}
                
    # Função de inserir dados a tabela_agendamentos na BDs.
    def Insercao_Dados_Agendamentos(self, tel_cliente, id_servico, data_hora):
        try:
            # Adicionar os dados do agendamento de serviços ao BDs do site.
            self.conexoes.table("Tabela_Agendamentos").insert({"tel_cliente": tel_cliente, "servico": id_servico, "data_hora": data_hora}).execute()
            return {"sucesso": True, "erro": None}
        
        # Captura qualquer falha e retorna a descrição do erro Técnico.
        except Exception as erro:
            return {"sucesso": False, "erro": str(erro)}
                