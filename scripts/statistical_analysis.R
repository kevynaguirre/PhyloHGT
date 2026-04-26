# Core
library(tidyverse)
# ML / evaluation
library(caret)
library(pROC)
library(MLmetrics)
library(mltools)
# Stats
library(PMCMRplus)
# Plotting extras
library(ggpubr)


#Statistical analysis of scores of ML models trained
#Load dataset
 
path_db <- "all_models_results.csv"
db <- read.csv(path_db, stringsAsFactors = FALSE)
 
results_list <- list()
plot_list <- list()
for (i in colnames(db)[-c(1,2)]) {
  temp_db <- db %>% select(fold, model, i) %>% pivot_wider(id_cols = "fold", names_from = "model", values_from = all_of(i))
  matrix_db <- as.matrix(temp_db[,-1]) #To work with the following tests i need data as matrix and i do not need col "fold"
  rownames(matrix_db) <- 1:dim(temp_db)[1]
  cat("\n✅ Created dataset for:", i, "\n")
  cat("📏 Dimensions:", paste(dim(matrix_db), collapse = " x "), "\n")
  #Now Run Fried man test
  friedman_test <- friedman.test(as.matrix(matrix_db))
  print(friedman_test$p.value)
  #Now run posthoc test to see which model differ
  posthoc <- frdAllPairsNemenyiTest(matrix_db, p.adjust = "bonferroni")
  print(posthoc$p.value)
  #summary(posthoc)
  #Graph the CD tree
  plot(posthoc, main = "", ylab = "")
  title(main = paste("Boxplot for", i), ylab = paste(i,"Mean"))
  # Mean and SD
  means <- round(colMeans(matrix_db), 4)
  sds   <- round(apply(matrix_db, 2, sd), 4)
  # Combine mean ± sd into one string per model
  combined <- paste0(means, " ± ", sds)
  names(combined) <- names(means)
  df_metric <- data.frame(
    metric = i,
    t(as.data.frame(combined)),
    row.names = NULL
  )
  #print(df_metric)
  results_list[[i]] <- df_metric
  # ---- Capture the plot ----
  plot_list[[i]] <- recordPlot({
    plot(posthoc)
    title(main = paste("Posthoc test for", i), ylab = "Mean")
  })

}
 
 
# Merge all metrics
results_df <- bind_rows(results_list)
write.csv(results_df, "statistical_results_df.csv")

#########################################################################################################
############## Start Statistical analysis with Hyperparameter tuned models ##############################
#########################################################################################################

path_db <- "op_models_results.csv"
db <- read.csv(path_db, stringsAsFactors = FALSE)

results_list <- list()
plot_list <- list()
for (i in colnames(db)[-c(1,2)]) {
  temp_db <- db %>% select(fold, model, i) %>% pivot_wider(id_cols = "fold", names_from = "model", values_from = all_of(i))
  matrix_db <- as.matrix(temp_db[,-1]) #To work with the following tests i need data as matrix and i do not need col "fold"
  rownames(matrix_db) <- 1:dim(temp_db)[1]
  cat("\n✅ Created dataset for:", i, "\n")
  cat("📏 Dimensions:", paste(dim(matrix_db), collapse = " x "), "\n")
  #Now Run Fried man test
  friedman_test <- friedman.test(as.matrix(matrix_db))
  print(friedman_test$p.value)
  #Now run posthoc test to see which model differ
  posthoc <- frdAllPairsNemenyiTest(matrix_db, p.adjust = "bonferroni")
  print(posthoc$p.value)
  #summary(posthoc)
  #Graph the CD tree
  plot(posthoc, main = "", ylab = "")
  title(main = paste("Boxplot for", i), ylab = paste(i,"Mean"))
  # Mean and SD
  means <- round(colMeans(matrix_db), 4)
  sds   <- round(apply(matrix_db, 2, sd), 4)
  # Combine mean ± sd into one string per model
  combined <- paste0(means, " ± ", sds)
  names(combined) <- names(means)
  df_metric <- data.frame(
    metric = i,
    t(as.data.frame(combined)),
    row.names = NULL
  )
  #print(df_metric)
  results_list[[i]] <- df_metric
  # ---- Capture the plot ----
  plot_list[[i]] <- recordPlot({
    plot(posthoc)
    title(main = paste("Posthoc test for", i), ylab = "Mean")
  })

}
 
 
# Merge all metrics
results_df <- bind_rows(results_list)
write.csv(results_df, "statistical_op_results_df.csv")
