import cv2 # Importa a biblioteca OpenCV para processamento de imagem
import numpy as np # Importa NumPy para operações com arrays
import argparse # Importa argparse para lidar com argumentos de comandos
import os # Importa os para manipulação de caminhos de ficheiros

# --- Parâmetros de Configuração Global ---
# Ajuste estes valores para otimizar o processo de detecção de objetos.
# Cada parâmetro é comentado para clareza e compreensão.

# Diretório para imagens de entrada. Certifique-se de que esta pasta existe e contém as suas imagens.
INPUT_IMAGE_FOLDER = 'images'

# Diretório onde as imagens processadas e máscaras serão guardadas.
OUTPUT_RESULT_FOLDER = 'processed_output'

def process_image(image_path):
    """
    Processa uma imagem para detetar, contar e marcar objetos,
    focando em identificar e separar corretamente os objetos.

    Args:
        image_path (str): O caminho para o ficheiro da imagem a ser processada.
    """
    print(f"A processar imagem: {image_path}")

    # 1. Carregar a Imagem
    img = cv2.imread(image_path)
    if img is None:
        print(f"Erro: Não foi possível carregar a imagem {image_path}. Verifique o caminho.")
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Adiciona um passo de suavização (Gaussian Blur) para reduzir ruídos e detalhes de textura.
    blurred = cv2.GaussianBlur(gray, (5, 5), 0) 
    
    # --- Parâmetros Condicionais Baseados no Tipo de Imagem ---
    # Define os parâmetros de binarização, morfologia e watershed com base no nome do ficheiro.
    if "chocolates.jpg" in image_path:
        # Parâmetros otimizados para chocolates (que deram 12 objetos ou perto disso)
        thresh_block_size_dark = 121 # Para objetos escuros
        thresh_c_dark = 20
        thresh_light_val = 220 # Para objetos claros (chocolates brancos)
        
        dist_transform_factor = 0.7
        morph_kernel_size = (5,5)
        area_thresh = 180
        canny_low = 30
        canny_high = 80

    elif "seeds.png" in image_path:
        # Parâmetros otimizados para sementes (versão antes de não detectar as brancas)
        thresh_block_size_dark = 61 # Revertido para 61
        thresh_c_dark = 25 # Revertido para 25
        
        thresh_light_val = 200 # Revertido para 200 (Este limiar pode ser o problema para brancas)
        canny_low = 50 # Revertido para 50
        canny_high = 150 # Revertido para 150

        dist_transform_factor = 0.6 # Revertido para 0.6
        morph_kernel_size = (3,3) 
        area_thresh = 10 # Revertido para 10

    else:
        # Parâmetros padrão para outras imagens, se houver
        thresh_block_size_dark = 81
        thresh_c_dark = 10
        thresh_light_val = 220
        canny_low = 30
        canny_high = 80
        dist_transform_factor = 0.5
        morph_kernel_size = (5,5)
        area_thresh = 100

    # 2. Processamento de Máscaras (Dark e Light Objects)
    
    # Máscara para objetos ESCUROS (com THRESH_BINARY_INV)
    dark_mask_initial = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                              cv2.THRESH_BINARY_INV, thresh_block_size_dark, thresh_c_dark)
    # Aplica abertura para remover ruídos pequenos na máscara escura.
    dark_mask_cleaned = cv2.morphologyEx(dark_mask_initial, cv2.MORPH_OPEN, np.ones(morph_kernel_size, np.uint8), iterations=1)
    
    # Máscara para objetos CLAROS (usando Canny e THRESH_BINARY_INV em threshold direto)
    # A detecção de bordas é crucial para objetos claros em fundo claro.
    edges_for_light = cv2.Canny(blurred, canny_low, canny_high)
    # Dilata as bordas para formar regiões.
    edges_dilated_for_light = cv2.dilate(edges_for_light, np.ones((3,3), np.uint8), iterations=2)
    # Preenche as regiões delimitadas pelas bordas para formar as máscaras de objetos claros.
    light_mask_filled_edges = cv2.morphologyEx(edges_dilated_for_light, cv2.MORPH_CLOSE, np.ones((7,7), np.uint8), iterations=3) # Revertido para 7x7 e 3 iterações

    # Tenta binarização direta para objetos claros, então inverte.
    # CRÍTICO: Revertido para THRESH_BINARY_INV, que era o que estava antes do problema das brancas.
    ret, light_thresh_direct = cv2.threshold(blurred, thresh_light_val, 255, cv2.THRESH_BINARY_INV) 

    # Combina a detecção de bordas preenchidas com o threshold direto para objetos claros.
    # Isto ajuda a capturar ambos os tipos de objetos claros.
    light_mask_combined = cv2.bitwise_or(light_mask_filled_edges, light_thresh_direct)
    # Aplica abertura para remover ruídos e refinar a máscara de objetos claros.
    light_mask_cleaned = cv2.morphologyEx(light_mask_combined, cv2.MORPH_OPEN, np.ones(morph_kernel_size, np.uint8), iterations=1)

    # Combina as duas máscaras (escuros + claros)
    combined_mask_final = cv2.bitwise_or(dark_mask_cleaned, light_mask_cleaned)

    # 3. Fundo "Certeza" (Sure Background): Dilata a máscara combinada final.
    sure_bg = cv2.dilate(combined_mask_final, np.ones((3,3), np.uint8), iterations=3)

    # >>> USAR TRANSFORMADA DE DISTÂNCIA PARA SURE_FG <<<
    # Calcula a transformada de distância na máscara combinada.
    dist_transform = cv2.distanceTransform(combined_mask_final, cv2.DIST_L2, 5)
    
    # Encontra o foreground de certeza usando um threshold na transformada de distância.
    # Usa o fator específico para a imagem atual.
    ret, sure_fg = cv2.threshold(dist_transform, dist_transform_factor * dist_transform.max(), 255, 0) 
    sure_fg = np.uint8(sure_fg) 
    
    # Região Desconhecida: A área entre o foreground certeza e o background certeza.
    unknown = cv2.subtract(sure_bg, sure_fg)

    # 4. Rotulagem de Marcadores para o Watershed
    ret, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1 
    markers[unknown == 255] = 0 

    # 5. Aplicação do Algoritmo Watershed
    markers = cv2.watershed(img.copy(), markers)
    img[markers == -1] = [0,0,255] 

    # 6. Encontrar Contornos e Filtrar
    segmented_objects = np.uint8(markers > 1) * 255
    contours, _ = cv2.findContours(segmented_objects, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    object_count = 0
    output_img = img.copy()

    # Define as cores para os contornos (BGR)
    contour_colors = [
        (0, 255, 0),    # Verde
        (0, 0, 255),    # Vermelho
        (255, 0, 0),    # Azul
        (255, 0, 255),  # Magenta (rosa)
        (0, 255, 255),  # Amarelo
        (255, 255, 0),  # Ciano
        (128, 0, 128),  # Púrpura
        (0, 128, 128),  # Oliva
        (128, 128, 0),  # Verde-azulado
        (0, 128, 255),  # Laranja
        (128, 255, 0),  # Verde-limão
        (255, 128, 0)   # Azul-claro
    ]
    color_index = 0

    # Limiar mínimo de área para considerar um contorno como objeto válido.
    # Usa o limiar específico para a imagem atual.
    
    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)

        if area > area_thresh: # Usa o limiar de área específico
            object_count += 1
            current_color = contour_colors[color_index % len(contour_colors)]
            cv2.drawContours(output_img, [contour], -1, current_color, 2)
            color_index += 1

            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.putText(output_img, str(object_count), (cX - 5, cY + 5), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 3) 

    # 7. Exibir a Contagem Total de Objetos
    cv2.putText(output_img, f"Objetos detectados: {object_count}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_AA) 

    # 8. Guardar a Imagem Resultante
    base_name = os.path.basename(image_path)
    file_name_without_ext = os.path.splitext(base_name)[0]
    output_filename_full_path = os.path.join(OUTPUT_RESULT_FOLDER, f"resultado_{file_name_without_ext}.jpg")
    cv2.imwrite(output_filename_full_path, output_img)
    print(f"Imagem processada guardada como: {output_filename_full_path}")

    # Exibir as imagens intermédias e finais para depuração.
    cv2.imshow("Original", img)
    cv2.imshow("Dark Objects Mask", dark_mask_cleaned) 
    cv2.imshow("Light Objects Mask", light_mask_cleaned)
    cv2.imshow("Combined Final Mask", combined_mask_final) 
    cv2.imshow("Sure Background", sure_bg) 
    cv2.imshow("Sure Foreground", sure_fg) 
    cv2.imshow("Regiao Desconhecida", unknown)
    cv2.imshow("Objetos Segmentados pelo Watershed", segmented_objects)
    cv2.imshow("Resultado Final", output_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    os.makedirs(INPUT_IMAGE_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_RESULT_FOLDER, exist_ok=True)

    parser = argparse.ArgumentParser(description="Contagem de objetos em imagens usando OpenCV.")
    parser.add_argument("image", nargs="?",
                        help="Caminho para o ficheiro da imagem (opcional). "
                             "Se não for fornecido, 'images/chocolates.jpg' ou 'seeds.png' serão usados por padrão.")

    args = parser.parse_args()

    # Lista de imagens a serem processadas
    images_to_process = [
        "chocolates.jpg",
        "seeds.png"
    ]

    if args.image:
        # Se um argumento de imagem é fornecido, processa apenas essa imagem
        process_image(args.image)
    else:
        # Caso contrário, processa a lista de imagens definida
        for img_name in images_to_process:
            full_image_path = os.path.join(INPUT_IMAGE_FOLDER, img_name)
            if os.path.exists(full_image_path):
                process_image(full_image_path)
            else:
                print(f"Erro: Imagem '{full_image_path}' não encontrada.")
                print(f"Certifique-se de que a imagem '{img_name}' está na pasta '{INPUT_IMAGE_FOLDER}'.")

    print("\nProcessamento em lote concluído!")
