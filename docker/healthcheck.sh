#!/usr/bin/env bash
curl -fsS http://localhost:8000/health || exit 1
