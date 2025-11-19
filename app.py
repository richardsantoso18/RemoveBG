import streamlit as st
from rembg import remove
from PIL import Image, ImageFilter
import io

st.title("Remove Background.")

uploaded = st.file_uploader("Upload image", type=["jpg","jpeg","png"])

if uploaded:

    # Load original
    img = Image.open(uploaded).convert("RGBA")

    # Remove background
    removed = remove(img)

    # --- FIX 1: Soften alpha edge biar gak ada putih-putih ---
    r, g, b, a = removed.split()

    # Blur tipis area alpha → hilangkan halo putih
    a = a.filter(ImageFilter.GaussianBlur(1.2))

    # Buat threshold lembut (feather)
    a = a.point(lambda x: 255 if x > 25 else 0)

    cleaned = Image.merge("RGBA", (r, g, b, a))

    # --- FIX 2: Pastikan download = PNG bukan raw bytes ---
    buf = io.BytesIO()
    cleaned.save(buf, format="PNG")
    png_bytes = buf.getvalue()

    col1, col2 = st.columns(2)

    with col1:
        st.image(img, caption="Original", use_container_width=True)

    with col2:
        st.image(cleaned, caption="Cleaned (No White Halo)", use_container_width=True)

    st.download_button(
        "Download PNG",
        data=png_bytes,
        file_name="removed_bg.png",
        mime="image/png"
    )
