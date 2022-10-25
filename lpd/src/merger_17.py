"""This script merges multitrack pianorolls to seventeen-track pianorolls.
"""
import os.path
import argparse
from pypianoroll import Multitrack, Track
from utils import make_sure_path_exists, change_prefix, findall_endswith
from config import CONFIG
if CONFIG['multicore'] > 1:
    import joblib

TRACK_INFO = (
    ('Drums', 0),
    ('Piano', 0),
    ('Chromatic Percussion', 8),
    ('Organ', 16),
    ('Guitar', 24),
    ('Bass', 32),
    ('Strings', 40),
    ('Ensemble', 48),
    ('Brass', 56),
    ('Reed', 64),
    ('Pipe', 72),
    ('Synth Lead', 80),
    ('Synth Pad', 88),
    ('Synth Effects', 96),
    ('Ethnic', 104),
    ('Percussive', 112),
    ('Sound Effects', 120),
)

def parse_args():
    """Return the parsed command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('src', help="root path to the source dataset")
    parser.add_argument('dst', help="root path to the destination dataset")
    args = parser.parse_args()
    return args.src, args.dst

def get_merged(multitrack):
    """Merge the multitrack pianorolls into sixteen instrument families and
    return the resulting multitrack pianoroll object."""
    track_lists_to_merge = [[] for _ in range(17)]
    for idx, track in enumerate(multitrack.tracks):
        if track.is_drum:
            track_lists_to_merge[0].append(idx)
        else:
            track_lists_to_merge[track.program//8 + 1].append(idx)

    tracks = []
    for idx, track_list_to_merge in enumerate(track_lists_to_merge):
        if track_list_to_merge:
            merged = multitrack[track_list_to_merge].get_merged_pianoroll('max')
            tracks.append(Track(merged, TRACK_INFO[idx][1], (idx == 0),
                                TRACK_INFO[idx][0]))
        else:
            tracks.append(Track(None, TRACK_INFO[idx][1], (idx == 0),
                                TRACK_INFO[idx][0]))
    return Multitrack(None, tracks, multitrack.tempo, multitrack.downbeat,
                      multitrack.beat_resolution, multitrack.name)

def merger(filepath, src, dst):
    """Load and merge a multitrack pianoroll and save to the given path."""
    # Load and merge the multitrack pianoroll
    multitrack = Multitrack(filepath)
    merged = get_merged(multitrack)

    # Save the merged multitrack pianoroll
    result_path = change_prefix(filepath, src, dst)
    make_sure_path_exists(os.path.dirname(result_path))
    merged.save(result_path)

def main():
    """Main function."""
    src, dst = parse_args()
    make_sure_path_exists(dst)

    if CONFIG['multicore'] > 1:
        joblib.Parallel(n_jobs=CONFIG['multicore'], verbose=5)(
            joblib.delayed(merger)(npz_path, src, dst)
            for npz_path in findall_endswith('.npz', src))
    else:
        for npz_path in findall_endswith('.npz', src):
            merger(npz_path, src, dst)

if __name__ == "__main__":
    main()
