from app.analyzer import Analyzer

def test_perform_dtw_analysis():
    analyzer = Analyzer()
    analyzer.current_pattern = 'C1.wav'
    analyzer.current_recording = 'R4.wav'
    analyzer.analyze_stuff()

    assert 22 == 15

def test_perform1():
    print('eloelo123')
    assert 2 == 2