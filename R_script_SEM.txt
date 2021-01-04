library(lavaan)

full.model2 <- 'competence =~ y2 + y12 + y15 + y16 + y17 + y18
                   functioning =~ y3 +y4+y5+y6+y9+y10+y11+y13+y14+ y21
                   positive_feeling =~ y1 + y7 + y8 + y19 + y20 + y22
   
                   unaware =~ x4+x3+x5+x6+x12+x11+x10

                   aware =~ x2+x7+x8+x9
 
                   y13 ~~ y14
 	                y4 ~~ y3
 	                y12 ~~ y15
 
         competence ~ unaware + aware
         functioning ~  unaware + aware
         positive_feeling ~  unaware + aware'
full.fit2 <- cfa(full.model2,res_SEM)
summary(full.fit2,standardized = TRUE , fit.measures = TRUE)

semPaths(full.fit2, intercepts = FALSE,edge.label.cex = 1, what = 'std',structural = TRUE)
