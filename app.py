import streamlit as st
from streamlit_drawable_canvas import st_canvas
from rembg import remove
from PIL import Image
import numpy as np
import io

st.title("Background Remover")

uploaded = st.file_uploader("Upload image", type=["jpg","jpeg","png"])

if uploaded:

    # Original
    original = Image.open(uploaded).convert("RGBA")
    removed = remove(original)

    st.subheader("Auto Remove Result")
    st.image(removed, use_container_width=True)

    st.subheader("Manual Edit (Erase / Restore)")

    mode = st.radio("Mode:", ["Erase", "Restore"])
    brush = st.slider("Brush size", 5, 80, 35)

    canvas = st_canvas(
        fill_color="rgba(255, 0, 0, 0)",  # Transparent marker
        stroke_width=brush,
        stroke_color="white",  # just for drawing cursor
        background_image=removed,
        height=removed.height,
        width=removed.width,
        drawing_mode="freedraw",
        key="canvas",
    )

    if canvas.image_data is not None:
        mask = canvas.image_data[:, :, 3]  # alpha (drawn strokes)
        mask = mask > 0  # convert to True/False

        edited = np.array(removed).copy()

        if mode == "Erase":
            # Set erased pixels to transparent
            edited[mask] = [0, 0, 0, 0]

        else:
            # Restore from original
            original_np = np.array(original)
            edited[mask] = original_np[mask]

        edited_img = Image.fromarray(edited, mode="RGBA")

        st.subheader("Edited Output")
        st.image(edited_img, use_container_width=True)

        # Download button
        buffer = io.BytesIO()
        edited_img.save(buffer, format="PNG")
        st.download_button(
            "Download Edited PNG",
            buffer.getvalue(),
            "edited.png",
            mime="image/png",
        )
