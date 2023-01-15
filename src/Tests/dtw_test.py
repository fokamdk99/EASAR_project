from app.analyzer import Analyzer

def test_perform_dtw_analysis():
    analyzer = Analyzer()
    analyzer.current_pattern = 'R4_krotko.wav'
    analyzer.current_recording = 'R4_krociutko.wav'
    analyzer.analyze_dtw()

    assert 22 == 15