import streamlit as st
from rembg import remove
from PIL import Image, ImageFilter
import io

st.set_page_config(page_title="AI Background Remover", layout="wide")
st.title("AI Background Remover – Clean & Soft Edges with Border")

# -----------------------------
# Upload Image
# -----------------------------
uploaded = st.file_uploader("Upload image", type=["jpg","jpeg","png"])

if uploaded:
    img = Image.open(uploaded).convert("RGBA")

    # -----------------------------
    # Resize original untuk preview max 500px
    # -----------------------------
    preview_width = 500
    ratio = min(preview_width / img.width, 1)
    preview_height = int(img.height * ratio)
    original_preview = img.resize((int(img.width*ratio), preview_height))

    st.subheader("Original Image (Preview)")
    # Border + tengah
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown(
            f"<div style='border:3px solid black; display:inline-block;'><img src='data:image/png;base64,{io.BytesIO(original_preview.tobytes()).getvalue().hex()}' width='{preview_width}'></div>",
            unsafe_allow_html=True
        )
        # Alternatif lebih mudah: pakai st.image + style col
        st.image(original_preview, use_column_width=False)

    # -----------------------------
    # Remove Background
    # -----------------------------
    removed = remove(img)

    # Soft edges
    r, g, b, a = removed.split()
    a = a.filter(ImageFilter.GaussianBlur(2))
    a = a.point(lambda x: int(x * 0.95))
    cleaned = Image.merge("RGBA", (r, g, b, a))

    # Resize cleaned untuk preview max 500px
    ratio_clean = min(preview_width / cleaned.width, 1)
    preview_height_clean = int(cleaned.height * ratio_clean)
    cleaned_preview = cleaned.resize((preview_width, preview_height_clean))

    st.subheader("Background Removed (Preview)")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown(
            f"<div style='border:3px solid black; display:inline-block;'><img src='data:image/png;base64,{io.BytesIO(cleaned_preview.tobytes()).getvalue().hex()}' width='{preview_width}'></div>",
            unsafe_allow_html=True
        )
        st.image(cleaned_preview, use_column_width=False)

    # -----------------------------
    # Download full size
    # -----------------------------
    buf = io.BytesIO()
    cleaned.save(buf, format="PNG")
    st.download_button(
        "Download PNG (Full Size)",
        data=buf.getvalue(),
        file_name="removed_bg.png",
        mime="image/png"
    )
