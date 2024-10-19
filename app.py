import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords', quiet=True)

def create_wordcloud(text, colormap='viridis', background_color='white', stopwords=None, width=800, height=400):
    if stopwords is None:
        stopwords = set(STOPWORDS)
    else:
        stopwords = stopwords.union(STOPWORDS)

    try:
        wordcloud = WordCloud(width=width, height=height - 50,
                              background_color=background_color, colormap=colormap,
                              stopwords=stopwords).generate(text)

        fig = plt.figure(figsize=(10, 8))
        ax_wordcloud = fig.add_axes([0, 0.1, 1, 0.9])
        ax_wordcloud.imshow(wordcloud, interpolation='bilinear')
        ax_wordcloud.axis('off')

        ax_header = fig.add_axes([0, 0.95, 1, 0.05])
        ax_header.text(0.5, 0.5, "Created by Arsalan Jamal, Data Analyst", ha='center', va='center', fontsize=12)
        ax_header.axis('off')

        canvas = FigureCanvas(fig)
        img = io.BytesIO()
        canvas.print_png(img)
        img.seek(0)

        # --- Watermark Addition ---
        img_pil = Image.open(img)
        draw = ImageDraw.Draw(img_pil)

        try:
            # Try to use a system font; fallback to a bundled font if not found.
            font = ImageFont.truetype("arial.ttf", 36) # Replace 'arial.ttf' with a path to a suitable font if needed.
        except IOError:
            font = ImageFont.load_default()

        # Calculate watermark position
        text_width, text_height = draw.textsize("Arsalan Jamal", font=font)
        x = img_pil.width - text_width - 10
        y = img_pil.height - text_height - 10

        # Add watermark with transparency
        draw.text((x, y), "Arsalan Jamal", font=font, fill=(0, 0, 0, 128)) #RGBA - last value is alpha (transparency)

        # Save the watermarked image back to the buffer
        img_pil.save(img, "PNG")
        img.seek(0)

        return img

    except Exception as e:
        return f"An error occurred: {e}"

def download_wordcloud(img, filename="wordcloud.png"):
    img.seek(0)
    b64 = base64.b64encode(img.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{b64}" download="{filename}">Download WordCloud</a>'
    return href

# ... (Rest of your Streamlit code remains the same) ...

# Streamlit app setup
st.title("Word Cloud Generator")  # Set the title of the Streamlit app.
st.markdown(
    """
    <h2 style="color:red;">“Turn Words into Art. Simply.”</h2>
    <h3 style="color:blue;">A beautiful application Created by Arsalan Jamal</p>
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
