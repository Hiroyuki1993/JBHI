library(tidyverse)
library(lme4)
library(lmerTest)
library(MuMIn)

averageActivity = function(activities) {
  x = strsplit(activities, " ")
  y = as.integer(unlist(x))
  mean(y)
}

data = read_csv("./result_3h.csv")
data = data %>% select(patient_id, activities, total_dep)
data %>% mutate(mean_act = mean(as.integer(strsplit(activities, " ")[[1]])))

data = data %>% mutate(mean_act = purrr::map_dbl(activities, averageActivity))

cor(data$total_dep, data$mean_act, use = "complete.obs")
res = lmer(total_dep ~ mean_act + (1|patient_id), data=data, REML=FALSE)
summary(res)
r.squaredGLMM(res)
