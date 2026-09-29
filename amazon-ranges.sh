#!/usr/bin/env bash

set -euo pipefail

if [[ $# -ne 1 ]]; then
	printf 'Usage: %s OUTPUT_DIR\n' "$0" >&2
	exit 2
fi

if ! command -v jq >/dev/null 2>&1; then
	printf 'Error: jq is required.\n' >&2
	exit 1
fi

if ! command -v wget >/dev/null 2>&1; then
	printf 'Error: wget is required.\n' >&2
	exit 1
fi

output_dir=$1
mkdir -p "$output_dir"
ranges_file=$(mktemp)
trap 'rm -f "$ranges_file"' EXIT

wget -qO "$ranges_file" https://ip-ranges.amazonaws.com/ip-ranges.json
jq -e '.prefixes | type == "array"' "$ranges_file" >/dev/null

while IFS=$'\t' read -r service region; do
	[[ -n "$service" && -n "$region" ]] || continue

	service_dir="$output_dir/$service"
	mkdir -p "$service_dir"
	jq --arg service "$service" --arg region "$region" \
		'[.prefixes[] | select(.service == $service and .region == $region)] | sort_by(.ip_prefix)' \
		"$ranges_file" > "$service_dir/$region.json"
done < <(
	jq -r '.prefixes | sort_by(.service, .region) | unique_by([.service, .region])[] | [.service, .region] | @tsv' \
		"$ranges_file"
)
