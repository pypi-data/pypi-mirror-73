from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag

class Car:
    def __init__(self, speed=0):
        self.speed = speed
        self.odometer = 0
        self.time = 0
        self.stemmer = PorterStemmer()
        self.lem = WordNetLemmatizer()

    def say_state(self):
        print("I'm going {} kmph!".format(self.speed))

    def accelerate(self):
        self.speed += 5

    def brake(self):
        self.speed -= 5

    def step(self):
        self.odometer += self.speed
        self.time += 1

    def average_speed(self):
        if (self.time != 0):
            return self.odometer / self.time
        else:
            pass

    def lemmatize_tokens(stentence):
        lemmatizer = WordNetLemmatizer()
        lemmatize_tokens = []
        for word, tag in pos_tag(stentence):
            if tag.startswith('NN'):
                pos = 'n'
            elif tag.startswith('VB'):
                pos = 'v'
            else:
                pos = 'a'
            lemmatize_tokens.append(lemmatizer.lemmatize(word, pos))
        return lemmatize_tokens


if __name__ == '__main__':
    my_car = Car()
    print("I'm a car!")
    my_car.say_state()
    my_car.accelerate()
    my_car.say_state()
    my_car.brake()
    my_car.say_state()
    print(word_tokenize("Hi, this is a car project."))
    print(my_car.stemmer.stem("constitutes"))
    print(my_car.lem.lemmatize("constitutes", "v"))

    sample = "Hi, this is a nice car."
    print(pos_tag(word_tokenize(sample)))

    sample1 = "Legal authority constitutes all magistrates."
    print(my_car.lemmatize_tokens(word_tokenize(sample1)))
