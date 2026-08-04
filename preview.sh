#!/usr/bin/env bash
# Serve this site locally exactly the way GitHub Pages builds it, without
# installing anything on this machine — everything runs inside the official
# jekyll/jekyll Docker image, using this repo's own Gemfile (the same
# github-pages gem GitHub itself builds with).
#
# Usage:
#   ./preview.sh          # start the server at http://localhost:4000
#   ./preview.sh stop     # stop it
#
# First run installs ~100 gems inside the container and takes a few minutes;
# after that the gems are cached in ./vendor/bundle (gitignored) and startup
# is a few seconds.

set -euo pipefail
cd "$(dirname "$0")"

CONTAINER_NAME="learn-claude-preview"

if [ "${1:-}" = "stop" ]; then
  docker stop "$CONTAINER_NAME" >/dev/null 2>&1 && echo "Stopped." || echo "Not running."
  exit 0
fi

if ! docker info >/dev/null 2>&1; then
  echo "Docker isn't running. Start Docker Desktop, then try again." >&2
  exit 1
fi

if docker ps --format '{{.Names}}' | grep -qx "$CONTAINER_NAME"; then
  echo "Already running at http://localhost:4000"
  exit 0
fi

mkdir -p vendor/bundle

docker run --rm -d --name "$CONTAINER_NAME" \
  --volume="$PWD:/srv/jekyll" \
  --volume="$PWD/vendor/bundle:/usr/local/bundle" \
  -e JEKYLL_ENV=development \
  -p 4000:4000 \
  jekyll/jekyll:latest \
  bash -c "bundle install && bundle exec jekyll serve --host 0.0.0.0 --livereload" >/dev/null

echo "Starting... first run installs gems and takes a few minutes."
echo "Watch progress with:  docker logs -f $CONTAINER_NAME"
echo "Once ready:           http://localhost:4000"
echo "Stop it with:         ./preview.sh stop"
