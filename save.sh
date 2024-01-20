#!/bin/bash

version=$1
tag=$2

usage() {
  echo "Usage: $0 <ver> <tag>"
}

if [ -z $version ] || [ -z $tag ] 
then
  usage
  exit 1
fi

src_folder="./"
bakup_folder="../complains_bakup"
file_name="${bakup_folder}/complaints_${version}_${tag}.tgz"
echo ${file_name}

# Create folder if not exists
mkdir -p ${bakup_folder}

if [ -f ${file_name} ] 
then
  echo "Error! The bakup file already exists. Change version and/or tag."
  exit 1
fi 


tar --exclude='bakup' --exclude='.idea' --exclude='__pycache__' --exclude='.git' -zcvf "${file_name}" "${src_folder}"

