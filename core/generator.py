import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-3-flash-preview")

def generate_pipeline(prompt, language, version, docker_config=None):

    # 🔥 Docker logic MUST be inside function
    docker_instructions = ""

    if docker_config:
        docker_instructions = f"""
Include a Docker build and push stage with:
- Image name: {docker_config.get("image_name")}
- Tag: {docker_config.get("tag")}
- Registry: {docker_config.get("registry")}

Requirements:
- Use docker/build-push-action@v5
- Build Docker image
- Tag image properly
- Push to registry
- Use GitHub secrets for authentication
"""

    # 🔥 Inject into system context
    system_context = f"""
You are a DevOps expert.

Generate a production-ready GitHub Actions YAML for:

Technology: {language}
Version: {version}

{docker_instructions}

Requirements:
- Use best practices
- Use latest stable GitHub Actions
- Include actions/checkout@v4
- Proper job structure
- Secure and optimized pipeline
"""

    response = model.generate_content(
        f"{system_context}\nUser Request:\n{prompt}"
    )

    return response.text

