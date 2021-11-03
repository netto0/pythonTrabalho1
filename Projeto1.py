
'''
> 1: Item:
        Receber Item(nome, código, qtd, preço e validade)
        Salvar em arquivo separado
        Função Ler Lista de Arquivos
        Extrair Preços de Planilha
> 2: Interface Gráfica:
'''

import sqlite3
from unidecode import unidecode
import re
from openpyxl import load_workbook

class baseDados:
    def __init__(self, arquivo):
        self.connec = sqlite3.connect(arquivo)
        self.cursor = self.connec.cursor()

    def inserir(self, cod, nome, preco):
        consulta = 'INSERT OR IGNORE INTO itens (cod, nome, preco) VALUES (?, ?, ?)'
        self.cursor.execute(consulta, (cod, nome, preco))
        self.connec.commit()

    def getItens(self):
        wb = load_workbook(filename='tabela de preços 2021.xlsx', data_only=True)
        ws = wb.active
        row_count = int(ws.max_row)
        for c in range(1, row_count + 1):
            numA = "A" + str(c)
            numB = "B" + str(c)
            numC = "C" + str(c)
            cellA = ws[numA].value
            cellB = ws[numB].value
            cellC = ws[numC].value
            item = []
            if isinstance(cellA, int):
                item.append(cellA)
                item.append(cellB)
                item.append(str(cellC).replace('.', ','))
                baseDados.inserir(self,cellA,cellB,cellC)
        for c in range(1, row_count + 1):
            numJ = "J" + str(c)
            numK = "K" + str(c)
            numL = "L" + str(c)
            cellJ = ws[numJ].value
            cellK = ws[numK].value
            cellL = ws[numL].value
            item = []
            if isinstance(cellJ, int):
                item.append(cellJ)
                item.append(cellK)
                item.append(str(cellL).replace('.', ','))
                baseDados.inserir(self,cellJ,cellK,cellL)

    def listar(self):
        self.cursor.execute('SELECT * FROM itens')
        for l in self.cursor.fetchall():
            print(l)

    def inserirComData(self, cod, nome, preco, qtd, val):
        consulta = 'INSERT INTO itens (cod, nome, preco, qtd, val) VALUES (?, ?, ?, ?, ?)'
        self.cursor.execute(consulta, (cod, nome, preco, qtd, val))
        self.connec.commit()

    def editVal(self,cod, qtd, val, op = ('+','-')):
        item = baseDados.getItemfromId(self, cod)
        if baseDados.verificar(self,cod,val) != None:
            quantidade = None
            if op == '+':
                quantidade = int(item[3]) + int(qtd)
            elif op == '-':
                quantidade = int(item[3]) - int(qtd)
            print(baseDados.verificar(self, cod, val))
            print(f'Validade "{val}" já cadastrada, quantidade atualizada para {quantidade}')
            update = 'UPDATE itens SET qtd = ? WHERE cod = ? AND val = ?'
            self.cursor.execute(update, (quantidade, cod, val))
            self.connec.commit()
        else:
            baseDados.inserirComData(self, cod, item[1], item[2], qtd, val)
            print(f'Data {val} inserida para o item "{cod}"')

    def qtdTotal(self,cod):
        item = []
        soma = 0
        consulta = 'SELECT * FROM itens'
        self.cursor.execute(consulta)
        for l in self.cursor.fetchall():
            codigo, nome, preco, qtd, validade = l
            if codigo == cod:
                item.append(l)
        for i in item:
            soma += int(i[3])
        return soma

    def verificar(self,cod,val):
        item = None
        consulta = 'SELECT * FROM itens'
        self.cursor.execute(consulta)
        for l in self.cursor.fetchall():
            codigo, nome, preco, qtd, validade = l
            if codigo == cod and validade == val:
                item = l
        return item

    def getItemfromId(self,cod):
        item = None
        consulta = 'SELECT * FROM itens'
        self.cursor.execute(consulta)
        for l in self.cursor.fetchall():
            codigo, nome, preco, qtd, validade = l
            if codigo == cod:
                item = l
        return item
        # self.connec.commit()


    # def remVal(self,cod,qtd,val):
    #     consulta = 'UPDATE OR IGNORE itens SET qtd=?, val=? WHERE cod=?'
    #     self.cursor.execute(consulta, (qtd, val, cod))
    #     self.connec.commit()


    def fechar(self):
        self.connec.close()
        self.cursor.close()


itens = baseDados('itensBaseDados.db')
# itens.listar()
# baseDados.getItens(itens)
#itens.edtVal(628,122224,33)


# itens.verificar(628,33)
# itens.editVal(628,67,'20/01/22','+')
# print(itens.qtdTotal(628))

# def salvarItem(temp):
#     with open('itens.csv', 'a', newline='') as arquivo:
#         escreve = csv.writer(
#             arquivo,
#             delimiter=',',  # Delimitador (Vírgula no caso)
#             quotechar='"',  # Caractere de citação (No caso deixa os valores entre aspas)
#             quoting=csv.QUOTE_ALL
#         )
#         escreve.writerow([temp[0], temp[1], temp[2], temp[3], temp[4]])
#
#
# def addItem(cod,nome,preco,qtd,validade):
#     temp = []
#     temp.append(cod)
#     temp.append(nome)
#     temp.append(preco)
#     temp.append(qtd)
#     temp.append(validade)
#     salvarItem(temp)
#     temp.clear()
#
#
# def verLista():
#     with open('itens.csv', 'r', newline='') as arquivo:
#         # Necessário a indentação por ser um gerador
#         # csv.reader = lê como listas
#         # csv.DictReader = lê como dicionários
#         #dados = csv.reader(arquivo) #Modo mais comum
#         dados = [x for x in csv.DictReader(arquivo)]  # Método para não esgotar o uso dos dados
#         for dado in dados:
#             print(dado)
#
#
# def to_ascii(ls):
#     for i in range(len(ls)):
#         ls[i] = unidecode(ls[i])
#
#
# def buscaItem(key):
#     #key = unidecode(key)
#
#     with open('itens.csv', 'r', newline='') as arquivo:
#         # Necessário a indentação por ser um gerador
#         # csv.reader = lê como listas
#         # csv.DictReader = lê como dicionários
#         #dados = csv.reader(arquivo) #Modo mais comum
#         dados = [x for x in csv.reader(arquivo)]  # Método para não esgotar o uso dos dados
#         cont = 0
#         results = []
#         for dado in dados:
#             #to_ascii(dado)
#             if re.findall(f'{key}',str(dado), flags=re.I) != []:
#                 results.append(dados[cont])
#             cont += 1
#         return results
#
# print(buscaItem('arroz'))
#
# def vender(cod,qtd,prc,val):
#     pass
#
# def getPreco():
#     pass
#
#


# addItem(1212,'arroz','14,25',32,'24/12/21')
# verLista()


