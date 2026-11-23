from safetyrules.model_stub import StubModel


def test_stub_reply() -> None:
    assert StubModel().reply("P-9", "hi") == "Thanks, P-9. I noted your message."
