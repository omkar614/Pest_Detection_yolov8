import streamlit as st
from PIL import Image
from ultralytics import YOLO
import requests

# Load the YOLO model
model = YOLO('best.pt')

# Google Search API function (with error handling)
API_KEY = 'AIzaSyBRF6Iuas79xOSjXX8a-I1XGLTZQ-zFzV0'
SEARCH_ENGINE_ID = '101d67946fc174845'

def search_pesticide_for_insect(insect_name):
    """Search Google for pesticides based on the detected pest name."""
    query = f"{insect_name} pesticide"
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={SEARCH_ENGINE_ID}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        search_results = data.get('items', [])
        
        if search_results:
            return search_results[0]['title'], search_results[0]['link']
        else:
            return "No relevant pesticide found.", ""
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}", ""

st.title('🌿 Pest Detection and Pesticide Recommendation')

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'png', 'jpeg'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    if st.button('Detect and Search'):
        results = model(image)
        results_image = results[0].plot()
        st.image(results_image, caption='Detection Results', use_column_width=True)

        st.subheader('Detected Pests and Web Search Results:')
        for result in results:
            for box in result.boxes:
                pest_class = model.names[int(box.cls)]
                confidence = float(box.conf)  # Convert tensor to float

                # Display detected pest with confidence
                st.markdown(f"""
                ### 🐛 Detected Pest: **{pest_class}**  
                **Confidence:** {confidence:.2%}
                """, unsafe_allow_html=True)

                # Search for pesticide recommendation
                title, link = search_pesticide_for_insect(pest_class)
                if link:
                    st.write(f"🔍 Top Search Result: [{title}]({link})")
                else:
                    st.write(f"🔍 {title}")
