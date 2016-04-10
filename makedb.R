#!/usr/bin/Rscript
#Script to make MongoDB from OpenSNP Json
#Mike Tung

#Setup libraries I'll be using
library(rjson)
library(plyr)
library(mongolite)
library(ggplot2)

#load the json and process it into DF.
json_file <- fromJSON(file = 'opensnp.FULL.json')
data <- lapply(json_file, function(x) {
  as.data.frame(replace(x, sapply(x, is.list), NA))  
})
data <- rbind.fill(data)

#Make the mongodb
mongo_data$drop()
mongo_data <- mongo("data")
mongo_data$insert(data)

#I'm interested in looking at the distribution of Joggers both male and female with asthma
females <- mongo_data$find('{"Sex":"female"}', fields = '{"Sex":1, "Handedness":1,"Asthma":1, "Jogger":1}')
males <- mongo_data$find('{"Sex":"Male"}', fields = '{"Sex":1, "Handedness":1, "Asthma":1, "Jogger":1}')

athletes <- rbind(females,males)