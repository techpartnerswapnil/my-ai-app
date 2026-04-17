import streamlit as st
from core.generator import generate_pipeline

st.set_page_config(page_title="ActionGen AI", layout="wide")

st.title("🚀 ActionGen AI")
st.write("Generate GitHub Actions pipelines using AI")

# 🔽 Language selection
language = st.selectbox(
    "Select Technology",
    ["Python", "Node.js", "Java", "Django", "Nginx", "Next.js"]
)

# 🔽 Version mapping
versions_map = {
    "Python": ["3.8", "3.9", "3.10", "3.11", "3.12"],
    "Node.js": ["16", "18", "20", "21"],
    "Java": ["8", "11", "17", "21"],
    "Django": ["3.x", "4.x", "5.x"],
    "Nginx": ["1.20", "1.22", "latest"],
    "Next.js": ["12", "13", "14"]
}

version = st.selectbox("Select Version", versions_map.get(language, []))

st.markdown("### 🐳 Docker Configuration")

use_docker = st.checkbox("Include Docker Build Stage")

docker_config = {}

if use_docker:
    docker_config["image_name"] = st.text_input("Docker Image Name", "my-app")
    docker_config["tag"] = st.text_input("Tag", "latest")

    docker_config["registry"] = st.selectbox(
        "Container Registry",
        ["Docker Hub", "AWS ECR", "GitHub Container Registry"]
    )

# 🔽 User input
user_input = st.text_area("Describe your pipeline:", height=150)

if st.button("Generate Pipeline"):
    if user_input.strip():
        with st.spinner("Generating..."):
            output = generate_pipeline(user_input, language, version, docker_config)

        st.subheader("Generated YAML")
        st.code(output, language="yaml")

        # 🔥 Download button
        st.download_button(
            "Download YAML",
            output,
            file_name="workflow.yml"
        )
    else:
        st.warning("Please enter a prompt.")
