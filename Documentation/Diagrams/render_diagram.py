import zlib
import urllib.request
import os

plantuml_alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"

def encode64(data):
    res = []
    for i in range(0, len(data), 3):
        b1 = data[i]
        b2 = data[i+1] if i+1 < len(data) else 0
        b3 = data[i+2] if i+2 < len(data) else 0
        c1 = b1 >> 2
        c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
        c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
        c4 = b3 & 0x3F
        res.append(plantuml_alphabet[c1])
        res.append(plantuml_alphabet[c2])
        if i + 1 < len(data):
            res.append(plantuml_alphabet[c3])
        if i + 2 < len(data):
            res.append(plantuml_alphabet[c4])
    return "".join(res)

def plantuml_encode(text):
    z = zlib.compressobj(9, zlib.DEFLATED, -15)
    compressed = z.compress(text.encode("utf-8")) + z.flush()
    return "~1" + encode64(compressed)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    puml_path = os.path.join(script_dir, "use_case_omnishop.puml")
    with open(puml_path, "r", encoding="utf-8") as f:
        content = f.read()

    encoded = plantuml_encode(content)
    
    # Download SVG
    svg_url = f"https://www.plantuml.com/plantuml/svg/{encoded}"
    req_svg = urllib.request.Request(svg_url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req_svg) as resp:
        svg_bytes = resp.read()
    with open(os.path.join(script_dir, "use_case_omnishop.svg"), "wb") as f:
        f.write(svg_bytes)
    print("Rendered SVG successfully!")

    # Download PNG
    png_url = f"https://www.plantuml.com/plantuml/png/{encoded}"
    req_png = urllib.request.Request(png_url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req_png) as resp:
        png_bytes = resp.read()
    with open(os.path.join(script_dir, "use_case_omnishop.png"), "wb") as f:
        f.write(png_bytes)
    print("Rendered PNG successfully!")

if __name__ == "__main__":
    main()
