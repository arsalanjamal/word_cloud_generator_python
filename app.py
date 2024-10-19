# Import necessary libraries
import matplotlib.pyplot as plt  # For creating plots and visualizations
from wordcloud import WordCloud, STOPWORDS  # For generating word clouds; STOPWORDS provides a default list
import streamlit as st  # For creating interactive web applications
from PIL import Image  # For image processing (not directly used here, but potentially useful for future enhancements)
import io  # For working with in-memory binary streams (handling image data)
import base64  # For encoding binary data into text format (base64), used for creating the download link
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas  # Matplotlib function to render figures as images
import nltk  # For natural language processing tasks, specifically stop word handling
from nltk.corpus import stopwords  # Provides a list of common English stop words
nltk.download('stopwords', quiet=True)  # Download stopwords data; quiet=True suppresses download messages


def create_wordcloud(text, colormap='viridis', background_color='white', stopwords=None, width=800, height=400):
    """Generates a word cloud image with a header and customizable background color.

    Args:
        text (str): The text to generate the word cloud from.
        colormap (str, optional): The Matplotlib colormap to use. Defaults to 'viridis'.
        background_color (str, optional): The background color of the word cloud. Defaults to 'white'.
        stopwords (set, optional): A set of words to exclude from the word cloud. Defaults to None (uses default STOPWORDS).
        width (int, optional): The width of the word cloud image. Defaults to 800.
        height (int, optional): The height of the word cloud image. Defaults to 400.

    Returns:
        io.BytesIO: An in-memory binary stream containing the generated word cloud image, or an error message if an exception occurs.
    """
    # Handle stopwords: If no custom stopwords are provided, use the default set. Otherwise, combine custom and default stopwords.
    if stopwords is None:
        stopwords = set(STOPWORDS)
    else:
        stopwords = stopwords.union(STOPWORDS)

    try:
        # Create the word cloud object with specified parameters.
        wordcloud = WordCloud(width=width, height=height - 50,  # Reduced height to accommodate the header.
                              background_color=background_color, colormap=colormap,  # Set background color and colormap.
                              stopwords=stopwords).generate(text)  # Generate the word cloud from the input text.

        # Create a Matplotlib figure with two subplots: one for the word cloud and one for the header.
        fig = plt.figure(figsize=(10, 8))
        # Wordcloud subplot
        ax_wordcloud = fig.add_axes([0, 0.1, 1, 0.9])  # Define the position and size of the word cloud subplot.
        ax_wordcloud.imshow(wordcloud, interpolation='bilinear')  # Display the word cloud image.
        ax_wordcloud.axis('off')  # Hide the axes.

        # Header subplot
        ax_header = fig.add_axes([0, 0.95, 1, 0.05])  # Define the position and size of the header subplot.
        ax_header.text(0.5, 0.5, "Created by Arsalan Jamal, Data Analyst", ha='center', va='center', fontsize=12)  # Add the header text.
        ax_header.axis('off')  # Hide the axes.

        # Render the figure to an in-memory buffer.
        canvas = FigureCanvas(fig)
        img = io.BytesIO()
        canvas.print_png(img)
        img.seek(0)  # Reset the stream pointer to the beginning of the buffer.
        return img  # Return the image data as a BytesIO object.

    except Exception as e:
        return f"An error occurred: {e}"  # Return an error message if any exception occurs during word cloud generation.


def download_wordcloud(img, filename="wordcloud.png"):
    """Creates a download link for the generated word cloud image.

    Args:
        img (io.BytesIO): The image data as a BytesIO object.
        filename (str, optional): The desired filename for the downloaded image. Defaults to "wordcloud.png".

    Returns:
        str: An HTML link for downloading the image.
    """
    img.seek(0)  # Reset the stream pointer to the beginning.
    b64 = base64.b64encode(img.getvalue()).decode()  # Encode the image data to base64 for embedding in the HTML link.
    href = f'<a href="data:image/png;base64,{b64}" download="{filename}">Download WordCloud</a>'  # Create an HTML link for downloading the image.
    return href  # Return the HTML link.


# Streamlit app setup
st.title("Word Cloud Generator")  # Set the title of the Streamlit app.
st.markdown(
    """
    <h2 style="color:red;">“Turn Words into Art. Simply.”</h2>
    <p>A beautiful application Created by Arsalan Jamal</p>
    """,
    unsafe_allow_html=True
)
st.write(
    """
    A word cloud is a picture made of words. The bigger the word, the more times it appears in a piece of writing. It's like a summary of what the writing is about, shown in a colorful and easy-to-understand way.
    """
)
text = st.text_area("Enter text for word cloud:", height=200)  # Create a text area for user input.

# Colormap selection
colormaps = plt.colormaps()  # Get available colormaps from Matplotlib.
selected_colormap = st.selectbox("Select Colormap", colormaps)  # Create a dropdown for selecting a colormap.

# Background color selection
background_colors = ["white", "black", "grey", "lightgrey", "darkgrey", "lightblue", "lightcoral"]  # Add more colors as needed.
selected_background_color = st.selectbox("Select Background Color", background_colors)  # Dropdown for background color selection

# Stopwords input
use_automatic_stopwords = st.checkbox("Use Automatic Stop Words")  # Checkbox to enable/disable automatic stop word selection
custom_stopwords_input = st.text_input("Enter custom stop words (comma-separated):", disabled=use_automatic_stopwords)  # Text input for custom stopwords; disabled if automatic selection is enabled.

custom_stopwords = set()  # Initialize an empty set for custom stopwords.
if custom_stopwords_input:
    custom_stopwords = set(word.strip().lower() for word in custom_stopwords_input.split(','))  # Process custom stopwords input.


# Button to trigger word cloud generation
if st.button("Generate Word Cloud"):
    if text:
        stop_words_to_use = set(STOPWORDS)  # Start with default stop words
        if use_automatic_stopwords:
            stop_words_to_use = stop_words_to_use.union(set(stopwords.words('english')))  # Add NLTK's English stopwords

        stop_words_to_use = stop_words_to_use.union(custom_stopwords)  # Include custom stop words if any are provided

        img = create_wordcloud(text, colormap=selected_colormap, background_color=selected_background_color, stopwords=stop_words_to_use)  # Generate word cloud.
        if isinstance(img, str):  # Error handling
            st.error(img)  # Display error message if an error occurred.
        else:
            st.image(img)  # Display the generated word cloud image.
            st.markdown(download_wordcloud(img), unsafe_allow_html=True)  # Display the download link.
    else:
        st.warning("Please enter some text.")  # Display a warning if no text is entered.
