import tables
import os
import hdf5_getters

def h5_reader():
    # Open and read the file
    # os_path = os.path.dirname(__file__)
    # print(os_path)
    file_path = os.path.join(os.path.dirname(__file__), 'TRAAAAW128F429D538.h5')
    print(f"Opening file at: {file_path}")

    h5 = tables.open_file(file_path, mode='r')

    # print(h5)
    # print(h5.root.metadata.artist_terms_freq[:])
    artist_terms = hdf5_getters.get_artist_terms(h5)
    artist_terms_freq = hdf5_getters.get_artist_terms_freq(h5)
    get_artist_terms_weight = hdf5_getters.get_artist_terms_weight(h5)

    print("artist_terms:", artist_terms)
    print("artist_terms_freq:", artist_terms_freq)
    print("get_artist_terms_weight:", get_artist_terms_weight)

    h5.close()

h5_reader()