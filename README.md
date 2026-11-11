# 🌪️ TORNADOS: OS MAIORES DO MUNDO, DOS EUA E DO BRASIL

Site desenvolvido em **Python com Flask** que apresenta os maiores tornados já registrados, destacando os mais mortais, mais largos e mais caros do mundo.

O projeto conta com rankings por país, uma linha do tempo dos tornados no Brasil e informações sobre a **Escala Fujita**, utilizada para classificar a intensidade dos tornados.

## 🚀 COMO RODAR

1. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

2. Execute o projeto:

   ```bash
   python app.py
   ```

3. O site será aberto automaticamente no Opera.

   Caso não abra, acesse: http://127.0.0.1:5000

## 📁 ARQUIVOS DO PROJETO

```text
projeto/
│
├── app.py
├── requirements.txt
│
├── templates/
│   └── index.html
│
└── static/
    └── style.css
```

- **app.py:** servidor Python, dados e lógica do site.
- **templates/index.html:** estrutura HTML da página.
- **static/style.css:** estilos e aparência visual.
- **requirements.txt:** dependências necessárias para executar o projeto.

**Importante:** as pastas `templates` e `static` são obrigatórias no Flask e devem ficar no mesmo diretório do arquivo `app.py`.

## ⚙️ COMO FUNCIONA

O navegador solicita uma página, o Python processa os dados, aplica os filtros e organiza as informações.

O Flask utiliza o arquivo `index.html` como modelo e devolve ao navegador uma página HTML já pronta.

Os filtros funcionam por meio de links comuns, sem necessidade de JavaScript.

## 📊 INFORMAÇÕES

- 🌎 Maiores tornados do mundo.
- 🇺🇸 Rankings dos Estados Unidos.
- 🇧🇷 Linha do tempo dos tornados no Brasil.
- ☠️ Tornados mais mortais.
- 📏 Tornados com maiores larguras registradas.
- 💰 Tornados com maiores prejuízos financeiros.
- 🌪️ Explicação da Escala Fujita.

## ⚠️ OBSERVAÇÃO

Os números apresentados são aproximados e podem variar de acordo com as fontes consultadas. Para trabalhos acadêmicos ou pesquisas, recomenda-se conferir os dados em fontes oficiais.

---

**Desenvolvido em Python + Flask.**
