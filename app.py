import streamlit as st
import numpy as np
import os
import time
import qrcode
import cv2
from PIL import Image

# QR Code setup
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4
)
timestr = time.strftime("%Y%m%d-%H%M%S")

# Function to load image


def load_image(img):
    return Image.open(img)


# --- Sidebar Navigation ---
st.sidebar.title("QR Code App")
page = st.sidebar.radio("Navigation", ["Home", "Decode QR", "About"])

# Sidebar Footer
st.sidebar.markdown("---")
st.sidebar.markdown(
    "This app lets you generate and decode QR codes easily.\n\n"
    "Follow me on [Twitter](https://x.com/danny_amah) 🐦"
)

# --- Main Pages ---
if page == "Home":
    st.title("Generate QR Code")
    with st.form(key='myqr_form'):
        raw_text = st.text_area("Enter text or a link:")
        submit_button = st.form_submit_button("Generate QR Code")

    if submit_button and raw_text.strip():
        col1, col2 = st.columns(2)

        with col1:
            # Generate QR
            qr.add_data(raw_text)
            qr.make(fit=True)
            img = qr.make_image(fill_color='black', back_color='white')

            # Save & display
            os.makedirs('image_folder', exist_ok=True)
            img_filename = f'generate_img_{timestr}.png'
            path_for_images = os.path.join('image_folder', img_filename)
            img.save(path_for_images)

            final_image = load_image(path_for_images)
            st.image(final_image, caption="Your QR Code")

        with col2:
            st.subheader("Original Text")
            st.write(raw_text)

elif page == "Decode QR":
    st.title("Decode a QR Code")
    image_file = st.file_uploader(
        "Upload a QR code image", type=['jpg', 'png', 'jpeg'])

    if image_file:
        file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
        opencv_image = cv2.imdecode(file_bytes, 1)

        col1, col2 = st.columns(2)
        with col1:
            st.image(opencv_image, channels="BGR", caption="Uploaded Image")
        with col2:
            st.subheader("Decoded Text")
            det = cv2.QRCodeDetector()
            retval, points, straight_qrcode = det.detectAndDecode(opencv_image)
            st.write(retval if retval else "No QR code detected.")

else:
    st.title("About This App")
    st.write(
        "This app lets you quickly generate QR codes from text or URLs, "
        "and decode QR codes from uploaded images. Built with Python, Streamlit, and OpenCV."
    )
