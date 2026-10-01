
CREATE TABLE public.Tabela_Servicos (
  id_servicos integer GENERATED ALWAYS AS IDENTITY NOT NULL,
  nome character varying NOT NULL,
  valor real NOT NULL,
  descricao text NOT NULL,
  Img_servico text NOT NULL,
  CONSTRAINT Tabela_Servicos_pkey PRIMARY KEY (id_servicos)
);
CREATE TABLE public.Tabela_Produtos (
  id_produtos integer GENERATED ALWAYS AS IDENTITY NOT NULL,
  nome character varying NOT NULL,
  valor real NOT NULL,
  descricao text NOT NULL,
  Qtd. integer NOT NULL,
  Img_produto text NOT NULL,
  CONSTRAINT Tabela_Produtos_pkey PRIMARY KEY (id_produtos)
);
CREATE TABLE public.Tabela_Horarios (
  id_horarios integer GENERATED ALWAYS AS IDENTITY NOT NULL,
  horarios time without time zone NOT NULL,
  CONSTRAINT Tabela_Horarios_pkey PRIMARY KEY (id_horarios)
);
CREATE TABLE public.Tabela_Contas (
  tel_cliente character varying NOT NULL,
  nome character varying NOT NULL,
  senha text NOT NULL,
  CONSTRAINT Tabela_Contas_pkey PRIMARY KEY (tel_cliente)
);
CREATE TABLE public.Tabela_Encomendas (
  id_encomendas integer GENERATED ALWAYS AS IDENTITY NOT NULL,
  cliente_tel character varying NOT NULL,
  hora timestamp with time zone NOT NULL,
  produto integer NOT NULL,
  Qtd. integer NOT NULL,
  status boolean,
  CONSTRAINT Tabela_Encomendas_pkey PRIMARY KEY (id_encomendas),
  CONSTRAINT Tabela_Encomendas_cliente_tel_fkey FOREIGN KEY (cliente_tel) REFERENCES public.Tabela_Contas(tel_cliente),
  CONSTRAINT Tabela_Encomendas_produto_fkey FOREIGN KEY (produto) REFERENCES public.Tabela_Produtos(id_produtos)
);

CREATE TABLE public.Tabela_Agendamentos (
  id_agenda integer GENERATED ALWAYS AS IDENTITY NOT NULL,
  tel_cliente character varying NOT NULL,
  data_hora timestamp with time zone NOT NULL,
  servico integer NOT NULL,
  CONSTRAINT Tabela_Agendamentos_pkey PRIMARY KEY (id_agenda),
  CONSTRAINT Tabela_Agendamentos_tel_cliente_fkey FOREIGN KEY (tel_cliente) REFERENCES public.Tabela_Contas(tel_cliente),
  CONSTRAINT Tabela_Agendamentos_servico_fkey FOREIGN KEY (servico) REFERENCES public.Tabela_Servicos(id_servicos)
);