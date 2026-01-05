import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from transformers import pipeline
import textwrap
import os

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="AIGen Retail Creative Optimizer",
    layout="wide"
)

st.title("🛍️ AIGen Retail Creative Optimizer")
st.write("AI-powered tool to generate retail ad creatives automatically")

# -------------------------------
# LOAD AI MODEL (TEXT GENERATION)
# -------------------------------
@st.cache_resource
def load_text_model():
    return pipeline(
        "text-generation",
        model="gpt2",
        max_length=80
    )

text_generator = load_text_model()

# -------------------------------
# SIDEBAR INPUTS
# -------------------------------
st.sidebar.header("Input Details")

platform = st.sidebar.selectbox(
    "Select Advertising Platform",
    ["Instagram", "Amazon Ads", "Google Ads"]
)

product_name = st.sidebar.text_input("Product Name", "Wireless Earbuds")
product_desc = st.sidebar.text_area(
    "Product Description",
    "High-quality wireless earbuds with noise cancellation and long battery life."
)

cta_options = {
    "Instagram": "Shop Now",
    "Amazon Ads": "Buy Now",
    "Google Ads": "Learn More"
}

uploaded_image = st.sidebar.file_uploader(
    "Upload Product Image",
    type=["jpg", "png"]
)

generate_btn = st.sidebar.button("🚀 Generate Creatives")

# -------------------------------
# HELPER FUNCTIONS
# -------------------------------
def generate_ad_copy(product_name, product_desc, platform):
    prompt = f"""
    Create a catchy ad headline and caption for {product_name}.
    Description: {product_desc}
    Platform: {platform}
    """

    result = text_generator(prompt, num_return_sequences=1)[0]["generated_text"]

    lines = result.split(".")
    headline = lines[0][:50]
    caption = ". ".join(lines[1:3])

    return headline.strip(), caption.strip(), cta_options[platform]


def create_ad_image(base_image, headline, cta, size):
    img = base_image.resize(size)
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arial.ttf", 36)
        font_cta = ImageFont.truetype("arial.ttf", 28)
    except:
        font_title = ImageFont.load_default()
        font_cta = ImageFont.load_default()

    wrapped_headline = textwrap.fill(headline, width=20)

    draw.rectangle(
        [(0, img.height - 180), (img.width, img.height)],
        fill=(0, 0, 0, 180)
    )

    draw.text(
        (20, img.height - 160),
        wrapped_headline,
        fill="white",
        font=font_title
    )

    draw.rectangle(
        [(20, img.height - 60), (200, img.height - 20)],
        fill=(255, 165, 0)
    )

    draw.text(
        (40, img.height - 55),
        cta,
        fill="black",
        font=font_cta
    )

    return img

# -------------------------------
# MAIN LOGIC
# -------------------------------
if generate_btn and uploaded_image:
    base_image = Image.open(uploaded_image).convert("RGB")

    st.subheader("📢 Generated Ad Copy")

    headline, caption, cta = generate_ad_copy(
        product_name,
        product_desc,
        platform
    )

    col1, col2 = st.columns(2)
    col1.metric("Headline", headline)
    col2.metric("CTA", cta)
    st.write("**Caption:**", caption)

    st.subheader("🎨 Generated Ad Creatives")

    platform_sizes = {
        "Instagram": [(1080, 1080), (1080, 1350)],
        "Amazon Ads": [(1200, 628)],
        "Google Ads": [(728, 90), (300, 250)]
    }

    for size in platform_sizes[platform]:
        ad_image = create_ad_image(
            base_image,
            headline,
            cta,
            size
        )

        st.image(
            ad_image,
            caption=f"{platform} Creative {size[0]}x{size[1]}"
        )

else:
    st.info("⬅ Upload a product image and click **Generate Creatives**")

