import json
import re

def validar_telefone(telefone):
    numeros = re.sub(r'\D', '', telefone)  # Remove caracteres não numéricos
    if len(numeros) == 11:
        return f'({numeros[:2]}) {numeros[2:7]}-{numeros[7:]}'
    elif len(numeros) == 10:
        return f'({numeros[:2]}) {numeros[2:6]}-{numeros[6:]}'
    else:
        return telefone  # Retorna como está caso não tenha 10 ou 11 dígitos

def validar_email(email):
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(padrao, email) is not None

def load_contatos():
    try:
        with open('agenda-contatos.json', 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return {}  # Retorna um dicionário vazio

def salvar_contatos(contatos):
    with open('agenda-contatos.json', 'w', encoding='utf-8') as arquivo:
        json.dump(contatos, arquivo, indent=4, ensure_ascii=False)

def add_contato(contatos):
    nome = input('Digite o nome do contato: ').strip()
    if nome in contatos:
        print('\nNome já salvo na agenda')
        return
    
    telefone = input('Digite o número de telefone do contato: ')
    telefone_formatado = validar_telefone(telefone)

    while True:
        email = input('Digite o e-mail do contato: ').strip()
        if validar_email(email):
            break
        else:
            print('\nE-mail inválido, tente novamente.')
    
    contatos[nome] = {
        'telefone': telefone_formatado,
        'email': email
    }
    salvar_contatos(contatos)
    print('\nContato adicionado com sucesso!')

def mod_contato(contatos):
    filtro = input('Digite o nome do contato que deseja modificar: ')
    if filtro not in contatos:
        print('\nContato não encontrado')
        return
    
    print('O que deseja mudar?\n1 - Nome\n2 - E-mail\n3 - Telefone\n4 - Cancelar')
    decisao = input('- ')
    
    if decisao == '1':
        novo_nome = input('Digite o novo nome: ').strip()
        contatos[novo_nome] = contatos.pop(filtro)
    elif decisao == '2':
        while True:
            novo_email = input('Digite o novo e-mail do contato: ').strip()
            if validar_email(novo_email):
                contatos[filtro]['email'] = novo_email
                break
            else:
                print('E-mail inválido, tente novamente.')
    elif decisao == '3':
        novo_telefone = input('Digite o novo telefone do contato: ')
        contatos[filtro]['telefone'] = validar_telefone(novo_telefone)
    elif decisao == '4':
        print('\nVoltando ao menu inicial...\n')
        return
    else:
        print('Opção inválida.')
        return
    
    salvar_contatos(contatos)
    print('\nDados atualizados com sucesso!')

def remover_contato(contatos):
    filtro = input('Digite o nome do contato que deseja remover: ')
    if filtro in contatos:
        del contatos[filtro]
        salvar_contatos(contatos)
        print('\nContato removido da agenda.')
    else:
        print('\nContato não encontrado.')

def listar_contatos(contatos):
    if not contatos:
        print('\nNenhum contato salvo na agenda...')
        return
    
    print('=' * 50)
    print('CONTATOS SALVOS'.center(50))
    print('=' * 50)
    for nome, dados in contatos.items():
        print(f'\nNome: {nome}')
        print(f'Telefone: {dados["telefone"]}')
        print(f'E-mail: {dados["email"]}\n')
        

def menu():
    contatos = load_contatos()
    while True:
        print('=' * 50)
        print('AGENDA DE CONTATOS'.center(50))
        print('=' * 50)
        print('\n1 - Adicionar novo contato')
        print('2 - Editar um contato já existente')
        print('3 - Remover um contato')
        print('4 - Listar contatos salvos')
        print('5 - Sair da agenda')
        
        decisao = input('- ')
        if decisao == '1':
            add_contato(contatos)
        elif decisao == '2':
            mod_contato(contatos)
        elif decisao == '3':
            remover_contato(contatos)
        elif decisao == '4':
            listar_contatos(contatos)
        elif decisao == '5':
            print('Saindo da aplicação')
            break
        else:
            print('Opção inválida, tente novamente.')

menu()
