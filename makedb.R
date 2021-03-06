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

#remove ".." from data labels
data_labels <- colnames(data)
data_labels <- gsub("[.]+", "_", data_labels, perl = TRUE)
colnames(data) <- data_labels

#Make the mongodb
mongo_data$drop()
mongo_data <- mongo("data")
mongo_data$insert(data)

#check data integrity by export
mongo_data$export(file("snp_db_data.txt"))

#I'm interested in looking at the distribution of Joggers both male and female with asthma
females <- mongo_data$find('{"Sex":"female"}', fields = '{"Sex":1, "Handedness":1,"Asthma":1, "Jogger":1, "ethnicity":1}')
males <- mongo_data$find('{"Sex":"Male"}', fields = '{"Sex":1, "Handedness":1, "Asthma":1, "Jogger":1, "ethnicity":1}')

athletes <- rbind(females,males)

#clean up data here by grouping related categories together and removing N/As
athletes <- na.omit(athletes)
athletes$Sex[athletes$Sex == "female"] <- "Female"
athletes$Jogger[athletes$Jogger == "No" | athletes$Jogger == "no"] <- "Never"
athletes$Jogger[athletes$Jogger == "Rare" | athletes$Jogger == "rare"] <- "Never"
athletes$Jogger[athletes$Jogger == "I work hard and walk alot no need to jog"] <- "Never"
athletes$Jogger[athletes$Jogger == "never"] <- "Never"
athletes$Jogger[athletes$Jogger == "Regular" | athletes$Jogger == "regular"| athletes$Jogger == "sometimes"] <- "Sometimes"


athletes$Asthma[athletes$Asthma == "slight"] <- "Slight"
athletes$Asthma[athletes$Asthma == "False" | athletes$Asthma == "No" | athletes$Asthma == "no"
                     | athletes$Asthma == "No (but i&#39;m not sure)"] <- "No Asthma"

#visualize the data on athletes based on sex and asthma levels
data_plot <- ggplot(athletes, aes(factor(Sex), fill = Asthma)) 
data_plot <- data_plot + xlab("Sex") + ylab("Number of Joggers") + ggtitle("Asthma Levels of Joggers Based on Frequency of Jogging")
data_plot + geom_bar(position="dodge") + scale_fill_brewer(palette = "Spectral") + facet_grid(.~Jogger)
