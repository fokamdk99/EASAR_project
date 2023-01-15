import os
from app.analyzer import Analyzer
import itertools

def test_perform1():
    recordings = os.listdir('./Recordings')
    patterns = os.listdir('./Patterns')
    list_tuple = list(itertools.product(recordings, patterns))
    analyzer = Analyzer()
    
    for item in list_tuple[0:2]:
        analyzer.current_recording = item[0]
        analyzer.current_pattern = item[1]
        analyzer.analyze_correlations()

    assert 2 == 2