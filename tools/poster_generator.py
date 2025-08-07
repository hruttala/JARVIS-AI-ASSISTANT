# poster_generator.py

import asyncio
import base64
import qrcode
from pathlib import Path
from PIL import Image
from io import BytesIO
import imageio
from playwright.async_api import async_playwright
from ollama_interface import generate_image

def main(task, memory):
    print(f"[{__name__}] received task: {task}")
    return f"Output for: {task}"


def encode_img(path):
    return base64.b64encode(Path(path).read_bytes()).decode("utf-8")


def generate_poster_html(prompt: str, style="minimal", layout="stacked", qr_path=None, logo_path=None, background_path=None) -> str:
    title, _, desc = prompt.partition(":")
    title, desc = title.strip(), desc.strip()

    styles = {
        "minimal": """
            body { font-family: sans-serif; background: white; color: #222; display: flex; justify-content: center; align-items: center; height: 100vh; padding: 2rem; }
            h1 { font-size: 3rem; margin-bottom: 1rem; }
            p { font-size: 1.5rem; max-width: 800px; text-align: center; }
        """,
        "neon": """
            body { font-family: 'Arial Black', sans-serif; background: black; color: #0ff; display: flex; justify-content: center; align-items: center; height: 100vh; padding: 2rem; }
            h1 { font-size: 4rem; text-shadow: 0 0 10px #0ff; }
            p { font-size: 2rem; max-width: 700px; text-align: center; color: #0ff; }
        """,
        "corporate": """
            body { font-family: Arial, sans-serif; background: #f2f2f2; color: #333; display: flex; justify-content: center; align-items: center; height: 100vh; padding: 2rem; }
            h1 { font-size: 2.5rem; color: #004080; }
            p { font-size: 1.2rem; max-width: 800px; text-align: center; }
        """,
        "event": """
            body { font-family: Verdana; background: linear-gradient(#ffecd2, #fcb69f); color: #222; display: flex; justify-content: center; align-items: center; height: 100vh; padding: 2rem; }
            h1 { font-size: 3rem; color: #c44536; }
            p { font-size: 1.5rem; max-width: 700px; text-align: center; }
        """,
        "party": """
            body { font-family: Comic Sans MS, cursive; background: linear-gradient(#f0f, #0ff); color: white; text-shadow: 2px 2px 4px #000; display: flex; justify-content: center; align-items: center; height: 100vh; padding: 2rem; }
            h1 { font-size: 4rem; margin-bottom: 1rem; }
            p { font-size: 2rem; max-width: 700px; text-align: center; }
        """,
        "startup": """
            body { font-family: 'Segoe UI'; background: white; color: #1e1e1e; display: flex; justify-content: center; align-items: center; height: 100vh; padding: 3rem; }
            h1 { font-size: 3rem; font-weight: 700; color: #007acc; }
            p { font-size: 1.3rem; max-width: 750px; text-align: center; }
        """
    }

    layout_css = {
        "stacked": "flex-direction: column;",
        "image-left": "flex-direction: row;",
        "image-right": "flex-direction: row-reverse;",
        "grid": "display: grid; grid-template-columns: 1fr 1fr;"
    }

    css = styles.get(style, styles["minimal"])
    layout_style = layout_css.get(layout, layout_css["stacked"])

    bg_style = ""
    if background_path:
        b64_bg = encode_img(background_path)
        bg_style = f"body {{ background-image: url('data:image/png;base64,{b64_bg}'); background-size: cover; background-position: center; }}"

    html = f"""
    <html>
    <head>
        <style>
            {css}
            body {{
                {layout_style}
            }}
            {bg_style}
        </style>
    </head>
    <body>
        {"<img src='data:image/png;base64," + encode_img(logo_path) + "' width='100' style='margin:1rem;'/>" if logo_path else ""}
        <div>
            <h1>{title}</h1>
            <p>{desc}</p>
        </div>
        {"<img src='data:image/png;base64," + encode_img(qr_path) + "' width='100' style='margin-top: 2rem;'/>" if qr_path else ""}
    </body>
    </html>
    """
    return html


async def render_html_to_image(html: str, output_path: str, size=(1080, 1080), dpi=1):
    width, height = size
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": width, "height": height, "deviceScaleFactor": dpi}
        )
        await page.set_content(html, wait_until="load")
        await page.screenshot(path=output_path)
        await browser.close()


def create_animated_gif(html: str, output_path="poster.gif", frames=10, size=(1080, 1080), dpi=1):
    temp_images = []
    for i in range(frames):
        temp_path = f"temp_frame_{i}.png"
        asyncio.run(render_html_to_image(html, temp_path, size=size, dpi=dpi))
        temp_images.append(imageio.imread(temp_path))
        Path(temp_path).unlink()

    imageio.mimsave(output_path, temp_images, duration=0.2)
    print(f"[🎞] Animated poster saved to: {Path(output_path).absolute()}")


def create_poster(prompt: str,
                  style: str = "minimal",
                  layout: str = "stacked",
                  output_path: str = "poster.png",
                  background=False,
                  animated=False,
                  animation_type="fade-in",
                  size=(1080, 1080),
                  dpi=1):
    qr_link, logo_path = None, None
    if "{qr:" in prompt:
        qr_link = prompt.split("{qr:")[1].split("}")[0]
        prompt = prompt.replace(f"{{qr:{qr_link}}}", "").strip()
    if "{logo:" in prompt:
        logo_path = prompt.split("{logo:")[1].split("}")[0]
        prompt = prompt.replace(f"{{logo:{logo_path}}}", "").strip()

    qr_path = None
    if qr_link:
        qr_img = qrcode.make(qr_link)
        qr_path = "temp_qr.png"
        qr_img.save(qr_path)

    bg_path = None
    if background:
        bg_prompt = f"poster background for: {prompt}"
        bg_path = generate_image(bg_prompt)

    html = generate_poster_html(prompt, style, layout, qr_path, logo_path, bg_path)

    if animated:
        create_animated_gif(html, output_path.replace(".png", ".gif"), size=size, dpi=dpi)
    else:
        asyncio.run(render_html_to_image(html, output_path, size=size, dpi=dpi))
        print(f"[✅] Poster saved to: {Path(output_path).absolute()}")

    if qr_path and Path(qr_path).exists():
        Path(qr_path).unlink()


def generate_poster_from_intent(params: dict):
    create_poster(
        prompt=params.get("prompt", ""),
        style=params.get("style", "minimal"),
        layout=params.get("layout", "stacked"),
        output_path=params.get("output", "poster.png"),
        background=params.get("background", False),
        animated=params.get("animated", False),
        animation_type=params.get("animation_type", "fade-in"),
        size=params.get("size", (1080, 1080)),
        dpi=params.get("dpi", 1),
    )