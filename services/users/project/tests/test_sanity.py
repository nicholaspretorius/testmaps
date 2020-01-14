import json

from project.tests.utils import get_auth0_access_token


def test_sanity_check_all_success(test_app):
    access_token = get_auth0_access_token()
    client = test_app.test_client()

    res = client.get(
        f"/sanity/",
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json",
    )

    data = json.loads(res.data.decode())
    assert res.status_code == 200
    assert res.content_type == "application/json"
    assert "Riders!" in data["hello"]


def test_sanity_check_all_invalid_token(test_app):
    client = test_app.test_client()

    res = client.get(
        f"/sanity/",
        headers={"Authorization": f"Bearer invalid"},
        content_type="application/json",
    )

    data = json.loads(res.data.decode())
    assert res.status_code == 401
    assert res.content_type == "application/json"
    assert "invalid_token" in data["code"]
    assert "Token is invalid." in data["description"]


def test_sanity_check_all_expired_token(test_app):
    access_token = (
        "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIs"
        "ImtpZCI6IlFUTTNOelUyUWpVMU5FWkNRMEk1T1VSRFJrUXdRek0xTk"
        "RnMlFqRkZNak5HTURaRE5UTXhNZyJ9.eyJpc3MiOiJodHRwczovL25"
        "pY2hvbGFzcHJlLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJxanFoR2lLS"
        "GVpOWg3MWxsNzBERzN0V1YyS3dnNUtFVEBjbGllbnRzIiwiYXVkIjo"
        "idGVzdG1hcHMiLCJpYXQiOjE1Nzg1NjQ5NjUsImV4cCI6MTU3ODY1M"
        "TM2NSwiYXpwIjoicWpxaEdpS0hlaTloNzFsbDcwREczdFdWMkt3ZzV"
        "LRVQiLCJzY29wZSI6ImRlbGV0ZTpjYWJsZXBhcmtzIHBvc3Q6Y2Fib"
        "GVwYXJrcyBwdXQ6Y2FibGVwYXJrcyBnZXQ6Y2FibGVwYXJrcyIsImd"
        "0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zIjpbI"
        "mRlbGV0ZTpjYWJsZXBhcmtzIiwicG9zdDpjYWJsZXBhcmtzIiwicHV"
        "0OmNhYmxlcGFya3MiLCJnZXQ6Y2FibGVwYXJrcyJdfQ.glKCfwrAz_"
        "_wiC10Gnlxeedx8MYC_XJgoPqEhjmPYtowmZD8QNJdtWuScUPsUEfT"
        "veDeDUHd3tHY9t4uGPHHnwgy_ip6vZhXYfZ3m--Nsm59fhKBWUPxza"
        "cJqwGCiidWs16DUM-WsfJdy2_N8Cm1H0sI3RLdMl7j8AbhGj1XmI9L"
        "deyE0dIv0c3wafj58qysAh9cjzZ78zWkVD-dub988FQJqIhT2YurpT"
        "zO5awgT1kCYWHiXtZzwOTbCqO80vtmI-YwqmCLOJborEvI3dfwIJ5x"
        "Ax_TanHkql0MmMWFsZf7BKUfsqhhin1m4wpI1qY-ukEcfdmaQIvAdk"
        "m6QfUang"
    )

    client = test_app.test_client()

    res = client.get(
        f"/sanity/",
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json",
    )

    data = json.loads(res.data.decode())
    assert res.status_code == 401
    assert res.content_type == "application/json"
    assert "token_expired" in data["code"]
    assert "Token expired." in data["description"]
