from app.analyzer import Analyzer
import os
import itertools

def perform_dtw_analysis():
    recordings = os.listdir('./Recordings')
    patterns = os.listdir('./Patterns')
    list_tuple = list(itertools.product(recordings, patterns))
    analyzer = Analyzer()

    list_tuple = [tuple for tuple in list_tuple if tuple[0] not in ('R1.wav', 'C61.wav', 'R150-1.wav')]
    
    for item in list_tuple:
        analyzer.current_recording = item[0]
        analyzer.current_pattern = item[1]
        analyzer.analyze_dtw()

perform_dtw_analysis()