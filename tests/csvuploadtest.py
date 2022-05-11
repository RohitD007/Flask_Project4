"""Test the csv upload"""


def test_csv(client):
    """test csv upload"""
    res = client.get("../app/upload")
    print(res.data)
    assert res.status_code == 302
    upload_res = client.post("../app/upload", data="../app/upload/transactions.csv",
    follow_redirects=True)
    assert upload_res.status_code == 200
