def test_jobs_require_login(client):
    assert client.get("/jobs/").status_code == 401


def test_create_job(client, make_headers):
    response = client.post("/jobs/", json={"name": "check-title"}, headers=make_headers())
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "check-title"
    assert body["status"] == "queued"


def test_list_only_my_jobs(client, make_headers):
    asha = make_headers("asha@example.com")
    ravi = make_headers("ravi@example.com")
    client.post("/jobs/", json={"name": "job-1"}, headers=asha)
    client.post("/jobs/", json={"name": "job-2"}, headers=asha)
    client.post("/jobs/", json={"name": "job-3"}, headers=ravi)
    response = client.get("/jobs/", headers=asha)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_job_of_other_user_returns_404(client, make_headers):
    asha = make_headers("asha@example.com")
    ravi = make_headers("ravi@example.com")
    job_id = client.post("/jobs/", json={"name": "private"}, headers=asha).json()["id"]
    assert client.get(f"/jobs/{job_id}", headers=ravi).status_code == 404


def test_update_job_status(client, make_headers):
    headers = make_headers()
    job_id = client.post("/jobs/", json={"name": "run-me"}, headers=headers).json()["id"]
    response = client.patch(f"/jobs/{job_id}", json={"status": "running"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_delete_job(client, make_headers):
    headers = make_headers()
    job_id = client.post("/jobs/", json={"name": "delete-me"}, headers=headers).json()["id"]
    assert client.delete(f"/jobs/{job_id}", headers=headers).status_code == 204
    assert client.get(f"/jobs/{job_id}", headers=headers).status_code == 404


def test_invalid_status_returns_422(client, make_headers):
    headers = make_headers()
    job_id = client.post("/jobs/", json={"name": "bad-status"}, headers=headers).json()["id"]
    response = client.patch(f"/jobs/{job_id}", json={"status": "banana"}, headers=headers)
    assert response.status_code == 422