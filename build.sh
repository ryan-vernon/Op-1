#!/usr/bin/env bash
# Wraps tombola.html (written as page content, the way the claude.ai artifact viewer expects)
# into a complete document for Firebase Hosting: public/index.html.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p public
{
  printf '%s\n' '<!doctype html>' '<html lang="en">' '<head>' '<meta charset="utf-8">' \
    '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">' \
    '<meta name="theme-color" content="#5e5b58">' \
    '<meta name="apple-mobile-web-app-capable" content="yes">' \
    '<meta name="apple-mobile-web-app-status-bar-style" content="black">' \
    '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}</style>' \
    '</head>' '<body>'
  cat tombola.html
  printf '%s\n' '</body>' '</html>'
} > public/index.html
rm -rf public/src && cp -R src public/src
