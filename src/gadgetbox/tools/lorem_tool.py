"""Lorem ipsum generator."""

from gadgetbox.tools.base import DevTool

_LOREM_TEXT = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor "
    "incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud "
    "exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure "
    "dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. "
    "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt "
    "mollit anim id est laborum."
)

_SENTENCES = [
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.",
    "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore.",
    "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia.",
    "Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit.",
    "Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet.",
    "Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis.",
    "Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse.",
    "At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis.",
    "Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit.",
    "Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus.",
]

_WORDS = _LOREM_TEXT.replace(",", "").replace(".", "").lower().split()


class LoremTool(DevTool):
    @property
    def name(self) -> str:
        return "Lorem Ipsum Generator"

    @property
    def keyword(self) -> str:
        return "lorem"

    @property
    def category(self) -> str:
        return "Generators"

    @property
    def description(self) -> str:
        return "Enter amount, e.g. '5 words', '3 sentences', or '2 paragraphs'"

    def process(self, input_text: str, **kwargs: object) -> str:
        text = input_text.strip().lower()
        mode = str(kwargs.get("mode", ""))

        if not text and not mode:
            return self._paragraphs(3)

        # Parse "5 words", "3 sentences", "2 paragraphs" or just a number
        parts = text.split()
        count = 1
        unit = mode or "paragraphs"

        if parts:
            try:
                count = int(parts[0])
            except ValueError:
                pass
            if len(parts) > 1:
                unit = parts[1].rstrip("s") + "s" if not parts[1].endswith("s") else parts[1]

        count = max(1, min(count, 100))

        if unit.startswith("word"):
            return self._words(count)
        elif unit.startswith("sentence"):
            return self._sentences(count)
        else:
            return self._paragraphs(count)

    def _words(self, count: int) -> str:
        result: list[str] = []
        while len(result) < count:
            result.extend(_WORDS)
        return " ".join(result[:count]).capitalize() + "."

    def _sentences(self, count: int) -> str:
        result: list[str] = []
        idx = 0
        while len(result) < count:
            result.append(_SENTENCES[idx % len(_SENTENCES)])
            idx += 1
        return " ".join(result[:count])

    def _paragraphs(self, count: int) -> str:
        paragraphs: list[str] = []
        for i in range(count):
            start = (i * 3) % len(_SENTENCES)
            sents = [_SENTENCES[(start + j) % len(_SENTENCES)] for j in range(4)]
            paragraphs.append(" ".join(sents))
        return "\n\n".join(paragraphs)


def register() -> DevTool:
    return LoremTool()
