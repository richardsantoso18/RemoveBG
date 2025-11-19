import streamlit as st
from rembg import remove
from PIL import Image, ImageFilter
import io

st.set_page_config(page_title="AI Background Remover", layout="wide")
st.title("AI Background Remover – Clean & Soft Edges")

# Upload image
uploaded = st.file_uploader("Upload image", type=["jpg","jpeg","png"])

if uploaded:
    # Load image
    img = Image.open(uploaded).convert("RGBA")
    st.subheader("Original Image")
    st.image(img, use_column_width=True)

    # Remove background
    removed = remove(img)

    # Soft alpha edges (hilangkan halo putih)
    r, g, b, a = removed.split()
    a = a.filter(ImageFilter.GaussianBlur(2))  # smooth edges
    a = a.point(lambda x: int(x * 0.95))       # feather alpha
    cleaned = Image.merge("RGBA", (r, g, b, a))

    st.subheader("Background Removed")
    st.image(cleaned, use_column_width=True)

    # Download PNG
    buf = io.BytesIO()
    cleaned.save(buf, format="PNG")
    st.download_button(
        "Download PNG",
        data=buf.getvalue(),
        file_name="removed_bg.png",
        mime="image/png"
    )
