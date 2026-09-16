from pathlib import Path
import argparse
import sys


def collect_target_files(base_directory: Path) -> list:
    """Collect .csv and .json files under 'Dados_Coletados/Dados_Brutos/Dados da API' recursively."""
    # O script está sendo executado da pasta raiz, então o caminho está correto
    dados_dir = base_directory / "Dados_Coletados" / "Dados_Brutos" / "Dados da API"
    print(f"Procurando arquivos em: {dados_dir}")
    
    if not dados_dir.exists():
        print(f"Diretório não encontrado: {dados_dir}")
        return []
    
    if not dados_dir.is_dir():
        print(f"O caminho existe mas não é um diretório: {dados_dir}")
        return []

    target_extensions = {".csv", ".json"}
    files = []
    for path in dados_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() in target_extensions:
            files.append(path)
    
    print(f"Encontrados {len(files)} arquivos .csv e .json")
    return files


def format_size(num_bytes: int) -> str:
    """Return human-readable size."""
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(num_bytes)
    for unit in units:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Apaga todos os arquivos .csv e .json dentro de 'Dados_Coletados/Dados_Brutos/Dados da API' "
            "e subpastas. Não remove diretórios."
        )
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Apenas lista o que seria apagado, sem apagar de fato.",
    )
    args = parser.parse_args()

    # Usar o diretório raiz do projeto como base (onde está o run.py)
    base_directory = Path(__file__).resolve().parents[1]
    print(f"Diretório base do projeto: {base_directory}")
    
    files = collect_target_files(base_directory)

    if not files:
        print("Nenhum arquivo .csv ou .json encontrado em 'Dados_Coletados/Dados_Brutos/Dados da API'.")
        return 0

    total_bytes = sum(f.stat().st_size for f in files if f.exists())

    if args.dry_run:
        print("[SIMULAÇÃO] Arquivos que seriam apagados:")
        for f in files:
            try:
                size = format_size(f.stat().st_size)
            except FileNotFoundError:
                size = "?"
            print(f"- {f} ({size})")
        print(
            "[SIMULAÇÃO] Total de arquivos: "
            f"{len(files)} | Espaço: {format_size(total_bytes)}"
        )
        return 0

    # Confirmar antes de apagar
    print(f"\nATENÇÃO: Você está prestes a apagar {len(files)} arquivos!")
    print(f"Espaço total que será liberado: {format_size(total_bytes)}")
    resposta = input("Digite 'SIM' para confirmar a exclusão: ")
    
    if resposta.upper() != 'SIM':
        print("Operação cancelada pelo usuário.")
        return 0

    errors = []
    for f in files:
        try:
            f.unlink()
            print(f"✓ Apagado: {f}")
        except OSError as exc:
            errors.append((f, str(exc)))
            print(f"✗ Erro ao apagar {f}: {exc}")

    deleted_count = len(files) - len(errors)
    remaining_bytes = sum(f.stat().st_size for f in files if f.exists())
    freed_bytes = max(0, total_bytes - remaining_bytes)

    print(f"\n{'='*50}")
    print(
        "Arquivos apagados: "
        f"{deleted_count}/{len(files)} | "
        "Espaço liberado (aprox.): "
        f"{format_size(freed_bytes)}"
    )

    if errors:
        print("\nAlguns arquivos não puderam ser apagados:")
        for f, msg in errors:
            print(f"- {f}: {msg}")
        return 1

    print("Limpeza concluída com sucesso!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
