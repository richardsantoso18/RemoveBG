import streamlit as st
from rembg import remove
from PIL import Image, ImageFilter
import io

st.set_page_config(page_title="AI Background Remover", layout="wide")
st.title("AI Background Remover")

# Upload image
uploaded = st.file_uploader("Upload image", type=["jpg","jpeg","png"])

if uploaded:
    # Load image asli
    img = Image.open(uploaded).convert("RGBA")
    st.subheader("Original Image")
    st.image(img, use_column_width=False)  # tampil asli tapi tidak stretch full

    # Remove background
    removed = remove(img)

    # Soft edges (hilangkan halo putih)
    r, g, b, a = removed.split()
    a = a.filter(ImageFilter.GaussianBlur(2))
    a = a.point(lambda x: int(x * 0.95))
    cleaned = Image.merge("RGBA", (r, g, b, a))

    # -------------------------
    # Resize untuk preview
    # -------------------------
    max_preview_width = 800  # maksimal lebar preview
    ratio = min(max_preview_width / cleaned.width, 1)  # jangan upscale
    preview = cleaned.resize((int(cleaned.width*ratio), int(cleaned.height*ratio)))

    st.subheader("Background Removed (Preview)")
    st.image(preview, use_column_width=False)

    # Download PNG (full size)
    buf = io.BytesIO()
    cleaned.save(buf, format="PNG")
    st.download_button(
        "Download PNG (Full Size)",
        data=buf.getvalue(),
        file_name="removed_bg.png",
        mime="image/png"
    )
