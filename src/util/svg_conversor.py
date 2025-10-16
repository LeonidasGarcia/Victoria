from PIL import Image, ImageTk
import cairosvg
from io import BytesIO


def load_svg_icon(svg_path, size=(24, 24)):
    try:
        png_data = cairosvg.svg2png(url=svg_path, output_width=size[0], output_height=size[1])
        image_data = Image.open(BytesIO(png_data))
        return ImageTk.PhotoImage(image_data)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo SVG en {svg_path}")
    except Exception as e:
        print(f"Ocurrió un error durante la conversión del SVG: {e}")


def load_jpeg_icon(jpeg_path, size=(24, 24)):
    try:
        image_pil = Image.open(jpeg_path)
        image_pil = image_pil.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image_pil)

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo JPEG en {jpeg_path}")
        return None
    except Exception as e:
        print(f"Ocurrió un error al cargar o procesar el JPEG: {e}")
        return None
