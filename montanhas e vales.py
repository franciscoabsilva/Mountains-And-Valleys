
def eh_territorio(arg):
    '''
    eh_territorio: universal → booleano

    Esta função recebe um argumento de qualquer tipo e devolve True se o seu
    argumento corresponde a um território e False caso contrário.
    '''

    # Verifica que o tuplo do território está correto
    if not isinstance(arg, tuple) or not 1 <= len(arg) <= 26:
        return False
    
    # Verifica que a primeira coluna está correta
    if not isinstance(arg[0], tuple) or not 1 <= len(arg[0]) <= 99: 
        return False
    
    # Verifica que todas as outras colunas e os seus valores estão corretos
    for caminho_vertical in arg:
        if not isinstance(caminho_vertical, tuple) or not len(caminho_vertical) == len(arg[0]):
            return False
        for valor_intersecao in caminho_vertical:
            if not valor_intersecao in (0,1) or not isinstance(valor_intersecao, int) or isinstance(valor_intersecao, bool):
                return False
    
    return True

def obtem_ultima_intersecao(t):
    '''
    obtem_ultima_intersecao: territorio → intersecao

    Esta função recebe um território e devolve a intersecao do extremo superior direito do território.
    '''

    return (chr(len(t)+64),len(t[0])) #Encontra a letra e o número da ultima interseção

def eh_intersecao(arg):
    '''
    eh_intersecao: universal → booleano

    Esta função recebe um argumento de qualquer tipo e devolve True
    se o seu argumento corresponde a uma interseção e False caso contrário.
    '''

    # Verifica que o formato do argumento está correto
    if not isinstance(arg, tuple) or not len(arg) == 2:
        return False
    
    # Verifica que a letra existiria em algum território
    if not isinstance(arg[0],str) or not len(arg[0]) == 1 or not arg[0] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        return False
    
    # Verifica que o número existiria em algum território
    if not isinstance(arg[1],int) or isinstance(arg[1],bool) or not arg[1] in range(1,100):
        return False
    
    return True

def eh_intersecao_valida(t, i):
    '''
    eh_intersecao_valida: territorio x intersecao → booleano

    Esta função recebe um território e uma interseção, e devolve True se a
    interseção corresponde a uma interseção do território, e False caso contrário.
    '''

    # Verifica se a letra pertence ao território
    if not ord(i[0])-64 in range(1, len(t)+1): 
        return False
    
    # Verifica se o número pertence ao território
    for caminho_vertical in t:
        if not i[1] in range(1, len(caminho_vertical)+1):
            return False
    
    return True

def eh_intersecao_livre(t, i):
    '''
    eh_intersecao_livre: territorio x intersecao → booleano

    Esta função recebe um território e uma interseção do território, e devolve
    True se a interseção corresponde a uma interseção livre (não ocupada por montanhas)
    dentro do território e False caso contrário.    
    '''

    valor_da_intersecao = t[ord(i[0])-65][i[1]-1]

    return valor_da_intersecao == 0

def obtem_intersecoes_adjacentes(t, i):
    '''
    obtem_intersecoes_adjacentes: territorio x intersecao → tuplo
    
    Esta função recebe um território e uma interseção do território, e
    devolve o tuplo formado pelas interseções válidas adjacentes da interseção
    em ordem de leitura de um território.
    '''

    intersecoes_adjacentes = ()

    posicoes_adjacentes = (
                (i[0] , i[1]-1), #posição abaixo
                (chr(ord(i[0])-1), i[1]), #posição à esquerda 
                (chr(ord(i[0])+1), i[1]), #posição à direita
                (i[0] , i[1]+1) #posição acima
                )
    
    for intersecao in posicoes_adjacentes:
        if eh_intersecao_valida(t, intersecao) == True:
            intersecoes_adjacentes += (intersecao),

    return intersecoes_adjacentes

def ordena_intersecoes(t):
    '''
    ordena_intersecoes: tuplo → tuplo
    
    Esta função recebe um tuplo de interseções (potencialmente vazio) e devolve um tuplo
    contendo as mesmas interseções ordenadas de acordo com a ordem de leitura do território.
    '''
    return tuple(sorted(t, key=lambda ordena_tuplo: (ordena_tuplo[1], ordena_tuplo[0])))

def territorio_para_str(t):
    '''
    territorio_para_str: territorio → cad. carateres

    Esta função recebe um território e devolve a cadeia de caracteres que o 
    representa de uma forma "visível" para os nossos olhos.
    '''

    if eh_territorio(t) == False:
        raise ValueError("territorio_para_str: argumento invalido")

    string_final = ""

    # Cria a primeira e a ultíma linha que serão as letras das colunas
    colunas = "   "
    for i in range(len(t)):
        if i == len(t)-1:
            colunas += str(chr(65+i))
        else:
            colunas += str(chr(65+i)) + " " 

    string_final += colunas +"\n"
    
    # Para cada linha (a contar de cima para baixo) cria uma string que representa a linha
    for linha in range(len(t[0])-1,-1,-1):
        if linha >= 9:
            str_linha = str(linha+1)
        else:
            str_linha = " "+str(linha+1)
       
        for coluna in t:
            if coluna[linha] == 0:
                str_linha += " ."
            else:
                str_linha += " X"
        
        if linha >= 9:
            str_linha += " "+str(linha+1)+"\n"
        else:
            str_linha += "  "+str(linha+1)+"\n"
        
        string_final += str_linha
    
    string_final += colunas

    return string_final

def obtem_cadeia(t, i):
    '''
    obtem_cadeia: territorio x intersecao → tuplo

    Esta função recebe um território e uma interseção do território (ocupada por uma
    montanha ou livre), e devolve o tuplo formado por todas as interseções que estão conetadas
    a essa interseção ordenadas (incluida si própria) de acordo com a ordem de leitura de um território.
    '''

    def intercesoes_iguais(t,i,tup):
        '''
        intercesoes_iguais: territorio x intersecao x tuplo de interseções → tuplo

        Esta função recursiva encontra as interseções adjacentes com o mesmo valor da interseção recebida.
        Depois as adjacentes com o mesmo valor dessas interseções e assim successivamente até que todas as
        interseçoes da cadeia estejam contabilizadas. Ela devolve um tuplo formado por todas essas interseções.
        '''

        for adjacente in obtem_intersecoes_adjacentes(t,i):
            if eh_intersecao_livre(t, adjacente):
                valor_intersecao_adjacente = 0
            else:
                valor_intersecao_adjacente = 1        
            if valor_intersecao_adjacente == valor_intersecao_base and not adjacente in tup:
                tup+=(adjacente),
                tup = intercesoes_iguais(t,adjacente,tup)

        return tup
    
    if not eh_territorio(t) or not eh_intersecao(i) or not eh_intersecao_valida(t, i):
        raise ValueError('obtem_cadeia: argumentos invalidos')
    
    tup=(i),

    if eh_intersecao_livre(t, i):
        valor_intersecao_base = 0
    else:
        valor_intersecao_base = 1

    return ordena_intersecoes(intercesoes_iguais(t,i,tup))

def obtem_vale(t, i):
    '''
    obtem_vale: territorio X intersecao → tuplo

    Esta função recebe um território e uma interseção do território ocupada por uma
    montanha, e devolve o tuplo (potencialmente vazio) formado por todas as interseções que formam parte do vale
    da montanha da interseção fornecida como argumento ordenadas de acordo à ordem de leitura de um território.
    '''

    if not eh_territorio(t) or not eh_intersecao(i) or not eh_intersecao_valida(t, i) or eh_intersecao_livre(t, i):
        raise ValueError('obtem_vale: argumentos invalidos')
    
    vales = ()

    for montanha in obtem_cadeia(t, i):
        for intersecao_adjacente in obtem_intersecoes_adjacentes(t, montanha):
            if eh_intersecao_livre(t, intersecao_adjacente) and intersecao_adjacente not in vales:
                vales += (intersecao_adjacente),

    return ordena_intersecoes(vales)

def verifica_conexao(t,i1,i2):
    '''
    verifica_conexao: territorio x intersecao x intersecao → booleano

    Esta função recebe um território e duas interseções do território e devolve
    True se as duas interseções estão conetadas e False caso contrário.
    '''

    if not eh_territorio(t) or not eh_intersecao(i1) or not eh_intersecao(i2) or not eh_intersecao_valida(t, i1) or not eh_intersecao_valida(t, i2):
        raise ValueError('verifica_conexao: argumentos invalidos')
    
    return i2 in obtem_cadeia(t, i1)

def calcula_numero_montanhas(t):
    '''
    calcula_numero_montanhas: territorio → int
    
    Esta função recebe um território e devolve o número de interseções
    ocupadas por montanhas no território.
    '''

    if not eh_territorio(t):
        raise ValueError('calcula_numero_montanhas: argumento invalido')
    
    montanhas = 0

    for caminho_vertical in t:
        for valor_intersecao in caminho_vertical:
            if valor_intersecao == 1:
                montanhas += 1

    return montanhas

def calcula_numero_cadeias_montanhas(t):
    '''
    calcula_numero_cadeias_montanhas: territorio → int
    
    Esta função recebe um território e devolve o número de cadeias
    de montanhas contidas no território.
    '''

    if not eh_territorio(t):
        raise ValueError('calcula_numero_cadeias_montanhas: argumento invalido')

    intersecoes_contabilizadas = () # Este tuplo permitirá que a função não revisite interseções
    numero_cadeias = 0

    for caminho_vertical in range(len(t)):
        for caminho_horizontal in range(len(t[caminho_vertical])):
            valor_intersecao = t[caminho_vertical][caminho_horizontal]
            intersecao = (chr(caminho_vertical+65), caminho_horizontal+1)
            if intersecao not in intersecoes_contabilizadas:
                if valor_intersecao == 1:
                    cadeia = obtem_cadeia(t, intersecao)
                    for intersecao_da_cadeia in cadeia:
                        intersecoes_contabilizadas += (intersecao_da_cadeia),
                    numero_cadeias += 1

    return numero_cadeias

def calcula_tamanho_vales(t):
    '''
    calcula_tamanho_vales: territorio → int

    Esta função recebe um território e devolve o número total de interseções
    diferentes que formam todos os vales do território.
    '''

    if not eh_territorio(t):
        raise ValueError('calcula_tamanho_vales: argumento invalido')
    
    lista_de_vales = ()

    for caminho_vertical in range(len(t)):
        for caminho_horizontal in range(len(t[caminho_vertical])):
                intersecao = (chr(caminho_vertical+65), caminho_horizontal+1) 
                if not eh_intersecao_livre(t, intersecao):
                    for vale in obtem_vale(t, intersecao):
                        if vale not in lista_de_vales:
                            lista_de_vales += (vale),

    return len(lista_de_vales)