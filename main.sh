#!/bin/bash
url="http://www.wsj.com/mdc/public/page/2_3021-activnyse-actives.html"
backend_script="hw9.py"
seconds_of_wait_time=5
total_iterations=3

for (( i=0; i < total_iterations; i++ )); do
    fn=$(date "+%Y_%m_%d_%H_%M_%S")
    wget --tries=3 $url -O $fn.html
    python $backend_script $fn.html
    rm -r $fn.*
    echo "####################"
    echo "## loop $(( $i + 1 ))"
    echo "## sleeping for... $seconds_of_wait_time seconds"
    echo "####################"
    sleep $seconds_of_wait_time
done
