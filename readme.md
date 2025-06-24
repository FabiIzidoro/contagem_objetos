
# 📦 contagem_objetos

Sistema de contagem de objetos em imagens com Visão Computacional em Python, utilizando OpenCV e processamento digital de imagens.

## 🧩 Funcionalidades

- Processamento de imagens para detectar e contar objetos mesmo em diferentes condições:
  - Objetos claros e escuros em fundos variados
  - Cores, texturas e agrupamentos distintos
- Segmentação avançada com binarização adaptativa, filtros morfológicos, transformada de distância e algoritmo Watershed
- Visualização aprimorada:
  - Máscaras intermediárias (dark_mask, light_mask, combined_mask, sure_foreground)
  - Contornos coloridos para cada objeto, com numeração legível
- Relatório final com resumo de contagens por imagem, exibido no console (ou janela adicional via `summary_display.py`)

## 💾 Tecnologias

- Python 3.7+
- OpenCV (cv2)
- NumPy
- argparse
- os

## 🚀 Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/FabiIzidoro/contagem_objetos.git
   cd contagem_objetos
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Como usar

Estrutura local esperada:
```
contagem_objetos/
├── images/              ← imagens de entrada (ex: chocolates.jpg, seeds.png)
├── processed_output/    ← onde os resultados são salvos automaticamente
├── main.py              ← script principal
├── count_objects.py     ← módulo principal de contagem/sequência de processamento
├── dependencias.txt
├── requirements.txt
└── README.md            ← este arquivo
```

Para processar todas as imagens padrões:
```bash
python main.py
```

Para processar uma imagem específica:
```bash
python main.py images/minha_imagem.jpg
```

A execução exibe janelas com cada etapa e salva máscaras intermediárias e resultados finais na pasta `processed_output/`. Pressione qualquer tecla para avançar em cada etapa.

## 🛠️ Parametrização & Ajustes

As seções de parâmetros por tipo de imagem estão em `main.py`, com variáveis como:

- `thresh_block_size_dark`, `thresh_c_dark`
- `dist_transform_factor`, `area_thresh`
- `canny_low`, `canny_high`

Ajuste conforme necessário caso algum cenário (ex: moedas, sementes) não esteja sendo detectado corretamente. Verifique as máscaras de depuração em `processed_output/` para entender possíveis falhas.

## 🐞 Solução de problemas

1. Reveja as máscaras de depuração (`dark_mask`, `light_mask`, etc.) para entender falhas de segmentação.
2. Modifique os parâmetros gradualmente e observe os efeitos.
3. Se quiser, utilize ou adapte o `summary_display.py` para visualizar o resumo da contagem em interface gráfica.

## 📄 Licença

MIT License — veja o arquivo `LICENSE` para mais detalhes.

## 🤝 Contribuições

Contribuições são bem-vindas!

1. Faça um fork do repositório.
2. Crie uma branch com sua feature ou correção.
3. Implemente e teste.
4. Abra um Pull Request.

## 💡 Melhorias futuras sugeridas

- Adição de testes automatizados (pytest)
- Interface gráfica (Tkinter, PyQT ou similar)
- Suporte a vídeo ou webcam (contagem em tempo real)
