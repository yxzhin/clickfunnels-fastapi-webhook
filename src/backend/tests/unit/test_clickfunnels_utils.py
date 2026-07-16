from datetime import UTC, datetime

from src.backend.app.utils import ClickFunnelsUtils


async def test_verify_clickfunnels_signature() -> None:
    raw_body = b'{"test22":"ril73"}'
    timestamp = str(int(datetime.now(UTC).timestamp()))
    secret = "test22ril73"
    import hmac
    from hashlib import sha256

    expected = hmac.new(
        secret.encode(), timestamp.encode() + b"." + raw_body, sha256
    ).hexdigest()

    assert (
        ClickFunnelsUtils.verify_clickfunnels_signature(
            raw_body=raw_body,
            signature_header=expected,
            timestamp_header=timestamp,
            secret=secret,
        )
        is True
    )
