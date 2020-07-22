#GLM

path = "c:/users/kryst/desktop/Poisson/Poisson-neural-network-insurance-pricing/preprocFull.csv"
path2 = "c:/users/kryst/desktop/Poisson/Poisson-neural-network-insurance-pricing/catOnly.csv"

data = read.csv(path)
data2 = read.csv(path2)

#Y : nclaims
y1 = data$NumberClaims
y2 = data2$NumberClaims

#duration
d1 = data$Duration
d2 = data$Duration

#delete the columns that we don't need for X
data = data[, -match(c("ClaimFrequency"), names(data))]
data2 = data2[, -match(c("X", "ClaimCost"), names(data2))]

model = glm(formula = NumberClaims ~ Gender.F + Zone.1 + Zone.2 + Zone.3 + Zone.4 + Zone.5 + Zone.6 + 
              Class.1 + Class.2 + Class.3 + Class.4 + Class.5 + Class.6 + 
              BonusClass.1 + BonusClass.2 + BonusClass.3 + BonusClass.4 + BonusClass.5 + BonusClass.6 + 
              OwnersAge + VehiculeAge, 
            family = poisson(link = "log"),
            data = data,
            offset = log(Duration)
            )

summary(model)
residuals(model) #residuals ^y-y
fitted(model) #predictions ?
plot(model)
step(model)

#refined model after step
refModel = glm(formula = NumberClaims ~ Gender.F + Zone.1 + Zone.2 + Zone.3 + 
      Class.3 + Class.4 + Class.6 + BonusClass.4 + OwnersAge + 
      VehiculeAge, family = poisson(link = "log"), data = data, 
    offset = log(Duration))
summary(refModel)

#second dataset
model2 = glm(formula = NumberClaims ~ Gender_M + Zone_2 + Zone_3 + Zone_4 + Zone_5 + Zone_6 + Zone_7 + 
               Class_2 + Class_3 + Class_4 + Class_5 + Class_6 + Class_7 + 
               BonusClass_2 + BonusClass_3 + BonusClass_4 + BonusClass_5 + BonusClass_6 + BonusClass_7 + 
               OwnersAgeCat_1 + OwnersAgeCat_2 + OwnersAgeCat_3 + OwnersAgeCat_4 + OwnersAgeCat_5 + 
               OwnersAgeCat_6 + OwnersAgeCat_7 + 
               VehiculeAgeCat_1 + VehiculeAgeCat_2 + VehiculeAgeCat_3 + VehiculeAgeCat_4 + VehiculeAgeCat_5,
             family = poisson(link = "log"),
             data = data2,
             offset = log(Duration)
             )

summary(model2)
residuals(model2) #residuals ^y-y
fitted(model2) #predictions ?
plot(model2) 

step(model2)

refModel2 = glm(formula = NumberClaims ~ Gender_M + Zone_2 + Zone_3 + Zone_4 + 
                  Zone_5 + Zone_6 + Zone_7 + Class_3 + Class_4 + Class_6 + 
                  BonusClass_4 + BonusClass_7 + OwnersAgeCat_1 + OwnersAgeCat_2 + 
                  OwnersAgeCat_3 + OwnersAgeCat_4 + OwnersAgeCat_5 + OwnersAgeCat_6 + 
                  VehiculeAgeCat_1 + VehiculeAgeCat_2 + VehiculeAgeCat_3 + 
                  VehiculeAgeCat_4 + VehiculeAgeCat_5, family = poisson(link = "log"), 
                data = data2, offset = log(Duration))
summary(refModel2)




















