from app.analyzer import Analyzer
import os
import itertools

def perform_dtw_analysis():
    recordings = os.listdir('./Recordings')
    patterns = os.listdir('./Patterns')
    list_tuple = list(itertools.product(recordings, patterns))
    analyzer = Analyzer()
    
    for item in list_tuple:
        analyzer.current_recording = item[0]
        analyzer.current_pattern = item[1]
        analyzer.analyze_dtw()

perform_dtw_analysis()