haraqat = ['ْ', 'ّ', 'ٌ', 'ٍ', 'ِ', 'ً', 'َ', 'ُ']
punctuations = ['.', '،', ':', '؛', '-', '؟']
arab_chars = 'ىعظحرسيشضق ثلصطكآماإهزءأفؤغجئدةخوبذتن'
arab_chars_no_space = 'ىعظحرسيشضقثلصطكآماإهزءأفؤغجئدةخوبذتن'
arab_chars_punctuations = arab_chars + ''.join(punctuations)
valid_arabic = haraqat + list(arab_chars)
basic_haraqat = {
    'َ': 'Fatha              ',
    'ً': 'Fathatah           ',
    'ُ': 'Damma              ',
    'ٌ': 'Dammatan           ',
    'ِ': 'Kasra              ',
    'ٍ': 'Kasratan           ',
    'ْ': 'Sukun              ',
    'ّ': 'Shaddah            ',
}
all_possible_haraqat = {'': 'No Diacritic       ',
                        'َ': 'Fatha              ',
                        'ً': 'Fathatah           ',
                        'ُ': 'Damma              ',
                        'ٌ': 'Dammatan           ',
                        'ِ': 'Kasra              ',
                        'ٍ': 'Kasratan           ',
                        'ْ': 'Sukun              ',
                        'ّ': 'Shaddah            ',
                        'َّ': 'Shaddah + Fatha    ',
                        'ًّ': 'Shaddah + Fathatah ',
                        'ُّ': 'Shaddah + Damma    ',
                        'ٌّ': 'Shaddah + Dammatan ',
                        'ِّ': 'Shaddah + Kasra    ',
                        'ٍّ': 'Shaddah + Kasratan '}
