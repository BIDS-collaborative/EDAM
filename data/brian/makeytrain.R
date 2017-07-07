setwd("C:/Users/Brian/Dropbox/BIDS/EDAM/brian")
df = read.csv("pacificplants.csv")
df2 = read.csv("pier_html_data.csv", header = FALSE)
df2[[1]] = as.character(df2[[1]])
df$Scientific.Name = gsub(" ", "_", df$Scientific.Name)
df$Scientific.Name = tolower(df$Scientific.Name)
recommendations = gsub("[[:punct:]]", "", df$Recommendation)

risks = c()
evaluates = c()
for (i in 1:length(df2[[1]])) {
  index = which(df$Scientific.Name == df2[[1]][i])[1]
  recommendation = recommendations[index]
  if (recommendation == "low risk") {
    risks = c(risks, 0)
  }
  else if (recommendation == "evaluate") {
    evaluates = c(evaluates, df2[[1]][i])
  }
  else {
    risks = c(risks, 1)
  }
}
remove = c()
for (i in 1:length(evaluates)) {
  index = which(df2[[1]] == evaluates[i])
  remove = c(remove, index)
}
df3 = df2[-remove, ]


risks = data.frame(risks)
write.csv(df3, file = "pier_html_data_noevaluates.csv", row.names = FALSE)
write.csv(risks, file = "pier_html_labels_noevaluates.csv", row.names = FALSE)