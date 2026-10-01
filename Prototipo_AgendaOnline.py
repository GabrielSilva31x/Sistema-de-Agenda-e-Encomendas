import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
from tkcalendar import DateEntry
from io import BytesIO
import webbrowser
from PIL import Image, ImageTk, ImageDraw, ImageOps
from Controles import *
import requests

class Prototipo():
    def __init__(self):
        self.janela_login()
        self.controles = Controles()

    # Função que converte o link no formato string da Header.
    def Converso_Img(self, Url_Img):
        # Tratamento correto para exibir a imagem do produtos na vitrine da janela loja.
        url_imagem = Url_Img
        foto_final = None

        try: 
            # Definindo o cabeçalho da imagem e usando as ferramentas para conversão.
            cabecalho = {"User-Agent": "Mozilla/5.0"}
            reposta = requests.get(url_imagem, timeout=5, headers=cabecalho)
            img_bruta = Image.open(BytesIO(reposta.content)).convert("RGB")
            img_rend = img_bruta.resize((700, 600)) # defindo seu tamanho.

            raio = 15
            mascara = Image.new("L", (700, 600), 0)
            draw = ImageDraw.Draw(mascara)
            draw.rounded_rectangle((0, 0, 700, 600), radius=raio,  fill=255)

            img_arredondada = Image.new("RGBA", (700, 600), (0, 0, 0, 0))
            img_arredondada.paste(img_rend, (0, 0), mask=mascara)

            foto_final = ImageTk.PhotoImage(img_arredondada)
            return foto_final

        except Exception as e:
            print(f"Erro ao baixar a imagem do produto: {e}")
            return None

    # Função que converte o link no formato string dos cards da janela loja.
    def Converso_img_cards(self, Url_Img):
        url_imagem = Url_Img
        foto_final = None
        
        try: 
            cabecalho = {"User-Agent": "Mozilla/5.0"}
            reposta = requests.get(url_imagem, timeout=5, headers=cabecalho)
            img_bruta = Image.open(BytesIO(reposta.content)).convert("RGB")
            img_rend = ImageOps.fit(img_bruta, (160, 260))
                
            # Aplica a máscara de cantos arredondados na imagem perfeitamente cheia
            raio = 15 
            mascara = Image.new("L", (160, 260), 0)
            draw = ImageDraw.Draw(mascara)
            draw.rounded_rectangle((0, 0, 160, 260), radius=raio, fill=255)
            
            img_arredondada = Image.new("RGBA", (160, 260), (0, 0, 0, 0))
            img_arredondada.paste(img_rend, (0, 0), mask=mascara)
            
            foto_final = ImageTk.PhotoImage(img_arredondada)
            return foto_final

        except Exception as e:
            print(f"Erro ao baixar a imagem do produto: {e}")
            return None

    # Função que converte o link no formato string dos cards da janela vitrine.
    def Converso_img_vitrine(self, Url_Img):
        url_imagem = Url_Img
        foto_final = None
        
        try: 
            cabecalho = {"User-Agent": "Mozilla/5.0"}
            reposta = requests.get(url_imagem, timeout=5, headers=cabecalho)
            img_bruta = Image.open(BytesIO(reposta.content)).convert("RGB")
            img_rend = ImageOps.fit(img_bruta, (260, 390))
                
            # Aplica a máscara de cantos arredondados na imagem perfeitamente cheia
            raio = 15 
            mascara = Image.new("L", (260, 390), 0)
            draw = ImageDraw.Draw(mascara)
            draw.rounded_rectangle((0, 0, 260, 390), radius=raio, fill=255)
            
            img_arredondada = Image.new("RGBA", (260, 390), (0, 0, 0, 0))
            img_arredondada.paste(img_rend, (0, 0), mask=mascara)
            
            foto_final = ImageTk.PhotoImage(img_arredondada)
            return foto_final

        except Exception as e:
            print(f"Erro ao baixar a imagem do produto: {e}")
            return None

    # Função que recebe os retornos das função do Backend e faz o tratamento correto.
    def return_especial(self, retorno, janela):
        # Verifica a estrutura do retorno para validação.
        if not retorno or not isinstance(retorno, dict):
            msg.showerror(title="Mensagem do Banco", message="Falha: Resposta inválida do banco.", parent=janela)
            return

        # Realiza o Login do User (Salva os dados, mas NÃO para a execução)
        if retorno.get("sucesso") == True and "nome_cliente" in retorno and "telefone_cliente" in retorno:
            self.usuario_logado = {
                "nome": retorno.get("nome_cliente"),
                "telefone": retorno.get("telefone_cliente")
            }
            usuario = self.usuario_logado
            janela.destroy()
            self.janela_loja(usuario) # Abre a janela da loja diretamente!
            return True
        
        # Retorno especifico para os produtos: Se houver URL, abre o WhatsApp primeiro
        if retorno.get("sucesso") == True and "url" in retorno:
            msg.showinfo(title="Mensagem do Banco", message="✅ Operação realizada com Sucesso!", parent=janela)
                        
            whats = retorno.get("url")
            webbrowser.open(whats)
            janela.destroy()

        # Retorno especifico para o Login/recuperação de senha: Se houver código/senha, exibe na tela
        elif retorno.get("sucesso") == True and "codigo" in retorno:
            codigo = retorno.get("codigo")
            msg.showinfo(title="Mensagem do Banco", message=f"🔑 Sua nova senha: {codigo}", parent=janela)
            janela.destroy()

            
        # Exibe a caixinha de "Operação realizada com Sucesso!" que você pediu!
        elif retorno.get("sucesso") == True:
            janela.focus_force()

            msg.showinfo(title="Mensagem do Banco", message="✅ Operação realizada com Sucesso!", parent=janela)
            janela.destroy()

        # Retorno para capturar os erros ocorrido durante a comunicação com o banco.
        else:
            erro_real = retorno.get("erro", "Erro desconhecido")
            msg.showerror(title="Mensagem do Banco", message=f"Falha: {erro_real}", parent=janela)

    # Função que recebe dados do banco atrávez das funções de consulta ao banco no backend e carrega para janela vitrine dos produtos.
    def return_vitrine_produtos(self, retorno):
        # 1. Garante que é um dicionário antes de testar as chaves
        if isinstance(retorno, dict) and retorno.get("sucesso") is True:
            # 2. Busca o dado com segurança (retorna [] se a chave não existir)
            dados_vitrine = retorno.get("dados_vitrine", [])

            # Caso não tenha na variavel que recebeu os dados do banco ele entra e retorna essa mensagem de notificação.
            if not dados_vitrine:
                print("⚠️ Não há produtos retornados do Banco de Dados.")
                tk.Label(self.frame_vitrine, text="Nenhum produto disponível.", bg="gray20", fg="gray50").pack(pady=20)
                return

            # Variavel definida para receber o usuário ativo no sistema para operações futuras.
            user_ativo = self.usuario_logado if hasattr(self, 'usuario_logado') and self.usuario_logado else {"nome": "Convidado", "telefone": ""}

            # Loop para percorrer os dados retornados do Banco.
            for posi, prod  in enumerate(dados_vitrine):
                coluna = posi
                linha = 0 

                # Dicionário que vai estruturar e armmzenar os dados do produto. 
                info_produto = {
                    "id": prod.get("id_produtos", prod.get("id_produtos", 0)),
                    "nome": prod.get("nome", "sem_nome"),
                    "valor": prod.get("valor", "sem_valor"),
                    "descricao": prod.get("descricao", ""),
                    "Qtd.": prod.get("Qtd.", ""),
                    "Imagem": prod.get("Img_produto", ""),
                    "Tipo": "Produto"
                }

                # Definindo os cards que serão os produtos exibidos na vitrine.
                card_prod = tk.Frame(self.frame_vitrine, bg="gray20", relief=tk.FLAT, bd=0, highlightthickness=1, highlightbackground="gray60", width=160, height=240)
                card_prod.grid(row=linha, column=coluna, padx=5, pady=5)
                card_prod.grid_propagate(False)
                card_prod.pack_propagate(False)  

                # Definindo os cards como clicavel para abrir as janelas vitrines das info dos produtos.
                card_prod.bind("<Button-1>", lambda event, item=info_produto: self.janela_vitrine(user_ativo, item))

                # Tratamento correto para exibir a Img do produtos na vitrines.
                url_imagem = info_produto['Imagem']
                try:
                    foto_final = self.Converso_img_cards(url_imagem)  # Chamando a função para tratar a imagem em formato URL para ser exibida na vitrines.
                except Exception as e: 
                    print(f"Erro ao baixar a imagem do produto: {e}")

                # SE a variavel tiver com alguma imagem ela vai exibir.
                if foto_final: 
                    foto_prod = tk.Label(card_prod, image=foto_final, bg="gray20")
                    foto_prod.image = foto_final
                    foto_prod.pack(padx=10, pady=10) 

                else: # SE NÃO o cards vai aparecer com o texto [ FOTO ].
                    foto_prod = tk.Label(card_prod, text="[ FOTO ]", bg="gray30")
                    foto_prod.pack(padx=10, pady=10)
                    
                foto_prod.place(x=0, y=0, relwidth=1, relheight=1)

                # Definindo a Img como clicavel para abrir as janelas vitrines das info dos produtos.
                foto_prod.bind("<Button-1>", lambda event, item=info_produto: self.janela_vitrine(user_ativo, item))

                # Trate a exibição dos centavos dividindo por 100.
                valor_bruto = float(info_produto["valor"])
                valor_real = valor_bruto / 100 if valor_bruto > 1000 else valor_bruto
                texto_preco = f"R$ {valor_real:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

                # Exibi o preço dos produtos no cards e define clicavel atrávez da função BIND
                preco_prod = tk.Label(foto_prod, text=texto_preco, bg="#1a1a1a",fg="lightgreen", font=("Ariel", 9, "bold"))
                preco_prod.place(x=2, y=195)
                preco_prod.bind("<Button-1>", lambda event, item=info_produto: self.janela_vitrine(user_ativo, item))

                # Exibi o nome dos produtos no cards e define clicavel atrávez da função BIND.
                nome_prod = tk.Label(foto_prod, text=info_produto["nome"], bg="#1a1a1a", fg="white",  font=("Ariel", 8, "bold"))
                nome_prod.place(x=2, y=215)
                nome_prod.bind("<Button-1>", lambda event, item=info_produto: self.janela_vitrine(user_ativo, item))
                
        else:  # SE NÃO apenas uma mensagem de ERRO.
            erro_real = retorno.get("erro", "Erro desconhecido")
            msg.showerror(title="Mensagem do Banco", message=f"Falha: {erro_real}")

    # Função que recebe dados do banco atrávez das funções de consulta ao banco no backend e carrega para janela vitrine dos serviços.
    def return_vitrine_servicos(self, retorno):
            # 1. Garante que é um dicionário antes de testar as chaves
            if isinstance(retorno, dict) and retorno.get("sucesso") is True:
                # 2. Busca o dado com segurança (retorna [] se a chave não existir)
                dados_vitrine = retorno.get("dados_vitrine", [])

                # Caso não tenha na variavel que recebeu os dados do banco ele entra e retorna essa mensagem de notificação.
                if not dados_vitrine:
                    print("⚠️ Não há serviços retornados do Banco de Dados.")
                    tk.Label(self.frame_vitrine, text="Nenhum produto disponível.", bg="gray20", fg="gray50").pack(pady=20)
                    return

                # Variavel definida para receber o usuário ativo no sistema para operações futuras.
                user_ativo = self.usuario_logado if hasattr(self, 'usuario_logado') and self.usuario_logado else {"nome": "Convidado", "telefone": ""}

                # Loop para percorrer os dados retornados do Banco.
                for posi, service  in enumerate(dados_vitrine):
                    coluna = posi 
                    linha = 0 

                    # Dicionário que vai estruturar e armmzenar os dados do serviço. 
                    info_servico = {
                        "id": service.get("id_servicos", service.get("id_servico", 0)),
                        "nome": service.get("nome", "sem_nome"),
                        "valor": service.get("valor", "sem_valor"),
                        "descricao": service.get("descricao", ""),
                        "Imagem": service.get("Img_servico", ""),
                        "Tipo": "Serviço"
                    }

                    # Definindo os cards que serão os serviços exibidos na vitrine.
                    card_servico = tk.Frame(self.frame_vitrine, bg="gray20", relief=tk.FLAT, bd=0, highlightthickness=1, highlightbackground="gray60", width=160, height=240)
                    card_servico.grid(row=linha, column=coluna, padx=5, pady=5)
                    card_servico.grid_propagate(False)
                    card_servico.pack_propagate(False)  

                    # Definindo os cards como clicavel para abrir as janelas vitrines das info dos Serviços.
                    card_servico.bind("<Button-1>", lambda event, item=info_servico: self.janela_vitrine(user_ativo, item))

                    # Tratamento correto para exibir a Img do servico na vitrines.
                    url_imagem = info_servico['Imagem']
                    try: 
                        foto_final = self.Converso_img_cards(url_imagem)  # Chamando a função para tratar a imagem em formato URL para ser exibida na vitrines.
                    except Exception as e:
                        print(f"Erro ao baixar a imagem do serviços: {e}")

                    # SE a variavel tiver com alguma imagem ela vai exibir.
                    if foto_final:
                        foto_servico = tk.Label(card_servico, image=foto_final, bg="gray20")
                        foto_servico.image = foto_final
                        
                    else:   # SE NÃO o cards vai aparecer com o texto [ FOTO ].
                        foto_servico = tk.Label(card_servico, text="[ FOTO ]", bg="gray30")

                    foto_servico.place(x=0, y=0, relwidth=1, relheight=1)

                    # Definindo a Img como clicavel para abrir as janelas vitrines das info dos produtos.
                    foto_servico.bind("<Button-1>", lambda event, item=info_servico: self.janela_vitrine(user_ativo, item))

                    # Trate a exibição dos centavos dividindo por 100.
                    valor_bruto = float(info_servico["valor"])
                    valor_real = valor_bruto / 100 if valor_bruto > 1000 else valor_bruto
                    texto_preco = f"R$ {valor_real:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

                    # Exibi o preço dos serviços no cards e define clicavel atrávez da função BIND
                    preco_servico = tk.Label(foto_servico, text=texto_preco, bg="#1a1a1a", fg="lightgreen", font=("Ariel", 9, "bold"))
                    preco_servico.place(x=2, y=195)
                    preco_servico.bind("<Button-1>", lambda event, item=info_servico: self.janela_vitrine(user_ativo, item))

                    # Exibi o nome dos serviços no cards e define clicavel atrávez da função BIND.
                    nome_servico = tk.Label(foto_servico, text=info_servico["nome"], bg="#1a1a1a", fg="white",  font=("Ariel", 8, "bold"))
                    nome_servico.place(x=2, y=215)
                    nome_servico.bind("<Button-1>", lambda event, item=info_servico: self.janela_vitrine(user_ativo, item))

            else:    # SE NÃO apenas uma mensagem de ERRO.
                erro_real = retorno.get("erro", "Erro desconhecido")
                msg.showerror(title="Mensagem do Banco", message=f"Falha: {erro_real}")

    # Frame da janela login e seu escopo.
    def janela_login(self):
        # Apontar a variavel para o poder de execução.
        self.root_login = tk.Tk()
        self.root_login.geometry("400x500")
        self.root_login.title("><")
        self.root_login.configure(bg="#1a1c1e") 

        # Definindo o titulo e o espaçamento entre as widgets da interface.
        titulo = tk.Label(self.root_login, text="_Stores", bg="#1a1c1e", font=("Brush Script MT", 20, "bold italic"), fg="white")
        titulo.pack(pady=(20, 20))

        # Definindo o titulo e o espaçamento entre as widgets da interface.
        frame = tk.Frame(self.root_login, bg="#1a1c1e")
        frame.pack(pady=30, padx=40, fill=tk.BOTH, expand=True)

        # Label + entry do telefone user
        label_tel = tk.Label(frame, text="Telefone:", font=("Arial", 10, "bold"), fg="white", bg="#1a1c1e")
        label_tel.pack(anchor="w", pady=(0, 3))

        entrada_tel = tk.Entry(frame, font=("Arial", 10, "bold"), fg="white", bg="gray18", bd=1, relief=tk.SOLID, insertbackground="white")
        entrada_tel.pack(fill=tk.X, pady=(0, 20), ipady=8)

        # Label + entry do senha user
        label_senha = tk.Label(frame, text="Senha:", font=("Arial", 10, "bold"), fg="white", bg="#1a1c1e")
        label_senha.pack(anchor="w", pady=(0, 3))

        entrada_senha = tk.Entry(frame, font=("Arial", 10, "bold"), fg="white", bg="gray18", bd=1, relief=tk.SOLID, insertbackground="white")
        entrada_senha.pack(fill=tk.X, pady=(0, 10), ipady=8)

        # Botão para realizar a recuperação da senha.
        button_recuperar = tk.Button(frame, text="Esqueci a senha",bg="#1a1c1e",fg="gray80",bd=0, font=("Arial", 9, "underline"), relief=tk.FLAT,activebackground="#1a1c1e", 
            activeforeground="white", 
                command=lambda: self.janela_recuperar_senha(self.root_login)
            , width=10, pady=1)
        button_recuperar.pack(anchor="center", pady=(0, 40))

        # Defininfo o buttom que chama o backend.
        button_login = tk.Button(frame, text="Acessar Conta", bg="#007acc", fg="white",
            command=lambda: self.return_especial(self.controles.Verificação_de_Credenciais( 
                entrada_tel.get(), entrada_senha.get()), self.root_login)
            , width=8)
        button_login.pack(fill=tk.X, pady=(0, 15), padx=70, ipady=4)

        # divizão da interface
        divizao = tk.Label(frame, text="----- ou -----", bg="#1a1c1e", fg="white")
        divizao.pack(fill=tk.X, pady=5)

        # Botão para criar nova conta
        btn_ir_cadastro = tk.Button(frame, text="Criar Nova Conta", font=("Arial", 10), bg="#d42424", fg="white", bd=0, cursor="hand2", pady=4, command= lambda: self.janela_cadastro(self.root_login))
        btn_ir_cadastro.pack(fill=tk.X, pady=10, padx=80, ipady=5)

    # Frame da janela cadastro e seu escopo.
    def janela_cadastro(self, root):
        # Apontar a variavel para o poder de execução.
        self.root_cadastro = tk.Toplevel(root)
        self.root_cadastro.configure(bg="#1a1c1e")
        self.root_cadastro.geometry("350x400")
        self.root_cadastro.title("Seja Bem-Vindo")


        # Definindo o titulo e o espaçamento entre as widgets da interface.
        frame_cadastro = tk.Frame(self.root_cadastro, bg="#1a1c1e")
        frame_cadastro.pack(padx=10, pady=10)

        # Label + entry do nome user
        label_nome = tk.Label(frame_cadastro, text="Nome_Usúario:", font=("Arial", 10, "bold"), fg="white", bg="#1a1c1e")
        label_nome.pack(anchor="w", pady=(15, 3))
        
        entrada_nome = tk.Entry(frame_cadastro, font=("Arial", 10, "bold"), fg="white", bg="gray18", bd=1, relief=tk.SOLID, insertbackground="white")
        entrada_nome.pack(fill=tk.X, pady=(0, 20), ipady=8)

        # Label + entry do telefone
        label_tel = tk.Label(frame_cadastro, text="Telefone:", font=("Arial", 10, "bold"), fg="white", bg="#1a1c1e")
        label_tel.pack(anchor="w", pady=(0, 3))
        
        entrada_tel = tk.Entry(frame_cadastro, font=("Arial", 10, "bold"), fg="white", bg="gray18", bd=1, relief=tk.SOLID, insertbackground="white")
        entrada_tel.pack(fill=tk.X, pady=(0, 20), ipady=8)

        # Label + entry do senha
        label_senha = tk.Label(frame_cadastro, text="Senha:", font=("Arial", 10, "bold"), fg="white", bg="#1a1c1e")
        label_senha.pack(anchor="w", pady=(0, 3))

        entrada_senha = tk.Entry(frame_cadastro, font=("Arial", 10, "bold"), fg="white", bg="gray18", bd=1, relief=tk.SOLID, insertbackground="white")
        entrada_senha.pack(fill=tk.X, pady=(0, 20), ipady=8)

        # Defininfo o buttom que chama o backend.
        click = tk.Button(frame_cadastro, text="Cadastrar-se", bg="#007acc",fg="white",
                    command=lambda: self.return_especial(self.controles.Controle_Dados_Cadastros(entrada_nome.get(), 
                entrada_tel.get(), entrada_senha.get()), self.root_cadastro)
            , width=15)
        click.pack(anchor="center", pady=3)

        # label linha
        separador = tk.Label(frame_cadastro, text="--------------------------------------------------------------------------------", bg="#1a1c1e", fg="gray40")
        separador.pack(fill=tk.X ,pady=(2, 5))

        # button voltar(destroy)
        buttom_voltar = tk.Button(frame_cadastro, text="voltar", font=("Ariel", 10), 
                bg="gray30", fg="white", padx=15,
            command= lambda: self.root_cadastro.destroy())
        buttom_voltar.pack(anchor="center", pady=3)

    # Frame da janela troca senha e seu escopo.
    def janela_recuperar_senha(self, root):
        # Toplevel cria uma NOVA janela independente na tela
            self.root_recuperar_senha = tk.Toplevel(root)
            self.root_recuperar_senha.title("-- Recuperar Senha --")
            self.root_recuperar_senha.geometry("400x300")
            self.root_recuperar_senha.configure(bg="#1a1c1e")
        
            frame = tk.Frame(self.root_recuperar_senha, bg="#1a1c1e")
            frame.pack(pady=30, padx=40, fill=tk.BOTH, expand=True)
    
            # Label + entry do telefone user
            label_tel = tk.Label(frame, text="Telefone:", font=("Arial", 10, "bold"), fg="white", bg="#1a1c1e")
            label_tel.pack(anchor="w", pady=(0, 3))

            entrada_tel = tk.Entry(frame, font=("Arial", 10, "bold"), fg="white", bg="gray18", bd=1, relief=tk.SOLID, insertbackground="white")
            entrada_tel.pack(fill=tk.X, pady=(0, 20), ipady=8)

            # Botão para gerar a nova senha simples para o usuário.
            BUtton_Trocar_senha = tk.Button(frame, text="Trocar senha",
                command=lambda: self.return_especial(self.controles.Atualizador_de_Senha(entrada_tel.get()), self.root_recuperar_senha), width=15)
            BUtton_Trocar_senha.pack(fill=tk.X, pady=10, padx=70, ipady=5)

            # label linha
            separador = tk.Label(frame, text="--------------------------------------------------------------------------------", bg="#1a1c1e", fg="gray40")
            separador.pack(fill=tk.X ,pady=(2, 2))

            # Botão voltar(destroy)
            buttom_voltar = tk.Button(frame, text="voltar", font=("Ariel", 10), 
                    bg="gray30", fg="white", padx=15,
                command= lambda: self.root_cadastro.destroy())
            buttom_voltar.pack(anchor="center", pady=3)

    # Frame da janela loja e seu escopo.
    def janela_loja(self, usuario):
        # Toplevel cria uma NOVA janela independente na tela
        self.root_loja = tk.Tk()
        self.root_loja.title("LOJA")
        self.root_loja.geometry("600x800")
        self.root_loja.configure(bg="#1a1c1e")
                
        # Definindo a frame e o espaçamento entre as widgets da interface.
        frame_loja = tk.Frame(self.root_loja, bg="#1a1c1e")
        frame_loja.pack(fill=tk.BOTH, expand=True)
        frame_loja.grid_columnconfigure(0, weight=1)

        # Definindo o LINK para Img para a header e a frame da imagem na interface.
        url = "https://conhecimentocientifico.r7.com/wp-content/uploads/2020/03/ceu-estrelado_1048-11828.jpg"
        img_cabecalho = self.Converso_Img(url)

        frame_img_header = tk.Label(frame_loja, image=img_cabecalho, bg="#1a1c1e")
        frame_img_header.pack(fill=tk.BOTH, expand=True)
        frame_img_header.image = img_cabecalho

        # Label + entry do nome user
        nome_user = tk.Label(frame_img_header, text=f"Olá, {usuario["nome"]}", font=("Arial", 13, "bold"), bg="#070707", wraplength=150, fg="white")
        nome_user.pack(padx=1, pady=1, anchor="e")

        # Titulo da grade do canvas.
        titulo_grade = tk.Frame(self.root_loja, bg="#1a1c1e")
        titulo_grade.pack(padx=25, pady=(1, 0), fill=tk.X)
        nome_grade = tk.Label(titulo_grade, text="Serviços", font=("Arial", 14, "bold"), fg="white", bg="#1a1c1e")
        nome_grade.pack(anchor="w")
        
        # Tabuleiro/grade dos serviços.
        container_vitrine = tk.Frame(self.root_loja, bg="gray20")
        container_vitrine.pack(padx=25, pady=5, fill=tk.X)

        # Onde irar ficar os cards dos serviços.
        self.canvas_rolante = tk.Canvas(container_vitrine, bg="gray20", highlightthickness=0, height=250)
        self.canvas_rolante.pack(fill=tk.X, side=tk.TOP, expand=True)

        # Definindo o scrollbar = barra rolante para os serviços.
        largura_horizontal = tk.Scrollbar(container_vitrine, orient="horizontal", command=self.canvas_rolante.xview)
        largura_horizontal.pack(fill=tk.X, side=tk.BOTTOM, pady=0)

        # Configuração do canvas.
        self.canvas_rolante.configure(xscrollcommand=largura_horizontal.set)

        # Frame da vitrine de serviços.
        self.frame_vitrine = tk.Frame(self.canvas_rolante, bg="gray20")

        # Janela interna para exibir a grade.
        self.canvas_janela = self.canvas_rolante.create_window((0, 0), window=self.frame_vitrine, anchor="nw")

        def atualiza_barra_servicos(event):
            self.canvas_rolante.configure(scrollregion=self.canvas_rolante.bbox("all"))
        self.frame_vitrine.bind("<Configure>", atualiza_barra_servicos)

        retorno_vitrine = self.controles.Controle_Vitrine_Servicos()
        self.return_vitrine_servicos(retorno_vitrine)

        # -------------------------------------------------------------------------------------------------------------

        # Segunda grade de vitrine
        titulo_grade2 = tk.Frame(self.root_loja, bg="#1a1c1e")
        titulo_grade2.pack(padx=25, pady=(15, 0), fill=tk.X)
        
        nome_grade2 = tk.Label(titulo_grade2, text="Produtos", font=("Arial", 14, "bold"), fg="white", bg="#1a1c1e")
        nome_grade2.pack(anchor="w")
        
        # Tabuleiro/grade dos produtos.
        container_vitrine2 = tk.Frame(self.root_loja, bg="gray20")
        container_vitrine2.pack(padx=25, pady=(5, 15), fill=tk.X)

        
        # Onde irar ficar os cards dos produtos.
        self.canvas_rolante2 = tk.Canvas(container_vitrine2, bg="gray20", highlightthickness=0, height=250)
        self.canvas_rolante2.pack(fill=tk.X, side=tk.TOP, expand=True)
        
        # Definindo o scrollbar = barra rolante para os produtos.
        largura_horizontal = tk.Scrollbar(container_vitrine2, orient="horizontal", command=self.canvas_rolante2.xview)
        largura_horizontal.pack(fill=tk.X, side=tk.BOTTOM, pady=(1, 0))
        
        # Configuração do canvas.
        self.canvas_rolante2.configure(xscrollcommand=largura_horizontal.set)
        
        # Frame da vitrine de seriços
        self.frame_vitrine = tk.Frame(self.canvas_rolante2, bg="gray20")
        
        # Janela interna para exibir a grade.
        self.canvas_janela = self.canvas_rolante2.create_window((0, 0), window=self.frame_vitrine, anchor="nw")
        
        def atualiza_barra_produtos(event):
            self.canvas_rolante2.configure(scrollregion=self.canvas_rolante2.bbox("all"))
        self.frame_vitrine.bind("<Configure>", atualiza_barra_produtos)
        
        retorno_vitrine = self.controles.Controle_Vitrine_Produtos()
        self.return_vitrine_produtos(retorno_vitrine)

    # Frame da janela vitrines e seu escopo.
    def janela_vitrine(self, usuario, dados):
        # Escopo da janela.
        self.root_vitrine = tk.Toplevel(self.root_loja)        
        self.root_vitrine.title(f"{dados['Tipo']}") 
        self.root_vitrine.geometry("600x495")
        self.root_vitrine.configure(bg="#1a1c1e")

        # Definindo a frame principal
        self.frame_vitrine = tk.Frame(self.root_vitrine, bg="#1a1c1e")
        self.frame_vitrine.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Condição para verificar se é informações de produtos ou serviços.
        if dados["Tipo"] == "Serviço":
            # Defindo a frame da img.
            frame_Img = tk.Frame(self.frame_vitrine, bg="gray20", bd=0, relief=tk.FLAT ,highlightbackground="gray60" ,highlightthickness=1, width=260, height=390)
            frame_Img.pack(side=tk.LEFT, anchor="nw", padx=(0, 20), pady=10)
            frame_Img.pack_propagate(False) 
            frame_Img.grid_propagate(False)

            # Pega a string da URL que veio do clique do card do banco
            url_imagem = dados.get("Imagem", "")
            foto_detalhe = None

            try: 
                foto_detalhe = self.Converso_img_vitrine(url_imagem)
            except Exception as e:
                print(f"Erro ao baixar a imagem do produto: {e}")

            # estrutura que trava a foto na memória para ela não esquecer.
            if foto_detalhe:
                label_Img = tk.Label(frame_Img, image=foto_detalhe, bg="gray20")
                label_Img.image = foto_detalhe 
                label_Img.place(x=0, y=0, relwidth=1.0, relheight=1.0) 
            else:
                # Caso a imagem falhe por timeout, a janela não cai e abre com um aviso
                label_Img = tk.Label(frame_Img, text="[ Sem Imagem ]", bg="gray30", fg="white")
                label_Img.place(x=0, y=0, relwidth=1.0, relheight=1.0)

            # frame para ficar as info laterais.
            frame_dados = tk.Frame(self.frame_vitrine, bg="#1a1c1e")
            frame_dados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)

            # label nome
            label_dados_nome = tk.Label(frame_dados, text=dados["nome"], bg="#1a1c1e", font=("Arial", 14), fg="white", wraplength=250, justify=tk.LEFT)
            label_dados_nome.pack(anchor="w", pady=(0, 2))

            try:
                valor_cru = str(dados.get("valor", "0")).replace(".", "").replace(",", "")
                valor_bruto = float(valor_cru)
                
                valor_real = valor_bruto / 100
            except Exception:
                valor_real = 0.0

            # Formata com pontos nos milhares e vírgula nos centavos
            texto_preco = f"R$ {valor_real:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

            # label valor
            label_dados_valor = tk.Label(frame_dados, text=texto_preco, bg="#1a1c1e", font=("Arial", 11, "bold"), fg="lightgreen")
            label_dados_valor.pack(pady=(0, 10), anchor="w")

            # frame descrição
            frame_dados_descricao = tk.Frame(frame_dados, bg="gray15", bd=1, relief=tk.SOLID, height=250)
            frame_dados_descricao.pack(fill=tk.X, expand=False, pady=(0, 15))
            frame_dados_descricao.pack_propagate(False)

            scroll_descricao = tk.Scrollbar(frame_dados_descricao, orient="vertical")
            scroll_descricao.pack(side=tk.RIGHT, fill=tk.Y)

            # Quebra de linha do texto da descrição do produto/serviços.
            text_descricao = tk.Text(
                frame_dados_descricao, 
                bg="gray10", 
                fg="white",
                font=("Ariel", 10),
                wrap=tk.WORD,
                bd=0, highlightthickness=0,
                yscrollcommand=scroll_descricao.set
            )
            text_descricao.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            # inserindo os dados do produto na caixa rolante.
            scroll_descricao.config(command=text_descricao.yview)

            texto_real = dados.get("descricao", "Nenhuma descrição disponível.")
            text_descricao.insert(tk.END, texto_real)
            text_descricao.config(state=tk.DISABLED)


            # frame para agrupar os 2 botoes finais.
            frame_acoes = tk.Frame(frame_dados, bg="#1a1c1e")
            frame_acoes.pack(fill=tk.X, pady=(0, 5))

            # frame botão
            # Tratamento de futuros erros.
            try:
                buttom_agenda = tk.Button(frame_acoes, text="Agendar Serviço", bg="#007acc", 
                        fg="white", font=("Ariel", 11, "bold"), padx=10, pady=5, 
                    command=lambda: self.janela_agendar(usuario["telefone"], dados))
                buttom_agenda.pack(anchor="center", pady=2)

            except Exception as e:
                print(f"Erro: {e}")

            # label linha
            separador = tk.Label(frame_dados, text="--------------------------------------------------------------------------------", bg="#1a1c1e", fg="gray40")
            separador.pack(fill=tk.X ,pady=(2, 2))

            # button voltar(destroy)
            buttom_voltar = tk.Button(frame_dados, text="voltar", font=("Ariel", 10), 
                    bg="gray30", fg="white", padx=15,
                command= lambda: self.root_vitrine.destroy())
            buttom_voltar.pack(anchor="center",pady=3)

        # ------------------------------------------------------------------------------------------------------------------
        # Layout dos produtos.
        elif dados["Tipo"] == "Produto":
            # Defindo a frame da img.
            frame_Img = tk.Frame(self.frame_vitrine, bg="gray20", bd=0, relief=tk.FLAT, highlightbackground="gray60", highlightthickness=1, width=260, height=390)
            frame_Img.pack(side=tk.LEFT, anchor="nw", padx=(0, 20), pady=10)
            frame_Img.pack_propagate(False) 
            frame_Img.grid_propagate(False)

            # Pega a string da URL que veio do clique do card do banco
            url_imagem = dados.get("Imagem", "")
            foto_detalhe = None

            try: 
                foto_detalhe = self.Converso_img_vitrine(url_imagem)
            except Exception as e:
                print(f"Erro ao baixar a imagem do produto: {e}")

            # exibir a label da imagem.
            if foto_detalhe:
                label_Img = tk.Label(frame_Img, image=foto_detalhe, bg="gray20")
                label_Img.image = foto_detalhe
                label_Img.place(x=0, y=0, relwidth=1.0, relheight=1.0)
            else:
                # Caso a imagem falhe por timeout, a janela não cai e abre com um aviso
                label_Img = tk.Label(frame_Img, text="[ Sem Imagem ]", bg="gray30", fg="white")
                label_Img.place(x=0, y=0, relwidth=1.0, relheight=1.0)

            # -----------------------------------------------------------------------------

            # frame para ficar as info laterais.
            frame_dados = tk.Frame(self.frame_vitrine, bg="#1a1c1e")
            frame_dados.place(relx=0.53, rely=0.0, relwidth=0.47, relheight=1.0)


            # label nome
            label_dados_nome = tk.Label(frame_dados, text=dados["nome"], bg="#1a1c1e", font=("Arial", 14), fg="white", wraplength=250, justify=tk.LEFT)
            label_dados_nome.pack(anchor="w", pady=(10, 2))

            try:
                valor_cru = str(dados.get("valor", "0")).replace(".", "").replace(",", "")
                valor_bruto = float(valor_cru)
                
                valor_real = valor_bruto / 100
            except Exception:
                valor_real = 0.0

            # Formata com pontos nos milhares e vírgula nos centavos
            texto_preco = f"R$ {valor_real:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

            # label valor
            label_dados_valor = tk.Label(frame_dados, text=texto_preco, bg="#1a1c1e", font=("Arial", 11, "bold"), fg="lightgreen")
            label_dados_valor.pack(pady=(0, 10), anchor="w")

            # frame descrição
            frame_dados_descricao = tk.Frame(frame_dados, bg="gray15", bd=1, relief=tk.SOLID, height=210)
            frame_dados_descricao.pack(fill=tk.X, expand=False, pady=(0, 15))
            frame_dados_descricao.pack_propagate(False)

            scroll_descricao = tk.Scrollbar(frame_dados_descricao, orient="vertical")
            scroll_descricao.pack(side=tk.RIGHT, fill=tk.Y)

            # Quebra de linha do texto da descrição do produto/serviços.
            text_descricao = tk.Text(
                frame_dados_descricao,
                bg="gray10", 
                fg="white",
                font=("Ariel", 10),
                wrap=tk.WORD,
                bd=0, highlightthickness=0,
                yscrollcommand=scroll_descricao.set
            )
            text_descricao.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            # inserindo os dados do produto na caixa rolante.
            scroll_descricao.config(command=text_descricao.yview)

            texto_real = dados.get("descricao", "Nenhuma descrição disponível.")
            text_descricao.insert(tk.END, texto_real)
            text_descricao.config(state=tk.DISABLED)

            # frame para agrupar os 2 botoes finais.
            frame_acoes2 = tk.Frame(frame_dados, bg="#1a1c1e")
            frame_acoes2.pack(fill=tk.X, pady=(15, 5))

            # Tratamento de futuros erros.
            try:
                # frame botão
                buttom_encomenda = tk.Button(frame_acoes2, text="Encomendar via WhatsApp", bg="#007acc", 
                                fg="white", font=("Ariel", 10, "bold"), padx=2, pady=5, 
                            command=lambda id_fixo=dados.get("id_produtos", dados.get("id")), tel_fixo=usuario["telefone"]: self.return_especial(
                        self.controles.Controle_da_Encomendas(id_fixo, entrada_qtd.get(), tel_fixo), 
                    self.root_vitrine
                    )
                )
                buttom_encomenda.pack(side=tk.LEFT, expand=False,padx=(5, 2))
            except Exception as e:
                print(f"Erro: {e}")

            
            entrada_qtd = tk.Spinbox(frame_acoes2, from_=1, to=5, width=2, font=("Arial", 11))
            entrada_qtd.pack(side=tk.RIGHT, pady=2, padx=(2, 2))

            # caixa de entrada e label da quantidade do produto a ser encomendada.
            label_qtd = tk.Label(frame_acoes2, text="Qtd.", bg="#1a1c1e", fg="white", font=("Arial", 10, "bold"))
            label_qtd.pack(side=tk.RIGHT, pady=5)

            # espaco entre o button e caixa de entrada da Qtd. produto.
            espaco = tk.Label(frame_acoes2, text="    ", bg="#1a1c1e", fg="white", font=("Arial", 10, "bold"))
            espaco.pack(side=tk.LEFT)
            

            # label linha
            separador = tk.Label(frame_dados, text="--------------------------------------------------------------", bg="#1a1c1e", fg="gray40")
            separador.pack(fill=tk.X ,pady=10)

            # button voltar(destroy)
            buttom_voltar = tk.Button(frame_dados, text="voltar", font=("Ariel", 10), 
                    bg="gray30", fg="white", padx=20,
                command= lambda: self.root_vitrine.destroy())
            buttom_voltar.pack(anchor="center", pady=3)
        else:
            print("Opção Invalida!")

    # Frame da janela agenda e seu escopo.
    def janela_agendar(self, usuario, dados_servico):
        # Defininções da frame.
        self.root_agenda = tk.Toplevel(self.root_vitrine)
        self.root_agenda.configure(bg="#1a1c1e")
        self.root_agenda.title("Loja")
        self.root_agenda.geometry("400x500")

        # Frame Principal
        frame_agenda = tk.Frame(self.root_agenda, bg="#1a1c1e")
        frame_agenda.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # Label Titulo
        label_agenda = tk.Label(frame_agenda, text="Agendar Serviço",font=("Ariel", 12, "bold"), fg="white", bg="#1a1c1e")
        label_agenda.pack(anchor="center", pady=(5, 20))

        # Label + entry da data do agendamento.           
        label_data = tk.Label(frame_agenda, text="Data:",font=("Ariel", 11, "bold"), fg="white", bg="#1a1c1e")
        label_data.pack(anchor="w", pady=(5, 2))

        entrada_data = DateEntry(frame_agenda, 
            width=20, background='#007acc', foreground='white', borderwidth=2,
                date_pattern='yyyy-mm-dd',
                    state="readonly", font=("Ariel", 11))
        entrada_data.pack(anchor="w", pady=(0, 15))

        # Label + ComboBox dos Horarios disponiveis para o agendamentos.
        label_hora = tk.Label(frame_agenda, text="Horários Disponíveis:", font=("Ariel", 11, "bold"), fg="white", bg="#1a1c1e")
        label_hora.pack(anchor="w", pady=(5, 2))

        lista_horarios = []

        entrada_hora = ttk.Combobox(frame_agenda, values=lista_horarios ,font=("Ariel", 11), state="readonly")
        entrada_hora.pack(anchor="w", pady=(0, 20))

        def loop_list(event): # Função chama a função de que filtra os horarios e trata corretamente o retorno.
            lista_horarios = self.controles.Filtro_de_Horarios(entrada_data.get_date())
            entrada_hora['values'] = lista_horarios

            if isinstance(lista_horarios, list) and len(lista_horarios) > 0:
                entrada_hora.current(0)
            else:
                entrada_hora.set('')

        entrada_data.bind("<<DateEntrySelected>>", loop_list)

        # Caixa de marcação de Notificação.
        self.var = tk.BooleanVar(value=False)
        caixa_marcacao = tk.Checkbutton(frame_agenda, text="Aceito receber notificação antecipada do Serviço.", 
                font=("Ariel", 8), activeforeground="white", activebackground="#1a1c1e", selectcolor="gray10",
            fg="white", padx=5, pady=5, bg="#1a1c1e", variable=self.var, justify=tk.LEFT, wraplength=350)
        caixa_marcacao.pack(anchor="w", pady=15)

        # Butão do agendamento
        button_agendar = tk.Button(frame_agenda, text="Confirmar Agendamento",
                    font=("Ariel", 11, "bold"), bg="#007acc", bd=1, fg="white", padx=25, pady=5,
                command= lambda: self.return_especial(self.controles.Controle_de_Agendamentos(usuario.get("telefone")  if isinstance(usuario, dict) else usuario
            , dados_servico.get("id"), entrada_data.get_date(), entrada_hora.get()),
        self.root_agenda))
        button_agendar.pack(anchor="center", pady=(50, 5))

        # Label linha
        separador = tk.Label(frame_agenda, text="-----------------------------------------------------------------------------------------", bg="#1a1c1e", fg="gray40")
        separador.pack(fill=tk.X, pady=(5, 10))

        # Botão voltar(destroy)
        buttom_voltar = tk.Button(frame_agenda, text="voltar", font=("Ariel", 10), 
                bg="gray30", fg="white", padx=25, pady=3,
            command= lambda: self.root_agenda.destroy())
        buttom_voltar.pack(anchor="center", pady=5)
        
        
# Garante que o Tkinter inicie o loop para a janela não fechar imediatamente e executar.
app = Prototipo() 
app.root_login.mainloop()