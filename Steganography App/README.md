### Image Steganography App

## Overview

This is a simple image steganography web application built using Streamlit. It allows users to hide secret messages inside images and later retrieve them using a password.

### Features:

  * **Hide a Secret Message:** Encode text into an image with password protection.
  * **Extract a Hidden Message:** Retrieve and decrypt the hidden message only if the correct password is provided.
  * **User-friendly UI:** Built with Streamlit for easy interaction.
  * **Password protected** It has inbult password encoder and decoder for safer hidden message

### How It Works:
* **Encoding Process:**
The user uploads an image.
Enters a secret message and sets a password.
The application hides the message inside the image by modifying the least significant bits of pixels.
The modified image is available for download.

* **Decoding Process:**

The user uploads the steganographic image.
Enters the password. The app extracts and displays the hidden message if the password is correct.

### Dependencies
* **streamlit** for the web interface.
* **PIL (Pillow)** for image processing.
* **numpy** for pixel manipulation.


### Contributing:

We welcome contributions from the community\! Please follow these guidelines:

1.  **Fork the Repository:** Create a fork of this repository on GitHub.
2.  **Create a New Branch:** Create a new branch for your feature or bug fix.
3.  **Make Your Changes:** Commit your changes to your new branch.
4.  **Push Your Changes:** Push your branch to your forked repository.
5.  **Create a Pull Request:** Submit a pull request to the main repository.

**License:**

This project is licensed under the [MIT License](https://www.google.com/url?sa=E&source=gmail&q=LICENSE).

**Let's build amazing mobile apps together\!**
