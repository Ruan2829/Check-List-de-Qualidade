import streamlit as st
import os
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import base64
import matplotlib.pyplot as plt

# Criar pasta de fotos se não existir
if not os.path.exists("fotos"):
    os.makedirs("fotos")

# Criar classe PDF com cabeçalho, rodapé e logotipo
class PDF(FPDF):
    def header(self):
        # Decodificar e salvar o logotipo
        logo_base64 = "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"  # Substitua pelo código Base64 do seu logotipo
        logo_data = base64.b64decode(logo_base64)
        logo_path = "temp_logo.jpeg"
        with open(logo_path, "wb") as temp_logo:
            temp_logo.write(logo_data)
        
        # Inserir logotipo no PDF
        self.image(logo_path, 10, 8, 33)  
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Checklist de Qualidade - WEG AGW 110-2.1 MW', border=False, ln=True, align='C')
        self.set_font('Arial', '', 10)
        self.cell(0, 10, 'Operação e Manutenção', border=False, ln=True, align='C')
        self.ln(20)

        # Definir os campos do lado direito 
        
        self.set_font("Arial", "B", 8)           # Fonte Arial, negrito, tamanho 10

        # Linha 1: REV
        self.set_xy(160, 10)                      # Posição da célula "REV." (coluna 1)
        self.cell(20, 10, "REV.:", border=False, align="R")      # Campo rótulo "REV."
        self.cell(30, 10, "00", border=False, ln=1)   # Valor da revisão, ln=1 quebra linha
        self.set_font("Arial", "", 8)            # Fonte normal, tamanho 8
        
    """ # Linha 4: Cód.
        self.set_x(160)                           # Mesma coluna
        self.cell(20, 10, "Cód.:", border=False, align="R")      # Campo rótulo "Cód."
        self.cell(20, 10, "IQONY-INSPQ-01", border=False, ln=1)  # Código do relatório
        self.set_font("Arial", "", 8)            # Fonte normal, tamanho 8
"""
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()} de {{nb}}  |  Iqony Solutions do Brasil', align='C')

# Função para criar PDF com múltiplas fotos e formatação correta

# Criar PDF com checklist e assinatura corretamente
def gerar_pdf_multifotos(inspecao_data):
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    # Adicionar informações gerais
    pdf.ln(30)
    for chave, valor in inspecao_data["geral"].items():
        pdf.set_font("Arial", 'B', 10)  # Negrito para a chave
        pdf.cell(50, 10, txt=f"{chave}:", ln=0)  # Largura fixa p/ alinhar valores
        pdf.set_font("Arial", '', 10)  # Normal para o valor preenchido
        pdf.cell(0, 10, txt=f"{valor}", ln=1)
    pdf.ln(10)

    # Adicionar uma página para cada sistema inspecionado
    for sistema, detalhes in inspecao_data["sistemas"].items():
        pdf.add_page()
        pdf.ln(20)
        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(0, 10, txt=sistema, ln=True)
        pdf.ln(5)

        pdf.set_font("Arial", size=10)
        pdf.cell(0, 10, txt="Observações:", ln=True)
        pdf.multi_cell(0, 10, txt=detalhes['observacoes'])
        pdf.ln(5)

        # Adicionar avaliação por estrelas
        pdf.cell(0, 10, txt=f"Avaliação: {detalhes['avaliacao']} / 5", ln=True)
        pdf.ln(5)

        # Inserir até 4 fotos organizadas em uma grade (2 colunas por 2 linhas)
        foto_width = 90  # Largura da imagem
        foto_height = 60  # Altura da imagem
        col_spacing = 10  # Espaço entre colunas
        row_spacing = 10  # Espaço entre linhas
        x_start = 10  # Posição inicial no eixo x
        y_start = pdf.get_y()  # Posição inicial no eixo y

        for i, foto_path in enumerate(detalhes['fotos'][:4]):  # Limita a 4 fotos por página
            try:
                x_pos = x_start + (i % 2) * (foto_width + col_spacing)
                y_pos = y_start + (i // 2) * (foto_height + row_spacing)
                pdf.image(foto_path, x=x_pos, y=y_pos, w=foto_width, h=foto_height)
            except Exception as e:
                pdf.cell(0, 10, txt=f"Erro ao carregar imagem {i+1}: {str(e)}", ln=True)

        pdf.ln(70)  # Adiciona espaço ao final da seção

    # 🔹 ADICIONANDO ASSINATURA APÓS TODOS OS SISTEMAS 🔹
    pdf.add_page()
    pdf.ln(20)
    pdf.set_font("Arial", size=12, style='B')
    pdf.cell(0, 10, "Assinatura do Inspetor", ln=True, align='C')
 
    pdf.ln(15)  # Espaço antes da linha de assinatura
    y_signature = pdf.get_y()  # Captura a posição da linha
    pdf.line(60, y_signature, 150, y_signature)  # Linha para assinatura

    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, f"Nome: {inspecao_data['geral']['Inspetor']}", ln=True, align='C')

    # 🔹 Criar gráfico de avaliação por sistema

    sistemas = list(inspecao_data["sistemas"].keys())
    avaliacoes = [detalhes["avaliacao"] for detalhes in inspecao_data["sistemas"].values()]

    plt.figure(figsize=(10, 5))
    plt.barh(sistemas, avaliacoes)
    plt.xlabel('Avaliação (0 a 5)')
    plt.title('Avaliação por Sistema')
    plt.xlim(0, 5)
    plt.tight_layout()

    grafico_path = "avaliacoes_sistemas.png"
    plt.savefig(grafico_path, dpi=200)
    plt.close()

    # 🔹 Adicionar gráfico ao PDF
    pdf.add_page()
    pdf.set_font("Arial", 'B', 12)
    pdf.ln(20)
    pdf.cell(0, 10, "Avaliação por Sistema", ln=True, align='C')
    pdf.ln(10)
    pdf.image(grafico_path, x=10, w=190)

    return pdf


    return pdf

# Função para exibir estrelas clicáveis
def estrelas_clicaveis(label, key, max_stars=5, default_stars=3):
    stars = st.session_state.get(key, default_stars)
    cols = st.columns(max_stars)
    for i in range(max_stars):
        if i < stars:
            estrela = "⭐"
        else:
            estrela = "☆"
        if cols[i].button(estrela, key=f"{key}_{i}"):
            st.session_state[key] = i + 1
    return st.session_state.get(key, default_stars)

# Título da aplicação
st.title("Checklist de Qualidade - WEG AGW 110-2.1 MW")

# Seção de informações gerais
st.header("Informações Gerais")
complexo = st.text_input("Complexo Eólico", key="complexo")
wtg_numero = st.text_input("Número da Turbina", key="wtg_numero")
inspetor = st.text_input("Inspetor", key="inspetor")
data_inspecao = st.date_input("Data da Inspeção", key="data_inspecao")
motivo = st.text_input("Motivo da Parada", key="motivo")
Numero_relatorio = st.text_input("Número do Relatório", key="Numero_relatorio")

# Lista de sistemas inspecionados
sistemas = [
    "Ground", "Cubiculo MT", "Torre", "Elevador", "Iluminação", "Escada de Acesso",
    "Linha de Vida", "Yaw Deck", "Transformador",  "Paineis de Controle",
    "Conversores de Potência", "Estrutura da Nacele", "Sistema de Freio", 
    "Guincho de Serviço", "Sensores Ambientais", "Sistema de Arrefecimento",
    "Gerador", "Sistema de Lubrificação", "Pitch", "Sistema Hidráulico", 
     "Pás"
]

# Dicionário para armazenar dados de inspeção
dados_inspecao = {"geral": {}, "sistemas": {}}

dados_inspecao["geral"] = {
    "Complexo Eólico": complexo,
    "Número da Turbina": wtg_numero,
    "Inspetor": inspetor,
    "Data da Inspeção": data_inspecao.strftime("%d/%m/%Y"),
    "Motivo da Parada": motivo,
    "Número do Relatório": Numero_relatorio
}

for i, sistema in enumerate(sistemas):
    st.subheader(sistema)

    # Adicionando chave única para evitar erro de ID duplicado
    observacoes = st.text_area(f"Observações para {sistema}", key=f"obs_{i}")

    # Avaliação por estrelas
    estrelas = estrelas_clicaveis(f"Avalie o sistema {sistema}", key=f"stars_{i}")

    # Upload de fotos
    fotos = st.file_uploader(
        f"Carregar fotos para {sistema}",
        accept_multiple_files=True,
        type=["jpg", "jpeg", "png"],
        key=f"fotos_{i}"
    )

    # Salvar fotos localmente
    fotos_paths = []
    if fotos:
        for foto in fotos:
            foto_path = os.path.join("fotos", foto.name)
            with open(foto_path, "wb") as f:
                f.write(foto.read())
            fotos_paths.append(foto_path)

    dados_inspecao["sistemas"][sistema] = {
        "observacoes": observacoes,
        "avaliacao": estrelas,
        "fotos": fotos_paths
    }

# Botão para gerar PDF
if st.button("Gerar PDF do Checklist"):
    pdf = gerar_pdf_multifotos(dados_inspecao)
    pdf_output = "checklist_qualidade.pdf"
    pdf.output(pdf_output)

    with open(pdf_output, "rb") as pdf_file:
        st.download_button(
            label="Baixar Checklist como PDF",
            data=pdf_file,
            file_name="checklist_qualidade.pdf",
            mime="application/pdf",
        )

    