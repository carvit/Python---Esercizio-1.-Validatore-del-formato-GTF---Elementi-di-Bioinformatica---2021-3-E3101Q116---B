import re

def numerico(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def stampa(n_record, codice_errore = '', valore1 = '', valore2 = ''):
    if codice_errore == 'transcript_id':
        testo_errore = "Errore di tipo transcript_id - Valore transcript_id Inaspettato: " + valore1 + "\n"

    if codice_errore == 'gene_id':
        testo_errore = "Errore di tipo gene_id - Valore gene_id Inaspettato: " + valore1 + "\n"

    if codice_errore == 'strand':
        testo_errore = "Errore di tipo strand - Valore strand Inaspetatto: " + valore1 + "\n"

    if codice_errore == 'frame':
        testo_errore = "Errore di tipo frame - Valore frame Inaspettato: " + valore1 + "\n"

    if codice_errore == 'feature':
        testo_errore = "Errore di tipo feature - Valore feature Inaspettato: " + valore1 + "\n"

    if codice_errore == 'score':
        testo_errore = "Errore di tipo score - Valore score Inaspettato: " + valore1 + "\n"

    if codice_errore == 'gene_value':
        testo_errore = "Errore di tipo gene_value - Campo gene_value Vuoto\n"

    if codice_errore == 'transcript_value':
        testo_errore = "Errore di tipo transcript_value - Campo transcript_value Vuoto\n"

    if codice_errore == 'sorgente':
        testo_errore = "Errore di tipo sorgente - Identificativo sorgente Inaspettato: " + valore1 + "\n"

    if codice_errore == 'software':
        testo_errore = "Errore di tipo software - Nome software Inaspettato: " + valore1 + "\n"

    if codice_errore == 'index':
        testo_errore = "Errore di tipo index - Valori inizio o fine feature Inaspettati: " +         valore1 + ' ' + valore2   + "\n"

    if codice_errore == 'lunghezza':
        testo_errore = "Errore di tipo lunghezza - Lunghezza start/stop codon non Corretta: " + str(int(valore1) -  int(valore2)) + "\n"

    print("Record numero " + str(n_record) + ". " + testo_errore)

def controllo(attributo):
    att      = re.search('^(\w+)\s\"(\S*)\";\s(\w+)\s\"(\S*)\";(\s(\w+)\s\"(\S*)\";)*(\s+#+.*)*$', attributo)
    t_id     = att.group(1)
    t_valore = att.group(2)
    g_id     = att.group(3)
    g_valore = att.group(4)
    if t_id == "transcript_id":
        if g_id == "gene_id":
            if t_valore != '':
               if g_valore == '':
                        stampa(n_record, 'gene_value')

            else:
               stampa(n_record, 'transcript_value')

        else:
            stampa(n_record, 'gene_id', g_id)

    else:
        stampa(n_record, 'transcript_id', t_id)

with open(input("Nome File (completo di path): "),'r') as gtf_input:
    gtf_input_righe = gtf_input.readlines()

n_record = 0
print("\nValidatore GTF\n")
inizio = True

for row in gtf_input_righe:
    n_record = n_record + 1
    campo = row.rstrip().split('\t')
    if inizio:
        sorgente = campo[0]
        software = campo[1]
        print('Sorgente: ' + sorgente + '\n')
        print('Software: ' + software + '\n')
        print("ELENCO RIGHE NON VALIDE - INIZIO\n")
        inizio = False

    if numerico(campo[3]) and numerico(campo[4]) and ( int(campo[3]) < int(campo[4])):
        if campo[5] == '.' or numerico(campo[5]):
            if campo[0] == sorgente:
                if campo[1] == software:
                    if campo[6] == "-" or campo[6] == "+":
                        if campo[2] == "exon":
                            if campo[7] == '.':
                                controllo(campo[8])

                            else:
                                stampa(n_record, 'frame', campo[7])

                        elif campo[2] == "CDS":
                            if int(campo[7])>=0 and int(campo[7])<= 2:
                                controllo(campo[8])

                            else:
                                stampa(n_record, 'frame', campo[7])

                        elif (campo[2] == 'start_codon' or campo[2] == 'stop_codon'):
                            if (int(campo[4]) - int(campo[3])) <= 2:
                                if int(campo[7]) >= 0 and int(campo[7]) <= 2:
                                    controllo(campo[8])

                                else:
                                    stampa(n_record, 'frame', campo[7])

                            else:
                                stampa(n_record, 'lunghezza', campo[4], campo[3])

                        elif (campo[2] == '5UTR' or campo[2] == '3UTR'):
                            if campo[7] == '.':
                                controllo(campo[8])

                            else:
                                stampa(n_record, 'frame', campo[7])

                        else:
                            stampa(n_record, 'feature', campo[2])

                    else:
                        stampa(n_record, 'strand', campo[6])

                else:
                    stampa(n_record, 'software', campo[1])

            else:
                stampa(n_record, 'sorgente', campo[0])

        else:
            stampa(n_record, 'score', campo[5])

    else:
        stampa(n_record, 'index', campo[3], campo[4])

print("ELENCO RIGHE NON VALIDE - FINE")