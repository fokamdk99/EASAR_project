from app.analyzer import Analyzer

def test_perform_dtw_analysis():
    analyzer = Analyzer()
    analyzer.current_pattern = 'C1.wav'
    analyzer.current_recording = 'R4.wav'
    #analyzer.analyze_stuff()
    print('jello!')

    assert 1 == 2
    #print(self.current_recording +" and "+self.current_pattern)
    #query, fs_query = librosa.load(query_path + self.current_recording)
    #template, fs_template = librosa.load(template_path + self.current_pattern)