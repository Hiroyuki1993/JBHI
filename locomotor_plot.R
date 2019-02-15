library(tidyverse)

activity = read_csv("./Todai_office_workers_data/Activity_data/todai_activity_2011.csv")
activity.oneday = activity[6933:8044,]
activity.oneday = activity.oneday %>% mutate(time = str_sub(`datetime (ddMONTHyy:hh:mm)`, -5,-1))
activity.oneday = activity.oneday %>% mutate(time = str_c("2011-11-", str_sub(`datetime (ddMONTHyy:hh:mm)`, 1, 2), time), time = as.POSIXct(time, "UTC"))

EMA = read_csv("./Todai_office_workers_data/Todai_EMA_2011-2012.csv")
EMA.oneday = EMA[42:48,]
EMA.oneday = EMA.oneday[-6,] # because of putoff
EMA.oneday = EMA.oneday %>% select(time) %>% mutate(end_time = as.POSIXct(time), start_time = end_time - 30*60)
write.csv(EMA.oneday, file = "EMAoneday.csv", row.names = F)
EMA.fill = read_csv("./EMA_fill.csv") # It requires some manual labor to transform data for area plot.

ggplot() + geom_area(data = EMA.fill, aes(x = time, y = ymax), fill = "gray") + 
  geom_bar(data = activity.oneday, aes(x = time, y = `Activity counts per minute`), stat = "identity", fill = "black") +
   theme_classic(base_size = 24) + ylab("Zero-Crossing Counts\n Per Minute") + scale_x_datetime(date_breaks = "3 hour", date_labels = "%H:%M") + xlab("Time")
