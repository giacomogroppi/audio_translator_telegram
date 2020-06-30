import riconoscimento_lingua as rl
class riconoscimento():
    def __init__(self, lingua, dst):
        self.lingua = lingua
        self.lingua_possibile = None
        self.dst = dst


    def ritorno(self, dst=None):
        if dst is None:
            import sys
            sys.exit("dst is the name/path of the file, it can't be none")
        
    def lingua_possibile_funzione(self):
        """
        We pass the position of the file, and the language None
        If we want to passa a dictionary of the language, we can pass it 
        """
        self.lingua_possibile = rl.riconoscimento__init(
                                        self.dst,
                                        lingue = None 
                                        )

        if self.lingua == self.lingua_possibile:
            return True
        else:
            return self.lingua_possibile


    def stampa(self):
        return [self.lingua, self.lingua_possibile, self.dst]


if __name__ == '__main__':
    lingua = 'it-IT'
    dst = 'audio_prova.wav'
    oggetto = riconoscimento(lingua, dst)
    lingua = oggetto.lingua_possibile_funzione()
    print(lingua)