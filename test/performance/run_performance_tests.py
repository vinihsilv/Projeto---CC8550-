#!/usr/bin/env python3
"""
Script para executar testes de performance do projeto.

Uso:
    python run_performance_tests.py [--html] [--json] [--compare]

Opções:
    --html      Gera relatório HTML
    --json      Salva resultados em JSON
    --compare   Compara com resultados anteriores
"""

import sys
import subprocess
from pathlib import Path


def run_performance_tests(generate_html=False, save_json=False, compare=False):
    """Executa os testes de performance com opções configuráveis."""

    # Comando base
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "test/performance/performance_test.py",
        "-v",
        "--benchmark-only",
    ]

    # Adicionar opções baseadas nos parâmetros
    if generate_html:
        cmd.extend(["--benchmark-save-data"])

    if save_json:
        cmd.extend(["--benchmark-json=test/performance/performance_results.json"])

    if compare:
        # Verifica se existe arquivo de comparação
        compare_file = Path("test/performance/performance_baseline.json")
        if compare_file.exists():
            cmd.extend([f"--benchmark-compare={compare_file}"])
        else:
            print(
                "Aviso: Arquivo de baseline não encontrado. Execute primeiro sem --compare."
            )

    # Configurações adicionais do benchmark
    cmd.extend(
        ["--benchmark-min-rounds=5", "--benchmark-warmup=on", "--benchmark-sort=mean"]
    )

    print("Executando testes de performance...")
    print(f"Comando: {' '.join(cmd)}")
    print("-" * 50)

    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print("\nTestes de performance concluídos com sucesso!")

        if generate_html:
            print("Relatórios salvos em: test/performance/")

        if save_json:
            print(
                "Resultados JSON salvos em: test/performance/performance_results.json"
            )

    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar testes: {e}")
        return False

    return True


def main():
    """Função principal."""
    import argparse

    parser = argparse.ArgumentParser(description="Executar testes de performance")
    parser.add_argument("--html", action="store_true", help="Gerar relatório HTML")
    parser.add_argument("--json", action="store_true", help="Salvar resultados em JSON")
    parser.add_argument(
        "--compare", action="store_true", help="Comparar com resultados anteriores"
    )

    args = parser.parse_args()

    success = run_performance_tests(
        generate_html=args.html, save_json=args.json, compare=args.compare
    )

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
