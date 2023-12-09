--- Retorna todos os autos com veiculo citado, cujo veículo faz parte da nossa grota
SELECT *
FROM auto_infracao
JOIN veiculos  ON veiculo = veiculos.num_veiculo;

--- Retorna todos os autos sem veiculo citado cuja consorcio é composto pelas empresas do grupo
SELECT *
FROM auto_infracao
JOIN operadora ON auto_infracao.concessionaria = operadora.concessionaria
WHERE veiculo IS NULL;

--- Retorna todos os autos sem veiculo citado cuja linha é operada pelo grupo de forma compartilhada
SELECT *
FROM auto_infracao
JOIN linha ON auto_infracao.linha = linha.num_linha
WHERE veiculo IS NULL and linha.compartilhada = 1;

--- Retorna todos os autos sem veiculo citado cuja linha é operada pelo grupo de forma exclusiva
SELECT *
FROM auto_infracao
JOIN linha ON auto_infracao.linha = linha.num_linha
WHERE veiculo IS NULL and linha.compartilhada = 0;