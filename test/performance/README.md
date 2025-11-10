# Testes de Performance

Este diretório contém os testes de performance para o projeto de simulação financeira.

## Configuração

Para executar os testes de performance, você precisará ter o `pytest-benchmark` instalado:

```bash
pip install pytest-benchmark
```

Ou instale todas as dependências:

```bash
pip install -r config/requirements.txt
```

## Executando os Testes

### Execução Básica

```bash
# Executar todos os testes de performance
pytest test/performance/performance_test.py --benchmark-only -v

# Executar um teste específico
pytest test/performance/performance_test.py::test_large_transaction_batch --benchmark-only -v
```

### Usando o Script Personalizado

```bash
# Execução simples
python test/performance/run_performance_tests.py

# Salvar resultados em JSON
python test/performance/run_performance_tests.py --json

# Gerar relatórios adicionais
python test/performance/run_performance_tests.py --html --json
```

## Testes Disponíveis

### Grupo "transaction"
- **`test_large_transaction_batch`**: Testa a performance de criação em lote de 1000 transações
- **`test_transaction_retrieval_performance`**: Testa a performance de recuperação de transações por usuário
- **`test_transaction_update_performance`**: Testa a performance de atualização de transações
- **`test_transaction_deletion_performance`**: Testa a performance de deleção de transações

### Grupo "query"
- **`test_transaction_by_account_performance`**: Testa a performance de consultas por conta
- **`test_transaction_by_category_performance`**: Testa a performance de consultas por categoria

## Interpretando os Resultados

O pytest-benchmark fornece estatísticas detalhadas incluindo:

- **Min**: Tempo mínimo de execução
- **Max**: Tempo máximo de execução  
- **Mean**: Tempo médio de execução
- **StdDev**: Desvio padrão
- **Median**: Mediana dos tempos
- **IQR**: Intervalo interquartil
- **Outliers**: Valores atípicos
- **OPS**: Operações por segundo

### Exemplo de Saída

```
Name (time in us)                           Min        Max        Mean      StdDev     Median      IQR     
test_transaction_retrieval_performance   605.30   1,983.00     799.27     151.49     782.50    30.45
test_large_transaction_batch          1,031K   1,092K    1,048K      25K   1,039K     21K
```

## Otimizações Identificadas

Com base nos testes de performance, você pode identificar:

1. **Operações mais lentas**: Criação em lote vs consultas individuais
2. **Gargalos de banco de dados**: Operações que podem se beneficiar de índices
3. **Padrões de uso**: Quais operações são mais frequentes e precisam de otimização

## Configuração Avançada

### Arquivo de Configuração

O arquivo `benchmark_config.json` contém configurações personalizadas para os benchmarks.

### Comparação com Versões Anteriores

Para comparar performance entre versões:

1. Execute os testes e salve uma baseline:
   ```bash
   pytest test/performance/ --benchmark-save=baseline
   ```

2. Após mudanças, compare:
   ```bash
   pytest test/performance/ --benchmark-compare=baseline
   ```

## Métricas de Performance Esperadas

| Operação | Volume | Tempo Esperado | OPS |
|----------|--------|---------------|-----|
| Criação individual | 1 transação | < 1ms | > 1000 |
| Criação em lote | 1000 transações | < 2s | > 500 |
| Consulta por usuário | 100 transações | < 1ms | > 1000 |
| Atualização | 50 transações | < 100ms | > 10 |

*Nota: Os valores são aproximados e podem variar dependendo do hardware.*