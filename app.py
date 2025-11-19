import streamlit as st
from rembg import remove
from PIL import Image, ImageFilter
from streamlit_drawable_canvas import st_canvas
import io
import os

st.set_page_config(page_title="AI Background Remover + Manual Fix", layout="wide")
st.title("Background Remover")

# -----------------------------
# Upload Image
# -----------------------------
uploaded = st.file_uploader("Upload image", type=["jpg","jpeg","png"])

if uploaded:
    # Original image
    original = Image.open(uploaded).convert("RGBA")

    st.subheader("Original Image")
    st.image(original, use_column_width=True)

    # -----------------------------
    # Remove Background
    # -----------------------------
    st.subheader("Auto Remove Background")
    removed = remove(original)

    # Soft alpha edges
    r, g, b, a = removed.split()
    a = a.filter(ImageFilter.GaussianBlur(2))  # smooth edges
    a = a.point(lambda x: int(x * 0.95))       # slight feather
    removed_cleaned = Image.merge("RGBA", (r, g, b, a))

    st.image(removed_cleaned, caption="Background Removed", use_column_width=True)

    # Save temporary file for canvas background
    tmp_file = "removed_temp.png"
    removed_cleaned.save(tmp_file)

    # -----------------------------
    # Manual Edit Canvas
    # -----------------------------
    st.subheader("Manual Erase / Restore Tool")
    mode = st.radio("Mode:", ["Erase", "Restore"])
    brush_size = st.slider("Brush Size", 5, 80, 35)

    canvas_result = st_canvas(
        fill_color="rgba(255,0,0,0)",
        stroke_width=brush_size,
        stroke_color="white",
        background_image=Image.open(tmp_file),
        height=removed_cleaned.height,
        width=removed_cleaned.width,
        drawing_mode="freedraw",
        key="canvas",
    )

    # -----------------------------
    # Process Manual Edits
    # -----------------------------
    if canvas_result.image_data is not None:
        mask = canvas_result.image_data[:, :, 3]  # alpha channel from drawing
        mask = mask > 0  # convert to boolean

        edited = removed_cleaned.copy()
        edited_np = np.array(edited)

        if mode == "Erase":
            edited_np[mask] = [0, 0, 0, 0]  # make transparent
        else:  # Restore
            original_np = np.array(original)
            edited_np[mask] = original_np[mask]

        edited_img = Image.fromarray(edited_np, mode="RGBA")

        st.subheader("Edited Result")
        st.image(edited_img, use_column_width=True)

        # Download button
        buf = io.BytesIO()
        edited_img.save(buf, format="PNG")
        st.download_button(
            "Download Edited PNG",
            data=buf.getvalue(),
            file_name="edited_result.png",
            mime="image/png"
        )

    # Clean up temporary file
    if os.path.exists(tmp_file):
        os.remove(tmp_file)
