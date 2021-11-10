
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


    def fechar(self):
        self.connec.close()
        self.cursor.close()


itens = baseDados('itensBaseDados.db')
