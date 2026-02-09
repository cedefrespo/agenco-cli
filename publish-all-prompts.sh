#!/bin/bash
# Publish all prompts to Agenco marketplace
# Run after logging in with: agenco login

echo " Publishing all prompts to Agenco..."
echo ""

# Get list of prompts from prompts.json
PROMPTS=(
  "fix-bug"
  "new-feature"
  "code-review"
  "refactor"
  "explain"
  "music-con-li-ds"
  "music-bjm"
  "music-oh-sees"
  "music-lp-roxette"
  "music-king-gizzard"
  "trent-nin"
)

SUCCESS=0
FAILED=0

for prompt in "${PROMPTS[@]}"; do
  echo "Publishing: $prompt"
  if ./agenco publish prompt "$prompt"; then
    ((SUCCESS++))
  else
    ((FAILED++))
  fi
  echo ""
done

echo " Published: $SUCCESS"
echo " Failed: $FAILED"
