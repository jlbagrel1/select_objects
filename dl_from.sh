#!/bin/bash

url="${1}"
query=$(echo "${url}" | grep -oP '(?<=\?q=).+?(?=&)' | sed 's/+/_/g')
echo "${query}"
mkdir "${query}"
cd "${query}"
i=0
curl -s -A 'Mozilla/5.0 (X11; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0' "${url}" |\
    grep -ioP 'https?://[^" ]+?\.(jpg|jpeg|png|tiff|gif)' |\
    while IFS= read -r line; do
        last="${line##*/}"
        ext="${last##*.}"
        name="${query}_$(printf "%05d" "${i}").${ext}"
        curl -A 'Mozilla/5.0 (X11; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0' --max-time 60 --retry 2 -o "${name}" "${line}" || rm -f "${name}"
        identify "${name}" && echo "${name} is an image; keeping" || { echo "${name} is not an image; removing"; rm -f "${name}"; }
        ((i=i+1))
    done
    rdfind -deleteduplicates true .
    rm results.txt
cd ..

