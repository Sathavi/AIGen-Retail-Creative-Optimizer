import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap
import random

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="AIGen Retail Creative Optimizer",
    layout="wide"
)

st.title("🛍️ AIGen Retail Creative Optimizer")
st.write("AI-powered tool to automatically generate retail ad creatives")

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

uploaded_image = st.sidebar.file_uploader(
    "Upload Product Image",
    type=["jpg", "png"]
)

generate_btn = st.sidebar.button("🚀 Generate Creatives")

# -------------------------------
# COPY GENERATION (AI LOGIC)
# -------------------------------
def generate_ad_copy(product_name, product_desc, platform):
    headlines = [
        f"Experience the Power of {product_name}",
        f"Upgrade Your Life with {product_name}",
        f"{product_name} That Redefines Performance",
        f"Smarter Choice for Everyday Use"
    ]

    captions = [
        f"{product_desc} Designed to deliver premium quality and unmatched comfort.",
        f"Discover why {product_name} is the perfect choice for modern users.",
        f"Engineered for performance, style, and reliability."
    ]

    ctas = {
        "Instagram": "Shop Now",
        "Amazon Ads": "Buy Now",
        "Google Ads": "Learn More"
    }

    return (
        random.choice(headlines),
        random.choice(captions),
        ctas[platform]
    )

# -------------------------------
# IMAGE GENERATION
# -------------------------------
def create_ad_image(base_image, headline, cta, size):
    img = base_image.resize(size)
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("arial.ttf", 36)
        cta_font = ImageFont.truetype("arial.ttf", 26)
    except:
        title_font = ImageFont.load_default()
        cta_font = ImageFont.load_default()

    wrapped_text = textwrap.fill(headline, width=20)

    # Overlay
    draw.rectangle(
        [(0, img.height - 180), (img.width, img.height)],
        fill=(0, 0, 0)
    )

    draw.text(
        (20, img.height - 160),
        wrapped_text,
        fill="white",
        font=title_font
    )

    # CTA Button
    draw.rectangle(
        [(20, img.height - 60), (200, img.height - 20)],
        fill=(255, 165, 0)
    )

    draw.text(
        (45, img.height - 55),
        cta,
        fill="black",
        font=cta_font
    )

    return img

# -------------------------------
# MAIN FLOW
# -------------------------------
if generate_btn and uploaded_image:
    base_image = Image.open(uploaded_image).convert("RGB")

    headline, caption, cta = generate_ad_copy(
        product_name,
        product_desc,
        platform
    )

    st.subheader("📢 Generated Ad Copy")
    st.markdown(f"**Headline:** {headline}")
    st.markdown(f"**Caption:** {caption}")
    st.markdown(f"**CTA:** {cta}")

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


