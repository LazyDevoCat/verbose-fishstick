from audit import check_api


def test_check_api():
    assert check_api("apps/v1beta2") == "Fix apps/v1beta2! Because removed in v1.16, use apps/v1"
    assert check_api("batch/v1") is None
