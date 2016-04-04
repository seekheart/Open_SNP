#!/usr/bin/Rscript
#Script to make MongoDB from OpenSNP Json
#Mike Tung

#Setup libraries I'll be using
library(rjson)
library(plyr)
library(mongolite)

#load the json and process it into DF.
json_file <- fromJSON(file = 'opensnp.json')
data <- lapply(json_file, function(x) {
  as.data.frame(replace(x, sapply(x, is.list), NA))  
})
data <- rbind.fill(data)