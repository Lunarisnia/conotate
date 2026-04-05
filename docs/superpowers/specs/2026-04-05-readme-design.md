# README Design — Conotate

**Date:** 2026-04-05
**Status:** Approved

## Overview

A full rewrite of `README.md` from a placeholder to a compelling, discovery-focused page for developers finding the project on GitHub.

## Goals

- Audience: developers discovering Conotate on GitHub
- Tone: friendly & approachable
- Structure: problem-first narrative
- Include: usage walkthrough with sample output
- Include: installation via Claude Marketplace and GitHub custom marketplace fallback

## Structure

1. **Header + Hook** — tagline and one-paragraph pitch
2. **The Problem** — why large codebases are hard to navigate with AI, and what Conotate solves
3. **How It Works** — the two skills (`/explore-domain`, `/read-knowledge`) explained simply
4. **Walkthrough** — concrete example: generate → load → update cycle
5. **Installation** — via Claude Marketplace, and via GitHub using custom marketplace commands
6. **Requirements / Contributing / License** — housekeeping

## Key Decisions

- Problem-first narrative chosen over feature-grid or concept-forward to best match the friendly tone and GitHub discovery context
- Custom marketplace install uses `/plugin marketplace add` + `/plugin install conotate@conotate-dev` based on `marketplace.json` name
- Walkthrough uses `src/auth` as a realistic example domain
- No usage reference / API docs — this README is purely for discovery, not as a usage guide
