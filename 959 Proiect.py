class Stoc:
    """
    This class is used for a warehouse stock.

     The required parameters when creating an object are set in the "__init__" function as following:

        :param str denp: Name of the product
        :param str categ: Category of the product
        :param str um: Unit of measurement. The default value is set to "Buc".
        :param int sold: Quantity of the product. The default value is set to 0.
        :param int lim_min: This parameter is used to set a quantity limit for the product.

        When creating a new object, it captures user input as it fallows:

        expeditor: Email address from which the message will be sent;
        parola: Email address's password
        destinatar: Email address to whom the message will be sent;


        It prints a confirmation message.
    """

    from datetime import datetime
    lista_produse = []
    dictionar_categorii = {}

    def __init__(self, denp, categ, um='Buc', sold=0, lim_min=0):
        self.expeditor = input("Intrduceti adresa de email de pe care se vor transmite mesaje: \n")
        self.parola = input("Intrduceti parola pentru adresa de email: \n")
        self.destinatar = input("Intrduceti adresa de email catre care se vor transmite mesaje: \n")
        self.lim_min = lim_min
        self.denp = denp
        self.categ = categ
        self.um = um
        self.sold = sold
        self.miscari = {}
        self.lista_produse = Stoc.lista_produse
        self.dictionar_categorii = Stoc.dictionar_categorii
        self.lista_produse.append(self.denp)
        if self.categ in self.dictionar_categorii.keys():
            self.dictionar_categorii[self.categ] += [self.denp]
        else:
            self.dictionar_categorii[self.categ] = [self.denp]
        print("Obiectul a fost creat.")

    def intrari(self, cant, pret_intrare=0, data=str(datetime.now().strftime('%Y%m%d'))):
        """
        This method is used to create a new stock entry for the object.

        :param int cant: Quantity of the exit
        :param int pret_intrare: Entry price. The default value is set to 0.
        :param str data: Must be a string in the format "%Y%m%d".
The default value is set using the datetime module that must be imported beforehand.


        It prints a confirmation message.
        """
        self.pret_intrare = int(pret_intrare)
        self.cant = cant
        self.date = data
        if self.miscari.keys():
            cheie = max(self.miscari.keys()) + 1
        else:
            cheie = 1
        self.miscari[cheie] = (self.date, self.cant, 0, self.pret_intrare)
        self.sold += self.cant
        pret_stoc = 0
        cant_prod = 0
        for intrare in self.miscari:
            pret_stoc += self.miscari[intrare][3] * self.miscari[intrare][1]
            cant_prod += self.miscari[intrare][1]
        self.pret_iesire = float(f"{pret_stoc / cant_prod :.2f}")
        print("Intrarea a fost creata.")

    def iesiri(self, cant, data=str(datetime.now().strftime('%Y%m%d'))):
        """
        This method is used to create a new stock exit for the object.

        :param int cant: Quantity of the exit
        :param str data: Must be a string in the format "%Y%m%d".
The default value is set using the datetime module that must be imported beforehand.

        It prints a confirmation message.
        """
        self.cant = cant
        self.data = data
        if self.miscari.keys():
            cheie = max(self.miscari.keys()) + 1
        else:
            cheie = 1
        self.miscari[cheie] = (self.data, 0, self.cant, self.pret_iesire)
        self.sold -= self.cant
        print("Iesirea a fost creata")
        if self.sold < self.lim_min:
            print("Limita minima a fost depasita.\n\
Se transmite un email de avertizare catre {}".format(self.destinatar))
            self.trimite_email_avertizare()

    def fisap(self):
        """
        This method is used to create and print the object's product sheet.

        Returns:
        corp
        """
        corp = '*-* ' * 10 + "\nFisa produsului {0} [{1}]\n".format(self.denp, self.um) + \
               '-' * 50 + '\n Nrc   Data   Intrare   Iesire   Pret intrare\n' + '-' * 50

        for cheie in self.miscari:
            corp += "\n" + str(cheie).rjust(3) + \
                    str(self.miscari[cheie][0]).rjust(10) + \
                    str(self.miscari[cheie][1]).rjust(8) + \
                    str(self.miscari[cheie][2]).rjust(8) + \
                    str(self.miscari[cheie][3]).rjust(8)
        corp += "\n" + '-' * 30 + '\nStocul final \t\t\t {0}\n'.format(self.sold) + \
                "\nPret iesire \t\t\t {}\n".format(self.pret_iesire) + '*-* ' * 10
        print(corp)
        return corp

    def grafic(self, data1=str(datetime.now().strftime('%Y%m%d')),
               data2=str(datetime.now().strftime('%Y%m%d'))):
        """
        This method is used to create a graphic with the entry and exit of the object on stock in a set period of time.

        :param str data1: Must be a string in the format "%Y%m%d".
        The default value is set using the datetime module that must be imported beforehand;
        :param str data2: Must be a string in the format "%Y%m%d".
        The default value is set using the datetime module that must be imported beforehand;

        It prints a confirmation message and the path where the file was created using the os module. The module does
not need to be imported beforehand.
"""
        import os
        import pygal
        var_i = []
        var_e = []
        interval_data = data1.format('%Y/%m/%d') + " - " + data2.format('%Y/%m/%d')
        var_data = []
        for miscare in self.miscari:
            if data1 <= self.miscari[miscare][0] <= data2:
                var_i.append(self.miscari[miscare][1])
                var_e.append(self.miscari[miscare][2])
                var_data.append((self.miscari[miscare][0]))
        grafic = pygal.StackedBar()
        grafic.add('Intrari', var_i)
        grafic.add('Iesiri', var_e)
        grafic.x_labels = var_data
        grafic.render_to_file('Grafic {} Intrari - Iesiri {}.svg'.format(self.denp, interval_data))
        user_paths = os.getcwd()
        print("Ati creat un grafic al produsului \"{}\"  din perioada {} - {} in urmatoarea locatie:\n{}".
              format(self.denp, data1.format('%Y.%m.%d'), data2.format('%Y/%m/%d'), user_paths))

    def trimite_email_avertizare(self):
        """
        This method captures input from the user that is used to select the type of information to be send via email,
using the "smtplib" module and the email.message module. The module does not need to be imported beforehand.

        The email will be sent to the email address set when the object was created.

        Prints a message if the email was sent successfully or not.
        """
        import smtplib
        from email.message import EmailMessage

        subject = "Limita minima depasita!"
        body = """
Limita minima de {0} {1} pentru produsul {2} a fost depasita!
        
In data de {3}, a fost inregistrata o iesire de {4} {1} pentru produsul {2}, care a rezultat in depasirea \
limiteai stabilite de {0} {1}.  
        
        """.format(self.lim_min, self.um, self.denp, self.data, self.cant)

        mesaj = EmailMessage()
        mesaj.set_content("""\
From: %s
To: %s
Subject: %s
        
%s
""" % (self.expeditor, self.destinatar, subject, body))

        mesaj['Subject'] = subject
        mesaj['From'] = self.expeditor
        mesaj['To'] = self.destinatar

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(self.expeditor, self.parola)
            server.send_message(mesaj)
            server.quit()
            print("Mesaj expediat cu succes catre {}!".format(self.destinatar))
        except Exception as e:
            print("Mesajul nu a putut fi expediat!\nA aparut eroarea: {}.".format(e))

    def trimite_email_info(self):
        """
        This method captures input from the user that is used to select the type of information to be send via email,
using the "smtplib" module. The module does not need to be imported beforehand.

        The email will be sent to the email address set when the object was created.

        Prints a message if the email was sent successfully or not.
        """
        import smtplib
        from email.message import EmailMessage
        while True:
            subject = input("""
Introduceti numarul aferent informatiilor pe care doriti sa le transmiteti:
-----------------------------
1.\tFisa produsului
2.\tUltima intrare
3.\tUltima iesire
4.\tPret iesire
5.\tSoldul
6.\tLista produselor
7.\tDictionarul categoriilor
0.\tNu trimite email
-----------------------------

""")

            if subject == "1":
                subject = "Fisa produsului {}".format(self.denp)
                body = self.fisap()
                break
            elif subject == "2":
                ult_intr = 0
                canti = 0
                pret = 0
                for miscare in self.miscari:
                    if int(self.miscari[miscare][2]) == 0 and int(self.miscari[miscare][0]) > int(ult_intr):
                        ult_intr = self.miscari[miscare][0]
                        canti = self.miscari[miscare][1]
                        pret = self.miscari[miscare][3]
                if int(ult_intr) == 0:
                    subject = "Nu exista intrari pentru produsul {}".format(self.denp)
                    body = "Pentru produsul {} nu s-au gasit inregistrare intrari."
                else:
                    subject = "Ultima intrare pentru produsul {}".format(self.denp)
                    body = "Ultima intrare pentru produsul {} este de {} {} din data de {} la pretul {} LEI. "\
                        .format(self.denp, canti, self.um, ult_intr, pret)
                break
            elif subject == "3":
                ult_ie = 0
                canti = 0
                pret = 0
                for miscare in self.miscari:
                    if int(self.miscari[miscare][1]) == 0 and int(self.miscari[miscare][0]) > int(ult_ie):
                        ult_ie = self.miscari[miscare][0]
                        canti = self.miscari[miscare][2]
                        pret = self.miscari[miscare][3]
                if int(ult_ie) == 0:
                    subject = "Nu exista intrari pentru produsul {}".format(self.denp)
                    body = "Pentru produsul {} nu s-au gasit inregistrare intrari."
                else:
                    subject = "Data ultimei iesiri pentru produsul {}".format(self.denp)
                    body = "Ultima intrare pentru produsul {} este de {} {} din data de {} la pretul {} LEI. "\
                        .format(self.denp, canti, self.um, ult_ie, pret)
                break
            elif subject == "4":
                subject = "Pret iesire pentru produsul {}".format(self.pret_iesire)
                body = "Pret iesire pentru produsul {} este: {}".format(self.denp, self.pret_iesire)
                break
            elif subject == "5":
                subject = "Soldul produsului {}".format(self.sold)
                body = "Soldul produsului {} este: {}".format(self.denp, self.sold)
                break
            elif subject == "6":
                subject = "Lista produselor"
                body = ""
                for i, j in enumerate(self.lista_produse):
                    body += "\n" + str(i) + " " + str(j)
                break
            elif subject == "7":
                subject = "Dictionarul categoriilor"
                body = ""
                for i, j in self.dictionar_categorii.items():
                    body += "\n" + str(i) + " " + str(j)
                break
            elif subject == "0":
                body = ""
                break

        if subject != "0":
            mesaj = EmailMessage()
            mesaj.set_content("""\
    From: %s
    To: %s
    Subject: %s
    
    %s
    """ % (self.expeditor, self.destinatar, subject, body))

            mesaj['Subject'] = subject
            mesaj['From'] = self.expeditor
            mesaj['To'] = self.destinatar

            try:
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.ehlo()
                server.login(self.expeditor, self.parola)
                server.send_message(mesaj)
                server.quit()
                print("Mesaj expediat cu succes!")
            except:
                print("Mesajul nu a putut fi expediat!")

    def verif_tranz(self):
        """
        This function captures user input to search using the "re" module. The module does not need to be
imported beforehand.

        It will print a confirmation message if the product is on stock or not for every fount value,
with the date of the transaction
        """
        import re
        tranzactie = input("Introduceti cantitatea tranzactiei pe care o cautati:\n")
        matches = 0
        pattern = r"\b(?=\w)" + re.escape(tranzactie) + r"\b(?!\w)"
        for miscare in self.miscari:
            result_e = re.match(pattern, str(self.miscari[miscare][2]), re.I)
            result_i = re.match(pattern, str(self.miscari[miscare][1]), re.I)
            if result_i is not None:
                matches += 1
                print("Tranzactia cautata de {} a fost inregistrata in data de {}\n"
                      .format(tranzactie, self.miscari[miscare][0]))
            elif result_e is not None:
                matches += 1
                print("Tranzactia cautata de {} a fost inregistrata in data de {}\n"
                      .format(tranzactie, self.miscari[miscare][0]))
        if matches == 0:
            print("Nu s-a gasit nicio inregistrare pentru tranzactia cautata de \"{}\".".format(tranzactie))


def ver_prod():
    """
    This function captures user input to search using the "re" module. The module does not need to be imported beforehand.

    It will print the message if the product is on stock.
    """
    import re
    produs_cautat = input("Introduceti numele produsului pe care il cautati:")
    matches = 0
    pattern = r"\b(?=\w)" + re.escape(produs_cautat) + r"\b(?!\w)"
    for produs in Stoc.lista_produse:
        result = re.match(pattern, produs, re.I)
        if result is not None:
            matches += 1
    if matches > 0:
        print("Produsul cautat \"{}\", se regaseste pe stoc.".format(produs_cautat))
    else:
        print("Produsul cautat \"{}\", nu se regaseste pe stoc".format(produs_cautat))


alune = Stoc("alune", "nuci", um="kg", lim_min=5)

alune.intrari(42, 10, "19991203")
alune.iesiri(6, "20081003")
alune.iesiri(8, "20180813")
alune.intrari(3, 12, "20100122")
alune.iesiri(26, "20160222")
alune.iesiri(3, "20160820")
alune.intrari(42, 24)

alune.trimite_email_info()
alune.grafic("20080101", "20181230")
alune.verif_tranz()

prune = Stoc("prune", "fructe", um="kg", lim_min=32)
prune.intrari(512, 12, "20081003")
prune.iesiri(42)
prune.iesiri(47)

prune.grafic("20000101")

prune.trimite_email_info()
prune.verif_tranz()

ver_prod()





