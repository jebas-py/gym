#PROBABILIDADE
def frequencia(lista):
    '''
    frequencia() = extrai a contagem e o percentual individual de cada valor na lista
    :param(lista) = recebe uma lista com valores variáveis (str, int, float)
    resultado = retorna um DataFrame com a quantidade e o percentual de ocorrência individual dos valores; index = 1° coluna
    '''
    # Remove os valores duplicados
    lista_copia = lista.copy()
    lista_copia.sort()
    for i in lista_copia:
        while lista_copia.count(i) >= 2:
            lista_copia.remove(i)
    # Calcula a ocorrência de cada valor dentro da lista
    lista_frequencia = []
    frequencia = 0
    for i in lista_copia:
        frequencia = lista.count(i)
        lista_frequencia.append(frequencia)
    # Calcula o percentual de cada valor na lista
    lista_frequencia_percentual = []
    percentual = 0
    for i in lista_frequencia:
        percentual = (i / sum(lista_frequencia) * 100)
        lista_frequencia_percentual.append(round(percentual, 2))
    # Une os valores da lista com o percentual
    from pandas import DataFrame
    resultado = {'Frequencia': lista_frequencia,
                 'Frequencia(%)': lista_frequencia_percentual}
    frame = DataFrame(resultado, index=lista_copia)
    return frame


def percentual(*sequencia, divisor, colunas, indice, casa_decimal=1, inverter=False):
    '''
    percentual() - calcular o percentual de uma variável em relação a outra com saída em um DataFrame
    :parâm(*sequencia) - parâmetro a ser calculado o percentual / recebe "n" argumentos de uma sequencia de valores exclusivamente
    em lista unidimensional, array unidimensional e Series
    :parâm(divisor) - parâmetro que dividirá o parâmetro sequencia / recebe sequência de valores a serem exclusivamente em 
    lista unidimensional, array unidimensional e Series (deve ter a mesma quantidade de itens que a variável do parâmetro sequencia)
    :parâm(colunas) - recebe sequência de valores a serem exclusivamente em lista unidimensional, array unidimensional e Series 
    contendo as colunas para a saída do DataFrame (deve ter a mesma quantidade de itens que a variável do parâmetro sequencia)
    :parâm(indice) - recebe os índices de saída do DataFrame (deve conter a mesma quantidade de variáveis no parâmetro sequencia)
    :parâm(casa_decimal) - opcional/default = 1 - casas decimais de saída
    :parâm(inverter) - opcional/default = False - inverte a posição entre as linhas e colunas (True ou False)
    '''
    from numpy import array, round
    ar_sequencia = array(sequencia)
    ar_divisor = array(divisor)
    lista_resultado = []
    for item in ar_sequencia:
        resultado = round(item / ar_divisor * 100, decimals=casa_decimal)
        lista_resultado.append(resultado)
    from pandas import DataFrame
    if inverter is False:
        return DataFrame(lista_resultado, columns=colunas, index=indice)
    elif inverter is True:
        return DataFrame(lista_resultado, columns=colunas, index=indice).transpose()
    else:
        return DataFrame(lista_resultado, columns=colunas, index=indice)
    
def percentual_coluna(tabela, decimais=1):
    '''
    percentual_coluna() = calcula o percentual das linhas em relação as respectivas colunas
    :parâm(tabela) = aceita um dataframe em Pandas
    :parâm(decimais) = opcional/default=1; quantidade de casas decimais desejada para o percentual
    '''
    from pandas import DataFrame as df
    from numpy import array, round
    #transforma o dataframe em lista aninhada e depois em um array multidimensional
    lista_temp = []
    for i in range(0, tabela.shape[0]):
        lista_temp.append(list(tabela.iloc[i]))
    transforma_array = array(lista_temp)
    resultado = round((transforma_array / transforma_array[transforma_array.shape[0] - 1]) * 100, decimals=decimais)
    return df(data=resultado, columns=tabela.columns, index=tabela.index)

    
#ESTATÍSTICA_MEDIDAS
def medidas_dispersao(lista):
    '''
    tendencia_central() = calcula um conjunto de medidas de dispersão
    :param(lista) = lista UNIDIMENSIONAL e EXCLUSIVAMENTE de valores numéricos
    retorno = retorna uma Series com Amplitude, Desvio padrão, Coeficiente de variação e Assimetria
     '''
    import statistics as st
    amplitude = max(lista) - min(lista)
    desvio_padrao = round(st.stdev(lista), 2)
    media = sum(lista) / len(lista)
    coeficiente_variacao = round((desvio_padrao / media) * 100, 2)
    desvio_padrao_positivo = media + desvio_padrao
    desvio_padrao_negativo = media - desvio_padrao
    from scipy import stats
    assimetria = round(stats.skew(lista), 2)

    resultado = {'Amplitude': amplitude, 'Desvio Padrão': desvio_padrao, 'Desvio Padrão (+)': desvio_padrao_positivo,
                 'Desvio Padrão (-)': desvio_padrao_negativo, 'Coeficiente de Variação(%)': coeficiente_variacao,
                 'Assimetria': assimetria}
    from pandas import Series
    return Series(resultado)


def medidas_posicao(lista):
    '''
    medidas_posicao() = calcula um conjunto de medidas de posição
    :param(lista) = lista UNIDIMENSIONAL e EXCLUSIVAMENTE de valores numéricos
    retorno = retorna uma Series com Média, Moda (única), Mediana e Quartil
     '''
    import statistics as st
    try:
        moda = st.mode(lista)
    except:
        moda = '-'  # caso retorne mais de um valor, a moda é múltipla (-)
    media = round(st.mean(lista), 2)
    mediana = st.median(lista)
    mediana_menor = st.median_low(lista)  # escolhe o MENOR quando a mediana é um valor médio entre dois números
    mediana_maior = st.median_high(lista)  # escolhe o MAIOR quando a mediana é um valor médio entre dois números
    lista.sort()
    pos1 = len(lista) // 4
    pos2 = (len(lista) // 4) * 2
    pos3 = (len(lista) // 4) * 3
    amplitude_quartil = lista[pos3] - lista[pos1]

    resultado = {'Moda': moda, 'Média': media, 'Mediana': mediana, 'Mediana(menor)': mediana_menor,
                 'Mediana(maior)': mediana_maior, '1° quartil': lista[pos1], '2° quartil': lista[pos2],
                 '3° quartil': lista[pos3], 'Amplitude quartil': amplitude_quartil}

    from pandas import Series
    return Series(resultado)


def descricao(lista):
    '''
    descricao() = apresenta as principais características de lista
    :param(lista) = lista UNIDIMENSIONAL e EXCLUSIVAMENTE de valores numéricos
    retorno = retorna uma Series com Contagem total, contagem distintos, contagem numéricos, Maio, menor, Amplitude, 2° maior e 2° menor
    OBS.: em CONTAGEM NÃO NUMÉRICO, podem haver valores float - corrigir código
    '''
    lista.sort()
    contagem = len(lista)
    # Contagem de distintos (início)
    distintos = lista.copy()
    for i in distintos:
        while distintos.count(i) > 1:
            distintos.remove(i)
    contagem_distintos = len(distintos)
    # Contagem de distintos (fim)
    # Contagem de números, strings e alfanuméricos (início)
    contagem_numero = contagem_nao_numero = 0
    for i in lista:
        x = str(i)
        if x.isnumeric() is True:
            contagem_numero += 1
        else:
            contagem_nao_numero += 1
    # Contagem de números, strings e alfanuméricos (fim)
    maior = max(lista)
    menor = min(lista)
    amplitude = maior - menor
    segundo_maior = lista[len(lista) - 2]  # posição len(lista) fora do range
    segundo_menor = lista[1]
    resultado = {'Contagem total': contagem, 'Contagem distintos': contagem_distintos,
                 'Contagem Numéricos': contagem_numero,
                 'Contagem Não numérico': contagem_nao_numero, 'Maior': maior, 'Menor': menor, 'Amplitude': amplitude,
                 '2° maior': segundo_maior, '2° menor': segundo_menor}
    from pandas import Series
    return Series(resultado)


def outliers(lista, funcao=0, decimais=1):
    '''
    outliers() = segmenta o conjunto de dados em 3: outlier menor (abaixo Desvio Padrão (-)), padrão (entre Desvio Pdrão (-) e (+)) e 
    outlier maior (acima Desvio Padrão (+))
    :param(lista) = lista UNIDIMENSIONAL e EXCLUSIVAMENTE de valores numéricos
    retorno = retorna um DataFrame em pandas Contagem absoluta, Contagem percentual, Média e Mediana
    '''
    #define as variáveis mediante a função escolhida
    if funcao == 'limite': #utiliza como variáveis o cálculo dos limites interquartil
      from pandas import Series
      dados = Series(lista)
      quartil_1 = dados.quantile(.25)
      quartil_3 = dados.quantile(.75)
      intervalo_quartil = quartil_3 - quartil_1
      minimo = quartil_1 - 1.5 * intervalo_quartil
      maximo = quartil_3 + 1.5 * intervalo_quartil
    elif funcao == 'desvio':
      from __init__ import medidas_dispersao
      dados = medidas_dispersao(lista)
      minimo = dados['Desvio Padrão (-)']
      maximo = dados['Desvio Padrão (+)']
    else:
      return print('ERRO: parâmetro funcao não definido')
    #iteração para contar os valores que estão acima, dentro e abaixo do desvio padrão e adicionar os elementos a uma lista específica
    outlier_minimo = outlier_maximo = padrao = 0 #contador
    lista_outlier_minimo = [] 
    lista_outlier_maximo = []
    lista_padrao = []
    for i in lista:
        if i < minimo:
            outlier_minimo += 1
            lista_outlier_minimo.append(i)
        elif i > maximo:
            outlier_maximo +=1
            lista_outlier_maximo.append(i)
        else:
            padrao += 1
            lista_padrao.append(i)
    lista_absoluto = [outlier_minimo, padrao, outlier_maximo] #lista com a quantidade de itens em cada variável
    #cálculo para obter o valor em percentual das quantidades acima, dentro e abaixo do desvio padrão
    outlier_minimo_percentual = round(outlier_minimo / len(lista) * 100, decimais)
    outlier_maximo_percentual = round(outlier_maximo / len(lista) * 100, decimais)
    padrao_percentual = round(padrao / len(lista) * 100, decimais)
    lista_percentual = [outlier_minimo_percentual, padrao_percentual, outlier_maximo_percentual]
    #importar Statistics para extrair os valores das listas com os elementos dentro, fora e abaixo do padrão 
    from statistics import mean, median
    #trantando erro das médias em caso de lista vazia
    try:
      media_outlier_minimo = round(mean(lista_outlier_minimo), decimais)
    except:
      media_outlier_minimo = '-'
    try:
      media_outlier_maximo = round(mean(lista_outlier_maximo), decimais)
    except:
      media_outlier_maximo = '-'    
    try:
      media_padrao = round(mean(lista_padrao), decimais)
    except:
      media_padrao = '-'
    lista_media = [media_outlier_minimo, media_padrao, media_outlier_maximo]
    #trantando erro das medianas em caso de lista vazia
    try:
      mediana_outlier_minimo = round(median(lista_outlier_minimo), decimais)
    except:
      mediana_outlier_minimo = '-'
    try:
      mediana_outlier_maximo = round(median(lista_outlier_maximo), decimais)
    except:
      mediana_outlier_maximo = '-'
    try:
      mediana_padrao = round(median(lista_padrao), decimais)
    except:
      mediana_padrao = '-'
    lista_mediana = [mediana_outlier_minimo, mediana_padrao, mediana_outlier_maximo]
    #importar Pandas para apresentar o resultado em uma DataFrame
    from pandas import DataFrame
    index = ['Outlier menor', 'Padrão', 'Outlier maior']
    resultado = {'Absoluto': lista_absoluto, 'Percentual': lista_percentual, 'Média': lista_media, 'Mediana': lista_mediana}
    frame = DataFrame(resultado, index=index)
    return frame

def outliers_valores(dados):
    '''
    outliers_valores() = retorna o 1° quartil, 3° quartil, Intervalo interquartil, Limite inferior e Limite Superior
    :parâm(dados) = recebe sequência de dados UNIDIMENSIONAL em lista, series ou array
    '''
    from pandas import Series
    transforma_series = Series(dados)
    quartil_1 = transforma_series.quantile(.25)
    quartil_3 = transforma_series.quantile(.75)
    intervalo_quartil = quartil_3 - quartil_1
    limite_inferior = quartil_1 - 1.5 * intervalo_quartil
    limite_superior = quartil_3 + 1.5 * intervalo_quartil
    resultado = Series([quartil_1, quartil_3, intervalo_quartil, limite_inferior, limite_superior],
                       index=['1° quartil', '3° quartil', 'Intervalo interquartil', 'Limite inferior', 'Limite Superior'])
    return resultado


#ESTATÍSTICA VARIAÇÃO
def lista_variacao_ordenada(lista):
    '''
    lista_variacao() = calcula a diferença entre os elementos ordenados de uma variável
    :param(lista) = recebe uma lista UNIDIMENSIONAL e EXCLUSIVAMENTE de valores numérios
    retorna: lista o intervalo entre valores
    '''
    lista_variacao = []
    lista.sort()
    pos1 = 1
    pos2 = 0
    for i in lista:
        while pos1 < len(lista):
            x = lista[pos1] - lista[pos2]
            lista_variacao.append(x)
            pos1 += 1
            pos2 += 1
    return lista_variacao

def variacao(lista):
    '''
    variacao() = calcula a diferença entre os elementos de uma variável
    :param(lista) = recebe uma lista UNIDIMENSIONAL e EXCLUSIVAMENTE de valores numérios
    retorna: lista o intervalo absoluto e percentual entre valores
    '''
    lista_variacao = []
    lista_variacao_percentual = []
    pos1 = 1
    pos2 = 0
    for i in lista:
        while pos1 < len(lista):
            x = lista[pos1] - lista[pos2]
            lista_variacao.append(x)
            y = round((((lista[pos1] / lista[pos2]) - 1) * 100), 2)
            lista_variacao_percentual.append(y)
            pos1 += 1
            pos2 += 1
    from pandas import DataFrame
    resultado = {'Absoluto': lista_variacao, 'Percentual': lista_variacao_percentual}
    return DataFrame(resultado)


def variacao_medidas(lista):
    '''
    variacao() = analisa a variação dos elementos ordenados de uma variável, extraindo algumas medidas de dispersão e posição 
    parâmetro = recebe uma lista UNIDIMENSIONAL e EXCLUSIVAMENTE de valores numérios
    retorna = Média, Mediana, Desvio Padrão, Máximo e Mínimo
    '''
    lista_variacao = []
    lista.sort()
    pos1 = 1
    pos2 = 0
    for i in lista:
        while pos1 < len(lista):
            x = lista[pos1] - lista[pos2]
            lista_variacao.append(x)
            pos1 += 1
            pos2 += 1
    from statistics import mean, median, stdev
    media = mean(lista_variacao)
    mediana = median(lista_variacao)
    desvio_padrao = stdev(lista_variacao)
    maxima = max(lista_variacao)
    minima = min(lista_variacao)
    resultado = {'Variação Média': round(media, 2), 'Variação Mediana': mediana, 'Desvio Padrão': round(desvio_padrao, 2),
                 'Varição Máxima': maxima, 'Variação Mínima': minima}
    from pandas import Series
    return Series(resultado)

def erro(amostra, desvio_padrao, confianca=0.95, media=False, percentual=False):
    '''
    erro: calcula o erro amostral de uma característica da amostra; retorna o valor na escala do parâmatro inserido, exceto se selecionar o 
    retorno em percentual=True 
    :param(amostra) = quantidade de registros ou casos selecionados dentro do universo
    :param(desvio_padrao) = desvio padrão da média dos resultados obtidos da amostra
    :param(confianca) = opcional-default 95% / intervalo de confianca pretendido; valores recomendados de 0.90 a 0.99
    :param(media) = média aritmética amostral, obrigatória quando percentual=True
    :param(percentual) = opcional-default=False / recebe valor booleano e retorna o erro em percentual da média
    '''
    from scipy.stats import norm
    from numpy import sqrt
    z = norm.ppf(0.5 + (confianca / 2))
    erro = z * (desvio_padrao / sqrt(amostra))
    if percentual is False and media is False:
        return erro
    elif percentual is True and media is False:
        print('Falta parâmetro: (inserir a média)')
    elif percentual is True and media is not True:
        erro_percentual = erro / media * 100
        return erro_percentual

#PREVISÃO
def previsao_media(lista, elementos):
    '''previsao() = procura prever os próximos valores da lista, utilizando como base a média de variação apresentada no resultado da 
    função variacao_medidas
    :param(lista) = lista UNIDIMENSIONAL e NUMÉRICA
    :param(elementos) = quantidade de elementos a serem previstos (somente número)
    :return = lista com os valores previstos em float
    '''
    #Importa função para verificar a média da diferença dos valores da variável
    from __init__ import variacao_medidas
    resultado_variacao = variacao_medidas(lista)
    media_previsao = resultado_variacao['Variação Média']
    #Primeiro elemento da lista de previsão
    previsao_inicial = lista[len(lista) - 1] + media_previsao
    lista_previsao = [previsao_inicial]
    #Estrutura de repetição que retorna os valores previstos (tamanho determinado ao chamar a função)
    for i in range(0, elementos - 1):
        previsao_inicial += media_previsao
        lista_previsao.append(previsao_inicial)
    return lista_previsao


def previsao_mediana(lista, elementos):
    '''previsao() = procura prever os próximos valores da lista, utilizando como base a mediana de variação apresentada no resultado 
    da função variacao_medidas
    :param(lista) = lista UNIDIMENSIONAL e NUMÉRICA
    :param(elementos) = quantidade de elementos a serem previstos (somente número)
    :return = lista com os valores previstos em float
    '''
    #Importa função para verificar a mediana da diferença dos valores da variável
    from __init__ import variacao_medidas
    resultado_variacao = variacao_medidas(lista)
    mediana_previsao = resultado_variacao['Variação Mediana']
    #Primeiro elemento da lista de previsão
    previsao_inicial = lista[len(lista) - 1] + mediana_previsao
    lista_previsao = [previsao_inicial]
    #Estrutura de repetição que retorna os valores previstos (tamanho determinado ao chamar a função)
    for i in range(0, elementos - 1):
        previsao_inicial += mediana_previsao
        lista_previsao.append(previsao_inicial)
    return lista_previsao


def previsao_probabilistica(lista, elementos):
    '''
    previsao_probabilistica() = prevê os próximos elementos de uma série de dados se utilizando a probabilidade da variação dos elementos
    :param(lista) = lista UNIDIMENSIONAL e NUMÉRICA
    :param(elementos) = quantidade de elementos a serem previstos (somente número)
    :return = lista com os valores previstos em int    
    '''
    #Importa a biblioteca para extrair a listade variação
    from __init__ import lista_variacao
    frame = lista_variacao(lista)
    #importar a função sample de random para selecionar os valores na lista de acordo com a probabilidade de ocorrer os valores
    from random import sample
    valor_aleatorio =  sample(frame, 1)[0]
    previsao_inicial = lista[len(lista) - 1] + valor_aleatorio
    lista_previsao = [previsao_inicial]
    for i in range(0, elementos - 1):
        previsao_inicial += sample(frame, 1)[0]
        lista_previsao.append(previsao_inicial)
    return lista_previsao