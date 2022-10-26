import pypianoroll as pp
import os
from matplotlib import pyplot as plt

if __name__ == "__main__":
    root_dir = os.getcwd()
    folder = f'{root_dir}/lpd_5/lpd_5_cleansed/A/'
    output_audio = 'piano_audios'
    output_npz = 'piano_tracks'
    count = 0
    for root, folders, files in os.walk(folder):
        path = root
        for file in files:
            count += 1
            if file.endswith('.npz'):
                multitrack = pp.load(f'{root}/{file}')
                for track in multitrack:
                    # a midi code from 0-127 to denote what instrument to select
                    if track.pianoroll.sum() != 0 and track.name == 'Piano':
                        new_track = pp.Multitrack(tracks=[track.trim()])
                        if not os.path.exists(f'{root_dir}/{output_audio}/'):
                            os.mkdir(f'{root_dir}/{output_audio}/')
                        if not os.path.exists(f'{root_dir}/{output_npz}/'):
                            os.mkdir(f'{root_dir}/{output_npz}/')

                        pp.write(f'{root_dir}/{output_audio}/{multitrack.name}.mid', new_track)
                        pp.save(f'{root_dir}/{output_npz}/{multitrack.name}.npz', new_track)
                        # track.plot()
    # plt.show()
    print(count)
