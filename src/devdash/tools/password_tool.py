"""Secure password generator using secrets module."""

import math
import secrets
import string

from devdash.tools.base import DevTool

# Word list for passphrases (common English words)
_WORDLIST = [
    "abandon", "ability", "able", "about", "above", "absent", "absorb", "abstract",
    "absurd", "abuse", "access", "accident", "account", "accuse", "achieve", "acid",
    "acquire", "across", "action", "actor", "actress", "actual", "adapt", "address",
    "adjust", "admit", "adult", "advance", "advice", "aerobic", "afford", "afraid",
    "again", "agent", "agree", "ahead", "alarm", "album", "alert", "alien", "allow",
    "almost", "alone", "alpha", "already", "also", "alter", "always", "amateur",
    "amazing", "among", "amount", "amused", "anchor", "ancient", "anger", "angle",
    "animal", "annual", "answer", "apart", "apple", "approve", "arctic", "arena",
    "armor", "army", "arrow", "artist", "assign", "assist", "atom", "attack",
    "attend", "august", "aunt", "author", "auto", "autumn", "average", "avocado",
    "avoid", "awake", "aware", "awesome", "badge", "balance", "bamboo", "banana",
    "banner", "barrel", "basket", "battle", "beach", "beauty", "become", "before",
    "begin", "behind", "believe", "bench", "benefit", "bicycle", "blade", "blanket",
    "blast", "bless", "blind", "blood", "blossom", "board", "bonus", "border",
    "bottle", "bounce", "brave", "breeze", "bridge", "bright", "broken", "brother",
    "budget", "bundle", "burger", "butter", "cabin", "cable", "camera", "campus",
    "canal", "cancel", "candy", "cannon", "canvas", "canyon", "captain", "carbon",
    "carpet", "castle", "catalog", "catch", "cattle", "caught", "cause", "ceiling",
    "celery", "cement", "census", "century", "cereal", "certain", "chair", "chalk",
    "champion", "change", "chapter", "charge", "chase", "cherry", "chicken", "choice",
    "circle", "citizen", "civil", "claim", "clap", "clarify", "clean", "clever",
    "climate", "clinic", "clock", "close", "cloud", "cluster", "coach", "coconut",
    "coffee", "collect", "color", "column", "combine", "comfort", "comic", "common",
    "company", "concert", "conduct", "confirm", "congress", "connect", "consider",
    "control", "convince", "cookie", "copper", "coral", "correct", "cotton", "country",
    "couple", "course", "cousin", "cover", "cradle", "craft", "cream", "credit",
    "creek", "crew", "crisis", "cross", "crowd", "crucial", "cruel", "cruise",
    "crystal", "cube", "culture", "current", "curtain", "custom", "cycle", "damage",
    "dance", "danger", "daughter", "dawn", "debate", "decade", "december", "decide",
    "decline", "decorate", "decrease", "defense", "define", "degree", "delay", "deliver",
    "demand", "denial", "dentist", "deny", "depart", "depend", "deposit", "describe",
    "desert", "design", "detail", "detect", "develop", "device", "devote", "diagram",
    "diamond", "diary", "diesel", "differ", "digital", "dignity", "dilemma", "dinner",
    "dinosaur", "direct", "discover", "dismiss", "display", "distance", "divide",
    "doctor", "document", "dolphin", "domain", "donate", "donkey", "double", "dragon",
]


class PasswordTool(DevTool):
    @property
    def name(self) -> str:
        return "Password Generator"

    @property
    def keyword(self) -> str:
        return "password"

    @property
    def category(self) -> str:
        return "Generators"

    @property
    def description(self) -> str:
        return "Generate secure passwords or passphrases"

    def process(self, input_text: str, **kwargs: object) -> str:
        text = input_text.strip().lower()
        mode = str(kwargs.get("mode", ""))

        if text == "passphrase" or mode == "passphrase":
            word_count = int(kwargs.get("words", 4))
            return self._passphrase(max(2, min(word_count, 12)))

        length = 16
        if text.isdigit():
            length = int(text)
        elif kwargs.get("length"):
            length = int(kwargs["length"])  # type: ignore[arg-type]

        length = max(8, min(length, 128))

        include_upper = bool(kwargs.get("uppercase", True))
        include_lower = bool(kwargs.get("lowercase", True))
        include_digits = bool(kwargs.get("digits", True))
        include_symbols = bool(kwargs.get("symbols", True))
        count = int(kwargs.get("count", 1))
        count = max(1, min(count, 20))

        charset = ""
        if include_lower:
            charset += string.ascii_lowercase
        if include_upper:
            charset += string.ascii_uppercase
        if include_digits:
            charset += string.digits
        if include_symbols:
            charset += string.punctuation
        if not charset:
            charset = string.ascii_letters + string.digits

        results: list[str] = []
        for _ in range(count):
            password = "".join(secrets.choice(charset) for _ in range(length))
            entropy = self._entropy(length, len(charset))
            results.append(f"{password}  (entropy: {entropy:.0f} bits)")

        return "\n".join(results)

    def _passphrase(self, word_count: int) -> str:
        words = [secrets.choice(_WORDLIST) for _ in range(word_count)]
        passphrase = "-".join(words)
        entropy = math.log2(len(_WORDLIST)) * word_count
        return f"{passphrase}\n\nWords: {word_count}, Entropy: {entropy:.0f} bits"

    def _entropy(self, length: int, charset_size: int) -> float:
        if charset_size <= 0:
            return 0.0
        return length * math.log2(charset_size)


def register() -> DevTool:
    return PasswordTool()
