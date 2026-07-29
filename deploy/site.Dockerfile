# Static-site image for chains-student.durczok.ovh
# This is separate from the root Dockerfile (which students use to run their
# Flask scaffold locally via `docker compose up`). This image serves only
# the case-study landing page — no Python, no server.py, no /api routes.
FROM nginx:1.27-alpine

COPY index.html /usr/share/nginx/html/index.html

EXPOSE 80
