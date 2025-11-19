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
    st.image(img, use_column_width=False)

    # Remove background
    removed = remove(img)

    # Soft edges
    r, g, b, a = removed.split()
    a = a.filter(ImageFilter.GaussianBlur(2))
    a = a.point(lambda x: int(x * 0.95))
    cleaned = Image.merge("RGBA", (r, g, b, a))

    # -------------------------
    # Resize untuk preview 500 px
    # -------------------------
    preview_width = 500
    ratio = preview_width / cleaned.width
    preview_height = int(cleaned.height * ratio)
    preview = cleaned.resize((preview_width, preview_height))

    # Tampilkan tengah
    st.subheader("Background Removed (Preview)")
    st.markdown(
        f"<div style='text-align:center'><img src='data:image/png;base64,{io.BytesIO(preview.tobytes()).getvalue().hex()}' width='{preview_width}' /></div>",
        unsafe_allow_html=True
    )

    # Alternatif lebih mudah: gunakan col untuk tengah
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image(preview, use_column_width=False)

    # Download full size
    buf = io.BytesIO()
    cleaned.save(buf, format="PNG")
    st.download_button(
        "Download PNG (Full Size)",
        data=buf.getvalue(),
        file_name="removed_bg.png",
        mime="image/png"
    )
