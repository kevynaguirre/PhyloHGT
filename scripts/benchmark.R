# Load libraries
library(tidyverse)
library(caret)
library(pROC)
library(MLmetrics)
library(mltools)
library(ggplot2)
library(ggpubr)
# ---- INPUT FILES ----
pred_file <- "results/simulation_pred.tsv"
avp_file  <- "results/simulation_avp.tsv"
# ---- LOAD DATA ----
df <- read.csv(pred_file, sep="\t", stringsAsFactors = FALSE)
avp <- read.csv(avp_file, sep="\t", stringsAsFactors = FALSE)
colnames(avp) <- c("filename", "AVP")
# ---- STANDARDIZE LABELS ----
standardize_label <- function(x) {
  case_when(
    x == "iHGT" ~ "iHGT",
    x == "NoHGT" ~ "NoHGT",
    TRUE ~ "Inconclusive"
  )
}
df <- df %>%
  mutate(
    Reference = standardize_label(tag),
    RF = standardize_label(pred)
  )
avp <- avp %>%
  mutate(AVP = standardize_label(AVP))
# ---- MERGE DATA ----
df_full <- df %>%
  select(filename, Reference, RF) %>%
  left_join(avp, by = "filename")
# ---- CONVERT TO FACTOR ----
df_full$Reference <- as.factor(df_full$Reference)
df_full$RF <- as.factor(df_full$RF)
df_full$AVP <- as.factor(df_full$AVP)
# ---- METRICS ----
# Accuracy
accuracy_mytool <- mean(df_full$RF == df_full$Reference, na.rm = TRUE)
accuracy_avp <- mean(df_full$AVP == df_full$Reference, na.rm = TRUE)
# Confusion matrices
cm_mytool <- confusionMatrix(df_full$RF, df_full$Reference)
cm_avp <- confusionMatrix(df_full$AVP, df_full$Reference)
# Macro metrics
precision_mytool <- mean(cm_mytool$byClass[, "Precision"], na.rm=TRUE)
recall_mytool <- mean(cm_mytool$byClass[, "Recall"], na.rm=TRUE)
f1_mytool <- mean(cm_mytool$byClass[, "F1"], na.rm=TRUE)
precision_avp <- mean(cm_avp$byClass[, "Precision"], na.rm=TRUE)
recall_avp <- mean(cm_avp$byClass[, "Recall"], na.rm=TRUE)
f1_avp <- mean(cm_avp$byClass[, "F1"], na.rm=TRUE)
# MCC
mcc_mytool <- mcc(df_full$RF, df_full$Reference)
mcc_avp <- mcc(df_full$AVP, df_full$Reference)
# ---- BUILD METRICS TABLE ----
metrics <- data.frame(
  Metric = rep(c("Accuracy","Precision","Recall","F1-score","MCC"),2),
  Value = c(accuracy_mytool,precision_mytool,recall_mytool,f1_mytool,mcc_mytool,
            accuracy_avp,precision_avp,recall_avp,f1_avp,mcc_avp),
  Tool = rep(c("RF","AVP"), each=5)
)
print(metrics)
# ---- PLOT ----
p_sim <- ggplot(metrics, aes(x=Metric, y=Value, fill=Tool)) +
  geom_bar(stat="identity", position=position_dodge()) +
  geom_text(aes(label=round(Value,3),
                vjust=ifelse(Value >= 0, -0.3, 1.3)),
            position=position_dodge(width=0.9),
            size=3) +
  coord_cartesian(ylim=c(-0.1,1)) +
  theme_minimal() +
  labs(y="Metric value", x="") +
  ggpubr::theme_pubr()
# ---- SAVE FIGURES ----
ggsave("sim_benchmark.tiff", plot = p_sim, width = 15 , height = 9, units = "cm", dpi = 400)


################################################
# work with real biological data
# ---- INPUT FILES ----
pred_file <- "results/real_biological_pred.tsv"
avp_file  <- "results/real_biological_avp.tsv"
# ---- LOAD DATA ----
df <- read.csv(pred_file, sep="\t", stringsAsFactors = FALSE)
avp <- read.csv(avp_file, sep="\t", stringsAsFactors = FALSE)
colnames(avp) <- c("filename", "AVP")
# ---- STANDARDIZE LABELS ----
standardize_label <- function(x) {
  case_when(
    x == "iHGT" ~ "iHGT",
    x == "NoHGT" ~ "NoHGT",
    TRUE ~ "Inconclusive"
  )
}
df <- df %>%
  mutate(
    Reference = standardize_label(tag),
    RF = standardize_label(pred)
  )
avp <- avp %>%
  mutate(AVP = standardize_label(AVP))
# ---- MERGE DATA ----
df_full <- df %>%
  select(filename, Reference, RF) %>%
  left_join(avp, by = "filename")
# ---- CONVERT TO FACTOR ----
df_full$Reference <- as.factor(df_full$Reference)
df_full$RF <- as.factor(df_full$RF)
df_full$AVP <- as.factor(df_full$AVP)
# ---- METRICS ----
# Accuracy
accuracy_mytool <- mean(df_full$RF == df_full$Reference, na.rm = TRUE)
accuracy_avp <- mean(df_full$AVP == df_full$Reference, na.rm = TRUE)
# Confusion matrices
cm_mytool <- confusionMatrix(df_full$RF, df_full$Reference)
cm_avp <- confusionMatrix(df_full$AVP, df_full$Reference)
# Macro metrics
precision_mytool <- mean(cm_mytool$byClass[, "Precision"], na.rm=TRUE)
recall_mytool <- mean(cm_mytool$byClass[, "Recall"], na.rm=TRUE)
f1_mytool <- mean(cm_mytool$byClass[, "F1"], na.rm=TRUE)
precision_avp <- mean(cm_avp$byClass[, "Precision"], na.rm=TRUE)
recall_avp <- mean(cm_avp$byClass[, "Recall"], na.rm=TRUE)
f1_avp <- mean(cm_avp$byClass[, "F1"], na.rm=TRUE)
# MCC
mcc_mytool <- mcc(df_full$RF, df_full$Reference)
mcc_avp <- mcc(df_full$AVP, df_full$Reference)
# ---- BUILD METRICS TABLE ----
metrics <- data.frame(
  Metric = rep(c("Accuracy","Precision","Recall","F1-score","MCC"),2),
  Value = c(accuracy_mytool,precision_mytool,recall_mytool,f1_mytool,mcc_mytool,
            accuracy_avp,precision_avp,recall_avp,f1_avp,mcc_avp),
  Tool = rep(c("RF","AVP"), each=5)
)
print(metrics)
# ---- PLOT ----
#Plot real data
p_real <- ggplot(metrics, aes(x=Metric, y=Value, fill=Tool)) +
  geom_bar(stat="identity", position=position_dodge()) +
  geom_text(aes(label=round(Value,3)),
            position=position_dodge(width=0.9),
            vjust=-0.3,
            size=3) +
  ylim(0,1) +
  theme_minimal() +
  labs(
    title="",
    y="Metric value",
    x=""
  ) + ggpubr::theme_pubr() + theme(legend.position = "right")
# ---- SAVE FIGURES ----
ggsave("real_bio_benchmark.tiff", plot = p_real, width = 15 , height = 9, units = "cm", dpi = 400)
