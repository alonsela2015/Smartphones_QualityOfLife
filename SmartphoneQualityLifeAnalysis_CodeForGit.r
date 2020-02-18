########################################################################################
# # This code is a part of the data analysis in the Smartphone Lifequality article.  # #
# # The code inspects the different questions on the questionairs, and finds the     # #
# # relationships between the different features.                                    # #
# # Created by Dr. Alon Sela 24.7.2019                                               # #
# # For questions you can contact me al alonse@ariel.c.il                            # #
########################################################################################
install.packages("Rtools")
install.packages("clmm2")
install.packages("readstata13")
install.packages("pheatmap")
install.packages("glm")
install.packages("lme4")
## load package
library(pheatmap)
library(readstata13)
library(lme4)

# setwd("../data/")
a<-Sys.info()
MYPATH<-dirname(rstudioapi::getSourceEditorContext()$path)
setwd(MYPATH)
dat<-read.csv(file = "../data/results3.9 withCorrelations.csv", header = TRUE, stringsAsFactors = FALSE, )

dat<-read.csv(file = "E:/dropbox/Dropbox/_WORK_IN_PROGRESS/Smartphone H bengal/2019/data/results3.9 withCorrelations.csv", header = TRUE, stringsAsFactors = FALSE, )
header<-colnames(dat)
df2<-dat
# Change variable to ordered var
# ordrd_df2<-ordered(df2)
# Normalize sum of "well being" factors
df2$sum<-(round(as.numeric(dat$sum) / 10))
# 
df2$sum<-ordered(df2$sum, levels = c(0,1 ,2 ,3, 4, 5, 6, 7, 8, 9))
colnames(df2) <- header

# compute spearman ranked correlation matrix for variable 1:16 vs 39
dt<-as.data.frame(c())
for (j in 1:38){
  a<-c()
  for (i in 1:38){
    a<-c(a,cor(as.numeric(df2[,i]), as.numeric(df2[,j]), use = "complete.obs", method="spearman"))
  }
  dt<-rbind(dt,a)
}
#check absolute value of corelations.
#dt<-abs(dt)

mat_dt<-as.matrix(dt)

colnames(mat_dt) <- c(header)
row.names(mat_dt) <- c(header)

# First heatmap - all questions
heatmap(t(mat_dt[1:37, 1:37]), 
        labRow = rownames(mat_dt),
        labCol = header, 
        hclustfun = hclust,
        symm = TRUE, margins = c(20,20),
        cexRow = 0.5,
        cexCol = 0.5)
  
# Second heatmap - Only Smartphone use on Life Quality effect
mat_short<-mat_dt[1:15,16:37]

heatmap(t(mat_short), 
        labRow = rownames(mat_short),
        labCol = colnames(mat_short), 
        symm = FALSE, margins = c(13,13), 
        cexRow = 0.9)

# Separates to two components according to the hirarchical clusteirng analysis
# We name these clusters, the "Latent" and the "Concious" clusters of factors.

Latent <- (df2$Do.you.use.your.smartphone.in.parallel.with.other.activities...driving..cooking...TV. +
           df2$How.many.apps.you.have.in.your.smartphone. + 
           df2$Do.you.go.to.bed.with.the.smartphonephone.at.your.side. +
           df2$Do.you.use.your.smartphone.in.the.middle.of.the.night. +
           df2$Do.you.consider.yourself.as.addicted.to.the.use.of.the.smartphone.) / 5
Concious<-(df2$Do.you.consider.the.smartphone.an.indispensable.tool.for.your.work.+
           df2$Do.you.consider.the.smartphon.an.indispensable.tool.for.your.social.life.+
           df2$Do.you.take.your.smartphone.with.you.to.the.restroom.+
           df2$How.many.social.networks..e.g..facebook..twitter..are..on.your.smartphone.+
           df2$how.many.socia.netowrks.apps+
           df2$Do.you.use.the.location.based.services.of.the.smartphone.+
           df2$For.how.long.have.you.had.a.smartphone.+
           df2$How.many.apps.you.have.in.your.smartphone.+
           df2$How.often.do.you.change.your.smartphone.+
           df2$Do.you.use.your.smartphone.camera..calculator..notes..reading.book..payments.) / 10

# binds the Latent cluster, the Concious cluster, and the Lfe Quality results into a single data frame.
reg_table<-as.data.frame(cbind(dat$sum, Concious, Latent, deparse.level = 1))
colnames(reg_table) <- c("LifeQuality","Concious", "Latent")
# Thre were only a few NA in the data, but these were removed. 
reg_table<-na.omit(reg_table)
# Normalize to Unit size in order to find a true slope in the regression
normalize <- function(x) {
  return ((x - min(x)) / (max(x) - min(x)))
}
reg_table$LifeQuality <- normalize(reg_table$LifeQuality) 
reg_table$Concious<-normalize(reg_table$Concious) 
reg_table$Latent<-normalize(reg_table$Latent)
#Histogram of Life_quality measure
plot.new()
hist(reg_table$LifeQuality, breaks = 30, xlab = "Life_Quality (Normalized)", main = "Life Quality Distribution")
med<-median(reg_table$LifeQuality)
#med<-0.4
abline(v=med, col="red", lwd=3, lty=2)

# # create a boolean measure of life quality above / below median
# reg_table_latent$LifeQualityBoolean<-reg_table_latent$LifeQuality <= med

# simple regresson analysis
linearMod <- lm(LifeQuality ~ Concious + Latent, data=reg_table)
summary(linearMod)


# simple regresson analysis
linearMod <- lm(LifeQuality ~ Concious + Latent, data=reg_table)
summary(linearMod)


# # ################################################################
