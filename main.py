import json
import os
from datetime import datetime


ARQUIVO_DADOS = "data/vagas.json"


def carregar_vagas():
    if not os.path.exists(ARQUIVO_DADOS):
        return []

    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def salvar_vagas(vagas):
    os.makedirs("data", exist_ok=True)

    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(vagas, arquivo, ensure_ascii=False, indent=4)


def gerar_id(vagas):
    if not vagas:
        return 1

    return max(vaga["id"] for vaga in vagas) + 1


def cadastrar_vaga(vagas):
    print("\n=== NOVA CANDIDATURA ===")

    empresa = input("Empresa: ").strip()
    cargo = input("Cargo: ").strip()
    tecnologias = input("Tecnologias (separe por vírgula): ").strip()
    link = input("Link da vaga: ").strip()
    observacoes = input("Observações: ").strip()

    if not empresa or not cargo:
        print("\nEmpresa e cargo são obrigatórios.")
        return

    vaga = {
        "id": gerar_id(vagas),
        "empresa": empresa,
        "cargo": cargo,
        "tecnologias": [
            tecnologia.strip()
            for tecnologia in tecnologias.split(",")
            if tecnologia.strip()
        ],
        "data_candidatura": datetime.now().strftime("%d/%m/%Y"),
        "status": "Aplicado",
        "link": link,
        "observacoes": observacoes
    }

    vagas.append(vaga)
    salvar_vagas(vagas)

    print("\nCandidatura cadastrada com sucesso!")


def listar_vagas(vagas):
    print("\n=== MINHAS CANDIDATURAS ===")

    if not vagas:
        print("Nenhuma candidatura cadastrada.")
        return

    for vaga in vagas:
        tecnologias = ", ".join(vaga["tecnologias"])

        print(f"\nID: {vaga['id']}")
        print(f"Empresa: {vaga['empresa']}")
        print(f"Cargo: {vaga['cargo']}")
        print(f"Tecnologias: {tecnologias}")
        print(f"Data: {vaga['data_candidatura']}")
        print(f"Status: {vaga['status']}")
        print(f"Link: {vaga['link']}")
        print(f"Observações: {vaga['observacoes']}")
        print("-" * 50)


def buscar_vaga(vagas):
    print("\n=== BUSCAR CANDIDATURA ===")

    termo = input("Digite empresa ou cargo: ").strip().lower()

    if not termo:
        print("Digite algum termo para realizar a busca.")
        return

    resultados = [
        vaga
        for vaga in vagas
        if termo in vaga["empresa"].lower()
        or termo in vaga["cargo"].lower()
    ]

    if not resultados:
        print("\nNenhuma candidatura encontrada.")
        return

    for vaga in resultados:
        print(
            f"\nID: {vaga['id']} | "
            f"{vaga['empresa']} | "
            f"{vaga['cargo']} | "
            f"{vaga['status']}"
        )


def atualizar_status(vagas):
    print("\n=== ATUALIZAR STATUS ===")

    if not vagas:
        print("Nenhuma candidatura cadastrada.")
        return

    try:
        id_vaga = int(input("Digite o ID da candidatura: "))
    except ValueError:
        print("ID inválido.")
        return

    vaga = next((vaga for vaga in vagas if vaga["id"] == id_vaga), None)

    if not vaga:
        print("Candidatura não encontrada.")
        return

    print("\nStatus disponíveis:")
    print("1 - Aplicado")
    print("2 - Entrevista")
    print("3 - Teste técnico")
    print("4 - Rejeitado")
    print("5 - Contratado")

    opcao = input("Escolha o novo status: ").strip()

    status_map = {
        "1": "Aplicado",
        "2": "Entrevista",
        "3": "Teste técnico",
        "4": "Rejeitado",
        "5": "Contratado"
    }

    if opcao not in status_map:
        print("Opção inválida.")
        return

    vaga["status"] = status_map[opcao]
    salvar_vagas(vagas)

    print("\nStatus atualizado com sucesso!")


def excluir_vaga(vagas):
    print("\n=== EXCLUIR CANDIDATURA ===")

    if not vagas:
        print("Nenhuma candidatura cadastrada.")
        return

    try:
        id_vaga = int(input("Digite o ID da candidatura: "))
    except ValueError:
        print("ID inválido.")
        return

    vaga = next((vaga for vaga in vagas if vaga["id"] == id_vaga), None)

    if not vaga:
        print("Candidatura não encontrada.")
        return

    confirmacao = input(
        f"Excluir a candidatura para {vaga['empresa']}? (s/n): "
    ).strip().lower()

    if confirmacao != "s":
        print("Operação cancelada.")
        return

    vagas.remove(vaga)
    salvar_vagas(vagas)

    print("\nCandidatura excluída com sucesso!")


def mostrar_estatisticas(vagas):
    print("\n=== ESTATÍSTICAS ===")

    total = len(vagas)

    if total == 0:
        print("Nenhuma candidatura cadastrada.")
        return

    status_contagem = {
        "Aplicado": 0,
        "Entrevista": 0,
        "Teste técnico": 0,
        "Rejeitado": 0,
        "Contratado": 0
    }

    for vaga in vagas:
        status = vaga["status"]

        if status in status_contagem:
            status_contagem[status] += 1

    print(f"Total de candidaturas: {total}")

    for status, quantidade in status_contagem.items():
        print(f"{status}: {quantidade}")

    entrevistas = (
        status_contagem["Entrevista"]
        + status_contagem["Teste técnico"]
        + status_contagem["Contratado"]
    )

    taxa_entrevista = (entrevistas / total) * 100

    print(f"Taxa de avanço: {taxa_entrevista:.1f}%")


def exibir_menu():
    print("\n" + "=" * 50)
    print("         PYTHON JOB TRACKER")
    print("=" * 50)

    print("1 - Cadastrar candidatura")
    print("2 - Listar candidaturas")
    print("3 - Buscar candidatura")
    print("4 - Atualizar status")
    print("5 - Excluir candidatura")
    print("6 - Mostrar estatísticas")
    print("0 - Sair")


def main():
    vagas = carregar_vagas()

    while True:
        exibir_menu()

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_vaga(vagas)

        elif opcao == "2":
            listar_vagas(vagas)

        elif opcao == "3":
            buscar_vaga(vagas)

        elif opcao == "4":
            atualizar_status(vagas)

        elif opcao == "5":
            excluir_vaga(vagas)

        elif opcao == "6":
            mostrar_estatisticas(vagas)

        elif opcao == "0":
            print("\nEncerrando o Python Job Tracker...")
            break

        else:
            print("\nOpção inválida.")


if __name__ == "__main__":
    main()