# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A documentation-only course repository ("Multi Cloud + DevOps with AI", CloudDevOpsHub, mentored by Vikas Ratnawat). It contains ~250 Markdown files and no source code, so there is no build, lint, or test tooling.

## Structure

- [README.md](README.md) is the course landing page: syllabus, session list, and links.
- `Session-NN-<Topic>/` directories, numbered 00–59 in course order (Linux → AWS → Git → Jenkins → Docker → Kubernetes/GKE → Prometheus/Grafana → Terraform → Ansible → Python → Azure → AI → capstone projects). Each normally holds:
  - `README.md`: session overview
  - `Interview-QnA.md`
  - `Scenarios.md`: practical/troubleshooting scenarios
  - One or more dated class-notes files named like `🚀 Day-N of <Topic> Batch-NN | <date>.md`. These are transcripts/notes from live sessions for a specific batch (Batch-44, Batch-45).
- Top-level extras: `Mock-Interview/`, `FREE Workshop's/`, and a standalone Kafka session note.
- Some entries deviate from the layout. `Session-41-Ansible-Architect` and `Session-59-Project-9-on MCP server .md` are single Markdown files, not directories.

## Conventions

- File and directory names contain spaces, emoji, apostrophes, `|` and `_`. Quote paths in shell commands.
- Recent git history shows content is added by uploading class notes and then editing them, with commit messages that echo the file name.
- Batch notes carry the date and batch number in the file name. Keep that pattern when adding new notes, and add them inside the matching `Session-NN-*` directory.
