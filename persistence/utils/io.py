import pickle

def save_pickle(filename: str, file_to_save) -> None:
    with open(filename, "wb") as f:
        pickle.dump(file_to_save, f)

def load_pickle(filename: str):
    with open(filename, "rb") as f:
        loaded_file = pickle.load(f)
    return loaded_file