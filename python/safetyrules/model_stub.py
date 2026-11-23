"""A fake model. It is deterministic, free and makes no network calls."""


class StubModel:
    def reply(self, patient_code: str, text: str) -> str:
        return f"Thanks, {patient_code}. I noted your message."
