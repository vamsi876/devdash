"""Color converter - HEX, RGB, HSL, HSV."""

import colorsys
import re

from devdash.tools.base import DevTool

_HEX_RE = re.compile(r"^#?([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$")
_RGB_RE = re.compile(r"^rgb\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)$", re.IGNORECASE)
_HSL_RE = re.compile(r"^hsl\(\s*(\d{1,3})\s*,\s*(\d{1,3})%?\s*,\s*(\d{1,3})%?\s*\)$", re.IGNORECASE)


class ColorTool(DevTool):
    @property
    def name(self) -> str:
        return "Color Converter"

    @property
    def keyword(self) -> str:
        return "color"

    @property
    def category(self) -> str:
        return "Converters"

    @property
    def description(self) -> str:
        return "Convert between HEX, RGB, HSL, and HSV color formats"

    def process(self, input_text: str, **kwargs: object) -> str:
        if not input_text.strip():
            return (
                "Error: Empty input. Provide a color (e.g., #FF0000, rgb(255,0,0), hsl(0,100,50))"
            )

        text = input_text.strip()

        # Try HEX
        hex_match = _HEX_RE.match(text)
        if hex_match:
            hex_val = hex_match.group(1)
            if len(hex_val) == 3:
                hex_val = "".join(c * 2 for c in hex_val)
            r, g, b = int(hex_val[0:2], 16), int(hex_val[2:4], 16), int(hex_val[4:6], 16)
            return self._format_all(r, g, b)

        # Try RGB
        rgb_match = _RGB_RE.match(text)
        if rgb_match:
            r, g, b = int(rgb_match.group(1)), int(rgb_match.group(2)), int(rgb_match.group(3))
            if not all(0 <= v <= 255 for v in (r, g, b)):
                return "Error: RGB values must be between 0 and 255."
            return self._format_all(r, g, b)

        # Try HSL
        hsl_match = _HSL_RE.match(text)
        if hsl_match:
            h = int(hsl_match.group(1))
            s = int(hsl_match.group(2))
            l_val = int(hsl_match.group(3))
            if not (0 <= h <= 360 and 0 <= s <= 100 and 0 <= l_val <= 100):
                return "Error: HSL values out of range (H: 0-360, S: 0-100, L: 0-100)."
            r, g, b = self._hsl_to_rgb(h, s, l_val)
            return self._format_all(r, g, b)

        # Try plain RGB numbers: "255, 0, 0" or "255 0 0"
        parts = re.split(r"[,\s]+", text)
        if len(parts) == 3 and all(p.isdigit() for p in parts):
            r, g, b = int(parts[0]), int(parts[1]), int(parts[2])
            if all(0 <= v <= 255 for v in (r, g, b)):
                return self._format_all(r, g, b)

        return "Error: Unrecognized color format. Use #HEX, rgb(r,g,b), hsl(h,s,l), or r,g,b"

    def _format_all(self, r: int, g: int, b: int) -> str:
        hex_val = f"#{r:02X}{g:02X}{b:02X}"

        # HSL
        h_norm, l_norm, s_norm = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        h_deg = round(h_norm * 360)
        s_pct = round(s_norm * 100)
        l_pct = round(l_norm * 100)

        # HSV
        h_norm2, s_norm2, v_norm2 = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        h_deg2 = round(h_norm2 * 360)
        s_pct2 = round(s_norm2 * 100)
        v_pct2 = round(v_norm2 * 100)

        # Complementary color
        comp_r, comp_g, comp_b = 255 - r, 255 - g, 255 - b
        comp_hex = f"#{comp_r:02X}{comp_g:02X}{comp_b:02X}"

        return (
            f"HEX:           {hex_val}\n"
            f"RGB:           rgb({r}, {g}, {b})\n"
            f"HSL:           hsl({h_deg}, {s_pct}%, {l_pct}%)\n"
            f"HSV:           hsv({h_deg2}, {s_pct2}%, {v_pct2}%)\n"
            f"Complementary: {comp_hex}"
        )

    def _hsl_to_rgb(self, h: int, s: int, lightness: int) -> tuple[int, int, int]:
        r, g, b = colorsys.hls_to_rgb(h / 360, lightness / 100, s / 100)
        return round(r * 255), round(g * 255), round(b * 255)


def register() -> DevTool:
    return ColorTool()
