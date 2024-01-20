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
bakup_folder="bakup"
file_name="${bakup_folder}/complaints_${version}_${tag}.tgz"
echo ${file_name}

if [ -f ${file_name} ] 
then
  echo "Error! The file with specified suffix already exists."
  exit 1
fi 


tar --exclude='bakup' --exclude='.idea' --exclude='__pycache__' --exclude='.git' -zcvf "${file_name}" "${src_folder}"

