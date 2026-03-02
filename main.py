import json
import os

nome_arquivo = "estoque.json"

def carregar_dados():
    # Checar se o arquivo existe no seu computador
    if os.path.exists(nome_arquivo):
        
        # Abrir o arquivo no modo de leitura ('r' de read)
        # Usamos encoding='utf-8' para aceitar acentos (como em "Feijão")
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            
            # Transformar o texto do arquivo em um dicionário
            return json.load(arquivo)
            
    # Se o arquivo NÃO existir, retorna um dicionário vazio
    return {}


def salvar_dados(dados):
    # 'w' significa write (escrita). Se o arquivo não existir, o Python cria.
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        # indent=4 deixa o arquivo bonitinho para humanos lerem
        # ensure_ascii=False permite acentos como em "Feijão"
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)
    print(">> Dados salvos no disco!")


def adicionar_item(estoque):
    # Input´s que pedem ao usuário todas as informações sobre o produto
    nome = input("Nome do mantimento: ").strip().capitalize()
    peso = input("Peso/Volume (ex: 500g): ").strip()
    validade = input("Validade (DD/MM/AAAA): ").strip()
    quantidade = float(input(f"Quantidade de {nome}: "))
    minimo = float(input(f"Mínimo para {nome}: "))

    # Adiciona o item no dicionario com as informações recebidas
    estoque[nome] = {
        "quantidade": quantidade,
        "peso": peso,
        "validade": validade,
        "minimo": minimo
    }

    # Salva as informações receebidas no estoque
    salvar_dados(estoque)
    print(f"\n✅ {nome} salvo com sucesso!")


def editar_item(estoque):

    # Veridica se o estoque está vazio caso esteja retorna para o sub-menu
    if not estoque:
        print("\n[!] O estoque está vazio. Não há nada para editar.")
        return
    
    ver_estoque(estoque) # Mostra a lista para o usuário ver os nomes
    nome = input("\nDigite o nome exato do item que deseja editar: ").strip().capitalize()

    # Verifica se o item existe no estoque e abre o input de edição
    if nome in estoque:
        print(f"\nO que você deseja editar em {nome}?")
        print("[1] Quantidade | [2] Peso | [3] Validade | [4] Mínimo | [5] Tudo")
        sub_op = input("Escolha: ")

        if sub_op == "1":
            estoque[nome]["quantidade"] = float(input(f"Nova quantidade para {nome}: "))
        elif sub_op == "2":
            estoque[nome]["peso"] = input(f"Novo peso para {nome}: ")
        elif sub_op == "3":
            estoque[nome]["validade"] = input(f"Nova validade para {nome}: ")
        elif sub_op == "4":
            estoque[nome]["minimo"] = float(input(f"Novo estoque mínimo para {nome}: "))
        elif sub_op == "5":
            # Aqui chamamos a lógica de adicionar para sobrescrever tudo
            adicionar_item(estoque)
            return # Sai da função para não salvar duas vezes
        
        
        salvar_dados(estoque) # Salva os itens no estoque
        print(f"✨ {nome} atualizado!")
    
    else: # Caso o item não seja encontrado no estoque
        print("❌ Item não encontrado.")


def remover_item(estoque):

    if not estoque: # Verifica se o estoque está vazio se estiver ele retorna para o menu
        print("\n[!] O estoque já está totalmente vazio. Não há nada para remover.")
        return
    
    ver_estoque(estoque) # Exibe a lista de items
    
    print("\n--- REMOVER DO SISTEMA ---")
    print("Dica: Digite 'TUDO' para apagar todo o estoque.")
    
    nome = input("\nQual item deseja remover? ").strip().capitalize()

    # Lógica para remover tudo
    if nome == "Tudo":
        confirmacao = input("⚠️  TEM CERTEZA? Isso apagará tudo! (S/N): ").strip().upper()
        if confirmacao == "S":
            estoque.clear()
            salvar_dados(estoque)
            print("💥 Estoque totalmente resetado!")
        else:
            print("Operação cancelada.")
            
    # Lógica para remover um item específico
    elif nome in estoque:
        del estoque[nome]
        salvar_dados(estoque)
        print(f"🗑️  {nome} foi removido com sucesso.")
        
    else: # Caso o item não seja encontrado no estoque
        print(f"❌ O item '{nome}' não foi encontrado no estoque.")


def ver_estoque(estoque):
    if not estoque:
        print("\n[!] O estoque está vazio.")
        return # Sai da função mais cedo

    print("\n" + "="*70)
    # Definindo cabeçalhos com alinhamento (ex: 15 caracteres para o nome)
    print(f"{'Item':<15} | {'Qtd':<8} | {'Peso':<10} | {'Validade':<12}")
    print("-" * 70)

    for nome, info in estoque.items():
        # :<15 preenche com espaços até completar 15 caracteres à esquerda
        print(f"{nome:<15} | {info['quantidade']:<8} | {info['peso']:<10} | {info['validade']:<12}")
    
    print("="*70)


def gerar_lista_compras(estoque):
    print("\n" + "="*40)
    print("🛒 ITENS QUE PRECISAM DE REPOSIÇÃO")
    print("="*40)
    
    nada_faltando = True
    
    for nome, info in estoque.items():
        # A mágica acontece aqui:
        if info['quantidade'] <= info['minimo']:
            print(f"• {nome:<15} | Atual: {info['quantidade']} | Mínimo: {info['minimo']}")
            nada_faltando = False
            
    if nada_faltando:
        print("Tudo certo por aqui! Sua despensa está abastecida.")
    
    print("="*40)
    input("\nPressione Enter para voltar ao menu...")


def gerenciar_item(estoque):
    while True:
        print("\n--- GERENCIAR MANTIMENTOS ---")
        print("1. Adicionar Novo Item")
        print("2. Editar Item Existente")
        print("3. Voltar")
        
        escolha = input("Escolha: ")
        
        if escolha == "1":
            adicionar_item(estoque)
        elif escolha == "2":
            editar_item(estoque)
        elif escolha == "3":
            break


def menu():
    # Carrega o dicionário do JSON para a memória RAM
    estoque = carregar_dados()
    
    while True:
        print("\n" + "="*30)
        print("   🏠 GESTÃO DE DESPENSA")
        print("="*30)
        print("1. Ver Estoque Completo")
        print("2. Adicionar ou Editar Item")
        print("3. Remover Item do Sistema")
        print("4. Gerar Lista de Compras")
        print("5. Sair do Programa")
        print("="*30)
        
        opcao = input("Escolha uma opção (1-5): ")
        
        if opcao == "1":
            ver_estoque(estoque)
        elif opcao == "2":
            gerenciar_item(estoque)
        elif opcao == "3":
            remover_item(estoque)
        elif opcao == "4":
            gerar_lista_compras(estoque)
        elif opcao == "5":
            print("\nEncerrando o sistema... Até a próxima!")
            break # Única forma de sair do loop 'while True'
        else:
            print("\n⚠️ Opção inválida! Digite um número entre 1 e 5.")


if __name__ == "__main__":
    menu()