import PlayAndSave
import DateAndCreation
import MusicInfluence

class main:
    def __init__(self):
        self.playAndSave = PlayAndSave.PlayAndSave()
        self.DateAndCreation = DateAndCreation.DateAndCreation()
        self.MusicInfluence = MusicInfluence.MusicInfluence()

    def run(self):
        self.playAndSave.run()
        self.DateAndCreation.run()
        self.MusicInfluence.run()

if __name__ == '__main__':
    main = main()
    main.run()