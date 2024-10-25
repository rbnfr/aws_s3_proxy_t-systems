import pytest


def test_health_check(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json()['status'] == "healthy"


def test_settings_values(test_settings):
    assert test_settings.APP_NAME == 'AWS S3 Proxy Service'


@pytest.mark.integration
def test_upload_and_download(test_client):
    test_content = b"Hello, this is a test file!"
    test_filename = "first_test_file.txt"
    bucket_name = "test-bucket"
    object_name = "test_files/first_test_file.txt"

    files = {"file": (test_filename, test_content, "text/plain")}
    upload_response = test_client.post(
        f"/upload/?bucket_name={bucket_name}&object_name={object_name}",
        files=files
    )
    assert upload_response.status_code == 200

    download_response = test_client.get(
        f"/download/?bucket_name={bucket_name}&object_name={object_name}"
    )
    assert download_response.status_code == 200
    assert download_response.content == test_content
