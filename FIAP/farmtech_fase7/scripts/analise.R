dados <- read.csv("data/clima_historico.csv")
matriz_cor <- cor(dados[, c("temperatura", "umidade", "precipitacao")])
write.csv(matriz_cor, "data/clima_correlacao.csv", row.names = TRUE)
