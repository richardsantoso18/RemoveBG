import streamlit as st
from rembg import remove, new_session
from PIL import Image, ImageFilter
import io

def clean_edges(image: Image.Image, blur_amount=1):
    image = image.convert("RGBA")
    r, g, b, a = image.split()

    # Kurangi halo dengan aman
    a = a.point(lambda x: max(0, x - 5))

    # Blur ringan agar pinggiran halus
    a = a.filter(ImageFilter.GaussianBlur(blur_amount))

    return Image.merge("RGBA", (r, g, b, a))

st.title("Background Remover .")

uploaded = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])

session = new_session("u2net_human_seg")

if uploaded:
    image = Image.open(uploaded).convert("RGB")
    st.image(image, caption="Original", use_column_width=True)

    with st.spinner("Removing background..."):
        removed = remove(image, session=session)
        output = clean_edges(removed)

    st.image(output, caption="Cleaned Result", use_column_width=True)

    buf = io.BytesIO()
    output.save(buf, format="PNG")
    st.download_button("Download PNG", buf.getvalue(), "result.png")
