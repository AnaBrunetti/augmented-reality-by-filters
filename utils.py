import streamlit as st
import cv2

### Change path variable to run ###
path = 'C:/Ana/cs7/augmented-reality-by-filters/venv/Lib/site-packages/cv2/data/'
face_cascade = cv2.CascadeClassifier(path + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(path + 'haarcascade_eye.xml')


def build_sidebar():
    st.sidebar.write("## Aplicação de Realidade Aumentada por meio de filtros.")
    nomes = [
        "Ana Carolina de M. Brunetti RA N464828 - CC7Q18",
        "Raphael Bassi Alves da Silva RA F119556 - CC6P18",
        "Wellington Fagundes de Oliveira RA N429160 - CC7Q18",
        "Samuel Batista Costa RA N3792C4 - CC7P18",
        "Sávio Henrique Cangussu dos Santos RA T870577 - CC7P18"
    ]
    st.sidebar.write("## Grupo:")
    for nome in sorted(nomes):
        st.sidebar.write(f"{nome}")

    st.sidebar.write()
    st.sidebar.markdown(
        """ 
        ### Ferramentas utilizadas
        - Python 3.9
        - opencv-python
        - streamlit
        """
    )


def put_sticker_on_head(img):
    witch = cv2.imread('images/pokemon-filter.png')
    original_witch_h, original_witch_w, witch_channels = witch.shape
    witch_gray = cv2.cvtColor(witch, cv2.COLOR_BGR2GRAY)
    ret, original_mask = cv2.threshold(witch_gray, 10, 255, cv2.THRESH_BINARY_INV)
    original_mask_inv = cv2.bitwise_not(original_mask)
    img_h, img_w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        face_w = w
        face_h = h
        face_x1 = x
        face_x2 = face_x1 + face_w
        face_y1 = y
        witch_width = int(2.1 * face_w)
        witch_height = int(witch_width * original_witch_h / original_witch_w)
        witch_x1 = face_x2 - int(face_w/2) - int(witch_width/2)
        witch_x2 = witch_x1 + witch_width
        witch_y1 = face_y1 - int(face_h*1.25)
        witch_y2 = witch_y1 + witch_height
        if witch_x1 < 0:
            witch_x1 = 0
        if witch_y1 < 0:
            witch_y1 = 0
        if witch_x2 > img_w:
            witch_x2 = img_w
        if witch_y2 > img_h:
            witch_y2 = img_h
        witch_width = witch_x2 - witch_x1
        witch_height = witch_y2 - witch_y1
        witch = cv2.resize(witch, (witch_width, witch_height), interpolation=cv2.INTER_AREA)
        mask = cv2.resize(original_mask, (witch_width, witch_height), interpolation=cv2.INTER_AREA)
        mask_inv = cv2.resize(original_mask_inv, (witch_width, witch_height), interpolation=cv2.INTER_AREA)
        roi = img[witch_y1:witch_y2, witch_x1:witch_x2]
        roi_bg = cv2.bitwise_and(roi, roi, mask=mask)
        roi_fg = cv2.bitwise_and(witch, witch, mask=mask_inv)
        dst = cv2.add(roi_bg, roi_fg)
        img[witch_y1:witch_y2, witch_x1:witch_x2] = dst
    return img


def process_types(img, type_selectbox, color_selectbox):
    result_image = img
    if type_selectbox == "Colocar adesivo":
        result_image = put_sticker_on_head(img)
    return result_image


def process_video(col_right):
    type_selectbox = st.selectbox(
        "Escolha o tipo de processamento",
        ("Colocar adesivo",)
    )
    color_selectbox = None
    process = st.button('Iniciar o vídeo')
    with col_right:
        st.markdown(
            """
            ### Uma janela irá abrir no seu computador com o vídeo rodando.
            """
        )

    if process:
        cap = cv2.VideoCapture(0)
        while True:
            ret, img = cap.read()
            result_image = process_types(img, type_selectbox, color_selectbox)
            cv2.imshow('img', result_image)
            if cv2.waitKey(1) == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
