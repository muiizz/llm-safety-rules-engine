from dataclasses import dataclass, field


@dataclass
class RecordingModel:
    """Records every call. `answer` can be hostile on purpose."""

    answer: str = "Thanks. Noted."
    calls: list[tuple[str, str]] = field(default_factory=list)

    def reply(self, patient_code: str, text: str) -> str:
        self.calls.append((patient_code, text))
        return self.answer
