# file-storage
Django app for file storage

# Quick setup

Pre-requisite: Docker

This django app uses 3 containers: file-storage-database with psql, file-storage-django where the django app lives and file-storage-s3mock where we have a local s3 storage.
You can start them with:

`docker compose up --build`

After they're all up, generate some basic data with:

`docker exec file-storage-django uv run manage.py generate_base_data`

This will create two organizations and two users:
- Superuser (username: root, password: root), with access to Django Admin
- Regular user (username: test, password: test)

# Simple test

1. Open [localhost:8000](http://localhost:8000)
2. Log in to DRF's browseable UI as test user
3. In [files](http://localhost:8000/files) scroll down and POST a file
4. Refresh and check that there's a new entry with download_count and download_link
5. Click the download link, check that it works
6. Go back to the list, refresh and check that the download_count is now 1
7. Go to [organizations](http://localhost:8000/organizations), check that the download_count for Organization 2 Carrots is now 1
8. Go to [downloadsByUser/{test_user_id}](http://localhost:8000/downloadsByUser/2) to check that the downloads are registered
9. Go to [downloadsByFile/{file_id}](http://localhost:8000/downloadsByFile/1) to check that the downloads are registered
10. Go to [admin](http://localhost:8000/admin/login/), log in as root and browse objects if you'd like

# Teardown

When you finish you can take down the containers with

`docker compose down -v`
