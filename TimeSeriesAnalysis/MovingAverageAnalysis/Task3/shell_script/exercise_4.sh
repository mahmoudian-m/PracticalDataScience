#!/usr/bin/env bash
#######################################################################
# Title      :    Calculate moving average
# Author     :    Mostafa Mahmoudian <mahmoudian.m1991@gmail.com>
# Date       :    2022-11-25
# Requires   :
# Category   :
#######################################################################
# Description
#   Calculate moving average for CSV file based on Risk_Score column for 2007 year
#######################################################################
clear
# constants
NC='\033[0m'
GREEN="\e[32m"

source_file="../../calculatedma50.csv"
output_result="../../moving_avg_result/mv_result.csv"
sma50="SMA50"
declare -A filtered_values=()
risk_score_values=()
window_size=50
declare moving_averages

#######################################
# Calculate exponential moving average from list.
# Outputs:
#   Calculate exponential moving average
#######################################
calculate_ema50() {
  echo -e "${GREEN}Start calculating exponential moving average${NC}"
  x=0.5
  i=0
  moving_averages+=("${risk_score_values[0]}")
  while [ ${i} -lt "${#risk_score_values[@]}" ]; do
    window_average=$(echo "scale=2; (${x} * ${risk_score_values[$i]}) + ( 1 - ${x} ) * ${moving_averages[-1]}" | bc)
    moving_averages+=("${window_average}" )
    ((i = i + 1))
  done
}
#######################################
# extract rows from CSV file and filter based on year.
# Outputs:
#   array of row based on filter, array of moving average
#######################################
extract_data() {
  echo -e "${GREEN}Start extracting data from CSV${NC}"
  head_file=$(head -n 1 ${source_file})
  local count=0
  while IFS=$'\n' read -r row; do
    risk_score=$(echo "${row}" | awk -F'"' -v OFS='' '{ for (i=2; i<=NF; i+=2) gsub(",", "", $i) } 1' | cut -d, -f4)
    if [ ! -z "${risk_score}" ]; then
      filtered_values["${count}"]+="${row}"
      risk_score_values+=("${risk_score}")
      ((count = count + 1))
    fi
  done < <(cat "${source_file}" | awk -F, '$2 ~ /^2007/{print}')
}

#######################################
# Transform exponential moving average
# Outputs:
#  array of calculated moving average based on filter
#######################################
transform_emoving_avg() {
  echo -e "${GREEN}Start transforming exponential moving average${NC}"
  local sequence=()
  while IFS='' read -r line; do sequence+=("$line"); done < <(seq 0 $((${#filtered_values[*]} - 1)))
  for i in "${!sequence[@]}"; do
    if [[ i -ge $((window_size -1)) ]]; then
      filtered_values["$i"]="$( echo "${filtered_values["$i"]} "| awk -F, '{ print $1 "," $2 ","$3 ","$4 ","$5 ","$6 ","$7 ","$8 ","$9 ","}')${moving_averages[$i+1]}"
    fi
  done
}
#######################################
# Save final result into CSV file
#######################################

store_data() {
  echo -e "${GREEN}Start saving result into: ${output_result}${NC}"
  echo "${head_file},${sma50}" >"${output_result}"
  local sequence=()
  while IFS='' read -r line; do sequence+=("$line"); done < <(seq 0 $((${#filtered_values[*]} - 1)))
  for i in "${!sequence[@]}"; do
    echo "${filtered_values[$i]}"
  done >>"${output_result}"
}
extract_data
calculate_ema50
transform_emoving_avg
store_data
