import os
import plantuml

def render_all_diagrams():
    diagrams_dir = os.path.dirname(os.path.abspath(__file__))
    server_png = plantuml.PlantUML("https://www.plantuml.com/plantuml/img/")
    server_svg = plantuml.PlantUML("https://www.plantuml.com/plantuml/svg/")

    puml_files = [f for f in os.listdir(diagrams_dir) if f.endswith(".puml")]

    for puml_file in puml_files:
        puml_path = os.path.join(diagrams_dir, puml_file)
        base_name = os.path.splitext(puml_file)[0]
        png_path = os.path.join(diagrams_dir, f"{base_name}.png")
        svg_path = os.path.join(diagrams_dir, f"{base_name}.svg")

        with open(puml_path, "r", encoding="utf-8") as f:
            code = f.read()

        try:
            png_bytes = server_png.processes(code)
            with open(png_path, "wb") as f:
                f.write(png_bytes)
            print(f"Rendered PNG: {base_name}.png")

            svg_bytes = server_svg.processes(code)
            with open(svg_path, "wb") as f:
                f.write(svg_bytes)
            print(f"Rendered SVG: {base_name}.svg")
        except Exception as e:
            print(f"Error rendering {puml_file}: {e}")

if __name__ == "__main__":
    render_all_diagrams()
