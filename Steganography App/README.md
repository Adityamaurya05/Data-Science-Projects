
# Image Steganography App

A simple web application built with [Streamlit](https://streamlit.io/) that allows users to hide text messages inside images (encoding) and extract hidden messages from images (decoding) using steganography. The app uses a password-based mechanism to secure the hidden messages.

The steganography technique employed here modifies the least significant bits (LSB) of the RGB values in an image to embed the binary representation of the text message, making the changes imperceptible to the human eye.

## Features

- **Encode**: Hide a text message in an image with a password.
- **Decode**: Extract a hidden message from an image using the correct password.
- **Secure**: Messages are prefixed with a password and delimited for reliable extraction.
- **Download**: Save the encoded image as a PNG file.
- **User-Friendly**: Intuitive interface built with Streamlit.

## Prerequisites

Before running the app, ensure you have the following installed:

- Python 3.7 or higher
- Required Python packages (listed in `requirements.txt`)

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/image-steganography-app.git
   cd image-steganography-app
   ```

2. **Create a Virtual Environment (Optional but Recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   If you don't have a `requirements.txt` file yet, install the dependencies manually:
   ```bash
   pip install streamlit pillow numpy
   ```

4. **Run the App**
   ```bash
   streamlit run app.py
   ```

   This will start the Streamlit server, and a browser window should open automatically with the app running at `http://localhost:8501`.

## Usage

### Encoding a Message
1. Select "Encode" from the sidebar.
2. Upload an image (PNG, JPG, or JPEG).
3. Enter the message you want to hide.
4. Provide a password to secure the message.
5. Click the "Download Encoded Image" button to save the resulting image with the hidden message.

### Decoding a Message
1. Select "Decode" from the sidebar.
2. Upload an encoded image.
3. Enter the password used during encoding.
4. The hidden message will be displayed if the password is correct.

## How It Works

- **Encoding**: 
  - The message is prefixed with the password and a delimiter (`###`).
  - The combined string is converted to binary.
  - The binary data is embedded into the least significant bits of the RGB channels of the image pixels.

- **Decoding**: 
  - The binary data is extracted from the image.
  - The delimiter (`###`) is used to identify the end of the message.
  - The password is verified, and the original message is returned if the password matches.

## Example

### Encoding
- **Input**: 
  - Image: `input.png`
  - Message: "Hello, World!"
  - Password: "secret123"
- **Output**: An encoded image (`encoded_image.png`) with the hidden message.

### Decoding
- **Input**: 
  - Image: `encoded_image.png`
  - Password: "secret123"
- **Output**: "Hello, World!"

- If the wrong password is provided (e.g., "wrongpass"), the output will be "Incorrect password!"

## Limitations

- The maximum message length depends on the image size (3 bits per pixel: 1 bit per RGB channel).
- Only PNG, JPG, and JPEG formats are supported for input images.
- The app does not handle transparency (alpha channel); images are converted to RGB.

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue for bugs, feature requests, or improvements.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m "Add some feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/), [Pillow](https://pillow.readthedocs.io/), and [NumPy](https://numpy.org/).
- Inspired by basic steganography techniques using LSB encoding.

---

Happy hiding and revealing messages! If you have any questions, feel free to reach out.


