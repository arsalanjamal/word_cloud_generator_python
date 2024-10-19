import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import streamlit as st
from PIL import Image
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def create_wordcloud(text, colormap='viridis', stopwords=None, width=800, height=400):
    """Generates a word cloud image with a header."""
    if stopwords is None:
        stopwords = set(STOPWORDS)
    else:
        stopwords = stopwords.union(STOPWORDS)

    try:
        wordcloud = WordCloud(width=width, height=height - 50,  # Reduced height for header
                              background_color='white', colormap=colormap,
                              stopwords=stopwords).generate(text)

        fig = plt.figure(figsize=(10, 8))
        #Wordcloud
        ax_wordcloud = fig.add_axes([0, 0.1, 1, 0.9]) #adjust position
        ax_wordcloud.imshow(wordcloud, interpolation='bilinear')
        ax_wordcloud.axis('off')

        #Header
        ax_header = fig.add_axes([0, 0.95, 1, 0.05]) #adjust position
        ax_header.text(0.5, 0.5, "Created by Arsalan Jamal, Data Analyst", ha='center', va='center', fontsize=12)
        ax_header.axis('off')

        canvas = FigureCanvas(fig)
        img = io.BytesIO()
        canvas.print_png(img)
        img.seek(0)
        return img


    except Exception as e:
        return f"An error occurred: {e}"



def download_wordcloud(img, filename="wordcloud.png"):
    """Saves the word cloud image as a PNG and allows for download."""
    img.seek(0)
    b64 = base64.b64encode(img.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{b64}" download="{filename}">Download WordCloud</a>'
    return href


# Streamlit app
st.title("Word Cloud Generator")

text = st.text_area("Enter text for word cloud:", height=200)

# Colormap selection
colormaps = plt.colormaps()
selected_colormap = st.selectbox("Select Colormap", colormaps)

# Stopwords input
custom_stopwords_input = st.text_input("Enter custom stop words (comma-separated):")
custom_stopwords = set()
if custom_stopwords_input:
    custom_stopwords = set(word.strip().lower() for word in custom_stopwords_input.split(','))


if st.button("Generate Word Cloud"):
    if text:
        img = create_wordcloud(text, colormap=selected_colormap, stopwords=custom_stopwords)
        if isinstance(img, str):  # Error handling
            st.error(img)
        else:
            st.image(img)
            st.markdown(download_wordcloud(img), unsafe_allow_html=True)
    else:
        st.warning("Please enter some text.")
