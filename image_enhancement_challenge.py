import streamlit as st
from PIL import Image, ImageEnhance, ImageOps, ImageFilter

def apply_enhancement(image, option, value):
    if option == 'Brightness':
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(value)
    elif option == 'Contrast':
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(value)
    elif option == 'Rotation':
        return image.rotate(value, expand=True)
    elif option == 'Grayscale':
        return ImageOps.grayscale(image)
    elif option == 'Blur':
        return image.filter(ImageFilter.GaussianBlur(value))
    else:
        return image


st.title("Image Manipulation App")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    if 'history' not in st.session_state:
        st.session_state.history = []
        st.session_state.current_image = image

    st.image(st.session_state.current_image, caption='Current Image', use_column_width=True)

    
    option = st.selectbox('Select an enhancement feature', 
                          ['Brightness', 'Contrast', 'Rotation', 'Grayscale', 'Blur'])

    if option in ['Brightness', 'Contrast']:
        value = st.slider('Select a value', 0.1, 3.0, 1.0)
    elif option == 'Blur':
        value = st.slider('Select a blur radius', 0.0, 10.0, 0.0)
    elif option == 'Rotation':
        value = st.slider('Select rotation angle', 0, 360, 0)
    else:
        value = None

    if st.button('Apply'):
        enhanced_image = apply_enhancement(st.session_state.current_image, option, value)
        st.image(enhanced_image, caption='Enhanced Image', use_column_width=True)
        st.session_state.history.append((enhanced_image.copy(), option, value))
        st.session_state.current_image = enhanced_image

    if st.button('Undo last step') and st.session_state.history:
        st.session_state.history.pop()
        if st.session_state.history:
            st.session_state.current_image = st.session_state.history[-1][0]
        else:
            st.session_state.current_image = Image.open(uploaded_file)
        st.image(st.session_state.current_image, caption='Reverted Image', use_column_width=True)

    if st.button('Save final result'):
        
        if st.session_state.history:
            final_image = st.session_state.history[-1][0]
            final_image.save("final_image.png")
            st.success("Final image saved!")
        else:
            st.warning("No enhancements applied yet.")

    st.write("Applied features history:")
    for idx, (_, opt, val) in enumerate(st.session_state.history):
        st.write(f"{idx + 1}: {opt} with value {val}")
