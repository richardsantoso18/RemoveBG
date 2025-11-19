import streamlit as st
from rembg import remove
from PIL import Image

st.title("Remove Background")

uploaded_file = st.file_uploader("Upload image", type=["jpg","png","jpeg"])

if uploaded_file:
    col1, col2 = st.columns(2)

    with col1:
        st.image(uploaded_file, caption="Original", use_container_width=True)

    # Load upload
    input_img = Image.open(uploaded_file).convert("RGBA")

    # Remove background
    no_bg = remove(input_img)

    # FIX: Hilangkan area gelap/hitam dari alpha dengan cara clamp alpha
    r, g, b, a = no_bg.split()
    a = a.point(lambda i: 255 if i > 15 else 0)  # threshold biar ga jadi hitam item
    no_bg_fixed = Image.merge("RGBA", (r, g, b, a))

    with col2:
        st.image(no_bg_fixed, caption="Background Removed (FIXED)", use_container_width=True)

    # Download button
    st.download_button(
        label="Download PNG",
        data=no_bg_fixed.tobytes(),
        file_name="removed_bg.png",
        mime="image/png"
    )
