import streamlit as st
from PIL import Image
import numpy as np
import io

# Function to convert text to binary
def text_to_binary(message):
    return ''.join(format(ord(char), '08b') for char in message)

# Function to convert binary to text
def binary_to_text(binary_message):
    chars = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    return ''.join(chr(int(byte, 2)) for byte in chars if byte)

# Function to encode message into image with password
def encode_image(image, message, password):
    img = Image.open(image)
    img = img.convert('RGB')
    array = np.array(img, dtype=np.uint8)
    height, width, _ = array.shape

    secure_message = password + "::" + message + "###"  # Delimiter to signify end of message
    binary_message = text_to_binary(secure_message)
    msg_len = len(binary_message)
    index = 0

    for row in range(height):
        for col in range(width):
            if index < msg_len:
                r, g, b = array[row, col]
                r = (r & ~1) | int(binary_message[index])
                index += 1
                if index < msg_len:
                    g = (g & ~1) | int(binary_message[index])
                    index += 1
                if index < msg_len:
                    b = (b & ~1) | int(binary_message[index])
                    index += 1
                array[row, col] = [r, g, b]
            else:
                break
        if index >= msg_len:
            break

    encoded_image = Image.fromarray(array)
    return encoded_image

# Function to decode message from image with password verification
def decode_image(image, password):
    img = Image.open(image)
    img = img.convert('RGB')
    array = np.array(img, dtype=np.uint8)

    binary_message = ""
    delimiter = text_to_binary("###")
    
    for row in array:
        for pixel in row:
            r, g, b = pixel
            binary_message += str(r & 1) + str(g & 1) + str(b & 1)
            if delimiter in binary_message:
                binary_message = binary_message[:binary_message.index(delimiter)]
                message = binary_to_text(binary_message)
                stored_password, hidden_message = message.split("::", 1)
                if stored_password == password:
                    return hidden_message
                else:
                    return "Incorrect password!"
    
    return "No hidden message found."

# Streamlit App
def main():
    st.title("Image Steganography App")
    st.write("Hide and extract text messages in images using steganography.")

    option = st.sidebar.selectbox("Choose an option", ["Encode", "Decode"], key="navigation")

    if option == "Encode":
        st.header("Encode a Message into an Image")
        uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"], key="encode_uploader")
        message = st.text_area("Enter the message to hide", key="encode_message")
        password = st.text_input("Enter a password", type="password", key="encode_password")

        if uploaded_file and message and password:
            st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
            st.write("Encoding message...")
            
            encoded_image = encode_image(uploaded_file, message, password)
            
            # Convert image to bytes
            img_bytes = io.BytesIO()
            encoded_image.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            st.image(encoded_image, caption='Encoded Image', use_column_width=True)
            st.write("Message encoded successfully!")
            
            # Download button
            st.download_button(
                label="Download Encoded Image",
                data=img_bytes,
                file_name="encoded_image.png",
                mime="image/png"
            )
    
    elif option == "Decode":
        st.header("Decode a Message from an Image")
        uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"], key="decode_uploader")
        password = st.text_input("Enter the password", type="password", key="decode_password")
        
        if uploaded_file and password:
            st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
            st.write("Decoding message...")
            
            decoded_message = decode_image(uploaded_file, password)
            st.success(f"Decoded Message: {decoded_message}")

if __name__ == "__main__":
    main()
