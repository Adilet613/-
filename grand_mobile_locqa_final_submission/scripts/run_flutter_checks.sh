#!/usr/bin/env bash
set -euo pipefail
submission_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
command -v flutter >/dev/null || { echo 'Flutter SDK is required and must be in PATH.' >&2; exit 2; }
cd "$submission_root/flutter_smoke"
flutter --version
flutter pub get
flutter gen-l10n
flutter analyze --no-fatal-infos
flutter test
