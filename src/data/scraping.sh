#!/bin/bash
## declare an array variable
declare -a arr=('Aasee Münster' 'Hafen Münster')

## now loop through the above array
for i in "${arr[@]}"
do
   echo "Scraping for $i"
   # scrape for every element in above defined array
   bbid.py "$i" -o "imgs/${i// /_}" -a --limit 500
   cd "imgs/"
   zip -r "${i// /_}.zip" "${i// /_}"
   rm -rf "${i// /_}"
   # shellcheck disable=SC2103
   cd ..
done
# exit script
exit
