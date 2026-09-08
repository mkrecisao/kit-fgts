# -*- coding: utf-8 -*-
from fpdf import FPDF
from pathlib import Path

def A(s):
    # Helvetica core fonts: latin-1 only; strip/replace unsupported
    repl = {
        '\u2022': '-', '\u2013': '-', '\u2014': '-', '\u201c': '"', '\u201d': '"',
        '\u2018': "'", '\u2019': "'", '\u2026': '...', '\u00a0': ' ',
    }
    for a,b in repl.items():
        s = s.replace(a,b)
    # common Portuguese via latin-1 is ok (áéíóú etc)
    try:
        s.encode('latin-1')
        return s
    except UnicodeEncodeError:
        return s.encode('latin-1', 'replace').decode('latin-1')

ORANGE = (255, 138, 31)
DARK = (10, 15, 28)
MUTED = (90, 100, 120)
LINE = (220, 225, 235)

class KitPDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_fill_color(*DARK)
        self.rect(0, 0, 210, 12, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 9)
        self.set_xy(12, 3)
        self.cell(100, 6, A('Kit FGTS - Guia completo'))
        self.set_xy(120, 3)
        self.set_font('Helvetica', '', 8)
        self.cell(78, 6, A('Conteudo informativo'), align='R')
        self.ln(14)
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-14)
        self.set_draw_color(*LINE)
        self.line(12, self.get_y(), 198, self.get_y())
        self.set_y(-11)
        self.set_font('Helvetica', '', 8)
        self.set_text_color(*MUTED)
        self.cell(0, 8, A(f'Pagina {self.page_no()} | Nao substitui Caixa, gov.br ou advogado | Kit FGTS'), align='C')

    def h1(self, t):
        self.set_font('Helvetica', 'B', 18)
        self.set_text_color(*DARK)
        self.multi_cell(0, 9, A(t))
        self.ln(2)

    def h2(self, t):
        self.ln(2)
        self.set_fill_color(*ORANGE)
        self.rect(12, self.get_y()+1, 3, 7, 'F')
        self.set_x(18)
        self.set_font('Helvetica', 'B', 13)
        self.set_text_color(*DARK)
        self.cell(0, 9, A(t), new_x='LMARGIN', new_y='NEXT')
        self.ln(1)

    def h3(self, t):
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(*DARK)
        self.cell(0, 7, A(t), new_x='LMARGIN', new_y='NEXT')

    def p(self, t):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(40, 45, 55)
        self.multi_cell(0, 5.2, A(t))
        self.ln(1.5)

    def bullet(self, t):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(40, 45, 55)
        x = self.l_margin
        self.set_x(x)
        self.multi_cell(186, 5.2, A('- ' + t))

    def callout(self, title, lines):
        self.set_fill_color(255, 248, 240)
        self.set_draw_color(*ORANGE)
        start = self.get_y()
        h = 8 + len(lines)*5.5 + 8
        if start + h > 275:
            self.add_page()
            start = self.get_y()
        self.rect(12, start, 186, h, 'DF')
        self.set_xy(16, start + 3)
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(*DARK)
        self.cell(178, 6, A(title), new_x='LMARGIN', new_y='NEXT')
        self.set_font('Helvetica', '', 9)
        self.set_text_color(50, 55, 65)
        for line in lines:
            self.set_x(16)
            self.multi_cell(178, 5, A(line))
        self.set_y(start + h + 3)

    def field_row(self, label):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(40, 45, 55)
        y = self.get_y()
        self.cell(70, 8, A(label))
        self.set_draw_color(180, 185, 195)
        self.line(82, y + 7, 198, y + 7)
        self.ln(10)

    def check(self, t):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(40, 45, 55)
        self.set_x(self.l_margin)
        self.multi_cell(186, 6, A('[ ] ' + t))

    def link_url(self, url, label=None):
        label = label or url
        self.set_font('Helvetica', 'U', 10)
        self.set_text_color(0, 90, 180)
        self.set_x(self.l_margin)
        self.cell(0, 6, A(label), link=url, new_x='LMARGIN', new_y='NEXT')
        self.set_text_color(40, 45, 55)
        self.ln(2)

pdf = KitPDF()
pdf.set_auto_page_break(True, 18)
pdf.set_margins(12, 16, 12)

# COVER
pdf.add_page()
pdf.set_fill_color(*DARK)
pdf.rect(0, 0, 210, 297, 'F')
pdf.set_fill_color(*ORANGE)
pdf.rect(0, 0, 210, 8, 'F')
pdf.set_xy(12, 50)
pdf.set_text_color(*ORANGE)
pdf.set_font('Helvetica', 'B', 12)
pdf.cell(0, 8, A('GUIA DIGITAL + CALCULADORAS'), new_x='LMARGIN', new_y='NEXT')
pdf.set_x(12)
pdf.set_text_color(255, 255, 255)
pdf.set_font('Helvetica', 'B', 28)
pdf.multi_cell(0, 12, A('Kit FGTS Completo'))
pdf.set_x(12)
pdf.set_font('Helvetica', '', 14)
pdf.set_text_color(200, 210, 230)
pdf.multi_cell(0, 8, A('Consulta | Saque | Lucro | Calculadora online | Checklists'))
pdf.ln(8)
pdf.set_x(12)
pdf.set_font('Helvetica', '', 11)
pdf.multi_cell(186, 6, A('Roteiro pratico para entender seu FGTS, estimar valores e nao sacar no escuro.'))
pdf.ln(8)
pdf.set_fill_color(*ORANGE)
pdf.set_text_color(20, 10, 0)
pdf.set_font('Helvetica', 'B', 11)
pdf.set_x(12)
pdf.cell(95, 10, A('  Entrega nivel R$49,90  |  Preco R$9,90  '), fill=True)
pdf.ln(16)
pdf.set_x(12)
pdf.set_text_color(180, 190, 210)
pdf.set_font('Helvetica', '', 10)
pdf.multi_cell(0, 5, A('Conteudo informativo. Nao substitui Caixa, gov.br, app FGTS nem advogado. Regras mudam - confirme sempre na fonte oficial.'))

# SUMARIO
pdf.add_page()
pdf.h1('Sumario')
for i in [
    '1. Como usar este kit',
    '2. O que e o FGTS (visao rapida)',
    '3. Como consultar o saldo (passo a passo)',
    '4. Ler o extrato sem confusao',
    '5. Modalidades de saque (mapa)',
    '6. CALCULADORA ONLINE (link) + papel: rescisao',
    '7. Calculadora em papel: saque-aniversario',
    '8. Lucro / distribuicao do FGTS',
    '9. Calculadora em papel: estimativa de lucro',
    '10. Checklist do dia do saque',
    '11. Erros comuns e golpes',
    '12. Scripts: o que perguntar (RH / Caixa)',
    '13. Glossario rapido',
    '14. Fontes oficiais',
    '15. Folha em branco para suas contas',
]:
    pdf.p(i)

pdf.add_page()
pdf.h1('1. Como usar este kit')
pdf.p('Este material foi feito para voce PREENCHER com seus numeros - nao so ler texto generico.')
pdf.bullet('Leia as secoes 2 a 5 para entender o cenario.')
pdf.bullet('Use a calculadora ONLINE (link abaixo) no celular - resultado na hora.')
pdf.bullet('As secoes 6, 7 e 9 tambem tem planilha em papel se preferir.')
pdf.callout('Calculadora inclusa (link)', [
    'https://mkrecisao.github.io/kit-fgts/calculadora.html',
    'Abra no celular: saque-aniversario, rescisao e lucro. Sem cadastro.',
])
pdf.link_url('https://mkrecisao.github.io/kit-fgts/calculadora.html', 'Abrir calculadora FGTS (toque aqui)')
pdf.bullet('Feche com os checklists antes de sacar ou assinar.')
pdf.bullet('Confirme sempre no app FGTS / Caixa / gov.br.')
pdf.callout('Importante', [
    'Tudo aqui e estimativa educativa. O valor oficial e o do extrato/app.',
    'Multa, modalidades e calendarios podem mudar. Confira a norma vigente.',
])

pdf.h2('2. O que e o FGTS (visao rapida)')
pdf.p('O FGTS e uma poupanca trabalhista: em regra, o empregador deposita mensalmente um percentual sobre a remuneracao na conta vinculada do trabalhador.')
pdf.h3('Para que serve na pratica')
pdf.bullet('Protecao em demissoes (conforme a modalidade e a lei).')
pdf.bullet('Uso em hipoteses previstas (moradia, doencas etc. - veja lista oficial).')
pdf.bullet('Atualizacao e, periodicamente, distribuicao de resultados (lucro).')
pdf.h3('O que este kit NAO faz')
pdf.bullet('Nao acessa sua conta Caixa.')
pdf.bullet('Nao garante direito a saque.')
pdf.bullet('Nao substitui analise do seu contrato/caso.')

pdf.add_page()
pdf.h1('3. Como consultar o saldo (passo a passo)')
pdf.h3('Caminhos oficiais')
pdf.bullet('App FGTS (smartphone)')
pdf.bullet('Internet Banking Caixa (se disponivel)')
pdf.bullet('Canais indicados pela Caixa / gov.br')
pdf.h3('Roteiro')
pdf.p('1) Abra o canal oficial e faca login.')
pdf.p('2) Localize Saldo / Extrato / contas vinculadas.')
pdf.p('3) Anote: saldo total, contas por empregador, ultima atualizacao.')
pdf.p('4) Tire print ou exporte o extrato para as calculadoras.')
pdf.callout('Organizacao', [
    'Separe: (A) saldo total  (B) conta do emprego atual  (C) contas antigas.',
    'Isso evita misturar valores no saque-aniversario ou na rescisao.',
])
pdf.h3('Ficha de consulta (preencha)')
for lab in ['Data da consulta:', 'Canal usado (app/site):', 'Saldo total (R$):', 'Conta emprego atual (R$):', 'Outras contas (R$):', 'Ultima movimentacao:']:
    pdf.field_row(lab)

pdf.add_page()
pdf.h1('4. Ler o extrato sem confusao')
pdf.p('No extrato costumam aparecer depositos mensais, atualizacao e, quando houver, creditos de distribuicao de resultados.')
pdf.h3('Perguntas ao olhar o extrato')
pdf.bullet('Os depositos do emprego atual estao em dia?')
pdf.bullet('Ha contas antigas com saldo?')
pdf.bullet('Existe credito recente de distribuicao/resultado?')
pdf.bullet('Estou no saque-rescisao ou saque-aniversario?')
pdf.h3('Tabela de anotacoes')
pdf.set_font('Helvetica', 'B', 9)
pdf.set_fill_color(240, 242, 248)
pdf.cell(50, 8, A('Item'), border=1, fill=True)
pdf.cell(45, 8, A('Valor (R$)'), border=1, fill=True)
pdf.cell(45, 8, A('Data'), border=1, fill=True)
pdf.cell(46, 8, A('Obs.'), border=1, fill=True, new_x='LMARGIN', new_y='NEXT')
pdf.set_font('Helvetica', '', 9)
for label in ['Deposito mes', 'Deposito mes', 'Atualizacao', 'Lucro/distr.', 'Saque', 'Outro']:
    pdf.cell(50, 8, A(label), border=1)
    pdf.cell(45, 8, '', border=1)
    pdf.cell(45, 8, '', border=1)
    pdf.cell(46, 8, '', border=1, new_x='LMARGIN', new_y='NEXT')
pdf.ln(3)
pdf.p('Se faltar deposito, anote o mes e leve ao RH (script na secao 12).')

pdf.add_page()
pdf.h1('5. Modalidades de saque (mapa)')
pdf.p('Mapa educativo das hipoteses mais buscadas. A lista oficial completa esta na Caixa.')
pdf.h3('A) Demissao sem justa causa (cenario tipico)')
pdf.bullet('Pode haver saque do saldo, conforme regras vigentes.')
pdf.bullet('Em muitos casos ha multa do empregador (historicamente ligada a 40% - confirme o percentual oficial do seu caso).')
pdf.bullet('Documentos: papel do acerto/TRCT, documentos pessoais, chave de saque quando exigida.')
pdf.h3('B) Pedido de demissao')
pdf.bullet('Em regra NAO se saca o FGTS pela demissao pedida (salvo hipoteses legais).')
pdf.bullet('O saldo continua na conta vinculada.')
pdf.h3('C) Saque-aniversario')
pdf.bullet('Parte do saldo no mes do aniversario, segundo faixa/aliquota oficial.')
pdf.bullet('Atencao: a adesao muda regras em caso de demissao - leia o efeito atual na Caixa.')
pdf.h3('D) Outras hipoteses')
pdf.bullet('Doencas graves, moradia, aposentadoria, calamidade etc. - checar lista oficial.')
pdf.callout('Antes de aderir ao saque-aniversario', [
    'Simule a parcela (secao 7).',
    'Leia o efeito na demissao sem justa causa no texto oficial.',
    'Nao decida so por post de rede social.',
])

pdf.add_page()
pdf.h1('6. Calculadora ONLINE + rescisao (papel)')
pdf.callout('Abra a calculadora no celular', [
    'https://mkrecisao.github.io/kit-fgts/calculadora.html',
    'Tres abas: aniversario | rescisao | lucro. Sem cadastro, sem enviar dados.',
])
pdf.link_url('https://mkrecisao.github.io/kit-fgts/calculadora.html', 'Abrir calculadora FGTS (toque aqui)')
pdf.p('Abaixo: planilha em papel para estimar o acerto. O oficial e o extrato + documentos do empregador.')
pdf.h3('Dados de entrada')
for lab in ['Saldo FGTS depositado (emprego) R$:', 'Tipo de saida (sem justa / pedido / acordo):', 'Esta no saque-aniversario? (S/N):', 'Data da rescisao:']:
    pdf.field_row(lab)
pdf.h3('Conta auxiliar (sem justa causa - educativa)')
pdf.p('1) Saldo FGTS da conta do emprego: R$ __________')
pdf.p('2) Multa estimada (ex.: 40% x item 1, SE aplicavel):')
pdf.p('    0,40 x (1) = R$ __________')
pdf.p('3) Soma estimada FGTS no acerto: (1)+(2) = R$ __________')
pdf.callout('Atencao', [
    'Acordo (art. 484-A) e pedido de demissao mudam multa e saque.',
    'No saque-aniversario a regra na demissao pode ser diferente.',
    'Salario, ferias, 13o e aviso NAO entram nesta conta de FGTS.',
])
pdf.h3('Resultado')
for lab in ['Estimativa FGTS + multa:', 'Valor no extrato/documentos:', 'Diferenca / duvida para o RH:']:
    pdf.field_row(lab)

pdf.add_page()
pdf.h1('7. Calculadora: saque-aniversario (papel)')
pdf.p('Automatico no celular: https://mkrecisao.github.io/kit-fgts/calculadora.html')
pdf.p('Usa faixas de aliquota + parcela adicional da tabela OFICIAL da Caixa. A tabela oficial prevalece.')
pdf.h3('Passo 1 - Seu saldo')
for lab in ['Saldo total disponivel (R$):', 'Mes de nascimento:', 'Janela de saque (datas oficiais):']:
    pdf.field_row(lab)
pdf.h3('Passo 2 - Faixa (tabela oficial)')
for lab in ['Aliquota (%) da faixa:', 'Parcela adicional (R$):']:
    pdf.field_row(lab)
pdf.h3('Passo 3 - Conta')
pdf.p('Estimativa = (Saldo x Aliquota) + Parcela adicional')
pdf.p('Exemplo FICTICIO: saldo 10.000 | aliquota 20% | adicional 500 => 2.000 + 500 = 2.500')
pdf.p('Sua conta:')
pdf.p('(Saldo) R$ ______ x (aliquota) ______ % = R$ ______')
pdf.p('+ adicional R$ ______ = ESTIMATIVA R$ ______')
pdf.callout('Checklist saque-aniversario', [
    '[ ] Confirmei a tabela oficial do ano',
    '[ ] Confirmei a janela do meu mes',
    '[ ] Entendi o efeito na demissao',
    '[ ] Nao usei so calculadora de blog',
])

pdf.add_page()
pdf.h1('8. Lucro / distribuicao do FGTS')
pdf.p('Periodicamente, resultados do FGTS podem ser distribuidos conforme regras vigentes. O credito, quando houver, aparece no extrato.')
pdf.h3('O que pesquisar nas fontes oficiais')
pdf.bullet('Quem tem direito naquele ciclo')
pdf.bullet('Data prevista de credito')
pdf.bullet('Se o valor e sacavel na hora ou so rende no saldo')
pdf.bullet('Como consultar no app')
pdf.h3('Ficha lucro')
for lab in ['Ano/ciclo:', 'Saldo-base (R$):', 'Vi credito no extrato? (S/N):', 'Valor creditado (R$):', 'Data do credito:']:
    pdf.field_row(lab)

pdf.h2('9. Calculadora: estimativa de lucro')
pdf.p('Automatico: https://mkrecisao.github.io/kit-fgts/calculadora.html')
pdf.p('Sem percentual oficial do ciclo, qualquer conta e chute. Use:')
pdf.p('Estimativa = Saldo x (% oficial do ciclo, SE publicado)')
for lab in ['Saldo (R$):', '% oficial (se houver):', 'Estimativa (R$):', 'Valor real no extrato:']:
    pdf.field_row(lab)
pdf.callout('Regra de ouro', [
    'Nao tome decisao com percentual de influencer.',
    'Espere o extrato oficial.',
])

pdf.add_page()
pdf.h1('10. Checklist do dia do saque')
pdf.h3('Documentos / acesso')
for t in ['App FGTS atualizado / senha ok', 'Documento com foto', 'PIS/NIS se pedido', 'Chave de saque / docs do empregador (se demissao)', 'Conta bancaria liberada para credito']:
    pdf.check(t)
pdf.h3('Conferencia')
for t in ['Extrato baixado/printado', 'Modalidade correta (rescisao x aniversario x outra)', 'Valores batem com a estimativa (ou anotei a diferenca)', 'Nao cliquei em link suspeito de liberar FGTS']:
    pdf.check(t)
pdf.h3('Depois do saque')
for t in ['Confirmei o credito no banco', 'Guardei comprovantes', 'Se erro, abri chamado no canal oficial']:
    pdf.check(t)

pdf.h2('11. Erros comuns e golpes')
pdf.bullet('Achar que pedido de demissao libera FGTS igual demissao sem justa causa.')
pdf.bullet('Aderir ao saque-aniversario sem ler o efeito na demissao.')
pdf.bullet('Usar calculadora nao oficial como verdade absoluta.')
pdf.bullet('Cair em golpe de taxinha para liberar FGTS.')
pdf.bullet('Nao conferir depositos atrasados do empregador.')
pdf.callout('Sinais de golpe', [
    'Pedem senha do app / token / codigo SMS',
    'Prometem liberacao mediante PIX antecipado',
    'Link fora de dominio oficial Caixa/gov.br',
])

pdf.add_page()
pdf.h1('12. Scripts: o que perguntar')
pdf.h3('Para o RH')
pdf.p('"Ola, pode confirmar se os depositos de FGTS do periodo estao em dia e a data dos documentos/chave do acerto?"')
pdf.p('"No extrato nao aparece o deposito do mes X - podem verificar, por favor?"')
pdf.h3('Para Caixa / app')
pdf.p('"Quero confirmar se estou no saque-rescisao ou saque-aniversario e qual valor esta disponivel hoje."')
pdf.p('"Houve credito de distribuicao de resultados neste ciclo? Em qual data?"')

pdf.h2('13. Glossario rapido')
pdf.p('Conta vinculada: conta do trabalhador no FGTS.')
pdf.p('Deposito mensal: valor do empregador sobre a remuneracao.')
pdf.p('Saque-rescisao: modalidade tipica ligada ao termino do contrato (regras oficiais).')
pdf.p('Saque-aniversario: saque parcial anual no mes de nascimento.')
pdf.p('Distribuicao de resultados (lucro): credito eventual de resultados do fundo.')
pdf.p('Papel do acerto / TRCT: documentos da rescisao.')
pdf.p('Chave de saque: dado/documento que pode ser exigido para sacar.')

pdf.h2('14. Fontes oficiais')
pdf.bullet('App FGTS / canais Caixa Economica Federal')
pdf.bullet('Portal gov.br (busca FGTS)')
pdf.bullet('Comunicados do Conselho Curador do FGTS')
pdf.bullet('Documentos do RH no desligamento')

pdf.add_page()
pdf.h1('15. Folha em branco para suas contas')
pdf.p('Use esta pagina livre para anotar simulacoes extras.')
for i in range(14):
    y = pdf.get_y()
    pdf.set_draw_color(200, 205, 215)
    pdf.line(12, y + 8, 198, y + 8)
    pdf.ln(12)

pdf.ln(4)
pdf.callout('Pronto', [
    'Voce pagou R$9,90. O kit foi montado com densidade de um guia bem mais caro.',
    'Mapa + extrato + 3 calculadoras + checklists + scripts + anti-golpe.',
    'Preencha, valide no oficial e boa consulta.',
])

out = Path('/workspace/kit-fgts/kit-fgts.pdf')
pdf.output(str(out))
print('OK pages=', pdf.page_no(), 'bytes=', out.stat().st_size)
