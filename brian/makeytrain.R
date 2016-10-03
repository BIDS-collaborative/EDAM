setwd("C:/Users/Brian/Dropbox/BIDS/EDAM/brian")
df = read.csv("pacificplants.csv")
df2 = read.csv("pier_html_data.csv", header = FALSE)
df2[[1]] = as.character(df2[[1]])
df$Scientific.Name = gsub(" ", "_", df$Scientific.Name)
df$Scientific.Name = tolower(df$Scientific.Name)
recommendations = gsub("[[:punct:]]", "", df$Recommendation)

risks = c()
for (i in 1:length(df2[[1]])) {
  index = which(df$Scientific.Name == df2[[1]][i])[1]
  recommendation = df$Recommendation[index]
  if (recommendation == "low risk") {
    risks = c(risks, 0)
  }
  else if (recommendation == "evaluate") {
    risks = c(risks, 1)
  }
  else {
    risks = c(risks, 2)
  }
}

risks = data.frame(risks)
write.csv(risks, file = "pier_html_labels.csv", row.names = FALSE)