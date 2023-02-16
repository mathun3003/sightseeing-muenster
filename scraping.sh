#!/bin/bash
## declare an array variable
declare -a arr=('Antiquariat Münster' 'Cavete Münster' 'Provinzial Münster' 'Rathaus Münster' 'Aaseekugeln Münster')

## now loop through the above array
for i in "${arr[@]}"
do
   echo "Scraping for $i"
   # scrape for every element in above defined array
   bbid.py "$i" -o "data/${i// /_}" -a --limit 500
   cd "data/"
   zip -r "${i// /_}.zip" "${i// /_}"
   rm -rf "${i// /_}"
   # shellcheck disable=SC2103
   cd ..
done
# exit script
exit
