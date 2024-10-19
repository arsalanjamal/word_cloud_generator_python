# Import necessary libraries
import streamlit as st  # For creating the Streamlit web app
from wordcloud import WordCloud, STOPWORDS  # For generating word clouds
import matplotlib.pyplot as plt  # For displaying images
from PIL import Image  # For image manipulation (masks)
import os  # For file system operations (optional)
import numpy as np #For using numpy arrays with masks

# Define themes for the word cloud (background color and colormap)
themes = {
    "Default": None,  # No specific theme
    "Ocean": {"background_color": "skyblue", "colormap": "Blues"},  # Blue theme
    "Sunset": {"background_color": "orange", "colormap": "Reds"},  # Red/Orange theme
    "Forest": {"background_color": "darkgreen", "colormap": "Greens"},  # Green theme
    "Night": {"background_color": "black", "colormap": "magma"},  # Dark theme
    "Pastel": {"background_color": "white", "colormap": "Pastel1"},  # Pastel colors
    "Dark": {"background_color": "#222222", "colormap": "viridis"},  # Dark gray theme
    "Vibrant": {"background_color": "white", "colormap": "gist_rainbow"},  # Vibrant colors
    "Monochrome": {"background_color": "white", "colormap": "gray"},  # Gray scale
    "Earth": {"background_color": "#663300", "colormap": "terrain"}  # Brown/Green theme
}

# Define styles for the word cloud (shapes using masks)
styles = {
    "Circle": None,  # Default circular shape
    "Square": {"mask": np.array(Image.open("square_mask.png"))},  # Uses a square mask image
    "Heart": {"mask": np.array(Image.open("heart_mask.png"))},  # Uses a heart mask image
    "Cloud": {"mask": np.array(Image.open("cloud_mask.png"))},  # Uses a cloud mask image
    # Add more styles with different masks as needed
}


def create_wordcloud(text, theme="Default", style="Circle", stopwords=None):
    """Generates a word cloud image."""

    # Handle stopwords: use default or user-provided
    if stopwords is None:
        stopwords = set(STOPWORDS)
    else:
        stopwords.update(STOPWORDS)

    # Get theme parameters (or defaults)
    wc_kwargs = themes.get(theme, {})
    # Get style parameters (or defaults)
    style_kwargs = styles.get(style, {})
    # Combine theme and style parameters
    wc_kwargs.update(style_kwargs)

    # Generate the word cloud
    wordcloud = WordCloud(**wc_kwargs).generate(text)
    # Display the word cloud using matplotlib
    plt.figure(figsize=(10, 8))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    return plt  # Return the matplotlib plot


def load_text_from_file(file_path):
    """Loads text from a file, handling potential errors."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
        return text
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"An error occurred: {e}"


# Streamlit app code
import streamlit as st
import numpy as np

st.title("Word Cloud Generator")  # Set the title of the app

uploaded_file = st.file_uploader("Choose a text file", type=["txt"])  # File uploader

if uploaded_file is not None:
    # Decode the uploaded file (handle potential encoding issues)
    text = uploaded_file.read().decode("utf-8")
    text = load_text_from_file(uploaded_file.name)  # Use the error-handling function

    selected_theme = st.selectbox("Select Theme", list(themes.keys()))  # Theme selection
    selected_style = st.selectbox("Select Style", list(styles.keys()))  # Style selection

    if st.button("Generate Word Cloud"):  # Button to trigger word cloud generation
        # Get custom stop words from user input
        custom_stopwords = st.text_input("Enter custom stop words (comma-separated):")
        if custom_stopwords:
            stopwords = set(custom_stopwords.lower().split(","))
        else:
            stopwords = None

        # Generate and display the word cloud
        plt = create_wordcloud(text, selected_theme, selected_style, stopwords)
        st.pyplot(plt)  # Display the plot in Streamlit


# Function to create mask images (you'll need to run this separately or integrate it better)
from PIL import Image, ImageDraw

def create_mask(shape, size=200):
    """Creates a mask image with the specified shape and saves it as a PNG."""
    img = Image.new("RGB", (size, size), "white")  # Create a white image
    draw = ImageDraw.Draw(img)  # Get a drawing context

    if shape == "square":
        draw.rectangle([(0, 0), (size, size)], fill="black")  # Draw a black square
    elif shape == "circle":
        draw.ellipse([(0, 0), (size, size)], fill="black")  # Draw a black circle
    # Add more shapes as needed...
    img.save(f"{shape}_mask.png")  # Save the image as a PNG file

# Example usage:  (Uncomment to generate masks if you don't have them already)
#create_mask("square")
#create_mask("circle")
#create_mask("heart") #You will need to create the heart shape yourself using an image editor or code.
#create_mask("cloud") #You will need to create the cloud shape yourself using an image editor or code.
