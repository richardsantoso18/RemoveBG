import streamlit as st
from rembg import remove
from PIL import Image, ImageFilter
import io

st.title("AI Background Remover")

uploaded = st.file_uploader("Upload image", type=["jpg","jpeg","png"])

if uploaded:

    img = Image.open(uploaded).convert("RGBA")

    # Remove background
    removed = remove(img)

    # ----- FIX: Soft feather edges, no white halo, no lines -----
    r, g, b, a = removed.split()

    # Blur alpha sedikit untuk rambut agar halus
    a = a.filter(ImageFilter.GaussianBlur(2.2))

    # TIPIS turunkan alpha → menghilangkan "garis rambut"
    a = a.point(lambda x: int(x * 0.95))

    cleaned = Image.merge("RGBA", (r, g, b, a))
    # ------------------------------------------------------------

    # Show images
    st.image(img, caption="Original", use_container_width=True)
    st.image(cleaned, caption="Clean Result (No White, No Lines)",
             use_container_width=True)

    # Download PNG
    buf = io.BytesIO()
    cleaned.save(buf, format="PNG")
    st.download_button(
        "Download PNG",
        data=buf.getvalue(),
        file_name="removed_bg.png",
        mime="image/png"
    )
