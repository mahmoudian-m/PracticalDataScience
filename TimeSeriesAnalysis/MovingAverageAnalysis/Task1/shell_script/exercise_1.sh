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

source_file="../../rejected_2007_to_2018Q4.csv"
output_result="../../moving_avg_result/mv_result.csv"
sma50="SMA50"
declare -A filtered_values=()
risk_score_values=()
window_size=50
#######################################
# Calculate moving average for specified offset and window size from list.
# Arguments:
#   offset, window_size
# Outputs:
#   calculated moving average
#######################################
moving_avg() {
  if [[ ! "$1" -ge $(($2 - 1)) || "$1" -gt $((${#risk_score_values[@]} - 1)) ]]; then
    echo -e "${RED}Unable to calculate MA${NC}"
    return 0
  fi
  local offset=$1
  local window_size=$2
  local sum
  local window_average
  local window=("${risk_score_values[@]:${offset}-(${window_size} - 1):${window_size}}")
  sum=$(
    IFS=+
    echo "${window[*]}" | bc
  )
  window_average=$(echo "scale=2;  ${sum} / ${#window[@]}" | bc)
  echo "${window_average}"
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
# Calculate moving average
# Outputs:
#  array of calculated moving average based on filter
#######################################
calculate_moving_avg() {
  echo -e "${GREEN}Start calculating moving average${NC}"
  local sequence=()
  while IFS='' read -r line; do sequence+=("$line"); done < <(seq 0 $((${#filtered_values[*]} - 1)))
  for i in "${!sequence[@]}"; do
    if [[ i -ge $((window_size - 1)) ]]; then
      filtered_values["$i"]="${filtered_values["$i"]},$(moving_avg "$i" "${window_size}")"
      moving_avg "$i" "${window_size}"
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
calculate_moving_avg
store_data