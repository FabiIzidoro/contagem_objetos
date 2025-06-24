📦 contagem_objetos
Sistema de contagem de objetos em imagens com Visão Computacional em Python, utilizando OpenCV e processamento digital de imagens.

🧩 Funcionalidades
Processamento de imagens para detectar e contar objetos mesmo em diferentes condições:

Objetos claros e escuros em fundos variados

Cores, texturas e agrupamentos distintos 
github.com

Segmentação avançada com binarização adaptativa, filtros morfológicos, transformada de distância e algoritmo Watershed 
github.com

Visualização aprimorada:

Máscaras intermediárias (dark_mask, light_mask, combined_mask, sure_foreground)

Contornos coloridos para cada objeto, com numeração legível 
github.com

Relatório final com resumo de contagens por imagem, exibido no console (ou janela adicional via summary_display.py) 
github.com

💾 Tecnologias
Python 3.7+

OpenCV (cv2)

NumPy

argparse

os 
github.com

🚀 Instalação
Clone o repositório:

bash
Copiar
Editar
git clone https://github.com/FabiIzidoro/contagem_objetos.git
cd contagem_objetos
Instale as dependências:

bash
Copiar
Editar
pip install -r requirements.txt
O arquivo requirements.txt já está incluído no repo 
github.com

▶️ Como usar
A estrutura local esperada:

less
Copiar
Editar
contagem_objetos/
├── images/              ← imagens de entrada (ex: chocolates.jpg, seeds.png)
├── processed_output/    ← onde os resultados são salvos automaticamente
├── main.py              ← script principal
├── count_objects.py     ← módulo principal de contagem/sequência de processamento
├── dependencias.txt
├── requirements.txt
└── README.md            ← este arquivo
Para processar todas as imagens padrões:

bash
Copiar
Editar
python main.py
Para processar uma imagem específica:

bash
Copiar
Editar
python main.py images/minha_imagem.jpg
A execução exibe janelas com cada etapa e salva máscaras intermediárias e resultados finais na pasta processed_output/. Pressione qualquer tecla para avançar em cada etapa 
github.com
.

🛠️ Parametrização & Ajustes
As seções de parâmetros condicional por tipo de imagem estão em main.py, com variáveis como:

thresh_block_size_dark, thresh_c_dark

dist_transform_factor, area_thresh

canny_low, canny_high

Ajuste-as conforme necessário se algum cenário específico (ex: moedas, jóias) não estiver sendo detectado corretamente. Verifique as máscaras de depuração em processed_output/ para identificar onde ocorre falha 
github.com
.

🐞 Solução de problemas
Reveja as máscaras de depuração (dark_mask, light_mask, etc.) para entender possíveis falhas.

Modifique os parâmetros uma variável por vez e observe o efeito.

Se necessário, crie/adapte summary_display.py para visualizar o resumo em GUI.

📄 Licença
MIT License — veja o arquivo LICENSE para mais detalhes 
github.com

🤝 Contribuições
Contribuições são bem-vindas! Para contribuir:

Faça um fork do repositório

Crie uma branch com a sua feature ou correção

Implemente e teste suas alterações

Envie um Pull Request descrevendo as mudanças

