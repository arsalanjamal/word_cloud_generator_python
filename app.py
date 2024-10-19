# Import necessary libraries
import matplotlib.pyplot as plt  # Library for creating plots and visualizations.
from wordcloud import WordCloud, STOPWORDS  # Library for generating word clouds.  STOPWORDS provides a default list of common words to ignore.
import streamlit as st  # Library for creating interactive web applications.
from PIL import Image  # Library for image processing.  Not directly used in this code, but included for potential future expansion.
import io  # Library for working with in-memory binary streams.  Used to handle the image data.
import base64  # Library for encoding binary data into text format (base64). Used for creating the download link.
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas  # Matplotlib function to render figures as images.


def create_wordcloud(text, colormap='viridis', stopwords=None, width=800, height=400):
    """Generates a word cloud image with a header."""
    # Handle stopwords: If no custom stopwords are provided, use the default set. Otherwise, combine custom and default stopwords.
    if stopwords is None:
        stopwords = set(STOPWORDS)  
    else:
        stopwords = stopwords.union(STOPWORDS)  

    try:
        # Create the word cloud object with specified parameters.
        wordcloud = WordCloud(width=width, height=height - 50,  # Reduced height to accommodate the header.
                              background_color='white', colormap=colormap, # Set background color and colormap.
                              stopwords=stopwords).generate(text)  # Generate the word cloud from the input text.

        # Create a Matplotlib figure with two subplots: one for the word cloud and one for the header.
        fig = plt.figure(figsize=(10, 8))  
        #Wordcloud subplot
        ax_wordcloud = fig.add_axes([0, 0.1, 1, 0.9])  # Define the position and size of the word cloud subplot.
        ax_wordcloud.imshow(wordcloud, interpolation='bilinear')  # Display the word cloud image.
        ax_wordcloud.axis('off')  # Hide the axes.

        #Header subplot
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
    """Creates a download link for the generated word cloud image."""
    img.seek(0)  # Reset the stream pointer to the beginning.
    b64 = base64.b64encode(img.getvalue()).decode()  # Encode the image data to base64 for embedding in the HTML link.
    href = f'<a href="data:image/png;base64,{b64}" download="{filename}">Download WordCloud</a>'  # Create an HTML link for downloading the image.
    return href  # Return the HTML link.


# Streamlit app setup
st.title("Word Cloud Generator")  # Set the title of the Streamlit app.

text = st.text_area("Enter text for word cloud:", height=200)  # Create a text area for user input.

# Colormap selection
colormaps = plt.colormaps()  # Get available colormaps from Matplotlib.
selected_colormap = st.selectbox("Select Colormap", colormaps)  # Create a dropdown for selecting a colormap.

# Stopwords input
custom_stopwords_input = st.text_input("Enter custom stop words (comma-separated):")  # Text input for custom stopwords.
custom_stopwords = set()  # Initialize an empty set for custom stopwords.
if custom_stopwords_input:
    custom_stopwords = set(word.strip().lower() for word in custom_stopwords_input.split(','))  # Process custom stopwords input.


# Button to trigger word cloud generation
if st.button("Generate Word Cloud"):
    if text:
        img = create_wordcloud(text, colormap=selected_colormap, stopwords=custom_stopwords)  # Generate word cloud.
        if isinstance(img, str):  # Error handling
            st.error(img)  # Display error message if an error occurred.
        else:
            st.image(img)  # Display the generated word cloud image.
            st.markdown(download_wordcloud(img), unsafe_allow_html=True)  # Display the download link.
    else:
        st.warning("Please enter some text.")  # Display a warning if no text is entered.
