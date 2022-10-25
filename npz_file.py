import pypianoroll as pp
import os
from matplotlib import pyplot as plt

if __name__ == "__main__":
    folder = '/Users/jwang/MusicDiffusion/lpd/lpd_cleansed/A/A/'
    output = 'test'
    for root, folders, files in os.walk(folder):
        path = root
        for file in files:
            if file.endswith('.npz'):
                multitrack = pp.load(f'{root}/{file}')
                for track in multitrack:
                    # a midi code from 0-127 to denote what instrument to select
                    if track.pianoroll.sum() != 0:
                        new_track = pp.Multitrack(tracks=[track])
                        new_track.trim()
                        pp.write(f'/Users/jwang/MusicDiffusion/{output}/{multitrack.name}_{str(track.program)}.mid', new_track)
                        # track.plot()
    # plt.show()
