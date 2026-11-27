
## 2026-11-27: GHCR make-public and read-only pull (Session 22)
- Test package ghcr.io/shivamnamdev/atithi-ghcr-vis:1 (nginx:alpine). Private: anonymous token 401, manifest 403. After the user made it public in the web UI (no API exists): anonymous manifest 200. Classic token with only read:packages (user-made): pull OK, push refused (permission_denied: token does not match expected scopes), tags unchanged; private atithi-ghcr-test readable with it, 403 anonymously. Docker Desktop pulled a private image with a clean DOCKER_CONFIG (stored credentials), so privacy was proven with curl instead.
- Incident: the user saved the token inside the course repo folder (tmp-token, untracked, never committed); moved to /private/tmp/claude-501/ghcr-ro/token mode 600, now deleted.
- Cleanup for the user: delete packages atithi-ghcr-vis and atithi-ghcr-test (my gh token has no delete:packages), revoke the read:packages token.
