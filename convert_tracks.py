import pypianoroll as pp
import numpy as np
import os
import scipy
from matplotlib import pyplot as plt

def convert(root, filename, output_track, fileOutput):
    track = np.load(f'{root}/{filename}') # Loads track
    noteData, noteIndices, noteIndptr, noteShape = np.array([]), np.array([]), np.array([]), np.array([])
    for file in track.files: # Copies CSC representation of track.
        if file.endswith("data"):
            noteData = track[file]
        elif file.endswith("indices"):
            noteIndices = track[file]
        elif file.endswith("indptr"):
            noteIndptr = track[file]
        elif file.endswith("shape"):
            noteShape = track[file]
    if noteData is np.array([]) or noteIndices is np.array([]) or noteIndptr is np.array([]) or noteShape is np.array([]):
        return 1 # If any of these does not copy correctly, throw an error.
    matrix = scipy.sparse.csc_matrix((noteData, noteIndices, noteIndptr), shape=noteShape)
    array = matrix.toarray()
    transposeArray = array.T # Transpose pianoroll to enable us to take the highest pitch note at each timestamp.
    pianoroll = scipy.sparse.csc_matrix(transposeArray)
    noteData = pianoroll.data
    noteIndices = pianoroll.indices
    noteIndptr = pianoroll.indptr
    noteShape = pianoroll.shape
    newIndices, newData, newIndptr = np.array([]), np.array([]), np.array([0]) # Create new data for edited track.
    for i in range(1, noteIndptr.shape[0]): # Takes highest pitched note for each timestamp.
        if noteIndptr[i-1] == noteIndptr[i]:
            newIndptr = np.append(newIndptr, newIndptr[i - 1])
            continue
        else:
            newIndptr = np.append(newIndptr, newIndptr[i - 1] + 1)
            newData = np.append(newData, noteData[noteIndptr[i] - 1])
            newIndices = np.append(newIndices, noteIndices[noteIndptr[i] - 1])
    newMatrix = scipy.sparse.csc_matrix((newData, newIndices, newIndptr), shape=pianoroll.shape) # Reconverts to CSC Matrix representation.
    np.savez(f'{output_path}/{fileOutput}', newMatrix) # Saves to a file in the output folder.
    return 0


if __name__ == "__main__":
    root_dir = os.getcwd()
    folder = "piano_tracks" # Path to folder from root_dir to be looped through.
    output_path = f'{folder}/edited_piano_tracks' # Path to output folder for edited tracks.
    if not os.path.exists(f'{output_path}/'):
        os.mkdir(f'{output_path}/') # Create output folder if it doesn't yet exist.
    # Loop through all files to convert each one into a monophonic sequence.
    for root, __, files in os.walk(f'{root_dir}/{folder}'): # Loop through folder and convert each track one by one.
        for file in files:
            fileOutput = f'{file}_edited.npz'
            if convert(root, file, output_path, fileOutput):
                print("Error: The process quit because something went wrong.")
                break
    print("Finished converting files.")
