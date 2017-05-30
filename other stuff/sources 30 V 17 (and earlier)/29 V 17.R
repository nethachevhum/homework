setwd("C:/Users/netkachev/Documents/ВМЛИ/Проект/Ordinals Map")
df <- read.csv("output2.csv", sep = ";", header = F)

library(lingtypology)
map.feature(languages = df$V4,
            longitude = df$V3,
            latitude = df$V2,
            features = df$V8,
            stroke.features = df$V5,
            stroke.color = c("brown","yellow","blue","darkgoldenrod1","palegreen1","bisque4"),
            label = df$V4,
            popup = df$V1,
            color = c("tomato", "dodgerblue", "green", "gold"),
            radius = 2,
            stroke.radius = 7,
            minimap = TRUE)
